#!/usr/bin/env python3
"""Require explicit single-use authorization for deployment-capable Supabase migrations."""
from __future__ import annotations

import pathlib
import re
import sys

AUTH_DIR = pathlib.Path("governance/v7.3/authorizations/supabase")
TEMPLATE_NAME = "SUPABASE_TRANSACTION_AUTHORIZATION_TEMPLATE.yaml"


def scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}:\s*[\"']?([^\n\"']*)", text)
    return match.group(1).strip() if match else ""


def truthy(text: str, key: str) -> bool:
    return scalar(text, key).lower() == "true"


def packets() -> list[tuple[pathlib.Path, str]]:
    if not AUTH_DIR.exists():
        return []
    return [
        (path, path.read_text(encoding="utf-8"))
        for path in sorted(AUTH_DIR.glob("*.yaml"))
        if path.name != TEMPLATE_NAME
    ]


def validates(packet: str, migration: str) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if scalar(packet, "state").upper() != "AUTHORIZED":
        errors.append("state must be AUTHORIZED")
    if migration not in packet:
        errors.append("exact migration path is not listed")
    for key in ("task_id", "project_name", "project_ref", "environment", "operation_class", "authorized_by", "authority_reference"):
        if not scalar(packet, key):
            errors.append(f"{key} is required")
    for key in ("git_integration_apply_authorized", "live_mutation_authorized", "single_use"):
        if not truthy(packet, key):
            errors.append(f"{key} must be true")
    if scalar(packet, "destructive_effect").lower() != "none" and not scalar(packet, "backup_checkpoint"):
        errors.append("destructive changes require backup_checkpoint")
    return not errors, errors


def main(paths: list[str]) -> int:
    migrations = [
        path.replace("\\", "/")
        for path in paths
        if path.replace("\\", "/").startswith("supabase/migrations/") and path.endswith(".sql")
    ]
    if not migrations:
        print("Supabase authorization gate: no changed deployment-capable migrations.")
        return 0

    available = packets()
    failures: list[str] = []
    for migration in migrations:
        matched = False
        diagnostics: list[str] = []
        for packet_path, packet in available:
            if migration not in packet:
                continue
            ok, errors = validates(packet, migration)
            if ok:
                print(f"AUTHORIZED: {migration} via {packet_path}")
                matched = True
                break
            diagnostics.append(f"{packet_path}: {', '.join(errors)}")
        if not matched:
            detail = "; ".join(diagnostics) if diagnostics else "no task-specific packet lists the exact migration path"
            failures.append(f"{migration}: {detail}")

    if failures:
        print("SUPABASE_MUTATION_NOT_AUTHORIZED", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
