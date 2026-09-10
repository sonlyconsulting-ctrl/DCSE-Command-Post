from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlparse

from apps.escd.api.workflow_index import handler as WorkflowESCDHandler


class handler(WorkflowESCDHandler):
    """Vercel entrypoint for ESCD candidate runtime.

    A specific rewrite may preserve the ESCD subpath in the `escd_path` query
    parameter. Reconstruct it before the governed handler dispatches. No
    authentication or authorization behavior is changed here.
    """

    def _restore_escd_path(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        preserved = str((params.get("escd_path") or [""])[0]).strip()
        if not preserved:
            return
        route = unquote(preserved).lstrip("/")
        remaining = [(k, v) for k, values in params.items() if k != "escd_path" for v in values]
        suffix = ""
        if remaining:
            from urllib.parse import urlencode
            suffix = "?" + urlencode(remaining)
        self.path = "/api/escd/" + route + suffix

    def do_GET(self):
        self._restore_escd_path()
        return super().do_GET()

    def do_POST(self):
        self._restore_escd_path()
        return super().do_POST()
