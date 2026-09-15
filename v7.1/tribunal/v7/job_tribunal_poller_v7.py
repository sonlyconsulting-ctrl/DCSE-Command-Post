"""DCSE Tribunal Poller v7 candidate.

Default mode is a one-pass audit. Worker execution requires --dispatch and an
explicit POLLER_V7 authorization block in the source packet. Source packets are
read-only. Git, quarantine moves, launcher changes, and publication are absent.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

from tribunal_v7_codex_adapter import run_codex
from tribunal_v7_fable_adapter import run_fable
from tribunal_v7_state_machine import (
    GovernanceError,
    PollerState,
    TaskSpec,
    VerificationError,
    atomic_write_json,
    new_receipt,
    safe_receipt_stem,
    sha256_file,
    transition,
    verify_worker_result,
)

DEFAULT_INBOX = Path(r"C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox")
DEFAULT_COMMAND_CENTER = Path(r"C:\DS All Things\DCSE_Command_Center")
DEFAULT_INTERVAL_SECONDS = 120


def log(message: str) -> None:
    print(message, flush=True)


def load_packet(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(payload, dict):
        raise GovernanceError("Tribunal packet must be a JSON object")
    return payload


def has_v7_marker(path: Path) -> bool:
    try:
        return '"POLLER_V7"' in path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return False


def candidate_files(inbox: Path) -> list[Path]:
    return sorted(
        (
            path
            for path in inbox.glob("TRIBUNAL_*.json")
            if path.is_file() and has_v7_marker(path)
        ),
        key=lambda path: path.stat().st_mtime,
    )


def receipt_path(runtime_dir: Path, task_id: str, source_sha256: str) -> Path:
    name = f"{safe_receipt_stem(task_id)}__{source_sha256[:12]}.receipt.json"
    return runtime_dir / "receipts" / name


def terminal_receipt_exists(path: Path, source_sha256: str) -> bool:
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        return (
            str(data.get("source_sha256", "")).upper() == source_sha256.upper()
            and data.get("state")
            in {
                PollerState.COMPLETED.value,
                PollerState.FAILED.value,
                PollerState.QUARANTINE_PENDING.value,
            }
        )
    except (OSError, json.JSONDecodeError):
        return False


def _task_id_hint(path: Path, packet: dict[str, Any] | None) -> str:
    if packet:
        block = packet.get("POLLER_V7")
        if isinstance(block, dict) and block.get("task_id"):
            return str(block["task_id"])
    return path.stem


def process_packet(
    path: Path,
    runtime_dir: Path,
    allowed_roots: list[Path],
    dispatch: bool,
) -> dict[str, Any]:
    source_sha256 = sha256_file(path)
    packet: dict[str, Any] | None = None
    task_id = path.stem
    try:
        packet = load_packet(path)
        task_id = _task_id_hint(path, packet)
    except (OSError, json.JSONDecodeError, GovernanceError):
        pass

    out = receipt_path(runtime_dir, task_id, source_sha256)
    if terminal_receipt_exists(out, source_sha256):
        return {"outcome": "IDEMPOTENT_SKIP", "receipt": str(out), "task_id": task_id}

    receipt = new_receipt(path, source_sha256, task_id)
    atomic_write_json(out, receipt)

    try:
        if packet is None:
            packet = load_packet(path)
        spec = TaskSpec.from_packet(packet, path, source_sha256, allowed_roots)
        transition(receipt, PollerState.VALIDATED, "Packet schema and path boundaries validated.")
        atomic_write_json(out, receipt)
        transition(
            receipt,
            PollerState.AUTHORIZED,
            f"GO recorded by {spec.approved_by} at {spec.approved_at}.",
        )
        receipt["authorized_scope"] = {
            "worker": spec.worker,
            "working_directory": str(spec.working_directory),
            "sandbox": spec.sandbox,
            "expected_outputs": list(spec.expected_outputs),
            "timeout_seconds": spec.timeout_seconds,
        }
        atomic_write_json(out, receipt)

        if not dispatch:
            receipt["outcome"] = "AUTHORIZED_DRY_RUN_HOLD"
            atomic_write_json(out, receipt)
            return {"outcome": receipt["outcome"], "receipt": str(out), "task_id": task_id}

        transition(receipt, PollerState.DISPATCHED, f"Dispatched to {spec.worker} adapter.")
        atomic_write_json(out, receipt)
        if spec.worker == "codex":
            worker_result = run_codex(spec)
        else:
            worker_result = run_fable(spec)

        receipt["worker_result"] = worker_result
        transition(receipt, PollerState.VERIFYING, "Worker exited; verifying trusted completion evidence.")
        atomic_write_json(out, receipt)
        verified_outputs = verify_worker_result(spec, worker_result)
        receipt["verified_outputs"] = verified_outputs
        transition(
            receipt,
            PollerState.COMPLETED,
            "Exit, structured result, task ID, source hash, and expected outputs verified.",
        )
        receipt["outcome"] = "VERIFIED_COMPLETION"
        atomic_write_json(out, receipt)
        return {"outcome": receipt["outcome"], "receipt": str(out), "task_id": task_id}

    except GovernanceError as exc:
        transition(receipt, PollerState.QUARANTINE_PENDING, str(exc))
        receipt["outcome"] = "QUARANTINE_PENDING_NO_MOVE_PERFORMED"
    except VerificationError as exc:
        if receipt["state"] != PollerState.VERIFYING.value:
            transition(receipt, PollerState.FAILED, str(exc))
        else:
            transition(receipt, PollerState.FAILED, str(exc))
        receipt["outcome"] = "FAILED_VERIFICATION"
    except Exception as exc:
        current = PollerState(receipt["state"])
        if current not in {
            PollerState.COMPLETED,
            PollerState.FAILED,
            PollerState.QUARANTINE_PENDING,
        }:
            transition(receipt, PollerState.FAILED, f"{type(exc).__name__}: {exc}")
        receipt["outcome"] = "FAILED_INTERNAL_ERROR"

    atomic_write_json(out, receipt)
    return {"outcome": receipt["outcome"], "receipt": str(out), "task_id": task_id}


def run_once(
    inbox: Path,
    runtime_dir: Path,
    allowed_roots: list[Path],
    dispatch: bool,
) -> list[dict[str, Any]]:
    results = []
    for path in candidate_files(inbox):
        result = process_packet(path, runtime_dir, allowed_roots, dispatch)
        results.append(result)
        log(json.dumps(result, ensure_ascii=False))
    if not results:
        log(json.dumps({"outcome": "NO_EXPLICIT_POLLER_V7_TASKS"}))
    return results


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Governed DCSE Tribunal Poller v7 candidate")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    parser.add_argument("--runtime-dir", type=Path, default=None)
    parser.add_argument("--allow-root", action="append", type=Path, default=[])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="run one pass (default)")
    mode.add_argument("--watch", action="store_true", help="continue polling")
    parser.add_argument(
        "--dispatch",
        action="store_true",
        help="execute authorized tasks; without this flag the poller is audit-only",
    )
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_INTERVAL_SECONDS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    inbox = args.inbox.resolve()
    if not inbox.is_dir():
        log(json.dumps({"error": f"Inbox does not exist: {inbox}"}))
        return 2
    runtime_dir = (
        args.runtime_dir.resolve()
        if args.runtime_dir
        else (inbox / "_Poller_v7_Runtime").resolve()
    )
    allowed_roots = [path.resolve() for path in args.allow_root] or [DEFAULT_COMMAND_CENTER.resolve()]
    if args.poll_interval < 5:
        log(json.dumps({"error": "poll interval must be at least 5 seconds"}))
        return 2

    while True:
        run_once(inbox, runtime_dir, allowed_roots, args.dispatch)
        if not args.watch:
            return 0
        time.sleep(args.poll_interval)


if __name__ == "__main__":
    raise SystemExit(main())
