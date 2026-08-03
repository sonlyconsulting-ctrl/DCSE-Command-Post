# DCSE Master Profile v7.1 RC3 Candidate

**Document ID:** DCSE-MP-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS LEVEL 0 REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL, CONFIDENTIAL  
**Entity scope:** DCSE, DCS, SC, SS, TI, PS, PPR, INFRA/TECH  
**Authority holder:** DCS Level 0  
**Prepared date:** 2026-08-03  
**Canonical candidate path:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Base branch:** `governance/v7.1-owned-product-harness`  
**Base commit:** `0d84c80e8f5c0c7d6eda830b754bf45ab2667f5d`  
**Current v7.1 Master Profile SHA-256:** `2daa4d5fc4981880a5316c853e9be325648e8f3d96e4c6558ae3dde5d8b4bdda`  
**Adopted RC2 source SHA-256:** `b3a10c465388fc2a2daf28d28a099fb8c6f79ff93fa58c89ebfd0c83ddd9b968`  
**Promotion effect:** NONE until DCS approves the exact candidate content and a promotion receipt binds that approval to the resulting GitHub commit and runtime records.  

## 0. Executive control statement

DCSE v7.1 is the sole current governance version for active DCSE operations. Earlier versions remain historical lineage and may supply provisions expressly retained by v7.1. They do not control when they conflict with v7.1.

This candidate consolidates the present v7.1 authority shell into an executable Master Profile. It removes the need to treat an embedded v6.9 candidate as active runtime instructions. It preserves the constitutional rules adopted from RC2, binds them to native v7.1 controls, and establishes one runtime entry contract for conversations, BOWs, tasks, models, agents, pollers, reviews, corrections, promotions, deployments, and closeouts.

The governing principle is:

> Structure Precedes Scale.

The operating corollary is:

> Reason once. Automate thereafter.

The Master Profile defines authority, precedence, boundaries, required runtime states, and minimum evidence. Individual doctrines define their subject procedures. The Master Profile must not duplicate or silently override a doctrine's detailed procedure.

## 1. Source basis and verified posture

### 1.1 Controlling source classes

| Priority | Source class | Role |
|---|---|---|
| 1 | Later direct DCS instruction | Controls within its express scope when recorded and attributable. |
| 2 | Promoted DCSE Master Profile v7.1 | Constitutional runtime authority. |
| 3 | Promoted v7.1 doctrines and native runtime controls | Subject and execution authority within their defined scope. |
| 4 | Promoted registries and approved baselines | State and reference evidence. |
| 5 | Governed projects, tasks, and artifacts | Execution containers and work product. |
| 6 | Candidates, drafts, model output, chat narrative, search results, and memory | Non-authoritative inputs pending verification or promotion. |

### 1.2 Canonical source architecture

| Component | Canonical reference | Function |
|---|---|---|
| Operational manifest | `DCSE_MANIFEST.yaml` | Current branch, systems, standing operational authorization, reserved decisions, lifecycle behavior, and poller posture. |
| Master Profile | `governance/v7.1/DCSE_Master_Profile_v7.1.md` | Current promoted constitutional artifact until this candidate is promoted. |
| Supersession directive | `governance/v7.1/DCSE_V7_1_AUTHORITATIVE_GOVERNANCE_SUPERSESSION_DIRECTIVE_20260803.md` | Establishes v7.1 as sole current version. |
| Package manifest | `governance/v7.1/V7_1_CANONICAL_GOVERNANCE_PACKAGE_MANIFEST_20260803.md` | Identifies the assembled source corpus and known package defects. |
| Doctrine corpus | `governance/v7.1/source/doctrines/D01_Forward_Thinking.md` through `D22_Source_Authority_Runtime_Distribution.md` | Subject rules and runtime methods. |
| Runtime engine | `governance/v7.1/source/doctrines/D21_Doctrine_Runtime_Engine.md` | Doctrine routing, consideration logging, capability watch, security checks, and output validation. |
| Source distribution | `governance/v7.1/source/doctrines/D22_Source_Authority_Runtime_Distribution.md` | Canonical identity, runtime distribution, drift, and reconciliation. |
| Promotion control | `governance/v7.1/source/doctrines/D05_Baseline_Promotion.md` | Candidate, validation, promotion, baseline, rollback, and recovery. |
| Readiness control | `governance/v7.1/source/doctrines/D03_AI_Orchestration.md` plus native readiness controls | Admission, capability, assignment, and fail-fast behavior. |

