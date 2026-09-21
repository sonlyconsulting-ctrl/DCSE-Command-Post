from __future__ import annotations

import json
import os
import re
import socket
import base64
import hmac
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib import request, error, parse


class MVPServiceError(RuntimeError):
    pass


PROVIDERS = ("openai", "anthropic", "qwen", "gemini", "openrouter", "ollama")
ANTHROPIC_VERSION = "2023-06-01"
OLLAMA_DEFAULT_BASE_URL = "https://ollama.com"


def _ollama_base_url() -> str:
    raw = (os.getenv("OLLAMA_BASE_URL") or OLLAMA_DEFAULT_BASE_URL).strip().rstrip("/")
    parsed = parse.urlparse(raw)
    if parsed.scheme != "https" or not parsed.hostname:
        raise MVPServiceError("OLLAMA_BASE_URL must be an https URL reachable from the ESCD server")
    return raw


def _ollama_requires_key() -> bool:
    try:
        return parse.urlparse(_ollama_base_url()).hostname in {"ollama.com", "www.ollama.com"}
    except MVPServiceError:
        return True


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
        (r"sk-ant-[A-Za-z0-9_\-]{8,}", "sk-ant-***"),
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
    if provider in ("qwen", "dashscope"):
        return os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or ""
    if provider == "openrouter":
        return os.getenv("OPENROUTER_API_KEY") or ""
    if provider == "ollama":
        return os.getenv("OLLAMA_API_KEY") or ""
    if provider == "anthropic":
        return os.getenv("ANTHROPIC_API_KEY") or ""
    return ""


PROVIDER_CATALOG = {
    "openai": [
        {"id": "gpt-5.6-sol", "name": "GPT-5.6 Sol (Flagship)", "tier": "flagship"},
        {"id": "gpt-4o", "name": "GPT-4o (Production Fast)", "tier": "balanced"},
        {"id": "o3-mini", "name": "o3-mini (High Reasoning / STEM)", "tier": "reasoning"},
        {"id": "gpt-4.1-mini", "name": "GPT-4.1 Mini (High Throughput)", "tier": "fast"},
    ],
    "anthropic": [
        {"id": "claude-sonnet-5", "name": "Claude Sonnet 5 (Operative)", "tier": "flagship"},
        {"id": "claude-3-7-sonnet-20250219", "name": "Claude 3.7 Sonnet (Hybrid Reasoning)", "tier": "reasoning"},
        {"id": "claude-3-5-haiku-20241022", "name": "Claude 3.5 Haiku (Fast Triage)", "tier": "fast"},
    ],
    "qwen": [
        {"id": "qwen-max", "name": "Qwen Max (Flagship)", "tier": "flagship"},
        {"id": "qwen-plus", "name": "Qwen Plus (Balanced)", "tier": "balanced"},
        {"id": "qwen-turbo", "name": "Qwen Turbo (Fast)", "tier": "fast"},
        {"id": "qwen-2.5-72b-instruct", "name": "Qwen 2.5 72B Instruct", "tier": "flagship"},
    ],
    "gemini": [
        {"id": "gemini-3.8-flash", "name": "Gemini 3.8 Flash (Operative)", "tier": "fast"},
        {"id": "gemini-2.5-pro", "name": "Gemini 2.5 Pro (Deep Context)", "tier": "flagship"},
        {"id": "gemini-2.5-flash", "name": "Gemini 2.5 Flash (Mobile Fast)", "tier": "fast"},
    ],
    "openrouter": [
        {"id": "openrouter/auto", "name": "OpenRouter Auto-Route", "tier": "auto"},
        {"id": "deepseek/deepseek-r1", "name": "DeepSeek R1 (Economic Logic)", "tier": "reasoning"},
        {"id": "qwen/qwen-2.5-72b-instruct", "name": "Qwen 2.5 72B (Governance)", "tier": "flagship"},
        {"id": "nousresearch/hermes-3-llama-3.1-405b", "name": "Hermes 3 405B (Uncensored Local)", "tier": "flagship"},
    ],
    "ollama": [
        {"id": "gpt-oss:120b", "name": "GPT-OSS 120B (Operative)", "tier": "flagship"},
        {"id": "deepseek-r1:70b", "name": "DeepSeek R1 70B", "tier": "reasoning"},
        {"id": "qwen2.5:72b", "name": "Qwen 2.5 72B", "tier": "flagship"},
    ],
}


