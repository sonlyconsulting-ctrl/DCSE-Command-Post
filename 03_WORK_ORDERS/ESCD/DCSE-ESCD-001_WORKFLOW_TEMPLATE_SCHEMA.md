# ESCD WORKFLOW TEMPLATE SCHEMA

**Task ID:** DCSE-ESCD-001  
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

A workflow template is a reusable governed recipe, not a product-specific script. It MAY instantiate product-specific MAKE or FIX work, but the schema must also support REVIEW, RELEASE, MONITOR, ROUTINE, RESEARCH, COMMUNICATE, DECIDE, and general DO flows.

## Core principle

Separate:

`template definition -> instantiated workflow -> execution jobs -> evidence -> closeout`

Templates define how work should proceed. Instances bind the template to a specific product, project, asset, person, system, or task.

## Required template fields

- `template_id`: stable identifier
- `name`
- `version`
- `status`: draft/candidate/approved/superseded/archived
- `template_type`: MAKE/FIX/REVIEW/RELEASE/MONITOR/ROUTINE/RESEARCH/COMMUNICATE/DECIDE/DO
- `purpose`
- `scope`
- `supported_context_types`: product/project/asset/system/document/person/event/general
- `input_contract`
- `required_sources`
- `preconditions`
- `steps`
- `decision_points`
- `approval_points`
- `executor_classes`
- `connector_requirements`
- `evidence_requirements`
- `test_requirements`
- `rollback_or_recovery`
- `exit_criteria`
- `follow_up_rules`
- `notification_policy`
- `sensitivity/lane restrictions`
- `timeout/retry policy`
- `owner`
- `provenance`

## Step schema

Each step should contain:

- `step_id`
- `sequence_or_dependency`
- `action_type`
- `instruction`
- `input_refs`
- `output_contract`
- `executor`
- `autonomy_class`
- `approval_required`
- `verification_method`
- `evidence_required`
- `failure_route`
- `next_step_on_success`
- `next_step_on_failure`

## Product-specific MAKE/FIX binding

Product-specific behavior belongs in the workflow instance or a specialized child template.

Example:

`MAKE_PRODUCT_BASE` can be instantiated for a website, app, video, document, campaign, module, or database artifact by binding:

- product type
- baseline/reference assets
- entity/brand
- audience/destination
- architecture/technical requirements
- validation rules
- release destination

`FIX_PRODUCT_BASE` can be instantiated by binding:

- affected product/asset
- defect/problem statement
- known-good baseline
- severity
- reproduction evidence
- repair constraints
- regression surface
- rollback point

This avoids creating a separate workflow engine for every product while still allowing product-specific rules.

## Template inheritance

Allow controlled inheritance:

`BASE -> ENTITY -> PRODUCT_CLASS -> PRODUCT/PROJECT SPECIFIC`

Child templates may add requirements but must not silently weaken parent approval, security, evidence, or rollback controls.

## Rules

1. Template presence does not authorize execution.
2. Instantiation must resolve required context before execution.
3. Consequential steps must pass the autonomy contract.
4. Unknown required fields block only the affected step, not unrelated work.
5. Template versions are immutable after use; changes create a new version.
6. Every workflow instance records the exact template version used.
7. Product-specific exceptions must be explicit and provenance-linked.
8. Failed workflows retain evidence and resumable state.
9. No template may embed secrets.
10. Specialized builds such as DCS Employment may publish templates for ESCD integration without placing their domain logic inside ESCD core.
