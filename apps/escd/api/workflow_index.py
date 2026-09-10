from __future__ import annotations

import json
from urllib.parse import urlparse

from apps.escd.api.index import handler as BaseESCDHandler
from apps.escd.runtime.auth import AuthError
from apps.escd.runtime.repository import RepositoryError
from apps.escd.runtime.workflow_api import dispatch_get, dispatch_post, handles


class handler(BaseESCDHandler):
    """ESCD handler with the WORKFLOW-004 routes layered over the validated base runtime."""

    server_version = "ESCD/0.5"

    def do_GET(self):
        path = urlparse(self.path).path
        if not handles("GET", path):
            return super().do_GET()

        origin = self._origin()
        try:
            _, repo = self._authorized()
            status, payload = dispatch_get(repo, self.path)
            self._json(status, payload, origin)
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)}, origin)
        except RepositoryError as exc:
            self._json(502, {"error": str(exc)}, origin)
        except (ValueError, TypeError) as exc:
            self._json(400, {"error": str(exc)}, origin)
        except Exception:
            self._json(500, {"error": "internal_error"}, origin)

    def do_POST(self):
        path = urlparse(self.path).path
        if not handles("POST", path):
            return super().do_POST()

        origin = self._origin()
        try:
            _, repo = self._authorized()
            payload = self._read_json()
            status, response = dispatch_post(repo, path, payload)
            self._json(status, response, origin)
        except AuthError as exc:
            self._json(401 if str(exc) != "dcs_operator_not_authorized" else 403, {"error": str(exc)}, origin)
        except RepositoryError as exc:
            self._json(502, {"error": str(exc)}, origin)
        except json.JSONDecodeError:
            self._json(400, {"error": "invalid_json"}, origin)
        except (ValueError, TypeError) as exc:
            self._json(400, {"error": str(exc)}, origin)
        except Exception:
            self._json(500, {"error": "internal_error"}, origin)
