from __future__ import annotations
from dataclasses import asdict
from datetime import timedelta
import re
from typing import Iterable, Dict, Any, List, Tuple
from .models import Action, Item, RetryContext, NotificationState, CalendarEvent, WorkflowTemplate

AUTONOMY = ("A0_AUTO", "A1_AUTO_LOG", "A2_PROPOSE", "A3_APPROVAL_REQUIRED", "A4_PROHIBITED")
QUEUES = ("NOW", "APPROVAL", "WAITING", "WATCH", "BACKLOG")
TEMPLATE_TYPES = {"MAKE","FIX","REVIEW","RELEASE","MONITOR","ROUTINE","RESEARCH","COMMUNICATE","DECIDE","DO"}
WEIGHTS = {
    "mission_priority": .15,
    "explicit_priority": .15,
    "urgency": .20,
    "revenue_relevance": .10,
    "unblock_value": .10,
    "consequence": .10,
    "aging": .05,
    "effort_efficiency": .05,
    "strategic_leverage": .05,
    "dcs_override": .05,
}
REQUIRED_TEMPLATE_FIELDS = {
    "template_id","name","version","status","template_type","purpose","scope",
    "supported_context_types","input_contract","required_sources","preconditions","steps",
    "decision_points","approval_points","executor_classes","connector_requirements",
    "evidence_requirements","test_requirements","rollback_or_recovery","exit_criteria",
    "follow_up_rules","notification_policy","lane_restrictions","retry_policy","owner","provenance"
}
SECRET_PATTERNS = [
    re.compile(r"(?i)service[_-]?role[_-]?key"), re.compile(r"(?i)api[_-]?key\s*[:=]"),
    re.compile(r"(?i)password\s*[:=]"), re.compile(r"(?i)private[_-]?key"),
    re.compile(r"(?i)connection[_-]?string"), re.compile(r"(?i)recovery[_-]?code"),
]

def clamp100(value: float) -> float:
    return max(0.0, min(100.0, float(value)))

def classify_autonomy(action: Action) -> str:
    if action.exposes_secret or action.bypasses_control or action.fabricates_evidence or action.protected_lane_conflict:
        return "A4_PROHIBITED"
    if any((action.external, action.public, action.financial, action.production, action.destructive,
            action.auth_change, action.authority_change, action.legal_privacy_security, action.irreversible)):
        return "A3_APPROVAL_REQUIRED"
    if action.proposal_only or action.kind.upper().startswith("PROPOSE_"):
        return "A2_PROPOSE"
    if action.internal_state_change:
        return "A1_AUTO_LOG"
    return "A0_AUTO"

def route_queue(item: Item) -> str:
    if item.missing_approval:
        return "APPROVAL"
    if item.explicit_hold or item.external_dependency or item.blocked:
        return "WAITING"
    if item.future_trigger:
        return "WATCH"
    return "NOW" if item.actionable else "BACKLOG"

def score_item(item: Item) -> Dict[str, Any]:
    queue = route_queue(item)
    if queue != "NOW":
        return {"item_id": item.item_id, "queue": queue, "score": None, "contributions": {}, "actionable": False}
    factors = {name: clamp100(getattr(item, name)) for name in WEIGHTS}
    contributions = {k: round(factors[k] * WEIGHTS[k], 4) for k in WEIGHTS}
    score = round(sum(contributions.values()), 4)
    top = sorted(contributions.items(), key=lambda kv: (-kv[1], kv[0]))[:3]
    return {"item_id": item.item_id, "queue": "NOW", "score": score,
            "contributions": contributions, "top_factors": top, "actionable": True}

def rank_items(items: Iterable[Item]) -> List[Dict[str, Any]]:
    ranked = []
    for item in items:
        result = score_item(item)
        if result["queue"] == "NOW":
            ranked.append((item, result))
    ranked.sort(key=lambda x: (
        -x[1]["score"],
        -clamp100(x[0].dcs_override),
        x[0].deadline_ts if x[0].deadline_ts is not None else float("inf"),
        -clamp100(x[0].revenue_relevance),
        -clamp100(x[0].unblock_value),
        x[0].item_id,
    ))
    return [r for _, r in ranked]

