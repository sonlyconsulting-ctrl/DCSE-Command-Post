from typing import Iterable, Dict, Any, Tuple

STATE_TRANSITIONS = {
    "item": {
        "captured": {"triaged", "cancelled"},
        "triaged": {"planned", "active", "waiting", "watch", "approval", "cancelled"},
        "planned": {"active", "waiting", "watch", "approval", "cancelled"},
        "active": {"waiting", "watch", "approval", "completed", "cancelled"},
        "waiting": {"active", "watch", "approval", "cancelled"},
        "watch": {"active", "waiting", "approval", "cancelled"},
        "approval": {"active", "waiting", "cancelled"},
        "completed": {"archived"}, "cancelled": {"archived"}, "archived": set(),
    },
    "job": {
        "queued": {"running", "cancelled"},
        "running": {"waiting_approval", "completed", "failed", "cancelled"},
        "waiting_approval": {"running", "cancelled", "failed"},
        "completed": {"archived"}, "failed": {"queued", "archived"},
        "cancelled": {"archived"}, "archived": set(),
    },
    "approval": {
        "proposed": {"pending", "withdrawn"},
        "pending": {"approved", "rejected", "expired", "withdrawn"},
        "approved": set(), "rejected": set(), "expired": set(), "withdrawn": set(),
    },
}

SOURCE_PRECEDENCE = {
    "operative_authority": 1,
    "verified_live_operational": 2,
    "versioned_evidence": 3,
    "linked_external_source": 4,
    "escd_derived": 5,
    "model_inference": 6,
}

def transition_allowed(domain: str, current: str, target: str) -> Tuple[bool, str]:
    graph = STATE_TRANSITIONS.get(domain)
    if graph is None:
        return False, "unknown_domain"
    if current not in graph:
        return False, "unknown_current_state"
    return (True, "allowed") if target in graph[current] else (False, "invalid_transition")

def choose_source(sources: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = list(sources)
    if not items:
        return {"selected": None, "conflicts": [], "status": "unknown"}
    ordered = sorted(items, key=lambda s: (SOURCE_PRECEDENCE.get(s.get("source_class"), 999), str(s.get("source_ref", ""))))
    selected = ordered[0]
    conflicts = [s for s in ordered[1:] if s.get("value") != selected.get("value")]
    return {"selected": selected, "conflicts": conflicts, "status": "conflict" if conflicts else "verified"}

def completion_valid(exit_criteria_met: bool, evidence_refs: Iterable[str], attempted_only: bool = False) -> Tuple[bool, str]:
    refs = [r for r in evidence_refs if r]
    if attempted_only:
        return False, "attempt_not_completion"
    if not exit_criteria_met:
        return False, "exit_criteria_not_met"
    if not refs:
        return False, "evidence_required"
    return True, "verified_completion"

def build_briefing_snapshot(state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "changed": list(state.get("changed") or []),
        "completed": list(state.get("completed") or []),
        "approvals": list(state.get("approvals") or []),
        "due_or_at_risk": list(state.get("due_or_at_risk") or []),
        "blockers": list(state.get("blockers") or []),
        "next_best_action": state.get("next_best_action"),
        "watches": list(state.get("watches") or []),
        "source": "persisted_reconciled_state",
    }

def notification_escalation(notification_class: str, acknowledged: bool, shrinking_window: bool = False,
                            material_risk: bool = False) -> Tuple[str, str]:
    if acknowledged:
        return notification_class, "acknowledged"
    if notification_class == "N0":
        return "N0", "no_escalation"
    if notification_class == "N1":
        return "N1", "briefing_only"
    if notification_class == "N2" and shrinking_window:
        return "N3", "action_window_shrinking"
    if notification_class == "N3" and material_risk:
        return "N3", "bounded_renotify"
    if notification_class == "N4":
        return "N4", "persistent_hard_stop"
    return notification_class, "no_material_change"

def mobile_action_result(server_acknowledged: bool, evidence_ref: str | None = None) -> Dict[str, Any]:
    if not server_acknowledged:
        return {"state": "pending", "completed": False, "evidence_ref": None}
    if not evidence_ref:
        return {"state": "acknowledged_unverified", "completed": False, "evidence_ref": None}
    return {"state": "verified", "completed": True, "evidence_ref": evidence_ref}

def connector_execution_class(system: str, operation: str) -> str:
    system = system.lower()
    operation = operation.lower()
    if operation == "read":
        return "A0_AUTO"
    if system in {"gmail", "google_calendar"} and operation in {"send", "write", "modify", "delete"}:
        return "A3_APPROVAL_REQUIRED"
    if system == "escd_state" and operation in {"create", "update"}:
        return "A1_AUTO_LOG"
    if operation in {"publish", "deploy", "delete", "credential_change", "permission_change"}:
        return "A3_APPROVAL_REQUIRED"
    return "A2_PROPOSE"
