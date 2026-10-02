from __future__ import annotations

from dataclasses import dataclass
import json
import socket
from typing import Any, Callable, Mapping
from urllib import request, error


class AuthError(RuntimeError):
    pass


@dataclass(frozen=True)
class AuthContext:
    user_id: str
    email: str | None
    access_token: str


def extract_bearer(headers: Mapping[str, str]) -> str:
    value = headers.get("Authorization") or headers.get("authorization") or ""
    parts = value.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1].strip():
        raise AuthError("missing_bearer_token")
    return parts[1].strip()


import time

_AUTH_CACHE: dict[str, tuple[float, AuthContext]] = {}
_AUTH_CACHE_TTL = 60.0


def _default_http_get(url: str, headers: dict[str, str], timeout: int = 8) -> tuple[int, dict[str, Any]]:
    req = request.Request(url, headers=headers, method="GET")
    for attempt in range(2):
        try:
            with request.urlopen(req, timeout=timeout) as response:
                body = response.read().decode("utf-8")
                return response.status, json.loads(body or "{}")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            try:
                parsed = json.loads(body or "{}")
            except json.JSONDecodeError:
                parsed = {"error": "auth_http_error"}
            return exc.code, parsed
        except (TimeoutError, socket.timeout):
            if attempt == 0:
                time.sleep(0.3)
                continue
            return 504, {"error": "auth_timeout"}
        except error.URLError as exc:
            if attempt == 0:
                time.sleep(0.3)
                continue
            return 503, {"error": f"auth_unreachable: {exc.reason}"}
    return 504, {"error": "auth_timeout"}


def verify_supabase_user(
    access_token: str,
    supabase_url: str,
    anon_key: str,
    http_get: Callable[[str, dict[str, str], int], tuple[int, dict[str, Any]]] | None = None,
) -> AuthContext:
    if not supabase_url or not anon_key:
        raise AuthError("auth_configuration_missing")
    now = time.time()
    # Fast in-memory cache to prevent redundant Supabase Auth round-trips on every request
    if not http_get and access_token in _AUTH_CACHE:
        cached_at, cached_ctx = _AUTH_CACHE[access_token]
        if (now - cached_at) < _AUTH_CACHE_TTL:
            return cached_ctx
    getter = http_get or _default_http_get
    status, payload = getter(
        supabase_url.rstrip("/") + "/auth/v1/user",
        {"Authorization": f"Bearer {access_token}", "apikey": anon_key},
        8,
    )
    if status != 200:
        if status in (503, 504):
            raise AuthError("auth_service_temporarily_unreachable")
        raise AuthError("invalid_or_expired_token")

    user_id = str(payload.get("id") or "").strip()
    if not user_id:
        raise AuthError("auth_user_id_missing")
    email = payload.get("email")
    ctx = AuthContext(user_id=user_id, email=str(email).lower() if email else None, access_token=access_token)
    if not http_get:
        _AUTH_CACHE[access_token] = (now, ctx)
    return ctx


def authorize_operator(auth: AuthContext, operator_rows: list[dict[str, Any]]) -> dict[str, Any]:
    allowed_scopes = {"dcse_internal_dashboards", "dcse_owner"}
    for row in operator_rows:
        if (
            str(row.get("user_id")) == auth.user_id
            and row.get("active") is True
            and row.get("access_scope") in allowed_scopes
        ):
            return row
    raise AuthError("dcs_operator_not_authorized")
