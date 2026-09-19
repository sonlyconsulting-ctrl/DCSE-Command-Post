import json
from unittest.mock import patch
from urllib.parse import unquote

import pytest

from apps.escd.runtime import mvp_data as data
from apps.escd.api.mvp import handler

REGISTRY = [
    {"agent_key": "antigravity", "status": "active", "agent_type": "code_agent", "metadata": {"expected_runtime_surface": "agy_windows_cli"}},
    {"agent_key": "chatgpt", "status": "active", "agent_type": "model", "metadata": {}},
    {"agent_key": "dcs_authority", "status": "active", "agent_type": "dcs_authority", "metadata": {}},
]
U1 = "11111111-1111-4111-8111-111111111111"
U2 = "22222222-2222-4222-8222-222222222222"
C1 = "33333333-3333-4333-8333-333333333333"


@pytest.fixture(autouse=True)
def service(monkeypatch):
    monkeypatch.setattr(data, "_service_config", lambda: ("https://nevgdyfpxdaloacuutal.supabase.co", "k"))


def test_agents_list_excludes_dcs_and_marks_delivery_mode():
    with patch.object(data, "_http_json", return_value=(200, REGISTRY)) as h:
        agents = data.orchestrator_agents()
    assert "status=in.(active,standby)" in h.call_args.args[0]
    assert [a["agent_key"] for a in agents] == ["antigravity", "chatgpt"]
    assert agents[0]["delivery_mode"] == "push" and agents[1]["delivery_mode"] == "pull"


def test_send_uses_dcs_identity_one_thread_and_is_communication_only():
    calls = []
    with patch.object(data, "orchestrator_agents", return_value=[{"agent_key": "antigravity"}, {"agent_key": "chatgpt"}]), \
         patch.object(data, "_rpc", side_effect=lambda name, p: calls.append((name, p)) or U1):
        out = data.orchestrator_send(["antigravity", "chatgpt", "antigravity"], " Hi ", "Body", {"kind": "task", "id": U2, "title": "T"}, "sc@example.com")
    assert len(calls) == 2 and len(out["sent"]) == 2
    corr = {p["p_correlation_id"] for _, p in calls}
    assert corr == {out["correlation_id"]}
    for name, p in calls:
        assert name == "send_agent_message"
        assert p["p_sender"] == "dcs_authority" and p["p_message_class"] == "communication"
        assert p["p_subject"] == "Hi"
        assert p["p_metadata"]["record"]["id"] == U2 and p["p_metadata"]["expects_reply"] is True
        assert "execution_authorized" not in json.dumps(p)


@pytest.mark.parametrize("recipients,subject,body,err", [([], "s", "b", "recipient_required"), (["nobody"], "s", "b", "unknown_or_inactive_agent"), (["chatgpt"], "", "b", "subject_required"), (["chatgpt"], "s", "x" * 20001, "body_too_long")])
def test_send_validation(recipients, subject, body, err):
    with patch.object(data, "orchestrator_agents", return_value=[{"agent_key": "chatgpt"}]), patch.object(data, "_rpc") as rpc:
        with pytest.raises(data.MVPServiceError, match=err):
            data.orchestrator_send(recipients, subject, body)
        rpc.assert_not_called()


def _router(messages, health=None):
    def fake(url, **kw):
        u = unquote(url)
        if "rpc/read_agent_messages" in u:
            assert kw["payload"]["p_agent_key"] == "dcs_authority"
            return 200, [{"id": U2}]
        if "agent_message_delivery_status" in u:
            return 200, health or []
        if "agent_messages?" in u:
            return 200, messages
        raise AssertionError(u)
    return fake