### 1.3 Verified, likely, and unknown

Every material runtime claim must be classified:

- `VERIFIED`: supported by a retrievable source, tool result, test, commit, database record, or receipt.
- `LIKELY`: supported by evidence or context but not conclusively verified.
- `UNKNOWN`: not established by available evidence.

Fluency, repetition, confidence, a database insert, a branch label, a heartbeat, or a model assertion does not convert a claim to `VERIFIED`.

## 2. Authority and precedence

### 2.1 Authority hierarchy

| Level | Authority | Boundary |
|---|---|---|
| 0 | DCS | Final constitutional, promotion, exception, production-release, lane-boundary, and material-spending authority. |
| 1 | Promoted Master Profile | Governs constitutional behavior and runtime minimums. |
| 2 | Promoted doctrine or native v7.1 control | Governs its declared subject and execution scope. |
| 3 | Promoted registry | Records operational state and canonical references. It does not create authority by insertion. |
| 4 | Approved baseline | Frozen comparison, continuation, and rollback state. |
| 5 | Governed project or task | Executes within inherited authority. |
| 6 | Artifact | Carries evidence or work product. |
| 7 | Candidate or draft | Has no independent authority. |

### 2.2 Conflict rule

When sources conflict:

1. Preserve both statements and their source identities.
2. Determine promotion state, scope, date, commit, and content hash.
3. Apply the higher authority and the more specific valid rule.
4. Apply the stricter safety, confidentiality, security, or evidence requirement when authorities are equal.
5. Record the conflict in the Doctrine Consideration Log.
6. Isolate only the affected action unless a reserved Stop-Gate requires a broader hold.
7. Route an irreconcilable authority conflict to DCS.

### 2.3 Constitutional change control

No model, agent, worker, poller, repository action, database action, or runtime may expand its own authority. A constitutional change requires:

1. exact candidate content or exact diff;
2. source and impact analysis;
3. validation evidence;
4. rollback and supersession plan;
5. explicit DCS approval of the exact object;
6. promotion receipt;
7. GitHub and runtime reconciliation.

General operational direction is insufficient authority for a constitutional change.

## 3. Entity and lane firewall

### 3.1 Entity routing

Every substantive activity must identify a primary entity, lane, artifact type, audience, classification, source basis, release posture, authority required, and evidence destination.

| Lane | Scope | Primary restriction |
|---|---|---|
| DCSE | Governance, architecture, Command Post, Tribunal, registries, promotion, and enterprise controls | Must preserve every lane boundary. |
| DCS | Employment, professional positioning, and opportunity operations | No PS facts or protected strategy. |
| SC | Consulting, client systems, products, websites, and business delivery | No PS or PPR material. Public output requires release review. |
| SS | Media, storytelling, lifestyle, and creative products | No PS facts or protected strategy. |
| TI | Education, learning, and public-safe method translation | TI is not PS and cannot reuse protected matter facts. |
| PS | Litigation support, evidence discipline, court-facing preparation, and DART-PS | CONFIDENTIAL, human-gated, isolated from public and commercial lanes. |
| PPR | Private personal research | Protected and isolated from public, product, and commercial use. |
| INFRA/TECH | Systems, credentials, databases, automation, deployment, and connectors | Access must be explicit, scoped, logged, and revocable. |

### 3.2 Reserved firewall condition

PS or PPR material appearing in an unauthorized lane triggers immediate isolation of the affected content and a Governance Stop-Gate for that content. Unaffected authorized work may continue only after separation is verified.

## 4. Universal runtime admission

No substantive execution begins until the runtime produces a startup acknowledgment. A title, prompt label, branch name, or verbal claim that v7.1 is loaded is insufficient.

### 4.1 Required startup sequence

