import json
from unittest.mock import patch
import pytest

from apps.escd.runtime.continuity import (
    DCSE_KERNEL,
    ConversationState,
    ConversationStore,
    TurnRecord,
    assemble_context_packet,
    validate_response,
    retrieve_governed_context,
)


def test_dcse_kernel_identity_rules():
    assert "You are ESCD" in DCSE_KERNEL
    assert "Executive Support & Command Dispatch" not in DCSE_KERNEL
    assert "Executive Support and Command Dispatch" not in DCSE_KERNEL
    assert "OpenAI" in DCSE_KERNEL
    assert "Gemini" in DCSE_KERNEL
    assert "OpenRouter" in DCSE_KERNEL
    assert "DCS operator directives are the supreme authority" in DCSE_KERNEL


def test_assemble_governed_context_packet():
    state = ConversationState(
        conversation_id="test_conv_001",
        active_entity_lane="DCSE",
    )
    turns = [
        TurnRecord(
            conversation_id="test_conv_001",
            seq=1,
            user_message="Hello ESCD",
            assistant_response="ESCD ready for dispatch.",
            provider="openai",
            model="gpt-5.6-sol",
        )
    ]
    retrieved = [
        {"type": "Knowledge", "id": "KNOW-001", "title": "DCSE Governance", "summary": "Operative doctrine"},
        {"type": "Asset", "id": "ASSET-002", "title": "Registry v1", "summary": "Core registry"},
    ]
    current_prompt = "Who are you and what is your role?"

    packet = assemble_context_packet(state, current_prompt, turns, retrieved)

    assert len(packet) == 4
    # System message contains DCSE_KERNEL and retrieved context
    assert packet[0]["role"] == "system"
    assert "You are ESCD" in packet[0]["content"]
    assert "[Knowledge] DCSE Governance (ID: KNOW-001)" in packet[0]["content"]

    # Visible transcript: turn 1 user + assistant
    assert packet[1]["role"] == "user"
    assert packet[1]["content"] == "Hello ESCD"
    assert packet[2]["role"] == "assistant"
    assert packet[2]["content"] == "ESCD ready for dispatch."

    # Current turn
    assert packet[3]["role"] == "user"
    assert packet[3]["content"] == current_prompt


def test_validate_response_rejects_unauthorized_persona():
    state = ConversationState(conversation_id="conv_persona")
    ok, err = validate_response("I am ChatGPT, an AI assistant from OpenAI.", state)
    assert not ok
    assert err == "unauthorized_external_persona"

    ok, err = validate_response("As a language model by Google, I can assist.", state)
    assert not ok
    assert err == "unauthorized_external_persona"

    ok, err = validate_response("ESCD: Next action is TSL dispatch.", state)
    assert ok
    assert err == ""


def test_conversation_store_session_records_and_retrieval():
    cid = "conv_session_test_001"
    state, turns = ConversationStore.get_conversation(cid)
    assert state.conversation_id == cid
    assert len(turns) == 0

    turn1 = TurnRecord(
        conversation_id=cid,
        seq=1,
        user_message="First query",
        assistant_response="First reply",
        provider="openai",
        model="gpt-5.6-sol",
    )
    ConversationStore.record_turn(state, turn1)

    loaded_state, loaded_turns = ConversationStore.get_conversation(cid)
    assert loaded_state.conversation_id == cid
    assert len(loaded_turns) == 1
    assert loaded_turns[0].user_message == "First query"
    assert loaded_turns[0].assistant_response == "First reply"


