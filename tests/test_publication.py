"""Layout checks, public evidence checks and optional external DBC qualification."""
from pathlib import Path
import csv
import importlib.util
import json
import math
import random
import re
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import accord_can as can

DBC_ROW=re.compile(r'^\s*SG_ (\w+) : (\d+)\|(\d+)@([01])\+ \(([-+\d.eE]+),([-+\d.eE]+)\) \[[-+\d.eE]+\|[-+\d.eE]+\] "[^"]*" Research$')

def parse_dbc(path):
    messages={};current=None
    for line in path.read_text().splitlines():
        if line.startswith('BO_ '):
            fields=line.split();current=int(fields[1]);messages[current]=[]
            if fields[3]!='8':raise ValueError('Unexpected DLC')
        elif line.lstrip().startswith('SG_ '):
            match=DBC_ROW.fullmatch(line)
            if not match:raise ValueError(f'Unparsed signal declaration: {line}')
            name,start,width,order,scale,offset=match.groups()
            messages[current].append((name,int(start),int(width),int(order),float(scale),float(offset)))
    return messages

def dbc_bits(start,width,order):
    if order==1:return list(range(start,start+width))
    bits=[];pos=start
    for _ in range(width):
        bits.append(pos);pos=pos+15 if pos%8==0 else pos-1
    return bits

