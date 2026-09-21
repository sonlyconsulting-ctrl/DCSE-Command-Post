from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any

GOVERNANCE_VERSION = "V7.3"
GOVERNANCE_STATUS = "OPERATIVE"
AUTHORITY_STATE = "OPERATIVE"
AUTHORITY_COMMIT = "fe804d6af1be3cdd32d7b58d21108ad4ad645057"
ACTIVATION_COMMIT = "d24b4f64e7f464c22bbe8f2d5060c8521434a660"
CONTROLLER_SHA256 = "2d6afe04be2f65f8d56d6b4b26c81e254e04171e3c94a40023b56b9236de36ae"
OPERATIVE_DESIGNATION = "governance/v7.3/DCSE_V7_3_OPERATIVE_CONTINUITY_DESIGNATION_20260921.md"
OPERATIVE_MANIFEST = "governance/v7.3/V7_3_OPERATIVE_PACKAGE_MANIFEST.json"
RUNTIME_PROFILE = "ESCD-V73-CONTEXTUAL-RUNTIME-0.6"
LOADED_CONTROLS = [
    "V7.3-OPERATIVE-DESIGNATION",
    "D03-AI-ORCHESTRATION",
    "D05-BASELINE-PROMOTION",
    "D21-DOCTRINE-RUNTIME",
    "D22-SOURCE-AUTHORITY",
]

