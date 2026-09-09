from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Iterable

from ..policy.models import Item
from ..policy.engine import rank_items
from ..policy.extensions import transition_allowed, completion_valid, build_briefing_snapshot


class RuntimeRuleError(ValueError):
    pass


def require_job_transition(
    job: dict[str, Any],
    target: str,
    evidence_refs: Iterable[str] = (),
    exit_criteria_met: bool = False,
    approved: bool = False,
) -> dict[str, Any]:
    current = str(job.get("status") or "")
    allowed, reason = transition_allowed("job", current, target)
    if not allowed:
        raise RuntimeRuleError(reason)

    if current == "waiting_approval" and target == "running" and job.get("requires_approval") and not approved:
        raise RuntimeRuleError("approved_decision_required")

    if target == "completed":
        if job.get("requires_approval") and not approved:
            raise RuntimeRuleError("approved_decision_required")
        valid, completion_reason = completion_valid(exit_criteria_met, evidence_refs)
        if not valid:
            raise RuntimeRuleError(completion_reason)

    update = {"status": target, "updated_at": datetime.now(timezone.utc).isoformat()}
    if target == "completed":
        update["completed_at"] = update["updated_at"]
        update["exit_criteria_met"] = True
    return update


def require_approval_decision(
    approval: dict[str, Any],
    decision: str,
    authenticated_user_id: str,
) -> dict[str, Any]:
    if approval.get("status") != "pending":
        raise RuntimeRuleError("approval_not_pending")
    if decision not in {"approved", "rejected"}:
        raise RuntimeRuleError("invalid_approval_decision")
    if not authenticated_user_id:
        raise RuntimeRuleError("authenticated_actor_required")
    return {
        "status": decision,
        "decided_by_user_id": authenticated_user_id,
        "decided_at": datetime.now(timezone.utc).isoformat(),
    }


def _deadline_ts(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return None


def job_to_item(job: dict[str, Any]) -> Item:
    return Item(
        item_id=str(job["id"]),
        title=str(job.get("title") or "Untitled"),
        actionable=bool(job.get("actionable", True)),
        blocked=bool(job.get("blocked", False)),
        external_dependency=bool(job.get("external_dependency", False)),
        future_trigger=bool(job.get("future_trigger", False)),
        missing_approval=bool(job.get("missing_approval", False)),
        explicit_hold=bool(job.get("explicit_hold", False)),
        mission_priority=float(job.get("mission_priority", 0) or 0),
        explicit_priority=float(job.get("explicit_priority", 0) or 0),
        urgency=float(job.get("urgency", 0) or 0),
        revenue_relevance=float(job.get("revenue_relevance", 0) or 0),
        unblock_value=float(job.get("unblock_value", 0) or 0),
        consequence=float(job.get("consequence", 0) or 0),
        aging=float(job.get("aging", 0) or 0),
        effort_efficiency=float(job.get("effort_efficiency", 0) or 0),
        strategic_leverage=float(job.get("strategic_leverage", 0) or 0),
        dcs_override=float(job.get("dcs_override", 0) or 0),
        deadline_ts=_deadline_ts(job.get("deadline")),
        source_refs=list(job.get("source_refs") or []),
    )


def next_best_action(jobs: Iterable[dict[str, Any]]) -> dict[str, Any] | None:
    jobs = list(jobs)
    by_id = {str(j["id"]): j for j in jobs}
    ranked = rank_items(job_to_item(job) for job in jobs)
    if not ranked:
        return None
    result = ranked[0]
    job = by_id[result["item_id"]]
    return {
        "job_id": result["item_id"],
        "title": job.get("title"),
        "score": result["score"],
        "contributions": result["contributions"],
        "top_factors": result.get("top_factors", []),
        "queue": result["queue"],
    }


def briefing_snapshot(
    *,
    changed: Iterable[dict[str, Any]],
    completed: Iterable[dict[str, Any]],
    approvals: Iterable[dict[str, Any]],
    due_or_at_risk: Iterable[dict[str, Any]],
    blockers: Iterable[dict[str, Any]],
    watches: Iterable[dict[str, Any]],
    jobs: Iterable[dict[str, Any]],
) -> dict[str, Any]:
    return build_briefing_snapshot({
        "changed": list(changed),
        "completed": list(completed),
        "approvals": list(approvals),
        "due_or_at_risk": list(due_or_at_risk),
        "blockers": list(blockers),
        "watches": list(watches),
        "next_best_action": next_best_action(jobs),
    })
