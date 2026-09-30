from pathlib import Path

from apps.escd.runtime.conversation_memory import classify_message, operation_view
from dcse.adapters import OllamaAdapter
from dcse.model import Operation

ROOT = Path(__file__).resolve().parents[1]
APP_HTML = ROOT / "web" / "app.html"
MVP_HTML = ROOT / "web" / "mvp.html"
LOGIN_HTML = ROOT / "web" / "login.html"


def test_ui_dual_lane_and_history_contract():
    for target in (APP_HTML, MVP_HTML):
        html = target.read_text(encoding="utf-8")
        assert '<option value="ollama">Ollama</option>' in html
        assert 'id="send"' in html
        assert 'id="orchestrate"' in html
        assert 'id="operationStrip"' in html
        assert 'id="stripStop"' in html
        assert 'id="stripContinue"' in html
        assert 'id="history"' in html
        assert "loadHistory" in html
        assert "resumeConversation" in html
        assert "escd_active_conversation_id" in html
        assert "/session/refresh" in html
        assert "conversation_id:activeConversationId" in html


def test_login_retains_refresh_token():
    html = LOGIN_HTML.read_text(encoding="utf-8")
    assert "refresh_token" in html
    assert "escd_refresh_token" in html


def test_greeting_remains_chat_only():
    result = classify_message("hi")
    assert result["primary_category"] == "CHAT_ONLY"
    assert result["confidence"] >= 0.95


def test_explicit_action_becomes_task():
    result = classify_message("Please complete the Vow & Go production review.")
    assert result["primary_category"] == "TASK"
    assert result["confidence"] >= 0.85


def test_exploratory_language_becomes_idea():
    result = classify_message("What if we add a keepsake mode to Vow & Go?")
    assert result["primary_category"] == "IDEA"
    assert result["confidence"] >= 0.85


def test_explicit_preservation_becomes_knowledge():
    result = classify_message("Remember that Vow & Go uses the family product line.")
    assert result["primary_category"] == "KNOWLEDGE"
    assert result["confidence"] >= 0.85


def test_generic_orchestrate_does_not_create_duplicate_task():
    result = classify_message("Vow & Go?", operational=True)
    assert result["primary_category"] == "CHAT_ONLY"


def test_attachment_without_stronger_signal_is_asset():
    result = classify_message("", has_attachment=True)
    assert result["primary_category"] == "ASSET"


def test_attachment_can_be_secondary_to_task():
    result = classify_message("Review this package and identify the gaps.", has_attachment=True)
    assert result["primary_category"] == "TASK"
    assert "ASSET" in result["secondary_categories"]


def test_operation_view_maps_durable_turn_to_ui_shape():
    snapshot = {
        "turn": {
            "turn_key": "TURN-ABC123",
            "state": "WAITING_USER",
            "stage": "PRECONDITION",
            "provider_preference": "ollama",
            "claimed_by_worker_key": "DCS-WINDOWS-OLLAMA-01",
            "final_response": {"content": "Decision required."},
        },
        "events": [{"event_type": "REQUEST_RECEIVED"}],
    }
    view = operation_view(snapshot)
    assert view["turn_id"] == "TURN-ABC123"
    assert view["status"] == "WAITING_USER"
    assert view["status_label"] == "WAITING FOR DCS"
    assert view["provider"] == "ollama"
    assert view["worker"] == "DCS-WINDOWS-OLLAMA-01"
    assert view["response"]["content"] == "Decision required."
    assert len(view["events"]) == 1


def test_ollama_failure_is_honest_not_simulated():
    adapter = OllamaAdapter(
        base_url="http://127.0.0.1:1",
        model="qwen2.5-coder:latest",
        worker="DCS-WINDOWS-OLLAMA-01",
    )
    op = Operation(
        lane="DCSE",
        entity="task",
        action="evaluate",
        facts={
            "prompt": "Review Vow & Go.",
            "turn_id": "TURN-TEST-001",
            "timeout_seconds": 1,
        },
    )
    result = adapter.perform(op)
    assert result["control"] == "RETURN_TO_ORCHESTRATOR"
    assert result["provider"] == "ollama"
    assert result["worker"] == "DCS-WINDOWS-OLLAMA-01"
    assert result["performed"] is False
    assert result["status"] == "FAILED"
    assert result["payload"]["error"] == "ollama_connection_failed"
    assert result["evidence_refs"] == []


def test_no_offline_simulation_or_in_memory_api_path():
    runtime = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    api = (ROOT / "api" / "mvp.py").read_text(encoding="utf-8")
    assert "allow_offline_sim" not in runtime
    assert "_synthesize_ollama_reasoning" not in runtime
    assert "create_orchestration_turn(" not in runtime
    assert "_run_orchestration_lifecycle" not in runtime
    assert "create_orchestration_turn(" not in api
    assert "get_orchestration_turn(" not in api
    assert "update_orchestration_turn_action(" not in api
    assert "repo.submit_operation_turn(" in api
    assert "repo.operation_turn_snapshot(" in api

def test_worker_format_as_escd_document_normalizes_em_dashes():
    from apps.escd.runtime.ollama_worker import format_as_escd_document
    raw = "Section 1\nThis text has an em dash \u2014 and an en dash \u2013 here."
    formatted = format_as_escd_document(raw)
    assert "\u2014" not in formatted
    assert "\u2013" not in formatted
    assert "-" in formatted


def test_worker_complete_distinguishes_execution_and_acceptance():
    from unittest.mock import MagicMock, patch
    from apps.escd.runtime.ollama_worker import _complete

    mock_turn = {"id": "turn-test-1", "conversation_id": "conv-test-1", "turn_key": "TURN-TEST-01"}
    
    with patch("apps.escd.runtime.ollama_worker._patch_turn") as mock_patch_turn, \
         patch("apps.escd.runtime.ollama_worker._append_assistant_turn", return_value={"id": "asst-1"}), \
         patch("apps.escd.runtime.ollama_worker._event") as mock_event:
        
        # 1. Passed acceptance
        _complete(
            mock_turn,
            "Clean response text.",
            evidence_refs=["ref-1"],
            usage={"total_tokens": 10},
            rule_evidence={"fail_count": 0},
            acceptance_passed=True,
        )
        assert mock_patch_turn.call_count == 2
        final_call = mock_patch_turn.call_args_list[-1]
        assert final_call[0][1]["state"] == "COMPLETE"
        assert final_call[0][1]["final_response"]["acceptance_status"] == "PASSED"

        # 2. Flagged acceptance (e.g. unverified guarantee detected)
        _complete(
            mock_turn,
            "Response with unverified claims.",
            evidence_refs=["ref-1"],
            usage={"total_tokens": 10},
            rule_evidence={"fail_count": 1},
            acceptance_passed=False,
        )
        final_flagged = mock_patch_turn.call_args_list[-1]
        assert final_flagged[0][1]["state"] == "COMPLETE"
        assert final_flagged[0][1]["final_response"]["acceptance_status"] == "FLAGGED"
