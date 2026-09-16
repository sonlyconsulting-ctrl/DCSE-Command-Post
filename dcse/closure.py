"""Deterministic human-review closeout guard.

This module operationalizes existing DCSE authority. It does not create new
constitutional authority. The controlling sources are DCS-DIR-20260906-002,
D21, and the cross-system reconciliation/completion-evidence contract.

A worker may finish implementation without making the work review-ready.
The guard therefore separates TECHNICALLY_COMPLETE from
HUMAN_REVIEW_EVIDENCE_READY and refuses a terminal/review-ready transition
until the evidence contract for the output class is satisfied.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Sequence

from model import Operation

RULE_ID = "CLOSEOUT-HUMAN-REVIEW-001"
RULESET = "CLOSURE_INTEGRITY"
VERSION = "1.0"

SOURCE_REFS = (
    "governance/v7.2/DCSE_V7_2_COMPLETION_EVIDENCE_COLLECTOR_DIRECTIVE_20260906.md",
    "governance/v7.2/doctrines/D21_Doctrine_Runtime_Engine_v7-2.md",
    "governance/v7.2/execution/DCSE_CROSS_SYSTEM_RECONCILIATION_AND_COMPLETION_EVIDENCE_CONTRACT_v1.md",
)

TERMINAL_ACTIONS = {
    "complete", "close", "finalize", "ready", "ready_for_review",
    "ready_for_dcs_review", "mark_complete", "mark_ready",
    "transition_complete", "transition_ready",
}
TERMINAL_STATES = {
    "complete", "completed", "closed", "closed_complete", "ready",
    "ready_for_review", "ready_for_dcs_review",
}

_BROWSER = {
    "browser", "browser_renderable", "html", "website", "web", "web_app",
    "landing_page", "webpage", "site", "app_ui",
}
_FILE = {"file", "document", "pdf", "docx", "package", "zip", "spreadsheet", "slides"}
_RUNTIME = {"database", "runtime", "migration", "api", "backend", "supabase"}
_MEDIA = {"media", "image", "video", "audio"}


@dataclass
class ClosureEvidenceResult:
    applicable: bool
    passed: bool
    artifact_class: str = ""
    target_state: str = ""
    missing: Sequence[str] = field(default_factory=tuple)
    evidence_refs: Sequence[str] = field(default_factory=tuple)
    detail: str = ""

    @property
    def remediation_state(self) -> str:
        if self.applicable and not self.passed:
            return "TECHNICALLY_COMPLETE / HUMAN_REVIEW_EVIDENCE_PENDING"
        if self.applicable and self.passed:
            return "HUMAN_REVIEW_EVIDENCE_READY"
        return ""


def _norm(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _first(op: Operation, *keys: str) -> Any:
    for key in keys:
        if key in op.facts:
            return op.facts.get(key)
    return None


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != [] and value != {}


def requests_review_ready_transition(op: Operation) -> tuple[bool, str]:
    action = _norm(op.action)
    target = _norm(_first(
        op, "target_state", "requested_state", "state_transition_to",
        "desired_state", "close_state",
    ))
    requested = action in TERMINAL_ACTIONS or target in TERMINAL_STATES
    return requested, target or action


def artifact_class(op: Operation) -> str:
    raw = _norm(_first(op, "artifact_class", "output_class", "deliverable_type"))
    if not raw and bool(op.get("browser_renderable")):
        raw = "browser_renderable"
    if raw in _BROWSER:
        return "browser"
    if raw in _FILE:
        return "file"
    if raw in _RUNTIME:
        return "runtime"
    if raw in _MEDIA:
        return "media"
    return raw or "generic"


def _common_missing(op: Operation) -> List[str]:
    missing: List[str] = []
    packet = _first(op, "completion_evidence_packet", "completion_evidence", "human_review_packet")
    source_id = _first(op, "source_sha", "commit_sha", "build_sha", "artifact_version", "version")
    validation = _first(op, "validation_results", "validation_evidence", "test_results")
    if not _present(packet):
        missing.append("completion_evidence_packet")
    if not _present(source_id):
        missing.append("source_sha_or_version")
    if not _present(validation):
        missing.append("validation_results")
    # An empty list is a valid statement that no unresolved findings remain.
    if "unresolved_findings" not in op.facts:
        missing.append("unresolved_findings")
    return missing


def _surface_verified(op: Operation) -> bool:
    accessible = _first(op, "review_surface_accessible", "artifact_accessible")
    probe = _norm(_first(op, "review_surface_probe_status", "accessibility_probe_status"))
    evidence = _first(op, "review_surface_evidence_ref", "accessibility_evidence_ref")
    return (accessible is True or probe == "pass") and _present(evidence)


def _browser_missing(op: Operation) -> List[str]:
    missing = _common_missing(op)
    preview = _first(op, "preview_url", "review_preview_url")
    bundle = _first(op, "preview_bundle", "review_bundle", "review_artifact")
    review_index = _first(op, "review_index", "review_index_url", "review_index_ref")
    desktop = _first(op, "desktop_screenshots", "desktop_screenshot")
    mobile = _first(op, "mobile_screenshots", "mobile_screenshot")
    manifest = _first(op, "artifact_hash_manifest", "hash_manifest", "preview_manifest")

    expires = _first(op, "review_surface_expires_at", "preview_expires_at")
    if expires is not None:
        try:
            if float(op.at) >= float(expires):
                missing.append("review_surface_not_expired")
        except (TypeError, ValueError):
            missing.append("review_surface_expiry_valid")

    if not (_present(preview) or (_present(bundle) and _present(review_index))):
        missing.append("working_preview_or_bundle_with_review_index")
    if not _surface_verified(op):
        missing.append("review_surface_accessibility_evidence")
    if not _present(desktop):
        missing.append("desktop_screenshots")
    if bool(_first(op, "mobile_in_scope", "responsive_scope")) and not _present(mobile):
        missing.append("mobile_screenshots")
    if not _present(manifest):
        missing.append("artifact_hash_manifest")
    return missing


def _file_missing(op: Operation) -> List[str]:
    missing = _common_missing(op)
    artifact = _first(op, "review_artifact", "artifact_url", "artifact_ref", "download_artifact")
    if not _present(artifact):
        missing.append("openable_or_downloadable_artifact")
    if not _surface_verified(op):
        missing.append("review_surface_accessibility_evidence")
    if bool(op.get("rendered_preview_required")) and not _present(
        _first(op, "rendered_preview", "preview_url", "preview_artifact")
    ):
        missing.append("rendered_preview")
    return missing


def _runtime_missing(op: Operation) -> List[str]:
    missing = _common_missing(op)
    if not _present(_first(op, "runtime_evidence", "runtime_query_evidence", "expected_actual_evidence")):
        missing.append("runtime_query_or_expected_actual_evidence")
    if not _present(_first(op, "runtime_identity", "migration_identity", "deployment_identity")):
        missing.append("runtime_or_migration_identity")
    return missing


def _media_missing(op: Operation) -> List[str]:
    missing = _common_missing(op)
    media = _first(op, "review_artifact", "playable_artifact", "viewable_artifact")
    manifest = _first(op, "artifact_hash_manifest", "hash_manifest", "media_manifest")
    if not _present(media):
        missing.append("playable_or_viewable_artifact")
    if not _surface_verified(op):
        missing.append("review_surface_accessibility_evidence")
    if not _present(manifest):
        missing.append("manifest_or_provenance")
    return missing


def validate_closeout(op: Operation) -> ClosureEvidenceResult:
    requested, target = requests_review_ready_transition(op)
    if not requested:
        return ClosureEvidenceResult(applicable=False, passed=True)

    # Explicitly non-substantive administrative transitions can opt out, but
    # the fact must be present. Absence does not imply non-substantive.
    if op.facts.get("substantive") is False:
        return ClosureEvidenceResult(
            applicable=True, passed=True, artifact_class="non_substantive",
            target_state=target, detail="non-substantive closeout transition",
        )

    kind = artifact_class(op)
    if kind == "browser":
        missing = _browser_missing(op)
    elif kind == "file":
        missing = _file_missing(op)
    elif kind == "runtime":
        missing = _runtime_missing(op)
    elif kind == "media":
        missing = _media_missing(op)
    else:
        missing = _common_missing(op)
        direct = _first(op, "direct_human_review_link", "review_artifact", "review_artifact_ref")
        if not _present(direct):
            missing.append("direct_human_review_artifact")

    refs = []
    for key in (
        "completion_evidence_packet", "completion_evidence", "human_review_packet",
        "review_surface_evidence_ref", "accessibility_evidence_ref", "preview_url",
        "review_bundle", "review_artifact", "review_index", "artifact_hash_manifest",
        "hash_manifest", "runtime_evidence",
    ):
        value = op.facts.get(key)
        if _present(value):
            if isinstance(value, (list, tuple)):
                refs.extend(str(v) for v in value)
            else:
                refs.append(str(value))

    passed = not missing
    detail = (
        "human-review evidence contract satisfied"
        if passed else
        "human-review evidence pending: " + ", ".join(missing)
    )
    return ClosureEvidenceResult(
        applicable=True,
        passed=passed,
        artifact_class=kind,
        target_state=target,
        missing=tuple(missing),
        evidence_refs=tuple(refs),
        detail=detail,
    )