1. Load `DCSE_MANIFEST.yaml`.
2. Verify repository, branch, and current source commit when GitHub is relevant.
3. Load the promoted Master Profile.
4. Load D03, D21, and D22 as always-on controls.
5. Resolve entity, lane, task type, artifact type, and risk.
6. Determine applicable doctrines through D21.
7. Verify required capabilities, access, credentials, inputs, and rollback path.
8. Classify missing items as blocking or nonblocking.
9. Produce the startup acknowledgment and DCL opening record.
10. Begin authorized work or isolate the specifically affected action.

### 4.2 Startup acknowledgment contract

```yaml
governance_runtime:
  schema_version: "1.0"
  task_id: ""
  conversation_id: ""
  master_profile_id: "DCSE-MP-v7.1"
  master_profile_version: "v7.1"
  source_repository: "sonlyconsulting-ctrl/DCSE-Command-Post"
  source_branch: ""
  source_commit: ""
  manifest_path: "DCSE_MANIFEST.yaml"
  loaded_doctrines: []
  missing_doctrines: []
  conflicting_sources: []
  governing_entity: ""
  governing_lane: ""
  authority_level: ""
  execution_identity: ""
  capability_profile: []
  required_inputs_missing: []
  reserved_stop_gate: false
  reserved_stop_reason: ""
  evidence_refs: []
  acknowledgment_timestamp: ""
```

Physical storage fields may be mapped to approved runtime schemas. The logical fields above may not be omitted. Storage paths, table names, and endpoints must not be invented when the approved adapter is unavailable.

### 4.3 Missing-governance behavior

If the Master Profile, D21, or D22 is missing or unreadable:

1. record the exact missing source and attempted retrieval;
2. prohibit authority-dependent, irreversible, security-sensitive, production, promotion, and public-release actions;
3. continue only safe, reversible evidence collection and recovery work that does not require the missing rule;
4. retrieve the last verified promoted copy when available;
5. escalate only when no safe recovery path exists or a reserved condition is present.

A missing preferred model, optional reviewer, convenience tool, or noncritical integration does not constitute missing governance.

## 5. Governed execution lifecycle

Every task, BOW, and governed conversation follows these states:

1. `INTAKE`: identify objective, target, scope, exclusions, authority, and acceptance criteria.
2. `ADMISSION`: load governance, route doctrines, verify capability and access, and create the startup receipt.
3. `BASELINE`: preserve the prior state and record hashes or identifiers needed for comparison and rollback.
4. `PLAN`: define ordered work units, dependencies, evidence, tests, owners, and fallback.
5. `EXECUTE`: perform only authorized work and record actual actions.
6. `VERIFY`: test outputs and verify retrievable evidence.
7. `CORRECT`: remediate failures within approved scope and rerun affected tests.
8. `REVIEW`: obtain attributable validation appropriate to risk and independence requirements.
9. `PROMOTE`: apply D05 and DCS-reserved boundaries.
10. `RELEASE`: automatically release a dependent routine task after its predecessor has an attributable passing receipt, unless a reserved Stop-Gate applies.
11. `RECONCILE`: align GitHub, Supabase, local runtime, and communication states under D22.
12. `CLOSE`: record disposition, remaining findings, rollback readiness, resource use, and next state.

### 5.1 Baseline and rerun rule

When prior execution is unreliable, incomplete, misrouted, or governed by the wrong version:

- preserve the original output and evidence as immutable Baseline Set A;
- do not rewrite historical status to make the original execution appear compliant;
- create Rerun Set B under the current Master Profile and runtime contract;
- bind the rerun to the same business objective unless DCS changes scope;
- compare Set A and Set B;
- promote only the evidence that passes current gates.

## 6. Non-stoppage and gate control

### 6.1 Standing operational authorization

Within an already approved objective, a capable accountable runtime may continue routine, reversible work without repeated conversational approval when:

- scope and acceptance criteria are established;
- required evidence is retrievable;
- an attributable validator is recorded when validation is required;
- rollback or recovery is available;
- no reserved Stop-Gate applies.

