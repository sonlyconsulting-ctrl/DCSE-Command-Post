import json
from unittest.mock import patch

import pytest

from apps.escd.runtime import mvp_data as data
from apps.escd.api.mvp import handler

ROOT_HTML = (data.Path(data.__file__).resolve().parents[1] / "web" / "mvp.html").read_text(encoding="utf-8")


def test_ollama_is_a_registry_provider_in_service_and_ui():
    assert "ollama" in data.PROVIDERS
    assert "'ollama'" in ROOT_HTML and 'option value="ollama"' in ROOT_HTML
    assert "OLLAMA_API_KEY" not in ROOT_HTML


def test_ollama_chat_routes_to_api_chat_with_bearer(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    cfg = {"provider": "ollama", "enabled": True, "model": "gpt-oss:120b", "api_key": "test-only-ollama-value", "timeout_seconds": 30, "max_output_tokens": 256}
    calls = []

    def fake_http(url, **kw):
        calls.append((url, kw))
        return 200, {"model": "gpt-oss:120b", "message": {"role": "assistant", "content": "hello"}}

    with patch.object(data, "provider_runtime", return_value=cfg), patch.object(data, "_http_json", side_effect=fake_http):
        out = data.chat("ollama", [{"role": "user", "content": "hi"}], conversation_id="conv_test_ollama")
    assert out["content"] == "hello" and out["provider"] == "ollama"
    url, kw = calls[0]
    assert url == "https://ollama.com/api/chat"
    assert kw["headers"]["Authorization"] == "Bearer test-only-ollama-value"
    assert kw["payload"]["stream"] is False


def test_ollama_cloud_without_key_is_not_configured(monkeypatch):
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)
    cfg = {"provider": "ollama", "enabled": True, "model": "m", "api_key": ""}
    with patch.object(data, "provider_runtime", return_value=cfg):
        with pytest.raises(data.MVPServiceError, match="credential is not configured"):
            data.chat("ollama", [{"role": "user", "content": "hi"}])


def test_ollama_base_url_must_be_https(monkeypatch):
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434")
    with pytest.raises(data.MVPServiceError, match="https"):
        data._ollama_base_url()


def test_merge_hides_canonical_rows_already_live():
    live = [{"id": "3f0b8f2c-1111-4222-8333-944455556666", "item_key": "CANON-001", "title": "live"}]
    canonical = [{"id": "CANON-001", "title": "dup"}, {"id": "CANON-002", "title": "only canonical"}]
    merged = data.merge_live_and_canonical(live, canonical, ("item_key",))
    assert [m["title"] for m in merged] == ["live", "only canonical"]
    assert merged[1]["record_origin"] == "canonical_registry"


def test_asset_listing_excludes_ps_lane(monkeypatch):
    rows = [{"asset_id": "A1", "entity_lane": "PS", "firewall_security_tag": "PS-Locked"}, {"asset_id": "A2", "entity_lane": "DCSE", "firewall_security_tag": "DCSE-Confidential"}]
    captured = {}

    def fake_http(url, **kw):
        captured["url"] = url
        return 200, rows

    monkeypatch.setattr(data, "_service_config", lambda: ("https://nevgdyfpxdaloacuutal.supabase.co", "k"))
    with patch.object(data, "_http_json", side_effect=fake_http):
        out = data.list_assets()
    assert "firewall_security_tag=neq.PS-Locked" in captured["url"]
    assert "A1" not in {r.get("asset_id") for r in out}


@pytest.mark.parametrize("payload", [{"entity_lane": "PS"}, {"firewall_security_tag": "PS-Locked"}])
def test_asset_writes_reject_protected_lane(payload):
    base = {"file_name": "f", "asset_type": "t", "topic": "x", "description": "d", "storage_location": "s", "entity_lane": "DCSE", "firewall_security_tag": "DCSE-Confidential"}
    base.update(payload)
    with pytest.raises(data.MVPServiceError, match="protected"):
        data._asset_fields(base, creating=True)


def test_asset_update_refuses_existing_ps_record():
    with patch.object(data, "get_asset", return_value={"asset_id": "A1", "entity_lane": "PS", "firewall_security_tag": "PS-Locked"}):
        with pytest.raises(data.MVPServiceError, match="protected_lane_record"):
            data.update_asset("A1", {"notes": "x"})


def test_new_asset_hash_is_marked_unverified():
    sent = {}

    def fake_req(method, query, payload=None):
        if method == "GET":
            return []
        sent.update(payload)
        return [payload]

    with patch.object(data, "_asset_request", side_effect=fake_req):
        data.create_asset({"file_name": "f.md", "asset_type": "Doc", "topic": "t", "description": "d", "storage_location": "repo/f.md", "entity_lane": "SC", "firewall_security_tag": "SC-Internal"})
    assert sent["sha256"] == "UNVERIFIED" and sent["hash_verified"] is False
    assert sent["asset_id"].startswith("ESCD-ASSET-")


