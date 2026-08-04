# DCSE Doctrine D21: Doctrine Runtime Engine v7.1 RC3 Candidate

**Document ID:** DCSE-D21-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS LEVEL 0 REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR firewalls  
**Authority holder:** DCS Level 0  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D21_Doctrine_Runtime_Engine.md`  
**Source SHA-256:** `11951eeb25ed215f61d2af7875c2a056a6ea1d9a82f6016cc35a95211ce92341`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate content and the promotion is reconciled under D05 and D22.  

## 1. Purpose

D21 defines the executable doctrine-runtime contract for every substantive governed task and conversation. It controls:

- task declaration and normalization;
- doctrine discovery and loading;
- deterministic doctrine routing;
- Doctrine Run Plan generation;
- Doctrine Consideration Log generation;
- capability and access validation;
- resolution-first behavior;
- artifact-scoped security and preview validation;
- change detection and doctrine replacement staging;
- lifecycle enforcement and promotion guarding;
- reconciliation and drift reporting;
- degraded and offline operation.

D21 specifies policy and logical contracts. A Python module or equivalent deterministic runtime implements those contracts. Neither D21 nor its implementation creates promotion authority.

## 2. Authority, precedence, and boundaries

### 2.1 Controlling authority

D21 is subordinate to the promoted Master Profile. D03 controls orchestration and admission. D05 controls baseline, promotion, rollback, and lifecycle authority. D22 controls canonical source identity, distribution, reconciliation, and drift.

When these sources conflict:

1. preserve the conflicting statements and identities;
2. apply the higher and more specific promoted authority;
3. isolate the affected action;
4. continue unaffected authorized work;
5. record the conflict in the DCL;
6. route irreconcilable authority conflicts to DCS.

### 2.2 Non-authority rule

The router, validator, reviewer, model, poller, repository, database, test harness, and runtime may produce evidence and recommendations. They cannot independently:

- promote doctrine;
- change lifecycle authority;
- waive a firewall or Stop-Gate;
- expand access;
- approve constitutional change;
- treat insertion, merge, deployment, or model consensus as authority.

The highest independent state produced by D21 is `READY_FOR_PROMOTION`.

### 2.3 Private reasoning boundary

D21 requires decision inputs, rules considered, evidence, actions, findings, and dispositions. It does not require private chain-of-thought or hidden reasoning content.

## 3. Runtime modes

The runtime operates in one of three source modes.

| Mode | Entry condition | Permitted behavior | Prohibited behavior |
|---|---|---|---|
| `REGISTRY_PRIMARY` | Approved schema adapter verified and registry reachable | Read verified registry metadata, load canonical content, generate plans and receipts, perform expressly authorized writes | Invented mappings or writes outside approved adapter |
| `REPOSITORY_READ_ONLY` | Canonical GitHub source available but registry unavailable or unverified | Inventory files, verify commits and hashes, route from repository metadata, generate local or repository receipts pending reconciliation | Registry writes, promotion, or claims that registry is reconciled |
| `OFFLINE_VERIFIED` | GitHub and registry unavailable but a promoted local copy and promotion evidence are verified | Load the last verified promoted copy, execute unaffected reversible work, create pending reconciliation records | New authority, promotion, distribution claims, or reliance on unverified local copies |

Mode changes must be recorded. Loss of one source does not create a global halt when a verified safe fallback exists.

## 4. Required runtime inputs

Every substantive run requires:

- task or conversation ID;
- objective and acceptance criteria;
- entity and lane;
- task type and artifact type;
- lifecycle phase;
- release posture;
- risk class;
- accountable execution identity;
- exposed runtime and model identity, when available;
- capability profile;
- access profile;
- source configuration;
- evidence destinations;
- rollback or recovery expectation.

Missing noncritical fields may be inferred only from verified context. Each inference must include its source, confidence category, and effect. Missing facts that affect authority, legality, confidentiality, PS or PPR isolation, material spending, destructive action, production or public release, deployment, or final disposition require an authority decision.

### 4.1 Task Declaration contract

```yaml
task_declaration:
  schema_version: "1.0"
  task_id: ""
  conversation_id: ""
  objective: ""
  acceptance_criteria: []
  entity: ""
  lane: ""
  task_type: ""
  artifact_type: ""
  lifecycle_phase: ""
  release_posture: ""
  risk_class: ""
  execution_identity: ""
  runtime_name: ""
  model_name: ""
  model_exposed: false
  capability_profile: []
  access_profile: []
  inferred_fields: []
  evidence_destinations: []
  rollback_expectation: ""
  timestamp: ""
