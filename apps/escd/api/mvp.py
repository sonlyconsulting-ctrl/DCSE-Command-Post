from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import hashlib
import json
import os
import sys
import types
from pathlib import Path
from urllib import request, error
from urllib.parse import urlparse, parse_qs

# Resilient dual-root bootstrap for standalone Vercel deployment
_escd_root = Path(__file__).resolve().parent.parent
if str(_escd_root) not in sys.path:
    sys.path.insert(0, str(_escd_root))
_monorepo_root = _escd_root.parent.parent
if _monorepo_root.exists() and str(_monorepo_root) not in sys.path:
    sys.path.insert(0, str(_monorepo_root))

if "apps.escd" not in sys.modules:
    try:
        import runtime  # type: ignore
        _apps_mod = sys.modules.setdefault("apps", types.ModuleType("apps"))
        _escd_mod = sys.modules.setdefault("apps.escd", types.ModuleType("apps.escd"))
        _apps_mod.escd = _escd_mod
        _escd_mod.runtime = runtime
        sys.modules["apps.escd.runtime"] = runtime
    except ImportError:
        pass

from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient, RepositoryError
from apps.escd.runtime.mvp_data import (
    MVPServiceError,
    canonical_item_payload,
    canonical_record,
    chat,
    create_asset,
    create_knowledge,
    is_uuid,
    merge_live_and_canonical,
    orchestrator_agents,
    orchestrator_reply,
    orchestrator_send,
    orchestrator_threads,
    update_asset,
    update_knowledge,
    get_canonical_convergence_items,
    get_conversation_state,
    governance_status,
    list_assets,
    list_ddna_jobs,
    list_ddna_sources,
    list_knowledge,
    list_saved_chats,
    provider_status,
    reset_conversation,
    save_chat,
    set_provider_secret,
    update_provider_config,
)



