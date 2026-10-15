"""Synthetic regression vectors. No captured trip or vehicle identity is embedded."""
import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
SPEC = importlib.util.find_spec('accord_can')
if SPEC:
    import accord_can as can

class TestImplementationPresent(unittest.TestCase):
    def test_offline_decoder_is_present(self):
        self.assertIsNotNone(SPEC, 'The offline CAN decoder has not been implemented.')

@unittest.skipUnless(SPEC, 'Implementation is not present yet')
class TestDecoder(unittest.TestCase):
    def test_checksum_year_boundary(self):
        bad = bytes.fromhex('0100000000000000')
        self.assertIsNone(can.checksum_valid(2003, 0x0C8, bad))
        self.assertFalse(can.checksum_valid(2007, 0x0C8, bad))
        for y in (2003, 2007):
            self.assertIsNone(can.checksum_valid(y, 0x1F4, bad))

    def test_checksum_vector_and_corruption(self):
        p = bytes.fromhex('805A00000BB810CE')
        # Nibble sum is a multiple of sixteen in this synthetic vector.
        self.assertTrue(can.checksum_valid(2007, 0x12C, p))
        self.assertFalse(can.checksum_valid(2007, 0x12C, bytes([p[0]^1])+p[1:]))

    def test_rpm_and_temperature_without_obd_divide(self):
        p = bytes.fromhex('805A00000BB810CE')
        x = can.decode(2007, 0x12C, p)
        self.assertEqual(x['EngineRPM'], 3000)
        self.assertEqual(x['CoolantTemperature'], 88)
        self.assertEqual(x['IntakeAirTemperature'], 50)
        self.assertEqual(x['MILStatus'], 1)

    def test_bad_checksum_rejected_by_decoder(self):
        with self.assertRaises(ValueError):
            can.decode(2007, 0x12C, bytes.fromhex('0100000000000000'))

    def test_unsupported_year_and_frame(self):
        for year, cid in [(2004,0x12C),(2003,0x0A6),(2007,0x777)]:
            with self.assertRaises(ValueError):
                can.decode(year,cid,bytes(8))
        with self.assertRaises(ValueError):
            can.decode(2007,0x12C,bytes(7))

    def test_candump_parser_both_formats(self):
        a=can.parse_line('(0.012345) can0 12C#805A00000BB810CE')
        b=can.parse_line('can0 12C [8] 80 5A 00 00 0B B8 10 CE')
        self.assertEqual(a[1:], b[1:])
        self.assertEqual(a[0],0.012345)
        self.assertIsNone(b[0])
        for line in ['junk','(0.0) can0 12C#00','(0.0) can0 12C##10000000000000000']:
            self.assertIsNone(can.parse_line(line))

    def test_gear_six_and_seven_are_distinct(self):
        for gear in (6,7):
            p=bytes([gear,6,0,2,0,0,14,0])
            x=can.decode(2007,0x188,p,validate=False)
            self.assertEqual(x['ReportedGear'],gear)
            self.assertEqual(x['SelectorCode'],2)

    def test_cruise_not_backported_to_2003(self):
        p=bytes.fromhex('805A00000BB80800')
        self.assertNotIn('CruiseEngaged', can.decode(2003,0x12C,p,validate=False))
        self.assertEqual(can.decode(2007,0x12C,p,validate=False)['CruiseEngaged'],1)

    def test_dimmer_split_and_legacy_raw(self):
        p=bytes.fromhex('04E4000000000000')
        x=can.decode(2007,0x1F4,p)
        self.assertEqual(x['DimmerLevelCode'],100)
        self.assertEqual(x['DimmerOverrideCandidate'],1)
        self.assertEqual(can.decode(2003,0x1F4,p)['DimmerRaw'],228)

    def test_counter_continuity_contract(self):
        self.assertEqual(can.counter_delta(254,1,256,continuous=True,maximum_delta=4),3)
        self.assertIsNone(can.counter_delta(254,1,256,continuous=False,maximum_delta=4))
        self.assertIsNone(can.counter_delta(1000,0,65536,continuous=True,maximum_delta=500))
        self.assertEqual(can.counter_delta(65534,2,65536,continuous=True,maximum_delta=10),4)
        with self.assertRaises(ValueError):
            can.counter_delta(0,256,256,continuous=True,maximum_delta=4)

    def test_raw_normalized_fuel_convention(self):
        self.assertAlmostEqual(can.fuel_ml(20,0.21117,normalized=False),2.1117)
        self.assertAlmostEqual(can.fuel_ml(10,0.21117,normalized=True),2.1117)
        with self.assertRaises(ValueError):
            can.fuel_ml(-1,0.21117,normalized=False)

    def test_year_specific_distance_and_odometer(self):
        self.assertAlmostEqual(can.distance_m(2007,164),1609.344)
        self.assertAlmostEqual(can.distance_m(2003,200),2000.0)
        self.assertAlmostEqual(can.odometer_miles(161000),100000.0)

    def test_freshness_has_unknown_state(self):
        self.assertIsNone(can.fresh_bool(0,age=2,max_age=0.5))
        self.assertIsNone(can.fresh_bool(None,age=0,max_age=0.5))
        self.assertFalse(can.fresh_bool(0,age=0.1,max_age=0.5))
        self.assertTrue(can.fresh_bool(1,age=0.1,max_age=0.5))

    def test_throttle_feedback_is_only_derived_from_b3(self):
        x=can.throttle_percent(100)
        self.assertAlmostEqual(x['relative_obd_equivalent'],44.5968847)
        self.assertAlmostEqual(x['absolute_obd_equivalent'],43.755042)
        self.assertNotIn('pedal_percent',x)
        with self.assertRaises(ValueError):
            can.throttle_percent(0)

if __name__=='__main__':
    unittest.main()
