from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, List, Tuple

from apps.escd.policy.engine import AUTONOMY, TEMPLATE_TYPES, child_controls_valid, contains_secret


TEMPLATE_STATUSES = {"draft", "candidate", "approved", "superseded", "archived"}
CONTEXT_TYPES = {"product", "project", "asset", "system", "document", "person", "event", "general"}
INSTANCE_STATUSES = {"planned", "running", "waiting_approval", "waiting", "failed", "completed", "cancelled", "archived"}
STEP_STATUSES = {"pending", "ready", "running", "waiting_approval", "waiting", "completed", "failed", "skipped", "cancelled"}
CONTROL_FIELDS = ("approval_required", "evidence_required", "security_required", "rollback_required")
REQUIRED_TEMPLATE_FIELDS = {
    "template_id", "name", "version", "status", "template_type", "purpose", "scope",
    "supported_context_types", "input_contract", "required_sources", "preconditions", "steps",
    "decision_points", "approval_points", "executor_classes", "connector_requirements",
    "evidence_requirements", "test_requirements", "rollback_or_recovery", "exit_criteria",
    "follow_up_rules", "notification_policy", "lane_restrictions", "retry_policy", "owner", "provenance",
}
REQUIRED_STEP_FIELDS = {
    "step_id", "sequence_or_dependency", "action_type", "instruction", "input_refs",
    "output_contract", "executor", "autonomy_class", "approval_required", "verification_method",
    "evidence_required", "failure_route", "next_step_on_success", "next_step_on_failure",
}


def _stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def stable_fingerprint(value: Any) -> str:
    return hashlib.sha256(_stable_json(value).encode("utf-8")).hexdigest()


def _clean_refs(values: Iterable[Any]) -> List[str]:
    out: List[str] = []
    for value in values or []:
        text = str(value or "").strip()
        if text and text not in out:
            out.append(text)
    return out


def validate_template_payload(payload: Dict[str, Any], parent: Dict[str, Any] | None = None) -> List[str]:
    errors: List[str] = []
    missing = sorted(field for field in REQUIRED_TEMPLATE_FIELDS if field not in payload)
    if missing:
        errors.append("missing_fields:" + ",".join(missing))

    template_type = str(payload.get("template_type") or "").upper()
    status = str(payload.get("status") or "").lower()
    if template_type not in TEMPLATE_TYPES:
        errors.append("invalid_template_type")
    if status not in TEMPLATE_STATUSES:
        errors.append("invalid_template_status")
    if not str(payload.get("template_id") or "").strip() or not str(payload.get("version") or "").strip():
        errors.append("template_identity_required")

    contexts = [str(x).lower() for x in payload.get("supported_context_types", [])]
    if not contexts or any(x not in CONTEXT_TYPES for x in contexts):
        errors.append("invalid_supported_context_types")
    if not payload.get("steps"):
        errors.append("steps_required")
    if not payload.get("rollback_or_recovery"):
        errors.append("rollback_or_recovery_required")
    if not payload.get("exit_criteria"):
        errors.append("exit_criteria_required")
    if not _clean_refs(payload.get("provenance", [])):
        errors.append("provenance_required")
    if contains_secret(payload):
        errors.append("secret_prohibited")

    seen_step_ids: set[str] = set()
    for raw_step in payload.get("steps", []):
        if not isinstance(raw_step, dict):
            errors.append("step_contract_invalid")
            continue
        step_id = str(raw_step.get("step_id") or "").strip()
        if not REQUIRED_STEP_FIELDS.issubset(raw_step):
            errors.append(f"step_contract_incomplete:{step_id or 'unknown'}")
        if not step_id:
            errors.append("step_identity_required")
        elif step_id in seen_step_ids:
            errors.append(f"duplicate_step_id:{step_id}")
        else:
            seen_step_ids.add(step_id)
        autonomy = raw_step.get("autonomy_class")
        if autonomy not in AUTONOMY:
            errors.append(f"invalid_autonomy:{step_id or 'unknown'}")
        if autonomy == "A3_APPROVAL_REQUIRED" and not bool(raw_step.get("approval_required")):
            errors.append(f"approval_required_for_a3:{step_id or 'unknown'}")
        if autonomy == "A4_PROHIBITED" and raw_step.get("next_step_on_success"):
            errors.append(f"prohibited_step_cannot_advance:{step_id or 'unknown'}")
        if contains_secret(raw_step):
            errors.append(f"secret_prohibited:{step_id or 'unknown'}")

    controls = dict(payload.get("parent_controls") or {})
    if parent:
        valid, control_errors = child_controls_valid(
            dict(parent.get("effective_controls") or parent.get("parent_controls") or {}),
            controls,
        )
        if not valid:
            errors.extend(control_errors)

    return sorted(set(errors))


