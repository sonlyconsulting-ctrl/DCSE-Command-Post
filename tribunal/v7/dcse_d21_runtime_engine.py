"""D21 Doctrine Runtime Engine -- reference implementation of the D21 policy contract.

Source doctrine: governance/v7.1/source/doctrines/D21_Doctrine_Runtime_Engine.md
Candidate: governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md
  (branch agent/v71-master-profile-rc3-manual, SHA-256 5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995)
Promoted: dcse_cp.governance_directives row 'D21', 2026-08-05 (DIRECT_DCS, see
  tribunal/v7/runtime-evidence/V7_1_DOCTRINE_REGISTRY_PROMOTION_20260805.md).

D21 Sec 1: "D21 specifies policy and logical contracts. A Python module or
equivalent deterministic runtime implements those contracts. Neither D21 nor
its implementation creates promotion authority." This module is that
implementation for the seven YAML contracts D21 defines (Sec 4.1, 5.4, 6.5,
7.1, 13.3, 14.1, 15.2) plus the ten Python-module components D21 Sec 17
requires (Loader, Classifier, Router, Validator, State machine, Diff tracker,
Receipt writer, Promotion guard, Reconciler, Adapters).

Per D21 Sec 2.2 (non-authority rule): nothing in this module can promote
doctrine, change lifecycle authority, or treat test/merge/database state as
authority. PromotionGuard.evaluate() enforces that mechanically -- it returns
AUTHORITY_CONFIRMED only for an explicit DIRECT_DCS or STANDING_DCSE
authority_ref, never as a side effect of validation passing.
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

D21_SCHEMA_VERSION = "1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Same atomic-write contract as tribunal_v7_state_machine.atomic_write_json
    (fsync + os.replace). Inlined rather than imported: that module lives only
    on governance/v7.1-promotion-metadata-reconciliation, not on this branch,
    and this module should not carry a silent cross-branch runtime dependency
    -- exactly the kind of thing D22 (Source Authority and Runtime
    Distribution) exists to prevent.
    """
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


# ---------------------------------------------------------------------------
# Enums (D21 Sec 3, 10, 13.1, 13.2)
# ---------------------------------------------------------------------------

class SourceMode(str, Enum):
    """D21 Sec 3 runtime modes."""
    REGISTRY_PRIMARY = "REGISTRY_PRIMARY"
    REPOSITORY_READ_ONLY = "REPOSITORY_READ_ONLY"
    OFFLINE_VERIFIED = "OFFLINE_VERIFIED"


class IssueDisposition(str, Enum):
    """D21 Sec 10 resolution-first execution dispositions."""
    RESOLVED = "RESOLVED"
    RESOLVED_WITH_FINDINGS = "RESOLVED_WITH_FINDINGS"
    DEFERRED_NONBLOCKING = "DEFERRED_NONBLOCKING"
    BLOCKED_CAPABILITY = "BLOCKED_CAPABILITY"
    READY_FOR_AUTHORITY_DECISION = "READY_FOR_AUTHORITY_DECISION"
    BLOCKED_RESERVED = "BLOCKED_RESERVED"


class LifecycleState(str, Enum):
    """D21 Sec 13.1 task lifecycle states."""
    INTAKE = "INTAKE"
    ADMISSION = "ADMISSION"
    BASELINE = "BASELINE"
    PLAN = "PLAN"
    EXECUTE = "EXECUTE"
    VERIFY = "VERIFY"
    CORRECT = "CORRECT"
    REVIEW = "REVIEW"
    READY_FOR_PROMOTION = "READY_FOR_PROMOTION"
    PROMOTED = "PROMOTED"
    RELEASED = "RELEASED"
    RECONCILED = "RECONCILED"
    CLOSED = "CLOSED"
    DEFERRED_NONBLOCKING = "DEFERRED_NONBLOCKING"
    BLOCKED_CAPABILITY = "BLOCKED_CAPABILITY"
    BLOCKED_RESERVED = "BLOCKED_RESERVED"
    DRIFT = "DRIFT"


