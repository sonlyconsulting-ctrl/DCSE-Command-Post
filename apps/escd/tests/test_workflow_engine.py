from __future__ import annotations

import unittest

from apps.escd.runtime.workflow_engine import (
    effective_controls,
    instantiate_steps,
    instantiate_workflow,
    next_step,
    normalize_template,
    stable_fingerprint,
    step_readiness,
    transition_instance,
    validate_template_payload,
    workflow_view,
)


def base_template(**overrides):
    payload = {
        "template_id": "BASE-REVIEW",
        "name": "Base Review",
        "version": "1.0.0",
        "status": "approved",
        "template_type": "REVIEW",
        "purpose": "Review a governed target",
        "scope": "general",
        "supported_context_types": ["project", "document", "general"],
        "input_contract": {"required": ["target"]},
        "required_sources": ["source-native"],
        "preconditions": [],
        "steps": [
            {
                "step_id": "inspect",
                "sequence_or_dependency": 1,
                "action_type": "REVIEW",
                "instruction": "Inspect the target against the supplied source.",
                "input_refs": ["target"],
                "output_contract": {"required": ["findings"]},
                "executor": "assistant",
                "autonomy_class": "A0_AUTO",
                "approval_required": False,
                "verification_method": "source_reconciliation",
                "evidence_required": True,
                "failure_route": "stop_with_evidence",
                "next_step_on_success": "decide",
                "next_step_on_failure": None,
            },
            {
                "step_id": "decide",
                "sequence_or_dependency": ["inspect"],
                "action_type": "DECIDE",
                "instruction": "Prepare the decision packet.",
                "input_refs": ["findings"],
                "output_contract": {"required": ["recommendation"]},
                "executor": "assistant",
                "autonomy_class": "A2_PROPOSE",
                "approval_required": True,
                "verification_method": "dcs_confirmed",
                "evidence_required": True,
                "failure_route": "waiting_approval",
                "next_step_on_success": None,
                "next_step_on_failure": None,
            },
        ],
        "decision_points": ["decide"],
        "approval_points": ["decide"],
        "executor_classes": ["assistant"],
        "connector_requirements": [],
        "evidence_requirements": ["source_reconciliation"],
        "test_requirements": ["deterministic", "approval_gate"],
        "rollback_or_recovery": "resume from last verified step",
        "exit_criteria": ["review evidence recorded"],
        "follow_up_rules": [],
        "notification_policy": "N1",
        "lane_restrictions": ["no protected-lane crossover"],
        "retry_policy": {"max_attempts": 2},
        "owner": "DCS",
        "provenance": ["DCSE-ESCD-001_WORKFLOW_TEMPLATE_SCHEMA.md"],
        "parent_controls": {
            "approval_required": True,
            "evidence_required": True,
            "security_required": True,
            "rollback_required": True,
        },
    }
    payload.update(overrides)
    return payload


class WorkflowTemplateTests(unittest.TestCase):
    def test_normalize_preserves_identity_and_fingerprint(self):
        normalized = normalize_template(base_template())
        self.assertEqual(normalized["template_id"], "BASE-REVIEW")
        self.assertEqual(normalized["version"], "1.0.0")
        self.assertEqual(normalized["template_type"], "REVIEW")
        self.assertEqual(len(normalized["definition_fingerprint"]), 64)
        again = normalize_template(base_template())
        self.assertEqual(normalized["definition_fingerprint"], again["definition_fingerprint"])

    def test_all_planned_template_types_are_valid(self):
        for template_type in ["MAKE", "FIX", "REVIEW", "RELEASE", "MONITOR", "ROUTINE", "RESEARCH", "COMMUNICATE", "DECIDE", "DO"]:
            with self.subTest(template_type=template_type):
                self.assertEqual(validate_template_payload(base_template(template_type=template_type)), [])

    def test_child_cannot_weaken_parent_controls(self):
        parent = normalize_template(base_template())
        child = base_template(
            template_id="CHILD-REVIEW",
            version="1.0.0",
            parent_controls={
                "approval_required": False,
                "evidence_required": True,
                "security_required": True,
                "rollback_required": True,
            },
        )
        errors = validate_template_payload(child, parent)
        self.assertIn("weakened:approval_required", errors)
        with self.assertRaisesRegex(ValueError, "weakened:approval_required"):
            effective_controls(parent["effective_controls"], child["parent_controls"])

    def test_secret_like_template_content_is_rejected(self):
        payload = base_template(scope="api_key=do-not-store")
        self.assertIn("secret_prohibited", validate_template_payload(payload))

    def test_duplicate_step_id_is_rejected(self):
        payload = base_template()
        payload["steps"] = [payload["steps"][0], dict(payload["steps"][0])]
        self.assertIn("duplicate_step_id:inspect", validate_template_payload(payload))


