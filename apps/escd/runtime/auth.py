from __future__ import annotations

from dataclasses import dataclass
import json
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


def _default_http_get(url: str, headers: dict[str, str], timeout: int = 10) -> tuple[int, dict[str, Any]]:
    req = request.Request(url, headers=headers, method="GET")
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


def verify_supabase_user(
    access_token: str,
    supabase_url: str,
    anon_key: str,
    http_get: Callable[[str, dict[str, str], int], tuple[int, dict[str, Any]]] | None = None,
) -> AuthContext:
    if not supabase_url or not anon_key:
        raise AuthError("auth_configuration_missing")
    getter = http_get or _default_http_get
    status, payload = getter(
        supabase_url.rstrip("/") + "/auth/v1/user",
        {"Authorization": f"Bearer {access_token}", "apikey": anon_key},
        10,
    )
    if status != 200:
        raise AuthError("invalid_or_expired_token")
    user_id = str(payload.get("id") or "").strip()
    if not user_id:
        raise AuthError("auth_user_id_missing")
    email = payload.get("email")
    return AuthContext(user_id=user_id, email=str(email).lower() if email else None, access_token=access_token)


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