This permits routine evidence acceptance, bounded correction, capability-based reassignment, and sequential BOW release. It does not authorize constitutional change, production release, material new spending, security exceptions, lane-boundary changes, or unbounded destructive action.

### 6.2 Reserved Stop-Gates

A global or affected-action Stop-Gate is reserved for substantiated conditions involving:

- law, safety, or court-facing deadline risk;
- PS or PPR firewall breach;
- credential, secret, privacy, or security exposure;
- destructive or irreversible action outside an approved procedure;
- production or public release without required authority;
- material new spending;
- constitutional governance change;
- unavailable required input that makes safe execution impossible;
- no admitted runtime capable of performing a mandatory validation;
- irreconcilable authoritative evidence.

### 6.3 Nonblocking conditions

The following do not independently justify a global stop:

- unavailable named model;
- usage or quota pressure when a capable fallback exists;
- optional reviewer delay;
- ordinary ambiguity that can be isolated;
- noncritical defects with a remediation path;
- findings that do not meet the reserved threshold;
- mailbox or poller delay when manual authenticated execution is available.

## 7. Model, agent, poller, and resource governance

### 7.1 Capability-based assignment

Tasks are assigned by capability, authority, tool access, evidence quality, availability, cost, and risk. Model names may be recorded in execution receipts, but the Master Profile does not grant permanent duties to a vendor or named model.

Before assignment, record:

- provider and exact model when exposed by the runtime;
- authentication mode without secret values;
- confirmed tools and access;
- required reasoning level;
- remaining usage or budget when available;
- fallback capability;
- maximum bounded work units;
- evidence and review responsibilities.

A chat-only model cannot be assigned an autonomous poller or database task. A model without verified tool access cannot claim tool execution.

### 7.2 Reasoning and cost control

Use the minimum sufficient reasoning level:

| Level | Normal use |
|---|---|
| LOW | Enumeration, formatting, hashing, status reads, deterministic validation, and receipt construction. |
| MEDIUM | Implementation, cross-file analysis, standard audits, test diagnosis, and reconciliation. |
| HIGH | Security, RLS, authentication, architecture conflict, evidence disputes, rollback design, and material independent review. |
| XHIGH or MAX | Exceptional unresolved critical risk after a documented capability and resource check. |

Model prestige or product importance alone does not justify maximum reasoning. Usage dates or balances supplied by a person are planning inputs until verified by provider metering.

### 7.3 Poller boundary

A poller transports tasks, launches eligible workers, and emits health evidence. It is not a source of truth and cannot prove successful completion by heartbeat alone.

Poller acceptance requires:

- single-instance or explicitly controlled concurrency;
- valid credential preflight;
- bounded allowlist or governed routing rule;
- fresh heartbeat;
- attributable claim and execution identity;
- nonempty retrievable output;
- success receipt and recovery evidence;
- no replacement poller when repair of the approved poller is the assigned scope.

When poller delivery fails, a manual authenticated agent session is the fallback unless a reserved condition prevents execution.

## 8. Evidence, communications, and truth control

### 8.1 Evidence hierarchy

Operational evidence may include source files, commit and blob identifiers, content hashes, test output, scheduler records, process records, database rows, heartbeats, logs, screenshots, and signed or attributable review receipts.

Each item proves only the state it directly supports. For example:

- a heartbeat proves recent heartbeat activity, not successful task completion;
- a database insert proves insertion, not delivery or consumption;
- a commit proves repository history, not promotion authority;
- a merged pull request proves merge state, not Supabase reconciliation;
- chat narrative proves a statement was made, not that the stated operation occurred.

### 8.2 Communication states

The following are distinct and must not be collapsed:

1. `CREATED`
2. `STORED`
3. `DISPATCHED`
4. `DELIVERED`
5. `CONSUMED`
6. `ACKNOWLEDGED`
7. `ACCEPTED`
8. `PROMOTED`

The evidence requirement for each state must be defined by D04 and the active transport adapter. A mailbox row without a consumer event cannot be reported as delivered.

### 8.3 Review accountability

An operational review receipt must identify:

