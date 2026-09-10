from __future__ import annotations

from urllib import parse

from .repository import RepositoryError, SupabaseRLSClient


def ensure_item_source(
    repo: SupabaseRLSClient,
    *,
    source_link_key: str,
    item_id: str,
    source_system: str,
    source_id: str,
    source_ref: str,
) -> dict:
    safe = parse.quote(source_link_key, safe="")
    rows = repo._call("GET", f"escd_item_sources?source_link_key=eq.{safe}&select=*&limit=1")
    if rows:
        return rows[0]
    payload = {
        "source_link_key": source_link_key,
        "item_id": item_id,
        "source_system": source_system,
        "source_id": source_id,
        "source_ref": source_ref,
    }
    try:
        rows = repo._call("POST", "escd_item_sources", payload)
    except RepositoryError as exc:
        if str(exc) == "postgrest_409":
            rows = repo._call("GET", f"escd_item_sources?source_link_key=eq.{safe}&select=*&limit=1")
            if rows:
                return rows[0]
        raise
    if not rows:
        raise RepositoryError("item_source_link_create_failed")
    return rows[0]
