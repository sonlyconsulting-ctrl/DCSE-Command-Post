from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGIN = ROOT / "web" / "login.html"
MVP = ROOT / "web" / "mvp.html"


def test_login_page_has_google_oauth_and_hash_handling():
    html = LOGIN.read_text(encoding="utf-8")
    assert "Sign in with Google" in html
    assert 'id="googleBtn"' in html
    assert "provider=google" in html
    assert "access_token" in html
    assert "handleOAuthHash" in html


def test_login_page_retains_governed_email_password_fallback():
    html = LOGIN.read_text(encoding="utf-8")
    assert 'type="email"' in html
    assert 'type="password"' in html
    assert "/api/mvp/login" in html
    assert "DCSE v7.2" in html


def test_mvp_page_has_multimodal_composer_and_selectors():
    html = MVP.read_text(encoding="utf-8")
    assert 'id="selRuntime"' in html
    assert 'id="selCapability"' in html
    assert "Claude Pro" in html
    assert 'id="filePicker"' in html
    assert 'id="cameraPicker"' in html
    assert 'id="micBtn"' in html
    assert 'id="sendBtn"' in html


def test_mvp_page_has_voice_input_and_response_controls():
    html = MVP.read_text(encoding="utf-8")
    assert "SpeechRecognition" in html
    assert "speechSynthesis" in html
    assert "voice-listening-banner" in html
    assert 'id="voiceDialog"' in html


def test_mvp_page_has_direct_storage_upload_sha():
    html = MVP.read_text(encoding="utf-8")
    assert "crypto.subtle.digest" in html
    assert "SHA-256" in html
    assert 'id="uploadBox"' in html
    assert "upload-progress-box" in html


def test_mvp_page_has_mobile_bottom_nav_and_pwa():
    html = MVP.read_text(encoding="utf-8")
    assert "mobile-bottom-nav" in html
    assert 'rel="manifest"' in html


def test_mvp_page_has_actionable_dashboard_sections():
    html = MVP.read_text(encoding="utf-8")
    assert "NOW — Active Orchestration" in html
    assert "Intelligence Runtimes" in html
    assert "Active Work" in html
    assert "Governance & Evidence" in html