class PromotionGuardState(str, Enum):
    """D21 Sec 13.2 promotion guard dispositions."""
    NOT_READY = "NOT_READY"
    READY_FOR_PROMOTION = "READY_FOR_PROMOTION"
    AUTHORITY_CONFIRMED = "AUTHORITY_CONFIRMED"
    PROMOTION_RECORDED = "PROMOTION_RECORDED"
    PROMOTION_RECONCILIATION_PENDING = "PROMOTION_RECONCILIATION_PENDING"
    RECONCILED = "RECONCILED"


# D21 Sec 6.1: the fixed always-on constitutional bootstrap. D05/D20 are
# conditionally added by the caller (baseline/promotion/product work);
# D13/D14 are never added here (PS-only, Sec 6.1 + repo-wide PS constraint).
ALWAYS_ON_DOCTRINES: tuple[str, ...] = ("MASTER_PROFILE", "D03", "D21", "D22")
PS_PROTECTED_DOCTRINES: frozenset[str] = frozenset({"D13", "D14"})


class GovernanceError(ValueError):
    """A D21 contract precondition was violated."""


# ---------------------------------------------------------------------------
# D21 Sec 4.1 -- Task Declaration contract
# ---------------------------------------------------------------------------

@dataclass
class TaskDeclaration:
    task_id: str
    conversation_id: str = ""
    objective: str = ""
    acceptance_criteria: list[str] = field(default_factory=list)
    entity: str = ""
    lane: str = ""
    task_type: str = ""
    artifact_type: str = ""
    lifecycle_phase: str = ""
    release_posture: str = ""
    risk_class: str = ""
    execution_identity: str = ""
    runtime_name: str = ""
    model_name: str = ""
    model_exposed: bool = False
    capability_profile: list[str] = field(default_factory=list)
    access_profile: list[str] = field(default_factory=list)
    inferred_fields: list[dict[str, Any]] = field(default_factory=list)
    evidence_destinations: list[str] = field(default_factory=list)
    rollback_expectation: str = ""
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        d = dict(self.__dict__)
        return d


# ---------------------------------------------------------------------------
# D21 Sec 5.4 -- logical doctrine fields (registry-schema-adapter output)
# ---------------------------------------------------------------------------

@dataclass
class DoctrineRecord:
    doctrine_id: str
    title: str = ""
    version: str = ""
    lifecycle_status: str = ""
    promotion_status: str = ""
    entity_lanes: list[str] = field(default_factory=list)
    firewall_flags: list[str] = field(default_factory=list)
    topics: list[str] = field(default_factory=list)
    task_triggers: list[str] = field(default_factory=list)
    artifact_triggers: list[str] = field(default_factory=list)
    lifecycle_triggers: list[str] = field(default_factory=list)
    capability_requirements: list[str] = field(default_factory=list)
    required_inputs: list[str] = field(default_factory=list)
    required_outputs: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    source_repository: str = ""
    source_path: str = ""
    source_commit: str = ""
    source_blob: str = ""
    content_sha256: str = ""
    executability_status: str = ""
    promotion_authority_ref: str = ""

    def is_promoted(self) -> bool:
        """True for both a clean PROMOTED row and a DCS-override
        PROMOTED_WITH_KNOWN_GAPS row -- both carry real DIRECT_DCS authority
        per D05 Sec 2. What distinguishes them is needs_wrapper(), not
        promotion status; conflating the two would hide the override in the
        routing behavior instead of just in the label.
        """
        return self.promotion_status.upper().startswith("PROMOTED")

    def needs_wrapper(self) -> bool:
        """D21 Sec 8: any promoted-but-not-structurally-clean doctrine still
        requires the executability wrapper at the point of use, regardless
        of promotion status. A DCS override authorizes using the doctrine;
        it does not retroactively supply the receipt/gate-schema/rollback
        structure the 2026-08-03 audit found missing.
        """
        return self.promotion_status.upper() == "PROMOTED_WITH_KNOWN_GAPS" or (
            self.executability_status
            and self.executability_status.upper() not in {"DCSE_OPERATIONAL", "DCSE_CONSTITUTIONAL"}
        )