```

Task types, artifact types, capability identifiers, and risk classes come from versioned logical catalogs. Hardcoded lists in prompts are fallback only.

## 5. Source loader and registry-schema adapter

### 5.1 Source priority

The loader resolves doctrine through:

1. promoted authority reference;
2. canonical GitHub repository, path, and commit;
3. approved runtime registry reference;
4. verified promoted local copy;
5. unpromoted repository discovery as candidate evidence only.

Search results, embeddings, summaries, caches, and model memory do not establish source authority.

### 5.2 Canonical doctrine identity

Every loaded doctrine must record:

- doctrine ID;
- title;
- version;
- lifecycle and promotion status;
- lane and firewall restrictions;
- repository and path;
- Git commit SHA;
- Git blob SHA when available;
- content SHA-256;
- promotion authority reference when promoted;
- supersedes and superseded-by references;
- executability status;
- source mode.

### 5.3 Registry-schema adapter

The router must not assume physical Supabase table names, columns, types, constraints, or enums.

Database-backed routing requires an approved versioned adapter derived from at least one verified controlling source:

- live read-only schema discovery;
- promoted migration;
- approved schema contract;
- verified database introspection receipt.

The adapter maps logical doctrine fields to physical storage and records:

- adapter ID and version;
- project and schema identity without secret values;
- source migration or introspection evidence;
- logical-to-physical field mapping;
- type and enum validation;
- read and write capabilities;
- validation timestamp;
- accountable validator;
- rollback or disable procedure.

If adapter verification fails, the runtime enters `REPOSITORY_READ_ONLY`. It may generate Doctrine Run Plans from canonical repository metadata but must set registry reconciliation to `UNKNOWN` and disable database writes.

### 5.4 Logical doctrine fields

The router requires these logical fields regardless of physical storage:

```yaml
doctrine_record:
  doctrine_id: ""
  title: ""
  version: ""
  lifecycle_status: ""
  promotion_status: ""
  entity_lanes: []
  firewall_flags: []
  topics: []
  task_triggers: []
  artifact_triggers: []
  lifecycle_triggers: []
  capability_requirements: []
  required_inputs: []
  required_outputs: []
  dependencies: []
  source_repository: ""
  source_path: ""
  source_commit: ""
  source_blob: ""
  content_sha256: ""
  executability_status: ""
  promotion_authority_ref: ""
```

## 6. Dynamic Doctrine Router

### 6.1 Always-on controls

Every substantive run loads or verifies:

- promoted Master Profile v7.1;
- D03 AI Orchestration;
- D21 Doctrine Runtime Engine;
- D22 Source Authority and Runtime Distribution;
- current doctrine registry or canonical package manifest.

D05 is added for baseline, review, promotion, rollback, supersession, and closeout. D20 is added for governed product assembly. D13 and D14 are excluded unless authorized PS mode is active.

The fixed always-on set is the constitutional bootstrap. Registry metadata may confirm it but cannot silently replace it.

### 6.2 Routing order

The router evaluates doctrine in this deterministic order:

1. verify source mode and Master Profile identity;
2. normalize the Task Declaration;
3. load the always-on controls;
4. inventory the current doctrine corpus;
5. verify doctrine identity and hashes;
6. filter by lifecycle and promotion status;
7. filter by entity and lane;
8. enforce PS, PPR, credential, and secret firewalls;
9. match task, artifact, lifecycle, and methodology triggers;
10. compare capability requirements with admitted runtime capabilities;
11. identify missing, conflicting, partial, descriptive-only, and drifting doctrine;
12. attach the executability wrapper where needed;
13. emit the Doctrine Run Plan before substantive execution.

### 6.3 Topic and trigger matching

Topic aliases and triggers must come from a versioned catalog or doctrine metadata. A built-in fallback catalog may be used only when:

- its version and hash are recorded;
- the canonical catalog is unavailable;
- the plan identifies `FALLBACK_TRIGGER_CATALOG`;
- no PS or PPR access is expanded;
- reconciliation is scheduled.

### 6.4 New doctrine discovery

A newly discovered doctrine is not automatically authoritative.

- If it has verified promotion authority and canonical identity, the router evaluates it normally.
- If it exists only in GitHub, the router records `UNREGISTERED_DISCOVERY` and treats it as candidate evidence.
- If it exists only in a registry, the router requires a resolvable canonical artifact and verified hash.
- If identity or authority cannot be verified, the doctrine is not applied to modifying execution.

Discovery creates a change record and reconciliation task. It does not create promotion.

### 6.5 Doctrine Run Plan contract

```yaml
doctrine_run_plan:
  schema_version: "1.0"
  plan_id: ""
  task_id: ""
  conversation_id: ""
  governance_version: "v7.1"
  source_mode: ""
  source_commit: ""
  task_declaration_ref: ""
  always_on: []
  selected: []
  evaluated_not_selected: []
  excluded_by_firewall: []
  reference_only: []
  missing: []
  conflicts: []
  drift: []
  wrappers_required: []
  unresolved_capabilities: []
  reserved_stop_gate: false
  reserved_stop_reason: ""
  evidence_refs: []
  router_version: ""
  generated_by: ""
  timestamp: ""
