from contextlib import contextmanager
from http.server import HTTPServer
from threading import Thread
from urllib import request, error
import json

from apps.escd.api.mvp import handler


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


def test_http_knowledge_contract():
    with live_server() as base:
        with request.urlopen(base + "/api/mvp/knowledge", timeout=5) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            assert resp.status == 200
            assert body["ok"] is True
            assert len(body["knowledge"]) == 24


def test_http_malformed_json_returns_400():
    with live_server() as base:
        req = request.Request(
            base + "/api/mvp/login",
            data=b"{invalid json!}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            request.urlopen(req, timeout=5)
            raise AssertionError("Expected HTTP 400")
        except error.HTTPError as exc:
            assert exc.code == 400
            body = json.loads(exc.read().decode("utf-8"))
            assert body["error"] == "invalid_json"


def test_http_legacy_upload_route_is_closed():
    with live_server() as base:
        req = request.Request(
            base + "/api/mvp/upload",
            data=json.dumps({"name": "x.txt"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            request.urlopen(req, timeout=5)
            raise AssertionError("Expected HTTP 410")
        except error.HTTPError as exc:
            assert exc.code == 410
            body = json.loads(exc.read().decode("utf-8"))
            assert body["error"] == "direct_upload_required"