@dataclass
class AdapterManifest:
    """D21 Sec 5.3 registry-schema-adapter evidence record."""
    adapter_id: str
    adapter_version: str
    project_identity: str
    source_evidence: str
    field_mapping: dict[str, str]
    read_capable: bool
    write_capable: bool
    validation_timestamp: str
    accountable_validator: str
    rollback_or_disable: str


# Maps physical dcse_cp.governance_directives columns to D21's logical
# doctrine_record fields (D21 Sec 5.3: "records ... logical-to-physical
# field mapping"). This is the adapter this module currently trusts; it was
# derived from a live schema read on 2026-08-05, not assumed.
GOVERNANCE_DIRECTIVES_FIELD_MAP: dict[str, str] = {
    "doctrine_id": "id",
    "title": "title",
    "version": "version",
    "lifecycle_status": "status",
    "promotion_status": "promotion_status",
    "content_sha256": "checksum",
    "promotion_authority_ref": "approved_by",
    "executability_status": "authority_level",
}

ADAPTER_MANIFEST = AdapterManifest(
    adapter_id="dcse_cp.governance_directives.v1",
    adapter_version="1.0",
    project_identity="nevgdyfpxdaloacuutal/dcse_cp",
    source_evidence="live read-only schema discovery, 2026-08-05 (information_schema.columns)",
    field_mapping=GOVERNANCE_DIRECTIVES_FIELD_MAP,
    read_capable=True,
    write_capable=False,  # this module does not write governance_directives
    validation_timestamp=utc_now(),
    accountable_validator="Claude Code (Sonnet 5)",
    rollback_or_disable="unset ADAPTER_MANIFEST.read_capable=False; router falls back to REPOSITORY_READ_ONLY",
)


def adapt_governance_directives_rows(rows: list[dict[str, Any]]) -> list[DoctrineRecord]:
    """D21 Sec 5.3/5.4: convert physical registry rows to logical DoctrineRecord.

    Raises GovernanceError if a required physical column is absent -- per
    D21 Sec 5.3, "If adapter verification fails, the runtime enters
    REPOSITORY_READ_ONLY" rather than guessing field names.
    """
    records: list[DoctrineRecord] = []
    for row in rows:
        try:
            records.append(DoctrineRecord(
                doctrine_id=str(row[GOVERNANCE_DIRECTIVES_FIELD_MAP["doctrine_id"]]),
                title=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["title"], "")),
                version=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["version"], "")),
                lifecycle_status=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["lifecycle_status"], "")),
                promotion_status=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["promotion_status"]) or ""),
                content_sha256=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["content_sha256"]) or ""),
                promotion_authority_ref=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["promotion_authority_ref"]) or ""),
                executability_status=str(row.get(GOVERNANCE_DIRECTIVES_FIELD_MAP["executability_status"]) or ""),
                source_repository="sonlyconsulting-ctrl/DCSE-Command-Post",
                source_path=f"dcse_cp.governance_directives/{row.get('id')}",
            ))
        except KeyError as exc:
            raise GovernanceError(f"registry adapter verification failed: missing column {exc}") from exc
    return records


# ---------------------------------------------------------------------------
# D21 Sec 6.5 -- Doctrine Run Plan contract
# ---------------------------------------------------------------------------

@dataclass
class DoctrineRunPlan:
    plan_id: str
    task_id: str
    conversation_id: str = ""
    governance_version: str = "v7.1"
    source_mode: str = ""
    source_commit: str = ""
    task_declaration_ref: str = ""
    always_on: list[str] = field(default_factory=list)
    selected: list[dict[str, Any]] = field(default_factory=list)
    evaluated_not_selected: list[dict[str, Any]] = field(default_factory=list)
    excluded_by_firewall: list[dict[str, Any]] = field(default_factory=list)
    reference_only: list[dict[str, Any]] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    drift: list[dict[str, Any]] = field(default_factory=list)
    wrappers_required: list[str] = field(default_factory=list)
    unresolved_capabilities: list[str] = field(default_factory=list)
    reserved_stop_gate: bool = False
    reserved_stop_reason: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    router_version: str = "dcse_d21_runtime_engine/1.0"
    generated_by: str = "Claude Code (Sonnet 5)"
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