def _fallback_config(provider: str) -> dict:
    defaults = {
        "openai": {"provider": "openai", "enabled": True, "model": "gpt-5.6-sol", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "anthropic": {"provider": "anthropic", "enabled": True, "model": "claude-sonnet-5", "timeout_seconds": 60, "max_output_tokens": 1024, "thinking_level": None},
        "qwen": {"provider": "qwen", "enabled": True, "model": "qwen-max", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "gemini": {"provider": "gemini", "enabled": True, "model": "gemini-3.8-flash", "timeout_seconds": 25, "max_output_tokens": 768, "thinking_level": "low"},
        "openrouter": {"provider": "openrouter", "enabled": False, "model": "openrouter/auto", "timeout_seconds": 45, "max_output_tokens": 1024, "thinking_level": None},
        "ollama": {"provider": "ollama", "enabled": True, "model": "gpt-oss:120b", "timeout_seconds": 60, "max_output_tokens": 1024, "thinking_level": None},
    }
    cfg = dict(defaults.get(provider) or {})
    cfg["api_key"] = _env_secret(provider)
    cfg["credential_source"] = "environment" if cfg["api_key"] else "none"
    return cfg


def provider_runtime(provider: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in PROVIDERS:
        raise MVPServiceError("unsupported_provider")
    try:
        rows = _rpc("get_escd_provider_runtime", {"p_provider": provider})
        row = rows[0] if isinstance(rows, list) and rows else (rows if isinstance(rows, dict) else None)
    except Exception:
        raise MVPServiceError("Provider registry unavailable. Verify the Preview Supabase server bindings and Vault RPC access.") from None
    if not row:
        row = _fallback_config(provider)
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
    for provider in PROVIDERS:
        try:
            cfg = provider_runtime(provider)
        except MVPServiceError as exc:
            result[provider] = {"enabled": False, "configured": False, "registry_available": False, "registry_error": str(exc), "credential_source": "none"}
            continue
        result[provider] = {
            "enabled": bool(cfg.get("enabled")),
            "configured": bool(cfg.get("api_key")) or (provider == "ollama" and not _ollama_requires_key()),
            "model": cfg.get("model"),
            "timeout_seconds": cfg.get("timeout_seconds"),
            "max_output_tokens": cfg.get("max_output_tokens"),
            "thinking_level": cfg.get("thinking_level"),
            "credential_source": cfg.get("credential_source"),
            "registry_available": True,
            "project_ref": cfg.get("project_ref"),
            "catalog": PROVIDER_CATALOG.get(provider, []),
        }
    return result


def set_provider_secret(provider: str, secret: str) -> dict:
    provider = str(provider or "").lower().strip()
    if provider not in PROVIDERS:
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
    if provider not in PROVIDERS:
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


def _provider_name(provider: str) -> str:
    return {
        "openai": "OpenAI",
        "anthropic": "Claude",
        "qwen": "Qwen",
        "gemini": "Gemini",
        "openrouter": "OpenRouter",
        "ollama": "Ollama",
    }.get(provider, provider.title())


def _provider_failure(provider: str, exc: Exception) -> MVPServiceError:
    if isinstance(exc, ProviderHTTPError):
        labels = {400: "request rejected", 401: "authentication failed", 403: "access denied", 404: "model or endpoint not found", 429: "rate or quota limited"}
        label = labels.get(exc.status, f"HTTP {exc.status}")
        return MVPServiceError(f"{_provider_name(provider)} {label}: {exc.detail}")
    text = str(exc)
    if text == "provider_timeout":
        return MVPServiceError(f"{provider.title()} timed out before responding")
    return MVPServiceError(f"{provider.title()} request failed: {_safe_provider_detail(text)}")


def get_canonical_convergence_items() -> dict[str, list[dict]]:
    candidates = [
        Path(__file__).resolve().parent / "escd_canonical_convergence_registry.json",
        Path(__file__).resolve().parents[2] / "DCSE_CP_Project" / "SC-ESCD" / "escd_canonical_convergence_registry.json",
    ]
    data = None
    for p in candidates:
        if p.is_file():
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
                break
            except Exception:
                continue
    if not data:
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
                "summary": raw,
                "status": it.get("status", "inactive"),
                "context": "task",
                "task_class": "DO",
                "actionable": False,
                "explicit_priority": 0,
                "source_system": it.get("source", "canonical_convergence")
            })
        elif disp == "IDEA":
            ideas.append({
                "id": cid,
                "item_key": cid,
                "title": title,
                "summary": raw,
                "status": it.get("status", "noncommittal"),
                "context": "idea",
                "task_class": "CAPTURE",
                "actionable": False,
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
                "id": cid,
                "source_type": "DDNA",
                "source_ref_id": cid,
                "source_title": title,
                "entity": "DCSE",
                "lane": "DDNA",
                "status": it.get("status", "staged"),
                "public_safe": True,
                "content_snapshot": raw
            })
        elif disp == "ASSET":
            assets.append({
                "id": cid,
                "asset_id": cid,
                "file_name": title,
                "entity_lane": "DCSE",
                "asset_type": "Canonical Asset",
                "topic": raw[:120],
                "semantic_version": "1.0.0",
                "lifecycle_status": it.get("status", "staged")
            })
    return {"tasks": tasks, "ideas": ideas, "knowledge": knowledge, "ddna": ddna, "assets": assets}


UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
KNOWLEDGE_STATUSES = {"staged", "active", "superseded", "archived"}
KNOWLEDGE_AUTHORITY = {"OBSERVED", "VERIFIED", "LIKELY", "UNKNOWN", "DCS_DIRECTION", "DERIVED"}
ASSET_LIFECYCLE = {"Draft", "Review", "Active", "Deprecated", "Retired"}
ASSET_LANES = {"DCSE", "DCS", "SC", "SS", "TI", "TSL", "FAMILY"}
ASSET_TAGS = {"Public", "SC-Internal", "SS-Internal", "TI-Internal", "DCSE-Confidential", "PPR-Protected"}


def is_uuid(value) -> bool:
    return bool(UUID_RE.match(str(value or "")))


def canonical_record(kind: str, record_id: str) -> dict | None:
    bucket = {"task": "tasks", "idea": "ideas", "knowledge": "knowledge", "asset": "assets"}.get(kind)
    if not bucket:
        return None
    for item in get_canonical_convergence_items().get(bucket, []):
        if str(item.get("id")) == str(record_id):
            return item
    return None


def canonical_item_payload(item: dict) -> dict:
    """escd_items payload for adopting a read-only canonical registry task or idea."""
    kind = "idea" if item.get("context") == "idea" else "task"
    key = str(item.get("item_key") or item.get("id"))
    return {
        "item_key": key,
        "title": str(item.get("title") or key)[:500],
        "summary": item.get("summary"),
        "status": "captured",
        "task_class": "CAPTURE" if kind == "idea" else "DO",
        "context": kind,
        "actionable": False,
        "explicit_priority": 0,
        "source_system": "canonical_convergence",
        "source_id": key,
        "normalized_intent": str(item.get("title") or key)[:500],
        "source_refs": ["escd:canonical:" + key],
        "evidence_refs": [],
    }


def merge_live_and_canonical(live: list[dict], canonical: list[dict], key_fields: tuple[str, ...]) -> list[dict]:
    """Live rows win. A canonical row is shown only when no live row carries its id or key."""
    seen = set()
    for row in live:
        for field in ("id",) + key_fields:
            if row.get(field) not in (None, ""):
                seen.add(str(row.get(field)))
    merged = list(live)
    for row in canonical:
        if str(row.get("id")) not in seen:
            merged.append(dict(row, record_origin="canonical_registry"))
    return merged


def _knowledge_update(payload: dict) -> dict:
    update = {}
    if "title" in payload:
        title = str(payload.get("title") or "").strip()
        if not title:
            raise MVPServiceError("title_required")
        update["title"] = title[:500]
    if "content" in payload:
        content = str(payload.get("content") or "").strip()
        if not content:
            raise MVPServiceError("content_required")
        update["content"] = content
    if "status" in payload:
        if payload["status"] not in KNOWLEDGE_STATUSES:
            raise MVPServiceError("invalid_status")
        update["status"] = payload["status"]
    if "authority_classification" in payload:
        if payload["authority_classification"] not in KNOWLEDGE_AUTHORITY:
            raise MVPServiceError("invalid_authority_classification")
        update["authority_classification"] = payload["authority_classification"]
    if "confidence" in payload and payload["confidence"] not in (None, ""):
        value = float(payload["confidence"])
        if not 0 <= value <= 1:
            raise MVPServiceError("confidence_out_of_range")
        update["confidence"] = value
    return update


def create_knowledge(repo, payload: dict) -> dict:
    fields = _knowledge_update({"title": payload.get("title"), "content": payload.get("content"), **{k: payload[k] for k in ("status", "authority_classification", "confidence") if k in payload}})
    key = "escd-knowledge-" + hashlib.sha256((fields["title"].lower() + "\n" + fields["content"]).encode()).hexdigest()[:32]
    record = {"knowledge_key": key, "status": "staged", "authority_classification": "DERIVED", "evidence_refs": [], "provenance": {"source": "escd_mvp_manual"}}
    record.update(fields)
    return repo.create_knowledge(record)


def adopt_canonical_knowledge(repo, record_id: str) -> dict:
    item = canonical_record("knowledge", record_id)
    if not item:
        raise MVPServiceError("knowledge_not_found")
    existing = repo.get_knowledge_by_key(str(item["id"]))
    if existing:
        return existing
    authority = item.get("authority_classification")
    status = item.get("status")
    return repo.create_knowledge({
        "knowledge_key": str(item["id"]),
        "title": str(item.get("title") or item["id"])[:500],
        "content": str(item.get("content") or item.get("title") or item["id"]),
        "status": status if status in KNOWLEDGE_STATUSES else "staged",
        "authority_classification": authority if authority in KNOWLEDGE_AUTHORITY else "OBSERVED",
        "confidence": float(item.get("confidence") or 0.5),
        "evidence_refs": [],
        "provenance": {"source": "canonical_convergence", "canonical_id": str(item["id"]), "original_authority_classification": authority, "original_status": status},
    })


def update_knowledge(repo, record_id: str, payload: dict) -> dict:
    update = _knowledge_update(payload)
    if not update:
        raise MVPServiceError("no_changes")
    if not is_uuid(record_id):
        record_id = adopt_canonical_knowledge(repo, record_id)["id"]
    return repo.patch_knowledge(record_id, update)


def list_knowledge(limit: int = 200, repo=None) -> list[dict]:
    live = []
    if repo is not None:
        try:
            live = repo.list_knowledge()
        except Exception:
            live = []
    canonical = get_canonical_convergence_items().get("knowledge", [])
    return merge_live_and_canonical(live, canonical, ("knowledge_key",))[:limit]


def search_knowledge(query: str, limit: int = 200, repo=None) -> list[dict]:
    items = list_knowledge(limit=limit, repo=repo)
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


def _asset_is_ps(row: dict) -> bool:
    lane = str(row.get("entity_lane") or "").strip().upper()
    return lane == "PS" or lane.startswith("PS ") or lane.startswith("PS/") or str(row.get("firewall_security_tag") or "") == "PS-Locked"


def _asset_fields(payload: dict, creating: bool) -> dict:
    text_fields = ("file_name", "asset_type", "topic", "description", "storage_location", "semantic_version", "notes", "package")
    update = {}
    for field in text_fields:
        if field in payload and payload[field] is not None:
            update[field] = str(payload[field]).strip()
    if "entity_lane" in payload:
        lane = str(payload.get("entity_lane") or "").strip()
        if lane.upper() not in ASSET_LANES:
            raise MVPServiceError("invalid_or_protected_lane")
        update["entity_lane"] = lane.upper()
    if "firewall_security_tag" in payload:
        if payload["firewall_security_tag"] not in ASSET_TAGS:
            raise MVPServiceError("invalid_or_protected_security_tag")
        update["firewall_security_tag"] = payload["firewall_security_tag"]
    if "lifecycle_status" in payload:
        if payload["lifecycle_status"] not in ASSET_LIFECYCLE:
            raise MVPServiceError("invalid_lifecycle_status")
        update["lifecycle_status"] = payload["lifecycle_status"]
    if "sha256" in payload and str(payload.get("sha256") or "").strip():
        digest = str(payload["sha256"]).strip().lower()
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise MVPServiceError("sha256_must_be_64_hex")
        update["sha256"] = digest
    required = ("file_name", "asset_type", "topic", "description", "storage_location", "entity_lane", "firewall_security_tag")
    for field in required:
        if (creating or field in update) and not update.get(field):
            raise MVPServiceError(field + "_required")
    return update


def _asset_request(method: str, query: str, payload=None):
    url, key = _service_config()
    headers = _postgrest_headers(key, "public")
    headers["Prefer"] = "return=representation"
    try:
        _, rows = _http_json(f"{url}/rest/v1/{query}", method=method, headers=headers, payload=payload, timeout=15)
    except ProviderHTTPError as exc:
        raise MVPServiceError(f"asset_registry_{exc.status}: {exc.detail}") from None
    return rows if isinstance(rows, list) else []


def get_asset(asset_id: str) -> dict | None:
    rows = _asset_request("GET", "dcse_asset_registry?select=*&limit=1&asset_id=eq." + parse.quote(str(asset_id), safe=""))
    return rows[0] if rows else None


def create_asset(payload: dict) -> dict:
    if not payload.get("file_name") and not payload.get("asset_id"):
        raise MVPServiceError("asset_file_name_required")
    fields = _asset_fields(payload, creating=True)
    asset_id = str(payload.get("asset_id") or "").strip() or "ESCD-ASSET-" + hashlib.sha256((fields["file_name"] + "\n" + fields["storage_location"]).encode()).hexdigest()[:12].upper()
    if not re.fullmatch(r"[A-Za-z0-9._:\-]{3,120}", asset_id):
        raise MVPServiceError("invalid_asset_id")
    if get_asset(asset_id):
        raise MVPServiceError("asset_id_already_exists")
    record = {"asset_id": asset_id, "author_model": "escd_mvp_operator", "sha256": "UNVERIFIED", "hash_verified": False, "lifecycle_status": "Draft", "semantic_version": "1.0.0"}
    record.update(fields)
    rows = _asset_request("POST", "dcse_asset_registry", record)
    if not rows:
        raise MVPServiceError("asset_create_failed")
    return rows[0]


def update_asset(asset_id: str, payload: dict) -> dict:
    existing = get_asset(asset_id)
    if existing and _asset_is_ps(existing):
        raise MVPServiceError("protected_lane_record")
    if not existing:
        canonical = canonical_record("asset", asset_id)
        if not canonical:
            raise MVPServiceError("asset_not_found")
        seed = {
            "asset_id": str(canonical["asset_id"]),
            "file_name": canonical.get("file_name") or canonical["asset_id"],
            "asset_type": canonical.get("asset_type") or "Canonical Asset",
            "topic": canonical.get("topic") or canonical["asset_id"],
            "description": canonical.get("topic") or canonical["asset_id"],
            "storage_location": "escd:canonical_convergence_registry",
            "entity_lane": "DCSE",
            "firewall_security_tag": "DCSE-Confidential",
        }
        seed.update({k: v for k, v in payload.items() if k != "asset_id"})
        return create_asset(seed)
    fields = _asset_fields(payload, creating=False)
    if not fields:
        raise MVPServiceError("no_changes")
    if "sha256" in fields and fields["sha256"] != existing.get("sha256"):
        fields["hash_verified"] = False
        fields["hash_verified_at"] = None
    fields["last_modified_at"] = datetime.now(timezone.utc).isoformat()
    rows = _asset_request("PATCH", "dcse_asset_registry?asset_id=eq." + parse.quote(str(asset_id), safe=""), fields)
    if not rows:
        raise MVPServiceError("asset_update_failed")
    return rows[0]


def list_assets(limit: int = 200) -> list[dict]:
    url, key = _service_config()
    # Lane firewall: PS-locked and PS-lane rows never reach the ESCD surface.
    query = "dcse_asset_registry?select=*&firewall_security_tag=neq.PS-Locked&entity_lane=not.ilike.PS*&order=last_modified_at.desc.nullslast,created_at.desc.nullslast,id.asc&limit=" + str(max(1, min(limit, 500)))
    rows = []
    try:
        _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "public"))
    except Exception:
        pass
    if not isinstance(rows, list):
        rows = []
    rows = [r for r in rows if not _asset_is_ps(r)]
    canonical = get_canonical_convergence_items().get("assets", [])
    return merge_live_and_canonical(rows, canonical, ("asset_id",))[:limit]


