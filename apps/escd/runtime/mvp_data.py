from __future__ import annotations

import json
import os
from urllib import request, error, parse


class MVPServiceError(RuntimeError):
    pass


def _http_json(url: str, *, method: str = "GET", headers: dict | None = None, payload: dict | None = None, timeout: int = 30):
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers or {}, method=method)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw or "null")
    except error.HTTPError as exc:
        exc.read()
        raise MVPServiceError(f"upstream_{exc.code}") from None


def _postgrest_headers(key: str, schema: str) -> dict[str, str]:
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept-Profile": schema,
        "Content-Type": "application/json",
    }


def list_assets(limit: int = 200) -> list[dict]:
    url = (os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("PABASE_SECRET_KEY") or ""
    if not url or not key:
        raise MVPServiceError("asset_source_not_configured")
    query = "dcse_asset_registry?select=*&order=updated_at.desc.nullslast,created_at.desc.nullslast&limit=" + str(max(1, min(limit, 500)))
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


def provider_status() -> dict:
    return {
        "openai": {"configured": bool(os.getenv("OPENAI_API_KEY"))},
        "gemini": {"configured": bool(os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))},
    }


def chat(provider: str, messages: list[dict]) -> dict:
    provider = provider.lower().strip()
    clean = []
    for message in messages[-30:]:
        role = str(message.get("role") or "user")
        content = str(message.get("content") or "").strip()
        if content and role in {"user", "assistant", "system"}:
            clean.append({"role": role, "content": content[:12000]})
    if not clean:
        raise MVPServiceError("chat_message_required")

    if provider == "openai":
        key = os.getenv("OPENAI_API_KEY") or ""
        if not key:
            raise MVPServiceError("openai_not_configured")
        model = os.getenv("ESCD_OPENAI_MODEL") or "gpt-5.6"
        payload = {"model": model, "messages": clean}
        _, data = _http_json(
            "https://api.openai.com/v1/chat/completions",
            method="POST",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            payload=payload,
            timeout=60,
        )
        text = (((data or {}).get("choices") or [{}])[0].get("message") or {}).get("content")
        if not text:
            raise MVPServiceError("openai_empty_response")
        return {"provider": "openai", "model": (data or {}).get("model") or model, "content": text}

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or ""
        if not key:
            raise MVPServiceError("gemini_not_configured")
        model = os.getenv("ESCD_GEMINI_MODEL") or "gemini-2.5-flash"
        contents = []
        system_parts = []
        for message in clean:
            if message["role"] == "system":
                system_parts.append({"text": message["content"]})
            else:
                contents.append({"role": "model" if message["role"] == "assistant" else "user", "parts": [{"text": message["content"]}]})
        payload = {"contents": contents}
        if system_parts:
            payload["systemInstruction"] = {"parts": system_parts}
        _, data = _http_json(
            f"https://generativelanguage.googleapis.com/v1beta/models/{parse.quote(model, safe='')}:generateContent?key={parse.quote(key, safe='')}",
            method="POST",
            headers={"Content-Type": "application/json"},
            payload=payload,
            timeout=60,
        )
        candidates = (data or {}).get("candidates") or []
        parts = (((candidates[0] if candidates else {}).get("content") or {}).get("parts") or [])
        text = "\n".join(str(x.get("text") or "") for x in parts if x.get("text")).strip()
        if not text:
            raise MVPServiceError("gemini_empty_response")
        return {"provider": "gemini", "model": model, "content": text}

    raise MVPServiceError("unsupported_provider")
