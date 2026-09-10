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
    transition_step,
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
        self.assertEqual(normalized["definition_fingerprint"], normalize_template(base_template())["definition_fingerprint"])

    def test_all_planned_template_types_are_valid(self):
        for template_type in ["MAKE", "FIX", "REVIEW", "RELEASE", "MONITOR", "ROUTINE", "RESEARCH", "COMMUNICATE", "DECIDE", "DO"]:
            with self.subTest(template_type=template_type):
                self.assertEqual(validate_template_payload(base_template(template_type=template_type)), [])

    def test_child_cannot_weaken_parent_controls(self):
        parent = normalize_template(base_template())
        child = base_template(template_id="CHILD-REVIEW", parent_controls={
            "approval_required": False,
            "evidence_required": True,
            "security_required": True,
            "rollback_required": True,
        })
        self.assertIn("weakened:approval_required", validate_template_payload(child, parent))
        with self.assertRaisesRegex(ValueError, "weakened:approval_required"):
            effective_controls(parent["effective_controls"], child["parent_controls"])

    def test_secret_and_duplicate_step_rejected(self):
        self.assertIn("secret_prohibited", validate_template_payload(base_template(scope="api_key=do-not-store")))
        payload = base_template()
        payload["steps"] = [payload["steps"][0], dict(payload["steps"][0])]
        self.assertIn("duplicate_step_id:inspect", validate_template_payload(payload))

    def test_a3_requires_explicit_approval_flag(self):
        payload = base_template()
        payload["steps"][0] = {**payload["steps"][0], "autonomy_class": "A3_APPROVAL_REQUIRED", "approval_required": False}
        self.assertIn("approval_required_for_a3:inspect", validate_template_payload(payload))

    def test_a4_cannot_advance_success_path(self):
        payload = base_template()
        payload["steps"][0] = {**payload["steps"][0], "autonomy_class": "A4_PROHIBITED", "next_step_on_success": "decide"}
        self.assertIn("prohibited_step_cannot_advance:inspect", validate_template_payload(payload))


class WorkflowInstanceTests(unittest.TestCase):
    def setUp(self):
        self.template = normalize_template(base_template())

    def _binding(self, **overrides):
        binding = {
            "context_type": "project",
            "context_ref": "project:escd",
            "bindings": {"target": "ESCD"},
            "source_refs": ["github:issue-70"],
            "job_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
        }
        binding.update(overrides)
        return binding

    def test_instance_binds_exact_template_version_context_and_job(self):
        instance = instantiate_workflow(self.template, self._binding())
        self.assertEqual(instance["template_id"], "BASE-REVIEW")
        self.assertEqual(instance["template_version"], "1.0.0")
        self.assertEqual(instance["template_fingerprint"], self.template["definition_fingerprint"])
        self.assertEqual(instance["job_id"], "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
        self.assertTrue(instance["execution_authorized"])
        self.assertEqual(instance["status"], "planned")

    def test_approved_template_without_job_is_plan_only(self):
        instance = instantiate_workflow(self.template, self._binding(job_id=None))
        self.assertFalse(instance["execution_authorized"])

    def test_candidate_template_does_not_claim_execution_authority(self):
        template = normalize_template(base_template(status="candidate"))
        instance = instantiate_workflow(template, self._binding(context_type="general", context_ref="candidate:test"))
        self.assertFalse(instance["execution_authorized"])

    def test_missing_required_binding_blocks_instantiation(self):
        with self.assertRaisesRegex(ValueError, "workflow_binding_missing:target"):
            instantiate_workflow(self.template, self._binding(bindings={}))

    def test_unsupported_context_blocks_instantiation(self):
        with self.assertRaisesRegex(ValueError, "unsupported_context_type"):
            instantiate_workflow(self.template, self._binding(context_type="person", context_ref="person:1"))

    def test_instance_key_is_deterministic(self):
        first = instantiate_workflow(self.template, self._binding())
        second = instantiate_workflow(self.template, self._binding())
        self.assertEqual(first["instance_key"], second["instance_key"])

    def test_step_readiness_respects_dependencies_approval_and_prohibited(self):
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

        prohibited = [{**steps[0], "autonomy_class": "A4_PROHIBITED", "status": "pending"}]
        self.assertEqual(step_readiness(prohibited)[0]["blocked_reason"], "prohibited_action")

    def test_next_step_is_deterministic(self):
        steps = [{"step_id": "b", "sequence_no": 2, "status": "ready"}, {"step_id": "a", "sequence_no": 1, "status": "ready"}]
        self.assertEqual(next_step(steps)["step_id"], "a")

    def test_transition_contracts_block_shortcuts(self):
        self.assertEqual(transition_instance("planned", "running"), (True, "allowed"))
        self.assertEqual(transition_instance("planned", "completed"), (False, "invalid_workflow_transition"))
        self.assertEqual(transition_instance("completed", "running"), (False, "invalid_workflow_transition"))
        self.assertEqual(transition_step("ready", "running"), (True, "allowed"))
        self.assertEqual(transition_step("pending", "completed"), (False, "invalid_workflow_step_transition"))

    def test_operator_view_exposes_template_step_and_control_state(self):
        instance = instantiate_workflow(self.template, self._binding())
        instance["id"] = "wf-1"
        view = workflow_view(instance, self.template, step_readiness(instantiate_steps(self.template, "wf-1")))
        self.assertTrue(view["operator_can_inspect"])
        self.assertFalse(view["external_execution_performed"])
        self.assertEqual(view["template"]["version"], "1.0.0")
        self.assertEqual(view["next_step"]["step_id"], "inspect")

    def test_stable_fingerprint_is_order_independent_for_dicts(self):
        self.assertEqual(stable_fingerprint({"a": 1, "b": 2}), stable_fingerprint({"b": 2, "a": 1}))


if __name__ == "__main__":
    unittest.main()