def test_threads_group_messages_and_flag_new():
    msgs = [
        {"id": U1, "correlation_id": C1, "sender": "dcs_authority", "recipient_agent_key": "antigravity", "subject": "S", "body": "q", "message_class": "communication", "status": "ACKNOWLEDGED", "receipt": {"receipt_type": "worker_delivery_receipt"}, "metadata": {"record": {"kind": "task", "id": "x"}}, "created_at": "2026-09-17T06:00:00+00:00"},
        {"id": U2, "correlation_id": C1, "reply_to": U1, "sender": "antigravity", "recipient_agent_key": "dcs_authority", "subject": "RE: S", "body": "a", "message_class": "reply", "status": "ACKNOWLEDGED", "receipt": {"receipt_type": "reader_pull_receipt"}, "metadata": {}, "created_at": "2026-09-17T06:01:00+00:00"},
    ]
    with patch.object(data, "_http_json", side_effect=_router(msgs, [{"id": U1, "delivery_health": "DELIVERED"}])):
        out = data.orchestrator_threads()
    assert out["new_count"] == 1
    t = out["threads"][0]
    assert t["correlation_id"] == C1 and t["new_count"] == 1 and t["record"]["kind"] == "task"
    assert [m["incoming"] for m in t["messages"]] == [False, True]
    assert t["messages"][0]["receipt_type"] == "worker_delivery_receipt" and t["messages"][0]["delivery_health"] == "DELIVERED"
    assert "receipt" not in t["messages"][0]


def test_reply_goes_to_original_sender_in_same_thread():
    orig = [{"id": U2, "sender": "antigravity", "recipient_agent_key": "dcs_authority", "subject": "Status", "correlation_id": C1}]
    sent = []
    with patch.object(data, "_http_json", return_value=(200, orig)), patch.object(data, "_rpc", side_effect=lambda n, p: sent.append(p) or U1):
        out = data.orchestrator_reply(U2, "thanks")
    p = sent[0]
    assert p["p_recipient_agent_key"] == "antigravity" and p["p_reply_to"] == U2 and p["p_correlation_id"] == C1
    assert p["p_subject"] == "RE: Status" and out["mode"] == "reply"


def test_reply_to_ineligible_message_becomes_follow_up():
    orig = [{"id": U2, "sender": "chatgpt", "recipient_agent_key": "dcs_authority", "subject": "RE: x", "correlation_id": C1}]
    sent = []

    def rpc(name, p):
        sent.append(dict(p))
        if len(sent) == 1:
            raise data.ProviderHTTPError(400, "REPLY_NOT_ELIGIBLE: message is a reply")
        return U1

    with patch.object(data, "_http_json", return_value=(200, orig)), patch.object(data, "_rpc", side_effect=rpc):
        out = data.orchestrator_reply(U2, "more")
    assert out["mode"] == "follow_up"
    assert sent[1]["p_reply_to"] is None and sent[1]["p_message_class"] == "communication"
    assert sent[1]["p_correlation_id"] == C1 and sent[1]["p_metadata"]["follow_up_of"] == U2


def test_reply_refuses_messages_not_addressed_to_dcs():
    orig = [{"id": U2, "sender": "dcs_authority", "recipient_agent_key": "chatgpt", "subject": "x", "correlation_id": C1}]
    with patch.object(data, "_http_json", return_value=(200, orig)), patch.object(data, "_rpc") as rpc:
        with pytest.raises(data.MVPServiceError, match="addressed_to_dcs"):
            data.orchestrator_reply(U2, "x")
        rpc.assert_not_called()


def _request(method, path, body=None):
    req = object.__new__(handler)
    req.path = path
    req.headers = {}
    req._read_json = lambda: body or {}
    out = []
    req._json = lambda code, payload: out.append((code, payload))
    getattr(req, "do_" + method)()
    return out[0]


@pytest.mark.parametrize("method,path", [("GET", "/api/mvp/orchestrator/threads"), ("GET", "/api/mvp/orchestrator/agents"), ("POST", "/api/mvp/orchestrator/send"), ("POST", "/api/mvp/orchestrator/reply")])
def test_orchestrator_routes_require_authentication(method, path):
    with patch("apps.escd.api.mvp.orchestrator_send") as s, patch("apps.escd.api.mvp.orchestrator_reply") as r, patch("apps.escd.api.mvp.orchestrator_threads") as t:
        code, _ = _request(method, path, {"recipients": ["chatgpt"], "subject": "s", "body": "b"})
        s.assert_not_called(); r.assert_not_called(); t.assert_not_called()
    assert code == 401
