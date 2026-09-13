from __future__ import annotations

from urllib.parse import parse_qs, unquote, urlencode, urlparse

from apps.escd.api.mvp import handler as MVPHandler


class handler(MVPHandler):
    """Vercel root entrypoint for the ESCD minimal MVP candidate.

    Root Vercel rewrites preserve the original MVP subpath in the mvp_path
    query parameter. Restore it before dispatching to the governed MVP
    handler. Authentication and authorization remain implemented by the MVP
    handler and existing ESCD runtime boundary.
    """

    def _restore_mvp_path(self) -> None:
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        preserved = str((params.get("mvp_path") or [""])[0]).strip()
        if not preserved:
            return
        route = unquote(preserved).lstrip("/")
        remaining = [(k, v) for k, values in params.items() if k != "mvp_path" for v in values]
        suffix = "?" + urlencode(remaining) if remaining else ""
        self.path = "/api/mvp/" + route + suffix

    def do_GET(self):
        self._restore_mvp_path()
        return super().do_GET()

    def do_POST(self):
        self._restore_mvp_path()
        return super().do_POST()

    def do_PATCH(self):
        self._restore_mvp_path()
        return super().do_PATCH()

    def do_PUT(self):
        self._restore_mvp_path()
        return super().do_PUT()

    def do_DELETE(self):
        self._restore_mvp_path()
        return super().do_DELETE()