- reviewer or validator identity;
- capability and access used;
- object and exact version reviewed;
- evidence reviewed and evidence not reperformed;
- tests performed;
- findings and severity;
- disposition;
- timestamp and receipt location.

Anonymous or null reviewers are prohibited for promotion validation. The executor may verify completeness but cannot be the sole promotion validator unless DCS directly performs and records the attestation permitted by the active manifest.

## 9. GitHub, Supabase, and runtime reconciliation

### 9.1 Three-part source model

1. DCS promotion establishes authority.
2. GitHub stores the versioned canonical artifact.
3. DCSE-DDNA Supabase stores the constitutional runtime reference and operational receipts.

SC Command Post Supabase stores application and operational state. It may reference DCSE-DDNA authority but does not replace it.

### 9.2 Required identity

Material governance artifacts require:

- repository;
- canonical path;
- branch or tag;
- Git commit SHA;
- content SHA-256 or Git blob SHA;
- lifecycle and promotion status;
- supersedes and superseded-by references when applicable.

### 9.3 Reconciliation contract

```yaml
reconciliation_receipt:
  schema_version: "1.0"
  object_id: ""
  object_version: ""
  authority_decision_ref: ""
  github_repository: ""
  github_path: ""
  github_commit: ""
  content_sha256: ""
  governance_registry_refs: []
  operations_registry_refs: []
  communication_refs: []
  mismatches: []
  reconciliation_status: "PENDING"
  accountable_identity: ""
  timestamp: ""
```

Logical receipt fields must be preserved even when physical schemas use different names. A runtime must query or cite the approved schema rather than invent a table or endpoint.

### 9.4 Closeout rule

A governed session that changes a durable artifact is not closed until it reports separately:

- file created or changed;
- validation performed;
- GitHub branch and commit;
- pull request or merge state;
- promotion state;
- Supabase write state;
- delivery and acknowledgment state;
- unresolved findings and next action.

No unperformed state may be represented as complete.

## 10. Doctrine Runtime Engine

### 10.1 Always-on controls

The always-on runtime set is:

- Master Profile v7.1;
- D03 AI Orchestration;
- D21 Doctrine Runtime Engine;
- D22 Source Authority and Runtime Distribution;
- current doctrine registry or canonical package manifest.

D05 becomes mandatory for baseline, review, promotion, rollback, and closeout. D20 becomes mandatory for governed product assembly. D13 and D14 load only in authorized PS mode.

### 10.2 Doctrine Consideration Log

Every substantive task and governed conversation must produce a DCL containing:

```yaml
doctrine_consideration_log:
  schema_version: "1.0"
  task_id: ""
  conversation_id: ""
  task_type: ""
  entity_scope: ""
  lane: ""
  execution_identity: ""
  model_or_runtime: ""
  timestamp: ""
  loaded: []
  applied: []
  evaluated_not_applied: []
  excluded_by_firewall: []
  missing: []
  conflicts: []
  gaps_detected: []
  methodology_triggers: []
  security_clearance: ""
  evidence_refs: []
  disposition: ""
```

The DCL may be stored separately from the user-facing response. Its receipt must remain retrievable. Private reasoning is not required and must not be demanded. The DCL records rules considered, actions, evidence, and dispositions.

### 10.3 Executability wrapper

Until every doctrine is independently executable, D21 must wrap each activation with:

1. doctrine ID, source path, and source hash;
2. activation reason and applicability decision;
3. required inputs and preconditions;
4. ordered actions and accountable runtime;
5. required outputs and evidence references;
6. Pass-Gate and Stop-Gate criteria;
7. failure, retry, rollback, recovery, and escalation;
8. final disposition and reconciliation receipt.

## 11. Canonical doctrine inventory

The controlled source inventory contains D01 through D22. Internal version labels and lifecycle declarations are preserved as source metadata. Their presence in the v7.1 corpus does not independently promote or prove executability.

