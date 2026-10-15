#!/usr/bin/env python3
"""Offline-only research decoder and aggregate auditor. Opens files, never a CAN socket.

The bundled JSON maps carry confidence and source information. A decoded value is
not permission to replace a factory instrument, issue vehicle commands, or infer
physical units for a raw/candidate field. Audit output excludes absolute times,
paths, odometer values and payloads; source captures remain private.
"""
from __future__ import annotations
import argparse
from collections import Counter
from functools import lru_cache
import json
import math
from pathlib import Path
import re
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
YEARS = (2003, 2007)
PACKED = re.compile(r'^\s*(?:\((\d+(?:\.\d+)?)\)\s+)?\S+\s+([0-9A-Fa-f]{3})#([0-9A-Fa-f]{16})\s*$')
SPACED = re.compile(r'^\s*(?:\((\d+(?:\.\d+)?)\)\s+)?\S+\s+([0-9A-Fa-f]{3})\s+\[8\]\s+((?:[0-9A-Fa-f]{2}\s+){7}[0-9A-Fa-f]{2})\s*$')

@lru_cache(maxsize=2)
def load_map(year: int) -> dict[str, Any]:
    if year not in YEARS:
        raise ValueError('Only the separately documented 2003 and 2007 profiles are supported.')
    return json.loads((ROOT / f'data/accord_{year}.json').read_text(encoding='utf-8'))

@lru_cache(maxsize=2)
def frame_ids(year: int) -> frozenset[int]:
    return frozenset(int(m['can_id'],16) for m in load_map(year)['messages'])

@lru_cache(maxsize=2)
def checksum_ids(year: int) -> frozenset[int]:
    return frozenset(int(i,16) for i in load_map(year)['checksum_ids'])

def _frame(year: int, can_id: int, payload: bytes) -> None:
    if can_id not in frame_ids(year):
        raise ValueError('Identifier is not in the selected observed-vehicle profile.')
    if not isinstance(payload, bytes) or len(payload) != 8:
        raise ValueError('Expected exactly eight payload bytes from a standard Classical CAN frame.')

def checksum_valid(year: int, can_id: int, payload: bytes) -> bool | None:
    """True/False for applicable messages; None means this rule is not applicable."""
    _frame(year,can_id,payload)
    if can_id not in checksum_ids(year):
        return None
    return sum((b >> 4) + (b & 15) for b in payload) % 16 == 0

def parse_line(line: str) -> tuple[float | None, int, bytes] | None:
    """Accept common eight-byte standard candump compact and spaced text forms.

    A None result is an unparsed/unsupported line, not an error frame silently
    interpreted as valid data. No CAN FD, RTR, extended IDs or truncated data.
    """
    match = PACKED.fullmatch(line) or SPACED.fullmatch(line)
    if match is None:
        return None
    timestamp = float(match[1]) if match[1] else None
    cid = int(match[2],16)
    if cid > 0x7FF or (timestamp is not None and not math.isfinite(timestamp)):
        return None
    return timestamp,cid,bytes.fromhex(match[3])

@lru_cache(maxsize=32)
def _signals(year: int, can_id: int) -> tuple[dict[str,Any], ...]:
    return tuple(s for s in load_map(year)['signals'] if int(s['can_id'],16)==can_id)

