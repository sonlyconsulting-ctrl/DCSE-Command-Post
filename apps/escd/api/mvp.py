from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import hashlib
import json
import os
from urllib import request, error
from urllib.parse import urlparse, parse_qs

from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient, RepositoryError
from apps.escd.runtime.mvp_data import (
    MVPServiceError,
    chat,
    list_assets,
    create_asset,
    patch_asset,
    delete_asset,
    list_ddna_jobs,
    list_ddna_sources,
    create_ddna_source,
    patch_ddna_source,
    delete_ddna_source,
    list_knowledge,
    search_knowledge,
    create_signed_attachment_upload,
    finalize_file_attachment,
    create_signed_attachment_download,
    delete_record_attachment,
    provider_status,
    set_provider_secret,
    update_provider_config,
    create_orchestration_turn,
    get_orchestration_turn,
    update_orchestration_turn_action,
)


class handler(BaseHTTPRequestHandler):
    server_version = "ESCD-MVP/0.4"

    def _json(self, status: int, payload: dict):
        raw = json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self) -> dict:
        size = int(self.headers.get("Content-Length") or 0)
        if size < 1:
            return {}
        if size > 10_000_000:
            raise MVPServiceError("payload_too_large")
        raw = self.rfile.read(size)
        try:
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict):
                raise MVPServiceError("invalid_json")
            return data
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise MVPServiceError("invalid_json") from exc

    def _supabase_config(self):
        url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        anon = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
        if not url or not anon:
            raise AuthError("auth_configuration_missing")
        return url.rstrip("/"), anon

    def _repo_for_token(self, token: str):
        url, anon = self._supabase_config()
        auth = verify_supabase_user(token, url, anon)
        repo = SupabaseRLSClient(url, anon, token, schema="dcse_cp")
        authorize_operator(auth, repo.operator_self())
        return auth, repo

    def _auth(self):
        return self._repo_for_token(extract_bearer(self.headers))[1]

    def _login(self, payload: dict):
        email_value = str(payload.get("email") or "").strip().lower()
        password = str(payload.get("password") or "")
        if not email_value or not password:
            raise AuthError("email_and_password_required")
        url, anon = self._supabase_config()
        body = json.dumps({"email": email_value, "password": password}).encode("utf-8")
        req = request.Request(
            url + "/auth/v1/token?grant_type=password",
            data=body,
            headers={"apikey": anon, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=15) as response:
                session = json.loads(response.read().decode("utf-8") or "{}")
        except error.HTTPError:
            raise AuthError("sign_in_failed") from None
        token = str(session.get("access_token") or "")
        if not token:
            raise AuthError("sign_in_failed")
        auth, _ = self._repo_for_token(token)
        return {"access_token": token, "expires_in": int(session.get("expires_in") or 3600), "user": {"email": auth.email}}

    def _patch_item_governed(self, repo: SupabaseRLSClient, item_id: str, update: dict):
        current = repo.get_item(item_id)
        if not current:
            raise RepositoryError("item_not_found")
        target = update.get("status")
        if not target or target == current.get("status"):
            return repo.patch_item(item_id, update)
        current_status = str(current.get("status") or "")
        if target == "active" and current_status == "captured":
            first = dict(update)
            first["status"] = "triaged"
            repo.patch_item(item_id, first)
            return repo.patch_item(item_id, {"status": "active"})
        if target == "completed" and current_status == "captured":
            repo.patch_item(item_id, {"status": "triaged"})
            repo.patch_item(item_id, {"status": "active"})
            rest = dict(update)
            rest["status"] = "completed"
            return repo.patch_item(item_id, rest)
        if target == "archived" and current_status not in {"completed", "cancelled"}:
            first = dict(update)
            first["status"] = "cancelled"
            repo.patch_item(item_id, first)
            return repo.patch_item(item_id, {"status": "archived"})
        return repo.patch_item(item_id, update)

    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        if path == "/api/mvp/health":
            self._json(200, {"ok": True, "service": "escd-mvp", "version": "0.4", "providers": provider_status()})
            return
        try:
            repo = self._auth()
            if path == "/api/mvp/items":
                self._json(200, {"ok": True, "items": repo.list_items()})
            elif path == "/api/mvp/assets":
                self._json(200, {"ok": True, "assets": list_assets()})
            elif path == "/api/mvp/ddna":
                self._json(200, {"ok": True, "records": list_ddna_sources()})
            elif path == "/api/mvp/ddna/jobs":
                source_id = str((query.get("source_id") or [""])[0])
                self._json(200, {"ok": True, "jobs": list_ddna_jobs(source_id) if source_id else []})
            elif path == "/api/mvp/knowledge":
                q = str((query.get("q") or [""])[0])
                if q:
                    self._json(200, {"ok": True, "knowledge": search_knowledge(q)})
                else:
                    self._json(200, {"ok": True, "knowledge": list_knowledge()})
            elif path == "/api/mvp/providers":
                self._json(200, {"ok": True, "providers": provider_status()})
            elif path.startswith("/api/mvp/orchestrate/turn/"):
                turn_id = path[len("/api/mvp/orchestrate/turn/"):].strip("/")
                self._json(200, {"ok": True, "turn": get_orchestration_turn(turn_id)})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
        except MVPServiceError as exc:
            if str(exc) == "invalid_json":
                self._json(400, {"error": "invalid_json"})
            elif str(exc) == "payload_too_large":
                self._json(413, {"error": "payload_too_large"})
            else:
                self._json(400, {"error": str(exc)})
            return

        if path == "/api/mvp/login":
            try:
                self._json(200, {"ok": True, "session": self._login(payload)})
            except AuthError as exc:
                self._json(401, {"error": str(exc)})
            except Exception:
                self._json(500, {"error": "internal_error"})
            return
        try:
            repo = self._auth()
            if path == "/api/mvp/items":
                kind = str(payload.get("kind") or "task").lower()
                if kind not in {"task", "idea"}:
                    self._json(400, {"error": "invalid_kind"}); return
                title = str(payload.get("title") or "").strip()
                if not title:
                    self._json(400, {"error": "title_required"}); return
                key = "mvp-" + hashlib.sha256((kind + "\n" + title.lower()).encode()).hexdigest()
                item = repo.create_item({
                    "item_key": key,
                    "title": title,
                    "summary": payload.get("notes"),
                    "status": "captured" if kind == "idea" else "active",
                    "task_class": "CAPTURE" if kind == "idea" else "DO",
                    "context": kind,
                    "actionable": kind == "task",
                    "explicit_priority": float(payload.get("priority") or 0),
                    "due_at": payload.get("due_at"),
                    "source_system": "escd_mvp",
                    "source_id": key,
                    "normalized_intent": title,
                    "source_refs": ["escd:mvp:" + kind],
                    "evidence_refs": [],
                })
                self._json(201, {"ok": True, "item": item})
            elif path == "/api/mvp/assets":
                self._json(201, {"ok": True, "asset": create_asset(payload)})
            elif path == "/api/mvp/ddna":
                self._json(201, {"ok": True, "record": create_ddna_source(payload)})
            elif path == "/api/mvp/upload":
                self._json(410, {"error": "direct_upload_required"})
            elif path == "/api/mvp/attachments/upload-url":
                res = create_signed_attachment_upload(
                    str(payload.get("file_name") or payload.get("name") or "attachment"),
                    str(payload.get("mime_type") or payload.get("type") or "application/octet-stream"),
                    int(payload.get("size") or 0),
                    str(payload.get("record_type") or "item"),
                    str(payload.get("record_id") or ""),
                )
                self._json(201, {"ok": True, "upload": res})
            elif path == "/api/mvp/attachments/finalize":
                res = finalize_file_attachment(
                    storage_path=str(payload.get("storage_path") or ""),
                    file_name=str(payload.get("file_name") or payload.get("name") or "attachment"),
                    mime_type=str(payload.get("mime_type") or payload.get("type") or "application/octet-stream"),
                    size=int(payload.get("size") or 0),
                    sha256=str(payload.get("sha256") or ""),
                    record_type=str(payload.get("record_type") or "item"),
                    record_id=str(payload.get("record_id") or ""),
                    repo=repo,
                )
                self._json(201, {"ok": True, "attachment": res})
            elif path == "/api/mvp/attachments/download-url":
                res = create_signed_attachment_download(
                    str(payload.get("storage_path") or ""),
                    str(payload.get("file_name") or ""),
                    int(payload.get("expires_in") or 300),
                )
                self._json(200, {"ok": True, "download": res})
            elif path == "/api/mvp/chat":
                self._json(200, {"ok": True, "response": chat(str(payload.get("provider") or "openai"), payload.get("messages") or [])})
            elif path == "/api/mvp/provider-secret":
                provider = str(payload.get("provider") or "").strip().lower()
                secret = str(payload.get("secret") or "")
                result = set_provider_secret(provider, secret)
                self._json(200, {"ok": True, "provider": result})
            elif path == "/api/mvp/orchestrate":
                prompt = str(payload.get("prompt") or "").strip()
                provider = str(payload.get("provider") or "ollama").strip()
                context_refs = payload.get("context_refs") or []
                user_id = getattr(repo, "user_id", None) or "DCS-OPERATOR"
                turn = create_orchestration_turn(prompt=prompt, provider=provider, context_refs=context_refs, user_id=user_id)
                self._json(200, {"ok": True, "turn_id": turn["turn_id"], "turn": turn})
            elif path.startswith("/api/mvp/orchestrate/turn/") and path.endswith("/action"):
                parts = path.strip("/").split("/")
                turn_id = parts[-2]
                action = str(payload.get("action") or "").strip()
                response_text = str(payload.get("response") or "").strip()
                turn = update_orchestration_turn_action(turn_id, action=action, response_text=response_text)
                self._json(200, {"ok": True, "turn": turn})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})

    def do_PATCH(self):
        path = urlparse(self.path).path
        try:
            payload = self._read_json()
        except MVPServiceError as exc:
            if str(exc) == "invalid_json":
                self._json(400, {"error": "invalid_json"})
            elif str(exc) == "payload_too_large":
                self._json(413, {"error": "payload_too_large"})
            else:
                self._json(400, {"error": str(exc)})
            return

        try:
            repo = self._auth()
            if path == "/api/mvp/provider-config":
                provider = str(payload.get("provider") or "").strip().lower()
                allowed = {"enabled", "model", "timeout_seconds", "max_output_tokens", "thinking_level"}
                changes = {k: v for k, v in payload.items() if k in allowed}
                self._json(200, {"ok": True, "provider": update_provider_config(provider, changes)})
                return
            elif path == "/api/mvp/assets":
                asset_id = str(payload.get("id") or payload.get("asset_id") or "")
                if not asset_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "asset": patch_asset(asset_id, payload)})
            elif path == "/api/mvp/ddna":
                source_id = str(payload.get("id") or payload.get("source_ref_id") or "")
                if not source_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "record": patch_ddna_source(source_id, payload)})
            elif path == "/api/mvp/items":
                item_id = str(payload.get("id") or "")
                if not item_id:
                    self._json(400, {"error": "id_required"}); return
                allowed = {"title", "summary", "status", "due_at", "explicit_priority", "actionable", "context", "task_class", "evidence_refs"}
                update = {k: v for k, v in payload.items() if k in allowed}
                self._json(200, {"ok": True, "item": self._patch_item_governed(repo, item_id, update)})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})

    def do_PUT(self):
        return self.do_PATCH()

    def do_DELETE(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        try:
            payload = self._read_json()
        except MVPServiceError:
            payload = {}

        try:
            repo = self._auth()
            if path == "/api/mvp/attachments":
                storage_path = str(payload.get("storage_path") or (query.get("storage_path") or [""])[0])
                record_type = str(payload.get("record_type") or (query.get("record_type") or ["item"])[0])
                record_id = str(payload.get("record_id") or (query.get("record_id") or [""])[0])
                if not storage_path or not record_id:
                    self._json(400, {"error": "storage_path_and_record_id_required"}); return
                delete_record_attachment(
                    storage_path=storage_path,
                    record_type=record_type,
                    record_id=record_id,
                    repo=repo,
                )
                self._json(200, {"ok": True, "deleted": storage_path})
            elif path == "/api/mvp/items":
                item_id = str(payload.get("id") or (query.get("id") or [""])[0])
                if not item_id:
                    self._json(400, {"error": "id_required"}); return
                try:
                    self._patch_item_governed(repo, item_id, {"status": "archived"})
                except Exception:
                    pass
                repo.delete_item(item_id)
                self._json(200, {"ok": True, "deleted": item_id})
            elif path == "/api/mvp/assets":
                asset_id = str(payload.get("id") or payload.get("asset_id") or (query.get("id") or [""])[0])
                if not asset_id:
                    self._json(400, {"error": "id_required"}); return
                delete_asset(asset_id)
                self._json(200, {"ok": True, "deleted": asset_id})
            elif path == "/api/mvp/ddna":
                source_id = str(payload.get("id") or payload.get("source_ref_id") or (query.get("id") or [""])[0])
                if not source_id:
                    self._json(400, {"error": "id_required"}); return
                delete_ddna_source(source_id)
                self._json(200, {"ok": True, "deleted": source_id})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})