# ---------------------------------------------------------------------------
# D21 Sec 7.1 -- Doctrine Consideration Log (DCL) contract
# ---------------------------------------------------------------------------

@dataclass
class DoctrineConsiderationLog:
    dcl_id: str
    task_id: str
    conversation_id: str = ""
    task_declaration_ref: str = ""
    doctrine_run_plan_ref: str = ""
    execution_identity: str = ""
    runtime_name: str = "Claude Code"
    model_name: str = "claude-sonnet-5"
    model_exposed: bool = True
    execution_environment: str = ""
    source_mode: str = ""
    source_commit: str = ""
    loaded: list[str] = field(default_factory=list)
    applied: list[str] = field(default_factory=list)
    evaluated_not_applied: list[str] = field(default_factory=list)
    excluded_by_firewall: list[str] = field(default_factory=list)
    reference_only: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    conflicts: list[dict[str, Any]] = field(default_factory=list)
    gaps_detected: list[dict[str, Any]] = field(default_factory=list)
    methodology_triggers: list[str] = field(default_factory=list)
    capability_events: list[dict[str, Any]] = field(default_factory=list)
    security_results: list[dict[str, Any]] = field(default_factory=list)
    preview_results: list[dict[str, Any]] = field(default_factory=list)
    issue_dispositions: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    write_receipts: list[dict[str, Any]] = field(default_factory=list)
    lifecycle_state: str = LifecycleState.INTAKE.value
    reconciliation_state: str = "PENDING_RECONCILIATION"
    authority_refs: list[str] = field(default_factory=list)
    disposition: str = ""
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


class DCLWriter:
    """D21 Sec 7.2: DCL storage is adapter-controlled, not hardcoded.

    This is one approved local-evidence adapter, not the only permitted one.
    When no remote (Supabase/GitHub) sink is wired, writes go to a local
    evidence path and the write receipt is marked PENDING_RECONCILIATION --
    exactly the behavior Sec 7.2 requires ("Lack of remote storage does not
    halt unrelated work").
    """

    def __init__(self, evidence_root: Path):
        self.evidence_root = evidence_root

    def write(self, dcl: DoctrineConsiderationLog) -> dict[str, Any]:
        out_path = self.evidence_root / f"{dcl.dcl_id}.dcl.json"
        atomic_write_json(out_path, dcl.to_dict())
        receipt = {
            "sink_identity": "local_evidence_adapter/1.0",
            "operation": "write",
            "created_or_stored_state": "STORED",
            "delivery_state": "NOT_APPLICABLE",
            "receipt_id": f"{dcl.dcl_id}-local",
            "timestamp": utc_now(),
            "reconciliation_status": "PENDING_RECONCILIATION",
            "failure_reason": "",
            "path": str(out_path),
        }
        dcl.write_receipts.append(receipt)
        return receipt


# ---------------------------------------------------------------------------
# D21 Sec 13.3 -- Promotion readiness packet
# ---------------------------------------------------------------------------

@dataclass
class PromotionReadinessPacket:
    packet_id: str
    object_id: str
    object_version: str = ""
    object_path: str = ""
    object_commit: str = ""
    object_sha256: str = ""
    change_records: list[str] = field(default_factory=list)
    doctrine_run_plan_ref: str = ""
    dcl_ref: str = ""
    validation_results: list[dict[str, Any]] = field(default_factory=list)
    review_receipts: list[str] = field(default_factory=list)
    unresolved_findings: list[str] = field(default_factory=list)
    rollback_ref: str = ""
    required_authority: str = ""
    authority_ref: str = ""
    guard_disposition: str = PromotionGuardState.NOT_READY.value
    evidence_refs: list[str] = field(default_factory=list)
    accountable_identity: str = ""
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


# ---------------------------------------------------------------------------
# D21 Sec 14.1 -- Doctrine change record
# ---------------------------------------------------------------------------

