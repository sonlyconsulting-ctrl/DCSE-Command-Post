from apps.escd.runtime.response_policy import (
    POLICY_ID,
    RULE_IDS,
    apply_response_policy,
    response_proof,
    response_system_message,
    validate_response_proof,
)


def test_response_policy_has_stable_rule_ids():
    assert POLICY_ID == "ESCD-RESP-V1"
    assert RULE_IDS == (
        "RESP-001",
        "RESP-002",
        "RESP-003",
        "RESP-004",
        "RESP-005",
        "RESP-006",
        "RESP-007",
        "RESP-008",
        "RESP-009",
        "RESP-010",
    )


def test_conversation_policy_forbids_fake_execution():
    prompt = response_system_message(lane="conversation")
    assert "Never claim that a tool" in prompt
    assert "simulated or fabricated success" in prompt
    assert "conversational Send lane" in prompt
    assert "No external execution evidence was supplied" in prompt


def test_operational_policy_keeps_control_with_orchestrator():
    prompt = response_system_message(
        lane="operational",
        evidence_refs=["operation://TURN-TEST", "item://ITEM-1"],
    )
    assert "control remains with the Orchestrator" in prompt
    assert "operation://TURN-TEST" in prompt


def test_policy_is_server_injected_before_user_prompt():
    messages = [{"role": "user", "content": "hello"}]
    governed = apply_response_policy(messages, lane="conversation")
    assert governed[0]["role"] == "system"
    assert POLICY_ID in governed[0]["content"]
    assert governed[-1] == messages[0]


def test_response_proof_detects_provider_return_without_simulation():
    messages = apply_response_policy(
        [{"role": "user", "content": "Return exactly TEST-123"}],
        lane="conversation",
    )
    proof = response_proof(
        provider="openai",
        model="test-model",
        request_messages=messages,
        response_text="TEST-123",
        provider_response_id="provider-response-1",
        transport="https_api",
        worker="api.example.test",
    )
    ok, problems = validate_response_proof(proof)
    assert ok is True
    assert problems == []
    assert proof["simulated"] is False
    assert proof["request_sha256"]
    assert proof["response_sha256"]
    assert proof["provider_response_id"] == "provider-response-1"


def test_response_hash_changes_if_content_changes():
    messages = [{"role": "user", "content": "test"}]
    first = response_proof(
        provider="ollama",
        model="qwen",
        request_messages=messages,
        response_text="one",
        transport="local_ollama",
    )
    second = response_proof(
        provider="ollama",
        model="qwen",
        request_messages=messages,
        response_text="two",
        transport="local_ollama",
    )
    assert first["response_sha256"] != second["response_sha256"]
