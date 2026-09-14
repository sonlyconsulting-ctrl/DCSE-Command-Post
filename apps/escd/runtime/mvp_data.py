from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import socket
from datetime import datetime, timezone
import time
from urllib import error, parse, request
import uuid


class MVPServiceError(RuntimeError):
    pass


class ProviderHTTPError(MVPServiceError):
    def __init__(self, status: int, detail: str):
        super().__init__(detail)
        self.status = status
        self.detail = detail


def _safe_provider_detail(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return "Provider request failed"
    patterns = [
        (r"sk-proj-[A-Za-z0-9_\-]{8,}", "sk-proj-***"),
        (r"sk-or-v1-[A-Za-z0-9_\-]{8,}", "sk-or-v1-***"),
        (r"sk-[A-Za-z0-9_\-]{8,}", "sk-***"),
        (r"AIza[A-Za-z0-9_\-]{12,}", "AIza***"),
        (r"(?i)Bearer\s+[A-Za-z0-9._\-]{10,}", "Bearer ***"),
    ]
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text[:900]


def _extract_error_detail(raw: str, status: int) -> str:
    try:
        data = json.loads(raw or "{}")
    except Exception:
        data = {}
    detail = ""
    if isinstance(data, dict):
        err = data.get("error")
        if isinstance(err, dict):
            detail = str(err.get("message") or err.get("detail") or err.get("code") or "")
        elif err:
            detail = str(err)
        if not detail:
            detail = str(data.get("message") or data.get("detail") or "")
    return _safe_provider_detail(detail or f"Provider returned HTTP {status}")


def _http_json(url: str, *, method: str = "GET", headers: dict | None = None, payload: dict | None = None, timeout: int = 30):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw or "null")
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise ProviderHTTPError(exc.code, _extract_error_detail(raw, exc.code)) from None
    except (TimeoutError, socket.timeout):
        raise MVPServiceError("provider_timeout") from None
    except error.URLError as exc:
        raise MVPServiceError(_safe_provider_detail(f"Provider connection failed: {exc.reason}")) from None


def _service_config() -> tuple[str, str]:
    url = (os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("PABASE_SECRET_KEY") or ""
    if not url or not key:
        raise MVPServiceError("runtime_registry_not_configured")
    if parse.urlparse(url).hostname != "nevgdyfpxdaloacuutal.supabase.co":
        raise MVPServiceError("ESCD requires the SC-Command-Post Supabase project")
    if key.count(".") == 2:
        try:
            claims = json.loads(base64.urlsafe_b64decode(key.split(".")[1] + "==="))
            matches = claims.get("ref") == "nevgdyfpxdaloacuutal" and claims.get("role") == "service_role"
        except Exception:
            matches = False
        if not matches:
            raise MVPServiceError("ESCD service credential does not match SC-Command-Post")
    return url, key


def _postgrest_headers(key: str, schema: str) -> dict[str, str]:
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept-Profile": schema,
        "Content-Profile": schema,
        "Content-Type": "application/json",
    }


def _rpc(name: str, payload: dict):
    url, key = _service_config()
    _, data = _http_json(
        f"{url}/rest/v1/rpc/{name}",
        method="POST",
        headers=_postgrest_headers(key, "dcse_cp"),
        payload=payload,
        timeout=12,
    )
    return data


def _env_secret(provider: str) -> str:
    if provider == "openai":
        return os.getenv("OPENAI_API_KEY") or ""
    if provider == "gemini":
        return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
    if provider == "openrouter":
        return os.getenv("OPENROUTER_API_KEY") or ""
    if provider == "anthropic":
        return os.getenv("ANTHROPIC_API_KEY") or ""
    return ""


