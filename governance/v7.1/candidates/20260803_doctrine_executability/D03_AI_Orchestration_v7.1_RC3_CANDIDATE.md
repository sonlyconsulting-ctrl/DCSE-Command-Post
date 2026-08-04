# DCSE Doctrine D03: AI Orchestration v7.1 RC3 Candidate

**Document ID:** DCSE-D03-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D03_AI_Orchestration.md`  
**Source SHA-256:** `a5ca6376ae4101571343d09794f00901097dae4e9184f3d710f84b3d0212290d`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D03 governs admission, context, capability selection, assignment, execution ownership, fallback, correction, validation routing, and closeout for AI models, agents, scripts, pollers, and human-assisted runtimes.

D03 coordinates work. It does not create constitutional, credential, database, deployment, publication, or promotion authority.

## 2. Orchestration principles

1. Assign by verified capability, access, risk, cost, and availability, not brand name.
2. Preserve one accountable owner for every active work item.
3. Use the minimum sufficient context without omitting controlling authority or evidence.
4. Resolve correctable issues within approved scope before escalating.
5. Isolate affected actions rather than stopping unrelated safe work.
6. Treat tool output as evidence only for the state it directly proves.
7. Separate execution, validation, promotion, deployment, and reconciliation.
8. Record limitations and unknowns without inventing identity, access, or completion.

## 3. Runtime admission contract

```yaml
runtime_admission:
  schema_version: "1.0"
  conversation_id: ""
  turn_id: ""
  task_id: ""
  assignment_id: ""
  entity: ""
  lane: ""
  classification: ""
  mode: "DISCUSS | PLAN | AUDIT | EXECUTE | REVIEW | DEPLOY | MONITOR"
  objective: ""
  exit_criteria: []
  release_posture: ""
  authority_ref: ""
  allowed_actions: []
  prohibited_actions: []
  required_sources: []
  required_capabilities: []
  required_access: []
  evidence_destinations: []
  rollback_ref: ""
  reserved_conditions: []
  accountable_owner: ""
  admitted_at: ""
```

The runtime scaffolds missing non-reserved structure when intent is clear. It must surface missing facts before affected actions involving authority, legality, confidentiality, PS or PPR boundaries, credentials, production, public release, destructive operations, or material spending.

## 4. Source loading

### 4.1 Constitutional bootstrap

Every substantive governed run resolves:

- current operational manifest;
- promoted Master Profile;
- D03;
- D21;
- D22;
- current doctrine catalog or package manifest.

D05 loads when baseline, promotion, rollback, supersession, or closeout is involved. D20 loads for product work. D13 and D14 load only inside an authorized protected PS context.

### 4.2 Source modes

Source retrieval follows D21 and D22:

- verified registry-primary mode when an approved adapter is available;
- GitHub or repository read-only mode;
- verified local or offline package mode.

No runtime is required to use a fixed Windows path, branch, vendor interface, or mailbox when another approved source mode is available.

### 4.3 Missing source

When a required source is missing:

1. record the exact source and attempted method;
2. identify actions dependent on that source;
3. retrieve another verified promoted representation when available;
4. continue safe discovery, evidence, correction, and recovery work;
5. prohibit only authority-dependent, irreversible, protected, production, or public actions affected by the gap;
6. trigger a reserved Stop-Gate only when no safe path exists or another reserved condition applies.

## 5. Minimum sufficient context

Context includes only what is necessary to execute accurately:

- controlling authority and doctrine;
- current objective and exit criteria;
- exact source artifacts and evidence;
- lane and confidentiality rules;
- relevant prior decisions and unresolved findings;
- target environment and access limitations;
- current product, branch, task, or runtime state.

Exclude unrelated history, cross-lane material, stale narrative, duplicate artifacts, secret values, and private reasoning.

Context reduction must not remove a dependency, exception, protected boundary, acceptance criterion, or authoritative correction that materially changes the task.

## 6. Capability catalog

### 6.1 Capability identity

```yaml
capability_profile:
  runtime_id: ""
  runtime_name: ""
  model_id: ""
  model_exposed: true
  capabilities: []
  tools: []
  access_scopes: []
  write_scopes: []
  sandbox_limits: []
  context_limit: ""
  cost_profile: ""
  availability: "UNKNOWN"
  reliability_evidence: []
  restrictions: []
  verified_at: ""