```

Each selected, excluded, or reference-only doctrine entry must identify the doctrine, source hash, decision reason, and applicable sections when available.

## 7. Doctrine Consideration Log

### 7.1 DCL contract

```yaml
doctrine_consideration_log:
  schema_version: "1.0"
  dcl_id: ""
  task_id: ""
  conversation_id: ""
  task_declaration_ref: ""
  doctrine_run_plan_ref: ""
  execution_identity: ""
  runtime_name: ""
  model_name: ""
  model_exposed: false
  execution_environment: ""
  source_mode: ""
  source_commit: ""
  timestamp: ""
  loaded: []
  applied: []
  evaluated_not_applied: []
  excluded_by_firewall: []
  reference_only: []
  missing: []
  conflicts: []
  gaps_detected: []
  methodology_triggers: []
  capability_events: []
  security_results: []
  preview_results: []
  issue_dispositions: []
  evidence_refs: []
  write_receipts: []
  lifecycle_state: ""
  reconciliation_state: ""
  authority_refs: []
  disposition: ""
```

The DCL records governance decisions and evidence. It must not contain secret values, protected cross-lane material, or private chain-of-thought.

### 7.2 Storage and delivery

DCL storage is adapter-controlled. D21 does not hardcode a Windows directory, database table, or model-interface behavior.

Each attempted sink records:

- sink identity;
- operation attempted;
- created or stored state;
- delivery and acknowledgment state when applicable;
- receipt ID;
- timestamp;
- reconciliation status;
- failure reason.

If no approved remote sink is available, the runtime writes to an approved local evidence location when authorized and marks `PENDING_RECONCILIATION`. Lack of remote storage does not halt unrelated work.

### 7.3 Gap aggregation

Gaps are deduplicated by doctrine ID, normalized finding type, source hash, and affected requirement. Recurrence counts support prioritization but do not independently create authority or a global Stop-Gate.

## 8. Executability wrapper

Any partial or descriptive-only doctrine must be wrapped with:

1. doctrine ID, source path, commit, and hash;
2. activation reason and applicability decision;
3. required inputs and preconditions;
4. ordered actions and accountable runtime;
5. required outputs and evidence;
6. Pass-Gate and Stop-Gate criteria;
7. failure, retry, correction, rollback, recovery, and escalation;
8. final disposition and reconciliation requirement.

The wrapper makes a bounded activation executable. It does not rewrite or promote the underlying doctrine.

## 9. Capability Watch and fallback

### 9.1 Capability identity

Capabilities use versioned logical identifiers and evidence. A capability claim records:

- capability ID and version;
- supported actions;
- access or tool dependency;
- verification method and timestamp;
- confidence category;
- restrictions;
- source of the claim.

Named model identity is not a capability. If a model name or version is not exposed, the runtime records `model_exposed: false` and does not infer it.

### 9.2 Capability changes

When capability changes:

1. record the prior and current capability claims;
2. verify the change through available runtime or provider evidence;
3. identify affected doctrine and tasks;
4. run deterministic compatibility checks;
5. isolate incompatible affected actions;
6. use a capability-qualified fallback when available;
7. continue unaffected authorized work;
8. route constitutional or reserved changes to DCS.

No named vendor or model-specific instruction controls this process.

### 9.3 Missing capability

If a runtime lacks an optional capability, reassign or defer the affected action. If every admitted runtime lacks a mandatory capability, mark the affected action `BLOCKED_CAPABILITY`, continue unaffected work, and route the evidence and options to the authority holder. `BLOCKED_RESERVED` applies only when the missing capability also triggers a reserved condition.

## 10. Resolution-first execution

For missing structure, routine defects, or transient failure:

1. inspect controlling sources and evidence;
2. classify the issue;
3. create reversible missing structure;
4. correct within approved scope;
5. test;
6. retry bounded transient failures;
7. reassign or use a qualified fallback;
8. isolate unresolved affected work;
9. continue unaffected authorized work;
10. escalate only reserved decisions or conditions with no safe fallback.

Issue dispositions are:

- `RESOLVED`;
- `RESOLVED_WITH_FINDINGS`;
- `DEFERRED_NONBLOCKING`;
- `BLOCKED_CAPABILITY`;
- `READY_FOR_AUTHORITY_DECISION`;
- `BLOCKED_RESERVED`.

## 11. Artifact-scoped security controls

### 11.1 Universal controls

Every artifact must pass applicable checks for:

- secret and credential exposure;
- PS and PPR leakage;
- lane and classification;
- source identity;
- input and output handling appropriate to the artifact;
- dependency and access scope;
- public or production release authority.

Secret or protected-data exposure isolates delivery of the affected artifact, triggers containment and remediation, and records an incident receipt. It does not require unrelated work to halt after isolation is verified.

### 11.2 Artifact classes

Security controls are selected by artifact class. Initial logical classes include:

- `GOVERNANCE_DOCUMENT`;
- `PUBLIC_UI`;
- `INTERNAL_UI`;
- `BACKEND_SERVICE`;
- `DATABASE_CHANGE`;
- `LOCAL_SCRIPT`;
- `MEDIA_ASSET`;
- `COMMUNICATION`.

The catalog may expand through a governed versioned change. CORS, CSP, HTTPS, browser sanitization, backend mediation, database parameterization, file-upload validation, and similar technical controls apply only when the artifact and architecture make them relevant.

### 11.3 Security exceptions

A technical requirement that does not apply must be recorded `NOT_APPLICABLE` with reason. A security exception that weakens a required control remains DCS-reserved.

## 12. Live preview and human-contact validation

Browser-renderable products, apps, and public interfaces require a live or equivalent rendered preview before completion is claimed.

Preview evidence is selected by the active preview adapter and may include:

- preview URL or local render target;
- screenshot or visual capture;
- golden-path result;
- console and network summary when applicable;
- responsive checks when applicable;
- accessibility checks when applicable;
- brand and lane checks;
- security checks;
- timestamp and accountable identity.

Governance documents, backend-only scripts, migrations, and nonvisual artifacts require their applicable deterministic validation rather than a browser preview.

Failure triggers correction and retest of the affected artifact. Unrelated work continues.

## 13. Lifecycle and promotion guard

### 13.1 Lifecycle states

D21 enforces the task lifecycle defined by the Master Profile and the artifact lifecycle defined by D05. It may validate a requested transition but cannot create promotion authority.

Task states include:

```text
INTAKE
ADMISSION
BASELINE
PLAN
EXECUTE
VERIFY
CORRECT
REVIEW
READY_FOR_PROMOTION
PROMOTED
RELEASED
RECONCILED
CLOSED
DEFERRED_NONBLOCKING
BLOCKED_CAPABILITY
BLOCKED_RESERVED
DRIFT
```

### 13.2 Promotion guard

The guard may issue:

- `NOT_READY`;
- `READY_FOR_PROMOTION`;
- `AUTHORITY_CONFIRMED`;
- `PROMOTION_RECORDED`;
- `PROMOTION_RECONCILIATION_PENDING`;
- `RECONCILED`.

`AUTHORITY_CONFIRMED` requires a direct DCS decision for the exact object or an exact DCS-approved standing authority that covers the routine object class, Pass-Gate, evidence, limits, and rollback. Constitutional change always requires direct exact-content DCS approval.

No numeric promotion score, model vote, review outcome, merge, test, or database state substitutes for promotion authority.

### 13.3 Promotion-readiness packet

```yaml
promotion_readiness_packet:
  schema_version: "1.0"
  packet_id: ""
  object_id: ""
  object_version: ""
  object_path: ""
  object_commit: ""
  object_sha256: ""
  change_records: []
  doctrine_run_plan_ref: ""
  dcl_ref: ""
  validation_results: []
  review_receipts: []
  unresolved_findings: []
  rollback_ref: ""
  required_authority: ""
  authority_ref: ""
  guard_disposition: "NOT_READY"
  evidence_refs: []
  accountable_identity: ""
  timestamp: ""