def list_ddna_sources(limit: int = 200) -> list[dict]:
    rows = []
    url = (os.getenv("DDNA_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("DDNA_SUPABASE_SERVICE_ROLE_KEY") or ""
    schema = "dcse_ddna_legacy"
    if not url or not key:
        try:
            url, key = _service_config()
            schema = "dcse_cp"
        except Exception:
            pass
    if url and key:
        fields = "id,source_type,source_ref_id,source_title,entity,lane,priority,status,assigned_model,assigned_agent_key,ps_lock,public_safe,queued_by,queued_at,extracted_at,notes,retry_count,max_retries,last_error,batch_id,content_snapshot"
        query = f"ddna_source_queue?select={fields}&order=queued_at.desc.nullslast,id.asc&limit={max(1, min(limit, 500))}"
        try:
            _, fetched = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, schema))
            if isinstance(fetched, list):
                rows.extend(fetched)
        except Exception:
            try:
                url, key = _service_config()
                _, fetched = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_cp"))
                if isinstance(fetched, list):
                    rows.extend(fetched)
            except Exception:
                pass
    canonical = get_canonical_convergence_items().get("ddna", [])
    existing_refs = {str(r.get("source_ref_id") or r.get("id")) for r in rows}
    for item in canonical:
        if item.get("source_ref_id") not in existing_refs:
            rows.append(item)
    return rows[:limit]


