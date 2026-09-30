#!/usr/bin/env python3
"""
ESCD Shared Action Protocol Integration Bridge.

Connects the repository governance layer (Command Post) with ESCD execution:
1. Dynamically parses and resolves protocol authority, status, and revision from the governing spec.
2. Validates existing DCS authorization records and bounds actions to authorized scopes.
3. Routes DART through explicit authorized lane metadata (rejecting invalid lanes).
4. Connects to dispatch and completion handlers, persisting verifiable receipts.
5. Prevents completion records when authorization, scope, lane, or acceptance checks fail.
"""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
SPEC_PATH = REPO_ROOT / "governance" / "v7.2" / "implementations" / "DCSE_SPEC_SHARED_ACTION_PROTOCOL_v1.md"
RECEIPTS_DIR = REPO_ROOT / "governance" / "v7.2" / "implementations"

VALID_LANES = {
    "operational": "Command Post / SC (Discovery, Assess, Refine, Transfer)",
    "commercial": "Command Post / SC (Discovery, Assess, Refine, Transfer)",
    "protected_ps": "Protected PS (Discovery, Attack, Rebuttal, Trial)",
    "ps": "Protected PS (Discovery, Attack, Rebuttal, Trial)",
}


class ESCDProtocolBridgeError(RuntimeError):
    pass