class WorkflowInstanceTests(unittest.TestCase):
    def setUp(self):
        self.template = normalize_template(base_template())

    def test_instance_binds_exact_template_version_and_context(self):
        instance = instantiate_workflow(self.template, {
            "context_type": "project",
            "context_ref": "project:escd",
            "bindings": {"target": "ESCD"},
            "source_refs": ["github:issue-70"],
        })
        self.assertEqual(instance["template_id"], "BASE-REVIEW")
        self.assertEqual(instance["template_version"], "1.0.0")
        self.assertEqual(instance["template_fingerprint"], self.template["definition_fingerprint"])
        self.assertTrue(instance["execution_authorized"])
        self.assertEqual(instance["status"], "planned")

    def test_candidate_template_does_not_claim_execution_authority(self):
        template = normalize_template(base_template(status="candidate"))
        instance = instantiate_workflow(template, {
            "context_type": "general",
            "context_ref": "candidate:test",
            "bindings": {"target": "test"},
            "source_refs": ["test:source"],
        })
        self.assertFalse(instance["execution_authorized"])

    def test_missing_required_binding_blocks_instantiation(self):
        with self.assertRaisesRegex(ValueError, "workflow_binding_missing:target"):
            instantiate_workflow(self.template, {
                "context_type": "project",
                "context_ref": "project:escd",
                "bindings": {},
                "source_refs": ["github:issue-70"],
            })

    def test_unsupported_context_blocks_instantiation(self):
        with self.assertRaisesRegex(ValueError, "unsupported_context_type"):
            instantiate_workflow(self.template, {
                "context_type": "person",
                "context_ref": "person:1",
                "bindings": {"target": "person:1"},
                "source_refs": ["contacts:1"],
            })

    def test_instance_key_is_deterministic(self):
        binding = {
            "context_type": "project",
            "context_ref": "project:escd",
            "bindings": {"target": "ESCD"},
            "source_refs": ["github:issue-70"],
        }
        first = instantiate_workflow(self.template, binding)
        second = instantiate_workflow(self.template, binding)
        self.assertEqual(first["instance_key"], second["instance_key"])

    def test_step_readiness_respects_dependencies_and_approval(self):
        steps = instantiate_steps(self.template, "wf-1")
        prepared = step_readiness(steps)
        self.assertEqual(prepared[0]["status"], "ready")
        self.assertEqual(prepared[1]["status"], "pending")

        prepared[0]["status"] = "completed"
        no_approval = step_readiness(prepared)
        decide = [x for x in no_approval if x["step_id"] == "decide"][0]
        self.assertEqual(decide["status"], "waiting_approval")

        approved = step_readiness(prepared, approvals=[{"status": "approved", "action_key": "workflow_step:decide"}])
        decide = [x for x in approved if x["step_id"] == "decide"][0]
        self.assertEqual(decide["status"], "ready")

    def test_next_step_is_deterministic(self):
        steps = [
            {"step_id": "b", "sequence_no": 2, "status": "ready"},
            {"step_id": "a", "sequence_no": 1, "status": "ready"},
        ]
        self.assertEqual(next_step(steps)["step_id"], "a")

    def test_transition_contract_blocks_invalid_shortcut(self):
        self.assertEqual(transition_instance("planned", "running"), (True, "allowed"))
        self.assertEqual(transition_instance("planned", "completed"), (False, "invalid_workflow_transition"))
        self.assertEqual(transition_instance("completed", "running"), (False, "invalid_workflow_transition"))

    def test_operator_view_exposes_template_step_and_control_state(self):
        instance = instantiate_workflow(self.template, {
            "context_type": "project",
            "context_ref": "project:escd",
            "bindings": {"target": "ESCD"},
            "source_refs": ["github:issue-70"],
        })
        instance["id"] = "wf-1"
        steps = step_readiness(instantiate_steps(self.template, "wf-1"))
        view = workflow_view(instance, self.template, steps)
        self.assertTrue(view["operator_can_inspect"])
        self.assertFalse(view["external_execution_performed"])
        self.assertEqual(view["template"]["version"], "1.0.0")
        self.assertEqual(view["next_step"]["step_id"], "inspect")

    def test_stable_fingerprint_is_order_independent_for_dicts(self):
        self.assertEqual(stable_fingerprint({"a": 1, "b": 2}), stable_fingerprint({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
