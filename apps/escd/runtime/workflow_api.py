from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlparse

from apps.escd.runtime.repository import RepositoryError, SupabaseRLSClient
from apps.escd.runtime.workflow_engine import (
    instantiate_steps,
    instantiate_workflow,
    normalize_template,
    transition_instance,
    transition_step,
    workflow_view,
)
from apps.escd.runtime.workflow_repository import (
    create_instance,
    create_steps,
    create_template,
    get_instance,
    get_step,
    get_template,
    list_events,
    list_instances,
    list_steps,
    list_templates,
    patch_instance,
    patch_step,
)


WORKFLOW_GET_PATHS = {
    "/api/escd/workflow-templates",
    "/api/escd/workflows",
    "/api/escd/workflows/detail",
}
WORKFLOW_POST_PATHS = {
    "/api/escd/workflow-templates",
    "/api/escd/workflows/instantiate",
    "/api/escd/workflows/transition",
    "/api/escd/workflows/steps/transition",
}


def handles(method: str, path: str) -> bool:
    return path in (WORKFLOW_GET_PATHS if method == "GET" else WORKFLOW_POST_PATHS if method == "POST" else set())


def _template_storage(normalized: dict[str, Any], payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "template_id": normalized["template_id"],
        "version": normalized["version"],
        "name": normalized["name"],
        "status": normalized["status"],
        "template_type": normalized["template_type"],
        "purpose": normalized["purpose"],
        "scope": normalized["scope"],
        "supported_context_types": normalized["supported_context_types"],
        "definition": normalized,
        "parent_template_id": payload.get("parent_template_id"),
        "parent_template_version": payload.get("parent_template_version"),
        "effective_controls": normalized["effective_controls"],
        "definition_fingerprint": normalized["definition_fingerprint"],
        "provenance": normalized["provenance"],
    }


def _definition(row: dict[str, Any]) -> dict[str, Any]:
    definition = dict(row.get("definition") or {})
    definition.setdefault("template_id", row.get("template_id"))
    definition.setdefault("version", row.get("version"))
    definition.setdefault("name", row.get("name"))
    definition.setdefault("status", row.get("status"))
    definition.setdefault("template_type", row.get("template_type"))
    definition.setdefault("effective_controls", row.get("effective_controls") or {})
    definition.setdefault("definition_fingerprint", row.get("definition_fingerprint"))
    return definition


def dispatch_get(repo: SupabaseRLSClient, raw_path: str) -> tuple[int, dict[str, Any]]:
    parsed = urlparse(raw_path)
    path = parsed.path
    query = parse_qs(parsed.query)

    if path == "/api/escd/workflow-templates":
        return 200, {"ok": True, "templates": list_templates(repo)}

    if path == "/api/escd/workflows":
        return 200, {"ok": True, "workflows": list_instances(repo)}

    if path == "/api/escd/workflows/detail":
        instance_id = str((query.get("instance_id") or [""])[0]).strip()
        if not instance_id:
            return 400, {"error": "workflow_instance_id_required"}
        instance = get_instance(repo, instance_id)
        if not instance:
            return 404, {"error": "workflow_not_found"}
        template_row = get_template(repo, str(instance.get("template_id") or ""), str(instance.get("template_version") or ""))
        if not template_row:
            return 409, {"error": "workflow_template_binding_missing"}
        view = workflow_view(instance, _definition(template_row), list_steps(repo, instance_id), list_events(repo, instance_id))
        return 200, {"ok": True, "workflow": view}

    return 404, {"error": "not_found"}