def decode(year: int, can_id: int, payload: bytes, *, validate: bool=True,
           include_raw: bool=False) -> dict[str,int | float]:
    """Decode numeric values, retaining candidate names; no cross-frame state.

    include_raw includes unmapped regions and protocol fields. It does not make
    unknown fields physical sensors. This function does not freshness-gate data;
    callers must preserve source age. validate=False is for inspected test data.
    """
    _frame(year,can_id,payload)
    if validate and checksum_valid(year,can_id,payload) is False:
        raise ValueError('Payload checksum failed; decoded values are not returned.')
    result: dict[str,int | float] = {}
    for row in _signals(year,can_id):
        if not include_raw and row['kind'] != 'signal':
            continue
        byte,bit,width=row['byte'],row['bit'],row['width']
        if width>8:
            raw=int.from_bytes(payload[byte:byte+width//8],'big')
        else:
            raw=(payload[byte]>>bit)&((1<<width)-1)
        result[row['name']]=raw*row['scale']+row['offset']
    return result

def counter_delta(previous: int, current: int, modulus: int, *,
                  continuous: bool, maximum_delta: int) -> int | None:
    """Bounded modulo delta only when caller independently establishes continuity.

    A modulo delta alone cannot distinguish every reset from rollover. A short
    reset can pass a numerical bound; the caller must invalidate its baseline on
    ignition/module resets, missing coverage or other discontinuities. The bound
    is application-selected, not a Honda constant. None must stay unavailable.
    """
    if not all(isinstance(x,int) for x in (previous,current,modulus,maximum_delta)):
        raise ValueError('Counter arguments must be integers.')
    if modulus<=0 or not 0<=previous<modulus or not 0<=current<modulus or not 0<=maximum_delta<modulus:
        raise ValueError('Invalid counter value, modulus or bound.')
    if not continuous:
        return None
    delta=(current-previous)%modulus
    return delta if delta<=maximum_delta else None

def _nonnegative(value: float, name: str) -> None:
    if not math.isfinite(value) or value<0:
        raise ValueError(f'{name} must be finite and nonnegative.')

def fuel_ml(delta: int, ml_per_normalized_count: float, *, normalized: bool) -> float:
    """Apply an explicitly supplied calibration, never a hidden default scale."""
    _nonnegative(delta,'delta')
    _nonnegative(ml_per_normalized_count,'calibration')
    return delta*ml_per_normalized_count*(1.0 if normalized else 0.5)

def distance_m(year: int, delta_ticks: int) -> float:
    """2003 historical approximate scale or 2007 odometer-relative scale."""
    _nonnegative(delta_ticks,'delta_ticks')
    return delta_ticks*load_map(year)['derived']['distance_m_per_tick']['value']

def odometer_miles(raw: int) -> float:
    """Later maintainer-confirmed display convention, not a true-kilometer claim."""
    if not isinstance(raw,int) or not 0<=raw<2**24:
        raise ValueError('Expected unsigned 24-bit raw odometer.')
    return raw/1.61

def fresh_bool(value: int | None, *, age: float, max_age: float) -> bool | None:
    """Preserve unknown separately from a fresh deasserted state."""
    _nonnegative(age,'age'); _nonnegative(max_age,'max_age')
    if value is None or age>max_age:
        return None
    return bool(value)

def throttle_percent(raw_b3: int) -> dict[str,float]:
    """2007 empirical OBD-equivalent B3 fits; no extrapolation beyond tested range."""
    if not isinstance(raw_b3,int) or not 8<=raw_b3<=208:
        raise ValueError('B3 is outside the empirically tested integer range 8..208.')
    return {'relative_obd_equivalent':0.0980247+0.4449886*raw_b3,
            'absolute_obd_equivalent':11.541592+0.3221345*raw_b3}

def audit(path: Path, year: int) -> dict[str,Any]:
    """Recount messages and integrity without exporting identifying payloads.

    Includes time-span and interval aggregates only. Counter discontinuities and
    time gaps are separate, potentially overlapping indicators, not dropped-frame
    estimates. No fuel or odometer accumulation across gaps is attempted.
    """
    ids=frame_ids(year)
    rate={int(m['can_id'],16):m['rate_hz'] for m in load_map(year)['messages']}
    count=Counter();failed=Counter();gaps=Counter();counter_breaks=Counter()
    previous={};first=None;last=None
    lines=unparsed=unsupported=applicable=0
    for line in path.open(encoding='utf-8'):
        lines+=1
        parsed=parse_line(line.rstrip('\r\n'))
        if parsed is None:
            unparsed+=1;continue
        timestamp,cid,payload=parsed
        if cid not in ids:
            unsupported+=1;continue
        count[cid]+=1
        valid=checksum_valid(year,cid,payload)
        if valid is not None:
            applicable+=1
            if not valid: failed[cid]+=1
        if timestamp is not None:
            if first is None: first=timestamp
            last=timestamp
        ctr=(payload[7]>>6)&3
        if cid in previous:
            old_t,old_ctr=previous[cid]
            if ctr != (old_ctr+1)%4: counter_breaks[cid]+=1
            if timestamp is not None and old_t is not None:
                dt=timestamp-old_t
                if dt<0 or dt>max(0.5,8/rate[cid]): gaps[cid]+=1
        previous[cid]=(timestamp,ctr)
    return {'year':year,'input_lines':lines,'parsed_known_frames':sum(count.values()),
            'unparsed_or_unsupported_format_lines':unparsed,'unknown_identifier_frames':unsupported,
            'duration_seconds':round(last-first,6) if first is not None and last is not None else None,
            'checksum_applicable':applicable,'checksum_pass':applicable-sum(failed.values()),
            'checksum_fail':sum(failed.values()),'checksum_not_applicable':sum(count.values())-applicable,
            'per_id':{f'0x{i:03X}':{'frames':count[i],'checksum_fail':failed[i],
               'counter_discontinuities':counter_breaks[i],'large_or_backward_time_gaps':gaps[i]}
               for i in sorted(count)},
            'privacy':'No path, absolute time, payload, odometer reading or source hash in this output.',
            'limitations':'Unparsed lines are counted. Counter discontinuities are not exact losses. Gap threshold=max(0.5 s, 8 nominal periods).'}

def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    a=sub.add_parser('audit',help='Aggregate a private local candump text file.')
    a.add_argument('--year',type=int,choices=YEARS,required=True)
    a.add_argument('path',type=Path)
    d=sub.add_parser('decode',help='Decode one user-supplied frame; output can contain private values.')
    d.add_argument('--year',type=int,choices=YEARS,required=True)
    d.add_argument('--id',required=True,help='Hex standard CAN ID, for example 12C')
    d.add_argument('--data',required=True,help='Sixteen hexadecimal payload digits')
    d.add_argument('--include-raw',action='store_true')
    args=parser.parse_args()
    try:
        result=audit(args.path,args.year) if args.command=='audit' else decode(args.year,int(args.id,16),bytes.fromhex(args.data),include_raw=args.include_raw)
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print(f'Input rejected: {exc}',file=sys.stderr)
        return 2
    print(json.dumps(result,indent=2,allow_nan=False))
    return 1 if args.command=='audit' and (result['checksum_fail'] or result['unparsed_or_unsupported_format_lines'] or result['unknown_identifier_frames']) else 0

if __name__=='__main__':
    raise SystemExit(main())
