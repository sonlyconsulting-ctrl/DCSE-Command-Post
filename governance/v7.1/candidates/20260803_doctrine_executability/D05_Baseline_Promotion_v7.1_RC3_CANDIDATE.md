# DCSE Doctrine D05: Baseline and Promotion v7.1 RC3 Candidate

**Document ID:** DCSE-D05-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D05_Baseline_Promotion.md`  
**Source SHA-256:** `693eeb94440c3b048117cd2e471a7628127a5b4ab081c0ac2b58d837cac30e90`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Runtime candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime candidate SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D22 reconciliation is complete.  

## 1. Purpose

D05 defines one enterprise lifecycle and promotion service. It determines:

- when an object is merely changing operational state;
- when a validated object may advance under standing authority;
- when direct DCS approval is required;
- what evidence creates promotion certainty;
- how baselines are scoped and recorded;
- how supersession, rollback, recovery, and drift are controlled.

D05 removes unnecessary approval repetition without reducing authority certainty. Review, testing, merge, database insertion, deployment, or model agreement may support a transition. None independently creates promotion authority.

## 2. Governing principle

Promotion is based solely on DCS authority expressed in one of two forms:

1. `DIRECT_DCS`: DCS approves the exact object or exact diff.
2. `STANDING_DCSE`: a previously approved DCSE rule expressly covers the object class, Pass-Gate, evidence, limits, executor, and rollback.

`STANDING_DCSE` is delegated DCS authority embodied in a promoted rule. It is not independent authority held by an agent, model, poller, reviewer, repository, database, or automation.

## 3. Scope and doctrine boundaries

| Doctrine | D05 relationship |
|---|---|
| Master Profile | Establishes constitutional authority, reserved decisions, and lifecycle minimums. |
| D03 | Controls admission, assignment, capability, and orchestration. |
| D04 | Controls communication, delivery, acknowledgment, and receipts. |
| D16 | Produces DDNA candidates and evidence, then requests D05 lifecycle evaluation. |
| D20 | Produces product build and release evidence, then requests D05 lifecycle evaluation. |
| D21 | Executes D05 rules, validates state transitions, and emits evidence. |
| D22 | Binds authority to GitHub and runtime records and reconciles drift. |

Domain doctrines may define subject-specific acceptance criteria. They may not create a competing promotion authority or weaken D05 reserved conditions.

## 4. Controlled object identity

Every material lifecycle decision must identify the exact object.

```yaml
controlled_object:
  object_id: ""
  object_class: ""
  version: ""
  lane: ""
  classification: ""
  canonical_repository: ""
  canonical_path: ""
  branch_or_tag: ""
  commit_sha: ""
  content_sha256: ""
  lifecycle_state: ""
  supersedes: ""
  rollback_ref: ""
```

A candidate without sufficient identity may be validated and corrected, but it cannot become `PROMOTED`.

## 5. Transition classes

### 5.1 Operational transition

Operational transitions do not change constitutional authority, canonical promotion status, or release authority. Examples include:

- `QUEUED` to `RUNNING`;
- `RUNNING` to `VERIFYING`;
- `VERIFYING` to `CORRECTING`;
- evidence submission;
- retry or capable reassignment;
- remediation-task creation;
- `READY_FOR_REVIEW` to `REVIEWING`.

Operational transitions proceed under approved task scope. They require an attributable event, but no new promotion decision.

### 5.2 Routine promotion

A routine promotion may execute under `STANDING_DCSE` only when all of the following are true:

1. the object class is expressly eligible;
2. the Pass-Gate is named and mechanically testable;
3. required evidence is complete and retrievable;
4. an accountable validator is recorded when validation is required;
5. unresolved findings fall within the standing rule's tolerance;
6. rollback or recovery is defined;
7. no reserved condition is triggered;
8. the promotion receipt cites the exact standing-authority reference.

Typical eligible objects may include bounded evidence packets, routine task completion, sequential BOW release, non-destructive corrections with rollback, and internal artifacts expressly covered by the manifest.

### 5.3 Reserved direct promotion

`DIRECT_DCS` is required for:

- constitutional or Master Profile change;
- governance-framework promotion;
- authority expansion or exception;
- lane-boundary, PS, or PPR control change;
- production or public release not expressly covered by standing authority;
- material architecture replacement;
- destructive operation outside an approved procedure;
- material new spending;
- security exception;
- irreconcilable authoritative evidence;
- any object the applicable rule expressly reserves to DCS.

### 5.4 Constitutional promotion

A constitutional change always requires direct DCS approval of the exact content or exact diff. General direction, historical approval, model consensus, or standing routine authority is insufficient.

## 6. Authority certainty contract

```yaml
promotion_authority:
  schema_version: "1.0"
  authority_type: "DIRECT_DCS | STANDING_DCSE"
  authority_ref: ""
  authority_scope: ""
  object_ref: ""
  object_hash: ""
  pass_gate_ref: ""
  evidence_refs: []
  validator_ref: ""
  unresolved_findings: []
  rollback_ref: ""
  limits: []
  reserved_gate_scan: "NOT_RUN"
  accountable_executor: ""
  timestamp: ""
