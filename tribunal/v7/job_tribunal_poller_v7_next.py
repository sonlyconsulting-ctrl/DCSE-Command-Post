"""DCSE Poller v7 next-version candidate.

Extends the governed v7 Poller lineage toward the neutral Universal Dispatch
Controller without replacing the existing production/runtime poller.

This candidate keeps source packets read-only and delegates authorization and
worker verification to the existing v7 state-machine contract. It adds:
- a transport-neutral message envelope;
- recipient lists and per-recipient correlation;
- bounded concurrent dispatch;
- explicit ACK/working/response lifecycle events;
- deterministic result collection;
- file-backed durable exchange state suitable for ESCD consumption.

Activation/cutover is intentionally outside this module.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from job_tribunal_poller_v7 import process_packet
from tribunal_v7_state_machine import GovernanceError, atomic_write_json, utc_now

SCHEMA = "dcse-universal-dispatch-envelope/0.1-candidate"
DEFAULT_INBOX = Path(r"C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox")
DEFAULT_COMMAND_CENTER = Path(r"C:\DS All Things\DCSE_Command_Center")
DEFAULT_INTERVAL_SECONDS = 60
TERMINAL = {"RESPONDED", "FAILED", "TIMEOUT", "UNREACHABLE", "CANCELLED", "BLOCKED"}


@dataclass(frozen=True)
class Envelope:
    message_id: str
    task_id: str
    conversation_id: str
    sender: str
    recipients: tuple[str, ...]
    mode: str
    instruction: str
    input_files: tuple[str, ...]
    expected_outputs: tuple[str, ...]
    return_to: str
    lane: str
    authority_ref: str
    timeout_seconds: int
    attempt: int
    source_packet: Path

    @classmethod
    def from_json(cls, payload: dict[str, Any], source: Path) -> "Envelope":
        block = payload.get("DCSE_DISPATCH")
        if not isinstance(block, dict):
            raise GovernanceError("DCSE_DISPATCH object is required")
        task_id = str(block.get("task_id", "")).strip()
        sender = str(block.get("sender", "")).strip()
        instruction = str(block.get("instruction", "")).strip()
        raw_recipients = block.get("recipients", [])
        if not task_id or not sender or len(instruction) < 5:
            raise GovernanceError("task_id, sender, and bounded instruction are required")
        if not isinstance(raw_recipients, list) or not raw_recipients:
            raise GovernanceError("recipients must be a non-empty array")
        recipients = tuple(str(x).strip().lower() for x in raw_recipients if str(x).strip())
        if not recipients:
            raise GovernanceError("recipients contains no usable participant")
        timeout = int(block.get("timeout_seconds", 900))
        if not 30 <= timeout <= 3600:
            raise GovernanceError("timeout_seconds must be between 30 and 3600")
        return cls(
            message_id=str(block.get("message_id") or uuid.uuid4()),
            task_id=task_id,
            conversation_id=str(block.get("conversation_id") or task_id),
            sender=sender,
            recipients=recipients,
            mode=str(block.get("mode", "DELEGATE")).upper(),
            instruction=instruction,
            input_files=tuple(str(x) for x in block.get("input_files", [])),
            expected_outputs=tuple(str(x) for x in block.get("expected_outputs", [])),
            return_to=str(block.get("return_to", "ESCD")),
            lane=str(block.get("lane", "SC/DCSE")),
            authority_ref=str(block.get("authority_ref", "")),
            timeout_seconds=timeout,
            attempt=int(block.get("attempt", 1)),
            source_packet=source.resolve(),
        )


def event(envelope: Envelope, recipient: str, status: str, detail: str = "") -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "message_id": envelope.message_id,
        "task_id": envelope.task_id,
        "conversation_id": envelope.conversation_id,
        "sender": envelope.sender,
        "recipient": recipient,
        "mode": envelope.mode,
        "return_to": envelope.return_to,
        "lane": envelope.lane,
        "authority_ref": envelope.authority_ref,
        "attempt": envelope.attempt,
        "status": status,
        "detail": detail,
        "at": utc_now(),
    }


def write_event(runtime: Path, item: dict[str, Any]) -> Path:
    stem = f"{item['message_id']}__{item['recipient']}__{item['status']}__{uuid.uuid4().hex[:8]}"
    path = runtime / "dispatch-events" / f"{stem}.json"
    atomic_write_json(path, item)
    return path


def _recipient_packet(envelope: Envelope, recipient: str, working_directory: Path, authorization: dict[str, Any], runtime: Path) -> Path:
    """Translate the neutral envelope into the existing governed POLLER_V7 contract.

    This is the compatibility seam. Existing adapters/state-machine remain the
    execution authority until a reviewed universal adapter registry supersedes it.
    """
    worker = recipient
    if recipient in {"claude", "fable"}:
        worker = "fable"
    if worker not in {"codex", "fable"}:
        raise GovernanceError(f"recipient adapter is not yet governed: {recipient}")
    packet = {
        "POLLER_V7": {
            "task_id": f"{envelope.task_id}.{recipient}.{envelope.attempt}",
            "worker": worker,
            "prompt": envelope.instruction,
            "working_directory": str(working_directory),
            "sandbox": "workspace-write",
            "timeout_seconds": envelope.timeout_seconds,
            "expected_outputs": list(envelope.expected_outputs),
            "authorization": authorization,
        },
        "DCSE_CORRELATION": {
            "message_id": envelope.message_id,
            "conversation_id": envelope.conversation_id,
            "parent_task_id": envelope.task_id,
            "recipient": recipient,
            "return_to": envelope.return_to,
            "input_files": list(envelope.input_files),
        },
    }
    path = runtime / "translated-packets" / f"{envelope.message_id}__{recipient}.json"
    atomic_write_json(path, packet)
    return path


def dispatch_one(envelope: Envelope, recipient: str, runtime: Path, working_directory: Path, authorization: dict[str, Any], allow_roots: list[Path], execute: bool) -> dict[str, Any]:
    write_event(runtime, event(envelope, recipient, "SENT"))
    write_event(runtime, event(envelope, recipient, "RECEIVED", "Envelope admitted by dispatch controller."))
    try:
        translated = _recipient_packet(envelope, recipient, working_directory, authorization, runtime)
    except GovernanceError as exc:
        result = event(envelope, recipient, "UNREACHABLE", str(exc))
        write_event(runtime, result)
        return result
    write_event(runtime, event(envelope, recipient, "ACKNOWLEDGED", "Governed adapter contract resolved."))
    if not execute:
        result = event(envelope, recipient, "BLOCKED", "Candidate dry run: execution not enabled.")
        write_event(runtime, result)
        return result
    write_event(runtime, event(envelope, recipient, "WORKING", "Dispatch handed to existing v7 worker path."))
    outcome = process_packet(translated, runtime / "worker-runtime", allow_roots, dispatch=True)
    status = "RESPONDED" if outcome.get("outcome") == "VERIFIED_COMPLETION" else "FAILED"
    result = event(envelope, recipient, status, json.dumps(outcome, ensure_ascii=False))
    result["worker_outcome"] = outcome
    write_event(runtime, result)
    return result


def process_envelope(path: Path, runtime: Path, allow_roots: list[Path], execute: bool, max_workers: int) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    envelope = Envelope.from_json(payload, path)
    block = payload["DCSE_DISPATCH"]
    working_directory = Path(str(block.get("working_directory", DEFAULT_COMMAND_CENTER))).resolve()
    authorization = block.get("authorization")
    if not isinstance(authorization, dict) or str(authorization.get("decision", "")).upper() != "GO":
        raise GovernanceError("DCSE_DISPATCH.authorization with decision GO is required")
    created = event(envelope, "*", "CREATED", f"Recipients: {', '.join(envelope.recipients)}")
    write_event(runtime, created)
    results: list[dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(max_workers, len(envelope.recipients))) as pool:
        futures = {
            pool.submit(dispatch_one, envelope, recipient, runtime, working_directory, authorization, allow_roots, execute): recipient
            for recipient in envelope.recipients
        }
        for future in concurrent.futures.as_completed(futures):
            recipient = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                failed = event(envelope, recipient, "FAILED", f"{type(exc).__name__}: {exc}")
                write_event(runtime, failed)
                results.append(failed)
    summary = {
        "schema": SCHEMA,
        "message_id": envelope.message_id,
        "task_id": envelope.task_id,
        "conversation_id": envelope.conversation_id,
        "return_to": envelope.return_to,
        "source_packet": str(path.resolve()),
        "results": sorted(results, key=lambda x: x["recipient"]),
        "complete": all(item["status"] in TERMINAL for item in results),
        "updated_at": utc_now(),
    }
    atomic_write_json(runtime / "results" / f"{envelope.message_id}.json", summary)
    return summary


def candidate_files(inbox: Path) -> list[Path]:
    return sorted((p for p in inbox.glob("DISPATCH_*.json") if p.is_file()), key=lambda p: p.stat().st_mtime)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="DCSE Universal Dispatch Poller v7 next-version candidate")
    parser.add_argument("--inbox", type=Path, default=DEFAULT_INBOX)
    parser.add_argument("--runtime-dir", type=Path)
    parser.add_argument("--allow-root", action="append", type=Path, default=[])
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--execute", action="store_true", help="Enable governed worker execution; default is transport dry-run")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_INTERVAL_SECONDS)
    parser.add_argument("--max-workers", type=int, default=4)
    args = parser.parse_args(argv)
    inbox = args.inbox.resolve()
    if not inbox.is_dir():
        print(json.dumps({"error": f"Inbox does not exist: {inbox}"}))
        return 2
    runtime = (args.runtime_dir or (inbox / "_Universal_Dispatch_Candidate")).resolve()
    allow_roots = [p.resolve() for p in args.allow_root] or [DEFAULT_COMMAND_CENTER.resolve()]
    if args.poll_interval < 5 or args.max_workers < 1:
        print(json.dumps({"error": "invalid poll interval or max workers"}))
        return 2
    while True:
        files = candidate_files(inbox)
        if not files:
            print(json.dumps({"outcome": "NO_DISPATCH_ENVELOPES"}), flush=True)
        for path in files:
            try:
                print(json.dumps(process_envelope(path, runtime, allow_roots, args.execute, args.max_workers), ensure_ascii=False), flush=True)
            except Exception as exc:
                print(json.dumps({"source": str(path), "outcome": "FAILED", "error": f"{type(exc).__name__}: {exc}"}), flush=True)
        if not args.watch:
            return 0
        time.sleep(args.poll_interval)


if __name__ == "__main__":
    raise SystemExit(main())
