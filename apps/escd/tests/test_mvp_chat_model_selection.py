"""Read-only unit tests for ESCD chat model selection and API-key isolation."""
import pytest

from apps.escd.runtime import mvp_data


def _provider(provider):
    return {
        "provider": provider,
        "enabled": True,
        "api_key": "unit-test-only-credential",
        "model": "gpt-5.6-sol" if provider == "openai" else "gemini-test",
        "timeout_seconds": 10,
        "max_output_tokens": 1024,
    }


def test_openai_model_menu_contains_all_approved_choices_and_configured_default(monkeypatch):
    monkeypatch.setattr(mvp_data, "provider_runtime", _provider)
    state = mvp_data.provider_status()
    assert [m["id"] for m in state["openai"]["chat_models"]] == [
        "gpt-5.6-sol", "gpt-5.6-terra", "gpt-5.6-luna"
    ]
    assert state["openai"]["model"] == "gpt-5.6-sol"
    assert state["gemini"]["chat_models"] == []
    assert "api_key" not in state["openai"]
    assert state["openai"]["configured"] is True


def test_current_admin_configured_openai_model_is_preserved_without_duplicates():
    choices = mvp_data._openai_chat_model_options("gpt-4.1")
    assert choices[0] == {"id": "gpt-4.1", "label": "gpt-4.1 (configured)"}
    assert len(mvp_data._openai_chat_model_options("gpt-5.6-sol")) == 3


def test_openai_chat_uses_selected_model_for_only_this_request(monkeypatch):
    sent = []
    monkeypatch.setattr(mvp_data, "provider_runtime", _provider)

    def fake_http(url, *, method="GET", headers=None, payload=None, timeout=30):
        sent.append((url, payload, headers))
        return 200, {"output_text": "Test reply", "model": payload["model"]}

    monkeypatch.setattr(mvp_data, "_http_json", fake_http)
    conversation = [{"role": "user", "content": "Test message"}]
    result = mvp_data.chat("openai", conversation, "gpt-5.6-terra")
    assert result == {"provider": "openai", "model": "gpt-5.6-terra", "content": "Test reply"}
    assert sent[0][0] == "https://api.openai.com/v1/responses"
    assert sent[0][1]["model"] == "gpt-5.6-terra"
    assert sent[0][2]["Authorization"] == "Bearer unit-test-only-credential"
    mvp_data.chat("openai", conversation)
    assert sent[1][1]["model"] == "gpt-5.6-sol"


@pytest.mark.parametrize("requested", ["gpt-malicious", "gpt-5.6-sol;DROP", "", "gpt-5.6-sol " + "x", 17])
def test_chat_rejects_unapproved_model_before_openai_http(monkeypatch, requested):
    monkeypatch.setattr(mvp_data, "provider_runtime", _provider)
    monkeypatch.setattr(mvp_data, "_http_json", lambda *args, **kwargs: pytest.fail("HTTP called"))
    with pytest.raises(mvp_data.MVPServiceError, match="chat_model"):
        mvp_data.chat("openai", [{"role": "user", "content": "Test"}], requested)


def test_override_is_not_accepted_for_other_provider(monkeypatch):
    monkeypatch.setattr(mvp_data, "provider_runtime", _provider)
    monkeypatch.setattr(mvp_data, "_http_json", lambda *args, **kwargs: pytest.fail("HTTP called"))
    with pytest.raises(mvp_data.MVPServiceError, match="chat_model_override_not_supported"):
        mvp_data.chat("gemini", [{"role": "user", "content": "Test"}], "gpt-5.6-sol")