```

If the exact model is not exposed, set `model_exposed: false`. Do not infer model identity from interface branding.

### 6.2 Capability classes

Capabilities may include:

- architecture and planning;
- repository inspection and implementation;
- code generation and repair;
- deterministic test execution;
- database read, migration, and policy validation;
- browser and UI inspection;
- image, audio, or video work;
- document or spreadsheet production;
- adversarial review;
- research and source verification;
- communication and delivery;
- local or offline inference;
- monitoring and scheduled execution.

Vendor names may appear in runtime inventory and receipts. They must not become permanent constitutional duties.

## 7. Assignment and selection

### 7.1 Selection order

The orchestrator evaluates:

1. required capability;
2. required tool and environment access;
3. lane and classification eligibility;
4. independence requirement;
5. evidence of reliability for the task class;
6. availability and rate limits;
7. expected cost and resource use;
8. context capacity;
9. fallback and handoff cost.

The lowest-cost capable runtime is preferred when accuracy, access, risk, and completion requirements remain satisfied.

### 7.2 Assignment contract

```yaml
assignment:
  assignment_id: ""
  task_ref: ""
  objective: ""
  assigned_runtime: ""
  required_capabilities: []
  authority_ref: ""
  allowed_actions: []
  prohibited_actions: []
  source_refs: []
  expected_outputs: []
  acceptance_refs: []
  evidence_destination: ""
  timeout_or_review_point: ""
  fallback_candidates: []
  accountable_owner: ""
  assigned_at: ""
```

An assignment row, prompt, mailbox entry, or poller claim does not prove execution or completion.

## 8. Execution ownership and concurrency

- Every active task has one accountable owner.
- Multiple workers may contribute bounded subtasks with separate output ownership.
- Overlapping writes to the same file, record, migration, branch reference, or deployment are prohibited without an explicit coordination protocol.
- Pollers transport and claim work. They are not the source of truth.
- Duplicate claims use idempotency and lease controls where supported.
- A stale owner may be reassigned after verified timeout or failure under standing authority.
- Reassignment preserves prior evidence and records the reason.

## 9. Execution lifecycle

```text
INTAKE
  -> ADMIT
  -> ASSIGN
  -> CLAIM
  -> EXECUTE
  -> VERIFY
  -> CORRECT
  -> REVIEW
  -> READY_FOR_PROMOTION
  -> PROMOTE
  -> RECONCILE
  -> CLOSE
```

Exceptional states include `DEFERRED_NONBLOCKING`, `BLOCKED_CAPABILITY`, `BLOCKED_RESERVED`, `FAILED_RETRYABLE`, `FAILED_FINAL`, and `DRIFT`.

D03 controls progression through execution and review. D05 controls promotion. D22 controls reconciliation.

## 10. Resolution-first behavior

When execution encounters a problem:

1. verify the failure and affected scope;
2. inspect available evidence and governing rules;
3. attempt safe correction within approved authority;
4. retry only the affected operation;
5. run relevant regression checks;
6. select a capable fallback when the failure is capability or availability related;
7. record remaining findings and continue unaffected work;
8. escalate only reserved decisions or issues with no safe resolution path.

The runtime must not ask the user to choose implementation details that can be resolved objectively within approved scope.

## 11. Fallback and reassignment

Named-runtime unavailability is not a constitutional Stop-Gate.

Fallback must preserve:

- lane and classification;
- required capabilities and access;
- task scope and authority;
- source identity;
- evidence produced so far;
- independence requirements;
- cost or resource limits;
- accountable identity.

A chat-only model must not be assigned autonomous polling, database, GitHub, or filesystem duties unless the active environment provides and verifies those tools.

False claims of execution are findings. Repeated unsupported operational claims remove that runtime from affected autonomous task classes until capability is reverified.

## 12. Prompt and instruction wrapper

D03 uses one provider-neutral logical wrapper. Adapters may translate it to provider-specific syntax.

```yaml
instruction_wrapper:
  schema_version: "1.0"
  entity: ""
  lane: ""
  classification: ""
  mode: ""
  objective: ""
  exit_criteria: []
  authority_ref: ""
  allowed_actions: []
  prohibited_actions: []
  source_refs: []
  evidence_requirements: []
  output_contract: ""
  constraints: []
  rollback_ref: ""
  next_action_if_blocked: ""