def list_ddna_jobs(source_queue_id: str) -> list[dict]:
    url = (os.getenv("DDNA_SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("DDNA_SUPABASE_SERVICE_ROLE_KEY") or ""
    schema = "dcse_ddna_legacy"
    if not url or not key:
        try:
            url, key = _service_config()
            schema = "dcse_cp"
        except Exception:
            pass
    if not url or not key:
        return []
    safe = parse.quote(source_queue_id, safe="")
    fields = "id,job_key,source_queue_id,model_id,provider,status,error_message,retry_count,duration_ms,characteristics_extracted,started_at,completed_at,created_at"
    query = f"ddna_ollama_jobs?source_queue_id=eq.{safe}&select={fields}&order=created_at.desc,id.asc"
    try:
        _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, schema))
        return rows if isinstance(rows, list) else []
    except Exception:
        return []


def create_ddna_source(payload: dict) -> dict:
    if not payload.get("source_title") and not payload.get("source_ref_id"):
        raise MVPServiceError("source_title_or_ref_required")
    url, key = _service_config()
    headers = dict(_postgrest_headers(key, "dcse_cp"))
    headers["Prefer"] = "return=representation"
    _, rows = _http_json(f"{url}/rest/v1/ddna_source_queue", method="POST", headers=headers, payload=payload)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def patch_ddna_source(source_id: str, update: dict) -> dict:
    url, key = _service_config()
    safe = parse.quote(str(source_id), safe="")
    headers = dict(_postgrest_headers(key, "dcse_cp"))
    headers["Prefer"] = "return=representation"
    col = "id" if "-" in str(source_id) and len(str(source_id)) == 36 else "source_ref_id"
    _, rows = _http_json(f"{url}/rest/v1/ddna_source_queue?{col}=eq.{safe}", method="PATCH", headers=headers, payload=update)
    if isinstance(rows, list) and rows:
        return rows[0]
    return rows if isinstance(rows, dict) else {"ok": True}