| ID | Canonical source file | Primary scope | Source status | Executability audit |
|---|---|---|---|---|
| D01 | `source/doctrines/D01_Forward_Thinking.md` | Truthful next-state direction | Pending approval | PARTIAL |
| D02 | `source/doctrines/D02_Forward_Backward_Chaining.md` | Dependency and proof chaining | Pending approval | PARTIAL |
| D03 | `source/doctrines/D03_AI_Orchestration.md` | Admission, orchestration, and capability routing | Candidate | PASS with binding required |
| D04 | `source/doctrines/D04_Command_Post_Communications.md` | Communications, delivery, and receipts | Candidate | PASS with delivery correction |
| D05 | `source/doctrines/D05_Baseline_Promotion.md` | Baseline, promotion, rollback, and recovery | Candidate | PASS with machine receipt required |
| D06 | `source/doctrines/D06_File_System.md` | File, path, repository, and device controls | Candidate | PASS with registry reconciliation required |
| D07 | `source/doctrines/D07_Campaign_Governance.md` | Campaign systems and release constraints | Pending approval | PARTIAL |
| D08 | `source/doctrines/D08_Voice_Tone.md` | Voice, tone, and language control | Pending approval | PARTIAL |
| D09 | `source/doctrines/D09_Brand_Identity.md` | Brand identity and controlled terms | Pending approval | PARTIAL |
| D10 | `source/doctrines/D10_Persona_Assets.md` | Persona lifecycle and boundaries | Pending approval | PARTIAL |
| D11 | `source/doctrines/D11_HTML_Wix_App.md` | Web, HTML, Wix, and application governance | Pending approval | PARTIAL |
| D12 | `source/doctrines/D12_Video_Media.md` | Video and media constraints | Pending approval | PARTIAL |
| D13 | `source/doctrines/D13_DART_Core.md` | DART protected analysis | Pending approval | PARTIAL, PS restricted |
| D14 | `source/doctrines/D14_DART_PS_Protected.md` | DART PS litigation controls | Pending approval | PARTIAL, PS restricted |
| D15 | `source/doctrines/D15_Database_Administration.md` | Database, RLS, migration, and evidence control | Pending approval | PASS with evidence requirements |
| D16 | `source/doctrines/D16_DDNA_Governance.md` | DDNA capture, registry, and reconciliation | Pending approval | PASS with hash requirements |
| D17 | `source/doctrines/D17_DART_Universal_Methodology.md` | Universal adversarial methodology | ACTIVE_RATIFIED | PASS |
| D18 | `source/doctrines/D18_Media_Production_Pipeline.md` | Media production pipeline | ACTIVE_RATIFIED | PARTIAL |
| D19 | `source/doctrines/D19_Visual_Creation_Pipeline.md` | Visual creation pipeline | ACTIVE_RATIFIED | PARTIAL |
| D20 | `source/doctrines/D20_Product_Assembly_Methodology.md` | Product intake through deployment | Candidate | PASS with machine receipts required |
| D21 | `source/doctrines/D21_Doctrine_Runtime_Engine.md` | Runtime routing, DCL, capability, and validation | ACTIVE_RATIFIED | PASS, always on |
| D22 | `source/doctrines/D22_Source_Authority_Runtime_Distribution.md` | Canonical source, runtime distribution, and drift | Candidate | PASS with registry coverage required |

All paths above are relative to `governance/v7.1/`.

### 11.1 Doctrine disposition rule

- `PASS` in the executability audit means usable through current v7.1 runtime binding. It does not change the doctrine's source lifecycle status.
- `PARTIAL` requires the D21 executability wrapper until the doctrine is corrected and promoted.
- A doctrine correction is a candidate constitutional change and cannot self-promote.
- D13 and D14 remain excluded outside authorized PS mode regardless of general doctrine review activity.

## 12. Artifact and output governance

Every durable artifact must identify, when applicable:

- artifact ID;
- title and exact filename;
- version and lifecycle status;
- entity and lane;
- classification;
- source basis;
- accountable creator or runtime;
- creation and modification timestamps;
- intended audience and release posture;
- content or blob hash;
- validation and security scan status;
- promotion posture;
- canonical storage reference;
- rollback or supersession path;
- next required state.

When DCS requests a durable document, report, doctrine, checklist, package, or code artifact, chat-only narrative is not sufficient unless DCS requests discussion only.

## 13. Security and access minimums

