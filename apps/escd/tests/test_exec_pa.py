from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]

from apps.escd.runtime.executive_pa import (
    calendar_contract,
    command_contract,
    communication_contract,
    contact_context_contract,
    executive_stream,
    file_route_contract,
    intake_item_key,
    meeting_prep_contract,
    merge_source_refs,
    mobile_action_contract,
    notification_contract,
    retry_contract,
    routine_contract,
)
from apps.escd.runtime.repository import SupabaseRLSClient


class ExecutiveStreamTests(unittest.TestCase):
    def _item(self, item_id: str, status: str, **overrides):
        row = {
            "id": item_id,
            "title": item_id,
            "status": status,
            "actionable": True,
            "blocked": False,
            "external_dependency": False,
            "future_trigger": False,
            "missing_approval": False,
            "explicit_hold": False,
            "mission_priority": 0,
            "explicit_priority": 0,
            "urgency": 0,
            "revenue_relevance": 0,
            "unblock_value": 0,
            "consequence": 0,
            "aging": 0,
            "effort_efficiency": 0,
            "strategic_leverage": 0,
            "dcs_override": 0,
            "source_refs": ["src:" + item_id],
        }
        row.update(overrides)
        return row

    def test_five_queue_projection_and_terminal_exclusion(self):
        items = [
            self._item("now", "active", urgency=90),
            self._item("approval", "approval"),
            self._item("waiting", "waiting"),
            self._item("watch", "watch"),
            self._item("backlog", "captured"),
            self._item("done", "completed"),
            self._item("cancelled", "cancelled"),
            self._item("archived", "archived"),
        ]
        stream = executive_stream(items)
        self.assertEqual(stream["counts"], {
            "NOW": 1, "APPROVAL": 1, "WAITING": 1, "WATCH": 1, "BACKLOG": 1
        })
        surfaced = {row["id"] for rows in stream["queues"].values() for row in rows}
        self.assertNotIn("done", surfaced)
        self.assertNotIn("cancelled", surfaced)
        self.assertNotIn("archived", surfaced)
        self.assertEqual(stream["next_best_action"]["item_id"], "now")

    def test_nba_is_deterministic_and_blocked_item_not_now(self):
        items = [
            self._item("b", "active", urgency=90, explicit_priority=50),
            self._item("a", "active", urgency=90, explicit_priority=50),
            self._item("x", "active", blocked=True, urgency=100, explicit_priority=100),
        ]
        first = executive_stream(items)
        second = executive_stream(list(reversed(items)))
        self.assertEqual(first["next_best_action"], second["next_best_action"])
        self.assertEqual(first["next_best_action"]["item_id"], "a")
        self.assertEqual(first["queues"]["WAITING"][0]["id"], "x")

    def test_intake_key_and_source_merge_are_stable(self):
        self.assertEqual(
            intake_item_key("Call vendor", "general"),
            intake_item_key(" call vendor ", " GENERAL "),
        )
        self.assertEqual(merge_source_refs(["gmail:1", "github:2"], ["gmail:1", "drive:3"]), [
            "gmail:1", "github:2", "drive:3"
        ])


class PersonalAssistantPolicyTests(unittest.TestCase):
    def test_calendar_conflict_is_source_bound_and_no_write(self):
        result = calendar_contract([
            {"event_id": "e1", "start": "2026-09-10T10:00:00-04:00", "end": "2026-09-10T11:00:00-04:00", "source_ref": "calendar:e1"},
            {"event_id": "e2", "start": "2026-09-10T10:30:00-04:00", "end": "2026-09-10T11:30:00-04:00", "source_ref": "calendar:e2"},
        ])
        self.assertEqual(result["conflicts"][0]["class"], "C1")
        self.assertTrue(result["conflicts"][0]["approval_required_for_external_change"])
        self.assertFalse(result["external_calendar_write_performed"])

    def test_meeting_prep_requires_provenance(self):
        with self.assertRaisesRegex(ValueError, "meeting_prep_source_required"):
            meeting_prep_contract({"purpose": "Review"})
        result = meeting_prep_contract({"purpose": "Review", "source_refs": ["calendar:e1"]})
        self.assertEqual(result["status"], "prepared")
        self.assertFalse(result["external_calendar_write_performed"])

    def test_communication_triage_never_sends(self):
        result = communication_contract({
            "source_ref": "gmail:m1",
            "reply_required": True,
            "proposed_reply": "Draft only",
        })
        self.assertEqual(result["triage_class"], "REPLY")
        self.assertEqual(result["draft"]["status"], "candidate")
        self.assertTrue(result["draft"]["approval_required_for_external_send"])
        self.assertFalse(result["draft"]["external_send_performed"])

    def test_contact_context_rejects_sensitive_inference(self):
        with self.assertRaisesRegex(ValueError, "sensitive_inference_prohibited"):
            contact_context_contract({
                "contact_ref": "contacts:1",
                "provenance_refs": ["contacts:1"],
                "inferred_sensitive_trait": True,
            })
        result = contact_context_contract({
            "contact_ref": "contacts:1",
            "provenance_refs": ["contacts:1"],
            "confidence_status": "verified",
        })
        self.assertFalse(result["source_of_truth_overwrite_performed"])

    def test_routine_duplicate_and_pause_are_bounded(self):
        duplicate = routine_contract({"run_key": "r:1"}, "r:1")
        self.assertEqual(duplicate["decision"], "SKIP")
        paused = routine_contract({"run_key": "r:2", "paused": True}, None)
        self.assertEqual(paused["reason"], "paused")
        run = routine_contract({"run_key": "r:3"}, None)
        self.assertTrue(run["trigger_creates_eligibility_only"])

    def test_notification_evaluation_is_intent_only(self):
        quiet = notification_contract({"key": "n", "current_value": "same", "prior_value": "same"})
        self.assertFalse(quiet["notify"])
        changed = notification_contract({"key": "n", "current_value": "new", "prior_value": "old", "notification_class": "N2"})
        self.assertTrue(changed["notify"])
        self.assertEqual(changed["delivery_claim"], "intent_only")

    def test_recovery_hard_stops_security_and_bounds_retry(self):
        blocked = retry_contract({"attempt": 0, "max_attempts": 3, "security_failure": True})
        self.assertFalse(blocked["retry_allowed"])
        allowed = retry_contract({"attempt": 1, "max_attempts": 3})
        self.assertTrue(allowed["retry_allowed"])

    def test_command_file_and_mobile_are_proposal_contracts(self):
        command = command_contract("release candidate build")
        self.assertEqual(command["operation"], "RELEASE")
        self.assertTrue(command["evidence_required"])
        self.assertFalse(command["execution_performed"])

        route = file_route_contract({"source_ref": "drive:f1", "target": "briefing"})
        self.assertTrue(route["source_native_authority_preserved"])
        self.assertFalse(route["external_write_performed"])

        mobile = mobile_action_contract({"action": "approve", "target_id": "approval:1"})
        self.assertEqual(mobile["operation"], "APPROVE")
        self.assertTrue(mobile["requires_existing_governed_endpoint"])
        self.assertFalse(mobile["execution_performed"])