def effective_controls(parent_controls: Dict[str, Any] | None, child_controls: Dict[str, Any] | None) -> Dict[str, bool]:
    parent = dict(parent_controls or {})
    child = dict(child_controls or {})
    valid, errors = child_controls_valid(parent, child)
    if not valid:
        raise ValueError(";".join(errors))
    effective: Dict[str, bool] = {}
    for field in CONTROL_FIELDS:
        effective[field] = bool(parent.get(field, False) or child.get(field, False))
    return effective


def normalize_template(payload: Dict[str, Any], parent: Dict[str, Any] | None = None) -> Dict[str, Any]:
    errors = validate_template_payload(payload, parent)
    if errors:
        raise ValueError("workflow_template_invalid:" + "|".join(errors))

    normalized = dict(payload)
    normalized["template_id"] = str(payload["template_id"]).strip()
    normalized["name"] = str(payload["name"]).strip()
    normalized["version"] = str(payload["version"]).strip()
    normalized["status"] = str(payload["status"]).lower()
    normalized["template_type"] = str(payload["template_type"]).upper()
    normalized["supported_context_types"] = [str(x).lower() for x in payload["supported_context_types"]]
    normalized["required_sources"] = _clean_refs(payload.get("required_sources", []))
    normalized["connector_requirements"] = _clean_refs(payload.get("connector_requirements", []))
    normalized["provenance"] = _clean_refs(payload.get("provenance", []))

    parent_controls = dict(parent.get("effective_controls") or parent.get("parent_controls") or {}) if parent else {}
    normalized["effective_controls"] = effective_controls(parent_controls, payload.get("parent_controls", {}))
    normalized["definition_fingerprint"] = stable_fingerprint({
        k: v for k, v in normalized.items() if k != "definition_fingerprint"
    })
    return normalized


def instantiate_workflow(template: Dict[str, Any], binding: Dict[str, Any]) -> Dict[str, Any]:
    context_type = str(binding.get("context_type") or "").lower()
    context_ref = str(binding.get("context_ref") or "").strip()
    source_refs = _clean_refs(binding.get("source_refs", []))
    job_id = str(binding.get("job_id") or "").strip() or None
    if context_type not in CONTEXT_TYPES:
        raise ValueError("invalid_context_type")
    if context_type not in [str(x).lower() for x in template.get("supported_context_types", [])]:
        raise ValueError("unsupported_context_type")
    if not context_ref:
        raise ValueError("context_ref_required")
    if not source_refs:
        raise ValueError("workflow_source_required")

    required_inputs = template.get("input_contract") or {}
    bindings = dict(binding.get("bindings") or {})
    required_keys = required_inputs.get("required", []) if isinstance(required_inputs, dict) else []
    missing = [str(key) for key in required_keys if key not in bindings]
    if missing:
        raise ValueError("workflow_binding_missing:" + ",".join(sorted(missing)))

    instance_key = str(binding.get("instance_key") or "").strip()
    if not instance_key:
        instance_key = "escd-wf-" + stable_fingerprint({
            "template_id": template.get("template_id"),
            "template_version": template.get("version"),
            "context_type": context_type,
            "context_ref": context_ref,
            "bindings": bindings,
            "source_refs": source_refs,
            "job_id": job_id,
        })

    executable = template.get("status") == "approved" and bool(job_id)
    return {
        "instance_key": instance_key,
        "template_id": template["template_id"],
        "template_version": template["version"],
        "template_fingerprint": template["definition_fingerprint"],
        "template_type": template["template_type"],
        "job_id": job_id,
        "context_type": context_type,
        "context_ref": context_ref,
        "bindings": bindings,
        "status": "planned",
        "current_step_id": None,
        "source_refs": source_refs,
        "evidence_refs": _clean_refs(binding.get("evidence_refs", [])),
        "effective_controls": dict(template.get("effective_controls") or {}),
        "execution_authorized": bool(executable),
    }


