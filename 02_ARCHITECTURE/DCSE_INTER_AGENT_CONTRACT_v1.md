# DCSE Provider-Neutral Inter-Agent Contract v1

**Task:** DCSE-ORCH-20260908-005  
**Lane:** DCSE / Command Post  
**Status:** CANDIDATE IMPLEMENTATION CONTRACT  
**Parent workstream:** GitHub Issue #56

## Purpose

Define the provider-neutral contract between the DCSE Universal Dispatch Controller, execution adapters, deterministic policy/rule gates, artifact handling, and receipts. Provider-specific CLI syntax belongs in adapters, not in the controller.

## Authority and boundaries

- Current GitHub governance and DCS directives control.
- AI may generate, analyze, and recommend. AI does not self-approve governance.
- Deterministic rules and policy gates decide whether progression is permitted.
- Logical agent identity remains separate from runtime/execution surface identity.
- Lane isolation, least privilege, Stop-Gates, credential containment, and publication controls are mandatory.
- Secrets must never be placed in task envelopes, artifacts, receipts, logs, GitHub, or Tribunal.
- PS access is denied unless explicitly authorized by controlling policy.

## Lifecycle

`TASK -> CLAIM -> EXECUTE -> ARTIFACT -> RECEIPT -> VALIDATE -> CONTINUE | RETRY | ESCALATE -> CLOSE`

Terminal failure states include `BLOCKED_POLICY`, `STOP_GATE`, `FAILED`, and `QUARANTINED` where supported by the controlling state machine.

## 1. TaskEnvelope

Required fields:

- `contract_version`
- `task_id`
- `workflow_id`
- `parent_task_id` when applicable
- `lane`
- `entity`
- `task_type`
- `capability_required`
- `priority`
- `authority_source[]`
- `instruction`
- `source_refs[]`
- `input_artifacts[]`
- `expected_outputs[]`
- `acceptance_criteria[]`
- `allowed_roots[]`
- `allowed_tools[]`
- `denied_tools[]`
- `secret_exposure`
- `ps_exposure`
- `approval_mode`
- `stop_gates[]`
- `timeout_seconds`
- `max_attempts`
- `cost_ceiling` when applicable
- optional `provider_preference[]`
- optional `model_preference[]`

Provider/model preference is advisory unless controlling policy explicitly binds it. Routing should primarily use required capability, authorization, health, cost, and availability.

## 2. ClaimContext

- `task_id`
- `claim_id`
- `claimed_by_agent`
- `runtime_surface`
- `session_id`
- `claimed_at`
- `lease_expires_at`
- `attempt`
- `working_directory`
- `effective_allowed_roots[]`
- `effective_policy_refs[]`

## 3. ArtifactManifest

Each produced artifact records:

- `artifact_id`
- `task_id`
- `artifact_type`
- `name`
- `path_or_uri`
- `mime_type`
- `sha256`
- `size_bytes`
- `created_at`
- `producer_agent`
- `runtime_surface`
- `source_refs[]`
- `sensitivity`
- `lane`
- `registry_candidate`
- `validation_status`

Artifacts are evidence-bearing outputs. Conversation text alone is not sufficient when the task requires a durable artifact.

## 4. ResultEnvelope

- `task_id`
- `claim_id`
- `session_id`
- `agent_id`
- `runtime_surface`
- `provider`
- `model` when known
- `started_at`
- `completed_at`
- `status`
- `summary`
- `artifacts[]`
- `evidence[]`
- `deterministic_checks[]`
- `warnings[]`
- `errors[]`
- `retry_recommendation`
- `usage` when available
- `raw_exit_code` when available

A provider's textual response must be normalized into this envelope before the controller evaluates progression.

## 5. Receipt

A receipt is immutable evidence of one governed execution attempt and records:

- `receipt_id`
- `task_id`
- `claim_id`
- `attempt`
- `agent_id`
- `runtime_surface`
- `contract_version`
- `task_envelope_sha256`
- `artifact_manifest_sha256`
- `result_envelope_sha256`
- `policy_decision`
- `validation_decision`
- `created_at`

## Deterministic gate sequence

1. Admission gate: schema, authority, lane, exposure flags, allowed roots, capability and runtime authorization.
2. Pre-execution gate: claim validity, lease, runtime health, provider capability, tool policy, timeout and cost controls.
3. Post-execution gate: exit state, required artifacts, hashes, output schema, acceptance checks and prohibited side effects.
4. Promotion gate: evidence sufficiency, registry metadata and required approval.
5. Publication gate: public destination, PS firewall, privacy, brand/evidence requirements and explicit approval where required.

## Provider adapter contract

Every adapter must expose equivalent behavior for:

- `probe()`
- `capabilities()`
- `execute(task, context)`
- `cancel()` when supported
- `normalizeResult()`
- `health()`

The adapter owns provider-specific invocation, process handling, structured output parsing and provider error normalization. It must not own enterprise routing, governance promotion, publication approval, or rule changes.

## Fail-closed requirements

- Unknown CLI flags or undocumented behavior must not be invented.
- Unknown exit-code semantics remain `UNKNOWN` until tested.
- Permission denial is evidence of a boundary, not evidence that an asset is absent.
- A registry row alone does not prove runtime admission.
- Runtime admission requires a real heartbeat plus successful governed claim, execution, artifact/receipt production, and deterministic validation.

## First certification case

The first bounded certification target is read-only Supabase enterprise discovery using the Antigravity `agy.exe` runtime. It must produce sanitized JSON and Markdown inventory artifacts, retain the validated discovery script as a reusable enterprise asset, expose no secrets or private object contents, perform no database writes, and return a deterministic receipt.

## Exit criteria

This contract becomes operative only after schema/implementation review and one end-to-end certification run proves the lifecycle without manual copy/paste between dispatch and worker execution. Until then, status remains CANDIDATE.