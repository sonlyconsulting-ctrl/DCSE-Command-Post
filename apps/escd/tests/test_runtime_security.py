import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from apps.escd.api.index import _parse_ack_timestamp, _verification_key
from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient
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

    def test_expired_approval_cannot_be_decided(self):
        approval = {
            "status": "pending",
            "expires_at": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        }
        with self.assertRaisesRegex(RuntimeRuleError, "approval_expired"):
            require_approval_decision(approval, "approved", "u-auth")

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

    def test_verification_key_is_deterministic_and_scope_sensitive(self):
        first = _verification_key("job-1", "evidence-1", "verified", "test_result")
        self.assertEqual(first, _verification_key("job-1", "evidence-1", "verified", "test_result"))
        self.assertNotEqual(first, _verification_key("job-1", "evidence-2", "verified", "test_result"))
        self.assertNotEqual(first, _verification_key("job-1", "evidence-1", "failed", "test_result"))
        self.assertTrue(first.startswith("escd-v1-"))


class RepositoryTests(unittest.TestCase):
    def test_verification_create_is_idempotent_by_key(self):
        class FakeRepo(SupabaseRLSClient):
            def __init__(self):
                self.calls = []
                self.stored = None

            def _call(self, method, path, payload=None):
                self.calls.append((method, path, payload))
                if method == "GET" and path.startswith("escd_job_verifications?"):
                    return [self.stored] if self.stored else []
                if method == "POST" and path == "escd_job_verifications":
                    self.stored = dict(payload)
                    self.stored["id"] = "v1"
                    return [self.stored]
                raise AssertionError((method, path, payload))

        repo = FakeRepo()
        kwargs = dict(
            verification_key="escd-v1-key",
            job_id="j1",
            evidence_id="e1",
            outcome="verified",
            verification_method="test_result",
            notes="passed",
        )
        first = repo.create_job_verification(**kwargs)
        second = repo.create_job_verification(**kwargs)
        self.assertEqual(first, second)
        posts = [call for call in repo.calls if call[0] == "POST"]
        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0][2]["job_id"], "j1")
        self.assertEqual(posts[0][2]["evidence_id"], "e1")


class RenderingTests(unittest.TestCase):
    def test_rendering_escapes_untrusted_text(self):
        row = render_job_row({"title": "<script>alert(1)</script>", "status": "<b>x</b>", "updated_at": "now"})
        self.assertNotIn("<script>", row)
        self.assertNotIn("<b>x</b>", row)
        self.assertIn("&lt;script&gt;", row)


class StaticContractTests(unittest.TestCase):
    def setUp(self):
        self.api = (ROOT / "apps/escd/api/index.py").read_text()
        self.repo = (ROOT / "apps/escd/runtime/repository.py").read_text()
        self.web = (ROOT / "apps/escd/web/index.html").read_text()
        self.mig = (ROOT / "supabase/migrations/20260909_escd_runtime_state.sql").read_text()
        self.verify_mig = (ROOT / "supabase/migrations/20260910_escd_exit_verification.sql").read_text()

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

    def test_completion_does_not_trust_request_exit_assertion(self):
        self.assertNotIn('exit_criteria_met=bool(payload.get("exit_criteria_met"))', self.api)
        self.assertIn('exit_criteria_met=bool(job.get("exit_criteria_met"))', self.api)

    def test_verification_endpoint_is_persisted_evidence_bound(self):
        self.assertIn('/api/escd/jobs/verify', self.api)
        self.assertIn('repo.get_evidence(evidence_id)', self.api)
        self.assertIn('verification_evidence_job_mismatch', self.api)
        self.assertIn('repo.create_job_verification(', self.api)
        self.assertIn('job.get("status") != "running"', self.api)
        self.assertIn('create_job_verification', self.repo)
        self.assertIn('get_job_verification', self.repo)

    def test_approval_lookup_is_action_scoped_and_deterministic(self):
        self.assertIn('action_key = f"job_transition:{target}"', self.api)
        self.assertIn("latest_approval(job_id, action_key)", self.api)
        self.assertIn("action_key=eq.{safe_action}", self.repo)
        self.assertIn("order=requested_at.desc,id.desc", self.repo)

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
        self.assertIn("a.action_key = required_action_key", self.mig)
        self.assertIn("ORDER BY a.requested_at DESC, a.id DESC", self.mig)
        self.assertIn("latest_approval_status IS DISTINCT FROM 'approved'", self.mig)

    def test_migration_preserves_transition_history_and_ack_cursor_integrity(self):
        self.assertIn("escd_record_job_transition", self.mig)
        self.assertIn("'status_transition'", self.mig)
        self.assertIn("escd_record_approval_transition", self.mig)
        self.assertIn("'approval_transition'", self.mig)
        self.assertIn("payload_fingerprint", self.mig)
        self.assertIn("escd_validate_briefing_ack", self.mig)
        self.assertIn("briefing_ack_in_future", self.mig)
        self.assertIn("briefing_ack_regression", self.mig)

    def test_migration_provenance_fields_bind_to_authenticated_principal(self):
        self.assertIn("created_by_user_id = auth.uid()", self.mig)
        self.assertIn("actor_user_id = auth.uid()", self.mig)
        self.assertIn("requested_by_user_id = auth.uid()", self.mig)
        self.assertIn("decided_by_user_id IS NULL OR decided_by_user_id = auth.uid()", self.mig)

    def test_exit_verification_migration_is_rls_append_only_and_derived(self):
        self.assertIn("CREATE TABLE IF NOT EXISTS dcse_cp.escd_job_verifications", self.verify_mig)
        self.assertIn("ENABLE ROW LEVEL SECURITY", self.verify_mig)
        self.assertIn("FORCE ROW LEVEL SECURITY", self.verify_mig)
        self.assertIn("verifier_user_id = auth.uid()", self.verify_mig)
        self.assertIn("GRANT SELECT, INSERT ON dcse_cp.escd_job_verifications TO authenticated", self.verify_mig)
        self.assertNotIn("GRANT UPDATE", self.verify_mig)
        self.assertNotIn("GRANT DELETE", self.verify_mig)
        self.assertIn("verification_evidence_job_mismatch", self.verify_mig)
        self.assertIn("verification_job_not_running", self.verify_mig)
        self.assertIn("SET exit_criteria_met = (NEW.outcome = 'verified')", self.verify_mig)
        self.assertIn("'exit_criteria_verification'", self.verify_mig)

    def test_no_employment_seed_or_aegis_runtime_identity(self):
        combined = (self.mig + self.verify_mig).lower()
        self.assertNotIn("dcs_employment", combined)
        self.assertNotIn("AEGIS", self.web)


if __name__ == "__main__":
    unittest.main()
