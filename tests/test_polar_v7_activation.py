import unittest
import sys
import os
import json
from pathlib import Path

# Add _Tribunal_Inbox to sys.path
sys.path.insert(0, str(Path(r'C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox').resolve()))

from tribunal_v7_state_machine import (
    PollerState,
    TaskSpec,
    GovernanceError,
    VerificationError,
    new_receipt,
    transition,
    verify_worker_result,
    sha256_file
)
from tribunal_v7_codex_adapter import find_codex_executable, run_codex
from tribunal_v7_fable_adapter import run_fable
import job_tribunal_poller_v7 as poller

class TestPolarV7Activation(unittest.TestCase):

    def test_01_modules_and_codex_executable(self):
        self.assertIsNotNone(find_codex_executable())
        exe = find_codex_executable()
        self.assertTrue(Path(exe).is_file() or exe.endswith('.cmd'))

    def test_02_task_spec_validation_success(self):
        packet = {
            'POLLER_V7': {
                'task_id': 'TEST-POLAR-VALID-001',
                'worker': 'codex',
                'prompt': 'A valid prompt of sufficient length for test execution.',
                'working_directory': r'C:\DS All Things\DCSE_Command_Center',
                'sandbox': 'read-only',
                'timeout_seconds': 60,
                'expected_outputs': [],
                'authorization': {
                    'decision': 'GO',
                    'approved_by': 'DCS',
                    'approved_at': '2026-09-10T21:45:00Z'
                }
            }
        }
        spec = TaskSpec.from_packet(
            packet,
            Path(r'C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\test.json'),
            '0' * 64,
            [Path(r'C:\DS All Things\DCSE_Command_Center')]
        )
        self.assertEqual(spec.task_id, 'TEST-POLAR-VALID-001')
        self.assertEqual(spec.worker, 'codex')
        self.assertEqual(spec.sandbox, 'read-only')

    def test_03_failure_path_governance_rejections(self):
        # Missing decision GO
        bad_packet = {
            'POLLER_V7': {
                'task_id': 'TEST-POLAR-BAD-001',
                'worker': 'codex',
                'prompt': 'A valid prompt of sufficient length for test execution.',
                'working_directory': r'C:\DS All Things\DCSE_Command_Center',
                'sandbox': 'read-only',
                'timeout_seconds': 60,
                'expected_outputs': [],
                'authorization': {
                    'decision': 'HOLD',
                    'approved_by': 'DCS',
                    'approved_at': '2026-09-10T21:45:00Z'
                }
            }
        }
        with self.assertRaises(GovernanceError):
            TaskSpec.from_packet(
                bad_packet,
                Path(r'C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\test.json'),
                '0' * 64,
                [Path(r'C:\DS All Things\DCSE_Command_Center')]
            )

    def test_04_verification_error_on_failed_worker(self):
        spec = TaskSpec(
            task_id='TEST-SPEC-001',
            worker='fable',
            prompt='A valid prompt of sufficient length for test execution.',
            working_directory=Path(r'C:\DS All Things\DCSE_Command_Center'),
            sandbox='read-only',
            timeout_seconds=60,
            expected_outputs=(),
            approved_by='DCS',
            approved_at='2026-09-10T21:45:00Z',
            source_file=Path(r'C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox\test.json'),
            source_sha256='0' * 64
        )
        worker_result = run_fable(spec)
        with self.assertRaises(VerificationError):
            verify_worker_result(spec, worker_result)

    def test_05_idempotency_terminal_receipt(self):
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            receipt_file = Path(temp_dir) / "test.receipt.json"
            
            # Non-existent receipt -> False
            self.assertFalse(poller.terminal_receipt_exists(receipt_file, "A" * 64))
            
            # Completed receipt -> True
            receipt_file.write_text(json.dumps({"source_sha256": "A" * 64, "state": "COMPLETED"}), encoding="utf-8")
            self.assertTrue(poller.terminal_receipt_exists(receipt_file, "A" * 64))
            
            # Hash mismatch -> False
            self.assertFalse(poller.terminal_receipt_exists(receipt_file, "B" * 64))
            
            # Dry run hold in audit mode -> True when dispatch=False, False when dispatch=True
            receipt_file.write_text(json.dumps({"source_sha256": "A" * 64, "state": "AUTHORIZED", "outcome": "AUTHORIZED_DRY_RUN_HOLD"}), encoding="utf-8")
            self.assertTrue(poller.terminal_receipt_exists(receipt_file, "A" * 64, dispatch=False))
            self.assertFalse(poller.terminal_receipt_exists(receipt_file, "A" * 64, dispatch=True))

if __name__ == '__main__':
    unittest.main()
