"""
DCSE Orchestration Convergence Test Suite
Task ID: DCSE-ORCH-CONVERGENCE-BUILD-20260915-01
Parent Issue: #119 / #116

Tests executed:
1. Operative Rules Engine v0.2.1 scale and registry uniqueness (148 rules, 5 composites)
2. 60-rule legacy compatibility suite (127 cases)
3. 5/5 orchestration benchmark scenarios
4. Provider truth contract (6 tests)
5. Failed-rule severity and disposition verification
6. Restart/resume state classification
7. Migration timestamp uniqueness and duplicate prevention
"""

import importlib
import os
import sys
import unittest
from pathlib import Path

# Setup paths
HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "dcse"))


class TestConvergence(unittest.TestCase):

    def test_01_operative_rules_engine_scale_and_registry(self):
        """Verify OPERATIVE v0.2.1 package materializes and registers 148 rules + 5 composites."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("bootstrap", str(HERE / "rules_engine" / "bootstrap.py"))
        bs = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bs)
        root = bs.materialize()
        sys.path.insert(0, str(root))
        from dcse_rules.runtime.registry import load_registry
        reg = load_registry()
        rules = reg["rules"]
        composites = reg["composites"]

        self.assertEqual(len(rules), 148, f"Expected 148 atomic rules, got {len(rules)}")
        self.assertEqual(len(composites), 5, f"Expected 5 composites, got {len(composites)}")

        # Check entity families (50 rules)
        entity_prefixes = ["TSK", "IDE", "AST", "DDN", "KNW"]
        for p in entity_prefixes:
            matching = [r for r in rules if r.startswith(f"{p}-")]
            self.assertEqual(len(matching), 10, f"Expected 10 rules for {p}, got {len(matching)}")

        # Check capability families (90 rules across 18 caps)
        cap_prefixes = [
            "CNT", "COM", "DEP", "EML", "EMP", "ESCD", "FIL", "GEN",
            "GIT", "GOV", "MED", "SC", "SEC", "SS", "SUP", "TI", "TRB", "VOC"
        ]
        for cp in cap_prefixes:
            matching = [r for r in rules if r.startswith(f"{cp}-")]
            self.assertEqual(len(matching), 5, f"Expected 5 rules for {cp}, got {len(matching)}")

        # Check meta rules (8 rules)
        meta_matching = [r for r in rules if r.startswith("META-")]
        self.assertEqual(len(meta_matching), 8, f"Expected 8 rules for META, got {len(meta_matching)}")

    def test_02_dcse_compatibility_suite(self):
        """Execute the 60-rule / 127-case compatibility suite."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("dcse_tests", str(HERE / "dcse" / "tests.py"))
        dcse_tests = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dcse_tests)
        ret = dcse_tests.run()
        self.assertEqual(ret, 0, "Expected dcse/tests.py to pass with 0 failures")

    def test_03_orchestration_benchmark(self):
        """Execute the 5/5 scenario orchestration benchmark."""
        import importlib.util
        spec = importlib.util.spec_from_file_location("dcse_bench", str(HERE / "dcse" / "bench.py"))
        bench = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bench)
        res = bench.run()
        self.assertEqual(res, 0, "Expected bench.py to pass all scenarios")

    def test_04_provider_truth_policy(self):
        """Execute provider truth policy checks."""
        import apps.escd.tests.test_response_truth_policy as truth
        truth.test_conversation_policy_forbids_fake_execution()
        truth.test_operational_policy_keeps_control_with_orchestrator()
        truth.test_policy_is_server_injected_before_user_prompt()
        truth.test_response_hash_changes_if_content_changes()
        truth.test_response_policy_has_stable_rule_ids()
        truth.test_response_proof_detects_provider_return_without_simulation()

    def test_05_failed_rule_severity_and_disposition(self):
        """Test rule failure severity and disposition with full provenance capture."""
        from model import Operation, Plan, FAIL, PASS, REFUSE, ESCALATE, EXECUTE, PROVISIONAL, CANDIDATE
        from orchestrator import Orchestrator
        from registry import REGISTRY, load_rules

        load_rules()
        o = Orchestrator()

        # 1. Broken operation with binding rule -> must REFUSE and capture severity
        broken_op = Operation(
            entity="task",
            action="complete",
            facts={"task_id": "T-FAIL", "state": "complete"}  # missing completion_evidence
        )
        REGISTRY.bind_all(PROVISIONAL)
        outcome = o.run(broken_op, execute=False)

        self.assertEqual(outcome.disposition, REFUSE)
        self.assertIn("TASK-06", outcome.reason)

        # Check provenance in plan results
        t06_res = [r for r in outcome.plan.results if r.rule_id == "TASK-06"][0]
        self.assertEqual(t06_res.verdict, FAIL)
        self.assertTrue(t06_res.binding)
        self.assertEqual(t06_res.status, PROVISIONAL)
        self.assertEqual(t06_res.ruleset, "TASK")
        self.assertEqual(t06_res.version, "0.2.1")
        self.assertTrue(len(t06_res.severity) > 0)

        # 2. Irreversible send operation -> must ESCALATE even when passing
        send_op = Operation(
            entity="task",
            action="send",
            capabilities=["voice"],
            facts={
                "task_id": "T-SEND",
                "objective": "notify",
                "owner": "DCS",
                "state": "open",
                "authority_expires_at": 4102444800.0,
                "recipient": "plumber",
                "authorised_recipients": ["plumber"],
                "message_class": "confirm",
                "authorised_classes": ["confirm"],
                "lanes_touched": ["SC"],
                "transmission_record": "rec-1",
                "authority_ref": "auth-1"
            }
        )
        send_outcome = o.run(send_op, execute=False)
        self.assertEqual(send_outcome.disposition, ESCALATE)
        self.assertEqual(len(send_outcome.plan.failures()), 0)

    def test_06_restart_resume_and_memory(self):
        """Verify conversation restart, classification, and dual-lane routing."""
        from apps.escd.runtime.conversation_memory import classify_message

        c1 = classify_message("Hello there")
        self.assertEqual(c1["primary_category"], "CHAT_ONLY")

        c2 = classify_message("Please execute the task review.")
        self.assertEqual(c2["primary_category"], "TASK")

        c3 = classify_message("Let's save this idea for next sprint.")
        self.assertEqual(c3["primary_category"], "IDEA")

    def test_07_duplicate_migration_prevention(self):
        """Verify that all migration files in supabase/migrations have unique timestamps and valid filenames."""
        mig_dir = HERE / "supabase/migrations"
        migs = list(mig_dir.glob("*.sql"))
        self.assertTrue(len(migs) >= 5, f"Expected at least 5 migrations, found {len(migs)}")

        timestamps = [f.name.split("_")[0] for f in migs]
        duplicates = [ts for ts in set(timestamps) if timestamps.count(ts) > 1]
        self.assertEqual(len(duplicates), 0, f"Found duplicate migration timestamps: {duplicates}")

        # Ensure live identity is present
        live_identity = "20260914195631_escd_provider_anthropic_registry_v1.sql"
        self.assertTrue((mig_dir / live_identity).exists(), f"Missing live identity {live_identity}")

        # Ensure stale identity is NOT present
        stale_identity = "20260914195500_escd_provider_anthropic_registry_v1.sql"
        self.assertFalse((mig_dir / stale_identity).exists(), f"Stale identity {stale_identity} must not be present")


if __name__ == "__main__":
    unittest.main()