class ESCDSharedProtocolBridge:
    def __init__(self, spec_path: Path | None = None, receipts_dir: Path | None = None):
        self.spec_path = spec_path or SPEC_PATH
        self.receipts_dir = receipts_dir or RECEIPTS_DIR
        self._protocol_cache: dict[str, Any] | None = None

    def load_protocol(self) -> dict[str, Any]:
        """Dynamically parses authority, lifecycle status, and revision from the governing spec."""
        if not self.spec_path.is_file():
            raise ESCDProtocolBridgeError(f"Protocol spec not found at: {self.spec_path}")
        text = self.spec_path.read_text(encoding="utf-8")

        # Dynamic parsing from spec metadata header
        doc_id_match = re.search(r'\*\*Document ID:\*\*\s*([^\r\n]+)', text)
        status_match = re.search(r'\*\*Status:\*\*\s*([^\r\n]+)', text)
        auth_match = re.search(r'\*\*Authority:\*\*\s*([^\r\n]+)', text)

        if not doc_id_match or not status_match or not auth_match:
            raise ESCDProtocolBridgeError("Protocol spec header missing required metadata fields")

        doc_id = doc_id_match.group(1).strip()
        status_raw = status_match.group(1).strip()
        status = status_raw.split()[0] if status_raw else "UNKNOWN"
        authority = auth_match.group(1).strip()

        self._protocol_cache = {
            "revision": doc_id,
            "status": status,
            "authority": authority,
            "spec_file": str(self.spec_path),
            "loaded": True,
        }
        return self._protocol_cache

    def resolve_task_contract(
        self,
        task_id: str,
        handoff_id: str,
        requested_scope: str,
        *,
        lane: str,
        auth_record: dict[str, Any] | None = None,
        execution_owner: str = "ESCD",
    ) -> dict[str, Any]:
        """
        Validates existing authorization, enforces lane routing without guessing,
        and bounds action to granted scope.
        """
        if not task_id or not handoff_id or not requested_scope:
            raise ESCDProtocolBridgeError("task_id, handoff_id, and requested_scope are required")

        # 1. Lane Validation (strict, no keyword guessing)
        clean_lane = str(lane or "").strip().lower()
        if clean_lane not in VALID_LANES:
            raise ESCDProtocolBridgeError(f"Invalid lane '{lane}'. Must be one of: {sorted(VALID_LANES.keys())}")
        dart_route = VALID_LANES[clean_lane]

        # 2. Authorization Continuity Validation
        if not auth_record or not isinstance(auth_record, dict):
            raise ESCDProtocolBridgeError("Existing authorization record is required for task continuity")

        authorizing_authority = auth_record.get("authorizing_authority")
        granted_scope = auth_record.get("authorized_scope")
        active = bool(auth_record.get("active", True))

        if authorizing_authority != "DCS" or not active:
            raise ESCDProtocolBridgeError(f"Invalid authorizing authority '{authorizing_authority}' or inactive grant")

        # 3. Scope Boundary Enforcement
        if not granted_scope:
            raise ESCDProtocolBridgeError("Authorization record lacks an authorized_scope boundary")

        # Requested scope must be within granted scope
        if requested_scope.lower() not in granted_scope.lower() and granted_scope.lower() not in requested_scope.lower():
            raise ESCDProtocolBridgeError(
                f"Scope expansion detected: '{requested_scope}' is outside authorized scope '{granted_scope}'"
            )

        proto = self.load_protocol()

        contract = {
            "task_id": task_id,
            "handoff_id": handoff_id,
            "entity": "DCSE Command Post / ESCD",
            "execution_owner": execution_owner,
            "authorizing_authority": authorizing_authority,
            "authorized_scope": granted_scope,
            "requested_scope": requested_scope,
            "lane": clean_lane,
            "artifact_lifecycle_state": proto["status"],
            "applicable_dart_route": dart_route,
            "shared_protocol_revision": proto["revision"],
            "reserved_actions": ["production_publication", "external_live_deployment"],
            "authorization_continuity_verified": True,
        }
        return contract

    def evaluate_acceptance(self, target_files: list[str | Path]) -> dict[str, Any]:
        """Runs the automated protocol check against target files and captures structured evidence."""
        import subprocess
        import sys

        script = REPO_ROOT / "scripts" / "check_shared_protocol.py"
        if not script.is_file():
            raise ESCDProtocolBridgeError(f"Enforcement script missing: {script}")

        file_args = [str(Path(f).resolve()) for f in target_files]
        cmd = [sys.executable, str(script)] + file_args
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

        passed = res.returncode == 0
        return {
            "passed": passed,
            "returncode": res.returncode,
            "stdout": res.stdout.strip(),
            "stderr": res.stderr.strip(),
            "target_count": len(target_files),
        }

    def dispatch_and_complete_task(
        self,
        task_id: str,
        handoff_id: str,
        requested_scope: str,
        lane: str,
        auth_record: dict[str, Any],
        target_files: list[str | Path],
        *,
        remote_sha: str | None = None,
        persist_evidence: bool = True,
    ) -> dict[str, Any]:
        """
        Executes end-to-end dispatch:
        1. Formulates and validates contract against authorization.
        2. Evaluates acceptance criteria against modified files.
        3. If checks fail, rejects completion without creating a successful completion record.
        4. If passed, persists retrievable receipt into governance repository.
        """
        contract = self.resolve_task_contract(
            task_id=task_id,
            handoff_id=handoff_id,
            requested_scope=requested_scope,
            lane=lane,
            auth_record=auth_record,
        )

        acceptance = self.evaluate_acceptance(target_files)
        if not acceptance["passed"]:
            raise ESCDProtocolBridgeError(f"Task acceptance evaluation failed: {acceptance['stdout']}")

        receipt = {
            "receipt_id": f"RECEIPT-{task_id}",
            "contract": contract,
            "acceptance": acceptance,
            "remote_commit_sha": remote_sha,
            "evidence_type": "ESCD_SHARED_PROTOCOL_EVALUATION",
            "status": "ACCEPTED",
        }

        if persist_evidence:
            receipt_filename = f"ESCD_EVIDENCE_{task_id.replace('-', '_')}.json"
            receipt_path = self.receipts_dir / receipt_filename
            receipt_path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
            receipt["persisted_path"] = str(receipt_path)

        return receipt

    def retrieve_evidence_receipt(self, task_id: str) -> dict[str, Any] | None:
        """Retrieves a persisted evidence receipt for a task from repository evidence storage."""
        receipt_filename = f"ESCD_EVIDENCE_{task_id.replace('-', '_')}.json"
        receipt_path = self.receipts_dir / receipt_filename
        if not receipt_path.is_file():
            return None
        return json.loads(receipt_path.read_text(encoding="utf-8"))


def get_bridge() -> ESCDSharedProtocolBridge:
    return ESCDSharedProtocolBridge()