def _fallback_config(provider: str) -> dict:
    defaults = {
        "openai": {"provider": "openai", "enabled": True, "model": "gpt-5.6-sol", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "gemini": {"provider": "gemini", "enabled": True, "model": "gemini-3.8-flash", "timeout_seconds": 25, "max_output_tokens": 768, "thinking_level": "low"},
        "openrouter": {"provider": "openrouter", "enabled": False, "model": "openrouter/auto", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "anthropic": {"provider": "anthropic", "enabled": True, "model": "claude-3-7-sonnet-20250219", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "ollama": {"provider": "ollama", "enabled": True, "model": "qwen2.5-coder:latest", "timeout_seconds": 60, "max_output_tokens": 2048, "thinking_level": None, "worker": "DCS-WINDOWS-OLLAMA-01", "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")},
    }
    cfg = dict(defaults.get(provider) or {})
    cfg["api_key"] = _env_secret(provider)
    cfg["credential_source"] = "environment" if cfg["api_key"] else ("local/exchange" if provider == "ollama" else "none")
    return cfg


def provider_runtime(provider: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in {"openai", "gemini", "openrouter", "anthropic", "ollama"}:
        raise MVPServiceError("unsupported_provider")
    if provider == "ollama":
        try:
            rows = _rpc("get_escd_provider_runtime", {"p_provider": provider})
            row = rows[0] if isinstance(rows, list) and rows else (rows if isinstance(rows, dict) else None)
        except Exception:
            row = None
        if not row:
            cfg = _fallback_config("ollama")
            cfg["registry_available"] = True
            cfg["configured"] = True
            return cfg
        cfg = dict(row)
        cfg["registry_available"] = True
        cfg["configured"] = True
        return cfg
    try:
        rows = _rpc("get_escd_provider_runtime", {"p_provider": provider})
        row = rows[0] if isinstance(rows, list) and rows else (rows if isinstance(rows, dict) else None)
    except Exception:
        raise MVPServiceError("Provider registry unavailable. Verify the Preview Supabase server bindings and Vault RPC access.") from None
    if not row:
        if provider == "anthropic":
            cfg = _fallback_config("anthropic")
            cfg["registry_available"] = True
            return cfg
        raise MVPServiceError("Provider registry entry is missing")
    cfg = dict(row)
    cfg["registry_available"] = True
    cfg["project_ref"] = "nevgdyfpxdaloacuutal"
    vault_key = str(cfg.get("api_key") or "")
    env_key = _env_secret(provider)
    if vault_key:
        cfg["api_key"] = vault_key
        cfg["credential_source"] = "vault"
    elif env_key:
        cfg["api_key"] = env_key
        cfg["credential_source"] = "environment"
    else:
        cfg["api_key"] = ""
        cfg["credential_source"] = "none"
    return cfg


def provider_status() -> dict:
    result = {}
    for provider in ("ollama", "openai", "gemini", "openrouter", "anthropic"):
        try:
            cfg = provider_runtime(provider)
        except MVPServiceError as exc:
            result[provider] = {"enabled": False, "configured": False, "registry_available": False, "registry_error": str(exc), "credential_source": "none"}
            continue
        result[provider] = {
            "provider": provider,
            "enabled": bool(cfg.get("enabled")),
            "configured": bool(cfg.get("api_key")) or (provider == "ollama"),
            "model": cfg.get("model"),
            "timeout_seconds": cfg.get("timeout_seconds"),
            "max_output_tokens": cfg.get("max_output_tokens"),
            "thinking_level": cfg.get("thinking_level"),
            "credential_source": cfg.get("credential_source"),
            "registry_available": True,
            "project_ref": cfg.get("project_ref"),
        }
        if provider == "ollama":
            result[provider]["worker"] = cfg.get("worker", "DCS-WINDOWS-OLLAMA-01")
            result[provider]["exchange"] = "supabase-worker-bridge"
    return result


def set_provider_secret(provider: str, secret: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in {"openai", "gemini", "openrouter", "anthropic"}:
        raise MVPServiceError("unsupported_provider")
    if len(str(secret or "").strip()) < 10:
        raise MVPServiceError("provider_secret_required")
    value = str(secret).strip()
    try:
        saved = _rpc("set_escd_provider_secret", {"p_provider": provider, "p_secret": value})
        cfg = provider_runtime(provider)
        verified = saved is True and cfg.get("credential_source") == "vault" and hmac.compare_digest(str(cfg.get("api_key") or "").encode(), value.encode())
    except Exception:
        raise MVPServiceError("Vault save could not be verified. Check the Preview server connection and retry.") from None
    if not verified:
        raise MVPServiceError("Vault save could not be verified. Check the Preview server connection and retry.")
    return {"provider": provider, "configured": True, "credential_source": "vault"}


def update_provider_config(provider: str, changes: dict) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in {"openai", "gemini", "openrouter", "anthropic"}:
        raise MVPServiceError("unsupported_provider")
    payload = {
        "p_provider": provider,
        "p_enabled": changes.get("enabled") if "enabled" in changes else None,
        "p_model": changes.get("model"),
        "p_timeout_seconds": changes.get("timeout_seconds"),
        "p_max_output_tokens": changes.get("max_output_tokens"),
        "p_thinking_level": changes.get("thinking_level"),
    }
    data = _rpc("update_escd_provider_config", payload)
    return data[0] if isinstance(data, list) and data else data


def _provider_failure(provider: str, exc: Exception) -> MVPServiceError:
    if isinstance(exc, ProviderHTTPError):
        labels = {400: "request rejected", 401: "authentication failed", 403: "access denied", 404: "model or endpoint not found", 429: "rate or quota limited"}
        label = labels.get(exc.status, f"HTTP {exc.status}")
        return MVPServiceError(f"{provider.title()} {label}: {exc.detail}")
    text = str(exc)
    if text == "provider_timeout":
        return MVPServiceError(f"{provider.title()} timed out before responding")
    return MVPServiceError(f"{provider.title()} request failed: {_safe_provider_detail(text)}")


def list_assets(limit: int = 200) -> list[dict]:
    url, key = _service_config()
    query = "dcse_asset_registry?select=*&order=last_modified_at.desc.nullslast,created_at.desc.nullslast,id.asc&limit=" + str(max(1, min(limit, 500)))
    _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "public"))
    if not isinstance(rows, list):
        raise MVPServiceError("asset_source_invalid")
    return rows


def create_asset(payload: dict) -> dict:
    if not payload.get("file_name") and not payload.get("asset_id"):
        raise MVPServiceError("asset_file_name_required")
    url, key = _service_config()
    headers = dict(_postgrest_headers(key, "public"))
    headers["Prefer"] = "return=representation"
    _, rows = _http_json(f"{url}/rest/v1/dcse_asset_registry", method="POST", headers=headers, payload=payload)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def patch_asset(asset_id: str, update: dict) -> dict:
    url, key = _service_config()
    safe = parse.quote(str(asset_id), safe="")
    headers = dict(_postgrest_headers(key, "public"))
    headers["Prefer"] = "return=representation"
    col = "id" if "-" in str(asset_id) and len(str(asset_id)) == 36 else "asset_id"
    _, rows = _http_json(f"{url}/rest/v1/dcse_asset_registry?{col}=eq.{safe}", method="PATCH", headers=headers, payload=update)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def delete_asset(asset_id: str) -> bool:
    url, key = _service_config()
    safe = parse.quote(str(asset_id), safe="")
    col = "id" if "-" in str(asset_id) and len(str(asset_id)) == 36 else "asset_id"
    _http_json(f"{url}/rest/v1/dcse_asset_registry?{col}=eq.{safe}", method="DELETE", headers=_postgrest_headers(key, "public"))
    return True


def _ddna_config() -> tuple[str, str]:
    url = (os.getenv("DDNA_SUPABASE_URL") or os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("DDNA_SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("PABASE_SECRET_KEY") or ""
    if not url or not key:
        raise MVPServiceError("ddna_source_not_configured")
    return url, key


def list_ddna_sources(limit: int = 200) -> list[dict]:
    url, key = _ddna_config()
    fields = "id,source_type,source_ref_id,source_title,entity,lane,priority,status,assigned_model,assigned_agent_key,ps_lock,public_safe,queued_by,queued_at,extracted_at,notes,retry_count,max_retries,last_error,batch_id,content_snapshot"
    query = f"ddna_source_queue?select={fields}&order=queued_at.desc.nullslast,id.asc&limit={max(1, min(limit, 500))}"
    _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_cp"))
    if not isinstance(rows, list):
        raise MVPServiceError("ddna_source_invalid")
    return rows


def create_ddna_source(payload: dict) -> dict:
    if not payload.get("source_title") and not payload.get("source_ref_id"):
        raise MVPServiceError("source_title_or_ref_required")
    url, key = _ddna_config()
    headers = dict(_postgrest_headers(key, "dcse_cp"))
    headers["Prefer"] = "return=representation"
    _, rows = _http_json(f"{url}/rest/v1/ddna_source_queue", method="POST", headers=headers, payload=payload)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def patch_ddna_source(source_id: str, update: dict) -> dict:
    url, key = _ddna_config()
    safe = parse.quote(str(source_id), safe="")
    headers = dict(_postgrest_headers(key, "dcse_cp"))
    headers["Prefer"] = "return=representation"
    col = "id" if "-" in str(source_id) and len(str(source_id)) == 36 else "source_ref_id"
    _, rows = _http_json(f"{url}/rest/v1/ddna_source_queue?{col}=eq.{safe}", method="PATCH", headers=headers, payload=update)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def delete_ddna_source(source_id: str) -> bool:
    url, key = _ddna_config()
    safe = parse.quote(str(source_id), safe="")
    col = "id" if "-" in str(source_id) and len(str(source_id)) == 36 else "source_ref_id"
    _http_json(f"{url}/rest/v1/ddna_source_queue?{col}=eq.{safe}", method="DELETE", headers=_postgrest_headers(key, "dcse_cp"))
    return True


def list_ddna_jobs(source_queue_id: str) -> list[dict]:
    url, key = _ddna_config()
    safe = parse.quote(source_queue_id, safe="")
    fields = "id,job_key,source_queue_id,model_id,provider,status,error_message,retry_count,duration_ms,characteristics_extracted,started_at,completed_at,created_at"
    query = f"ddna_ollama_jobs?source_queue_id=eq.{safe}&select={fields}&order=created_at.desc,id.asc"
    _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_cp"))
    return rows if isinstance(rows, list) else []


_CANONICAL_REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "escd_canonical_convergence_registry.json")


def get_canonical_convergence_items() -> dict[str, list]:
    registry_path = _CANONICAL_REGISTRY_PATH
    if not os.path.exists(registry_path):
        return {"tasks": [], "ideas": [], "knowledge": [], "ddna": [], "assets": []}
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {"tasks": [], "ideas": [], "knowledge": [], "ddna": [], "assets": []}

    tasks, ideas, knowledge, ddna, assets = [], [], [], [], []
    for it in data.get("canonical_items", []):
        disp = it.get("disposition")
        cid = it.get("canonical_id") or ""
        raw = it.get("content") or ""
        first_line = raw.strip().split("\n")[0].replace("**", "").replace("Task ID:", "").strip()
        title = first_line[:90] if first_line else cid
        if disp == "TASK":
            tasks.append({
                "id": cid,
                "item_key": cid,
                "title": title,
                "explicit_priority": 0,
                "source_system": it.get("source", "canonical_convergence")
            })
        elif disp == "KNOWLEDGE":
            knowledge.append({
                "id": cid,
                "title": title,
                "content": raw,
                "source": it.get("source", "canonical_convergence"),
                "provenance": it.get("provenance", {}),
                "status": it.get("status", "staged"),
                "confidence": it.get("confidence", 0.95),
                "authority_classification": it.get("authority_classification", "HISTORICAL_RECOVERED")
            })
        elif disp == "DDNA":
            ddna.append({
                "semantic_version": "1.0.0",
                "lifecycle_status": it.get("status", "staged")
            })
    return {"tasks": tasks, "ideas": ideas, "knowledge": knowledge, "ddna": ddna, "assets": assets}


def list_knowledge(limit: int = 200) -> list[dict]:
    items = get_canonical_convergence_items().get("knowledge", [])
    return items[:limit]


def search_knowledge(query: str, limit: int = 200) -> list[dict]:
    items = list_knowledge(limit=limit)
    q = str(query or "").strip().lower()
    if not q:
        return items
    return [
        it for it in items
        if q in it.get("title", "").lower()
        or q in it.get("content", "").lower()
        or q in it.get("id", "").lower()
        or q in it.get("authority_classification", "").lower()
    ]


def _storage_service_request(path: str, *, method: str = "POST", payload: dict | None = None, extra_headers: dict | None = None) -> tuple[str, dict]:
    url, key = _service_config()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url + "/storage/v1/" + path.lstrip("/"), data=body, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=15) as resp:
            raw = resp.read().decode("utf-8")
            return url, json.loads(raw or "{}")
    except Exception as exc:
        raise MVPServiceError(f"storage_request_failed: {exc}") from exc


def _safe_storage_path(storage_path: str) -> str:
    path = str(storage_path or "").strip().lstrip("/")
    if not path or ".." in path.split("/"):
        raise MVPServiceError("invalid_storage_path")
    return path


def create_signed_attachment_upload(
    file_name: str,
    mime_type: str,
    size: int,
    record_type: str,
    record_id: str,
) -> dict:
    clean_name = re.sub(r"[^A-Za-z0-9._\-]", "_", str(file_name or "").strip() or "file")
    clean_mime = str(mime_type or "application/octet-stream").strip()
    if clean_name.lower().endswith(".zip") and (clean_mime in ("application/x-zip-compressed", "application/octet-stream", "") or "zip" in clean_mime):
        clean_mime = "application/zip"
    rec_type = str(record_type or "item").strip().lower()
    rec_id = str(record_id or "").strip()
    if not rec_id:
        raise MVPServiceError("record_id_required")
    try:
        file_size = int(size)
    except (TypeError, ValueError):
        raise MVPServiceError("invalid_file_size") from None
    if file_size < 1:
        raise MVPServiceError("empty_file")
    if file_size > 10 * 1024 * 1024:
        raise MVPServiceError("file_exceeds_size_limit")

    nonce = hashlib.sha256(
        f"{rec_type}\n{rec_id}\n{clean_name}\n{datetime.now(timezone.utc).isoformat()}".encode("utf-8")
    ).hexdigest()[:16]
    storage_path = f"{rec_type}s/{rec_id}/{nonce}_{clean_name}"
    quoted = parse.quote("escd-files/" + storage_path, safe="/")
    base_url, data = _storage_service_request(
        f"object/upload/sign/{quoted}",
        method="POST",
        payload={},
        extra_headers={"x-upsert": "false"},
    )
    relative = str(data.get("url") or "")
    if not relative:
        raise MVPServiceError("signed_upload_url_missing")
    storage_base = base_url.rstrip("/") + "/storage/v1"
    signed_url = relative if relative.startswith("http") else storage_base + (relative if relative.startswith("/") else "/" + relative)
    return {
        "storage_path": storage_path,
        "signed_upload_url": signed_url,
        "expires_in": 7200,
        "name": clean_name,
        "type": clean_mime,
        "size": file_size,
    }


def _asset_by_id(asset_id: str) -> dict:
    url, key = _service_config()
    safe = parse.quote(str(asset_id), safe="")
    col = "id" if "-" in str(asset_id) and len(str(asset_id)) == 36 else "asset_id"
    _, rows = _http_json(
        f"{url}/rest/v1/dcse_asset_registry?{col}=eq.{safe}&select=*&limit=1",
        headers=_postgrest_headers(key, "public"),
    )
    return rows[0] if isinstance(rows, list) and rows else {}


def _ddna_by_id(source_id: str) -> dict:
    url, key = _ddna_config()
    safe = parse.quote(str(source_id), safe="")
    col = "id" if "-" in str(source_id) and len(str(source_id)) == 36 else "source_ref_id"
    _, rows = _http_json(
        f"{url}/rest/v1/ddna_source_queue?{col}=eq.{safe}&select=*&limit=1",
        headers=_postgrest_headers(key, "dcse_cp"),
    )
    return rows[0] if isinstance(rows, list) and rows else {}


def _ddna_attachment_marker(attachment: dict) -> str:
    return "[ESCD_ATTACHMENT]" + json.dumps(attachment, separators=(",", ":"), sort_keys=True)


def finalize_file_attachment(
    *,
    storage_path: str,
    file_name: str,
    mime_type: str,
    size: int,
    sha256: str,
    record_type: str,
    record_id: str,
    repo=None,
) -> dict:
    path = _safe_storage_path(storage_path)
    rec_type = str(record_type or "item").strip().lower()
    rec_id = str(record_id or "").strip()
    if not rec_id:
        raise MVPServiceError("record_id_required")
    expected_prefix = f"{rec_type}s/{rec_id}/"
    if not path.startswith(expected_prefix):
        raise MVPServiceError("storage_path_record_mismatch")
    digest = str(sha256 or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise MVPServiceError("invalid_sha256")

    attachment = {
        "id": digest[:16],
        "name": re.sub(r"[^A-Za-z0-9._\-]", "_", str(file_name or "").strip() or "file"),
        "size": int(size or 0),
        "type": str(mime_type or "application/octet-stream"),
        "sha256": digest,
        "storage_path": path,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if rec_type in {"item", "task", "idea"}:
        if repo is None:
            raise MVPServiceError("repository_required")
        item = repo.get_item(rec_id)
        if not item:
            raise MVPServiceError("item_not_found")
        refs = item.get("evidence_refs") or []
        refs = refs if isinstance(refs, list) else []
        refs = [x for x in refs if not (isinstance(x, dict) and x.get("storage_path") == path)]
        refs.append(attachment)
        repo.patch_item(rec_id, {"evidence_refs": refs})
    elif rec_type == "asset":
        row = _asset_by_id(rec_id)
        if not row:
            raise MVPServiceError("asset_not_found")
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        refs = metadata.get("attachments") if isinstance(metadata.get("attachments"), list) else []
        refs = [x for x in refs if not (isinstance(x, dict) and x.get("storage_path") == path)]
        refs.append(attachment)
        metadata = dict(metadata)
        metadata["attachments"] = refs
        patch_asset(rec_id, {"metadata": metadata})
    elif rec_type == "ddna":
        row = _ddna_by_id(rec_id)
        if not row:
            raise MVPServiceError("ddna_source_not_found")
        existing_notes = str(row.get("notes") or "")
        marker = _ddna_attachment_marker(attachment)
        updated_notes = (existing_notes.rstrip() + "\n" + marker).strip() if existing_notes.strip() else marker
        patch_ddna_source(rec_id, {"notes": updated_notes})
    elif rec_type in {"chat", "turn"}:
        pass  # Client binds attachment metadata into message context / turn facts
    else:
        raise MVPServiceError("invalid_record_type")
    return attachment


def create_signed_attachment_download(storage_path: str, file_name: str = "", expires_in: int = 300) -> dict:
    path = _safe_storage_path(storage_path)
    ttl = max(60, min(int(expires_in or 300), 900))
    quoted = parse.quote("escd-files/" + path, safe="/")
    base_url, data = _storage_service_request(
        f"object/sign/{quoted}",
        method="POST",
        payload={"expiresIn": ttl},
    )
    relative = str(data.get("signedURL") or data.get("signedUrl") or "")
    if not relative:
        raise MVPServiceError("signed_download_url_missing")
    storage_base = base_url.rstrip("/") + "/storage/v1"
    signed_url = relative if relative.startswith("http") else storage_base + (relative if relative.startswith("/") else "/" + relative)
    if file_name:
        joiner = "&" if "?" in signed_url else "?"
        signed_url += joiner + "download=" + parse.quote(str(file_name), safe="")
    return {"signed_url": signed_url, "expires_in": ttl, "storage_path": path}


def delete_file_attachment(storage_path: str) -> bool:
    path = _safe_storage_path(storage_path)
    url, key = _service_config()
    del_payload = json.dumps({"prefixes": [path]}).encode("utf-8")
    req = request.Request(
        f"{url}/storage/v1/object/escd-files",
        data=del_payload,
        headers={
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="DELETE",
    )
    try:
        with request.urlopen(req, timeout=15):
            return True
    except Exception as exc:
        raise MVPServiceError(f"storage_delete_failed: {exc}") from exc


def delete_record_attachment(
    *,
    storage_path: str,
    record_type: str,
    record_id: str,
    repo=None,
) -> bool:
    path = _safe_storage_path(storage_path)
    rec_type = str(record_type or "item").strip().lower()
    rec_id = str(record_id or "").strip()
    if not rec_id:
        raise MVPServiceError("record_id_required")

    delete_file_attachment(path)

    if rec_type in {"item", "task", "idea"}:
        if repo is None:
            raise MVPServiceError("repository_required")
        item = repo.get_item(rec_id)
        if item:
            refs = item.get("evidence_refs") or []
            refs = refs if isinstance(refs, list) else []
            refs = [x for x in refs if not (isinstance(x, dict) and x.get("storage_path") == path)]
            repo.patch_item(rec_id, {"evidence_refs": refs})
    elif rec_type == "asset":
        row = _asset_by_id(rec_id)
        if row:
            metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
            refs = metadata.get("attachments") if isinstance(metadata.get("attachments"), list) else []
            metadata = dict(metadata)
            metadata["attachments"] = [
                x for x in refs if not (isinstance(x, dict) and x.get("storage_path") == path)
            ]
            patch_asset(rec_id, {"metadata": metadata})
    elif rec_type == "ddna":
        row = _ddna_by_id(rec_id)
        if row:
            kept = []
            for line in str(row.get("notes") or "").splitlines():
                if line.startswith("[ESCD_ATTACHMENT]"):
                    try:
                        meta = json.loads(line[len("[ESCD_ATTACHMENT]"):])
                    except Exception:
                        meta = {}
                    if meta.get("storage_path") == path:
                        continue
                kept.append(line)
            patch_ddna_source(rec_id, {"notes": "\n".join(kept).strip()})
    else:
        raise MVPServiceError("invalid_record_type")
    return True


def save_file_attachment(*args, **kwargs):
    raise MVPServiceError("direct_upload_required")

def _openai_output_text(data: dict) -> str:
    direct = data.get("output_text")
    if isinstance(direct, str) and direct.strip():
        return direct.strip()
    chunks = []
    for output in data.get("output") or []:
        if output.get("type") != "message":
            continue
        for part in output.get("content") or []:
            if part.get("type") == "output_text" and part.get("text"):
                chunks.append(str(part["text"]))
    return "\n".join(chunks).strip()


def estimate_tokens_and_cost(provider: str, model: str, prompt_text: str, completion_text: str, raw_usage: dict | None = None) -> dict:
    prov = str(provider or "").lower().strip()
    mod = str(model or "").lower().strip()

    if raw_usage and isinstance(raw_usage, dict):
        p_tokens = int(raw_usage.get("prompt_tokens") or raw_usage.get("input_tokens") or raw_usage.get("prompt_eval_count") or 0)
        c_tokens = int(raw_usage.get("completion_tokens") or raw_usage.get("output_tokens") or raw_usage.get("eval_count") or 0)
    else:
        p_tokens = max(1, len(prompt_text) // 4)
        c_tokens = max(1, len(completion_text) // 4)

    total = p_tokens + c_tokens

    if prov == "ollama":
        cost = 0.0
        label = "$0.0000 (Local Inference - Zero API Cost)"
    elif "gpt-4o-mini" in mod:
        cost = (p_tokens * 0.15 + c_tokens * 0.60) / 1_000_000
        label = f"${cost:.6f}"
    elif "gpt-4o" in mod:
        cost = (p_tokens * 2.50 + c_tokens * 10.00) / 1_000_000
        label = f"${cost:.6f}"
    elif "flash" in mod:
        cost = (p_tokens * 0.075 + c_tokens * 0.30) / 1_000_000
        label = f"${cost:.6f}"
    elif prov == "anthropic" or "claude" in mod:
        if "haiku" in mod:
            cost = (p_tokens * 0.80 + c_tokens * 4.00) / 1_000_000
        else:
            cost = (p_tokens * 3.00 + c_tokens * 15.00) / 1_000_000
        label = f"${cost:.6f}"
    else:
        cost = (p_tokens * 0.50 + c_tokens * 1.50) / 1_000_000
        label = f"${cost:.6f}"

    return {
        "prompt_tokens": p_tokens,
        "completion_tokens": c_tokens,
        "total_tokens": total,
        "cost_usd": round(cost, 6),
        "cost_label": label,
        "model": model,
        "provider": provider,
    }


TRACE_RECORDS: dict[str, dict] = {}


def _save_trace(trace_id: str, record: dict) -> None:
    TRACE_RECORDS[trace_id] = record
    for base in [os.path.join(os.path.abspath("."), "logs", "traces"), "/tmp/traces"]:
        try:
            os.makedirs(base, exist_ok=True)
            path = os.path.join(base, f"{trace_id}.json")
            with open(path, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2)
            break
        except Exception:
            continue


def get_trace_record(trace_id: str) -> dict | None:
    if trace_id in TRACE_RECORDS:
        return TRACE_RECORDS[trace_id]
    for base in [os.path.join(os.path.abspath("."), "logs", "traces"), "/tmp/traces"]:
        path = os.path.join(base, f"{trace_id}.json")
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
    return None


def chat(provider: str, messages: list[dict]) -> dict:
    provider = str(provider or "").lower().strip()
    if provider == "ollama":
        raise MVPServiceError("ollama_requires_durable_worker_exchange")
    cfg = provider_runtime(provider)
    if not cfg.get("enabled"):
        raise MVPServiceError(f"{provider.title()} is disabled in ESCD Provider Settings")
    key = str(cfg.get("api_key") or "")
    if not key and provider != "ollama":
        raise MVPServiceError(f"{provider.title()} credential is not configured. Add it in ESCD Provider Settings")
    model = str(cfg.get("model") or "").strip()
    timeout = int(cfg.get("timeout_seconds") or 30)
    max_tokens = int(cfg.get("max_output_tokens") or 1024)

    clean = []
    for message in messages[-30:]:
        role = str(message.get("role") or "user")
        content = str(message.get("content") or "").strip()
        if content and role in {"user", "assistant", "system"}:
            clean.append({"role": role, "content": content[:12000]})
    if not clean:
        raise MVPServiceError("chat_message_required")

    last_prompt = clean[-1]["content"] if clean else "No query"

    try:
        if provider == "openai":
            _, data = _http_json(
                "https://api.openai.com/v1/responses",
                method="POST",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                payload={"model": model, "input": clean, "max_output_tokens": max_tokens},
                timeout=timeout,
            )
            text = _openai_output_text(data or {})
            if not text:
                raise MVPServiceError("OpenAI returned an empty response")
            usage = estimate_tokens_and_cost(provider, model, last_prompt, text, (data or {}).get("usage"))
            return {"provider": provider, "model": (data or {}).get("model") or model, "content": text, "usage": usage}

        if provider == "gemini":
            contents = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [{"text": m["content"]}]} for m in clean if m["role"] != "system"]
            payload = {"contents": contents, "generationConfig": {"maxOutputTokens": max_tokens}}
            system_text = "\n".join(m["content"] for m in clean if m["role"] == "system").strip()
            if system_text:
                payload["systemInstruction"] = {"parts": [{"text": system_text}]}
            _, data = _http_json(
                f"https://generativelanguage.googleapis.com/v1beta/models/{parse.quote(model, safe='')}:generateContent?key={parse.quote(key, safe='')}",
                method="POST",
                headers={"Content-Type": "application/json"},
                payload=payload,
                timeout=timeout,
            )
            candidates = (data or {}).get("candidates") or []
            parts = (((candidates[0] if candidates else {}).get("content") or {}).get("parts") or [])
            text = "\n".join(str(x.get("text") or "") for x in parts if x.get("text")).strip()
            if not text:
                raise MVPServiceError("Gemini returned an empty response")
            usage = estimate_tokens_and_cost(provider, model, last_prompt, text, (data or {}).get("usageMetadata"))
            return {"provider": provider, "model": model, "content": text, "usage": usage}

        if provider == "openrouter":
            _, data = _http_json(
                "https://openrouter.ai/api/v1/chat/completions",
                method="POST",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "HTTP-Referer": "https://os.sonlyconsulting.com", "X-Title": "ESCD"},
                payload={"model": model, "messages": clean, "max_tokens": max_tokens},
                timeout=timeout,
            )
            choices = (data or {}).get("choices") or []
            text = str((((choices[0] if choices else {}).get("message") or {}).get("content") or "")).strip()
            if not text:
                raise MVPServiceError("OpenRouter returned an empty response")
            usage = estimate_tokens_and_cost(provider, model, last_prompt, text, (data or {}).get("usage"))
            return {"provider": provider, "model": (data or {}).get("model") or model, "content": text, "usage": usage}

        if provider == "anthropic":
            system_parts = []
            anthropic_messages = []
            for m in clean:
                if m["role"] == "system":
                    system_parts.append(m["content"])
                elif m["role"] in {"user", "assistant"}:
                    if anthropic_messages and anthropic_messages[-1]["role"] == m["role"]:
                        anthropic_messages[-1]["content"] += "\n\n" + m["content"]
                    else:
                        anthropic_messages.append({"role": m["role"], "content": m["content"]})
            if not anthropic_messages:
                anthropic_messages = [{"role": "user", "content": last_prompt}]

            payload = {
                "model": model,
                "messages": anthropic_messages,
                "max_tokens": max_tokens,
            }
            if system_parts:
                payload["system"] = "\n\n".join(system_parts)

            _, data = _http_json(
                "https://api.anthropic.com/v1/messages",
                method="POST",
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json",
                },
                payload=payload,
                timeout=timeout,
            )
            contents = (data or {}).get("content") or []
            text = "".join(str(c.get("text") or "") for c in contents if c.get("type") == "text").strip()
            if not text:
                raise MVPServiceError("Claude returned an empty response")
            raw_usage = (data or {}).get("usage") or {}
            usage = estimate_tokens_and_cost(
                provider, model, last_prompt, text,
                raw_usage={
                    "prompt_tokens": raw_usage.get("input_tokens"),
                    "completion_tokens": raw_usage.get("output_tokens"),
                }
            )
            return {
                "provider": provider,
                "model": (data or {}).get("model") or model,
                "worker": "api.anthropic.com",
                "content": text,
                "usage": usage,
                "evidence_refs": [f"anthropic://api.anthropic.com/{model}/messages"],
            }

        raise MVPServiceError("unsupported_provider")
    except Exception as exc:
        if isinstance(exc, MVPServiceError) and not isinstance(exc, ProviderHTTPError) and str(exc).startswith(("OpenAI returned", "Gemini returned", "OpenRouter returned", "Claude returned")):
            raise
        raise _provider_failure(provider, exc) from None