def delete_ddna_source(source_id: str) -> bool:
    url, key = _service_config()
    safe = parse.quote(str(source_id), safe="")
    col = "id" if "-" in str(source_id) and len(str(source_id)) == 36 else "source_ref_id"
    _http_json(f"{url}/rest/v1/ddna_source_queue?{col}=eq.{safe}", method="DELETE", headers=_postgrest_headers(key, "dcse_cp"))
    return True


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
        "type": str(mime_type or "application/octet-stream"),
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
    url, key = _service_config()
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
            raise MVPServiceError("record_not_found")
        refs = item.get("evidence_refs") or []
        refs = list(refs) if isinstance(refs, list) else []
        refs.append(attachment)
        repo.patch_item(rec_id, {"evidence_refs": refs})
    elif rec_type == "asset":
        row = _asset_by_id(rec_id)
        if not row:
            raise MVPServiceError("record_not_found")
        metadata = row.get("metadata") if isinstance(row.get("metadata"), dict) else {}
        refs = metadata.get("attachments") if isinstance(metadata.get("attachments"), list) else []
        refs = list(refs) if isinstance(refs, list) else []
        refs.append(attachment)
        metadata = dict(metadata)
        metadata["attachments"] = refs
        patch_asset(rec_id, {"metadata": metadata})
    elif rec_type == "ddna":
        row = _ddna_by_id(rec_id)
        if not row:
            raise MVPServiceError("record_not_found")
        existing_notes = str(row.get("notes") or "").strip()
        marker = _ddna_attachment_marker(attachment)
        updated_notes = (existing_notes + "\n" + marker).strip() if existing_notes else marker
        patch_ddna_source(rec_id, {"notes": updated_notes})
    else:
        raise MVPServiceError("invalid_record_type")
    return attachment


def create_signed_attachment_download(storage_path: str, file_name: str = "", expires_in: int = 300) -> dict:
    path = _safe_storage_path(storage_path)
    ttl = max(60, min(int(expires_in or 300), 3600))
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


def get_conversation_state(conversation_id: str = "conv_default") -> dict:
    from apps.escd.runtime.continuity import ConversationStore
    state, turns = ConversationStore.get_conversation(conversation_id)
    return {
        "conversation_id": state.conversation_id,
        "state": state.to_dict(),
        "turns": [t.to_dict() for t in turns],
    }


def reset_conversation(conversation_id: str = "conv_default") -> dict:
    from apps.escd.runtime.continuity import ConversationState, ConversationStore
    cid = str(conversation_id or "conv_default").strip()
    new_state = ConversationState(conversation_id=cid)
    ConversationStore._cache[cid] = {"state": new_state, "turns": []}
    return {"conversation_id": cid, "state": new_state.to_dict(), "turns": []}


def save_chat(conversation_id: str = "conv_default", title: str = "") -> dict:
    from apps.escd.runtime.continuity import ConversationStore
    return ConversationStore.save_explicit_chat(conversation_id, title)


def list_saved_chats(limit: int = 50) -> list[dict]:
    from apps.escd.runtime.continuity import ConversationStore
    return ConversationStore.list_saved_chats(limit)


def governance_status() -> dict:
    """Return the evidence-scoped V7.3 cross-system status contract."""
    from apps.escd.runtime.governance_runtime import cross_system_status
    return cross_system_status()


