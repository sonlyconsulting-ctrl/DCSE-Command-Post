import json
from unittest.mock import patch
import pytest

from apps.escd.runtime.continuity import (
    ConversationState,
    ConversationStore,
    TurnRecord,
    assemble_context_packet,
    extract_state_updates,
    validate_response,
    retrieve_governed_context,
)


def test_assemble_4_layer_context_packet():
    state = ConversationState(
        conversation_id="test_conv_001",
        current_goal="Deliver ESCD Minimal Assistant",
        active_entity_lane="DCSE",
        confirmed_decisions=["Execution Sequence: ESCD -> CTJ -> TSL"],
        pinned_facts=["DCS priority is high"],
        superseded_facts=["Prior Sequence: ESCD -> TSL"],
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
    current_prompt = "What is our current sequence?"

    packet = assemble_context_packet(state, current_prompt, turns, retrieved)

    # Layer A & B in system message
    assert len(packet) >= 3
    sys_msg = packet[0]["content"]
    assert packet[0]["role"] == "system"
    assert "You are ESCD" in sys_msg
    assert "Deliver ESCD Minimal Assistant" in sys_msg
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in sys_msg
    assert "Prior Sequence: ESCD -> TSL" in sys_msg
    assert "[Knowledge] DCSE Governance (ID: KNOW-001)" in sys_msg

    # Layer D: Prior turns + current prompt
    assert packet[1]["role"] == "user"
    assert packet[1]["content"] == "Hello ESCD"
    assert packet[2]["role"] == "assistant"
    assert packet[2]["content"] == "ESCD ready for dispatch."
    assert packet[3]["role"] == "user"
    assert packet[3]["content"] == current_prompt


def test_extract_state_updates_sequence_and_reorder():
    state = ConversationState(conversation_id="conv_seq_test")

    # Turn 1: Establish sequence
    msg1 = "We are finishing ESCD first. After ESCD comes CTJ, then TSL."
    extract_state_updates(msg1, "Acknowledged sequence: ESCD, CTJ, TSL.", state)
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in state.confirmed_decisions
    assert "Complete ESCD, followed by CTJ, then TSL" in state.current_goal

    # Turn 2: Move TSL ahead of CTJ
    msg2 = "Move TSL ahead of CTJ."
    extract_state_updates(msg2, "Understood. Re-ordered sequence.", state)
    assert "Execution Sequence: ESCD -> TSL -> CTJ" in state.confirmed_decisions
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in state.superseded_facts
    assert "Complete ESCD -> TSL -> CTJ" in state.current_goal
    assert any("Moved TSL ahead of CTJ" in pf for pf in state.pinned_facts)


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


def test_validate_response_detects_sequence_contradiction():
    state = ConversationState(
        conversation_id="conv_contra",
        confirmed_decisions=["Execution Sequence: ESCD -> TSL -> CTJ"],
    )
    # CTJ is claimed next after ESCD (contradicting TSL coming first)
    bad = "CTJ is next after ESCD in our roadmap."
    ok, err = validate_response(bad, state)
    assert not ok
    assert "contradicts_confirmed_sequence" in err

    good = "TSL is next after ESCD, followed by CTJ."
    ok, err = validate_response(good, state)
    assert ok


def test_conversation_store_and_turn_persistence():
    cid = "conv_persist_unit_test"
    state, turns = ConversationStore.get_conversation(cid)
    assert state.conversation_id == cid
    assert len(turns) == 0

    state.title = "Unit Test Thread"
    state.current_goal = "Test persistence"
    state.confirmed_decisions.append("Decision Alpha")

    turn1 = TurnRecord(
        conversation_id=cid,
        seq=1,
        user_message="First query",
        assistant_response="First reply",
        provider="openai",
        model="gpt-5.6-sol",
    )
    ConversationStore.persist_turn(state, turn1)

    # Fetch back
    loaded_state, loaded_turns = ConversationStore.get_conversation(cid)
    assert loaded_state.conversation_id == cid
    assert "Decision Alpha" in loaded_state.confirmed_decisions
    assert len(loaded_turns) >= 1
    assert loaded_turns[-1].user_message == "First query"
    assert loaded_turns[-1].assistant_response == "First reply"


def test_switching_test_simulation():
    """Simulate the 5-turn multi-model switching test across OpenAI, OpenRouter, and Gemini."""
    cid = "conv_switching_sim_001"
    state, turns = ConversationStore.get_conversation(cid)

    # Turn 1: OpenAI establishes sequence
    t1_user = "We are finishing ESCD first. After ESCD comes CTJ, then TSL."
    t1_asst = "Acknowledged. Order confirmed: ESCD first, then CTJ, followed by TSL."
    extract_state_updates(t1_user, t1_asst, state)
    turn1 = TurnRecord(cid, 1, t1_user, t1_asst, "openai", "gpt-5.6-sol")
    ConversationStore.persist_turn(state, turn1)
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in state.confirmed_decisions

    # Switch to OpenRouter (Turn 2)
    t2_user = "What did we decide comes after ESCD?"
    # OpenRouter context packet assembly
    state, turns = ConversationStore.get_conversation(cid)
    packet_or = assemble_context_packet(state, t2_user, turns, [])
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in packet_or[0]["content"]

    t2_asst = "After ESCD, we decided that CTJ comes next, followed by TSL."
    extract_state_updates(t2_user, t2_asst, state)
    turn2 = TurnRecord(cid, 2, t2_user, t2_asst, "openrouter", "openrouter/auto")
    ConversationStore.persist_turn(state, turn2)

    # Continue OpenRouter (Turn 3): Re-order
    t3_user = "Move TSL ahead of CTJ."
    t3_asst = "Understood. Updated sequence: ESCD -> TSL -> CTJ. TSL is now ahead of CTJ."
    extract_state_updates(t3_user, t3_asst, state)
    turn3 = TurnRecord(cid, 3, t3_user, t3_asst, "openrouter", "openrouter/auto")
    ConversationStore.persist_turn(state, turn3)
    assert "Execution Sequence: ESCD -> TSL -> CTJ" in state.confirmed_decisions
    assert "Execution Sequence: ESCD -> CTJ -> TSL" in state.superseded_facts

    # Switch to Gemini (Turn 4)
    t4_user = "What's our current order and what changed?"
    state, turns = ConversationStore.get_conversation(cid)
    packet_gemini = assemble_context_packet(state, t4_user, turns, [])
    assert "Execution Sequence: ESCD -> TSL -> CTJ" in packet_gemini[0]["content"]
    assert "Prior Sequence" not in packet_gemini[0]["content"] or "Superseded Facts" in packet_gemini[0]["content"]

    t4_asst = "Our current order is ESCD -> TSL -> CTJ. TSL was moved ahead of CTJ."
    extract_state_updates(t4_user, t4_asst, state)
    turn4 = TurnRecord(cid, 4, t4_user, t4_asst, "gemini", "gemini-3.8-flash")
    ConversationStore.persist_turn(state, turn4)

    # Switch back to OpenAI (Turn 5)
    t5_user = "Continue with the next body of work."
    state, turns = ConversationStore.get_conversation(cid)
    packet_oai = assemble_context_packet(state, t5_user, turns, [])
    assert "Execution Sequence: ESCD -> TSL -> CTJ" in packet_oai[0]["content"]
    assert len(turns) == 4


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


def test_dev_server_routes():
    import threading, time, urllib.request
    from scratch.dev_server import run

    t = threading.Thread(target=run, kwargs={"port": 3987}, daemon=True)
    t.start()
    time.sleep(0.5)

    req = urllib.request.Request("http://127.0.0.1:3987/escd/app")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
        assert resp.status == 200
        assert 'id="knowledge"' in html
        assert 'id="detailModal"' in html
        assert 'id="convPill"' in html