def extract_dbc(payload,row):
    _,start,width,order,scale,offset=row
    positions=dbc_bits(start,width,order)
    if order==1:
        raw=sum(((payload[p//8]>>(p%8))&1)<<i for i,p in enumerate(positions))
    else:
        raw=0
        for p in positions:raw=(raw<<1)|((payload[p//8]>>(p%8))&1)
    return raw*scale+offset

class TestPublication(unittest.TestCase):
    def test_json_and_csv_agree(self):
        for year in can.YEARS:
            source=can.load_map(year)['signals']
            with (ROOT/f'data/accord_{year}_signals.csv').open() as f: rows=list(csv.DictReader(f))
            self.assertEqual(len(source),len(rows))
            for a,b in zip(source,rows):
                self.assertEqual(a['name'],b['name'])
                self.assertEqual(a['can_id'],b['can_id'])
                self.assertEqual(a['width'],int(b['width']))
                self.assertEqual(a['scale'],float(b['scale']))
                self.assertEqual(a['choices'],json.loads(b['choices']))

    def test_dbc_every_bit_covered_once(self):
        for year in can.YEARS:
            messages=parse_dbc(ROOT/f'dbc/accord_{year}_research.dbc')
            self.assertEqual(set(messages),set(can.frame_ids(year)))
            for cid,rows in messages.items():
                bits=[bit for row in rows for bit in dbc_bits(row[1],row[2],row[3])]
                self.assertEqual(sorted(bits),list(range(64)),f'{year}:{cid:03X}')
                self.assertEqual(len({r[0] for r in rows}),len(rows))

    def test_dbc_synthetic_values_match_json_decoder(self):
        rng=random.Random(2026)
        for year in can.YEARS:
            messages=parse_dbc(ROOT/f'dbc/accord_{year}_research.dbc')
            for cid,rows in messages.items():
                for _ in range(256):
                    payload=bytes(rng.randrange(256) for _ in range(8))
                    actual=can.decode(year,cid,payload,validate=False,include_raw=True)
                    self.assertEqual(set(actual),{r[0] for r in rows})
                    for row in rows:
                        self.assertAlmostEqual(actual[row[0]],extract_dbc(payload,row),places=8)

    def test_source_tags_are_documented(self):
        text=(ROOT/'docs/provenance.md').read_text()
        for year in can.YEARS:
            for row in can.load_map(year)['signals']:
                self.assertIn(row['source'],text)

    def test_current_markdown_local_links_resolve(self):
        documents=list(ROOT.glob('*.md'))+list((ROOT/'docs').glob('*.md'))
        for path in documents:
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',path.read_text()):
                if target.startswith(('http:','https:','mailto:','#')):continue
                target=target.split('#')[0]
                self.assertTrue((path.parent/target).exists(),f'{path.name}: {target}')

    def test_all_fifteen_remaining_groups_retained(self):
        data=json.loads((ROOT/'data/remaining_signals.json').read_text())
        self.assertEqual([r['id'] for r in data['groups']],[f'R{i:02d}' for i in range(1,16)])
        for row in data['groups']:
            for key in ('status','evidence','limits','next_reference'):self.assertTrue(row[key])

    def test_all_original_2003_signal_rows_retained(self):
        with (ROOT/'archive/2003/workbook/signal-map.csv').open() as f:rows=list(csv.reader(f))
        self.assertEqual(len(rows),47)
        self.assertEqual(rows[0][0],'CAN ID')

    def test_fresh_raw_audit_totals_are_consistent(self):
        data=json.loads((ROOT/'evidence/independent_raw_audit.json').read_text())
        totals=data['totals']
        self.assertEqual(totals['parsed_known_frames'],1449999)
        self.assertEqual(totals['checksum_pass'],1389504)
        self.assertEqual(totals['checksum_not_applicable'],60495)
        self.assertEqual(totals['checksum_fail'],0)
        self.assertEqual(sum(x['parsed_known_frames'] for x in data['recordings'].values()),totals['parsed_known_frames'])
        focused=json.loads((ROOT/'evidence/independent_224_audit.json').read_text())
        self.assertEqual(focused['total_packets'],12113)
        self.assertTrue(focused['all_checksums_pass'])

    def test_published_stationary_reference_regression(self):
        with (ROOT/'evidence/throttle-reference-pairs.csv').open() as f: rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),123)
        for pid,n,expected_slope,expected_intercept in [('11',53,.3221345270555997,11.541592179996403),('45',51,.44498864457871,.09802469881729964)]:
            selected=[r for r in rows if r['pid']==pid and r['stable']=='True']
            self.assertEqual(len(selected),n)
            x=[int(r['B3']) for r in selected];y=[float(r['obd_percent']) for r in selected]
            xm=sum(x)/n;ym=sum(y)/n
            slope=sum((a-xm)*(b-ym) for a,b in zip(x,y))/sum((a-xm)**2 for a in x)
            self.assertAlmostEqual(slope,expected_slope,places=7)
            self.assertAlmostEqual(ym-slope*xm,expected_intercept,places=6)

    def test_odometer_slots_redacted_in_historical_masks(self):
        with (ROOT/'evidence/historical-v05-byte-masks.csv').open() as f:rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),80)
        for row in rows:
            if row['can_id']=='0x1F4' and int(row['byte_index']) in (3,4,5):
                self.assertTrue(all(v=='WITHHELD_ABSOLUTE_ODOMETER_SLOT' for k,v in row.items() if k not in ('can_id','byte_index')))

    @unittest.skipUnless(importlib.util.find_spec('cantools'),'Optional third-party cantools importer is not installed')
    def test_external_cantools_strict_import(self):
        import cantools
        for year in can.YEARS:
            database=cantools.database.load_file(str(ROOT/f'dbc/accord_{year}_research.dbc'),strict=True)
            self.assertEqual(len(database.messages),len(can.frame_ids(year)))
            rng=random.Random(2026+year)
            for msg in database.messages:
                payloads=[bytes(8),bytes([255])*8,bytes.fromhex('0123456789ABCDEF')]
                payloads.extend(bytes(rng.randrange(256) for _ in range(8)) for _ in range(256))
                for payload in payloads:
                    external=msg.decode(payload,decode_choices=False)
                    local=can.decode(year,msg.frame_id,payload,validate=False,include_raw=True)
                    self.assertEqual(set(external),set(local))
                    for name in external:self.assertAlmostEqual(external[name],local[name],places=8)

if __name__=='__main__':unittest.main()
