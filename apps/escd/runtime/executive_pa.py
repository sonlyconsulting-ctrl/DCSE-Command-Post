from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from typing import Any, Iterable

from ..policy.engine import (
    communication_triage,
    contact_context_valid,
    detect_calendar_conflicts,
    parse_command,
    retry_allowed,
    routine_run_decision,
    should_notify,
    decision_record_valid,
)
from ..policy.models import CalendarEvent, Item, NotificationState, RetryContext
from ..policy.engine import rank_items, route_queue


TERMINAL_ITEM_STATUSES = {"completed", "cancelled", "archived"}
TASK_CLASSES = {
    "CAPTURE", "TRIAGE", "PLAN", "MAKE", "FIX", "DO", "DECIDE", "APPROVE",
    "COMMUNICATE", "RESEARCH", "DCSE", "ROUTINE", "MONITOR", "REVIEW",
    "RELEASE", "ARCHIVE",
}
MOBILE_ACTIONS = {"capture", "defer", "approve", "reject", "done", "snooze", "open_source"}


def _deadline_ts(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc).timestamp()


def item_to_policy_item(record: dict[str, Any]) -> Item:
    return Item(
        item_id=str(record["id"]),
        title=str(record.get("title") or "Untitled"),
        actionable=bool(record.get("actionable", True)),
        blocked=bool(record.get("blocked", False)),
        external_dependency=bool(record.get("external_dependency", False)),
        future_trigger=bool(record.get("future_trigger", False)),
        missing_approval=bool(record.get("missing_approval", False)),
        explicit_hold=bool(record.get("explicit_hold", False)),
        mission_priority=float(record.get("mission_priority", 0) or 0),
        explicit_priority=float(record.get("explicit_priority", 0) or 0),
        urgency=float(record.get("urgency", 0) or 0),
        revenue_relevance=float(record.get("revenue_relevance", 0) or 0),
        unblock_value=float(record.get("unblock_value", 0) or 0),
        consequence=float(record.get("consequence", 0) or 0),
        aging=float(record.get("aging", 0) or 0),
        effort_efficiency=float(record.get("effort_efficiency", 0) or 0),
        strategic_leverage=float(record.get("strategic_leverage", 0) or 0),
        dcs_override=float(record.get("dcs_override", 0) or 0),
        deadline_ts=_deadline_ts(record.get("due_at")),
        source_refs=list(record.get("source_refs") or []),
    )


def _effective_queue(record: dict[str, Any]) -> str | None:
    status = str(record.get("status") or "")
    if status in TERMINAL_ITEM_STATUSES:
        return None
    if status == "approval":
        return "APPROVAL"
    if status == "waiting":
        return "WAITING"
    if status == "watch":
        return "WATCH"
    if status in {"captured", "triaged"}:
        return "BACKLOG"
    return route_queue(item_to_policy_item(record))


def _non_now_sort_key(record: dict[str, Any]) -> tuple[Any, ...]:
    deadline = _deadline_ts(record.get("due_at"))
    return (
        -float(record.get("dcs_override", 0) or 0),
        deadline if deadline is not None else float("inf"),
        -float(record.get("explicit_priority", 0) or 0),
        -float(record.get("urgency", 0) or 0),
        str(record.get("id") or ""),
    )


