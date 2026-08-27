"""Fail-closed Codex CLI adapter for Tribunal Poller v7."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from tribunal_v7_state_machine import TaskSpec

KNOWN_CODEX_PATH = Path(
    r"C:\Users\dsead\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe"
)
SENSITIVE_ENV_MARKERS = (
    "API_KEY",
    "TOKEN",
    "SECRET",
    "PASSWORD",
    "CREDENTIAL",
    "SERVICE_ROLE",
    "CONNECTION_STRING",
)
OUTER_CODEX_CONTEXT_VARS = {
    "CODEX_INTERNAL_ORIGINATOR_OVERRIDE",
    "CODEX_PERMISSION_PROFILE",
    "CODEX_SANDBOX_NETWORK_DISABLED",
    "CODEX_SHELL",
    "CODEX_THREAD_ID",
}


def find_codex_executable() -> str | None:
    configured = os.environ.get("CODEX_EXECUTABLE", "").strip()
    if configured and Path(configured).is_file():
        return str(Path(configured).resolve())
    # Prefer the verified standalone CLI. On this host, PATH discovery can
    # resolve to a WindowsApps execution alias that returns WinError 5 when a
    # background Python worker tries to start it.
    if KNOWN_CODEX_PATH.is_file():
        return str(KNOWN_CODEX_PATH)
    discovered = shutil.which("codex")
    if discovered:
        return discovered
    return None


def sanitized_environment() -> dict[str, str]:
    clean: dict[str, str] = {}
    for key, value in os.environ.items():
        upper = key.upper()
        if upper in OUTER_CODEX_CONTEXT_VARS:
            continue
        if any(marker in upper for marker in SENSITIVE_ENV_MARKERS):
            continue
        clean[key] = value
    return clean


def output_schema() -> dict[str, Any]:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["task_id", "source_sha256", "status", "summary", "outputs"],
        "properties": {
            "task_id": {"type": "string"},
            "source_sha256": {"type": "string"},
            "status": {"type": "string", "enum": ["COMPLETED", "FAILED"]},
            "summary": {"type": "string"},
            "outputs": {"type": "array", "items": {"type": "string"}},
        },
    }


def build_prompt(spec: TaskSpec) -> str:
    expected = "\n".join(f"- {item}" for item in spec.expected_outputs) or "- none"
    return f"""DCSE TRIBUNAL POLLER V7 AUTHORIZED WORK ORDER

Task ID: {spec.task_id}
Source SHA-256: {spec.source_sha256}
Authorized by: {spec.approved_by} at {spec.approved_at}
Working directory: {spec.working_directory}
Sandbox: {spec.sandbox}

AUTHORIZED TASK
{spec.prompt}

EXPECTED OUTPUTS (relative to the working directory)
{expected}

BOUNDARIES
- Work only inside the stated working directory.
- Do not edit the Tribunal source packet.
- Do not run git add, commit, push, pull, branch, reset, clean, or checkout.
- Do not modify daemons, launchers, Supabase, credentials, or production state unless the task explicitly names that exact file/action and the sandbox permits it.
- Preserve unrelated user changes.
- Verify every expected output before returning.

FINAL RESPONSE CONTRACT
Return only the schema-conforming JSON object. Echo the exact task_id and source_sha256.
Use status COMPLETED only when the authorized task and expected outputs are verified; otherwise use FAILED.
List output paths relative to the working directory.
"""


def build_command(
    executable: str,
    spec: TaskSpec,
    schema_path: Path,
    final_path: Path,
) -> list[str]:
    """Build the host-verified Codex 0.145.0 noninteractive command.

    The preferred elevated Windows sandbox cannot initialize from a background
    worker on this machine (the setup helper returns WinError 5). OpenAI's
    documented unelevated fallback preserves a restricted token and ACL-based
    workspace boundaries and is therefore selected for this adapter.
    """
    return [
        executable,
        "-c",
        'windows.sandbox="unelevated"',
        "--sandbox",
        spec.sandbox,
        "--ask-for-approval",
        "never",
        "--cd",
        str(spec.working_directory),
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--output-schema",
        str(schema_path),
        "--output-last-message",
        str(final_path),
        "--json",
        "-",
    ]


def _parse_jsonl(text: str) -> tuple[bool, list[str]]:
    completed = False
    errors: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            errors.append("non-JSON line received from codex --json")
            continue
        event_type = str(event.get("type", ""))
        if event_type == "turn.completed":
            completed = True
        elif event_type in {"turn.failed", "error"}:
            errors.append(event_type)
    return completed, errors


def run_codex(spec: TaskSpec) -> dict[str, Any]:
    executable = find_codex_executable()
    if not executable:
        return {
            "adapter_status": "WORKER_UNAVAILABLE",
            "error": "Codex CLI executable was not found",
            "task_id": spec.task_id,
            "source_sha256": spec.source_sha256,
        }

    with tempfile.TemporaryDirectory(prefix="tribunal_v7_codex_") as temporary:
        temp_dir = Path(temporary)
        schema_path = temp_dir / "result.schema.json"
        final_path = temp_dir / "final.json"
        schema_path.write_text(json.dumps(output_schema(), indent=2), encoding="utf-8")

        command = build_command(executable, spec, schema_path, final_path)
        try:
            process = subprocess.run(
                command,
                input=build_prompt(spec),
                text=True,
                capture_output=True,
                timeout=spec.timeout_seconds,
                cwd=spec.working_directory,
                env=sanitized_environment(),
            )
        except subprocess.TimeoutExpired:
            return {
                "adapter_status": "TIMEOUT",
                "error": f"Codex exceeded {spec.timeout_seconds} seconds",
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        except OSError as exc:
            return {
                "adapter_status": "START_FAILED",
                "error": str(exc),
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }

        stream_completed, stream_errors = _parse_jsonl(process.stdout)
        if process.returncode != 0:
            return {
                "adapter_status": "NONZERO_EXIT",
                "exit_code": process.returncode,
                "error": process.stderr.strip()[-2000:],
                "stream_errors": stream_errors,
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        if not stream_completed or stream_errors:
            return {
                "adapter_status": "INVALID_EVENT_STREAM",
                "exit_code": process.returncode,
                "error": "Codex event stream did not prove successful completion",
                "stream_errors": stream_errors,
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        if not final_path.is_file():
            return {
                "adapter_status": "MISSING_FINAL_MESSAGE",
                "error": "Codex did not write the schema-constrained final message",
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        try:
            result = json.loads(final_path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            return {
                "adapter_status": "INVALID_FINAL_MESSAGE",
                "error": str(exc),
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        if not isinstance(result, dict):
            return {
                "adapter_status": "INVALID_FINAL_MESSAGE",
                "error": "Codex final message is not a JSON object",
                "task_id": spec.task_id,
                "source_sha256": spec.source_sha256,
            }
        result["adapter_status"] = "EXECUTED"
        result["exit_code"] = process.returncode
        return result