```

Provider wrappers must not alter authority, lane, scope, or acceptance criteria.

## 13. Truthful posture and communication

Forward-thinking language must not conceal present state.

Required communication order is:

1. verified current condition;
2. likely explanation clearly labeled;
3. unknowns clearly labeled;
4. correction or next executable state;
5. authority or action required, if any.

Blocked, failed, stale, missing, or incomplete conditions must be stated plainly. Constructive framing may follow the factual condition but cannot replace it.

D08 governs voice and tone. D01 governs forward reasoning. D04 governs delivery and acknowledgment.

## 14. Tools, access, and credentials

Before using a modifying tool, the runtime verifies:

- target system and environment;
- permitted action and scope;
- lane and classification;
- authentication method;
- secret-exposure risk;
- rollback or recovery;
- destructive or irreversible effect;
- required evidence.

Secrets are not reproduced in prompts, doctrine, logs, source, receipts, screenshots, or handoffs. Runtimes receive approved scoped interfaces or secured-location references.

Ordinary use of already configured task-relevant credentials is permitted within assigned scope. New credential authority, privilege expansion, or repurposing credentials outside their configured purpose requires the applicable decision.

## 15. Validation and independence

- Execution and validation are separate roles even when the same runtime performs a disclosed self-check.
- Anonymous or null validators are prohibited.
- Independent validation is required only when the governing rule, risk, or standing authority requires it.
- A capable attributable substitute is selected when a preferred reviewer is unavailable.
- Review validates evidence and recommends disposition. It does not promote.
- Direct DCS attestation may substitute only when expressly recorded.

## 16. Evidence contract

```yaml
execution_receipt:
  schema_version: "1.0"
  task_ref: ""
  assignment_ref: ""
  runtime_identity: ""
  model_exposed: true
  source_refs: []
  authority_ref: ""
  actions_attempted: []
  actions_completed: []
  tool_results: []
  output_refs: []
  test_results: []
  findings: []
  corrections: []
  access_limitations: []
  unresolved_items: []
  disposition: ""
  accountable_identity: ""
  started_at: ""
  completed_at: ""
