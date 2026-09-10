from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import hashlib
import json
import os
from datetime import datetime, timezone
from urllib.parse import urlparse

from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient, RepositoryError
from apps.escd.runtime.service import (
    RuntimeRuleError,
    require_job_transition,
    require_approval_decision,
    next_best_action,
    briefing_snapshot,
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


class handler(BaseHTTPRequestHandler):
    server_version = "ESCD/0.3"

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
            self._json(200, {"ok": True, "service": "escd", "version": "0.3"}, origin)
            return

        try:
            auth, repo = self._authorized()
            if path == "/api/escd/jobs":
                self._json(200, {"ok": True, "jobs": repo.list_jobs()}, origin)
                return
            if path == "/api/escd/next-action":
                jobs = repo.list_jobs()
                self._json(200, {"ok": True, "next_action": next_best_action(jobs)}, origin)
                return
            if path == "/api/escd/approvals":
                self._json(200, {"ok": True, "approvals": repo.list_pending_approvals()}, origin)
                return
            if path == "/api/escd/briefing":
                ack = repo.last_briefing_ack()
                since = ack.get("acknowledged_through") if ack else None
                jobs = repo.list_jobs()
                events = repo.list_events_since(since)
                approvals = repo.list_pending_approvals()
                completed = [
                    j for j in jobs
                    if j.get("status") == "completed"
                    and (not since or str(j.get("completed_at") or "") > since)
                ]
                blockers = [j for j in jobs if j.get("blocked") or j.get("status") == "failed"]
                watches = [j for j in jobs if j.get("future_trigger")]
                snapshot = briefing_snapshot(
                    changed=events,
                    completed=completed,
                    approvals=approvals,
                    due_or_at_risk=[],
                    blockers=blockers,
                    watches=watches,
                    jobs=jobs,
                )
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
        except Exception:
            self._json(500, {"error": "internal_error"}, origin)