def retry_allowed(ctx: RetryContext) -> Tuple[bool, str]:
    if ctx.attempt >= ctx.max_attempts:
        return False, "retry_limit"
    if any((ctx.permission_failure, ctx.security_failure, ctx.payload_changed, ctx.unexpected_cost, ctx.authority_conflict)):
        return False, "hard_stop"
    if ctx.uncertain_external_side_effect:
        return False, "reconcile_external_effect"
    if ctx.destructive and not ctx.idempotent:
        return False, "non_idempotent_destructive"
    return True, "within_authorization_envelope"

def should_notify(state: NotificationState) -> Tuple[bool, str]:
    changed = state.current_value != state.prior_value
    if state.threshold_crossed:
        return True, "threshold_crossed"
    if state.worsened:
        return True, "worsened"
    if state.deadline_approaching:
        return True, "deadline_approaching"
    if changed and not state.acknowledged:
        return True, "meaningful_change"
    return False, "unchanged_or_acknowledged"

def detect_calendar_conflicts(events: Iterable[CalendarEvent], buffer_minutes: int = 0) -> List[Dict[str, Any]]:
    ordered = sorted(events, key=lambda e: (e.start, e.end, e.event_id))
    out = []
    for i, a in enumerate(ordered):
        for b in ordered[i+1:]:
            if b.start < a.end and a.start < b.end:
                out.append({"class":"C1", "events":[a.event_id,b.event_id], "source_refs":[a.source_ref,b.source_ref]})
            elif buffer_minutes and b.start < a.end + timedelta(minutes=buffer_minutes):
                out.append({"class":"C2", "events":[a.event_id,b.event_id], "source_refs":[a.source_ref,b.source_ref]})
            elif b.start >= a.end + timedelta(minutes=buffer_minutes):
                break
    return out