def executive_stream(items: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [dict(x) for x in items]
    queues: dict[str, list[dict[str, Any]]] = {
        "NOW": [], "APPROVAL": [], "WAITING": [], "WATCH": [], "BACKLOG": []
    }

    now_items: list[Item] = []
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        queue = _effective_queue(row)
        if queue is None:
            continue
        row["queue"] = queue
        by_id[str(row["id"])] = row
        if queue == "NOW":
            now_items.append(item_to_policy_item(row))
        else:
            queues[queue].append(row)

    ranked = rank_items(now_items)
    for ranking in ranked:
        row = dict(by_id[ranking["item_id"]])
        row["score"] = ranking["score"]
        row["contributions"] = ranking["contributions"]
        row["top_factors"] = ranking.get("top_factors", [])
        queues["NOW"].append(row)

    for queue in ("APPROVAL", "WAITING", "WATCH", "BACKLOG"):
        queues[queue].sort(key=_non_now_sort_key)

    nba = None
    if queues["NOW"]:
        top = queues["NOW"][0]
        nba = {
            "item_id": str(top["id"]),
            "title": top.get("title"),
            "score": top.get("score"),
            "top_factors": top.get("top_factors", []),
            "queue": "NOW",
        }

    return {
        "queues": queues,
        "counts": {name: len(values) for name, values in queues.items()},
        "next_best_action": nba,
        "source": "persisted_reconciled_state",
    }


def intake_item_key(normalized_intent: str, context: str) -> str:
    canonical = "\n".join((normalized_intent.strip().lower(), context.strip().lower())).encode("utf-8")
    return "escd-item-v1-" + hashlib.sha256(canonical).hexdigest()


def merge_source_refs(existing: Iterable[str], incoming: Iterable[str]) -> list[str]:
    out: list[str] = []
    for ref in [*list(existing), *list(incoming)]:
        value = str(ref or "").strip()
        if value and value not in out:
            out.append(value)
    return out


def calendar_contract(events: Iterable[dict[str, Any]], buffer_minutes: int = 0) -> dict[str, Any]:
    parsed: list[CalendarEvent] = []
    for raw in events:
        try:
            start = datetime.fromisoformat(str(raw.get("start") or "").replace("Z", "+00:00"))
            end = datetime.fromisoformat(str(raw.get("end") or "").replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("invalid_calendar_timestamp") from exc
        if start.tzinfo is None or end.tzinfo is None or end <= start:
            raise ValueError("invalid_calendar_window")
        source_ref = str(raw.get("source_ref") or "").strip()
        event_id = str(raw.get("event_id") or "").strip()
        if not source_ref or not event_id:
            raise ValueError("calendar_event_source_required")
        parsed.append(CalendarEvent(event_id=event_id, start=start, end=end, hard=bool(raw.get("hard", True)), source_ref=source_ref))

    conflicts = detect_calendar_conflicts(parsed, buffer_minutes=max(0, int(buffer_minutes)))
    enriched = []
    for conflict in conflicts:
        enriched.append({
            **conflict,
            "impact": "schedule_conflict",
            "options": ["keep_and_prepare", "propose_reschedule", "add_transition_buffer"],
            "recommended_resolution": "surface_for_dcs_review",
            "approval_required_for_external_change": True,
        })
    return {"conflicts": enriched, "external_calendar_write_performed": False}


def meeting_prep_contract(payload: dict[str, Any]) -> dict[str, Any]:
    source_refs = [str(x).strip() for x in payload.get("source_refs", []) if str(x).strip()]
    if not source_refs:
        raise ValueError("meeting_prep_source_required")
    return {
        "purpose": payload.get("purpose"),
        "participants_context": payload.get("participants_context", []),
        "prior_decisions_commitments": payload.get("prior_decisions_commitments", []),
        "open_questions": payload.get("open_questions", []),
        "files_evidence": payload.get("files_evidence", []),
        "desired_outcome": payload.get("desired_outcome"),
        "follow_up_items": payload.get("follow_up_items", []),
        "source_refs": source_refs,
        "status": "prepared",
        "external_calendar_write_performed": False,
    }


def communication_contract(message: dict[str, Any]) -> dict[str, Any]:
    source_ref = str(message.get("source_ref") or "").strip()
    if not source_ref:
        raise ValueError("communication_source_required")
    triage = communication_triage(message)
    proposed_reply = message.get("proposed_reply")
    return {
        "triage_class": triage,
        "source_ref": source_ref,
        "requested_action": message.get("requested_action"),
        "explicit_deadline": message.get("explicit_deadline"),
        "inferred_deadline": message.get("inferred_deadline"),
        "suggested_next_action": message.get("suggested_next_action"),
        "follow_up_trigger": message.get("follow_up_trigger"),
        "draft": {
            "status": "candidate" if proposed_reply else "not_prepared",
            "text": proposed_reply,
            "approval_required_for_external_send": True,
            "external_send_performed": False,
        },
    }


def contact_context_contract(context: dict[str, Any]) -> dict[str, Any]:
    valid, errors = contact_context_valid({
        "source_refs": context.get("provenance_refs") or context.get("source_refs") or [],
        "inferred_sensitive_trait": context.get("inferred_sensitive_trait", False),
    })
    if not valid:
        raise ValueError(errors[0])
    return {
        "contact_ref": context.get("contact_ref"),
        "display_name": context.get("display_name"),
        "organization": context.get("organization"),
        "role": context.get("role"),
        "relationship_context": context.get("relationship_context"),
        "active_commitments": context.get("active_commitments", []),
        "waiting_on_them": context.get("waiting_on_them", []),
        "they_are_waiting_on_dcs": context.get("they_are_waiting_on_dcs", []),
        "recent_interaction_refs": context.get("recent_interaction_refs", []),
        "next_follow_up_at": context.get("next_follow_up_at"),
        "communication_preferences": context.get("communication_preferences", {}),
        "important_dates": context.get("important_dates", []),
        "notes": context.get("notes"),
        "provenance_refs": context.get("provenance_refs") or context.get("source_refs") or [],
        "confidence_status": context.get("confidence_status", "unknown"),
        "source_of_truth_overwrite_performed": False,
    }


def routine_contract(routine: dict[str, Any], prior_run_key: str | None) -> dict[str, Any]:
    decision, reason = routine_run_decision(routine, prior_run_key)
    return {
        "decision": decision,
        "reason": reason,
        "run_key": routine.get("run_key"),
        "approval_required": bool(routine.get("approval_required", False)),
        "trigger_creates_eligibility_only": True,
    }


def notification_contract(payload: dict[str, Any]) -> dict[str, Any]:
    state = NotificationState(
        key=str(payload.get("key") or ""),
        current_value=payload.get("current_value"),
        prior_value=payload.get("prior_value"),
        acknowledged=bool(payload.get("acknowledged", False)),
        worsened=bool(payload.get("worsened", False)),
        threshold_crossed=bool(payload.get("threshold_crossed", False)),
        deadline_approaching=bool(payload.get("deadline_approaching", False)),
    )
    if not state.key:
        raise ValueError("notification_key_required")
    notify, reason = should_notify(state)
    return {
        "notify": notify,
        "reason": reason,
        "notification_class": payload.get("notification_class", "N1"),
        "channel": payload.get("channel", "in_app"),
        "delivery_claim": "intent_only",
    }


def retry_contract(payload: dict[str, Any]) -> dict[str, Any]:
    ctx = RetryContext(
        attempt=int(payload.get("attempt", 0)),
        max_attempts=int(payload.get("max_attempts", 0)),
        destructive=bool(payload.get("destructive", False)),
        idempotent=bool(payload.get("idempotent", False)),
        permission_failure=bool(payload.get("permission_failure", False)),
        security_failure=bool(payload.get("security_failure", False)),
        payload_changed=bool(payload.get("payload_changed", False)),
        unexpected_cost=bool(payload.get("unexpected_cost", False)),
        authority_conflict=bool(payload.get("authority_conflict", False)),
        uncertain_external_side_effect=bool(payload.get("uncertain_external_side_effect", False)),
    )
    allowed, reason = retry_allowed(ctx)
    return {"retry_allowed": allowed, "reason": reason}


def decision_contract(payload: dict[str, Any]) -> dict[str, Any]:
    valid, errors = decision_record_valid(payload)
    if not valid:
        raise ValueError(errors[0])
    return dict(payload)


def command_contract(text: str) -> dict[str, Any]:
    base = parse_command(text)
    stripped = text.strip()
    if not stripped:
        raise ValueError("command_required")
    first = stripped.split(None, 1)[0].upper()
    operation = first if first in TASK_CLASSES else base["operation"]
    target = stripped[len(stripped.split(None, 1)[0]):].strip()
    return {
        "raw_request": stripped,
        "operation": operation,
        "target": target,
        "authority_class": "evaluate_before_execution",
        "evidence_required": operation in {"RELEASE", "APPROVE", "COMMUNICATE"},
        "status": "parsed",
        "execution_performed": False,
    }


def file_route_contract(payload: dict[str, Any]) -> dict[str, Any]:
    source_ref = str(payload.get("source_ref") or "").strip()
    target = str(payload.get("target") or "").strip()
    if not source_ref or not target:
        raise ValueError("file_source_and_target_required")
    return {
        "source_ref": source_ref,
        "target": target,
        "operation": str(payload.get("operation") or "RESEARCH").upper(),
        "route_status": "proposed",
        "source_native_authority_preserved": True,
        "external_write_performed": False,
    }


def mobile_action_contract(payload: dict[str, Any]) -> dict[str, Any]:
    action = str(payload.get("action") or "").strip().lower()
    if action not in MOBILE_ACTIONS:
        raise ValueError("invalid_mobile_action")
    target_id = str(payload.get("target_id") or "").strip()
    if action != "capture" and not target_id:
        raise ValueError("mobile_target_required")
    mapping = {
        "capture": "CAPTURE",
        "defer": "WAITING",
        "approve": "APPROVE",
        "reject": "APPROVE",
        "done": "COMPLETION_REQUEST",
        "snooze": "WATCH",
        "open_source": "OPEN_SOURCE",
    }
    return {
        "action": action,
        "target_id": target_id or None,
        "operation": mapping[action],
        "requires_existing_governed_endpoint": action in {"approve", "reject", "done"},
        "execution_performed": False,
    }
