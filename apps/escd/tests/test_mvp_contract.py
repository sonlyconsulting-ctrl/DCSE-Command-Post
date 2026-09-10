from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "web" / "app.html"
LOGIN = ROOT / "web" / "login.html"


def test_mvp_surface_is_real_data_only():
    html = APP.read_text(encoding="utf-8")
    for label in ("Chat", "Tasks", "Ideas", "Assets", "DDNA"):
        assert label in html
    assert "73 Queued" not in html
    assert "placeholder data" not in html.lower()


def test_mvp_has_responsive_breakpoints():
    html = APP.read_text(encoding="utf-8")
    assert "@media(max-width:820px)" in html
    assert "@media(max-width:520px)" in html
    assert 'id="bottom"' in html


def test_mvp_uses_normal_sign_in_not_token_prompt():
    login = LOGIN.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    assert 'type="email"' in login
    assert 'type="password"' in login
    assert "/api/mvp/login" in login
    assert "Preview access token" not in app
    assert "prompt('ESCD Preview access token')" not in app


def test_mvp_api_keeps_provider_keys_server_side():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    browser = APP.read_text(encoding="utf-8") + LOGIN.read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" in service
    assert "GEMINI_API_KEY" in service
    assert "OPENAI_API_KEY" not in browser
    assert "GEMINI_API_KEY" not in browser
    assert "apiKey" not in browser


def test_mvp_api_reads_live_sources():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    assert "dcse_asset_registry" in service
    assert "last_modified_at.desc" in service
    assert "ddna_source_queue" in service
    assert "DDNA_SUPABASE_URL" in service
    assert "DDNA_SUPABASE_SERVICE_ROLE_KEY" in service


def test_mvp_chat_excludes_claude():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    assert "anthropic" not in service.lower()
    assert "claude" not in service.lower()
    assert "claude" not in app.lower()


def test_mvp_provider_defaults_are_current_and_errors_are_provider_specific():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    assert '"gpt-5.6-sol"' in service
    assert '"gemini-3.8-flash"' in service
    assert '"x-goog-api-key"' in service
    assert '"https://api.openai.com/v1/responses"' in service
    assert 'f"{provider}_auth_failed"' in service
    assert 'f"{provider}_model_or_endpoint_not_found"' in service


def test_mvp_routes_to_operable_surface():
    routes = (ROOT / "vercel.json").read_text(encoding="utf-8")
    assert '"src":"/app","dest":"/web/app.html"' in routes
    assert '"src":"/","dest":"/web/login.html"' in routes
