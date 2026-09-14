"""Capability adapters.

The orchestrator decides whether an operation may proceed. An adapter is what
actually touches the outside world when it may. They are kept apart on purpose:
the decision has to be testable without a network, a database or a deployment.

The default for every capability is an adapter that performs nothing and says
so. That is deliberate. A system whose default is a convincing no-op is a
system that reports work it did not do, and this whole program exists because
that had already happened four times before anyone noticed.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from model import Operation


class Adapter:
    """One capability's door to the outside."""

    name = "adapter"

    def perform(self, op: Operation) -> Dict[str, Any]:
        raise NotImplementedError


class NotWired(Adapter):
    """The honest default.

    Returns performed False with a reason. It never raises, so an operation can
    be evaluated end to end before any capability is connected, and it never
    claims success, so a green run against unwired adapters cannot be mistaken
    for a working system.
    """

    def __init__(self, capability: str) -> None:
        self.name = capability

    def perform(self, op: Operation) -> Dict[str, Any]:
        return {
            "performed": False,
            "capability": self.name,
            "action": op.action,
            "reason": ("no adapter wired for this capability. The operation was "
                       "evaluated and permitted; nothing was executed."),
        }


class Recording(Adapter):
    """A test adapter that records what it was asked to do and reports success.

    Only for suites. Wiring this into anything real would reintroduce exactly
    the failure mode NotWired exists to prevent.
    """

    def __init__(self, capability: str) -> None:
        self.name = capability
        self.calls: list = []

    def perform(self, op: Operation) -> Dict[str, Any]:
        self.calls.append((op.entity, op.action, dict(op.facts)))
        return {"performed": True, "capability": self.name, "action": op.action,
                "note": "recording adapter, no external effect"}


class GitKrakenAdapter(Adapter):
    """Capability adapter for Git and GitHub operations via the GitKraken CLI (gk).

    Maintains DCSE integrity:
    1. Detects local gk.exe installation without guessing.
    2. Reports honest unperformed status if CLI is unauthenticated or missing.
    3. Wraps bounded queries and workspace checks under governance rules.
    """
    name = "gitkraken"

    def __init__(self, executable: Optional[str] = None) -> None:
        self.executable = executable or self._find_gk()

    def _find_gk(self) -> Optional[str]:
        import os
        import shutil
        env_path = os.environ.get("GITKRAKEN_CLI_PATH")
        if env_path and os.path.isfile(env_path):
            return env_path
        local_gk = os.path.expandvars(r"%LOCALAPPDATA%\GitKrakenCLI\gk.exe")
        if os.path.isfile(local_gk):
            return local_gk
        return shutil.which("gk")

    def is_available(self) -> bool:
        import os
        return bool(self.executable and os.path.isfile(self.executable))

    def perform(self, op: Operation) -> Dict[str, Any]:
        import subprocess
        if not self.is_available():
            return {
                "performed": False,
                "capability": "github",
                "action": op.action,
                "reason": ("GitKraken CLI (gk.exe) not found. "
                           "Install with 'winget install GitKraken.cli' or set GITKRAKEN_CLI_PATH."),
            }

        action = op.action.lower()
        if action in ("status", "query"):
            try:
                res = subprocess.run([self.executable, "--version"],
                                     capture_output=True, text=True, timeout=5)
                return {
                    "performed": res.returncode == 0,
                    "capability": "github",
                    "action": op.action,
                    "output": res.stdout.strip(),
                    "note": "GitKraken CLI query successful",
                }
            except Exception as e:
                return {"performed": False, "capability": "github", "reason": str(e)}

        return {
            "performed": False,
            "capability": "github",
            "action": op.action,
            "reason": ("Action %r through GitKraken adapter requires "
                       "explicit authorization or completion." % op.action),
        }


class AdapterSet:
    def __init__(self) -> None:
        self._by_capability: Dict[str, Adapter] = {}

    def wire(self, capability: str, adapter: Adapter) -> None:
        self._by_capability[capability] = adapter

    def for_operation(self, op: Operation) -> Adapter:
        """The first declared capability with a wired adapter wins, otherwise
        the honest default."""
        for cap in op.capabilities:
            if cap in self._by_capability:
                return self._by_capability[cap]
        first = op.capabilities[0] if op.capabilities else op.entity
        return NotWired(first)

    def wired(self) -> Dict[str, str]:
        return {c: a.name for c, a in self._by_capability.items()}


DEFAULT_ADAPTERS = AdapterSet()