```

Certainty requires a resolvable authority reference, exact object identity, satisfied evidence conditions, and an attributable receipt. Formal ceremony, a named model, or repeated conversational approval is not required.

## 7. Lifecycle states

### 7.1 Artifact lifecycle

```text
DRAFT
  -> CANDIDATE
  -> VALIDATING
  -> READY_FOR_PROMOTION
  -> PROMOTED
  -> RELEASED
  -> RECONCILED
  -> SUPERSEDED
  -> ARCHIVED
```

Exceptional states are:

- `CORRECTING`;
- `DEFERRED_NONBLOCKING`;
- `BLOCKED_CAPABILITY`;
- `BLOCKED_RESERVED`;
- `DRIFT`;
- `ROLLED_BACK`.

### 7.2 State rules

- A validator may move a valid object to `READY_FOR_PROMOTION`.
- Only a valid authority record may move an object to `PROMOTED`.
- Release and promotion are separate states.
- D22 reconciliation is required before an enterprise closeout may claim `RECONCILED`.
- A rejected or insufficient object returns to `CORRECTING` when correction is authorized and possible.
- A nonblocking finding creates remediation without automatically preventing routine progression.

## 8. Promotion decision procedure

The D05 evaluator performs this sequence:

1. resolve the exact object identity;
2. classify the requested transition;
3. load the applicable standing authority and reserved conditions;
4. evaluate lane and confidentiality controls;
5. evaluate the named Pass-Gate;
6. verify evidence and attributable validation;
7. classify unresolved findings by actual effect;
8. verify rollback or recovery;
9. select `DIRECT_DCS`, `STANDING_DCSE`, or `NO_APPLICABLE_AUTHORITY`;
10. emit a deterministic disposition;
11. execute the transition only when the disposition permits it;
12. issue the receipt and route D22 reconciliation.

## 9. Deterministic dispositions

The evaluator returns exactly one primary disposition:

- `OPERATIONAL_TRANSITION_ALLOWED`;
- `ROUTINE_PROMOTION_ALLOWED`;
- `DIRECT_DCS_APPROVAL_REQUIRED`;
- `CORRECTION_REQUIRED`;
- `DEFERRED_NONBLOCKING`;
- `BLOCKED_CAPABILITY`;
- `BLOCKED_RESERVED`;
- `DRIFT_RECONCILIATION_REQUIRED`;
- `INSUFFICIENT_EVIDENCE`.

The disposition must include reasons, failed conditions, permissible corrections, and the next executable action.

## 10. Evidence and review

### 10.1 Evidence rule

Evidence is proportional to the object and risk. The evaluator must not require repository-wide checks for a bounded object unless a dependency or standing rule makes them relevant.

Required evidence may include:

- exact artifact and hashes;
- validation results;
- security and lane scans;
- accountable review receipt;
- unresolved-findings register;
- rollback or recovery proof;
- deployment or preview evidence when release is involved;
- GitHub and Supabase references when reconciliation is involved.

### 10.2 Review rule

Review validates completeness, accuracy, risk, and Pass-Gate satisfaction. Review does not create authority.

Independent review is required only when the governing risk rule, object class, or standing authority requires it. The executor may self-check but must disclose self-validation. Anonymous or null validation receipts are prohibited.

Named-model unavailability is not a Stop-Gate. D03 assigns another capable, attributable validator or routes a direct DCS attestation when expressly provided.

## 11. Findings and corrections

Findings block promotion only when they:

- violate an explicit Pass-Gate;
- trigger a reserved condition;
- create unresolved critical or high risk;
- compromise credentials, security, lane isolation, or confidentiality;
- require destructive action outside an approved procedure;
- make the object identity or evidence irreconcilable;
- invalidate rollback or recovery.

Other findings are recorded as remediation tasks and progression continues when the standing rule permits it.

When a correction is within approved scope, reversible, and does not alter a reserved decision, the responsible executor corrects it and reruns the affected checks without requesting a new conversational approval.

## 12. Baseline system

### 12.1 Baseline scopes

D05 recognizes:

| Scope | Use |
|---|---|
| `OBJECT` | One governed file, record, or artifact. |
| `PACKAGE` | A bounded set of interdependent artifacts. |
| `PRODUCT` | A product release and its required dependencies. |
| `SYSTEM` | A runtime, database, or infrastructure state. |
| `REPOSITORY` | A whole-repository constitutional or major release baseline. |

The smallest sufficient scope must be used. A whole-repository hash map is not required for every routine promotion.

### 12.2 Baseline receipt

```yaml
baseline_receipt:
  schema_version: "1.0"
  baseline_id: ""
  scope: "OBJECT | PACKAGE | PRODUCT | SYSTEM | REPOSITORY"
  object_refs: []
  included_hashes: []
  exclusions: []
  validation_refs: []
  authority_ref: ""
  created_by: ""
  created_at: ""
  rollback_ref: ""
  status: "CANDIDATE"