```

## 14. Change tracking, replacement, and drift

### 14.1 Change record

```yaml
doctrine_change_record:
  schema_version: "1.0"
  change_id: ""
  doctrine_id: ""
  prior_path: ""
  current_path: ""
  prior_commit: ""
  current_commit: ""
  prior_sha256: ""
  current_sha256: ""
  metadata_changes: []
  content_diff_ref: ""
  dependency_effects: []
  lifecycle_effect: ""
  constitutional_change: false
  evidence_refs: []
  accountable_identity: ""
  timestamp: ""
```

### 14.2 Replacement protocol

Doctrine replacement requires:

1. change record;
2. dependency impact analysis;
3. candidate identity and validation;
4. D05 promotion-readiness packet;
5. DCS authority for the exact constitutional change;
6. canonical GitHub update;
7. content and commit hashes;
8. D22 registry and runtime reconciliation;
9. distribution verification;
10. prior version retained as superseded lineage.

No model may change registry lifecycle status or assume caches refreshed. Polling, notification, cache invalidation, and runtime acknowledgment are adapter behaviors that require evidence.

### 14.3 Drift response

When promoted authority, GitHub, registry, local copy, or loaded runtime disagree:

1. classify the mismatch `DRIFT`;
2. retain the last verified promoted source;
3. isolate actions dependent on the mismatched copy;
4. continue unrelated work;
5. compare authority, commits, hashes, and distribution receipts;
6. correct the source or reference;
7. verify distribution;
8. issue a reconciliation receipt.

`BLOCKED_RESERVED` is used only when no verified promoted source exists or the drift also creates a reserved condition.

## 15. Adapters and reconciliation

### 15.1 Adapter minimums

Each GitHub, Supabase, filesystem, preview, security, or communication adapter must support:

- versioned identity;
- declared read and write capabilities;
- dry-run mode when mutation is possible;
- least privilege;
- bounded retries;
- structured audit output;
- secret-safe error reporting;
- evidence references;
- disable and rollback behavior.

### 15.2 Reconciliation receipt

```yaml
reconciliation_receipt:
  schema_version: "1.0"
  reconciliation_id: ""
  object_id: ""
  authority_ref: ""
  github_identity: {}
  registry_identity: {}
  local_identity: {}
  runtime_identities: []
  communication_refs: []
  mismatches: []
  remediation_actions: []
  final_disposition: "PENDING"
  evidence_refs: []
  accountable_identity: ""
  timestamp: ""