def dedupe_commitments(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[str, Dict[str, Any]] = {}
    for r in records:
        key = (r.get("commitment_id") or r.get("normalized_intent") or "").strip().lower()
        if not key:
            key = f"source:{r.get('source_ref','')}:{r.get('title','').strip().lower()}"
        if key not in grouped:
            grouped[key] = {**r, "source_refs": []}
        ref = r.get("source_ref")
        if ref and ref not in grouped[key]["source_refs"]:
            grouped[key]["source_refs"].append(ref)
    return list(grouped.values())

def communication_triage(message: Dict[str, Any]) -> str:
    if message.get("explicit_decision_required"):
        return "DECISION"
    if message.get("meeting_request"):
        return "SCHEDULE"
    if message.get("reply_required"):
        return "REPLY"
    if message.get("waiting_on_other"):
        return "WAITING"
    if message.get("deadline") or message.get("action_required"):
        return "ACTION"
    if message.get("monitor"):
        return "WATCH"
    return "REFERENCE"

def parse_command(text: str) -> Dict[str, Any]:
    t = text.strip()
    low = t.lower()
    op = "DO"
    for key, prefix in (("MAKE","make "),("FIX","fix "),("REVIEW","review "),("RELEASE","release "),
                        ("MONITOR","monitor "),("RESEARCH","research "),("COMMUNICATE","send "),
                        ("DECIDE","decide "),("ROUTINE","remind ")):
        if low.startswith(prefix):
            op = key
            break
    return {"operation": op, "raw": t, "requires_authority_check": True, "parsed": bool(t)}

def contains_secret(value: Any) -> bool:
    secret_keys = {"password","token","api_key","apikey","service_role_key","private_key","connection_string","recovery_code","mfa"}
    def walk(v: Any) -> bool:
        if isinstance(v, dict):
            for k, val in v.items():
                nk = str(k).strip().lower().replace("-","_")
                if nk in secret_keys or any(sk in nk for sk in ("password","private_key","service_role","connection_string","recovery_code")):
                    return True
                if walk(val):
                    return True
            return False
        if isinstance(v, (list, tuple, set)):
            return any(walk(x) for x in v)
        text = str(v)
        return any(p.search(text) for p in SECRET_PATTERNS)
    return walk(value)

def validate_workflow_template(template: WorkflowTemplate) -> List[str]:
    errors = []
    data = asdict(template)
    missing = [f for f in REQUIRED_TEMPLATE_FIELDS if f not in data]
    if missing:
        errors.append("missing_fields:" + ",".join(sorted(missing)))
    if template.template_type not in TEMPLATE_TYPES:
        errors.append("invalid_template_type")
    if template.status not in {"draft","candidate","approved","superseded","archived"}:
        errors.append("invalid_status")
    if not template.version or not template.template_id:
        errors.append("identity_required")
    if not template.steps:
        errors.append("steps_required")
    if not template.rollback_or_recovery:
        errors.append("rollback_or_recovery_required")
    if not template.exit_criteria:
        errors.append("exit_criteria_required")
    if contains_secret(data):
        errors.append("secret_prohibited")
    for step in template.steps:
        needed = {"step_id","action_type","instruction","autonomy_class","verification_method","failure_route"}
        if not needed.issubset(step):
            errors.append(f"step_contract_incomplete:{step.get('step_id','unknown')}")
        if step.get("autonomy_class") not in AUTONOMY:
            errors.append(f"invalid_autonomy:{step.get('step_id','unknown')}")
    return errors

def child_controls_valid(parent: Dict[str, Any], child: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    for field in ("approval_required", "evidence_required", "security_required", "rollback_required"):
        if parent.get(field) is True and child.get(field) is False:
            errors.append(f"weakened:{field}")
    return (not errors), errors

def ddna_candidate_valid(candidate: Dict[str, Any]) -> Tuple[bool, List[str]]:
    required = {"candidate_id","source_refs","provenance","candidate_type","content","status"}
    errors = []
    if not required.issubset(candidate):
        errors.append("missing_required_fields")
    if candidate.get("status") not in {"candidate","rejected","validated"}:
        errors.append("invalid_status")
    if candidate.get("status") == "operative":
        errors.append("self_promotion_prohibited")
    if not candidate.get("source_refs"):
        errors.append("source_required")
    if contains_secret(candidate):
        errors.append("secret_prohibited")
    return (not errors), errors

def decision_record_valid(record: Dict[str, Any]) -> Tuple[bool, List[str]]:
    required = {"decision_id","facts","unknowns","alternatives","tradeoffs","recommendation","decision","evidence_refs"}
    errors = []
    if not required.issubset(record):
        errors.append("missing_required_fields")
    if record.get("decision") == "executed" and not record.get("execution_evidence_ref"):
        errors.append("execution_evidence_required")
    return (not errors), errors

def contact_context_valid(context: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    if not context.get("source_refs"):
        errors.append("source_required")
    if context.get("inferred_sensitive_trait"):
        errors.append("sensitive_inference_prohibited")
    return (not errors), errors

def routine_run_decision(routine: Dict[str, Any], prior_run_key: str | None) -> Tuple[str, str]:
    if routine.get("paused"):
        return "SKIP", "paused"
    if routine.get("cancelled"):
        return "SKIP", "cancelled"
    run_key = routine.get("run_key")
    if run_key and run_key == prior_run_key:
        return "SKIP", "idempotent_duplicate"
    if routine.get("missed") and routine.get("missed_run_policy") == "skip":
        return "SKIP", "missed_policy_skip"
    return "RUN", "eligible"

def make_fix_release_gate(kind: str, context: Dict[str, Any]) -> Tuple[bool, List[str]]:
    kind = kind.upper()
    errors = []
    if kind == "MAKE":
        for f in ("requirements","baseline","test_requirements","exit_criteria"):
            if not context.get(f):
                errors.append(f"missing:{f}")
    elif kind == "FIX":
        for f in ("target","problem_statement","reproduction_evidence","known_good_baseline","regression_surface","rollback_point"):
            if not context.get(f):
                errors.append(f"missing:{f}")
    elif kind == "RELEASE":
        for f in ("validated_build","test_evidence","rollback","approval_state"):
            if not context.get(f):
                errors.append(f"missing:{f}")
        if context.get("approval_state") != "approved":
            errors.append("approval_required")
    else:
        errors.append("unsupported_kind")
    return (not errors), errors
