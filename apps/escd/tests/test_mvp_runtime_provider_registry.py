from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "runtime" / "mvp_data.py"
API = ROOT / "api" / "mvp.py"
UI = ROOT / "web" / "mvp.html"


def test_runtime_provider_registry_is_server_side():
    service = SERVICE.read_text(encoding="utf-8")
    assert "get_escd_provider_runtime" in service
    assert "set_escd_provider_secret" in service
    assert "update_escd_provider_config" in service
    assert "credential_source" in service
    assert "openrouter" in service


def test_provider_errors_preserve_detail_but_redact_keys():
    service = SERVICE.read_text(encoding="utf-8")
    assert "_extract_error_detail" in service
    assert "_safe_provider_detail" in service
    assert "sk-proj-***" in service
    assert "sk-or-v1-***" in service
    assert "AIza***" in service


def test_provider_admin_requires_authenticated_api_boundary():
    api = API.read_text(encoding="utf-8")
    assert '"/api/mvp/provider-secret"' in api
    assert '"/api/mvp/provider-config"' in api
    assert "self._auth()" in api
    assert "set_provider_secret" in api
    assert "update_provider_config" in api


def test_browser_never_persists_provider_secret():
    html = UI.read_text(encoding="utf-8")
    assert 'id="providerSecret" type="password"' in html
    assert "autocomplete=\"new-password\"" in html
    assert "localStorage" not in html
    assert "OPENAI_API_KEY" not in html
    assert "GEMINI_API_KEY" not in html
    assert "OPENROUTER_API_KEY" not in html
    assert "Key stored in Vault. No redeploy required." in html


def test_openrouter_is_dormant_runtime_provider():
    service = SERVICE.read_text(encoding="utf-8")
    html = UI.read_text(encoding="utf-8")
    assert "https://openrouter.ai/api/v1/chat/completions" in service
    assert 'option value="openrouter"' in html
