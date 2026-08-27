"""Fail-closed Fable/Claude adapter placeholder for Tribunal Poller v7.

An interactive Cowork session is not a headless worker. This adapter performs
no execution until a separate DCS-approved noninteractive contract is added and
validated on this host.
"""
from __future__ import annotations

import shutil
from typing import Any

from tribunal_v7_state_machine import TaskSpec


def fable_status() -> dict[str, Any]:
    return {
        "status": "PENDING_CLAUDE_CODE_INSTALL_OR_APPROVED_API_ADAPTER",
        "claude_cli_visible": shutil.which("claude") is not None,
        "headless_exchange_enabled": False,
        "reason": (
            "No verified, DCS-approved headless Claude/Fable invocation and "
            "receipt contract is installed. Interactive Cowork access does not satisfy it."
        ),
    }


def run_fable(spec: TaskSpec) -> dict[str, Any]:
    status = fable_status()
    return {
        "adapter_status": status["status"],
        "task_id": spec.task_id,
        "source_sha256": spec.source_sha256,
        "status": "FAILED",
        "summary": status["reason"],
        "outputs": [],
        "details": status,
    }
