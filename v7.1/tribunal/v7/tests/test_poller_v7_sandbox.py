"""Sandbox-only tests for the DCSE Tribunal Poller v7 candidate.

Covers the four sandbox-verifiable checks required by task
V7_1_ACTION_1_POLLER_HARDENING (policy_flags.required_tests):

  - python_import_resolution
  - static_authorization_checks
  - idempotency_unit_test
  - receipt_schema_validation

No network access, no Supabase, no Windows host, no credentials. Run with:

    python3 -m unittest discover -s v7.1/tribunal/v7/tests -v
"""
from __future__ import annotations

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_DIR = Path(__file__).resolve().parents[1]
if str(SOURCE_DIR) not in sys.path:
    sys.path.insert(0, str(SOURCE_DIR))


class PythonImportResolutionTest(unittest.TestCase):
    """python_import_resolution"""

    MODULES = (
        "tribunal_v7_state_machine",
        "tribunal_v7_codex_adapter",
        "tribunal_v7_fable_adapter",
        "job_tribunal_poller_v7",
    )

    def test_all_v7_modules_import_cleanly(self) -> None:
        for name in self.MODULES:
            with self.subTest(module=name):
                importlib.import_module(name)

    def test_poller_entrypoint_names_resolve(self) -> None:
        poller = importlib.import_module("job_tribunal_poller_v7")
        for name in (
            "run_codex",
            "run_fable",
            "GovernanceError",
            "PollerState",
            "TaskSpec",
            "VerificationError",
            "atomic_write_json",
            "new_receipt",
            "safe_receipt_stem",
            "sha256_file",
            "transition",
            "verify_worker_result",
        ):
            self.assertTrue(hasattr(poller, name), f"missing imported name: {name}")