def chat(provider: str, messages: list[dict], conversation_id: str = "conv_default", model_override: str = None) -> dict:
    from apps.escd.runtime.continuity import (
        ConversationStore,
        TurnRecord,
        assemble_context_packet,
        retrieve_governed_context,
        validate_response,
    )

    provider = str(provider or "").lower().strip()
    cid = str(conversation_id or "conv_default").strip() or "conv_default"

    cfg = provider_runtime(provider)
    key = str(cfg.get("api_key") or "")
    if not key and not (provider == "ollama" and not _ollama_requires_key()):
        raise MVPServiceError(f"{provider.title()} credential is not configured. Add it in ESCD Provider Settings")
    if not cfg.get("enabled"):
        try:
            update_provider_config(provider, {"enabled": True})
            cfg["enabled"] = True
        except Exception:
            raise MVPServiceError(f"{provider.title()} is disabled in ESCD Provider Settings")
    model = str(model_override or "").strip() or str(cfg.get("model") or "").strip()
    timeout = int(cfg.get("timeout_seconds") or 30)
    max_tokens = int(cfg.get("max_output_tokens") or 1024)

    # Extract current user prompt
    last_user = ""
    for m in reversed(messages):
        if str(m.get("role") or "").lower() == "user":
            last_user = str(m.get("content") or "").strip()
            if last_user:
                break
    if not last_user:
        raise MVPServiceError("chat_message_required")

    # Load canonical conversation state & turn history (Rule 1 & 3)
    state, turns = ConversationStore.get_conversation(cid)

    # Retrieve governed context (Rule 5 Layer C)
    retrieved = retrieve_governed_context(last_user, limit=4)

    # Assemble governed context packet and retain its quiet machine-readable attestation.
    from apps.escd.runtime.governance_runtime import runtime_context
    _, governance_attestation = runtime_context(state, last_user, turns)
    clean = assemble_context_packet(state, last_user, turns, retrieved)
    clean.insert(1 if clean and clean[0].get("role") == "system" else 0, {
        "role": "system",
        "content": f"Current execution engine for this reply: {_provider_name(provider)} ({model}). Identity stays ESCD; name this engine if asked which engine or model answered.",
    })

    try:
        data = None
        text = ""

        if provider == "openai":
            # For OpenAI responses API, adapt roles
            oai_clean = []
            for item in clean:
                role = item["role"]
                if role == "system":
                    role = "developer"
                oai_clean.append({"role": role, "content": item["content"][:12000]})
            _, data = _http_json(
                "https://api.openai.com/v1/responses",
                method="POST",
                headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                payload={"model": model, "input": oai_clean, "max_output_tokens": max_tokens},
                timeout=timeout,
            )
            text = _openai_output_text(data or {})
            if not text:
                raise MVPServiceError("OpenAI returned an empty response")

        elif provider == "gemini":
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

        elif provider == "openrouter":
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

        elif provider in ("qwen", "dashscope"):
            url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": clean, "max_tokens": max_tokens}
            _, data = _http_json(url, method="POST", headers=headers, payload=payload, timeout=timeout)
            choices = (data or {}).get("choices") or []
            text = str((((choices[0] if choices else {}).get("message") or {}).get("content") or "")).strip()
            if not text:
                raise MVPServiceError("Qwen returned an empty response")

        elif provider == "anthropic":
            system_text = "\n".join(m["content"] for m in clean if m["role"] == "system").strip()
            anthropic_turns = []
            for m in clean:
                if m["role"] == "system":
                    continue
                role = "assistant" if m["role"] == "assistant" else "user"
                if anthropic_turns and anthropic_turns[-1]["role"] == role:
                    anthropic_turns[-1]["content"] += "\n\n" + m["content"]
                else:
                    anthropic_turns.append({"role": role, "content": m["content"]})
            while anthropic_turns and anthropic_turns[0]["role"] != "user":
                anthropic_turns.pop(0)
            payload = {"model": model, "max_tokens": max_tokens, "messages": anthropic_turns}
            if system_text:
                payload["system"] = system_text
            _, data = _http_json(
                "https://api.anthropic.com/v1/messages",
                method="POST",
                headers={"x-api-key": key, "anthropic-version": ANTHROPIC_VERSION, "Content-Type": "application/json"},
                payload=payload,
                timeout=timeout,
            )
            text = "\n".join(str(b.get("text") or "") for b in ((data or {}).get("content") or []) if b.get("type") == "text").strip()
            if not text:
                raise MVPServiceError("Claude returned an empty response")

        elif provider == "ollama":
            headers = {"Content-Type": "application/json"}
            if key:
                headers["Authorization"] = f"Bearer {key}"
            _, data = _http_json(
                _ollama_base_url() + "/api/chat",
                method="POST",
                headers=headers,
                payload={"model": model, "messages": clean, "stream": False, "options": {"num_predict": max_tokens}},
                timeout=timeout,
            )
            text = str((((data or {}).get("message") or {}).get("content") or "")).strip()
            if not text:
                raise MVPServiceError("Ollama returned an empty response")

        else:
            raise MVPServiceError("unsupported_provider")

        # Response Validation
        valid, err = validate_response(text, state)
        if not valid:
            raise MVPServiceError(f"Response validation failed: {err}")

        # Update active session turn history (no automatic DB conversion)
        new_seq = len(turns) + 1
        turn = TurnRecord(
            conversation_id=cid,
            seq=new_seq,
            user_message=last_user,
            assistant_response=text,
            provider=provider,
            model=(data or {}).get("model") or model,
            entity_lane=state.active_entity_lane,
            retrieved_refs=retrieved,
            governance_attestation=governance_attestation,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        ConversationStore.record_turn(state, turn)

        return {
            "provider": provider,
            "model": (data or {}).get("model") or model,
            "content": text,
            "conversation_id": cid,
            "seq": new_seq,
            "state": state.to_dict(),
            "governance": governance_attestation,
        }

    except Exception as exc:
        if isinstance(exc, MVPServiceError) and not isinstance(exc, ProviderHTTPError) and str(exc).startswith(("OpenAI returned", "Claude returned", "Gemini returned", "OpenRouter returned", "Ollama returned")):
            raise
        raise _provider_failure(provider, exc) from None




# ---------------------------------------------------------------------------
# AI Orchestrator (DCSE agent message bus). ESCD participates as the DCS console
# under the dcs_authority identity. Messages are communication only
# (execution_authorized is always false at the database); every delivery carries a receipt.
# ---------------------------------------------------------------------------
ORCH_IDENTITY = "dcs_authority"
ORCH_READER = "dcs_authority@escd-console"
ORCH_AGENT_KEY_RE = re.compile(r"^[a-z0-9_]{2,64}$")
ORCH_MESSAGE_FIELDS = "id,correlation_id,reply_to,sender,recipient_agent_key,subject,body,message_class,status,attempts,max_attempts,first_delivered_at,acknowledged_at,acknowledged_by_instance,receipt,expires_at,metadata,created_at"


def _orch_get(query: str):
    url, key = _service_config()
    try:
        _, rows = _http_json(f"{url}/rest/v1/{query}", headers=_postgrest_headers(key, "dcse_cp"), timeout=12)
    except ProviderHTTPError as exc:
        raise MVPServiceError(f"orchestrator_read_failed_{exc.status}") from None
    return rows if isinstance(rows, list) else []


def _orch_rpc(name: str, payload: dict):
    try:
        return _rpc(name, payload)
    except ProviderHTTPError as exc:
        detail = str(exc.detail or "")
        for code in ("REPLY_NOT_ELIGIBLE", "DUPLICATE_REPLY"):
            if code in detail:
                raise MVPServiceError(code) from None
        raise MVPServiceError(f"orchestrator_write_failed_{exc.status}") from None


def orchestrator_agents() -> list[dict]:
    rows = _orch_get("agent_registry?select=agent_key,display_name,agent_type,status,metadata&status=in.(active,standby)&order=agent_key.asc")
    out = []
    for row in rows:
        key = str(row.get("agent_key") or "")
        if key == ORCH_IDENTITY or not ORCH_AGENT_KEY_RE.match(key):
            continue
        meta = row.get("metadata") or {}
        surface = str(meta.get("expected_runtime_surface") or meta.get("verified_runtime_surface") or "")
        # Host CLI agents get messages pushed by the Windows worker; chat surfaces pull them.
        mode = meta.get("delivery_mode") or ("push" if surface.endswith("_cli") else "pull")
        out.append({
            "agent_key": key,
            "display_name": row.get("display_name") or key,
            "agent_type": row.get("agent_type"),
            "status": row.get("status"),
            "delivery_mode": mode,
            "admission_status": meta.get("admission_status") or meta.get("v7_1_runtime_admission_status"),
        })
    return out


def _orch_clean_text(value, field: str, limit: int) -> str:
    text = str(value or "").strip()
    if not text:
        raise MVPServiceError(field + "_required")
    if len(text) > limit:
        raise MVPServiceError(f"{field}_too_long_max_{limit}")
    return text


def orchestrator_send(recipients, subject, body, record=None, operator_email: str = "") -> dict:
    if isinstance(recipients, str):
        recipients = [recipients]
    wanted = []
    for r in recipients or []:
        key = str(r or "").strip().lower()
        if key and key not in wanted:
            wanted.append(key)
    if not wanted:
        raise MVPServiceError("recipient_required")
    if len(wanted) > 12:
        raise MVPServiceError("too_many_recipients")
    known = {a["agent_key"] for a in orchestrator_agents()}
    unknown = [k for k in wanted if k not in known]
    if unknown:
        raise MVPServiceError("unknown_or_inactive_agent: " + ", ".join(unknown))
    subject = _orch_clean_text(subject, "subject", 200)
    body = _orch_clean_text(body, "body", 20000)
    metadata = {"origin": "escd_console", "expects_reply": True}
    if operator_email:
        metadata["operator"] = str(operator_email)[:200]
    if isinstance(record, dict) and record.get("id"):
        metadata["record"] = {
            "kind": str(record.get("kind") or "")[:20],
            "id": str(record.get("id"))[:120],
            "title": str(record.get("title") or "")[:300],
        }
    import uuid as _uuid
    correlation = str(_uuid.uuid4())
    sent = []
    for key in wanted:
        message_id = _orch_rpc("send_agent_message", {
            "p_sender": ORCH_IDENTITY,
            "p_recipient_agent_key": key,
            "p_subject": subject,
            "p_body": body,
            "p_message_class": "communication",
            "p_ttl_minutes": 1440,
            "p_correlation_id": correlation,
            "p_metadata": metadata,
        })
        sent.append({"message_id": message_id, "recipient": key})
    return {"correlation_id": correlation, "sent": sent}


def orchestrator_sync(limit: int = 50) -> list[dict]:
    """Pull new messages addressed to DCS. The database records a reader receipt for each."""
    rows = _orch_rpc("read_agent_messages", {"p_agent_key": ORCH_IDENTITY, "p_reader_instance": ORCH_READER, "p_limit": max(1, min(int(limit), 100))})
    return rows if isinstance(rows, list) else []


def orchestrator_threads(days: int = 7) -> dict:
    received = orchestrator_sync()
    since = datetime.now(timezone.utc).timestamp() - max(1, min(int(days), 30)) * 86400
    since_iso = parse.quote(datetime.fromtimestamp(since, timezone.utc).isoformat(), safe="")
    base = f"agent_messages?select={ORCH_MESSAGE_FIELDS}&created_at=gte.{since_iso}&order=created_at.asc&limit=500"
    rows = _orch_get(base + f"&or=(sender.eq.{ORCH_IDENTITY},recipient_agent_key.eq.{ORCH_IDENTITY})")
    # Include other participants' messages inside the same conversations (for example agent-to-agent replies).
    corr = sorted({str(r.get("correlation_id")) for r in rows if r.get("correlation_id")})
    if corr:
        extra = []
        for i in range(0, len(corr), 40):
            chunk = ",".join(corr[i:i + 40])
            extra.extend(_orch_get(f"agent_messages?select={ORCH_MESSAGE_FIELDS}&correlation_id=in.({chunk})&order=created_at.asc&limit=500"))
        seen = {str(r.get("id")) for r in rows}
        rows.extend(r for r in extra if str(r.get("id")) not in seen)
    health = {}
    sent_ids = [str(r["id"]) for r in rows if r.get("sender") == ORCH_IDENTITY]
    for i in range(0, len(sent_ids), 60):
        chunk = ",".join(sent_ids[i:i + 60])
        for h in _orch_get(f"agent_message_delivery_status?select=id,delivery_health,recipient_last_heartbeat&id=in.({chunk})"):
            health[str(h.get("id"))] = h
    threads = {}
    for r in sorted(rows, key=lambda x: str(x.get("created_at"))):
        receipt = r.get("receipt") or {}
        msg = {k: r.get(k) for k in ("id", "reply_to", "sender", "recipient_agent_key", "subject", "body", "message_class", "status", "attempts", "max_attempts", "first_delivered_at", "acknowledged_at", "acknowledged_by_instance", "expires_at", "created_at")}
        msg["receipt_type"] = receipt.get("receipt_type") if isinstance(receipt, dict) else None
        msg["delivery_health"] = (health.get(str(r.get("id"))) or {}).get("delivery_health")
        msg["recipient_last_heartbeat"] = (health.get(str(r.get("id"))) or {}).get("recipient_last_heartbeat")
        msg["record"] = (r.get("metadata") or {}).get("record")
        msg["incoming"] = r.get("recipient_agent_key") == ORCH_IDENTITY
        cid = str(r.get("correlation_id") or r.get("id"))
        t = threads.setdefault(cid, {"correlation_id": cid, "subject": r.get("subject"), "participants": [], "messages": [], "record": None})
        for p in (r.get("sender"), r.get("recipient_agent_key")):
            if p and p not in t["participants"]:
                t["participants"].append(p)
        if msg["record"] and not t["record"]:
            t["record"] = msg["record"]
        t["messages"].append(msg)
    new_ids = {str(x.get("id")) for x in received}
    out = []
    for t in threads.values():
        t["last_at"] = t["messages"][-1]["created_at"]
        t["new_count"] = sum(1 for m in t["messages"] if str(m["id"]) in new_ids)
        out.append(t)
    out.sort(key=lambda t: str(t["last_at"]), reverse=True)
    return {"threads": out, "new_count": len(new_ids), "identity": ORCH_IDENTITY}


def orchestrator_reply(message_id: str, body: str, operator_email: str = "") -> dict:
    if not is_uuid(message_id):
        raise MVPServiceError("invalid_message_id")
    body = _orch_clean_text(body, "body", 20000)
    rows = _orch_get(f"agent_messages?select=id,sender,recipient_agent_key,subject,correlation_id&id=eq.{message_id}&limit=1")
    if not rows:
        raise MVPServiceError("message_not_found")
    orig = rows[0]
    if orig.get("recipient_agent_key") != ORCH_IDENTITY:
        raise MVPServiceError("can_only_reply_to_messages_addressed_to_dcs")
    to = str(orig.get("sender") or "")
    if not ORCH_AGENT_KEY_RE.match(to):
        raise MVPServiceError("sender_is_not_a_registered_agent")
    subject = str(orig.get("subject") or "")
    if not subject.lower().startswith("re:"):
        subject = "RE: " + subject
    metadata = {"origin": "escd_console", "expects_reply": True}
    if operator_email:
        metadata["operator"] = str(operator_email)[:200]
    payload = {
        "p_sender": ORCH_IDENTITY,
        "p_recipient_agent_key": to,
        "p_subject": subject[:200],
        "p_body": body,
        "p_message_class": "reply",
        "p_ttl_minutes": 1440,
        "p_correlation_id": orig.get("correlation_id"),
        "p_reply_to": orig.get("id"),
        "p_metadata": metadata,
    }
    mode = "reply"
    try:
        new_id = _orch_rpc("send_agent_message", payload)
    except MVPServiceError as exc:
        # The database stops agents from answering acknowledgements (and from answering twice).
        # DCS keeps the conversation going with a follow-up in the same thread, which agents may answer.
        if str(exc) not in {"REPLY_NOT_ELIGIBLE", "DUPLICATE_REPLY"}:
            raise
        payload.update({"p_message_class": "communication", "p_reply_to": None, "p_metadata": dict(metadata, follow_up_of=str(orig.get("id")))})
        new_id = _orch_rpc("send_agent_message", payload)
        mode = "follow_up"
    return {"message_id": new_id, "recipient": to, "correlation_id": orig.get("correlation_id"), "mode": mode}