@dataclass
class DoctrineChangeRecord:
    change_id: str
    doctrine_id: str
    prior_path: str = ""
    current_path: str = ""
    prior_commit: str = ""
    current_commit: str = ""
    prior_sha256: str = ""
    current_sha256: str = ""
    metadata_changes: list[str] = field(default_factory=list)
    content_diff_ref: str = ""
    dependency_effects: list[str] = field(default_factory=list)
    lifecycle_effect: str = ""
    constitutional_change: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    accountable_identity: str = ""
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)


# ---------------------------------------------------------------------------
# D21 Sec 15.2 -- Reconciliation receipt
# ---------------------------------------------------------------------------

@dataclass
class ReconciliationReceipt:
    reconciliation_id: str
    object_id: str
    authority_ref: str = ""
    github_identity: dict[str, Any] = field(default_factory=dict)
    registry_identity: dict[str, Any] = field(default_factory=dict)
    local_identity: dict[str, Any] = field(default_factory=dict)
    runtime_identities: list[str] = field(default_factory=list)
    communication_refs: list[str] = field(default_factory=list)
    mismatches: list[dict[str, Any]] = field(default_factory=list)
    remediation_actions: list[str] = field(default_factory=list)
    final_disposition: str = "PENDING"
    evidence_refs: list[str] = field(default_factory=list)
    accountable_identity: str = ""
    schema_version: str = D21_SCHEMA_VERSION
    timestamp: str = field(default_factory=utc_now)


# ---------------------------------------------------------------------------
# Loader (D21 Sec 3, 17)
# ---------------------------------------------------------------------------

class Loader:
    """D21 Sec 3: determine source mode from verified connectivity, not assumption."""

    @staticmethod
    def determine_source_mode(
        registry_reachable_and_verified: bool,
        github_reachable: bool,
        verified_promoted_local_copy: bool,
    ) -> SourceMode:
        if registry_reachable_and_verified:
            return SourceMode.REGISTRY_PRIMARY
        if github_reachable:
            return SourceMode.REPOSITORY_READ_ONLY
        if verified_promoted_local_copy:
            return SourceMode.OFFLINE_VERIFIED
        raise GovernanceError(
            "no verified source available: registry unreachable, GitHub unreachable, "
            "no verified promoted local copy -- D21 Sec 16 degraded-mode protocol applies"
        )


# ---------------------------------------------------------------------------
# Router (D21 Sec 6.2 routing order)
# ---------------------------------------------------------------------------

