# Wire conventions and integrity

## Frame scope

Both research profiles use 500 kbit/s Classical CAN with standard 11-bit identifiers and eight-byte payloads. The inventory is the IDs actually observed, not every identifier that might exist on a different engine, transmission, market, option package, network segment or diagnostic session. Physical sender assignments in old reports are hypotheses unless separately supported.

`B0` is the first byte. Bit 0 is its least significant bit. `BE16(Ba,Bb)=256*Ba+Bb`; `BE24(Ba,Bb,Bc)=65536*Ba+256*Bb+Bc`. Fields spanning bytes are big-endian unless explicitly stated. Single-byte bit masks are ordinary least-significant-bit numbering.

The DBCs use Motorola ordering for multi-byte words and Intel ordering for single-byte bitfields. For a big-endian field beginning at B4, the DBC start is 39, not 32; a 16-bit width then covers B4 and B5. The JSON keeps byte/bit/width explicit so users need not infer DBC sawtooth numbering.

## Two-bit rolling sequence

All observed messages have `counter=(B7>>6)&3`, independently advancing modulo four per identifier. Track each ID independently. This is a frame sequence indicator, not a timestamp, clock, mileage counter or sensor reading. A discontinuity may reflect missing packets, startup or a recording boundary. Missing a multiple of four frames can escape the sequence check; a passing sequence alone is not proof of complete coverage.

## Nibble-sum checksum

The applicable messages store the checksum in `B7 & 0x0F`:

```python
expected = (-sum((b >> 4) + (b & 0x0F) for b in payload[:7])
            - (payload[7] >> 4)) & 0x0F
valid = expected == (payload[7] & 0x0F)
```

Equivalently, the sum of all sixteen payload nibbles is zero modulo sixteen. There is **no CAN-ID contribution in this empirically validated rule**. The complete upper nibble of B7 participates, not just the rolling counter.

| Profile | Apply checksum to | Do not apply this rule to |
|---|---|---|
| 2003 | `0D4`, `12C`, `188`, `224` | `0C8`, `1F4` |
| 2007 | `0A6`, `0C8`, `0D4`, `12C`, `188`, `20C`, `224`, `2E4`, `405` | `1F4` |

The low B7 bits in the historical 2003 `0C8` and `1F4` data were observed as zero. The 2007 `0C8` behavior differs. A coincidental nibble-sum pass for a non-applicable frame is not evidence that it uses the checksum.

A valid nibble sum detects some corruptions, not all errors or spoofing. It is not authentication. The DBC does not perform validation: the offline decoder does, rejecting applicable failures by default.

## Continuity and freshness

Distance and fuel deltas may be unwrapped only within continuous coverage with a valid baseline. A restart/reset is not a rollover. Reject implausible deltas, use message ages, and invalidate baselines on gaps, reinitialization or uncertain timing. Modulo arithmetic cannot distinguish every reset by itself; even a small reset can fit a rate bound.

Carry three logical states into displays: fresh asserted, fresh clear, and unknown/stale. This is especially important for warning lamps, doors, seatbelts and ON-associated status. The normal 300 ms `405` period also means it cannot be judged by the same freshness threshold as a 10 ms RPM message.

The included auditor reports large/backward time gaps separately from sequence discontinuities, using a documented screening threshold of the larger of 0.5 s and eight nominal periods. That threshold is a publication audit policy, not a Honda sleep or failure specification.

## Network handling

Capture only with correctly configured listen-only hardware and appropriate electrical protection. Do not add another terminator to an already correctly terminated vehicle bus. Preserve factory safety systems and the OEM instrument cluster. This publication intentionally does not supply unverified wire-color/pinout instructions or a transmit interface.

Linux SocketCAN documents CAN interfaces and their listen-only configuration: https://docs.kernel.org/networking/can.html . The candump text format accepted here is a deliberately restricted subset: standard eight-byte compact or spaced records; unparsed records are reported, not silently decoded.