def instantiate_steps(template: Dict[str, Any], instance_id: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for ordinal, step in enumerate(template.get("steps", []), start=1):
        dependency = step.get("sequence_or_dependency")
        dependencies: List[str]
        if isinstance(dependency, list):
            dependencies = _clean_refs(dependency)
        elif dependency in (None, "", ordinal - 1, ordinal):
            dependencies = [] if ordinal == 1 else [str(template["steps"][ordinal - 2]["step_id"])]
        else:
            dependencies = [str(dependency)]
        out.append({
            "instance_id": instance_id,
            "step_id": str(step["step_id"]),
            "sequence_no": ordinal,
            "dependencies": dependencies,
            "action_type": str(step["action_type"]),
            "instruction": str(step["instruction"]),
            "input_refs": list(step.get("input_refs") or []),
            "output_contract": dict(step.get("output_contract") or {}),
            "executor": str(step.get("executor") or ""),
            "autonomy_class": str(step["autonomy_class"]),
            "approval_required": bool(step.get("approval_required")),
            "verification_method": str(step.get("verification_method") or ""),
            "evidence_required": bool(step.get("evidence_required")),
            "failure_route": str(step.get("failure_route") or ""),
            "next_step_on_success": step.get("next_step_on_success"),
            "next_step_on_failure": step.get("next_step_on_failure"),
            "status": "pending",
            "attempt_count": 0,
        })
    return out


def step_readiness(steps: Iterable[Dict[str, Any]], approvals: Iterable[Dict[str, Any]] = ()) -> List[Dict[str, Any]]:
    rows = [dict(x) for x in steps]
    by_id = {str(x.get("step_id")): x for x in rows}
    approved_keys = {str(a.get("action_key")) for a in approvals if a.get("status") == "approved"}
    terminal = {"completed", "failed", "skipped", "cancelled"}

    for row in rows:
        status = str(row.get("status") or "pending")
        if status in terminal or status == "running":
            continue
        deps = [str(x) for x in row.get("dependencies", [])]
        if any(str(by_id.get(dep, {}).get("status")) != "completed" for dep in deps):
            row["status"] = "pending"
            row["blocked_reason"] = "dependency_incomplete"
            continue
        if row.get("autonomy_class") == "A4_PROHIBITED":
            row["status"] = "waiting"
            row["blocked_reason"] = "prohibited_action"
            continue
        if row.get("approval_required") and f"workflow_step:{row.get('step_id')}" not in approved_keys:
            row["status"] = "waiting_approval"
            row["blocked_reason"] = "approval_required"
            continue
        row["status"] = "ready"
        row["blocked_reason"] = None
    return rows


def next_step(steps: Iterable[Dict[str, Any]]) -> Dict[str, Any] | None:
    ready = [dict(x) for x in steps if x.get("status") == "ready"]
    ready.sort(key=lambda x: (int(x.get("sequence_no") or 0), str(x.get("step_id") or "")))
    return ready[0] if ready else None


def transition_instance(current: str, target: str) -> Tuple[bool, str]:
    graph = {
        "planned": {"running", "waiting_approval", "waiting", "cancelled"},
        "running": {"waiting_approval", "waiting", "failed", "completed", "cancelled"},
        "waiting_approval": {"running", "waiting", "cancelled"},
        "waiting": {"running", "waiting_approval", "failed", "cancelled"},
        "failed": {"running", "archived"},
        "completed": {"archived"},
        "cancelled": {"archived"},
        "archived": set(),
    }
    if current not in graph:
        return False, "unknown_workflow_state"
    return (True, "allowed") if target in graph[current] else (False, "invalid_workflow_transition")


def transition_step(current: str, target: str) -> Tuple[bool, str]:
    graph = {
        "pending": {"ready", "waiting_approval", "waiting", "cancelled"},
        "ready": {"running", "waiting_approval", "cancelled"},
        "running": {"waiting_approval", "waiting", "completed", "failed", "cancelled"},
        "waiting_approval": {"ready", "running", "waiting", "cancelled"},
        "waiting": {"ready", "running", "failed", "cancelled"},
        "failed": {"ready", "cancelled"},
        "completed": set(),
        "skipped": set(),
        "cancelled": set(),
    }
    if current not in graph:
        return False, "unknown_workflow_step_state"
    return (True, "allowed") if target in graph[current] else (False, "invalid_workflow_step_transition")


def workflow_view(instance: Dict[str, Any], template: Dict[str, Any], steps: Iterable[Dict[str, Any]], events: Iterable[Dict[str, Any]] = ()) -> Dict[str, Any]:
    ordered_steps = sorted([dict(x) for x in steps], key=lambda x: (int(x.get("sequence_no") or 0), str(x.get("step_id") or "")))
    return {
        "instance": dict(instance),
        "template": {
            "template_id": template.get("template_id"),
            "name": template.get("name"),
            "version": template.get("version"),
            "status": template.get("status"),
            "template_type": template.get("template_type"),
            "definition_fingerprint": template.get("definition_fingerprint"),
            "effective_controls": template.get("effective_controls", {}),
        },
        "steps": ordered_steps,
        "next_step": next_step(ordered_steps),
        "events": sorted([dict(x) for x in events], key=lambda x: (str(x.get("created_at") or ""), str(x.get("id") or "")), reverse=True),
        "operator_can_inspect": True,
        "external_execution_performed": False,
    }