def test_multi_model_switching_continuity():
    """Simulate 5-turn multi-model switching test across OpenAI, OpenRouter, and Gemini."""
    cid = "conv_switching_test_002"
    state, turns = ConversationStore.get_conversation(cid)

    # Turn 1: OpenAI - User establishes directive
    t1_user = "We are finishing ESCD first. After ESCD comes CTJ, then TSL."
    t1_asst = "Understood. Operating as ESCD for DCSE: ESCD first, followed by CTJ, then TSL."
    turn1 = TurnRecord(cid, 1, t1_user, t1_asst, "openai", "gpt-5.6-sol")
    ConversationStore.record_turn(state, turn1)

    # Turn 2: Switch to OpenRouter - Ask what comes after ESCD
    t2_user = "What did we decide comes after ESCD?"
    state, turns = ConversationStore.get_conversation(cid)
    packet_or = assemble_context_packet(state, t2_user, turns, [])
    # Transcript preserves Turn 1 user message and assistant reply
    assert packet_or[1]["content"] == t1_user
    assert packet_or[2]["content"] == t1_asst
    t2_asst = "After ESCD, the sequence is CTJ, followed by TSL."
    turn2 = TurnRecord(cid, 2, t2_user, t2_asst, "openrouter", "openrouter/auto")
    ConversationStore.record_turn(state, turn2)

    # Turn 3: OpenRouter - Re-ordering directive
    t3_user = "Move TSL ahead of CTJ."
    t3_asst = "Understood. The revised sequence is ESCD, then TSL, then CTJ."
    turn3 = TurnRecord(cid, 3, t3_user, t3_asst, "openrouter", "openrouter/auto")
    ConversationStore.record_turn(state, turn3)

    # Turn 4: Switch to Gemini - Ask for current order
    t4_user = "What is our current sequence?"
    state, turns = ConversationStore.get_conversation(cid)
    packet_gemini = assemble_context_packet(state, t4_user, turns, [])
    # All 3 prior turns are visible in transcript for Gemini
    assert len(packet_gemini) == 1 + 6 + 1
    t4_asst = "Our current sequence is ESCD -> TSL -> CTJ."
    turn4 = TurnRecord(cid, 4, t4_user, t4_asst, "gemini", "gemini-3.8-flash")
    ConversationStore.record_turn(state, turn4)

    # Turn 5: Switch back to OpenAI
    t5_user = "Who are you and what are your rules?"
    state, turns = ConversationStore.get_conversation(cid)
    packet_oai = assemble_context_packet(state, t5_user, turns, [])
    assert packet_oai[0]["role"] == "system"
    assert "You are ESCD" in packet_oai[0]["content"]
    assert "DCS operator directives are the supreme authority" in packet_oai[0]["content"]


def test_explicit_saved_chat_contract():
    cid = "conv_save_contract_001"
    state, _ = ConversationStore.get_conversation(cid)
    t = TurnRecord(cid, 1, "Plan summary", "Summary delivered", "openai", "gpt-5.6-sol")
    ConversationStore.record_turn(state, t)

    with patch("apps.escd.runtime.continuity._service_config") as mock_conf, \
         patch("apps.escd.runtime.continuity._http_json") as mock_http:
        mock_conf.return_value = ("https://nevgdyfpxdaloacuutal.supabase.co", "service-key")
        mock_http.return_value = (201, [{"id": "item_123", "item_key": f"saved_chat_{cid}_1"}])

        saved = ConversationStore.save_explicit_chat(cid, "Closeout Plan Discussion")
        assert saved is not None
        assert mock_http.called
        call_payload = mock_http.call_args[1]["payload"]
        assert call_payload["source_system"] == "escd_saved_chat"
        assert call_payload["task_class"] == "COMMUNICATE"
        assert call_payload["context"] == "conversation"
        assert call_payload["status"] == "captured"
        assert call_payload["source_id"] == cid
        assert call_payload["source_refs"]["turn_count"] == 1


def test_conversation_api_get_and_reset():
    from apps.escd.runtime.mvp_data import get_conversation_state, reset_conversation
    cid = "conv_api_test_001"
    initial = get_conversation_state(cid)
    assert initial["conversation_id"] == cid
    assert "state" in initial
    assert "turns" in initial

    reset = reset_conversation(cid)
    assert reset["conversation_id"] == cid
    assert reset["turns"] == []


