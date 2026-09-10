import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from apps.escd.api.index import _parse_ack_timestamp
from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.service import RuntimeRuleError, require_job_transition, require_approval_decision, next_best_action, briefing_snapshot
from apps.escd.runtime.render import render_job_row


class AuthTests(unittest.TestCase):
    def test_extract_bearer(self):
        self.assertEqual(extract_bearer({"Authorization": "Bearer abc"}), "abc")
        with self.assertRaises(AuthError):
            extract_bearer({})

    def test_verify_user_and_operator(self):
        def fake_get(url, headers, timeout):
            return 200, {"id": "u1", "email": "Owner@Example.com"}
        auth = verify_supabase_user("tok", "https://x.supabase.co", "anon", fake_get)
        self.assertEqual(auth.user_id, "u1")
        row = authorize_operator(auth, [{"user_id": "u1", "active": True, "access_scope": "dcse_owner"}])
        self.assertEqual(row["access_scope"], "dcse_owner")
        with self.assertRaises(AuthError):
            authorize_operator(auth, [{"user_id": "u2", "active": True, "access_scope": "dcse_owner"}])


class RuleTests(unittest.TestCase):
    def test_waiting_approval_cannot_complete(self):
        job = {"status": "waiting_approval", "requires_approval": True}
        with self.assertRaisesRegex(RuntimeRuleError, "invalid_transition"):
            require_job_transition(job, "completed", ["e1"], True, True)

    def test_waiting_approval_requires_approved_to_resume(self):
        job = {"status": "waiting_approval", "requires_approval": True}
        with self.assertRaisesRegex(RuntimeRuleError, "approved_decision_required"):
            require_job_transition(job, "running", [], False, False)
        self.assertEqual(require_job_transition(job, "running", [], False, True)["status"], "running")

    def test_completion_requires_evidence_exit_and_approval(self):
        job = {"status": "running", "requires_approval": True}
        with self.assertRaisesRegex(RuntimeRuleError, "approved_decision_required"):
            require_job_transition(job, "completed", ["e1"], True, False)
        with self.assertRaisesRegex(RuntimeRuleError, "exit_criteria_not_met"):
            require_job_transition(job, "completed", ["e1"], False, True)
        with self.assertRaisesRegex(RuntimeRuleError, "evidence_required"):
            require_job_transition(job, "completed", [], True, True)
        self.assertEqual(require_job_transition(job, "completed", ["e1"], True, True)["status"], "completed")

    def test_approval_actor_is_authenticated_identity(self):
        approval = {"status": "pending"}
        update = require_approval_decision(approval, "approved", "u-auth")
        self.assertEqual(update["decided_by_user_id"], "u-auth")
        with self.assertRaises(RuntimeRuleError):
            require_approval_decision(approval, "approved", "")

    def test_next_best_action_uses_governed_policy(self):
        jobs = [
            {"id": "b", "title": "B", "status": "queued", "explicit_priority": 50, "urgency": 20, "actionable": True},
            {"id": "a", "title": "A", "status": "queued", "explicit_priority": 80, "urgency": 70, "actionable": True},
            {"id": "x", "title": "Blocked", "status": "queued", "blocked": True, "explicit_priority": 100, "urgency": 100, "actionable": True},
        ]
        result = next_best_action(jobs)
        self.assertEqual(result["job_id"], "a")
        self.assertEqual(result["queue"], "NOW")
        self.assertEqual(len(result["contributions"]), 10)

    def test_briefing_is_persisted_state_snapshot(self):
        snap = briefing_snapshot(changed=[{"summary": "x"}], completed=[], approvals=[], due_or_at_risk=[], blockers=[], watches=[], jobs=[])
        self.assertEqual(snap["source"], "persisted_reconciled_state")
        self.assertIsNone(snap["next_best_action"])

    def test_briefing_ack_rejects_future_and_naive_timestamps(self):
        future = (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat()
        with self.assertRaisesRegex(RuntimeRuleError, "briefing_ack_in_future"):
            _parse_ack_timestamp(future)
        with self.assertRaisesRegex(RuntimeRuleError, "invalid_acknowledged_through"):
            _parse_ack_timestamp("2026-09-09T20:00:00")


class RenderingTests(unittest.TestCase):
    def test_rendering_escapes_untrusted_text(self):
        row = render_job_row({"title": "<script>alert(1)</script>", "status": "<b>x</b>", "updated_at": "now"})
        self.assertNotIn("<script>", row)
        self.assertNotIn("<b>x</b>", row)
        self.assertIn("&lt;script&gt;", row)


class StaticContractTests(unittest.TestCase):
    def setUp(self):
        self.api = (ROOT / "apps/escd/api/index.py").read_text()
        self.web = (ROOT / "apps/escd/web/index.html").read_text()
        self.mig = (ROOT / "supabase/migrations/20260909_escd_runtime_state.sql").read_text()

    def test_no_service_role_runtime(self):
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", self.api)
        self.assertIn("SUPABASE_ANON_KEY", self.api)

    def test_cors_is_allowlist_not_wildcard(self):
        self.assertNotIn('Access-Control-Allow-Origin\", \"*\"', self.api)
        self.assertIn("ESCD_ALLOWED_ORIGINS", self.api)

    def test_ui_avoids_innerhtml_for_persisted_content(self):
        self.assertNotIn("innerHTML", self.web)
        self.assertIn("textContent", self.web)

    def test_briefing_get_does_not_ack(self):
        get_block = self.api.split("def do_GET", 1)[1].split("def do_POST", 1)[0]
        self.assertNotIn("acknowledge_briefing(", get_block)
        self.assertIn("/api/escd/briefing/ack", self.api)
        self.assertIn("briefing_ack_in_future", self.api)
        self.assertIn("briefing_ack_regression", self.api)

    def test_migration_rls_and_completion_trigger(self):
        for table in ["escd_jobs", "escd_job_events", "escd_approvals", "escd_evidence", "escd_briefing_acks"]:
            self.assertIn(f"ALTER TABLE dcse_cp.{table} ENABLE ROW LEVEL SECURITY", self.mig)
            self.assertIn(f"ALTER TABLE dcse_cp.{table} FORCE ROW LEVEL SECURITY", self.mig)
        self.assertIn("dcse_cp.is_dcs_owner()", self.mig)
        self.assertNotIn("TO service_role", self.mig)
        self.assertIn("approved_decision_required", self.mig)
        self.assertIn("evidence_required", self.mig)
        self.assertIn("exit_criteria_not_met", self.mig)
        self.assertIn("WHEN 'waiting_approval' THEN NEW.status IN ('running','failed','cancelled')", self.mig)
        self.assertIn("ORDER BY a.requested_at DESC, a.id DESC", self.mig)
        self.assertIn("latest_approval_status IS DISTINCT FROM 'approved'", self.mig)

    def test_migration_preserves_transition_history_and_ack_cursor_integrity(self):
        self.assertIn("escd_record_job_transition", self.mig)
        self.assertIn("'status_transition'", self.mig)
        self.assertIn("from_status", self.mig)
        self.assertIn("to_status", self.mig)
        self.assertIn("escd_validate_briefing_ack", self.mig)
        self.assertIn("briefing_ack_in_future", self.mig)
        self.assertIn("briefing_ack_regression", self.mig)

    def test_no_employment_seed_or_aegis_runtime_identity(self):
        self.assertNotIn("dcs_employment", self.mig.lower())
        self.assertNotIn("AEGIS", self.web)


if __name__ == "__main__":
    unittest.main()
