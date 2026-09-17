from __future__ import annotations

import re
from typing import Any

from .repository import RepositoryError, SupabaseRLSClient


_GREETING = re.compile(r"^(hi|hello|hey|good (morning|afternoon|evening)|thanks|thank you|bye|goodbye)[!.?\s]*$", re.I)
_IDEA = [
    re.compile(p, re.I) for p in (
        r"\bidea\b", r"\bwhat if\b", r"\bcould we\b", r"\bmaybe we\b",
        r"\bthinking about\b", r"\bconcept\b", r"\bpotential\b",
    )
]
_TASK = [
    re.compile(p, re.I) for p in (
        r"\bneed to\b", r"\bshould\b", r"\bplease\b", r"\bcomplete\b",
        r"\bfinish\b", r"\bfix\b", r"\bbuild\b", r"\bcreate\b",
        r"\bupdate\b", r"\badd\b", r"\bremove\b", r"\bdeploy\b",
        r"\btest\b", r"\breview\b", r"\bcheck\b", r"\bevaluate\b",
        r"\bcompare\b", r"\bresearch\b", r"\bfollow up\b", r"\bfind\b",
    )
]
_KNOWLEDGE = [
    re.compile(p, re.I) for p in (
        r"\bremember that\b", r"\brecord that\b", r"\bnote that\b",
        r"\bwe established\b", r"\bwe decided\b", r"\bdecision is\b",
        r"\blocked\b", r"\bconfirmed\b", r"\bbaseline is\b",
    )
]


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _title(text: str, category: str, subject_name: str | None = None) -> str:
    clean = _clean(text)
    first = re.split(r"(?<=[.!?])\s+", clean, maxsplit=1)[0]
    if len(first) > 120:
        first = first[:117].rstrip() + "..."
    if subject_name and len(first) < 18:
        return f"{category.title()}: {subject_name}"
    return first or f"ESCD {category.title()}"


def classify_message(text: str, *, has_attachment: bool = False,
                     operational: bool = False) -> dict[str, Any]:
    clean = _clean(text)
    lower = clean.lower()

    if not clean:
        return {
            "primary_category": "ASSET" if has_attachment else "CHAT_ONLY",
            "secondary_categories": ["ASSET"] if has_attachment else [],
            "confidence": 0.99,
            "normalized_intent": "file intake" if has_attachment else "empty conversational turn",
            "rationale": "Attachment-only intake." if has_attachment else "No semantic request text.",
        }

    if _GREETING.match(clean):
        return {
            "primary_category": "CHAT_ONLY",
            "secondary_categories": [],
            "confidence": 0.99,
            "normalized_intent": lower,
            "rationale": "Greeting/closing with no durable operational intent.",
        }

    idea_hits = sum(bool(p.search(clean)) for p in _IDEA)
    task_hits = sum(bool(p.search(clean)) for p in _TASK)
    knowledge_hits = sum(bool(p.search(clean)) for p in _KNOWLEDGE)

    if idea_hits and task_hits <= 1:
        category, confidence, rationale = "IDEA", 0.93, "Exploratory/possibility language outweighs a single embedded action verb."
    elif task_hits:
        category = "TASK"
        confidence = min(0.98, 0.86 + (0.03 * min(task_hits, 4)))
        rationale = "Explicit action, review, build, fix, test, or follow-up language."
    elif knowledge_hits:
        category, confidence, rationale = "KNOWLEDGE", 0.94, "Explicit instruction to preserve an established fact, decision, or baseline."
    elif has_attachment:
        category, confidence, rationale = "ASSET", 0.91, "Attached artifact without a stronger task/idea/knowledge signal."
    elif clean.endswith("?"):
        category, confidence, rationale = "CHAT_ONLY", 0.88, "Question requiring a response; the question itself is not durable knowledge."
    elif operational:
        category, confidence, rationale = "CHAT_ONLY", 0.84, "Governed analysis request without an explicit durable-object creation signal."
    else:
        category, confidence, rationale = "CHAT_ONLY", 0.78, "Conversational statement with insufficient evidence for automatic materialization."

    secondary: list[str] = []
    if has_attachment and category != "ASSET":
        secondary.append("ASSET")
    if idea_hits and category != "IDEA":
        secondary.append("IDEA")
    if knowledge_hits and category != "KNOWLEDGE":
        secondary.append("KNOWLEDGE")

    return {
        "primary_category": category,
        "secondary_categories": secondary,
        "confidence": round(confidence, 4),
        "normalized_intent": lower[:500],
        "rationale": rationale,
    }


