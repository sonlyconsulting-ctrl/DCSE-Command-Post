from __future__ import annotations

from typing import Any, Iterable
from urllib import parse

from apps.escd.runtime.repository import RepositoryError, SupabaseRLSClient


def _safe(value: object) -> str:
    return parse.quote(str(value), safe="")


def list_templates(repo: SupabaseRLSClient) -> list[dict[str, Any]]:
    return repo._call(
        "GET",
        "escd_workflow_templates?select=*&order=template_id.asc,version.desc&limit=200",
    )


def get_template(repo: SupabaseRLSClient, template_id: str, version: str) -> dict[str, Any] | None:
    rows = repo._call(
        "GET",
        f"escd_workflow_templates?template_id=eq.{_safe(template_id)}&version=eq.{_safe(version)}&select=*&limit=1",
    )
    return rows[0] if rows else None


def create_template(repo: SupabaseRLSClient, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_template(repo, str(payload.get("template_id") or ""), str(payload.get("version") or ""))
    if existing:
        if existing.get("definition_fingerprint") != payload.get("definition_fingerprint"):
            raise RepositoryError("workflow_template_version_conflict")
        return existing
    try:
        rows = repo._call("POST", "escd_workflow_templates", payload)
    except RepositoryError as exc:
        if str(exc) == "postgrest_409":
            existing = get_template(repo, str(payload.get("template_id") or ""), str(payload.get("version") or ""))
            if existing and existing.get("definition_fingerprint") == payload.get("definition_fingerprint"):
                return existing
        raise
    if not rows:
        raise RepositoryError("workflow_template_create_failed")
    return rows[0]


def list_instances(repo: SupabaseRLSClient) -> list[dict[str, Any]]:
    return repo._call(
        "GET",
        "escd_workflow_instances?select=*&order=updated_at.desc,id.asc&limit=300",
    )


def get_instance(repo: SupabaseRLSClient, instance_id: str) -> dict[str, Any] | None:
    rows = repo._call("GET", f"escd_workflow_instances?id=eq.{_safe(instance_id)}&select=*&limit=1")
    return rows[0] if rows else None


def get_instance_by_key(repo: SupabaseRLSClient, instance_key: str) -> dict[str, Any] | None:
    rows = repo._call(
        "GET",
        f"escd_workflow_instances?instance_key=eq.{_safe(instance_key)}&select=*&limit=1",
    )
    return rows[0] if rows else None


def create_instance(repo: SupabaseRLSClient, payload: dict[str, Any]) -> dict[str, Any]:
    key = str(payload.get("instance_key") or "")
    existing = get_instance_by_key(repo, key)
    if existing:
        return existing
    try:
        rows = repo._call("POST", "escd_workflow_instances", payload)
    except RepositoryError as exc:
        if str(exc) == "postgrest_409":
            existing = get_instance_by_key(repo, key)
            if existing:
                return existing
        raise
    if not rows:
        raise RepositoryError("workflow_instance_create_failed")
    return rows[0]


def patch_instance(repo: SupabaseRLSClient, instance_id: str, update: dict[str, Any]) -> dict[str, Any]:
    rows = repo._call("PATCH", f"escd_workflow_instances?id=eq.{_safe(instance_id)}", update)
    if not rows:
        raise RepositoryError("workflow_instance_update_failed")
    return rows[0]


def list_steps(repo: SupabaseRLSClient, instance_id: str) -> list[dict[str, Any]]:
    return repo._call(
        "GET",
        f"escd_workflow_steps?instance_id=eq.{_safe(instance_id)}&select=*&order=sequence_no.asc,step_id.asc",
    )


def create_steps(repo: SupabaseRLSClient, steps: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    payload = list(steps)
    if not payload:
        return []
    rows = repo._call("POST", "escd_workflow_steps", payload)
    if not rows:
        raise RepositoryError("workflow_steps_create_failed")
    return rows


def get_step(repo: SupabaseRLSClient, instance_id: str, step_id: str) -> dict[str, Any] | None:
    rows = repo._call(
        "GET",
        f"escd_workflow_steps?instance_id=eq.{_safe(instance_id)}&step_id=eq.{_safe(step_id)}&select=*&limit=1",
    )
    return rows[0] if rows else None


def patch_step(repo: SupabaseRLSClient, instance_id: str, step_id: str, update: dict[str, Any]) -> dict[str, Any]:
    rows = repo._call(
        "PATCH",
        f"escd_workflow_steps?instance_id=eq.{_safe(instance_id)}&step_id=eq.{_safe(step_id)}",
        update,
    )
    if not rows:
        raise RepositoryError("workflow_step_update_failed")
    return rows[0]


def list_events(repo: SupabaseRLSClient, instance_id: str) -> list[dict[str, Any]]:
    return repo._call(
        "GET",
        f"escd_workflow_events?instance_id=eq.{_safe(instance_id)}&select=*&order=created_at.desc,id.desc&limit=300",
    )
