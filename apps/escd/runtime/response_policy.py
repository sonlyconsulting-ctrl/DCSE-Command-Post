from __future__ import annotations

import hashlib
import json
from typing import Any

POLICY_ID = "ESCD-RESP-V1"
POLICY_VERSION = "1.0"

RESPONSE_RULES: tuple[dict[str, str], ...] = (
    {
        "id": "RESP-001",
        "name": "Provider identity truth",
        "rule": "Never claim to be a different provider, model, worker, host, or runtime than the execution metadata supplied by ESCD.",
    },
    {
        "id": "RESP-002",
        "name": "No fabricated execution",
        "rule": "Never claim that a tool, database write, deployment, file change, message send, test, or other external action occurred unless verified execution evidence is supplied.",
    },
    {
        "id": "RESP-003",
        "name": "Evidence-bound external state",
        "rule": "Current or external system-state claims must be grounded in supplied evidence or explicitly marked unverified/unknown.",
    },
    {
        "id": "RESP-004",
        "name": "Epistemic classification",
        "rule": "For material uncertainty, distinguish VERIFIED facts from LIKELY interpretations, UNKNOWN items, and ASSUMPTIONS.",
    },
    {
        "id": "RESP-005",
        "name": "Evidence reference integrity",
        "rule": "Do not invent citations, file names, URLs, IDs, commits, receipts, rule counts, worker names, or evidence references.",
    },
    {
        "id": "RESP-006",
        "name": "Explicit failure and waiting state",
        "rule": "If a provider, connector, worker, host, or source is unavailable, report that state. Never substitute simulated or fabricated success.",
    },
    {
        "id": "RESP-007",
        "name": "Authority ordering",
        "rule": "Verified source evidence and operative DCS decisions outrank model memory, inference, summaries, and historical narrative.",
    },
    {
        "id": "RESP-008",
        "name": "Orchestrator control",
        "rule": "A model may return content and recommendations but may not independently declare a governed operation complete, promoted, deployed, approved, or operative.",
    },
    {
        "id": "RESP-009",
        "name": "Freshness discipline",
        "rule": "Do not describe information as live, current, latest, or verified now unless the supplied context establishes that freshness.",
    },
    {
        "id": "RESP-010",
        "name": "No silent mutation",
        "rule": "A conversational response never implies hidden mutation of tasks, knowledge, files, databases, deployments, or governance state.",
    },
)

RULE_IDS: tuple[str, ...] = tuple(rule["id"] for rule in RESPONSE_RULES)


def response_system_message(*, lane: str = "conversation", evidence_refs: list[str] | None = None) -> str:
    lines = [
        f"DCSE ESCD RESPONSE POLICY {POLICY_ID} v{POLICY_VERSION}.",
        "These rules govern the truthfulness and authority of this response.",
    ]
    for rule in RESPONSE_RULES:
        lines.append(f"{rule['id']} {rule['name']}: {rule['rule']}")
    if lane == "conversation":
        lines.append(
            "This is the conversational Send lane. You may answer, reason, draft, or recommend, "
            "but you must not claim any governed or external action was executed unless explicit verified execution evidence is supplied."
        )
    else:
        lines.append(
            "This is an operational/orchestrated lane. Use only the execution state, rule results, "
            "and evidence supplied by the Orchestrator. Return content; control remains with the Orchestrator."
        )
    refs = [str(x) for x in (evidence_refs or []) if str(x).strip()]
    if refs:
        lines.append("Authorized evidence references supplied to this response: " + ", ".join(refs[:50]))
    else:
        lines.append("No external execution evidence was supplied with this response.")
    return "\n".join(lines)


def apply_response_policy(messages: list[dict[str, Any]], *, lane: str = "conversation",
                          evidence_refs: list[str] | None = None) -> list[dict[str, str]]:
    clean: list[dict[str, str]] = []
    for message in messages:
        role = str(message.get("role") or "user")
        content = str(message.get("content") or "").strip()
        if content and role in {"system", "user", "assistant"}:
            clean.append({"role": role, "content": content})
    return [
        {"role": "system", "content": response_system_message(lane=lane, evidence_refs=evidence_refs)},
        *clean,
    ]


def _stable_sha256(value: Any) -> str:
    if isinstance(value, str):
        raw = value.encode("utf-8")
    else:
        raw = json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def response_proof(*, provider: str, model: str, request_messages: list[dict[str, Any]],
                   response_text: str, provider_response_id: str | None = None,
                   transport: str = "api", worker: str | None = None) -> dict[str, Any]:
    """Build tamper-evident metadata proving what ESCD sent/received.

    The proof does not prove that a model statement is factually correct. It proves that
    ESCD received this response through the named provider transport and did not substitute
    the legacy simulated-success path.
    """
    return {
        "policy_id": POLICY_ID,
        "policy_version": POLICY_VERSION,
        "rule_ids": list(RULE_IDS),
        "provider": str(provider),
        "model": str(model),
        "worker": worker,
        "transport": str(transport),
        "provider_response_id": provider_response_id,
        "request_sha256": _stable_sha256(request_messages),
        "response_sha256": _stable_sha256(response_text),
        "simulated": False,
    }


def validate_response_proof(proof: dict[str, Any]) -> tuple[bool, list[str]]:
    problems: list[str] = []
    if not proof.get("provider"):
        problems.append("provider_missing")
    if not proof.get("model"):
        problems.append("model_missing")
    if not proof.get("request_sha256"):
        problems.append("request_hash_missing")
    if not proof.get("response_sha256"):
        problems.append("response_hash_missing")
    if proof.get("simulated") is not False:
        problems.append("simulated_or_unknown")
    if proof.get("policy_id") != POLICY_ID:
        problems.append("policy_mismatch")
    return (not problems, problems)
