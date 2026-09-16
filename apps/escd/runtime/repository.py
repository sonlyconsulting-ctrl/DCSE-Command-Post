from __future__ import annotations

import json
from typing import Any
from urllib import request, error, parse
import uuid


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
        self.user_id: str | None = None

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


    def _rpc(self, name: str, payload: dict[str, Any]) -> Any:
        return self._call("POST", f"rpc/{name}", payload)

    @staticmethod
    def _one(value: Any) -> dict[str, Any] | None:
        if isinstance(value, list):
            return value[0] if value else None
        return value if isinstance(value, dict) else None

    # Persistent ESCD conversation / orchestration memory.
    def create_conversation(self, title: str, *, external_ref: str | None = None,
                            metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "external_ref": external_ref or f"ESCD-{uuid.uuid4().hex[:16].upper()}",
            "title": (str(title or "ESCD Conversation").strip() or "ESCD Conversation")[:180],
            "lane": "DCSE",
            "confidentiality": "internal",
            "status": "planned",
            "source_system": "ESCD",
            "metadata": metadata or {},
        }
        if self.user_id:
            payload["created_by"] = self.user_id
            payload["updated_by"] = self.user_id
        rows = self._call("POST", "conversations", payload)
        row = self._one(rows)
        if not row:
            raise RepositoryError("conversation_create_failed")
        return row

    def list_conversations(self, limit: int = 50) -> list[dict[str, Any]]:
        rows = self._rpc("escd_recent_conversations", {"p_limit": max(1, min(int(limit), 200))})
        return rows if isinstance(rows, list) else []

    def conversation_snapshot(self, conversation_id: str) -> dict[str, Any]:
        data = self._rpc("escd_conversation_snapshot", {"p_conversation_id": conversation_id})
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        if not row:
            raise RepositoryError("conversation_not_found")
        return row

    def append_conversation_turn(self, conversation_id: str, actor_label: str,
                                 actor_role: str, summary: str,
                                 metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        data = self._rpc("escd_append_conversation_turn", {
            "p_conversation_id": conversation_id,
            "p_actor_label": actor_label,
            "p_actor_role": actor_role,
            "p_summary": summary,
            "p_metadata": metadata or {},
        })
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        if not row:
            raise RepositoryError("conversation_turn_create_failed")
        return row

    def resolve_subjects(self, text: str, limit: int = 10) -> list[dict[str, Any]]:
        rows = self._rpc("escd_resolve_subjects", {
            "p_text": str(text or ""),
            "p_limit": max(1, min(int(limit), 50)),
        })
        return rows if isinstance(rows, list) else []

    def link_subject(self, subject_id: str, object_type: str, object_ref: str,
                     relation_type: str = "RELATED", confidence: float = 1.0,
                     provenance: dict[str, Any] | None = None) -> dict[str, Any] | None:
        payload: dict[str, Any] = {
            "subject_id": subject_id,
            "object_type": object_type,
            "object_ref": str(object_ref),
            "relation_type": relation_type,
            "confidence": max(0.0, min(float(confidence), 1.0)),
            "provenance": provenance or {},
        }
        if self.user_id:
            payload["created_by_user_id"] = self.user_id
        try:
            rows = self._call("POST", "escd_subject_links", payload)
        except RepositoryError as exc:
            if str(exc) == "postgrest_409":
                return None
            raise
        return self._one(rows)

    def create_turn_classification(self, payload: dict[str, Any]) -> dict[str, Any]:
        body = dict(payload)
        if self.user_id:
            body["created_by_user_id"] = self.user_id
        try:
            rows = self._call("POST", "escd_turn_classifications", body)
        except RepositoryError as exc:
            if str(exc) == "postgrest_409":
                turn_id = parse.quote(str(body.get("conversation_turn_id") or ""), safe="")
                existing = self._call("GET", f"escd_turn_classifications?conversation_turn_id=eq.{turn_id}&select=*&limit=1")
                row = self._one(existing)
                if row:
                    return row
            raise
        row = self._one(rows)
        if not row:
            raise RepositoryError("turn_classification_create_failed")
        return row

    def materialize_classification(self, classification_id: str, force: bool = False) -> dict[str, Any]:
        data = self._rpc("escd_materialize_classification", {
            "p_classification_id": classification_id,
            "p_force": bool(force),
        })
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        return row or {}

    def list_dynamic_knowledge(self, limit: int = 200) -> list[dict[str, Any]]:
        return self._call(
            "GET",
            "escd_knowledge_records?select=*&order=updated_at.desc,id.asc&limit="
            + str(max(1, min(int(limit), 500))),
        )

    def submit_operation_turn(self, conversation_id: str, request_turn_id: str,
                              request_text: str, provider_preference: str | None,
                              request_payload: dict[str, Any] | None = None) -> dict[str, Any]:
        data = self._rpc("escd_submit_operation_turn", {
            "p_conversation_id": conversation_id,
            "p_request_turn_id": request_turn_id,
            "p_request_text": request_text,
            "p_provider_preference": provider_preference,
            "p_request_payload": request_payload or {},
        })
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        if not row:
            raise RepositoryError("operation_turn_submit_failed")
        return row

    def operation_turn_snapshot(self, turn_key: str) -> dict[str, Any]:
        data = self._rpc("escd_operation_turn_snapshot", {"p_turn_key": turn_key})
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        if not row:
            raise RepositoryError("operation_turn_not_found")
        return row

    def control_operation_turn(self, turn_key: str, action: str,
                               response_text: str = "") -> dict[str, Any]:
        data = self._rpc("escd_user_control_turn", {
            "p_turn_key": turn_key,
            "p_action": action,
            "p_response_text": response_text,
        })
        row = self._one(data)
        if row is None and isinstance(data, dict):
            row = data
        if not row:
            raise RepositoryError("operation_turn_control_failed")
        return row

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

    def get_evidence(self, evidence_id: str) -> dict[str, Any] | None:
        safe = parse.quote(str(evidence_id), safe="")
        rows = self._call("GET", f"escd_evidence?id=eq.{safe}&select=id,job_id,evidence_type,reference_sha,created_at&limit=1")
        return rows[0] if rows else None

    def latest_approval(self, job_id: str, action_key: str) -> dict[str, Any] | None:
        safe_job = parse.quote(str(job_id), safe="")
        safe_action = parse.quote(str(action_key), safe="")
        rows = self._call(
            "GET",
            f"escd_approvals?job_id=eq.{safe_job}&action_key=eq.{safe_action}&select=*&order=requested_at.desc,id.desc&limit=1",
        )
        return rows[0] if rows else None

    def get_approval(self, approval_id: str) -> dict[str, Any] | None:
        safe = parse.quote(str(approval_id), safe="")
        rows = self._call("GET", f"escd_approvals?id=eq.{safe}&select=*&limit=1")
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

    def get_job_verification(self, verification_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(verification_key), safe="")
        rows = self._call("GET", f"escd_job_verifications?verification_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_job_verification(
        self,
        *,
        verification_key: str,
        job_id: str,
        evidence_id: str,
        outcome: str,
        verification_method: str,
        notes: str | None = None,
    ) -> dict[str, Any]:
        existing = self.get_job_verification(verification_key)
        if existing:
            return existing
        payload: dict[str, Any] = {
            "verification_key": verification_key,
            "job_id": job_id,
            "evidence_id": evidence_id,
            "outcome": outcome,
            "verification_method": verification_method,
        }
        if notes:
            payload["notes"] = notes
        try:
            rows = self._call("POST", "escd_job_verifications", payload)
        except RepositoryError as exc:
            if str(exc) == "postgrest_409":
                existing = self.get_job_verification(verification_key)
                if existing:
                    return existing
            raise
        if not rows:
            raise RepositoryError("job_verification_create_failed")
        return rows[0]

    def acknowledge_briefing(self, acknowledged_through: str) -> dict[str, Any]:
        rows = self._call("POST", "escd_briefing_acks", {"acknowledged_through": acknowledged_through})
        if not rows:
            raise RepositoryError("briefing_ack_failed")
        return rows[0]

    # Integrated Executive Stream + Personal Assistant state.
    def list_items(self) -> list[dict[str, Any]]:
        return self._call("GET", "escd_items?select=*&order=updated_at.desc,id.asc&limit=500")

    def get_item(self, item_id: str) -> dict[str, Any] | None:
        safe = parse.quote(str(item_id), safe="")
        rows = self._call("GET", f"escd_items?id=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def get_item_by_key(self, item_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(item_key), safe="")
        rows = self._call("GET", f"escd_items?item_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_item(self, payload: dict[str, Any]) -> dict[str, Any]:
        item_key = str(payload.get("item_key") or "")
        if not item_key:
            raise RepositoryError("item_key_required")
        existing = self.get_item_by_key(item_key)
        if existing:
            return existing
        try:
            rows = self._call("POST", "escd_items", payload)
        except RepositoryError as exc:
            if str(exc) == "postgrest_409":
                existing = self.get_item_by_key(item_key)
                if existing:
                    return existing
            raise
        if not rows:
            raise RepositoryError("item_create_failed")
        return rows[0]

    def patch_item(self, item_id: str, update: dict[str, Any]) -> dict[str, Any]:
        safe = parse.quote(str(item_id), safe="")
        rows = self._call("PATCH", f"escd_items?id=eq.{safe}", update)
        if not rows:
            raise RepositoryError("item_update_failed")
        return rows[0]

    def delete_item(self, item_id: str) -> bool:
        safe = parse.quote(str(item_id), safe="")
        self._call("DELETE", f"escd_items?id=eq.{safe}")
        return True

    def list_item_events_since(self, timestamp: str | None) -> list[dict[str, Any]]:
        if not timestamp:
            return self._call("GET", "escd_item_events?select=*&order=created_at.desc,id.asc&limit=300")
        safe = parse.quote(timestamp, safe=":-+.TZ")
        return self._call("GET", f"escd_item_events?created_at=gt.{safe}&select=*&order=created_at.desc,id.asc&limit=300")

    def get_project_by_key(self, project_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(project_key), safe="")
        rows = self._call("GET", f"escd_projects?project_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_project(self, payload: dict[str, Any]) -> dict[str, Any]:
        project_key = str(payload.get("project_key") or "")
        if not project_key:
            raise RepositoryError("project_key_required")
        existing = self.get_project_by_key(project_key)
        if existing:
            return existing
        rows = self._call("POST", "escd_projects", payload)
        if not rows:
            raise RepositoryError("project_create_failed")
        return rows[0]

    def get_decision_by_key(self, decision_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(decision_key), safe="")
        rows = self._call("GET", f"escd_decisions?decision_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_decision(self, payload: dict[str, Any]) -> dict[str, Any]:
        decision_key = str(payload.get("decision_key") or "")
        if not decision_key:
            raise RepositoryError("decision_key_required")
        existing = self.get_decision_by_key(decision_key)
        if existing:
            return existing
        rows = self._call("POST", "escd_decisions", payload)
        if not rows:
            raise RepositoryError("decision_create_failed")
        return rows[0]

    def get_contact_context_by_key(self, context_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(context_key), safe="")
        rows = self._call("GET", f"escd_contact_contexts?context_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_contact_context(self, payload: dict[str, Any]) -> dict[str, Any]:
        context_key = str(payload.get("context_key") or "")
        if not context_key:
            raise RepositoryError("context_key_required")
        existing = self.get_contact_context_by_key(context_key)
        if existing:
            return existing
        rows = self._call("POST", "escd_contact_contexts", payload)
        if not rows:
            raise RepositoryError("contact_context_create_failed")
        return rows[0]

    def get_routine(self, routine_key: str, version: int) -> dict[str, Any] | None:
        safe_key = parse.quote(str(routine_key), safe="")
        safe_version = parse.quote(str(int(version)), safe="")
        rows = self._call("GET", f"escd_routines?routine_key=eq.{safe_key}&version=eq.{safe_version}&select=*&limit=1")
        return rows[0] if rows else None

    def create_routine(self, payload: dict[str, Any]) -> dict[str, Any]:
        routine_key = str(payload.get("routine_key") or "")
        version = int(payload.get("version") or 1)
        if not routine_key:
            raise RepositoryError("routine_key_required")
        existing = self.get_routine(routine_key, version)
        if existing:
            return existing
        rows = self._call("POST", "escd_routines", payload)
        if not rows:
            raise RepositoryError("routine_create_failed")
        return rows[0]

    def patch_routine(self, routine_id: str, update: dict[str, Any]) -> dict[str, Any]:
        safe = parse.quote(str(routine_id), safe="")
        rows = self._call("PATCH", f"escd_routines?id=eq.{safe}", update)
        if not rows:
            raise RepositoryError("routine_update_failed")
        return rows[0]

    def get_notification_intent(self, notification_key: str) -> dict[str, Any] | None:
        safe = parse.quote(str(notification_key), safe="")
        rows = self._call("GET", f"escd_notification_intents?notification_key=eq.{safe}&select=*&limit=1")
        return rows[0] if rows else None

    def create_notification_intent(self, payload: dict[str, Any]) -> dict[str, Any]:
        key = str(payload.get("notification_key") or "")
        if not key:
            raise RepositoryError("notification_key_required")
        existing = self.get_notification_intent(key)
        if existing:
            return existing
        rows = self._call("POST", "escd_notification_intents", payload)
        if not rows:
            raise RepositoryError("notification_intent_create_failed")
        return rows[0]