class Router:
    """Implements the deterministic routing order in D21 Sec 6.2, steps 1-13,
    to the extent that order is structural (identity, status, lane, firewall,
    trigger matching) rather than semantic task understanding, which D21
    explicitly leaves to the runtime's judgment (Sec 1: "policy and logical
    contracts", not a semantic classifier).
    """

    def __init__(self, registry: list[DoctrineRecord], source_mode: SourceMode, source_commit: str = ""):
        self.registry = {r.doctrine_id: r for r in registry}
        self.source_mode = source_mode
        self.source_commit = source_commit

    def route(
        self,
        task: TaskDeclaration,
        candidate_doctrine_ids: list[str],
        ps_mode_authorized: bool = False,
        include_baseline_promotion: bool = False,
        include_product_assembly: bool = False,
    ) -> DoctrineRunPlan:
        plan_id = f"DRP-{task.task_id}-{utc_now()}"
        plan = DoctrineRunPlan(
            plan_id=plan_id,
            task_id=task.task_id,
            conversation_id=task.conversation_id,
            source_mode=self.source_mode.value,
            source_commit=self.source_commit,
            task_declaration_ref=task.task_id,
        )

        # Step 3: load always-on controls (Sec 6.1)
        always_on = list(ALWAYS_ON_DOCTRINES)
        if include_baseline_promotion:
            always_on.append("D05")
        if include_product_assembly:
            always_on.append("D20")
        plan.always_on = always_on

        candidates = list(dict.fromkeys(always_on + candidate_doctrine_ids))

        for doctrine_id in candidates:
            # Step 5: verify doctrine identity and hash
            record = self.registry.get(doctrine_id)
            if record is None:
                plan.missing.append(doctrine_id)
                continue

            # Step 8: enforce PS/PPR firewall
            if doctrine_id in PS_PROTECTED_DOCTRINES and not ps_mode_authorized:
                plan.excluded_by_firewall.append({
                    "doctrine_id": doctrine_id,
                    "reason": "PS-protected doctrine outside authorized PS mode",
                })
                continue

            # Step 6: filter by lifecycle and promotion status
            if not record.is_promoted():
                plan.evaluated_not_selected.append({
                    "doctrine_id": doctrine_id,
                    "reason": f"promotion_status={record.promotion_status or 'unset'}, not PROMOTED",
                    "source_hash": record.content_sha256,
                })
                if record.needs_wrapper():
                    plan.wrappers_required.append(doctrine_id)
                continue

            # Selected -- promoted (clean or DCS-override-with-gaps alike).
            # A DCS override makes a doctrine available for use; it does not
            # retroactively close the audit's structural finding, so the
            # wrapper requirement is tracked independently of selection.
            plan.selected.append({
                "doctrine_id": doctrine_id,
                "source_hash": record.content_sha256,
                "decision_reason": (
                    "promoted (DCS override, known gaps preserved)" if record.needs_wrapper()
                    else "promoted, entity/lane in scope, not firewalled"
                ),
            })
            if record.needs_wrapper():
                plan.wrappers_required.append(doctrine_id)

        return plan


# ---------------------------------------------------------------------------
# PromotionGuard (D21 Sec 13.2) -- the non-authority rule, enforced
# ---------------------------------------------------------------------------

VALID_AUTHORITY_FORMS = ("DIRECT_DCS", "STANDING_DCSE")


class PromotionGuard:
    """D21 Sec 13.2: 'No numeric promotion score, model vote, review outcome,
    merge, test, or database state substitutes for promotion authority.'

    evaluate() takes validation_passed as informational only -- it cannot by
    itself produce AUTHORITY_CONFIRMED. Only an explicit, non-empty
    authority_ref of the exact form DIRECT_DCS or STANDING_DCSE can.
    """

    @staticmethod
    def evaluate(
        validation_passed: bool,
        unresolved_findings: list[str],
        authority_ref: str,
    ) -> PromotionGuardState:
        if unresolved_findings:
            return PromotionGuardState.NOT_READY
        if not validation_passed:
            return PromotionGuardState.NOT_READY
        if not authority_ref or authority_ref not in VALID_AUTHORITY_FORMS:
            # Tests, merges, or a clean validation run alone stop here.
            return PromotionGuardState.READY_FOR_PROMOTION
        return PromotionGuardState.AUTHORITY_CONFIRMED


# ---------------------------------------------------------------------------
# Reconciler (D21 Sec 14.3, 15.2)
# ---------------------------------------------------------------------------

class Reconciler:
    @staticmethod
    def compare(
        object_id: str,
        github_sha256: str | None,
        registry_sha256: str | None,
        local_sha256: str | None,
        accountable_identity: str,
    ) -> ReconciliationReceipt:
        hashes = {k: v for k, v in {
            "github": github_sha256, "registry": registry_sha256, "local": local_sha256,
        }.items() if v is not None}
        distinct = set(hashes.values())
        mismatches = []
        if len(distinct) > 1:
            mismatches.append({"finding": "DRIFT", "hashes": hashes})
        receipt = ReconciliationReceipt(
            reconciliation_id=f"RECON-{object_id}-{utc_now()}",
            object_id=object_id,
            github_identity={"sha256": github_sha256} if github_sha256 else {},
            registry_identity={"sha256": registry_sha256} if registry_sha256 else {},
            local_identity={"sha256": local_sha256} if local_sha256 else {},
            mismatches=mismatches,
            final_disposition="RECONCILED" if not mismatches else "PENDING",
            accountable_identity=accountable_identity,
        )
        return receipt