```

The receipt records decision inputs and outcomes, not private chain-of-thought.

## 17. Communication-state distinction

D03 and D04 distinguish:

- created;
- queued;
- dispatched;
- delivered;
- acknowledged;
- claimed;
- executing;
- output submitted;
- validated;
- promoted;
- reconciled.

No earlier state proves a later state. A mailbox insert does not prove delivery, and a heartbeat does not prove task completion.

## 18. Model and tool capability watch

Capability review is event-driven and scheduled according to operational value. It is not required at every conversation open.

Review triggers include:

- version change;
- model deprecation or access change;
- repeated task failure;
- material cost change;
- new required capability;
- security or policy change;
- planned quarterly or release-cycle review.

Each update report records verified source, observed change, affected capabilities, cost or risk effect, candidate routing changes, and required doctrine review. A vendor announcement alone does not alter promoted doctrine.

## 19. Voice and transcription safeguard

Voice, dictation, and typed prompts are instruction interfaces. They do not expand authority.

Durable confirmation is required when a plausible transcription error could materially affect:

- target or scope;
- credentials or access;
- production deployment;
- migration or deletion;
- public publication;
- spending;
- promotion;
- PS or PPR boundaries.

Clear bounded instructions proceed without repetitive confirmation.

## 20. Error taxonomy

| Error | State | Response |
|---|---|---|
| Missing capability | `BLOCKED_CAPABILITY` | Reassign or select fallback. |
| Temporary provider failure | `FAILED_RETRYABLE` | Bounded retry, then fallback. |
| Missing authority | `BLOCKED_RESERVED` only when action is reserved | Continue non-reserved work. |
| Missing evidence | `CORRECT` or `INSUFFICIENT_EVIDENCE` | Retrieve, test, or disclose gap. |
| Source mismatch | `DRIFT` | Last verified promoted source controls; D22 reconciles. |
| Tool permission denial | Scope-specific blocked state | Preserve result and route only required authority. |
| Secret or protected-lane exposure | `BLOCKED_RESERVED` | Contain affected material and follow security or lane controls. |
| Unsupported execution claim | Validation failure | Correct status and reverify capability. |

## 21. Closeout

A governed closeout records:

- objective and final disposition;
- outputs and exact locations;
- tests and validation;
- GitHub commit and PR state when applicable;
- Supabase write and reconciliation state when applicable;
- delivery and acknowledgment state;
- remaining findings and remediation owners;
- rollback readiness;
- resource and cost observations;
- next executable state.

No Supabase insert is claimed when none occurred. No GitHub update is claimed without remote verification.

## 22. Implementation contract

A reusable D03 module must expose equivalent functions:

```python
admit_runtime(request, authority_context) -> RuntimeAdmission
load_required_sources(admission, source_adapters) -> SourceLoadResult
build_context(admission, sources, evidence) -> ContextPackage
resolve_capabilities(task, runtime_catalog) -> CapabilityMatch
assign_task(task, capability_match, authority_context) -> Assignment
claim_task(assignment, lease_adapter) -> ClaimResult
classify_failure(result, context) -> FailureClass
select_fallback(assignment, runtime_catalog, failure) -> FallbackResult
route_validation(output, risk_profile) -> ValidationAssignment
build_execution_receipt(context) -> ExecutionReceipt
build_closeout(context) -> CloseoutReceipt
```

Identical verified inputs and catalogs must produce deterministic admission, routing, and state classifications.

## 23. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D03-001 | Clear bounded implementation request | Missing non-reserved structure scaffolded; execution proceeds. |
| D03-002 | Production target is ambiguous | Production action isolates; safe planning and testing continue. |
| D03-003 | Preferred named model unavailable | Capable attributable fallback selected. |
| D03-004 | Chat-only runtime claims poller execution | Claim rejected until tool evidence exists. |
| D03-005 | Runtime model identifier is hidden | `model_exposed: false`; no identity invented. |
| D03-006 | Required doctrine unavailable but verified copy exists | Verified fallback loads and work continues. |
| D03-007 | Required authority doctrine unavailable | Authority-dependent action pauses; safe evidence work continues. |
| D03-008 | Two workers would edit the same file | Work serialized or explicit coordination established. |
| D03-009 | Worker lease expires without output | Evidence preserved and task reassigned under standing authority. |
| D03-010 | Database insert succeeds | Insertion recorded; delivery, consumption, and completion not inferred. |
| D03-011 | Heartbeat is fresh | Liveness recorded; successful task output not inferred. |
| D03-012 | Correctable test failure occurs | Correct, reverify, and run affected regression tests. |
| D03-013 | Correction requires destructive action | Affected action routes reserved decision. |
| D03-014 | Reviewer identity is null | Validation is invalid and reassigned. |
| D03-015 | Vendor announces new model | Capability candidate recorded; doctrine does not change automatically. |
| D03-016 | Voice instruction may have changed deployment target | Durable confirmation required before deployment only. |
| D03-017 | Factual status is failed | Failure stated plainly with next executable state. |
| D03-018 | Secret appears in context | Secret excluded and affected scope contained. |
| D03-019 | PS source appears in general lane | Protected source isolates; unrelated general work continues. |
| D03-020 | Closeout has GitHub update but no Supabase write | Both states reported accurately and separately. |

## 24. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| Permanent tasks assigned to named vendors | Uses verified capability, access, risk, cost, and availability | Prevents model dependency and false assignment. |
| Unknown runtime identity causes halt | Records honest unknown identity and routes by capability | Branding does not prove model identity. |
| Startup requires v69 branch and local Windows paths | Uses promoted v7.1 source modes under D21 and D22 | Removes stale source authority. |
| Missing doctrine globally halts and writes physical files | Isolates dependent actions and uses approved adapters | Preserves safe non-stoppage. |
| Every session checks every vendor update | Uses event-driven and scheduled capability watch | Controls cost and noise. |
| Provider-specific prompt wrappers are constitutional | Defines provider-neutral wrapper with adapters | Preserves scope across runtimes. |
| Affirmative language suppresses negative status | Requires verified, likely, and unknown states before constructive next steps | Prevents misleading status reports. |
| Context rules lack exact admission schema | Adds runtime admission, assignment, capability, evidence, and closeout contracts | Enables automation. |
| Poller, mailbox, heartbeat, and output states are blurred | Separates communication and execution states | Prevents false completion claims. |
| Validation and promotion boundaries are incomplete | Integrates D05 and D22 and requires attributable validation | Prevents reviewer-created authority. |
| No concurrency or ownership contract | Adds owner, lease, idempotency, and overlapping-write rules | Prevents duplicate execution. |
| No executable acceptance suite | Adds D03-001 through D03-020 | Makes orchestration mechanically testable. |

## 25. Candidate disposition

**Disposition:** `D03_EXECUTABLE_ORCHESTRATION_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate with D04, D06, D15, D21, D22, and the manifest; run D03-001 through D03-020; obtain exact DCS decision.
