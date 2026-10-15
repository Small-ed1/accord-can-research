"""Auditor and command-line contracts using synthetic frames only."""
from pathlib import Path
import json
import io
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import accord_can as can


def frame(counter=0, *, corrupt=False):
    payload = bytearray.fromhex('805A00000BB81000')
    payload[7] = counter << 6
    payload[7] |= -sum((b >> 4) + (b & 15) for b in payload) & 15
    if corrupt:
        payload[0] ^= 1
    return payload.hex().upper()


class TestAuditCLI(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'private-source.log'

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(ROOT / 'tools/accord_can.py'), *args],
            text=True, capture_output=True, check=False,
        )

    def test_audit_aggregates_failures_counters_and_time_gaps(self):
        self.path.write_text('\n'.join([
            f'(1234567890.000) can0 12C#{frame(0)}',
            f'(1234567890.010) can0 12C#{frame(1)}',
            f'(1234567891.000) can0 12C#{frame(3, corrupt=True)}',
            f'(1234567890.500) can0 12C#{frame(0)}',
            '(1234567891.010) can0 1F4#0000000000000000',
            '(1234567891.020) can0 777#0000000000000000',
            'unsupported input',
        ]) + '\n', encoding='utf-8')
        result = can.audit(self.path, 2007)
        self.assertEqual(result['input_lines'], 7)
        self.assertEqual(result['parsed_known_frames'], 5)
        self.assertEqual(result['checksum_applicable'], 4)
        self.assertEqual(result['checksum_pass'], 3)
        self.assertEqual(result['checksum_fail'], 1)
        self.assertEqual(result['checksum_not_applicable'], 1)
        self.assertEqual(result['unknown_identifier_frames'], 1)
        self.assertEqual(result['unparsed_or_unsupported_format_lines'], 1)
        self.assertAlmostEqual(result['duration_seconds'], 1.01)
        self.assertEqual(result['per_id']['0x12C']['counter_discontinuities'], 1)
        self.assertEqual(result['per_id']['0x12C']['large_or_backward_time_gaps'], 2)
        serialized = json.dumps(result)
        for private in (str(self.path), self.path.name, '1234567890', frame(0)):
            self.assertNotIn(private, serialized)

    def test_audit_preserves_year_specific_checksum_exemptions(self):
        self.path.write_text('can0 0C8#0100000000000000\n', encoding='utf-8')
        old = can.audit(self.path, 2003)
        new = can.audit(self.path, 2007)
        self.assertEqual(old['checksum_not_applicable'], 1)
        self.assertEqual(old['checksum_fail'], 0)
        self.assertEqual(new['checksum_fail'], 1)
        self.assertIsNone(old['duration_seconds'])

    def test_audit_closes_its_input_stream(self):
        can.load_map(2007)
        source = io.StringIO(f'can0 12C#{frame()}\n')
        with patch.object(Path, 'open', return_value=source):
            can.audit(self.path, 2007)
        self.assertTrue(source.closed)

    def test_audit_cli_valid_input_returns_json_and_success(self):
        self.path.write_text(f'can0 12C#{frame()}\n', encoding='utf-8')
        result = self.run_cli('audit', '--year', '2007', str(self.path))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['parsed_known_frames'], 1)
        self.assertEqual(result.stderr, '')

    def test_audit_cli_empty_input_cannot_report_success(self):
        self.path.write_text('', encoding='utf-8')
        result = self.run_cli('audit', '--year', '2007', str(self.path))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['parsed_known_frames'], 0)

    def test_audit_cli_rejected_records_return_failure(self):
        for line in ('junk', 'can0 777#0000000000000000',
                     f'can0 12C#{frame(corrupt=True)}'):
            with self.subTest(line=line):
                self.path.write_text(line + '\n', encoding='utf-8')
                result = self.run_cli('audit', '--year', '2007', str(self.path))
                self.assertEqual(result.returncode, 1)
                json.loads(result.stdout)

    def test_cli_invalid_input_returns_error_without_traceback(self):
        self.path.write_bytes(b'\xff\xfe')
        cases = [
            ('audit', '--year', '2007', str(self.path)),
            ('audit', '--year', '2007', str(self.path.with_name('missing.log'))),
            ('decode', '--year', '2007', '--id', '12C', '--data', 'bad'),
            ('decode', '--year', '2007', '--id', '777', '--data', frame()),
        ]
        for args in cases:
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, '')
                self.assertIn('Input rejected:', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_decode_cli_synthetic_example(self):
        result = self.run_cli('decode', '--year', '2007', '--id', '12C',
                              '--data', '805A00000BB810CE')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['EngineRPM'], 3000)


if __name__ == '__main__':
    unittest.main()