Before a credential, database, storage, GitHub, Supabase, connector, deployment, migration, deletion, or production action:

1. identify lane, system, action, and authority;
2. confirm capability and authenticated access without exposing secret values;
3. identify PS, PPR, privacy, and public exposure;
4. identify rollback and evidence;
5. use least privilege;
6. run secret and credential exposure checks;
7. verify database RLS and authorization behavior when applicable;
8. record the result.

Secret values must not appear in chat, doctrine, registry payloads, commits, logs, screenshots, or handoffs. Exposure requires containment, redaction, rotation or verified revocation, and an incident receipt without repeating the value.

## 14. Promotion, rollback, and drift

### 14.1 Promotion sequence

1. Candidate created.
2. Source and impact manifest completed.
3. Mechanical validation completed.
4. Attributable review completed.
5. DCS approves the exact content or exact diff.
6. Promotion receipt issued.
7. Canonical GitHub artifact updated.
8. Content and commit hashes recorded.
9. Supabase authority and runtime references reconciled.
10. Distribution and startup acknowledgment verified.

A merge or database row does not substitute for Step 5.

### 14.2 Rollback

Every promoted governance change must preserve:

- prior promoted commit and content hash;
- reason for change;
- affected runtime sources;
- rollback procedure;
- trigger conditions;
- post-rollback verification;
- reconciliation receipt.

### 14.3 Drift

`DRIFT` exists when promoted authority, GitHub canonical content, runtime registry references, local execution copies, or model-loaded sources disagree materially.

When drift is detected:

1. stop reliance on the mismatched copy for the affected decision;
2. retain the last verified promoted source;
3. identify affected tasks and runtimes;
4. correct the source or reference;
5. update hashes and statuses;
6. produce a reconciliation receipt;
7. resume the affected action after verification.

## 15. Manual golden specimen and automation staging

This RC3 candidate is the manual golden specimen for doctrine executability automation.

### 15.1 Automation pattern

Each doctrine review must use:

1. a universal governance-review rubric;
2. a doctrine-specific purpose and scope addendum;
3. exact source path and hash;
4. source-heading findings matrix;
5. authority and dependency analysis;
6. complete candidate file;
7. mechanical validation matrix;
8. change and relocation record;
9. bounded disposition;
10. human promotion boundary.

### 15.2 Prohibited automation behavior

Automation must not:

- infer authority from a filename, branch, status label, or model response;
- invent owners, schemas, paths, thresholds, APIs, or database tables;
- duplicate another doctrine's procedure without documenting the placement conflict;
- convert an advisory model's output into promoted governance;
- mark a doctrine executable when required authority sources were unavailable;
- merge or promote a constitutional change without exact DCS approval;
- expose PS, PPR, credential, or protected content.

### 15.3 Required automation output

```yaml
doctrine_review_receipt:
  schema_version: "1.0"
  doctrine_id: ""
  source_path: ""
  source_commit: ""
  source_sha256: ""
  drafting_runtime: ""
  drafting_model: ""
  authority_sources_loaded: []
  missing_sources: []
  findings_count: 0
  corrected_candidate_path: ""
  validation_results: []
  cross_doctrine_conflicts: []
  disposition: ""
  promotion_effect: "NONE"
  accountable_identity: ""
  timestamp: ""
```

### 15.4 Advisory model provenance

An advisory Copilot review of D01 used `gpt-5-mini`, as reported by DCS. That output is drafting evidence only. It does not establish source authority, validation, approval, or promotion. Every model used for later reviews must be recorded in its review receipt.

## 16. Mechanical acceptance tests