class handler(BaseHTTPRequestHandler):
    server_version = "ESCD-MVP/0.7.3"

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
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
            raise MVPServiceError("invalid_json") from exc

    def _supabase_config(self):
        url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        anon = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
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
        auth, repo = self._repo_for_token(extract_bearer(self.headers))
        self._operator_email = auth.email or ""
        return repo

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

    def _resolve_item_id(self, repo: SupabaseRLSClient, item_id: str) -> str:
        """Canonical registry tasks and ideas are read-only; editing one adopts it into escd_items first."""
        if is_uuid(item_id):
            return item_id
        existing = repo.get_item_by_key(item_id)
        if existing:
            return str(existing["id"])
        canonical = canonical_record("task", item_id) or canonical_record("idea", item_id)
        if not canonical:
            raise RepositoryError("item_not_found")
        return str(repo.create_item(canonical_item_payload(canonical))["id"])

    def _patch_item_governed(self, repo: SupabaseRLSClient, item_id: str, update: dict):
        item_id = self._resolve_item_id(repo, item_id)
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
        if target == "archived" and current_status == "archived":
            return current
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
            self._json(200, {"ok": True, "service": "escd-mvp", "version": "0.7.3", "providers": provider_status(), "governance": governance_status()})
            return

        try:
            repo = self._auth()
            if path == "/api/mvp/items":
                live_items = []
                try:
                    live_items = repo.list_items()
                except Exception:
                    pass
                canonical = get_canonical_convergence_items()
                merged = merge_live_and_canonical(live_items, canonical.get("tasks", []) + canonical.get("ideas", []), ("item_key",))
                self._json(200, {"ok": True, "items": merged})
            elif path == "/api/mvp/assets":
                self._json(200, {"ok": True, "assets": list_assets()})
            elif path == "/api/mvp/knowledge":
                self._json(200, {"ok": True, "knowledge": list_knowledge(repo=repo)})
            elif path == "/api/mvp/ddna":
                self._json(200, {"ok": True, "records": list_ddna_sources()})
            elif path == "/api/mvp/ddna/jobs":
                source_id = str((query.get("source_id") or [""])[0])
                self._json(200, {"ok": True, "jobs": list_ddna_jobs(source_id) if source_id else []})
            elif path == "/api/mvp/orchestrator/agents":
                self._json(200, {"ok": True, "agents": orchestrator_agents()})
            elif path == "/api/mvp/orchestrator/threads":
                days = int((query.get("days") or [7])[0])
                self._json(200, dict({"ok": True}, **orchestrator_threads(days)))
            elif path == "/api/mvp/providers":
                self._json(200, {"ok": True, "providers": provider_status()})
            elif path == "/api/mvp/governance/status":
                self._json(200, {"ok": True, "governance": governance_status()})
            elif path == "/api/mvp/conversation":
                cid = str((query.get("conversation_id") or ["conv_default"])[0]).strip()
                self._json(200, {"ok": True, "conversation": get_conversation_state(cid)})
            elif path == "/api/mvp/saved-chats":
                limit_val = int((query.get("limit") or [50])[0])
                self._json(200, {"ok": True, "saved_chats": list_saved_chats(limit_val)})
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
        if path == "/api/mvp/upload":
            self._json(410, {"error": "direct_upload_required"})
            return
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
            elif path == "/api/mvp/knowledge":
                self._json(201, {"ok": True, "record": create_knowledge(repo, payload)})
            elif path == "/api/mvp/assets":
                self._json(201, {"ok": True, "asset": create_asset(payload)})
            elif path == "/api/mvp/orchestrator/send":
                record = payload.get("record") if isinstance(payload.get("record"), dict) else None
                result = orchestrator_send(payload.get("recipients") or [], payload.get("subject"), payload.get("body"), record, getattr(self, "_operator_email", ""))
                self._json(201, dict({"ok": True}, **result))
            elif path == "/api/mvp/orchestrator/reply":
                result = orchestrator_reply(str(payload.get("message_id") or ""), payload.get("body"), getattr(self, "_operator_email", ""))
                self._json(201, dict({"ok": True}, **result))
            elif path == "/api/mvp/chat":
                cid = str(payload.get("conversation_id") or "conv_default").strip()
                prov = str(payload.get("provider") or "openai").strip()
                model_sel = str(payload.get("model") or "").strip() or None
                msgs = payload.get("messages") or []
                self._json(200, {"ok": True, "response": chat(prov, msgs, conversation_id=cid, model_override=model_sel)})
            elif path == "/api/mvp/chat/save":
                cid = str(payload.get("conversation_id") or "conv_default").strip()
                title = str(payload.get("title") or "").strip()
                self._json(200, {"ok": True, "saved": save_chat(cid, title)})
            elif path == "/api/mvp/conversation/reset":
                cid = str(payload.get("conversation_id") or "conv_default").strip()
                self._json(200, {"ok": True, "conversation": reset_conversation(cid)})
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
            if path == "/api/mvp/knowledge":
                record_id = str(payload.get("id") or "")
                if not record_id:
                    self._json(400, {"error": "id_required"}); return
                allowed = {"title", "content", "status", "authority_classification", "confidence"}
                self._json(200, {"ok": True, "record": update_knowledge(repo, record_id, {k: v for k, v in payload.items() if k in allowed})})
                return
            if path == "/api/mvp/assets":
                asset_id = str(payload.get("asset_id") or "")
                if not asset_id:
                    self._json(400, {"error": "asset_id_required"}); return
                allowed = {"file_name", "asset_type", "topic", "description", "storage_location", "semantic_version", "notes", "package", "entity_lane", "firewall_security_tag", "lifecycle_status", "sha256"}
                self._json(200, {"ok": True, "asset": update_asset(asset_id, {k: v for k, v in payload.items() if k in allowed})})
                return
            if path != "/api/mvp/items":
                self._json(404, {"error": "not_found"}); return
            item_id = str(payload.get("id") or "")
            if not item_id:
                self._json(400, {"error": "id_required"}); return
            allowed = {"title", "summary", "status", "due_at", "explicit_priority", "actionable", "context", "task_class"}
            update = {k: v for k, v in payload.items() if k in allowed}
            self._json(200, {"ok": True, "item": self._patch_item_governed(repo, item_id, update)})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})

    def do_DELETE(self):
        """Delete is a governed, recorded archive. No ESCD record is hard-deleted."""
        parsed = urlparse(self.path)
        path = parsed.path
        record_id = str((parse_qs(parsed.query).get("id") or [""])[0]).strip()
        try:
            repo = self._auth()
            if not record_id:
                self._json(400, {"error": "id_required"}); return
            if path == "/api/mvp/items":
                self._json(200, {"ok": True, "archived": True, "item": self._patch_item_governed(repo, record_id, {"status": "archived"})})
            elif path == "/api/mvp/knowledge":
                self._json(200, {"ok": True, "archived": True, "record": update_knowledge(repo, record_id, {"status": "archived"})})
            elif path == "/api/mvp/assets":
                self._json(200, {"ok": True, "archived": True, "asset": update_asset(record_id, {"lifecycle_status": "Retired"})})
            else:
                self._json(404, {"error": "not_found"})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError, ValueError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})
