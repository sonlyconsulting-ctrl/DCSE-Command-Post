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
    assert 'legacy_in_memory_orchestration_disabled' in runtime
    assert "create_orchestration_turn(" not in api
    assert "get_orchestration_turn(" not in api
    assert "update_orchestration_turn_action(" not in api