def test_knowledge_validation():
    with pytest.raises(data.MVPServiceError):
        data._knowledge_update({"status": "deleted"})
    with pytest.raises(data.MVPServiceError):
        data._knowledge_update({"confidence": 2})
    assert data._knowledge_update({"title": " T ", "confidence": "0.4"}) == {"title": "T", "confidence": 0.4}


class FakeRepo:
    def __init__(self):
        self.created, self.patched = [], []

    def get_knowledge_by_key(self, key):
        return None

    def create_knowledge(self, payload):
        self.created.append(payload)
        return dict(payload, id="3f0b8f2c-1111-4222-8333-944455556666")

    def patch_knowledge(self, rid, update):
        self.patched.append((rid, update))
        return dict(update, id=rid)


def test_editing_canonical_knowledge_adopts_then_patches():
    canonical = data.get_canonical_convergence_items()["knowledge"][0]
    repo = FakeRepo()
    data.update_knowledge(repo, canonical["id"], {"title": "Edited"})
    assert repo.created[0]["knowledge_key"] == canonical["id"]
    assert repo.created[0]["authority_classification"] in data.KNOWLEDGE_AUTHORITY
    assert repo.patched == [("3f0b8f2c-1111-4222-8333-944455556666", {"title": "Edited"})]


def _request(method, path, body=None):
    req = object.__new__(handler)
    req.path = path
    req.headers = {}
    req._read_json = lambda: body or {}
    out = []
    req._json = lambda code, payload: out.append((code, payload))
    getattr(req, "do_" + method)()
    return out[0]


@pytest.mark.parametrize("method,path", [("DELETE", "/api/mvp/items?id=x"), ("DELETE", "/api/mvp/assets?id=x"), ("POST", "/api/mvp/assets"), ("PATCH", "/api/mvp/knowledge"), ("POST", "/api/mvp/knowledge")])
def test_crud_routes_require_authentication(method, path):
    with patch("apps.escd.api.mvp.update_asset") as ua, patch("apps.escd.api.mvp.create_asset") as ca, patch("apps.escd.api.mvp.update_knowledge") as uk:
        code, _ = _request(method, path, {"id": "x", "title": "t"})
        ua.assert_not_called(); ca.assert_not_called(); uk.assert_not_called()
    assert code == 401


def test_delete_is_archive_not_hard_delete():
    api = (data.Path(data.__file__).resolve().parents[1] / "api" / "mvp.py").read_text(encoding="utf-8")
    assert '"DELETE"' not in api
    assert '{"status": "archived"}' in api and '{"lifecycle_status": "Retired"}' in api


def test_claude_chat_uses_messages_api_with_alternating_turns():
    cfg = {"provider": "anthropic", "enabled": True, "model": "claude-sonnet-5", "api_key": "sk-ant-test-only-value", "timeout_seconds": 30, "max_output_tokens": 256}
    calls = []

    def fake_http(url, **kw):
        calls.append((url, kw))
        return 200, {"model": "claude-sonnet-5", "content": [{"type": "text", "text": "hi from claude"}]}

    with patch.object(data, "provider_runtime", return_value=cfg), patch.object(data, "_http_json", side_effect=fake_http):
        out = data.chat("anthropic", [{"role": "user", "content": "hello"}], conversation_id="conv_test_claude")
    url, kw = calls[0]
    assert url == "https://api.anthropic.com/v1/messages"
    assert kw["headers"]["x-api-key"] == "sk-ant-test-only-value" and kw["headers"]["anthropic-version"] == "2023-06-01"
    msgs = kw["payload"]["messages"]
    assert msgs[0]["role"] == "user"
    assert all(msgs[i]["role"] != msgs[i + 1]["role"] for i in range(len(msgs) - 1))
    assert all(m["role"] in ("user", "assistant") for m in msgs)
    assert out["content"] == "hi from claude" and out["provider"] == "anthropic"
    assert "anthropic" in data.PROVIDERS and 'option value="anthropic"' in ROOT_HTML


def test_claude_key_is_redacted_in_errors():
    assert "sk-ant-***" in data._safe_provider_detail("bad key sk-ant-api03-abcdefghijklmnop")
    assert "abcdefghijklmnop" not in data._safe_provider_detail("bad key sk-ant-api03-abcdefghijklmnop")


def test_chat_tells_the_engine_which_provider_and_model_answered():
    cfg = {"provider": "openai", "enabled": True, "model": "gpt-test", "api_key": "k-test-only-000", "timeout_seconds": 30, "max_output_tokens": 64}
    calls = []
    with patch.object(data, "provider_runtime", return_value=cfg), patch.object(data, "_http_json", side_effect=lambda url, **kw: calls.append(kw) or (200, {"output_text": "ok"})):
        data.chat("openai", [{"role": "user", "content": "who answered?"}], conversation_id="conv_test_engine")
    sent = json.dumps(calls[0]["payload"])
    assert "Current execution engine for this reply: OpenAI (gpt-test)" in sent