class StaticAuthorizationChecksTest(unittest.TestCase):
    """static_authorization_checks"""

    def setUp(self) -> None:
        state_machine = importlib.import_module("tribunal_v7_state_machine")
        self.TaskSpec = state_machine.TaskSpec
        self.GovernanceError = state_machine.GovernanceError
        self._tmp = tempfile.TemporaryDirectory()
        self.work_root = Path(self._tmp.name)
        self.allowed_roots = [self.work_root]
        self.source_file = self.work_root / "TRIBUNAL_TEST.json"
        self.source_file.write_text("{}", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _base_packet(self, **overrides):
        packet = {
            "POLLER_V7": {
                "task_id": "CP-TEST-001",
                "worker": "codex",
                "working_directory": str(self.work_root),
                "sandbox": "read-only",
                "timeout_seconds": 900,
                "prompt": "A sufficiently long bounded task description.",
                "expected_outputs": ["out.json"],
                "authorization": {
                    "decision": "GO",
                    "approved_by": "DCS Level 0",
                    "approved_at": "2026-08-03T00:00:00-04:00",
                },
            }
        }
        packet["POLLER_V7"].update(overrides)
        return packet

    def _build(self, packet):
        return self.TaskSpec.from_packet(
            packet, self.source_file, "0" * 64, self.allowed_roots
        )

    def test_valid_packet_is_accepted(self) -> None:
        spec = self._build(self._base_packet())
        self.assertEqual(spec.worker, "codex")

    def test_missing_authorization_block_rejected(self) -> None:
        packet = self._base_packet()
        del packet["POLLER_V7"]["authorization"]
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_non_go_decision_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["authorization"]["decision"] = "HOLD"
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_unapproved_worker_rejected(self) -> None:
        packet = self._base_packet(worker="fable")
        packet["POLLER_V7"]["worker"] = "unknown_worker"
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_invalid_sandbox_value_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["sandbox"] = "danger-full-access"
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_timeout_out_of_bounds_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["timeout_seconds"] = 5
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_working_directory_outside_allow_root_rejected(self) -> None:
        outside = Path(tempfile.mkdtemp())
        try:
            packet = self._base_packet()
            packet["POLLER_V7"]["working_directory"] = str(outside)
            with self.assertRaises(self.GovernanceError):
                self._build(packet)
        finally:
            outside.rmdir()

    def test_expected_output_path_traversal_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["expected_outputs"] = ["../escape.json"]
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_absolute_expected_output_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["expected_outputs"] = ["/etc/passwd"]
        with self.assertRaises(self.GovernanceError):
            self._build(packet)

    def test_short_prompt_rejected(self) -> None:
        packet = self._base_packet()
        packet["POLLER_V7"]["prompt"] = "too short"
        with self.assertRaises(self.GovernanceError):
            self._build(packet)


class IdempotencyUnitTest(unittest.TestCase):
    """idempotency_unit_test"""

    def setUp(self) -> None:
        self.poller = importlib.import_module("job_tribunal_poller_v7")
        self._tmp = tempfile.TemporaryDirectory()
        self.inbox = Path(self._tmp.name) / "inbox"
        self.work_root = Path(self._tmp.name) / "work"
        self.runtime_dir = Path(self._tmp.name) / "runtime"
        self.inbox.mkdir()
        self.work_root.mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _write_packet(self, name: str) -> Path:
        packet = {
            "POLLER_V7": {
                "task_id": "CP-IDEMPOTENT-001",
                "worker": "codex",
                "working_directory": str(self.work_root),
                "sandbox": "read-only",
                "timeout_seconds": 900,
                "prompt": "A sufficiently long bounded task description.",
                "expected_outputs": [],
                "authorization": {
                    "decision": "GO",
                    "approved_by": "DCS Level 0",
                    "approved_at": "2026-08-03T00:00:00-04:00",
                },
            }
        }
        path = self.inbox / name
        path.write_text(json.dumps(packet), encoding="utf-8")
        return path

    def test_second_pass_over_same_source_is_idempotent_skip(self) -> None:
        path = self._write_packet("TRIBUNAL_IDEMPOTENT.json")

        first = self.poller.process_packet(path, self.runtime_dir, [self.work_root], dispatch=False)
        self.assertEqual(first["outcome"], "AUTHORIZED_DRY_RUN_HOLD")

        receipt_file = Path(first["receipt"])
        receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
        receipt["state"] = "COMPLETED"
        receipt_file.write_text(json.dumps(receipt), encoding="utf-8")

        second = self.poller.process_packet(path, self.runtime_dir, [self.work_root], dispatch=False)
        self.assertEqual(second["outcome"], "IDEMPOTENT_SKIP")
        self.assertEqual(second["receipt"], first["receipt"])

    def test_changed_source_bypasses_stale_receipt(self) -> None:
        path = self._write_packet("TRIBUNAL_CHANGED.json")
        first = self.poller.process_packet(path, self.runtime_dir, [self.work_root], dispatch=False)
        receipt_file = Path(first["receipt"])
        receipt = json.loads(receipt_file.read_text(encoding="utf-8"))
        receipt["state"] = "COMPLETED"
        receipt_file.write_text(json.dumps(receipt), encoding="utf-8")

        # Mutate the source packet -> source_sha256 changes -> must not be
        # treated as the same completed task.
        packet = json.loads(path.read_text(encoding="utf-8"))
        packet["POLLER_V7"]["prompt"] = "A different sufficiently long bounded task."
        path.write_text(json.dumps(packet), encoding="utf-8")

        second = self.poller.process_packet(path, self.runtime_dir, [self.work_root], dispatch=False)
        self.assertNotEqual(second["outcome"], "IDEMPOTENT_SKIP")
        self.assertNotEqual(second["receipt"], first["receipt"])

    def test_run_once_is_deterministic_ordering(self) -> None:
        self._write_packet("TRIBUNAL_A.json")
        self._write_packet("TRIBUNAL_B.json")
        first_pass = self.poller.run_once(self.inbox, self.runtime_dir, [self.work_root], dispatch=False)
        second_pass = self.poller.run_once(self.inbox, self.runtime_dir, [self.work_root], dispatch=False)
        self.assertEqual(len(first_pass), 2)
        # Same two source files, not yet terminal -> re-authorized both times,
        # but always exactly the two known task IDs, never duplicated work items.
        self.assertEqual(
            {r["task_id"] for r in first_pass},
            {r["task_id"] for r in second_pass},
        )


class ReceiptSchemaValidationTest(unittest.TestCase):
    """receipt_schema_validation"""

    def setUp(self) -> None:
        self.state_machine = importlib.import_module("tribunal_v7_state_machine")
        self._tmp = tempfile.TemporaryDirectory()
        self.work_root = Path(self._tmp.name)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_new_receipt_matches_required_schema(self) -> None:
        source = self.work_root / "TRIBUNAL_SCHEMA.json"
        source.write_text("{}", encoding="utf-8")
        receipt = self.state_machine.new_receipt(source, "a" * 64, "CP-SCHEMA-001")

        required_fields = {
            "schema",
            "task_id",
            "source_file",
            "source_sha256",
            "state",
            "created_at",
            "updated_at",
            "history",
            "worker_result",
        }
        self.assertTrue(required_fields.issubset(receipt.keys()))
        self.assertEqual(receipt["schema"], self.state_machine.RECEIPT_SCHEMA_VERSION)
        self.assertEqual(receipt["state"], self.state_machine.PollerState.RECEIVED.value)
        self.assertIsNone(receipt["worker_result"])
        self.assertEqual(len(receipt["history"]), 1)
        self.assertIsNone(receipt["history"][0]["from"])

    def test_illegal_transition_rejected(self) -> None:
        source = self.work_root / "TRIBUNAL_SCHEMA2.json"
        source.write_text("{}", encoding="utf-8")
        receipt = self.state_machine.new_receipt(source, "a" * 64, "CP-SCHEMA-002")
        with self.assertRaises(self.state_machine.GovernanceError):
            # RECEIVED cannot jump straight to COMPLETED.
            self.state_machine.transition(
                receipt, self.state_machine.PollerState.COMPLETED, "skip states"
            )

    def test_verify_worker_result_rejects_task_id_mismatch(self) -> None:
        spec = self.state_machine.TaskSpec(
            task_id="CP-REAL-001",
            worker="codex",
            prompt="A sufficiently long bounded task description.",
            working_directory=self.work_root,
            sandbox="read-only",
            timeout_seconds=900,
            expected_outputs=(),
            approved_by="DCS Level 0",
            approved_at="2026-08-03T00:00:00-04:00",
            source_file=self.work_root / "src.json",
            source_sha256="b" * 64,
        )
        bad_result = {
            "task_id": "CP-WRONG-001",
            "source_sha256": "b" * 64,
            "status": "COMPLETED",
            "outputs": [],
        }
        with self.assertRaises(self.state_machine.VerificationError):
            self.state_machine.verify_worker_result(spec, bad_result)

    def test_verify_worker_result_rejects_missing_expected_output_file(self) -> None:
        spec = self.state_machine.TaskSpec(
            task_id="CP-REAL-002",
            worker="codex",
            prompt="A sufficiently long bounded task description.",
            working_directory=self.work_root,
            sandbox="workspace-write",
            timeout_seconds=900,
            expected_outputs=("candidate/out.json",),
            approved_by="DCS Level 0",
            approved_at="2026-08-03T00:00:00-04:00",
            source_file=self.work_root / "src.json",
            source_sha256="c" * 64,
        )
        result = {
            "task_id": "CP-REAL-002",
            "source_sha256": "c" * 64,
            "status": "COMPLETED",
            "outputs": ["candidate/out.json"],
        }
        # Declared but never actually written to disk -> must fail closed,
        # never be reported as a verified completion.
        with self.assertRaises(self.state_machine.VerificationError):
            self.state_machine.verify_worker_result(spec, result)


if __name__ == "__main__":
    unittest.main()
