from __future__ import annotations

import json
import os
import re
import socket
import base64
import hmac
from urllib import request, error, parse


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
    return ""


def _fallback_config(provider: str) -> dict:
    defaults = {
        "openai": {"provider": "openai", "enabled": True, "model": "gpt-5.6-sol", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "gemini": {"provider": "gemini", "enabled": True, "model": "gemini-3.8-flash", "timeout_seconds": 25, "max_output_tokens": 768, "thinking_level": "low"},
        "openrouter": {"provider": "openrouter", "enabled": False, "model": "openrouter/auto", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
    }
    cfg = dict(defaults.get(provider) or {})
    cfg["api_key"] = _env_secret(provider)
    cfg["credential_source"] = "environment" if cfg["api_key"] else "none"
    return cfg


def provider_runtime(provider: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in {"openai", "gemini", "openrouter"}:
        raise MVPServiceError("unsupported_provider")
    try:
        rows = _rpc("get_escd_provider_runtime", {"p_provider": provider})
        row = rows[0] if isinstance(rows, list) and rows else (rows if isinstance(rows, dict) else None)
    except Exception:
        raise MVPServiceError("Provider registry unavailable. Verify the Preview Supabase server bindings and Vault RPC access.") from None
    if not row:
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
    for provider in ("openai", "gemini", "openrouter"):
        try:
            cfg = provider_runtime(provider)
        except MVPServiceError as exc:
            result[provider] = {"enabled": False, "configured": False, "registry_available": False, "registry_error": str(exc), "credential_source": "none"}
            continue
        result[provider] = {
            "enabled": bool(cfg.get("enabled")),
            "configured": bool(cfg.get("api_key")),
            "model": cfg.get("model"),
            "timeout_seconds": cfg.get("timeout_seconds"),
            "max_output_tokens": cfg.get("max_output_tokens"),
            "thinking_level": cfg.get("thinking_level"),
            "credential_source": cfg.get("credential_source"),
            "registry_available": True,
            "project_ref": cfg.get("project_ref"),
        }
    return result


def set_provider_secret(provider: str, secret: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in {"openai", "gemini", "openrouter"}:
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
    if provider not in {"openai", "gemini", "openrouter"}:
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


def list_ddna_sources(limit: int = 200) -> list[dict]:
    url = (os.getenv("DDNA_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("DDNA_SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        raise MVPServiceError("ddna_source_not_configured")
    fields = "id,source_type,source_ref_id,source_title,entity,lane,priority,status,assigned_model,assigned_agent_key,ps_lock,public_safe,queued_by,queued_at,extracted_at,notes,retry_count,max_retries,last_error,batch_id,content_snapshot"
    query = f"ddna_source_queue?select={fields}&order=queued_at.desc.nullslast,id.asc&limit={max(1, min(limit, 500))}"
    _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_ddna_legacy"))
    if not isinstance(rows, list):
        raise MVPServiceError("ddna_source_invalid")
    return rows


def list_ddna_jobs(source_queue_id: str) -> list[dict]:
    url = (os.getenv("DDNA_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("DDNA_SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        raise MVPServiceError("ddna_source_not_configured")
    safe = parse.quote(source_queue_id, safe="")
    fields = "id,job_key,source_queue_id,model_id,provider,status,error_message,retry_count,duration_ms,characteristics_extracted,started_at,completed_at,created_at"
    query = f"ddna_ollama_jobs?source_queue_id=eq.{safe}&select={fields}&order=created_at.desc,id.asc"
    _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_ddna_legacy"))
    return rows if isinstance(rows, list) else []


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


def chat(provider: str, messages: list[dict]) -> dict:
    provider = str(provider or "").lower().strip()
    cfg = provider_runtime(provider)
    key = str(cfg.get("api_key") or "")
    if not key:
        raise MVPServiceError(f"{provider.title()} credential is not configured. Add it in ESCD Provider Settings")
    if not cfg.get("enabled"):
        try:
            update_provider_config(provider, {"enabled": True})
            cfg["enabled"] = True
        except Exception:
            raise MVPServiceError(f"{provider.title()} is disabled in ESCD Provider Settings")
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
            return {"provider": provider, "model": (data or {}).get("model") or model, "content": text}

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
            return {"provider": provider, "model": model, "content": text}

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
            return {"provider": provider, "model": (data or {}).get("model") or model, "content": text}

        raise MVPServiceError("unsupported_provider")
    except Exception as exc:
        if isinstance(exc, MVPServiceError) and not isinstance(exc, ProviderHTTPError) and str(exc).startswith(("OpenAI returned", "Gemini returned", "OpenRouter returned")):
            raise
        raise _provider_failure(provider, exc) from None