class RepositoryContractTests(unittest.TestCase):
    def test_item_create_is_idempotent_by_key(self):
        class FakeRepo(SupabaseRLSClient):
            def __init__(self):
                self.stored = None
                self.posts = 0

            def _call(self, method, path, payload=None):
                if method == "GET" and path.startswith("escd_items?item_key="):
                    return [self.stored] if self.stored else []
                if method == "POST" and path == "escd_items":
                    self.posts += 1
                    self.stored = {**payload, "id": "i1"}
                    return [self.stored]
                raise AssertionError((method, path, payload))

        repo = FakeRepo()
        payload = {"item_key": "k1", "title": "T"}
        self.assertEqual(repo.create_item(payload), repo.create_item(payload))
        self.assertEqual(repo.posts, 1)

    def test_notification_intent_is_deduped(self):
        class FakeRepo(SupabaseRLSClient):
            def __init__(self):
                self.stored = None
                self.posts = 0

            def _call(self, method, path, payload=None):
                if method == "GET" and path.startswith("escd_notification_intents?"):
                    return [self.stored] if self.stored else []
                if method == "POST" and path == "escd_notification_intents":
                    self.posts += 1
                    self.stored = {**payload, "id": "n1"}
                    return [self.stored]
                raise AssertionError((method, path, payload))

        repo = FakeRepo()
        payload = {"notification_key": "n1", "reason": "change"}
        self.assertEqual(repo.create_notification_intent(payload), repo.create_notification_intent(payload))
        self.assertEqual(repo.posts, 1)


class StaticBuildPlanTests(unittest.TestCase):
    def setUp(self):
        self.api = (ROOT / "apps/escd/api/index.py").read_text()
        self.repo = (ROOT / "apps/escd/runtime/repository.py").read_text()
        self.mig = (ROOT / "supabase/migrations/20260910_escd_exec_pa_state.sql").read_text()

    def test_integrated_api_surface_is_present(self):
        for route in [
            "/api/escd/executive-stream",
            "/api/escd/intake",
            "/api/escd/items/transition",
            "/api/escd/projects",
            "/api/escd/decisions",
            "/api/escd/contacts/context",
            "/api/escd/routines",
            "/api/escd/routines/evaluate",
            "/api/escd/notifications/evaluate",
            "/api/escd/calendar/conflicts",
            "/api/escd/calendar/meeting-prep",
            "/api/escd/communications/triage",
            "/api/escd/commands/parse",
            "/api/escd/files/route",
            "/api/escd/mobile/action",
            "/api/escd/recovery/evaluate",
        ]:
            self.assertIn(route, self.api)

    def test_no_privileged_runtime_or_external_execution_claims(self):
        self.assertNotIn("SUPABASE_SERVICE_ROLE_KEY", self.api)
        self.assertIn('"delivery_performed": False', self.api)
        self.assertIn('"external_send_performed": False', (ROOT / "apps/escd/runtime/executive_pa.py").read_text())

    def test_candidate_state_has_required_rls_and_append_only_records(self):
        for table in [
            "escd_projects", "escd_items", "escd_item_events", "escd_decisions",
            "escd_contact_contexts", "escd_routines", "escd_notification_intents",
        ]:
            self.assertIn(f"ALTER TABLE dcse_cp.{table} ENABLE ROW LEVEL SECURITY", self.mig)
            self.assertIn(f"ALTER TABLE dcse_cp.{table} FORCE ROW LEVEL SECURITY", self.mig)
        self.assertIn("GRANT SELECT, INSERT ON dcse_cp.escd_item_events", self.mig)
        self.assertIn("escd_validate_item_transition", self.mig)
        self.assertIn("escd_record_item_transition", self.mig)
        self.assertIn("routine_configuration_immutable_create_new_version", self.mig)
        self.assertNotIn("TO service_role", self.mig)

    def test_employment_and_ddna_cutover_not_added(self):
        combined = (self.api + self.repo + self.mig).lower()
        self.assertNotIn("dcs_employment", combined)
        self.assertNotIn("ddna_runtime_mode", combined)


if __name__ == "__main__":
    unittest.main()