def dispatch_post(repo: SupabaseRLSClient, path: str, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
    if path == "/api/escd/workflow-templates":
        status = str(payload.get("status") or "candidate").lower()
        if status not in {"draft", "candidate"}:
            return 409, {"error": "runtime_template_promotion_prohibited"}

        parent = None
        parent_id = str(payload.get("parent_template_id") or "").strip()
        parent_version = str(payload.get("parent_template_version") or "").strip()
        if parent_id or parent_version:
            if not parent_id or not parent_version:
                return 400, {"error": "workflow_parent_identity_incomplete"}
            parent_row = get_template(repo, parent_id, parent_version)
            if not parent_row:
                return 404, {"error": "workflow_parent_not_found"}
            parent = _definition(parent_row)

        candidate = dict(payload)
        candidate["status"] = status
        normalized = normalize_template(candidate, parent)
        row = create_template(repo, _template_storage(normalized, payload))
        return 201, {"ok": True, "template": row, "promotion_performed": False}

    if path == "/api/escd/workflows/instantiate":
        template_id = str(payload.get("template_id") or "").strip()
        template_version = str(payload.get("template_version") or "").strip()
        if not template_id or not template_version:
            return 400, {"error": "workflow_template_identity_required"}
        template_row = get_template(repo, template_id, template_version)
        if not template_row:
            return 404, {"error": "workflow_template_not_found"}
        template = _definition(template_row)

        binding = {
            "instance_key": payload.get("instance_key"),
            "context_type": payload.get("context_type"),
            "context_ref": payload.get("context_ref"),
            "bindings": payload.get("bindings") or {},
            "source_refs": payload.get("source_refs") or [],
            "evidence_refs": payload.get("evidence_refs") or [],
            "job_id": payload.get("job_id"),
        }
        candidate = instantiate_workflow(template, binding)
        existing = None
        if candidate.get("instance_key"):
            for row in list_instances(repo):
                if row.get("instance_key") == candidate["instance_key"]:
                    existing = row
                    break
        if existing:
            instance = existing
        else:
            instance = create_instance(repo, candidate)
            create_steps(repo, instantiate_steps(template, str(instance["id"])))
        detail = workflow_view(instance, template, list_steps(repo, str(instance["id"])), list_events(repo, str(instance["id"])))
        return 201 if not existing else 200, {"ok": True, "deduped": bool(existing), "workflow": detail}

    if path == "/api/escd/workflows/transition":
        instance_id = str(payload.get("instance_id") or "").strip()
        target = str(payload.get("status") or "").strip()
        if not instance_id or not target:
            return 400, {"error": "workflow_instance_and_status_required"}
        instance = get_instance(repo, instance_id)
        if not instance:
            return 404, {"error": "workflow_not_found"}
        allowed, reason = transition_instance(str(instance.get("status") or ""), target)
        if not allowed:
            return 409, {"error": reason}
        if target == "running" and (not instance.get("execution_authorized") or not instance.get("job_id")):
            return 409, {"error": "workflow_execution_not_authorized"}
        update: dict[str, Any] = {"status": target}
        if "current_step_id" in payload:
            update["current_step_id"] = payload.get("current_step_id")
        if "evidence_refs" in payload:
            update["evidence_refs"] = payload.get("evidence_refs") or []
        updated = patch_instance(repo, instance_id, update)
        return 200, {"ok": True, "workflow": updated}

    if path == "/api/escd/workflows/steps/transition":
        instance_id = str(payload.get("instance_id") or "").strip()
        step_id = str(payload.get("step_id") or "").strip()
        target = str(payload.get("status") or "").strip()
        if not instance_id or not step_id or not target:
            return 400, {"error": "workflow_step_identity_and_status_required"}
        instance = get_instance(repo, instance_id)
        if not instance:
            return 404, {"error": "workflow_not_found"}
        step = get_step(repo, instance_id, step_id)
        if not step:
            return 404, {"error": "workflow_step_not_found"}
        allowed, reason = transition_step(str(step.get("status") or ""), target)
        if not allowed:
            return 409, {"error": reason}
        if target == "running" and not instance.get("execution_authorized"):
            return 409, {"error": "workflow_execution_not_authorized"}
        if target == "running" and step.get("autonomy_class") == "A4_PROHIBITED":
            return 409, {"error": "workflow_step_prohibited"}

        update: dict[str, Any] = {"status": target}
        if "approval_id" in payload:
            update["approval_id"] = payload.get("approval_id")
        if "evidence_refs" in payload:
            update["evidence_refs"] = payload.get("evidence_refs") or []
        if target == "running":
            update["attempt_count"] = int(step.get("attempt_count") or 0) + 1
        updated = patch_step(repo, instance_id, step_id, update)
        return 200, {"ok": True, "step": updated}

    raise RepositoryError("workflow_route_not_found")
