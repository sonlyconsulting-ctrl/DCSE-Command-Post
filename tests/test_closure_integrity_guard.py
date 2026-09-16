"""Regression tests for the DCSE Closure Integrity Guard.

Authority: DCS-DIR-20260906-002 + D21 + cross-system completion evidence contract.
Task: DCSE-CLOSURE-INTEGRITY-GUARD-20260915-01 / Issue #123.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "dcse"))

from model import ACTIVE, EXECUTE, PASS, REFUSE, Operation, Rule  # noqa: E402
from orchestrator import Orchestrator  # noqa: E402
from registry import Registry  # noqa: E402


def isolated_orchestrator() -> Orchestrator:
    """A truthy registry whose only rule is irrelevant to closeout tests."""
    reg = Registry()
    reg.register(Rule(
        id="TEST-IRRELEVANT-001",
        name="irrelevant test rule",
        applies_to=("knowledge",),
        actions=("noop",),
        check=lambda _op: PASS,
        lifecycle=ACTIVE,
    ))
    return Orchestrator(registry=reg)


def common_browser_facts() -> dict:
    return {
        "artifact_class": "browser_renderable",
        "substantive": True,
        "completion_evidence_packet": "issue://123/evidence",
        "source_sha": "a" * 40,
        "validation_results": ["browser-pass", "leak-pass"],
        "unresolved_findings": [],
        "artifact_hash_manifest": "artifact://preview-manifest",
        "desktop_screenshots": ["artifact://desktop/atlas.png"],
        "mobile_in_scope": True,
        "mobile_screenshots": ["artifact://mobile/atlas.png"],
        "review_surface_accessible": True,
        "review_surface_evidence_ref": "probe://review-surface-pass",
    }


class TestClosureIntegrityGuard(unittest.TestCase):

    def test_non_terminal_work_is_unchanged(self):
        op = Operation(
            entity="task",
            action="build",
            capabilities=("filehandling",),
            facts={"artifact_class": "browser_renderable"},
        )
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, EXECUTE)
        self.assertFalse(any(r.rule_id == "CLOSEOUT-HUMAN-REVIEW-001" for r in out.plan.results))

    def test_source_links_only_cannot_be_review_ready(self):
        op = Operation(
            entity="task",
            action="ready_for_dcs_review",
            facts={
                "artifact_class": "browser_renderable",
                "completion_evidence_packet": "issue://121/evidence",
                "source_sha": "b" * 40,
                "validation_results": ["tests-pass"],
                "unresolved_findings": [],
                "artifact_url": "https://github.example/source.html",
            },
        )
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, REFUSE)
        self.assertEqual(out.execution["state"], "TECHNICALLY_COMPLETE")
        self.assertEqual(out.execution["review_state"], "HUMAN_REVIEW_EVIDENCE_PENDING")
        self.assertIn("working_preview_or_bundle_with_review_index", out.execution["remediation_required"])

    def test_bundle_without_review_index_is_not_sufficient(self):
        facts = common_browser_facts()
        facts.update({
            "review_bundle": "artifact://persona-preview.zip",
        })
        op = Operation(entity="task", action="complete", facts=facts)
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, REFUSE)
        self.assertIn("working_preview_or_bundle_with_review_index", out.execution["remediation_required"])

    def test_expired_preview_invalidates_review_readiness(self):
        facts = common_browser_facts()
        facts.update({
            "preview_url": "https://preview.example/personas/",
            "review_surface_expires_at": 1000.0,
        })
        op = Operation(entity="task", action="ready_for_dcs_review", facts=facts, at=2000.0)
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, REFUSE)
        self.assertIn("review_surface_not_expired", out.execution["remediation_required"])

    def test_valid_self_contained_browser_review_package_passes(self):
        facts = common_browser_facts()
        facts.update({
            "review_bundle": "artifact://persona-preview.zip",
            "review_index": "artifact://persona-preview/review_index.html",
        })
        op = Operation(
            entity="task",
            action="ready_for_dcs_review",
            facts=facts,
        )
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, EXECUTE)
        guard = [r for r in out.plan.results if r.rule_id == "CLOSEOUT-HUMAN-REVIEW-001"]
        self.assertEqual(len(guard), 1)
        self.assertEqual(guard[0].verdict, PASS)

    def test_valid_database_runtime_evidence_does_not_require_browser_preview(self):
        op = Operation(
            entity="task",
            action="complete",
            facts={
                "artifact_class": "database",
                "substantive": True,
                "completion_evidence_packet": "tribunal://db-closeout",
                "source_sha": "c" * 40,
                "validation_results": ["query-pass", "advisor-pass"],
                "unresolved_findings": [],
                "runtime_evidence": "query://expected-actual",
                "migration_identity": "20260916000100_example",
            },
        )
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, EXECUTE)

    def test_empty_unresolved_findings_is_valid_evidence(self):
        facts = common_browser_facts()
        facts.update({
            "preview_url": "https://preview.example/review/",
            "unresolved_findings": [],
        })
        op = Operation(entity="task", action="complete", facts=facts)
        out = isolated_orchestrator().run(op, execute=False)
        self.assertEqual(out.disposition, EXECUTE)


if __name__ == "__main__":
    unittest.main()