```

## 13. Modification, supersession, and clerical correction

Any byte change creates a new hash and must be recorded. The effect depends on change class:

- `MATERIAL`: new candidate and new promotion authority required.
- `CONSTITUTIONAL`: direct DCS exact-content approval required.
- `NON_SUBSTANTIVE`: may use a promoted clerical-correction rule if that rule defines permitted changes, validation, receipt, and rollback.
- `RUNTIME_RECORD_ONLY`: correctable through the approved adapter when the canonical artifact is unchanged.

No correction may be labeled clerical merely to avoid material review. The prior verified promoted version remains controlling until the replacement transition is valid.

## 14. Promotion receipt

```yaml
promotion_receipt:
  schema_version: "1.0"
  receipt_id: ""
  object_ref: ""
  object_version: ""
  object_hash: ""
  prior_state: ""
  resulting_state: ""
  authority_type: "DIRECT_DCS | STANDING_DCSE"
  authority_ref: ""
  pass_gate_ref: ""
  evidence_refs: []
  validator_ref: ""
  findings: []
  rollback_ref: ""
  github_ref: ""
  runtime_refs: []
  reconciliation_status: "PENDING"
  accountable_executor: ""
  timestamp: ""
```

The receipt contains references, not secret values or private reasoning.

## 15. Rollback and recovery

Every material promotion must define:

- prior verified state;
- affected objects and systems;
- restore mechanism;
- data compatibility requirements;
- verification checks;
- accountable executor;
- conditions that trigger rollback.

Rollback may execute automatically only when an approved procedure expressly authorizes it and the action remains within its limits. Otherwise, isolate the affected action and route the required decision.

Rollback is complete only after the restored state is verified and reconciled.

## 16. Drift control

Hash, lifecycle, or authority mismatch among GitHub, Supabase, local audit state, or deployment is `DRIFT`.

During drift:

1. preserve all conflicting identities;
2. rely on the last verified promoted source;
3. isolate only actions dependent on the mismatch;
4. continue unaffected safe work;
5. compare authority, commit, content hash, and runtime records;
6. correct through approved adapters;
7. issue a D22 reconciliation receipt.

Drift alone does not authorize a new promotion.

## 17. Missing D05 and degraded operation

If D05 is missing or unreadable:

- prohibit promotion, production release, destructive action, authority expansion, and irreversible lifecycle change;
- continue safe evidence collection, validation, correction, retrieval, and recovery work;
- retrieve the last verified promoted D05 when available;
- record the affected scope and recovery attempt;
- trigger a reserved Stop-Gate only when no safe path exists or another reserved condition applies.

Missing D05 does not require a global halt of unrelated safe work.

## 18. Implementation contract

A reusable D05 module must expose equivalent functions:

```python
classify_transition(request) -> TransitionClass
resolve_object_identity(request, adapters) -> ControlledObject
resolve_authority(object_ref, transition, authority_sources) -> AuthorityResult
evaluate_pass_gate(object_ref, gate_ref, evidence) -> GateResult
classify_findings(findings, governing_rule) -> FindingsResult
verify_rollback(rollback_ref) -> ValidationResult
decide_promotion(context) -> PromotionDisposition
build_baseline(scope, object_refs) -> BaselineReceipt
build_promotion_receipt(context, disposition) -> PromotionReceipt
request_reconciliation(receipt, adapters) -> ReconciliationRequest
```

The implementation must be deterministic for identical verified inputs and must not infer missing authority.

## 19. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D05-001 | Task moves from queued to running | `OPERATIONAL_TRANSITION_ALLOWED`; no promotion authority requested. |
| D05-002 | Routine evidence packet satisfies an exact standing rule | `ROUTINE_PROMOTION_ALLOWED`; authority reference recorded. |
| D05-003 | Routine packet has a nonblocking finding | Remediation created; progression continues if standing rule permits. |
| D05-004 | Constitutional doctrine changes | `DIRECT_DCS_APPROVAL_REQUIRED`. |
| D05-005 | Public release has no covering standing rule | `DIRECT_DCS_APPROVAL_REQUIRED`. |
| D05-006 | Named validator model unavailable | D03 selects capable attributable fallback; no standalone stop. |
| D05-007 | Validator identity is null | `INSUFFICIENT_EVIDENCE`; validation corrected. |
| D05-008 | Merge exists without authority reference | Object remains `READY_FOR_PROMOTION`. |
| D05-009 | Supabase row exists without authority reference | Object remains non-promoted. |
| D05-010 | Bounded object promotion requested | Object baseline used; repository-wide baseline not required. |
| D05-011 | Material change follows promotion | New candidate created; prior promoted version controls. |
| D05-012 | Authorized clerical correction satisfies exact rule | New hash recorded and correction receipt issued without full repromotion. |
| D05-013 | GitHub and runtime hashes disagree | `DRIFT_RECONCILIATION_REQUIRED`; dependent actions isolate. |
| D05-014 | Correctable test failure occurs within scope | Correction and affected-test rerun proceed without new approval. |
| D05-015 | D05 source unavailable | Promotion pauses; safe unrelated work continues. |
| D05-016 | Standing rule lacks object class or rollback | `DIRECT_DCS_APPROVAL_REQUIRED` or `INSUFFICIENT_EVIDENCE`; no inferred authority. |

## 20. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| Every promotion described as manual Level 0 decision | Adds direct and expressly delegated standing authority | Removes repetitive approvals while retaining DCS authority. |
| Whole repository baseline implied for every release | Adds proportional object, package, product, system, and repository scopes | Prevents unnecessary work and false dependency. |
| Review and approval boundaries incomplete | Separates validation from authority | Prevents reviewer-created promotion. |
| Any modification reverts without change classification | Adds material, constitutional, clerical, and runtime-record classes | Supports controlled correction without weakening hashes. |
| Findings lack proportional blocking rules | Adds actual-risk and Pass-Gate criteria | Prevents nonblocking findings from stopping approved objectives. |
| Missing D05 requires global HALT | Adds isolation-first degraded behavior | Preserves safe non-stoppage. |
| Receipt lacks standing-authority detail | Adds explicit authority and reconciliation contracts | Makes promotion mechanically certain. |
| D16 and D20 can appear to define separate approval gates | Makes domain doctrines consumers of D05 | Establishes one enterprise promotion service. |

## 21. Candidate disposition

**Disposition:** `D05_EXECUTABLE_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate against D16, D20, D21, D22, and the manifest; obtain exact DCS decision; promote through D22; run D05-001 through D05-016.