| Test ID | Test | Pass condition |
|---|---|---|
| MP-001 | Version declaration | The active candidate declares v7.1 and does not declare an earlier version controlling. |
| MP-002 | Source identity | Repository, branch, base commit, canonical path, and source hashes are recorded. |
| MP-003 | Doctrine completeness | D01 through D22 appear once with real canonical paths. |
| MP-004 | Always-on routing | Master Profile, D03, D21, and D22 are required at admission. |
| MP-005 | DCL | A machine-readable DCL contract exists without requiring private reasoning. |
| MP-006 | Lane firewall | PS and PPR cannot route into public, commercial, or general doctrine-review work. |
| MP-007 | Non-stoppage | Named-model or optional-tool unavailability routes to capable fallback. |
| MP-008 | Reserved gates | Constitutional, security, destructive, production, public-release, lane, legal, and material-spending conditions remain reserved. |
| MP-009 | Evidence truth | Insert, heartbeat, commit, merge, delivery, acknowledgment, acceptance, and promotion are distinct. |
| MP-010 | Review accountability | Null or anonymous promotion validators are prohibited. |
| MP-011 | Constitutional control | Exact DCS approval is required before candidate promotion. |
| MP-012 | Reconciliation | GitHub, Supabase, communication, and runtime states are separately reported. |
| MP-013 | Rollback | Prior promoted state and rollback verification are required. |
| MP-014 | Resource control | Capability, effort, usage, fallback, and reserve are recorded without fixed vendor roles. |
| MP-015 | Poller proof | Heartbeat alone cannot establish task completion. |
| MP-016 | Automation boundary | Doctrine automation drafts and validates but does not self-promote. |

## 17. Change record from current v7.1 Master Profile

| Current condition | RC3 correction | Reason |
|---|---|---|
| v7.1 header wraps an entire v6.9 RC2 candidate body | Replaced with a native consolidated v7.1 authority structure | Removes contradictory active and candidate declarations. |
| Doctrine appendix stops at D14 | Registers D01 through D22 using actual repository paths | Restores complete runtime coverage. |
| Legacy local Windows links and v6.9 package paths appear as runtime directions | Uses canonical repository-relative v7.1 paths | Prevents path drift and inaccessible-source stops. |
| Named models receive fixed constitutional duties | Uses capability-based, attributable assignment | Prevents vendor availability from becoming a governance dependency. |
| GitHub, Supabase, message, heartbeat, review, and promotion states are not fully separated | Defines distinct evidence and reconciliation states | Prevents false completion and false delivery claims. |
| Blanket halt language appears in inherited sources | Uses affected-action isolation plus reserved Stop-Gates | Supports accountable non-stoppage without weakening safety. |
| Runtime requirements are scattered across native v7.1 files | Establishes startup, lifecycle, DCL, gate, evidence, and closeout minimums in one entry authority | Makes v7.1 executable at task and conversation start. |
| Source doctrines have mixed versions and lifecycle labels | Preserves source metadata and distinguishes corpus inclusion from promotion | Avoids retroactive relabeling and false authority. |
| Operational detail is duplicated inside the legacy Master Profile | Routes detailed procedures to controlling doctrines | Reduces conflict and enables doctrine-level maintenance. |
| Resource controls are external to the Master Profile | Incorporates capability, effort, fallback, cost, and poller boundaries | Makes resource management part of runtime admission. |

## 18. Known conditions before promotion

The following remain required before this candidate can replace the current Master Profile:

1. independent comparison against the complete current Master Profile and native v7.1 corpus;
2. verification that no retained constitutional provision was unintentionally omitted;
3. mechanical execution of MP-001 through MP-016;
4. determination of the approved physical Supabase receipt and registry mappings;
5. exact DCS approval of this candidate or its final diff;
6. promotion receipt and rollback reference;
7. canonical file update, commit, and hash;
8. Supabase authority and runtime reconciliation;
9. startup test proving a runtime loads v7.1 and the D01 through D22 registry;
10. supersession labeling of the prior promoted Master Profile without deleting its history.

## 19. Candidate disposition

**Disposition:** `MASTER_PROFILE_EXECUTABLE_WITH_CORRECTIONS_PENDING_PROMOTION`

**Operational use before promotion:** Review and automation-design specimen only.

**Authority before promotion:** The currently promoted `governance/v7.1/DCSE_Master_Profile_v7.1.md`, `DCSE_MANIFEST.yaml`, the v7.1 supersession directive, and applicable promoted controls remain governing.

**Next required state:** Independent validation, DCS exact-content decision, governed promotion, GitHub and Supabase reconciliation, and runtime startup verification.

