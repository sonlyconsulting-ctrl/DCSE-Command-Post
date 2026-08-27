"""Governed state and receipt primitives for the DCSE Tribunal Poller v7.

This module never moves, renames, deletes, stages, commits, pushes, or edits a
Tribunal source packet. Its only write primitive is an atomic JSON receipt.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Iterable

RECEIPT_SCHEMA_VERSION = "tribunal-poller-v7-receipt/1.0"
TASK_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")


class PollerState(str, Enum):
    RECEIVED = "RECEIVED"
    VALIDATED = "VALIDATED"
    AUTHORIZED = "AUTHORIZED"
    DISPATCHED = "DISPATCHED"
    VERIFYING = "VERIFYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    QUARANTINE_PENDING = "QUARANTINE_PENDING"


TERMINAL_STATES = {
    PollerState.COMPLETED,
    PollerState.FAILED,
    PollerState.QUARANTINE_PENDING,
}

ALLOWED_TRANSITIONS: dict[PollerState, set[PollerState]] = {
    PollerState.RECEIVED: {
        PollerState.VALIDATED,
        PollerState.FAILED,
        PollerState.QUARANTINE_PENDING,
    },
    PollerState.VALIDATED: {
        PollerState.AUTHORIZED,
        PollerState.FAILED,
        PollerState.QUARANTINE_PENDING,
    },
    PollerState.AUTHORIZED: {
        PollerState.DISPATCHED,
        PollerState.FAILED,
    },
    PollerState.DISPATCHED: {
        PollerState.VERIFYING,
        PollerState.FAILED,
    },
    PollerState.VERIFYING: {
        PollerState.COMPLETED,
        PollerState.FAILED,
        PollerState.QUARANTINE_PENDING,
    },
    PollerState.COMPLETED: set(),
    PollerState.FAILED: set(),
    PollerState.QUARANTINE_PENDING: set(),
}


class GovernanceError(ValueError):
    """The packet is not eligible for unattended execution."""


class VerificationError(RuntimeError):
    """A worker returned a result that cannot be trusted."""


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def is_within(path: Path, roots: Iterable[Path]) -> bool:
    candidate = path.resolve()
    for root in roots:
        try:
            candidate.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temporary.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


@dataclass(frozen=True)
class TaskSpec:
    task_id: str
    worker: str
    prompt: str
    working_directory: Path
    sandbox: str
    timeout_seconds: int
    expected_outputs: tuple[str, ...]
    approved_by: str
    approved_at: str
    source_file: Path
    source_sha256: str

    @classmethod
    def from_packet(
        cls,
        packet: dict[str, Any],
        source_file: Path,
        source_sha256: str,
        allowed_roots: Iterable[Path],
    ) -> "TaskSpec":
        block = packet.get("POLLER_V7")
        if not isinstance(block, dict):
            raise GovernanceError("POLLER_V7 object is required")

        task_id = str(block.get("task_id", "")).strip()
        if not TASK_ID_PATTERN.fullmatch(task_id):
            raise GovernanceError("POLLER_V7.task_id is missing or invalid")

        worker = str(block.get("worker", "")).strip().lower()
        if worker not in {"codex", "fable"}:
            raise GovernanceError("POLLER_V7.worker must be codex or fable")

        prompt = str(block.get("prompt", "")).strip()
        if len(prompt) < 20:
            raise GovernanceError("POLLER_V7.prompt must contain a bounded task")

        working_directory = Path(str(block.get("working_directory", ""))).expanduser()
        if not working_directory.is_absolute() or not working_directory.is_dir():
            raise GovernanceError("working_directory must be an existing absolute directory")
        if not is_within(working_directory, allowed_roots):
            raise GovernanceError("working_directory is outside the configured allow roots")

        sandbox = str(block.get("sandbox", "read-only")).strip().lower()
        if sandbox not in {"read-only", "workspace-write"}:
            raise GovernanceError("sandbox must be read-only or workspace-write")

        try:
            timeout_seconds = int(block.get("timeout_seconds", 900))
        except (TypeError, ValueError) as exc:
            raise GovernanceError("timeout_seconds must be an integer") from exc
        if not 30 <= timeout_seconds <= 3600:
            raise GovernanceError("timeout_seconds must be between 30 and 3600")

        raw_outputs = block.get("expected_outputs", [])
        if not isinstance(raw_outputs, list):
            raise GovernanceError("expected_outputs must be an array")
        expected_outputs: list[str] = []
        for raw in raw_outputs:
            relative = Path(str(raw))
            if relative.is_absolute() or ".." in relative.parts:
                raise GovernanceError("expected_outputs must be relative to working_directory")
            normalized = relative.as_posix()
            if not normalized or normalized == ".":
                raise GovernanceError("expected_outputs contains an empty path")
            resolved = (working_directory / relative).resolve()
            if not is_within(resolved, [working_directory]):
                raise GovernanceError("expected output escapes working_directory")
            expected_outputs.append(normalized)

        authorization = block.get("authorization")
        if not isinstance(authorization, dict):
            raise GovernanceError("POLLER_V7.authorization object is required")
        if str(authorization.get("decision", "")).strip().upper() != "GO":
            raise GovernanceError("authorization.decision must be GO")
        approved_by = str(authorization.get("approved_by", "")).strip()
        approved_at = str(authorization.get("approved_at", "")).strip()
        if not approved_by or not approved_at:
            raise GovernanceError("authorization requires approved_by and approved_at")

        return cls(
            task_id=task_id,
            worker=worker,
            prompt=prompt,
            working_directory=working_directory.resolve(),
            sandbox=sandbox,
            timeout_seconds=timeout_seconds,
            expected_outputs=tuple(expected_outputs),
            approved_by=approved_by,
            approved_at=approved_at,
            source_file=source_file.resolve(),
            source_sha256=source_sha256.upper(),
        )


def new_receipt(source_file: Path, source_sha256: str, task_id: str) -> dict[str, Any]:
    now = utc_now()
    return {
        "schema": RECEIPT_SCHEMA_VERSION,
        "task_id": task_id,
        "source_file": str(source_file.resolve()),
        "source_sha256": source_sha256.upper(),
        "state": PollerState.RECEIVED.value,
        "created_at": now,
        "updated_at": now,
        "history": [
            {
                "from": None,
                "to": PollerState.RECEIVED.value,
                "at": now,
                "detail": "Source packet observed; source was not modified.",
            }
        ],
        "worker_result": None,
    }


def transition(receipt: dict[str, Any], destination: PollerState, detail: str) -> None:
    current = PollerState(receipt["state"])
    if destination not in ALLOWED_TRANSITIONS[current]:
        raise GovernanceError(f"illegal transition {current.value} -> {destination.value}")
    now = utc_now()
    receipt["state"] = destination.value
    receipt["updated_at"] = now
    receipt.setdefault("history", []).append(
        {"from": current.value, "to": destination.value, "at": now, "detail": detail}
    )


def verify_worker_result(spec: TaskSpec, result: dict[str, Any]) -> list[str]:
    if result.get("task_id") != spec.task_id:
        raise VerificationError("worker task_id does not match authorized task")
    if str(result.get("source_sha256", "")).upper() != spec.source_sha256:
        raise VerificationError("worker source_sha256 does not match source packet")
    if str(result.get("status", "")).upper() != "COMPLETED":
        raise VerificationError("worker did not return COMPLETED")

    raw_outputs = result.get("outputs")
    if not isinstance(raw_outputs, list):
        raise VerificationError("worker outputs is not an array")
    reported = {Path(str(item)).as_posix() for item in raw_outputs}
    missing_declarations = [item for item in spec.expected_outputs if item not in reported]
    if missing_declarations:
        raise VerificationError(
            "worker omitted expected outputs: " + ", ".join(missing_declarations)
        )

    verified: list[str] = []
    for relative in spec.expected_outputs:
        output = (spec.working_directory / Path(relative)).resolve()
        if not is_within(output, [spec.working_directory]):
            raise VerificationError(f"output escaped work root: {relative}")
        if not output.is_file():
            raise VerificationError(f"expected output does not exist: {relative}")
        verified.append(relative)
    return verified


def safe_receipt_stem(task_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", task_id).strip("._-")
    return safe[:128] or "UNKNOWN_TASK"
