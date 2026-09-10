from __future__ import annotations

import json
from typing import Any
from urllib import request, error, parse


class RepositoryError(RuntimeError):
    pass


class SupabaseRLSClient:
    """User-scoped PostgREST client. Uses the caller JWT so RLS evaluates auth.uid()."""

    def __init__(self, supabase_url: str, anon_key: str, access_token: str, schema: str = "dcse_cp"):
        if not supabase_url or not anon_key or not access_token:
            raise RepositoryError("repository_configuration_missing")
        self.base = supabase_url.rstrip("/") + "/rest/v1"
        self.anon_key = anon_key
        self.access_token = access_token
        self.schema = schema

    def _headers(self, write: bool = False) -> dict[str, str]:
        headers = {
            "apikey": self.anon_key,
            "Authorization": f"Bearer {self.access_token}",
            "Accept-Profile": self.schema,
            "Content-Type": "application/json",
        }
        if write:
            headers["Content-Profile"] = self.schema
            headers["Prefer"] = "return=representation"
        return headers

    def _call(self, method: str, path: str, payload: Any = None) -> Any:
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        req = request.Request(
            self.base + "/" + path.lstrip("/"),
            data=body,
            headers=self._headers(write=method != "GET"),
            method=method,
        )
        try:
            with request.urlopen(req, timeout=15) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw or "[]")
        except error.HTTPError as exc:
            exc.read()
            raise RepositoryError(f"postgrest_{exc.code}") from None

    def operator_self(self) -> list[dict[str, Any]]:
        return self._call("GET", "operator_accounts?select=user_id,email,active,access_scope")

    def list_jobs(self) -> list[dict[str, Any]]:
        return self._call("GET", "escd_jobs?select=*&order=updated_at.desc,id.asc&limit=200")

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        safe = parse.quote(str(job_id), safe="")
        rows = self._call("GET", f"escd_jobs?id=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def patch_job(self, job_id: str, update: dict[str, Any]) -> dict[str, Any]:
        safe = parse.quote(str(job_id), safe="")
        rows = self._call("PATCH", f"escd_jobs?id=eq.{safe}", update)
        if not rows:
            raise RepositoryError("job_update_failed")
        return rows[0]

    def list_job_evidence(self, job_id: str) -> list[dict[str, Any]]:
        safe = parse.quote(str(job_id), safe="")
        return self._call("GET", f"escd_evidence?job_id=eq.{safe}&select=id,evidence_type,reference_sha,created_at&order=created_at.desc,id.asc")

    def latest_approval(self, job_id: str, action_key: str) -> dict[str, Any] | None:
        safe_job = parse.quote(str(job_id), safe="")
        safe_action = parse.quote(str(action_key), safe="")
        rows = self._call(
            "GET",
            f"escd_approvals?job_id=eq.{safe_job}&action_key=eq.{safe_action}&select=*&order=requested_at.desc,id.desc&limit=1",
        )
        return rows[0] if rows else None

    def list_pending_approvals(self) -> list[dict[str, Any]]:
        return self._call("GET", "escd_approvals?status=eq.pending&select=*&order=requested_at.desc,id.desc")

    def list_events_since(self, timestamp: str | None) -> list[dict[str, Any]]:
        if not timestamp:
            return self._call("GET", "escd_job_events?select=*&order=created_at.desc,id.asc&limit=200")
        safe = parse.quote(timestamp, safe=":-+.TZ")
        return self._call("GET", f"escd_job_events?created_at=gt.{safe}&select=*&order=created_at.desc,id.asc&limit=200")

    def last_briefing_ack(self) -> dict[str, Any] | None:
        rows = self._call("GET", "escd_briefing_acks?select=*&order=acknowledged_at.desc,id.desc&limit=1")
        return rows[0] if rows else None

    def patch_approval(self, approval_id: str, update: dict[str, Any]) -> dict[str, Any]:
        safe = parse.quote(str(approval_id), safe="")
        rows = self._call("PATCH", f"escd_approvals?id=eq.{safe}", update)
        if not rows:
            raise RepositoryError("approval_update_failed")
        return rows[0]

    def acknowledge_briefing(self, acknowledged_through: str) -> dict[str, Any]:
        rows = self._call("POST", "escd_briefing_acks", {"acknowledged_through": acknowledged_through})
        if not rows:
            raise RepositoryError("briefing_ack_failed")
        return rows[0]
