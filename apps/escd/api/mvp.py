from __future__ import annotations

from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import urlparse, parse_qs

from apps.escd.runtime.auth import AuthError, extract_bearer, verify_supabase_user, authorize_operator
from apps.escd.runtime.repository import SupabaseRLSClient, RepositoryError
from apps.escd.runtime.mvp_data import MVPServiceError, chat, list_assets, list_ddna_jobs, list_ddna_sources, provider_status


class handler(BaseHTTPRequestHandler):
    server_version = "ESCD-MVP/0.1"

    def _json(self, status: int, payload: dict):
        raw = json.dumps(payload, separators=(",", ":"), default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_json(self):
        size = int(self.headers.get("Content-Length") or 0)
        if size < 1 or size > 1_000_000:
            return {}
        return json.loads(self.rfile.read(size).decode("utf-8"))

    def _auth(self):
        token = extract_bearer(self.headers)
        url = os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
        anon = os.getenv("SUPABASE_ANON_KEY") or os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY") or ""
        auth = verify_supabase_user(token, url, anon)
        repo = SupabaseRLSClient(url, anon, token, schema="dcse_cp")
        authorize_operator(auth, repo.operator_self())
        return repo

    def do_GET(self):
        path = urlparse(self.path).path
        query = parse_qs(urlparse(self.path).query)
        if path == "/api/mvp/health":
            self._json(200, {"ok": True, "service": "escd-mvp", "providers": provider_status()})
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
        try:
            repo = self._auth()
            payload = self._read_json()
            if path == "/api/mvp/items":
                kind = str(payload.get("kind") or "task").lower()
                if kind not in {"task", "idea"}:
                    self._json(400, {"error": "invalid_kind"}); return
                title = str(payload.get("title") or "").strip()
                if not title:
                    self._json(400, {"error": "title_required"}); return
                import hashlib
                key = "mvp-" + hashlib.sha256((kind + "\n" + title.lower()).encode()).hexdigest()
                item = repo.create_item({
                    "item_key": key,
                    "title": title,
                    "summary": payload.get("notes"),
                    "status": "captured",
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
            elif path == "/api/mvp/chat":
                provider = str(payload.get("provider") or "openai")
                messages = payload.get("messages") or []
                self._json(200, {"ok": True, "response": chat(provider, messages)})
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
        if path != "/api/mvp/items":
            self._json(404, {"error": "not_found"}); return
        try:
            repo = self._auth()
            payload = self._read_json()
            item_id = str(payload.get("id") or "")
            if not item_id:
                self._json(400, {"error": "id_required"}); return
            allowed = {"title", "summary", "status", "due_at", "explicit_priority", "actionable", "context", "task_class"}
            update = {k: v for k, v in payload.items() if k in allowed}
            self._json(200, {"ok": True, "item": repo.patch_item(item_id, update)})
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)})
        except (RepositoryError, MVPServiceError) as exc:
            self._json(502, {"error": str(exc)})
        except Exception:
            self._json(500, {"error": "internal_error"})
