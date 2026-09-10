from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_mvp_surface_is_real_data_only():
    html = (ROOT / "web" / "mvp.html").read_text(encoding="utf-8")
    assert "Chat" in html
    assert "Tasks" in html
    assert "Ideas" in html
    assert "Assets" in html
    assert "DDNA" in html
    assert "73 Queued" not in html
    assert "placeholder data" not in html.lower()


def test_mvp_has_responsive_breakpoints():
    html = (ROOT / "web" / "mvp.html").read_text(encoding="utf-8")
    assert "@media(max-width:820px)" in html
    assert "@media(max-width:520px)" in html
    assert "mobile-nav" in html


def test_mvp_api_keeps_provider_keys_server_side():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    page = (ROOT / "web" / "mvp.html").read_text(encoding="utf-8")
    assert "OPENAI_API_KEY" in service
    assert "GEMINI_API_KEY" in service
    assert "OPENAI_API_KEY" not in page
    assert "GEMINI_API_KEY" not in page
    assert "apiKey" not in page


def test_mvp_api_reads_live_sources():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    assert "dcse_asset_registry" in service
    assert "ddna_source_queue" in service
    assert "DDNA_SUPABASE_URL" in service
    assert "DDNA_SUPABASE_SERVICE_ROLE_KEY" in service


def test_mvp_chat_excludes_claude():
    service = (ROOT / "runtime" / "mvp_data.py").read_text(encoding="utf-8")
    assert "anthropic" not in service.lower()
    assert "claude" not in service.lower()