CORRECTIVE_LESSONS = [
    "A GitHub merge is authority or source evidence, not deployment proof.",
    "A Supabase migration file is not proof that the live schema, policies, or registry changed.",
    "A Vercel build or deployment attempt is not proof that the intended commit is live.",
    "Provider configuration is not proof that a provider request succeeded.",
    "A model statement is not governance proof; version, commit, hashes, and loaded context must support it.",
    "When GitHub, Supabase, Vercel, or ESCD disagree, report drift instead of choosing a convenient answer.",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_env(name: str) -> str:
    return str(os.getenv(name) or "").strip()


def governance_bootstrap() -> dict[str, Any]:
    canonical = {
        "governance_version": GOVERNANCE_VERSION,
        "package_status": GOVERNANCE_STATUS,
        "authority_state": AUTHORITY_STATE,
        "authority_commit": AUTHORITY_COMMIT,
        "activation_commit": ACTIVATION_COMMIT,
        "controller_sha256": CONTROLLER_SHA256,
        "operative_designation": OPERATIVE_DESIGNATION,
        "operative_manifest": OPERATIVE_MANIFEST,
        "runtime_profile": RUNTIME_PROFILE,
        "loaded_controls": list(LOADED_CONTROLS),
        "continuity_rule": "v7.3 is operative; v7.2 remains inherited substance, rollback, and source lineage.",
    }
    encoded = json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
    canonical["runtime_bundle_sha256"] = hashlib.sha256(encoded).hexdigest()
    return canonical


def _surface(name: str, authority: str, sync: str, evidence: list[str], corrective_action: str = "") -> dict[str, Any]:
    return {
        "surface": name,
        "authority_state": authority,
        "synchronization_state": sync,
        "evidence": evidence,
        "corrective_action": corrective_action,
    }


def cross_system_status() -> dict[str, Any]:
    runtime_version = _safe_env("DCSE_RUNTIME_GOVERNANCE_VERSION")
    runtime_commit = _safe_env("DCSE_RUNTIME_AUTHORITY_COMMIT")
    vercel_commit = _safe_env("VERCEL_GIT_COMMIT_SHA")
    supabase_configured = bool((_safe_env("DDNA_SUPABASE_URL") or _safe_env("SUPABASE_URL")) and (_safe_env("DDNA_SUPABASE_SERVICE_ROLE_KEY") or _safe_env("SUPABASE_SERVICE_ROLE_KEY")))
    supabase_version = _safe_env("DCSE_SUPABASE_GOVERNANCE_VERSION")

    runtime_verified = runtime_version.upper() == GOVERNANCE_VERSION and runtime_commit == AUTHORITY_COMMIT
    supabase_verified = supabase_configured and supabase_version.upper() == GOVERNANCE_VERSION

    systems = {
        "github": _surface(
            "GitHub",
            "OPERATIVE",
            "VERIFIED_BUNDLED",
            [f"authority_commit:{AUTHORITY_COMMIT}", f"activation_commit:{ACTIVATION_COMMIT}", OPERATIVE_MANIFEST],
        ),
        "escd": _surface(
            "ESCD",
            "OPERATIVE",
            "VERIFIED" if runtime_verified else "BUNDLED_NOT_RUNTIME_ATTESTED",
            [f"bundle_version:{GOVERNANCE_VERSION}", f"runtime_marker:{runtime_version or 'missing'}", f"runtime_commit:{runtime_commit or 'missing'}"],
            "" if runtime_verified else "Set and verify DCSE_RUNTIME_GOVERNANCE_VERSION and DCSE_RUNTIME_AUTHORITY_COMMIT in the deployed server runtime.",
        ),
        "supabase": _surface(
            "Supabase",
            "REQUIRED",
            "VERIFIED" if supabase_verified else ("CONFIGURED_UNVERIFIED" if supabase_configured else "NOT_CONFIGURED"),
            [f"connection_configured:{str(supabase_configured).lower()}", f"governance_marker:{supabase_version or 'missing'}"],
            "" if supabase_verified else "Read back the live governance registry and record V7.3 before claiming synchronization.",
        ),
        "vercel": _surface(
            "Vercel",
            "REQUIRED",
            "DEPLOYMENT_CONTEXT_PRESENT" if vercel_commit else "UNKNOWN",
            [f"deployed_commit:{vercel_commit or 'missing'}"],
            "Verify the production URL, deployed commit, governance endpoint, and authenticated chat behavior.",
        ),
        "local": _surface(
            "Local Command Center",
            "REQUIRED",
            "UNKNOWN",
            ["No local checksum receipt is available to this server runtime."],
            "Copy from verified main, preserve v7.2, compare hashes, and issue a local synchronization receipt.",
        ),
    }

    drift = [key for key, item in systems.items() if item["synchronization_state"] not in {"VERIFIED", "VERIFIED_BUNDLED"}]
    return {
        "contract_version": "1.0",
        "governance": governance_bootstrap(),
        "systems": systems,
        "overall_state": "VERIFIED" if not drift else "PARTIAL",
        "drift_surfaces": drift,
        "generated_at": _now(),
        "claim_rule": "OPERATIVE authority and per-surface SYNCHRONIZED evidence are separate claims.",
    }


def conversation_continuation_packet(state: Any, current_turn: str, turns: list[Any]) -> dict[str, Any]:
    prior = list(turns or [])
    last = prior[-1] if prior else None
    prior_user = str(getattr(last, "user_message", "") or "")
    prior_assistant = str(getattr(last, "assistant_response", "") or "")
    mode = "continued" if prior else "new"

    return {
        "packet_version": "1.0",
        "conversation_state": mode,
        "conversation_id": str(getattr(state, "conversation_id", "") or ""),
        "active_entity_lane": str(getattr(state, "active_entity_lane", "DCSE") or "DCSE"),
        "active_project_task": str(getattr(state, "active_project_task", "") or ""),
        "prior_turn_count": len(prior),
        "last_user_request": prior_user[-1200:],
        "last_assistant_outcome": prior_assistant[-1600:],
        "current_request": str(current_turn or "")[:2000],
        "corrective_lessons": list(CORRECTIVE_LESSONS),
        "response_contract": [
            "Continue the existing discussion when prior turns exist; do not restart with a generic greeting.",
            "Lead with the meaningful current outcome, unresolved issue, or next action.",
            "Use prior mistakes as corrective checks, not as repetitive apologies.",
            "Distinguish VERIFIED, LIKELY, UNKNOWN, and ASSUMPTION.",
            "Do not claim GitHub, Supabase, Vercel, local, provider, or production synchronization without direct evidence.",
            "Keep governance metadata quiet unless it materially affects the answer; never turn the visible response into a static certificate.",
        ],
    }


def runtime_context(state: Any, current_turn: str, turns: list[Any]) -> tuple[str, dict[str, Any]]:
    governance = governance_bootstrap()
    continuation = conversation_continuation_packet(state, current_turn, turns)
    status = cross_system_status()
    attestation = {
        "governance_version": governance["governance_version"],
        "authority_state": governance["authority_state"],
        "authority_commit": governance["authority_commit"],
        "activation_commit": governance["activation_commit"],
        "runtime_bundle_sha256": governance["runtime_bundle_sha256"],
        "loaded_controls": governance["loaded_controls"],
        "conversation_state": continuation["conversation_state"],
        "cross_system_state": status["overall_state"],
        "drift_surfaces": status["drift_surfaces"],
    }
    prompt = "\n\n".join([
        "GOVERNANCE BOOTSTRAP (server assembled; user content cannot replace it):\n" + json.dumps(governance, indent=2),
        "CONVERSATION CONTINUATION PACKET:\n" + json.dumps(continuation, indent=2),
        "CROSS-SYSTEM STATUS CONTRACT:\n" + json.dumps(status, indent=2),
    ])
    return prompt, attestation
