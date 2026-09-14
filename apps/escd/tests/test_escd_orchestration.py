from contextlib import contextmanager
from http.server import HTTPServer
import json
from pathlib import Path
from threading import Thread
import time
from urllib import request, error
import pytest

from apps.escd.api.mvp import handler
from apps.escd.runtime.mvp_data import (
    create_orchestration_turn,
    get_orchestration_turn,
    update_orchestration_turn_action,
    ORCHESTRATION_TURNS,
)
from dcse.adapters import OllamaAdapter
from dcse.model import Operation

ROOT = Path(__file__).resolve().parents[1]
APP_HTML = ROOT / "web" / "app.html"
MVP_HTML = ROOT / "web" / "mvp.html"


class ESCDTestHandler(handler):
    def _auth(self):
        return object()

    def log_message(self, format, *args):
        pass


@contextmanager
def live_server():
    server = HTTPServer(("127.0.0.1", 0), ESCDTestHandler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        thread.join(timeout=5)


def test_escd_html_dual_lane_contract():
    for target in (APP_HTML, MVP_HTML):
        html = target.read_text(encoding="utf-8")
        assert '<option value="ollama">Ollama</option>' in html
        assert 'id="send"' in html
        assert 'id="orchestrate"' in html
        assert ">Orchestrate</button>" in html
        assert 'id="operationStrip"' in html
        assert 'id="stripTurn"' in html
        assert 'id="stripStage"' in html
        assert 'id="stripProvider"' in html
        assert 'id="stripWorker"' in html
        assert 'id="stripStatus"' in html
        assert 'id="stripStop"' in html
        assert 'id="stripContinue"' in html
        assert "$('orchestrate').onclick=orchestrate" in html
        assert "$('stripStop').onclick=stopTurn" in html
        assert "$('stripContinue').onclick=continueTurn" in html


def test_ollama_adapter_v72_contract():
    adapter = OllamaAdapter(base_url="http://127.0.0.1:99999", model="qwen2.5-coder:latest", worker="DCS-WINDOWS-OLLAMA-01")
    op = Operation(
        lane="DCSE",
        entity="task",
        action="evaluate",
        facts={"prompt": "Verify system health", "turn_id": "TURN-TEST-001", "allow_offline_sim": True},
    )
    result = adapter.perform(op)
    assert result["control"] == "RETURN_TO_ORCHESTRATOR"
    assert result["provider"] == "ollama"
    assert result["worker"] == "DCS-WINDOWS-OLLAMA-01"
    assert result["turn_id"] == "TURN-TEST-001"
    assert result["performed"] is True
    assert "payload" in result
    assert "evidence_refs" in result
    assert any("DCS-WINDOWS-OLLAMA-01" in ref for ref in result["evidence_refs"])


def test_http_providers_includes_ollama():
    with live_server() as base:
        with request.urlopen(base + "/api/mvp/providers", timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            providers = body["providers"]
            assert "ollama" in providers
            ollama = providers["ollama"]
            assert ollama["provider"] == "ollama"
            assert ollama["worker"] == "DCS-WINDOWS-OLLAMA-01"
            assert ollama["configured"] is True


def test_http_chat_conversational_lane_no_governed_turns():
    turn_count_before = len(ORCHESTRATION_TURNS)
    with live_server() as base:
        req = request.Request(
            base + "/api/mvp/chat",
            data=json.dumps({
                "provider": "ollama",
                "messages": [{"role": "user", "content": "What is the status of our systems?"}]
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            assert "response" in body
            assert "content" in body["response"]
            assert len(body["response"]["content"]) > 0

    turn_count_after = len(ORCHESTRATION_TURNS)
    assert turn_count_after == turn_count_before


def test_http_orchestrate_operational_lane_lifecycle():
    with live_server() as base:
        req = request.Request(
            base + "/api/mvp/orchestrate",
            data=json.dumps({
                "provider": "ollama",
                "prompt": "Evaluate candidate task schema",
                "context_refs": [{"role": "user", "content": "Evaluate candidate task schema"}]
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=10) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            assert "turn_id" in body
            turn_id = body["turn_id"]
            turn = body["turn"]
            assert turn["provider"] == "ollama"
            assert turn["worker"] == "DCS-WINDOWS-OLLAMA-01"
            assert turn["lane"] == "operational"

        # Poll turn state until terminal or timeout
        for _ in range(40):
            time.sleep(0.2)
            with request.urlopen(base + f"/api/mvp/orchestrate/turn/{turn_id}", timeout=5) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                assert resp.status == 200
                assert body["ok"] is True
                turn = body["turn"]
                if turn["status"] in ("COMPLETE", "WAITING_USER", "FAILED", "CANCELLED"):
                    break

        assert turn["turn_id"] == turn_id
        assert turn["status"] in ("COMPLETE", "WAITING_USER")
        assert len(turn["events"]) > 0


def test_http_orchestrate_stop_action():
    turn = create_orchestration_turn("ollama", "Inspect logs", [])
    turn_id = turn["turn_id"]
    turn["status"] = "WORKING"
    turn["stage"] = "EXECUTION"

    with live_server() as base:
        req = request.Request(
            base + f"/api/mvp/orchestrate/turn/{turn_id}/action",
            data=json.dumps({"action": "stop"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            assert body["turn"]["status"] == "CANCELLED"
            assert body["turn"]["stage"] == "TERMINATED"


def test_http_orchestrate_continue_action():
    turn = create_orchestration_turn("ollama", "Deploy candidate package", [])
    turn_id = turn["turn_id"]
    turn["status"] = "WAITING_USER"
    turn["stage"] = "PRECONDITION"

    with live_server() as base:
        req = request.Request(
            base + f"/api/mvp/orchestrate/turn/{turn_id}/action",
            data=json.dumps({"action": "continue", "response": "Approved by DCS"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with request.urlopen(req, timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            assert body["turn"]["status"] == "WORKING"

        for _ in range(25):
            time.sleep(0.2)
            with request.urlopen(base + f"/api/mvp/orchestrate/turn/{turn_id}", timeout=5) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                turn = body["turn"]
                if turn["status"] in ("COMPLETE", "FAILED"):
                    break

        assert turn["status"] == "COMPLETE"
        assert turn["stage"] == "RESPONSE"
        assert "Approved by DCS" in str(turn.get("response", {}).get("content", ""))
