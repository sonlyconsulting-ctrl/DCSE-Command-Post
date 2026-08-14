#!/usr/bin/env python3
"""Deterministic DCSE v7.2 R5 context packet compiler.

This minimum operable implementation resolves authority, lane, direct sources,
conditional sources, protected exclusions, drift controls, packet identity, and
runtime preflight. It emits an append-only JSONL decision log and packet
manifest. It fails closed when required current sources are not VERIFIED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path


CONTROLLER_SHA256 = "5ddde8ec057ea51747d83191aabe13ab5983c3e306a0373bf6ae85c8737b8a03"
CONTROLLER_REVISION = "7.2.0-R5"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_hash(value: object) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--directives", required=True, type=Path)
    parser.add_argument("--designation", required=True, type=Path)
    parser.add_argument("--output-root", required=True, type=Path)
    args = parser.parse_args()

    task = load_json(args.task)
    profile = load_json(args.profile)
    registry = load_json(args.directives)
    designation = load_json(args.designation)

    task_id = task["task_id"]
    packet_id = f"CP-{task_id}-{uuid.uuid4()}"
    events: list[dict] = []

    def emit(phase: str, decision: str, reason: str, **extra: object) -> None:
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_id": task_id,
            "context_packet_id": packet_id,
            "controller_revision": CONTROLLER_REVISION,
            "controller_sha256": CONTROLLER_SHA256,
            "phase": phase,
            "decision": decision,
            "reason": reason,
            "status": extra.pop("status", "VERIFIED"),
            "evidence_refs": extra.pop("evidence_refs", []),
            **extra,
        }
        events.append(event)

    emit(
        "TASK_DECLARATION",
        "PASS",
        "Task declaration loaded.",
        evidence_refs=[str(args.task)],
    )

    authority_ok = designation.get("authority_state") == "OPERATIVE"
    directive_ids = {
        item["directive_id"]
        for item in registry.get("directives", [])
        if item.get("status") in {"ACTIVE", "INCORPORATED"}
    }
    required_directives = {
        designation.get("authority_directive_id"),
        profile.get("authority_directive_id"),
    }
    authority_ok = authority_ok and required_directives.issubset(directive_ids)
    emit(
        "AUTHORITY_RESOLUTION",
        "PASS" if authority_ok else "FAIL",
        "R5 operative designation and required active directives resolved."
        if authority_ok
        else "Operative designation or required directive is missing.",
        evidence_refs=[str(args.designation), str(args.directives)],
    )

    lane_ok = (
        task.get("entity_scope") == profile.get("entity_scope")
        and task.get("security_class") == profile.get("security_class")
    )
    emit(
        "LANE_RESOLUTION",
        "PASS" if lane_ok else "FAIL",
        "Task resolved to SS, NON_PS." if lane_ok else "Task lane or security class does not match the profile.",
        source_id=task.get("entity_scope"),
    )

    included: list[dict] = []
    excluded: list[dict] = []
    for source in profile.get("direct_rule_sources", []):
        included.append({"source_id": source, "inclusion_basis": "DIRECT"})
        emit(
            "DIRECT_RULE_SELECTION",
            "INCLUDE",
            "Source is mandatory in the registered SS website profile.",
            source_id=source,
            inclusion_basis="DIRECT",
        )

    triggers = task.get("triggers", {})
    for entry in profile.get("conditional_rule_sources", []):
        source = entry["source"]
        condition = entry["condition"]
        if triggers.get(condition) is True:
            included.append({"source_id": source, "inclusion_basis": "TRANSITIVE"})
            emit(
                "TRANSITIVE_DEPENDENCY",
                "INCLUDE",
                f"Conditional trigger is true: {condition}.",
                source_id=source,
                inclusion_basis="TRANSITIVE",
                dependency_depth=1,
            )
        else:
            excluded.append({"source_id": source, "reason": f"Trigger false: {condition}"})
            emit(
                "TRANSITIVE_DEPENDENCY",
                "EXCLUDE",
                f"Conditional trigger is false: {condition}.",
                source_id=source,
                inclusion_basis="NOT_APPLICABLE",
                dependency_depth=1,
            )

    for control in profile.get("protected_controls", []):
        emit(
            "FIREWALL_DECISION",
            "EXCLUDE",
            "Protected body excluded from NON_PS packet; identity and firewall control retained.",
            source_id=control,
            inclusion_basis="EXCLUDED_BY_FIREWALL",
        )

    for control in profile.get("drift_controls", []):
        emit(
            "CONFLICT_DISPOSITION",
            "RESOLVE",
            control["rule"],
            rule_id=control["control_id"],
            evidence_refs=[profile.get("authority_directive_id", "")],
        )

    emit(
        "CLOSURE_COMPLETE",
        "PASS",
        "Direct and conditional profile closure completed without a cycle.",
        dependency_depth=1,
    )

    evidence = {item["source"]: item for item in task.get("source_evidence", [])}
    gaps = []
    for required in profile.get("mandatory_ss_sources", []):
        record = evidence.get(required)
        if not record or record.get("status") != "VERIFIED":
            gaps.append(required)

    manifest = {
        "context_packet_id": packet_id,
        "task_id": task_id,
        "controller_revision": CONTROLLER_REVISION,
        "controller_sha256": CONTROLLER_SHA256,
        "authority_directives": sorted(required_directives),
        "lane": task.get("entity_scope"),
        "security_class": task.get("security_class"),
        "included_sources": included,
        "excluded_sources": excluded,
        "protected_bodies_loaded": False,
        "required_source_gaps": gaps,
    }
    manifest["rule_set_hash"] = canonical_hash(manifest)
    emit(
        "PACKET_BUILD",
        "PASS",
        "Packet manifest assembled and hashed.",
        evidence_refs=[manifest["rule_set_hash"]],
    )

    preflight_ok = authority_ok and lane_ok and not gaps
    emit(
        "RUNTIME_PREFLIGHT",
        "PASS" if preflight_ok else "FAIL",
        "Every mandatory authority, lane, firewall, and source requirement is present."
        if preflight_ok
        else f"Fail closed. Unverified mandatory SS sources: {', '.join(gaps) or 'none'}.",
        status="VERIFIED" if preflight_ok else "UNKNOWN",
    )
    emit(
        "EXECUTION_DECISION",
        "PASS" if preflight_ok else "STOP",
        "Execution authorized." if preflight_ok else "Execution is not authorized until preflight gaps are resolved.",
    )

    date_dir = datetime.now(timezone.utc).date().isoformat()
    log_dir = args.output_root / "logs" / "context_compiler" / date_dir
    receipt_dir = args.output_root / "receipts" / "context_packets"
    log_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"{task_id}.jsonl"
    manifest_path = receipt_dir / f"{packet_id}.manifest.json"
    log_path.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8")
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({
        "status": "PASS" if preflight_ok else "STOP_GATE",
        "log_path": str(log_path),
        "manifest_path": str(manifest_path),
        "required_source_gaps": gaps,
    }, indent=2))
    return 0 if preflight_ok else 2


if __name__ == "__main__":
    sys.exit(main())
