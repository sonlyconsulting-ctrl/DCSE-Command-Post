from dataclasses import dataclass

from apps.escd.runtime.governance_runtime import (
    AUTHORITY_COMMIT,
    GOVERNANCE_VERSION,
    PROMOTION_COMMIT,
    RECONCILIATION_COMMIT,
    CONTEXTUAL_RUNTIME_MERGE,
    conversation_continuation_packet,
    cross_system_status,
    governance_bootstrap,
    runtime_context,
)


@dataclass
class State:
    conversation_id: str = "conv_test"
    active_entity_lane: str = "DCSE"
    active_project_task: str = "ESCD runtime"


@dataclass
class Turn:
    user_message: str
    assistant_response: str


def test_v73_governance_bootstrap_is_hash_attested():
    data = governance_bootstrap()
    assert data["governance_version"] == "V7.3"
    assert data["package_status"] == "OPERATIVE"
    assert data["authority_commit"] == AUTHORITY_COMMIT == PROMOTION_COMMIT
    assert data["activation_commit"] == PROMOTION_COMMIT
    assert data["reconciliation_commit"] == RECONCILIATION_COMMIT
    assert data["contextual_runtime_merge"] == CONTEXTUAL_RUNTIME_MERGE
    assert data["repository_head_rule"] == "dynamic_not_promotion_authority"
    assert "durable identifier" in data["evidence_language_rule"]
    assert len(data["runtime_bundle_sha256"]) == 64
    assert "D21-DOCTRINE-RUNTIME" in data["loaded_controls"]
    assert "D22-SOURCE-AUTHORITY" in data["loaded_controls"]


def test_continuation_packet_uses_prior_turn_and_is_not_static_greeting():
    packet = conversation_continuation_packet(
        State(),
        "What comes next?",
        [Turn("Promote v7.3", "v7.3 is operative; runtime synchronization remains.")],
    )
    assert packet["conversation_state"] == "continued"
    assert packet["prior_turn_count"] == 1
    assert packet["last_user_request"] == "Promote v7.3"
    assert "generic greeting" in " ".join(packet["response_contract"])
    assert any("Supabase migration file" in x for x in packet["corrective_lessons"])


def test_new_conversation_packet_is_explicit():
    packet = conversation_continuation_packet(State(), "Start", [])
    assert packet["conversation_state"] == "new"
    assert packet["prior_turn_count"] == 0


def test_cross_system_contract_does_not_invent_sync(monkeypatch):
    for name in (
        "DCSE_RUNTIME_GOVERNANCE_VERSION",
        "DCSE_RUNTIME_AUTHORITY_COMMIT",
        "DCSE_SUPABASE_GOVERNANCE_VERSION",
        "VERCEL_GIT_COMMIT_SHA",
        "DDNA_SUPABASE_URL",
        "DDNA_SUPABASE_SERVICE_ROLE_KEY",
        "SUPABASE_URL",
        "SUPABASE_SERVICE_ROLE_KEY",
    ):
        monkeypatch.delenv(name, raising=False)
    status = cross_system_status()
    assert status["systems"]["github"]["synchronization_state"] == "VERIFIED_BUNDLED"
    assert status["systems"]["supabase"]["synchronization_state"] == "NOT_CONFIGURED"
    assert status["systems"]["vercel"]["synchronization_state"] == "UNKNOWN"
    assert status["overall_state"] == "PARTIAL"


def test_runtime_context_contains_all_three_contracts():
    prompt, attestation = runtime_context(State(), "Continue", [])
    assert "GOVERNANCE BOOTSTRAP" in prompt
    assert "CONVERSATION CONTINUATION PACKET" in prompt
    assert "CROSS-SYSTEM STATUS CONTRACT" in prompt
    assert attestation["governance_version"] == GOVERNANCE_VERSION
    assert attestation["conversation_state"] == "new"


def test_github_evidence_preserves_commit_roles(monkeypatch):
    monkeypatch.delenv("DCSE_RUNTIME_GOVERNANCE_VERSION", raising=False)
    monkeypatch.delenv("DCSE_RUNTIME_AUTHORITY_COMMIT", raising=False)
    status = cross_system_status()
    evidence = " ".join(status["systems"]["github"]["evidence"])
    assert f"promotion_commit:{PROMOTION_COMMIT}" in evidence
    assert f"reconciliation_commit:{RECONCILIATION_COMMIT}" in evidence
    assert f"contextual_runtime_merge:{CONTEXTUAL_RUNTIME_MERGE}" in evidence
