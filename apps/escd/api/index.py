from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import hashlib
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

from apps.escd.policy.extensions import transition_allowed
from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient, RepositoryError
from apps.escd.runtime.service import (
    RuntimeRuleError,
    require_job_transition,
    require_approval_decision,
    next_best_action,
    briefing_snapshot,
)
from apps.escd.runtime.executive_pa import (
    TASK_CLASSES,
    calendar_contract,
    command_contract,
    communication_contract,
    contact_context_contract,
    decision_contract,
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


_VERIFICATION_OUTCOMES = {"verified", "failed"}
_VERIFICATION_METHODS = {
    "dcs_confirmed",
    "tool_result",
    "test_result",
    "runtime_observation",
    "source_reconciliation",
}


def _allowed_origin(origin: str | None) -> str | None:
    configured = [x.strip() for x in os.getenv("ESCD_ALLOWED_ORIGINS", "").split(",") if x.strip()]
    if not origin or origin not in configured:
        return None
    return origin


def _parse_ack_timestamp(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise RuntimeRuleError("invalid_acknowledged_through") from exc
    if parsed.tzinfo is None:
        raise RuntimeRuleError("invalid_acknowledged_through")
    parsed = parsed.astimezone(timezone.utc)
    if parsed > datetime.now(timezone.utc):
        raise RuntimeRuleError("briefing_ack_in_future")
    return parsed


def _approval_is_effective(approval: dict | None) -> bool:
    if not approval or approval.get("status") != "approved":
        return False
    expires_at = approval.get("expires_at")
    if not expires_at:
        return True
    try:
        expires = datetime.fromisoformat(str(expires_at).replace("Z", "+00:00"))
    except ValueError:
        return False
    if expires.tzinfo is None:
        return False
    return expires.astimezone(timezone.utc) > datetime.now(timezone.utc)


def _verification_key(job_id: str, evidence_id: str, outcome: str, verification_method: str) -> str:
    canonical = "\n".join((job_id, evidence_id, outcome, verification_method)).encode("utf-8")
    return "escd-v1-" + hashlib.sha256(canonical).hexdigest()


def _stable_key(prefix: str, *parts: object) -> str:
    canonical = "\n".join(str(x or "").strip().lower() for x in parts).encode("utf-8")
    return prefix + hashlib.sha256(canonical).hexdigest()


def _score_value(payload: dict, name: str) -> float:
    try:
        value = float(payload.get(name, 0) or 0)
    except (TypeError, ValueError) as exc:
        raise RuntimeRuleError(f"invalid_{name}") from exc
    if value < 0 or value > 100:
        raise RuntimeRuleError(f"invalid_{name}")
    return value


class handler(BaseHTTPRequestHandler):
    server_version = "ESCD/0.4"

    def _json(self, status: int, payload: dict, origin: str | None = None) -> None:
        data = json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.end_headers()
        self.wfile.write(data)

    def _origin(self) -> str | None:
        return _allowed_origin(self.headers.get("Origin"))

    def _read_json(self) -> dict:
        size = int(self.headers.get("Content-Length") or 0)
        if size <= 0 or size > 1_000_000:
            return {}
        raw = self.rfile.read(size)
        return json.loads(raw.decode("utf-8"))

    def _authorized(self):
        token = extract_bearer(self.headers)
        url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        anon = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
        auth = verify_supabase_user(token, url, anon)
        repo = SupabaseRLSClient(url, anon, token, schema="dcse_cp")
        authorize_operator(auth, repo.operator_self())
        return auth, repo

    def do_OPTIONS(self):
        origin = self._origin()
        if not origin:
            self._json(403, {"error": "origin_not_allowed"})
            return
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization,Content-Type")
        self.send_header("Access-Control-Max-Age", "600")
        self.send_header("Vary", "Origin")
        self.end_headers()

    def do_GET(self):
        origin = self._origin()
        path = urlparse(self.path).path

        if path == "/api/escd/health":
            self._json(200, {"ok": True, "service": "escd", "version": "0.4"}, origin)
            return

        try:
            auth, repo = self._authorized()

            if path == "/api/escd/jobs":
                self._json(200, {"ok": True, "jobs": repo.list_jobs()}, origin)
                return

            if path == "/api/escd/items":
                self._json(200, {"ok": True, "items": repo.list_items()}, origin)
                return

            if path == "/api/escd/executive-stream":
                stream = executive_stream(repo.list_items())
                self._json(200, {"ok": True, "executive_stream": stream}, origin)
                return

            if path == "/api/escd/next-action":
                items = repo.list_items()
                action = executive_stream(items)["next_best_action"] if items else next_best_action(repo.list_jobs())
                self._json(200, {"ok": True, "next_action": action}, origin)
                return

            if path == "/api/escd/approvals":
                self._json(200, {"ok": True, "approvals": repo.list_pending_approvals()}, origin)
                return

            if path == "/api/escd/briefing":
                ack = repo.last_briefing_ack()
                since = ack.get("acknowledged_through") if ack else None
                jobs = repo.list_jobs()
                items = repo.list_items()
                stream = executive_stream(items)
                job_events = repo.list_events_since(since)
                item_events = repo.list_item_events_since(since)
                approvals = repo.list_pending_approvals()
                completed = [
                    x for x in items
                    if x.get("status") == "completed"
                    and (not since or str(x.get("completed_at") or "") > since)
                ]
                blockers = list(stream["queues"]["WAITING"])
                watches = list(stream["queues"]["WATCH"])
                due_or_at_risk = [
                    x for x in items
                    if x.get("due_at") and x.get("status") not in {"completed", "cancelled", "archived"}
                ]
                changed = sorted(
                    [*job_events, *item_events],
                    key=lambda x: (str(x.get("created_at") or ""), str(x.get("id") or "")),
                    reverse=True,
                )
                snapshot = briefing_snapshot(
                    changed=changed,
                    completed=completed,
                    approvals=approvals,
                    due_or_at_risk=due_or_at_risk,
                    blockers=blockers,
                    watches=watches,
                    jobs=jobs,
                )
                snapshot["next_best_action"] = stream["next_best_action"]
                snapshot["executive_stream_counts"] = stream["counts"]
                snapshot["acknowledged_through"] = since
                snapshot["generated_at"] = datetime.now(timezone.utc).isoformat()
                self._json(200, {"ok": True, "briefing": snapshot}, origin)
                return

            self._json(404, {"error": "not_found"}, origin)
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)}, origin)
        except RepositoryError as exc:
            self._json(502, {"error": str(exc)}, origin)
        except Exception:
            self._json(500, {"error": "internal_error"}, origin)

    def do_POST(self):
        origin = self._origin()
        path = urlparse(self.path).path

        try:
            auth, repo = self._authorized()
            payload = self._read_json()

            if path == "/api/escd/jobs/transition":
                job_id = str(payload.get("job_id") or "")
                target = str(payload.get("status") or "")
                if not job_id or not target:
                    self._json(400, {"error": "job_id_and_status_required"}, origin)
                    return
                job = repo.get_job(job_id)
                if not job:
                    self._json(404, {"error": "job_not_found"}, origin)
                    return
                evidence = repo.list_job_evidence(job_id)
                action_key = f"job_transition:{target}"
                approval = repo.latest_approval(job_id, action_key)
                approved = _approval_is_effective(approval)
                update = require_job_transition(
                    job,
                    target,
                    evidence_refs=[str(e.get("id")) for e in evidence],
                    exit_criteria_met=bool(job.get("exit_criteria_met")),
                    approved=approved,
                )
                updated = repo.patch_job(job_id, update)
                self._json(200, {"ok": True, "job": updated}, origin)
                return

            if path == "/api/escd/jobs/verify":
                job_id = str(payload.get("job_id") or "").strip()
                evidence_id = str(payload.get("evidence_id") or "").strip()
                outcome = str(payload.get("outcome") or "").strip()
                verification_method = str(payload.get("verification_method") or "").strip()
                notes = str(payload.get("notes") or "").strip()
                if not job_id or not evidence_id or not outcome or not verification_method:
                    self._json(400, {"error": "job_id_evidence_id_outcome_and_method_required"}, origin)
                    return
                if outcome not in _VERIFICATION_OUTCOMES:
                    self._json(400, {"error": "invalid_verification_outcome"}, origin)
                    return
                if verification_method not in _VERIFICATION_METHODS:
                    self._json(400, {"error": "invalid_verification_method"}, origin)
                    return
                if len(notes) > 4000:
                    self._json(400, {"error": "verification_notes_too_long"}, origin)
                    return
                job = repo.get_job(job_id)
                if not job:
                    self._json(404, {"error": "job_not_found"}, origin)
                    return
                if job.get("status") != "running":
                    self._json(409, {"error": "verification_job_not_running"}, origin)
                    return
                evidence = repo.get_evidence(evidence_id)
                if not evidence:
                    self._json(404, {"error": "evidence_not_found"}, origin)
                    return
                if str(evidence.get("job_id") or "") != job_id:
                    self._json(409, {"error": "verification_evidence_job_mismatch"}, origin)
                    return
                verification_key = _verification_key(job_id, evidence_id, outcome, verification_method)
                verification = repo.create_job_verification(
                    verification_key=verification_key,
                    job_id=job_id,
                    evidence_id=evidence_id,
                    outcome=outcome,
                    verification_method=verification_method,
                    notes=notes or None,
                )
                updated_job = repo.get_job(job_id)
                self._json(201, {"ok": True, "verification": verification, "job": updated_job}, origin)
                return

            if path == "/api/escd/intake":
                title = str(payload.get("title") or "").strip()
                source_ref = str(payload.get("source_ref") or "").strip()
                source_system = str(payload.get("source_system") or "").strip()
                source_id = str(payload.get("source_id") or "").strip()
                normalized_intent = str(payload.get("normalized_intent") or title).strip()
                context = str(payload.get("context") or "general").strip()
                task_class = str(payload.get("task_class") or "CAPTURE").strip().upper()
                if not title or not source_ref or not source_system or not source_id or not normalized_intent:
                    self._json(400, {"error": "intake_source_and_identity_required"}, origin)
                    return
                if task_class not in TASK_CLASSES:
                    self._json(400, {"error": "invalid_task_class"}, origin)
                    return

                item_key = intake_item_key(normalized_intent, context)
                existing = repo.get_item_by_key(item_key)
                if existing:
                    merged = merge_source_refs(existing.get("source_refs") or [], [source_ref])
                    if merged != list(existing.get("source_refs") or []):
                        existing = repo.patch_item(str(existing["id"]), {"source_refs": merged})
                    self._json(200, {"ok": True, "deduped": True, "item": existing}, origin)
                    return

                item_payload = {
                    "item_key": item_key,
                    "title": title,
                    "summary": payload.get("summary"),
                    "status": "captured",
                    "task_class": task_class,
                    "context": context,
                    "approval_class": payload.get("approval_class"),
                    "actionable": False,
                    "blocked": bool(payload.get("blocked", False)),
                    "external_dependency": bool(payload.get("external_dependency", False)),
                    "future_trigger": bool(payload.get("future_trigger", False)),
                    "missing_approval": bool(payload.get("missing_approval", False)),
                    "explicit_hold": bool(payload.get("explicit_hold", False)),
                    "mission_priority": _score_value(payload, "mission_priority"),
                    "explicit_priority": _score_value(payload, "explicit_priority"),
                    "urgency": _score_value(payload, "urgency"),
                    "revenue_relevance": _score_value(payload, "revenue_relevance"),
                    "unblock_value": _score_value(payload, "unblock_value"),
                    "consequence": _score_value(payload, "consequence"),
                    "aging": _score_value(payload, "aging"),
                    "effort_efficiency": _score_value(payload, "effort_efficiency"),
                    "strategic_leverage": _score_value(payload, "strategic_leverage"),
                    "dcs_override": _score_value(payload, "dcs_override"),
                    "due_at": payload.get("due_at"),
                    "source_system": source_system,
                    "source_id": source_id,
                    "normalized_intent": normalized_intent,
                    "source_refs": [source_ref],
                    "evidence_refs": list(payload.get("evidence_refs") or []),
                }
                item = repo.create_item(item_payload)
                self._json(201, {"ok": True, "deduped": False, "item": item}, origin)
                return

            if path == "/api/escd/items/transition":
                item_id = str(payload.get("item_id") or "").strip()
                target = str(payload.get("status") or "").strip()
                if not item_id or not target:
                    self._json(400, {"error": "item_id_and_status_required"}, origin)
                    return
                item = repo.get_item(item_id)
                if not item:
                    self._json(404, {"error": "item_not_found"}, origin)
                    return
                allowed, reason = transition_allowed("item", str(item.get("status") or ""), target)
                if not allowed:
                    raise RuntimeRuleError(reason)
                update = {"status": target}
                if target in {"planned", "active"}:
                    update["actionable"] = True
                elif target in {"completed", "cancelled", "archived"}:
                    update["actionable"] = False
                updated = repo.patch_item(item_id, update)
                self._json(200, {"ok": True, "item": updated}, origin)
                return

            if path == "/api/escd/projects":
                title = str(payload.get("title") or "").strip()
                project_key = str(payload.get("project_key") or "").strip()
                source_refs = [str(x).strip() for x in payload.get("source_refs", []) if str(x).strip()]
                if not title or not project_key or not source_refs:
                    self._json(400, {"error": "project_identity_and_source_required"}, origin)
                    return
                project = repo.create_project({
                    "project_key": project_key,
                    "title": title,
                    "objective": payload.get("objective"),
                    "status": str(payload.get("status") or "active"),
                    "source_refs": source_refs,
                })
                self._json(201, {"ok": True, "project": project}, origin)
                return

            if path == "/api/escd/decisions":
                question = str(payload.get("question") or "").strip()
                source_refs = [str(x).strip() for x in payload.get("source_refs", []) if str(x).strip()]
                if not question or not source_refs:
                    self._json(400, {"error": "decision_question_and_source_required"}, origin)
                    return
                decision_key = str(payload.get("decision_key") or _stable_key("escd-decision-v1-", question, source_refs))
                contract_input = {
                    "decision_id": decision_key,
                    "facts": payload.get("facts", []),
                    "unknowns": payload.get("unknowns", []),
                    "alternatives": payload.get("alternatives", []),
                    "tradeoffs": payload.get("tradeoffs", []),
                    "recommendation": payload.get("recommendation"),
                    "decision": payload.get("decision"),
                    "evidence_refs": payload.get("evidence_refs", []),
                    "execution_evidence_ref": payload.get("execution_evidence_ref"),
                }
                decision_contract(contract_input)
                decision = repo.create_decision({
                    "decision_key": decision_key,
                    "item_id": payload.get("item_id"),
                    "question": question,
                    "facts": contract_input["facts"],
                    "unknowns": contract_input["unknowns"],
                    "alternatives": contract_input["alternatives"],
                    "tradeoffs": contract_input["tradeoffs"],
                    "recommendation": contract_input["recommendation"],
                    "decision": contract_input["decision"],
                    "evidence_refs": contract_input["evidence_refs"],
                    "execution_evidence_ref": contract_input["execution_evidence_ref"],
                    "source_refs": source_refs,
                })
                self._json(201, {"ok": True, "decision": decision}, origin)
                return

            if path == "/api/escd/contacts/context":
                contract = contact_context_contract(payload)
                contact_ref = str(contract.get("contact_ref") or "").strip()
                if not contact_ref:
                    self._json(400, {"error": "contact_ref_required"}, origin)
                    return
                context_key = str(payload.get("context_key") or _stable_key(
                    "escd-contact-v1-", contact_ref, contract.get("provenance_refs"), payload.get("last_reconciled_at")
                ))
                row = repo.create_contact_context({
                    "context_key": context_key,
                    "contact_ref": contact_ref,
                    "display_name": contract.get("display_name"),
                    "organization": contract.get("organization"),
                    "role": contract.get("role"),
                    "relationship_context": contract.get("relationship_context"),
                    "active_commitments": contract.get("active_commitments"),
                    "waiting_on_them": contract.get("waiting_on_them"),
                    "they_are_waiting_on_dcs": contract.get("they_are_waiting_on_dcs"),
                    "recent_interaction_refs": contract.get("recent_interaction_refs"),
                    "next_follow_up_at": contract.get("next_follow_up_at"),
                    "communication_preferences": contract.get("communication_preferences"),
                    "important_dates": contract.get("important_dates"),
                    "notes": contract.get("notes"),
                    "provenance_refs": contract.get("provenance_refs"),
                    "confidence_status": contract.get("confidence_status"),
                })
                self._json(201, {"ok": True, "person_context": row, "source_of_truth_overwrite_performed": False}, origin)
                return

            if path == "/api/escd/routines":
                routine_key = str(payload.get("routine_key") or "").strip()
                mission = str(payload.get("mission") or "").strip()
                purpose = str(payload.get("purpose") or "").strip()
                trigger_type = str(payload.get("trigger_type") or "").strip()
                autonomy_class = str(payload.get("autonomy_class") or "").strip()
                source_refs = [str(x).strip() for x in payload.get("source_refs", []) if str(x).strip()]
                if not routine_key or not mission or not purpose or not trigger_type or not autonomy_class or not source_refs:
                    self._json(400, {"error": "routine_contract_incomplete"}, origin)
                    return
                row = repo.create_routine({
                    "routine_key": routine_key,
                    "version": int(payload.get("version") or 1),
                    "mission": mission,
                    "purpose": purpose,
                    "trigger_type": trigger_type,
                    "trigger_spec": payload.get("trigger_spec", {}),
                    "autonomy_class": autonomy_class,
                    "source_refs": source_refs,
                    "action_template": payload.get("action_template", {}),
                    "approval_required": bool(payload.get("approval_required", False)),
                    "expected_evidence": payload.get("expected_evidence", []),
                    "failure_policy": payload.get("failure_policy", {}),
                    "escalation_class": payload.get("escalation_class", "N1"),
                    "last_run_at": payload.get("last_run_at"),
                    "next_run_at": payload.get("next_run_at"),
                    "paused": bool(payload.get("paused", False)),
                    "cancelled": bool(payload.get("cancelled", False)),
                })
                self._json(201, {"ok": True, "routine": row}, origin)
                return

            if path == "/api/escd/routines/evaluate":
                result = routine_contract(payload, payload.get("prior_run_key"))
                self._json(200, {"ok": True, "routine_evaluation": result}, origin)
                return

            if path == "/api/escd/notifications/evaluate":
                result = notification_contract(payload)
                intent = None
                if result["notify"]:
                    source_event_ref = str(payload.get("source_event_ref") or "").strip()
                    if not source_event_ref:
                        self._json(400, {"error": "notification_source_event_required"}, origin)
                        return
                    notification_key = str(payload.get("notification_key") or _stable_key(
                        "escd-notify-v1-",
                        payload.get("key"),
                        source_event_ref,
                        result["notification_class"],
                        payload.get("current_value"),
                    ))
                    intent = repo.create_notification_intent({
                        "notification_key": notification_key,
                        "notification_class": result["notification_class"],
                        "source_event_ref": source_event_ref,
                        "item_id": payload.get("item_id"),
                        "reason": result["reason"],
                        "channel": result["channel"],
                        "state": "created",
                        "payload": {"key": payload.get("key"), "current_value": payload.get("current_value")},
                    })
                self._json(200, {
                    "ok": True,
                    "notification_evaluation": result,
                    "intent": intent,
                    "delivery_performed": False,
                }, origin)
                return

            if path == "/api/escd/calendar/conflicts":
                result = calendar_contract(payload.get("events", []), int(payload.get("buffer_minutes") or 0))
                self._json(200, {"ok": True, "calendar": result}, origin)
                return

            if path == "/api/escd/calendar/meeting-prep":
                result = meeting_prep_contract(payload)
                self._json(200, {"ok": True, "meeting_prep": result}, origin)
                return

            if path == "/api/escd/communications/triage":
                result = communication_contract(payload)
                self._json(200, {"ok": True, "communication": result}, origin)
                return

            if path == "/api/escd/commands/parse":
                result = command_contract(str(payload.get("text") or ""))
                self._json(200, {"ok": True, "command": result}, origin)
                return

            if path == "/api/escd/files/route":
                result = file_route_contract(payload)
                self._json(200, {"ok": True, "file_route": result}, origin)
                return

            if path == "/api/escd/mobile/action":
                result = mobile_action_contract(payload)
                self._json(200, {"ok": True, "mobile_action": result}, origin)
                return

            if path == "/api/escd/recovery/evaluate":
                result = retry_contract(payload)
                self._json(200, {"ok": True, "recovery": result}, origin)
                return

            if path == "/api/escd/approvals/decide":
                approval_id = str(payload.get("approval_id") or "")
                decision = str(payload.get("decision") or "")
                if not approval_id or not decision:
                    self._json(400, {"error": "approval_id_and_decision_required"}, origin)
                    return
                approval = repo.get_approval(approval_id)
                if not approval:
                    self._json(404, {"error": "approval_not_found"}, origin)
                    return
                update = require_approval_decision(approval, decision, auth.user_id)
                updated = repo.patch_approval(approval_id, update)
                self._json(200, {"ok": True, "approval": updated}, origin)
                return

            if path == "/api/escd/briefing/ack":
                acknowledged_through = str(payload.get("acknowledged_through") or "")
                if not acknowledged_through:
                    self._json(400, {"error": "acknowledged_through_required"}, origin)
                    return
                acknowledged_dt = _parse_ack_timestamp(acknowledged_through)
                prior = repo.last_briefing_ack()
                if prior:
                    prior_dt = _parse_ack_timestamp(str(prior.get("acknowledged_through") or ""))
                    if acknowledged_dt < prior_dt:
                        raise RuntimeRuleError("briefing_ack_regression")
                ack = repo.acknowledge_briefing(acknowledged_dt.isoformat())
                self._json(201, {"ok": True, "ack": ack}, origin)
                return

            self._json(404, {"error": "not_found"}, origin)
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)}, origin)
        except RuntimeRuleError as exc:
            self._json(409, {"error": str(exc)}, origin)
        except RepositoryError as exc:
            self._json(502, {"error": str(exc)}, origin)
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid_json"}, origin)
        except (ValueError, TypeError) as exc:
            self._json(400, {"error": str(exc)}, origin)
        except Exception:
            self._json(500, {"error": "internal_error"}, origin)
