import base64
import json
from unittest.mock import patch

import pytest

from apps.escd.runtime import mvp_data as data
from apps.escd.api.mvp import handler


def runtime(key="test-only-provider-value", model="test-model"):
    return [{"provider": "openai", "api_key": key, "enabled": True, "model": model}]


def test_key_save_requires_matching_vault_readback():
    with patch.object(data, "_rpc", side_effect=[True, runtime()]) as rpc:
        result = data.set_provider_secret("openai", "test-only-provider-value")
    assert result == {"provider": "openai", "configured": True, "credential_source": "vault"}
    assert [call.args[0] for call in rpc.call_args_list] == ["set_escd_provider_secret", "get_escd_provider_runtime"]
    assert "test-only-provider-value" not in json.dumps(result)


@pytest.mark.parametrize("responses", [[False, runtime()], [True, runtime("different-value")], [True, runtime("")]])
def test_failed_readback_never_reports_configured(responses):
    with patch.object(data, "_rpc", side_effect=responses):
        with pytest.raises(data.MVPServiceError, match="Vault save could not be verified"):
            data.set_provider_secret("openai", "test-only-provider-value")


def test_registry_outage_is_visible_and_does_not_use_environment_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-only-environment-value")
    with patch.object(data, "_rpc", side_effect=RuntimeError("private upstream detail")):
        status = data.provider_status()
    assert status["openai"]["configured"] is False
    assert status["openai"]["registry_available"] is False
    assert "Provider registry unavailable" in status["openai"]["registry_error"]
    assert "private upstream detail" not in json.dumps(status)
    assert "test-only-environment-value" not in json.dumps(status)


def test_credential_must_match_service_role_and_expected_project(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://nevgdyfpxdaloacuutal.supabase.co")
    for ref, role in [("otherproject", "service_role"), ("nevgdyfpxdaloacuutal", "anon")]:
        payload = base64.urlsafe_b64encode(json.dumps({"ref": ref, "role": role}).encode()).decode().rstrip("=")
        monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "test." + payload + ".test")
        with pytest.raises(data.MVPServiceError, match="does not match"):
            data._service_config()


def test_each_request_reads_current_model_and_key():
    with patch.object(data, "_rpc", side_effect=[runtime("first-key", "first-model"), runtime("second-key", "second-model")]):
        first = data.provider_runtime("openai")
        second = data.provider_runtime("openai")
    assert (first["api_key"], first["model"]) == ("first-key", "first-model")
    assert (second["api_key"], second["model"]) == ("second-key", "second-model")


def test_provider_save_rejects_unauthenticated_request_before_vault():
    request = object.__new__(handler)
    request.path = "/api/mvp/provider-secret"
    request.headers = {}
    request._read_json = lambda: {"provider": "openai", "secret": "test-only-provider-value"}
    result = []
    request._json = lambda code, body: result.append((code, body))
    with patch("apps.escd.api.mvp.set_provider_secret") as save:
        request.do_POST()
        save.assert_not_called()
    assert result[0][0] == 401


def test_auth_config_is_public_and_returns_supabase_url(monkeypatch):
    monkeypatch.setenv("SUPABASE_URL", "https://nevgdyfpxdaloacuutal.supabase.co")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_ANON_KEY", "test-anon-key")
    request = object.__new__(handler)
    request.path = "/api/mvp/auth-config"
    request.headers = {}
    result = []
    request._json = lambda code, body: result.append((code, body))
    request.do_GET()
    assert result[0][0] == 200
    assert result[0][1]["ok"] is True
    assert result[0][1]["supabase_url"] == "https://nevgdyfpxdaloacuutal.supabase.co"
    assert result[0][1]["anon_key"] == "test-anon-key"


def test_provider_status_circuit_breaker_trips_and_fast_fails():
    data._SUPABASE_RPC_FAIL_UNTIL = 0.0
    with patch.object(data, "_rpc", side_effect=data.MVPServiceError("mock database timeout")) as mock_rpc:
        status = data.provider_status()
    assert mock_rpc.call_count == 1
    assert data._SUPABASE_RPC_FAIL_UNTIL > 0.0
    for p in data.PROVIDERS:
        assert status[p]["registry_available"] is False


def test_login_timeout_returns_503_service_unavailable():
    from apps.escd.runtime.auth import AuthError
    request = object.__new__(handler)
    request.path = "/api/mvp/login"
    request.headers = {"Content-Length": "10"}
    request._read_json = lambda: {"email": "test@sonlyconsulting.com", "password": "pass"}
    result = []
    request._json = lambda code, body: result.append((code, body))
    with patch.object(request, "_login", side_effect=AuthError("auth_timeout")):
        request.do_POST()
    assert result[0][0] == 503
    assert "temporarily unreachable" in result[0][1]["error"]

