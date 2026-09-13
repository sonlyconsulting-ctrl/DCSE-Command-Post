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
    save_file_attachment,
    provider_status,
    set_provider_secret,
    update_provider_config,
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

    def _read_json(self):
        size = int(self.headers.get("Content-Length") or 0)
        if size < 1 or size > 1_000_000:
            return {}
        return json.loads(self.rfile.read(size).decode("utf-8"))

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
            elif path == "/api/mvp/providers":
                self._json(200, {"ok": True, "providers": provider_status()})
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
        payload = self._read_json()
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
                record_type = str(payload.get("record_type") or "task").lower()
                record_id = str(payload.get("record_id") or "")
                file_name = str(payload.get("file_name") or "attachment.bin")
                file_data = str(payload.get("file_data") or "")
                file_type = str(payload.get("file_type") or "application/octet-stream")
                attachment = save_file_attachment(
                    record_type=record_type,
                    record_id=record_id,
                    file_name=file_name,
                    file_data=file_data,
                    file_type=file_type,
                    repo=repo,
                )
                self._json(201, {"ok": True, "attachment": attachment})
            elif path == "/api/mvp/chat":
                self._json(200, {"ok": True, "response": chat(str(payload.get("provider") or "openai"), payload.get("messages") or [])})
            elif path == "/api/mvp/provider-secret":
                provider = str(payload.get("provider") or "").strip().lower()
                secret = str(payload.get("secret") or "")
                result = set_provider_secret(provider, secret)
                self._json(200, {"ok": True, "provider": result})
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
            repo = self._auth()
            payload = self._read_json()
            if path == "/api/mvp/provider-config":
                provider = str(payload.get("provider") or "").strip().lower()
                allowed = {"enabled", "model", "timeout_seconds", "max_output_tokens", "thinking_level"}
                changes = {k: v for k, v in payload.items() if k in allowed}
                self._json(200, {"ok": True, "provider": update_provider_config(provider, changes)})
                return
            if path == "/api/mvp/items":
                item_id = str(payload.get("id") or "")
                if not item_id:
                    self._json(400, {"error": "id_required"}); return
                allowed = {"title", "summary", "status", "due_at", "explicit_priority", "actionable", "context", "task_class", "notes", "evidence_refs", "source_refs"}
                update = {}
                for k, v in payload.items():
                    if k == "notes" and "summary" not in payload:
                        update["summary"] = v
                    elif k == "priority" and "explicit_priority" not in payload:
                        try:
                            update["explicit_priority"] = float(v)
                        except (TypeError, ValueError):
                            pass
                    elif k in allowed and k not in ("notes", "priority"):
                        update[k] = v
                self._json(200, {"ok": True, "item": self._patch_item_governed(repo, item_id, update)})
            elif path == "/api/mvp/assets":
                asset_id = str(payload.get("id") or payload.get("asset_id") or "")
                if not asset_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "asset": patch_asset(asset_id, payload)})
            elif path == "/api/mvp/ddna":
                source_id = str(payload.get("id") or "")
                if not source_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "record": patch_ddna_source(source_id, payload)})
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
        payload = self._read_json()
        target_id = str((query.get("id") or [payload.get("id") or ""])[0])
        try:
            repo = self._auth()
            if path == "/api/mvp/items":
                if not target_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "item": self._patch_item_governed(repo, target_id, {"status": "archived"})})
            elif path == "/api/mvp/assets":
                asset_id = target_id or str(payload.get("asset_id") or "")
                if not asset_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "deleted": delete_asset(asset_id)})
            elif path == "/api/mvp/ddna":
                if not target_id:
                    self._json(400, {"error": "id_required"}); return
                self._json(200, {"ok": True, "deleted": delete_ddna_source(target_id)})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})

