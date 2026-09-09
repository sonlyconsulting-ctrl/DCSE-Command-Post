from __future__ import annotations

from http.server import BaseHTTPRequestHandler
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


def _allowed_origin(origin: str | None) -> str | None:
    configured = [x.strip() for x in os.getenv("ESCD_ALLOWED_ORIGINS", "").split(",") if x.strip()]
    if not origin or origin not in configured:
        return None
    return origin


class handler(BaseHTTPRequestHandler):
    server_version = "ESCD/0.2"

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
            self._json(200, {"ok": True, "service": "escd", "version": "0.2"}, origin)
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
                approval = repo.latest_approval(job_id)
                approved = bool(approval and approval.get("status") == "approved")
                update = require_job_transition(
                    job,
                    target,
                    evidence_refs=[str(e.get("id")) for e in evidence],
                    exit_criteria_met=bool(payload.get("exit_criteria_met")),
                    approved=approved,
                )
                updated = repo.patch_job(job_id, update)
                self._json(200, {"ok": True, "job": updated}, origin)
                return

            if path == "/api/escd/approvals/decide":
                approval_id = str(payload.get("approval_id") or "")
                decision = str(payload.get("decision") or "")
                if not approval_id or not decision:
                    self._json(400, {"error": "approval_id_and_decision_required"}, origin)
                    return
                rows = repo._call("GET", f"escd_approvals?id=eq.{approval_id}&select=*&limit=1")
                if not rows:
                    self._json(404, {"error": "approval_not_found"}, origin)
                    return
                update = require_approval_decision(rows[0], decision, auth.user_id)
                updated = repo.patch_approval(approval_id, update)
                self._json(200, {"ok": True, "approval": updated}, origin)
                return

            if path == "/api/escd/briefing/ack":
                acknowledged_through = str(payload.get("acknowledged_through") or "")
                if not acknowledged_through:
                    self._json(400, {"error": "acknowledged_through_required"}, origin)
                    return
                ack = repo.acknowledge_briefing(acknowledged_through)
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