```

## 16. Error and degraded-mode protocol

If D21 is missing, unreadable, or fails validation:

1. emit `ERR_MISSING_OR_INVALID_D21` with attempted sources and evidence;
2. isolate doctrine-routing and authority-dependent modifying actions;
3. load the last verified promoted D21 when available;
4. use the Master Profile, D03, D22, and a recorded static doctrine fallback for safe unaffected work;
5. enter `REPOSITORY_READ_ONLY` or `OFFLINE_VERIFIED` as applicable;
6. prohibit promotion, public or production release, destructive action, and registry writes until the required authority path is restored;
7. continue safe evidence collection, recovery, and unaffected reversible work;
8. escalate only when no safe fallback exists or a reserved condition is present;
9. reconcile all pending receipts after restoration.

No physical Tribunal path or STOPGATE file is assumed. The active communication adapter determines storage and delivery evidence.

## 17. Python module contract

The reusable implementation contains these bounded components:

| Component | Required function |
|---|---|
| Loader | Resolve sources, verify identity and hash, and select source mode. |
| Classifier | Normalize task declarations and record supported inferences. |
| Router | Evaluate doctrine deterministically and emit the Doctrine Run Plan. |
| Validator | Test prerequisites, capability, evidence, security, and executability. |
| State machine | Enforce allowed lifecycle transitions and required evidence. |
| Diff tracker | Record metadata, content, dependency, and hash changes. |
| Receipt writer | Generate DCL and lifecycle receipts without secrets. |
| Promotion guard | Prepare readiness packets and reject unauthorized promotion. |
| Reconciler | Compare authority, GitHub, registry, local, and runtime identity. |
| Adapters | Bind approved external systems without leaking physical assumptions into core policy. |

The implementation must be deterministic for identical inputs and source state. Model analysis may recommend classifications or corrections, but deterministic validation controls recorded state transitions.

## 18. Mechanical acceptance tests

| Test ID | Scenario | Pass condition |
|---|---|---|
| D21-001 | New D23 exists only in GitHub | Recorded as `UNREGISTERED_DISCOVERY`; not applied as authority; unrelated work continues. |
| D21-002 | D01 content changes without lifecycle update | Change and drift recorded; dependent use isolates; prior promoted source remains controlling. |
| D21-003 | Supabase unavailable, GitHub available | `REPOSITORY_READ_ONLY`; plans and local receipts continue; database writes and promotion remain disabled. |
| D21-004 | GitHub unavailable, verified promoted local copy available | `OFFLINE_VERIFIED`; unaffected reversible work continues; reconciliation pending. |
| D21-005 | Preferred model unavailable | Capable fallback selected and recorded without a global stop. |
| D21-006 | Mandatory capability unavailable everywhere | Affected work becomes `BLOCKED_CAPABILITY`; unrelated work continues. |
| D21-007 | D13 selected outside PS | D13 excluded by firewall and event recorded. |
| D21-008 | Doctrine is descriptive-only | Executability wrapper attached or doctrine remains reference-only. |
| D21-009 | Tests pass without promotion authority | Packet stops at `READY_FOR_PROMOTION`. |
| D21-010 | GitHub and registry hashes disagree | `DRIFT`; last verified promoted source controls; affected work isolates. |
| D21-011 | DCL lacks evidence references | DCL is incomplete; promotion guard returns `NOT_READY`; correction is required. |
| D21-012 | Correction changes constitutional rule | Direct exact-content DCS approval required. |
| D21-013 | Registry adapter fields do not validate | Database routing disabled; repository-only mode used. |
| D21-014 | Model identifier not exposed | `model_exposed: false`; no identity invented. |
| D21-015 | Security control is not applicable | `NOT_APPLICABLE` with artifact-class reason; no false failure. |
| D21-016 | D21 unavailable but verified fallback exists | Affected modifying actions isolate; safe recovery and unaffected work continue. |

## 19. Change record from active D21 source

| Active source condition | Candidate correction | Reason |
|---|---|---|
| Internal version and parent references remain v6.9 | Native v7.1 candidate with current parent and source identity | Removes version and authority conflict. |
| Router assumes a named physical registry and fields | Requires a verified schema adapter and repository-only fallback | Prevents guessed Supabase behavior. |
| Fixed task, model-tier, and topic lists control routing | Uses versioned logical catalogs with recorded fallback | Prevents static-list drift. |
| Always-loaded source points to v6.9 authority and index | Uses promoted v7.1 Master Profile, D03, D21, D22, and current registry or manifest | Establishes correct runtime bootstrap. |
| New registry entries auto-activate | Separates discovery from authority and promotion | Prevents unreviewed doctrine activation. |
| DCL storage is tied to local folders and model interfaces | Uses approved adapters and pending reconciliation | Supports connected and disconnected runtimes. |
| Capability watch references named-model instructions | Uses capability evidence and versioned identifiers | Removes vendor dependency. |
| Security rules are universalized | Selects controls by artifact class | Prevents false failures and irrelevant requirements. |
| Preview proof is underspecified | Uses preview-adapter evidence appropriate to the artifact | Makes human-contact validation testable. |
| Replacement assumes registry and cache updates occur automatically | Requires D05 readiness, D22 reconciliation, and distribution evidence | Prevents false synchronization. |
| Missing D21 triggers global HALT and physical STOPGATE files | Uses isolation-first degraded modes and adapter-controlled receipts | Preserves safe non-stoppage. |
| No enforceable promotion guard or change schema | Adds readiness, change, lifecycle, and reconciliation contracts | Supports the reusable Python module. |

## 20. Candidate disposition

**Disposition:** `D21_EXECUTABLE_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and Python-module design specimen only.

**Authority before promotion:** The currently promoted Master Profile and active D21 source remain controlling, subject to the native v7.1 manifest and supersession controls.

**Next required state:** Mechanical validation, D05 comparison, exact DCS decision, governed promotion, GitHub and Supabase reconciliation, and runtime tests.