def persist_message_classification(
    repo: SupabaseRLSClient,
    turn: dict[str, Any],
    text: str,
    *,
    operation_turn_id: str | None = None,
    attachment: dict[str, Any] | None = None,
    operational: bool = False,
) -> dict[str, Any]:
    classification = classify_message(
        text,
        has_attachment=bool(attachment),
        operational=operational,
    )

    subjects = repo.resolve_subjects(text)
    subject_name = subjects[0].get("canonical_name") if subjects else None
    payload = {
        "title": _title(text, classification["primary_category"], subject_name),
        "content": _clean(text),
        "subjects": [
            {
                "id": s.get("id"),
                "subject_key": s.get("subject_key"),
                "canonical_name": s.get("canonical_name"),
                "confidence": s.get("confidence"),
            }
            for s in subjects
        ],
    }
    if attachment:
        payload["attachment"] = attachment

    row = repo.create_turn_classification({
        "conversation_turn_id": turn["id"],
        "operation_turn_id": operation_turn_id,
        "primary_category": classification["primary_category"],
        "secondary_categories": classification["secondary_categories"],
        "normalized_intent": classification["normalized_intent"],
        "confidence": classification["confidence"],
        "rationale": classification["rationale"],
        "candidate_payload": payload,
    })

    for index, subject in enumerate(subjects):
        relation = "PRIMARY" if index == 0 else "ABOUT"
        provenance = {
            "source": "deterministic_alias_resolution",
            "conversation_turn_id": turn["id"],
            "classification_id": row.get("id"),
        }
        repo.link_subject(
            subject["id"], "conversation_turn", turn["id"],
            relation_type=relation,
            confidence=float(subject.get("confidence") or 0.9),
            provenance=provenance,
        )
        repo.link_subject(
            subject["id"], "conversation", turn["conversation_id"],
            relation_type="ABOUT",
            confidence=float(subject.get("confidence") or 0.9),
            provenance=provenance,
        )

    materialized: dict[str, Any] | None = None
    if (
        row.get("primary_category") in {"TASK", "IDEA", "KNOWLEDGE"}
        and float(row.get("confidence") or 0) >= 0.85
    ):
        try:
            materialized = repo.materialize_classification(row["id"], force=False)
        except RepositoryError:
            materialized = None

    return {
        "classification": row,
        "subjects": subjects,
        "materialized": materialized,
    }


def operation_view(snapshot: dict[str, Any]) -> dict[str, Any]:
    turn = dict(snapshot.get("turn") or {})
    final_response = turn.get("final_response") or {}
    state = turn.get("state") or "REQUESTED"
    turn["turn_id"] = turn.get("turn_key")
    turn["status"] = state
    turn["provider"] = turn.get("active_provider") or turn.get("provider_preference")
    turn["model"] = turn.get("active_model")
    turn["worker"] = turn.get("claimed_by_worker_key")
    labels = {
        "REQUESTED": "Queued for orchestrator",
        "CLAIMED": "Claimed",
        "INTERPRETING": "Interpreting",
        "PLANNING": "Planning",
        "EXECUTING": "Executing",
        "VERIFYING": "Verifying",
        "RESPONDING": "Composing response",
        "WAITING_USER": "WAITING FOR DCS",
        "ESCALATED": "ESCALATED",
        "COMPLETE": "✓ COMPLETE",
        "REFUSED": "REFUSED",
        "FAILED": "FAILED",
        "CANCELLED": "CANCELLED",
    }
    turn["status_label"] = labels.get(state, state)
    if isinstance(final_response, dict) and final_response:
        turn["response"] = final_response
    turn["events"] = snapshot.get("events") or []
    return turn
