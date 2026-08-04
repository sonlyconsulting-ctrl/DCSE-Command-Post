# DCSE Doctrine D22: Source Authority and Runtime Distribution v7.1 RC3 Candidate

**Document ID:** DCSE-D22-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D22_Source_Authority_Runtime_Distribution.md`  
**Source SHA-256:** `be24661b9fc9c6a3e5e1d5ea9adfa706c59ab9ef5da925904a1bf814fd561885`  
**Promotion dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D05_Baseline_Promotion_v7.1_RC3_CANDIDATE.md`  
**Promotion dependency SHA-256:** `9fb13438dff5dd97d31a54b6daab58d33d7cf028b85057b27a54b6834170cd71`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and this doctrine's own reconciliation requirements are satisfied.  

## 1. Purpose

D22 governs authoritative source identity and the controlled distribution of promoted and candidate artifacts across:

- DCS authority records;
- GitHub canonical artifacts;
- DCSE-DDNA constitutional runtime references;
- SC Command Post operational references;
- approved local and offline copies;
- model retrieval, indexes, caches, and uploads;
- deployments and published destinations;
- receipts, acknowledgments, and reconciliation records.

D22 proves what source controls, where it was distributed, what consumed it, and whether every material representation still matches. D22 does not create promotion authority.

## 2. Governing principles

1. Authority and storage are separate.
2. A source must have exact identity before it can be distributed as controlling.
3. Distribution is a stateful process, not an assumed side effect.
4. Insertion is not delivery; delivery is not acknowledgment; acknowledgment is not load; load is not use.
5. The last verified promoted source controls during drift.
6. Safe repository-only and offline operations remain available when a runtime registry adapter is unavailable.
7. Only affected actions isolate unless a reserved condition requires broader containment.

## 3. Authority model

D22 recognizes the D05 authority forms:

- `DIRECT_DCS`: DCS approves the exact object or exact diff.
- `STANDING_DCSE`: a previously DCS-approved rule expressly covers the object class, Pass-Gate, evidence, limits, executor, and rollback.

Standing DCSE authority is delegated DCS authority. It is not authority created by a model, reviewer, poller, workflow, repository, database, deployment, or unanimous vote.

Constitutional change, governance-framework promotion, authority expansion, lane-boundary change, security exception, and other D05 reserved conditions require direct DCS approval.

## 4. Source authority hierarchy

| Level | Source | Function |
|---|---|---|
| 0 | Recorded DCS authority | Constitutional and reserved decision authority. |
| 1 | Promoted Master Profile | Enterprise constitutional runtime authority. |
| 2 | Promoted doctrine and native v7.1 controls | Subject and execution authority within scope. |
| 3 | Promoted registry references | Runtime state and canonical pointers; no independent authority. |
| 4 | Approved baselines | Frozen comparison, recovery, and rollback state. |
| 5 | Governed tasks, projects, and artifacts | Authorized execution containers and work products. |
| 6 | Candidates, drafts, model output, retrieval results, chat narrative, and memory | Non-authoritative inputs pending verification and promotion. |

Higher authority controls only within its scope. More specific promoted rules control over general rules at the same level. Equal-authority safety, confidentiality, security, and evidence conflicts apply the stricter applicable control while reconciliation proceeds.

## 5. Four-part source model

### 5.1 Authority record

The D05 promotion receipt identifies the applicable direct or standing authority and exact controlled object.

### 5.2 Canonical artifact

GitHub stores versioned canonical governance and governed source artifacts. Canonical identity is:

```text
repository + path + commit SHA + content SHA-256
```

A branch, commit, merge, tag, or pull request is evidence and distribution infrastructure. It is controlling only when linked to a valid promotion state.

### 5.3 Constitutional runtime reference

DCSE-DDNA Supabase stores constitutional runtime references, promotion state, integrity identity, scopes, queues, acknowledgments, and governance execution records through an approved schema adapter.

The runtime reference points to and verifies the canonical artifact. It does not replace the artifact or create authority by insertion.

### 5.4 Distributed representations

Local copies, offline stores, Command Post references, retrieval indexes, embeddings, model uploads, caches, deployments, and publications are distributed representations. Each representation must retain enough provenance to resolve the canonical artifact and promotion state.

## 6. Operational Supabase separation

DCSE-DDNA is the constitutional runtime governance project. SC Command Post stores application and operational state.

An SC Command Post record may reference DCSE-DDNA authority. Copying a governance record into the operational project does not make the operational project authoritative.

No physical table, field, RPC, or policy is assumed by D22. Database behavior requires an approved, versioned schema adapter derived from verified live schema or a promoted migration.

## 7. Canonical identity contract

```yaml
canonical_identity:
  schema_version: "1.0"
  object_id: ""
  object_class: ""
  version: ""
  lane: ""
  classification: ""
  promotion_state: ""
  authority_type: "DIRECT_DCS | STANDING_DCSE"
  authority_ref: ""
  github_repository: ""
  github_path: ""
  github_commit_sha: ""
  git_blob_sha: ""
  content_sha256: ""
  supersedes: ""
  superseded_by: ""
  rollback_ref: ""
```

Material governance objects require repository, path, commit, and content identity. Runtime systems must not infer an omitted hash from a label or filename.

## 8. Runtime registry adapter

### 8.1 Adapter requirements

An approved runtime adapter must define:

- project and environment identity;
- verified physical schema mapping;
- permitted read and write operations;
- authentication method without exposing credentials;
- RLS and role expectations;
- idempotency key behavior;
- canonical identity mapping;
- lifecycle and distribution-state mapping;
- acknowledgment and consumption evidence;
- retry and dead-letter behavior;
- reconciliation queries;
- rollback or compensating procedure;
- adapter version and approval reference.

### 8.2 Adapter failure

If the adapter or physical schema cannot be verified:

- disable database-backed authority writes;
- continue GitHub-based read-only source resolution;
- preserve candidate and receipt generation locally or in the repository;
- mark runtime reconciliation `PENDING_ADAPTER`;
- do not invent tables, fields, policies, or successful writes;
- continue unrelated safe work.

## 9. Logical runtime record

```yaml
runtime_source_record:
  schema_version: "1.0"
  runtime_record_id: ""
  canonical_identity_ref: ""
  object_id: ""
  version: ""
  lane: ""
  classification: ""
  promotion_state: ""
  authority_ref: ""
  model_read_scope: []
  write_scope: []
  ps_restricted: false
  ppr_restricted: false
  secret_scan_status: "NOT_RUN"
  runtime_status: "CANDIDATE"
  distribution_state: "NOT_QUEUED"
  idempotency_key: ""
  adapter_version: ""
  created_at: ""
  updated_at: ""
```

The logical record is mapped to physical storage only by the approved adapter.

## 10. Distribution lifecycle

### 10.1 Distribution states

```text
NOT_QUEUED
  -> QUEUED
  -> DISPATCHED
  -> DELIVERED
  -> ACKNOWLEDGED
  -> LOADED
  -> VERIFIED_IN_USE
```

Exceptional states are:

- `RETRY_PENDING`;
- `DELIVERY_FAILED`;
- `ACKNOWLEDGMENT_FAILED`;
- `LOAD_FAILED`;
- `STALE`;
- `REVOKED`;
- `DRIFT`;
- `PENDING_ADAPTER`.

### 10.2 State evidence

| State | Minimum proof |
|---|---|
| `QUEUED` | Durable queue record and target identity. |
| `DISPATCHED` | Transport attempt with attributable sender and timestamp. |
| `DELIVERED` | Target endpoint or mailbox accepted the payload. |
| `ACKNOWLEDGED` | Intended consumer or governed listener acknowledged receipt. |
| `LOADED` | Runtime reports the exact object identity and hash loaded. |
| `VERIFIED_IN_USE` | A governed execution receipt cites the loaded source identity. |

A mailbox or database insert proves only the state directly supported by its receipt.

## 11. Distribution request contract

```yaml
distribution_request:
  schema_version: "1.0"
  request_id: ""
  canonical_identity_ref: ""
  source_state: ""
  target_type: "SUPABASE | LOCAL | OFFLINE | MODEL | INDEX | DEPLOYMENT | PUBLICATION"
  target_id: ""
  target_lane: ""
  target_scope: []
  transport_adapter: ""
  idempotency_key: ""
  required_acknowledgment: ""
  expiration_or_revocation: ""
  requested_by: ""
  requested_at: ""
```

## 12. Model and runtime access

Models and runtimes may access governance through approved GitHub retrieval, operator-provided files, scoped Supabase retrieval, approved local sources, or verified offline packages.

Access must be:

- explicit;
- lane-scoped;
- classification-aware;
- attributable;
- revocable;
- limited to the required source set;
- recorded when the governing environment supports receipts.

Runtime access does not imply write, execution, promotion, deployment, or publication authority.

If a runtime cannot expose its model identifier, record `model_exposed: false`. Do not infer the identifier from branding, interface labels, or assumptions.

## 13. Retrieval, indexes, and caches

Embeddings, chunks, summaries, search results, caches, and retrieved passages are access aids. They are not canonical artifacts.

Before authority-dependent use, verify:

- object and doctrine ID;
- version;
- lane and classification;
- promotion state;
- canonical repository and path;
- commit and content hash;
- supersession state;
- retrieval timestamp and cache freshness.

Stale or incomplete retrieval may support discovery but cannot override the last verified promoted source.

## 14. Change-scope routing and workflow side effects

Every GitHub change must be classified before automated workflows execute.

```yaml
change_scope:
  class: "GOVERNANCE_DOCUMENTATION | GOVERNANCE_RUNTIME | APPLICATION_CODE | DATABASE | DEPLOYMENT | MEDIA | MIXED"
  changed_paths: []
  eligible_workflows: []
  prohibited_workflows: []
  validation_profile: ""
```

A governance-documentation-only commit must not trigger application deployment, production database work, media generation, or model-completion repair workflows unless an approved path rule expressly requires them.

An unrelated workflow failure:

- is recorded as configuration remediation;
- does not invalidate a successful applicable governance validation;
- does not block candidate review unless it reveals a reserved condition or corrupts required evidence;
- must not generate one notification per file commit when safe batching is available.

Workflow path filters, concurrency, notification routing, and documentation-only exclusions must be mechanically tested.

## 15. Promotion and synchronization

### 15.1 Direct DCS sequence

```text
CANDIDATE
  -> VALIDATE
  -> READY_FOR_PROMOTION
  -> DIRECT_DCS exact-object approval
  -> D05 promotion receipt
  -> GitHub canonical update
  -> runtime reference update
  -> distributed-copy update
  -> reconciliation receipt
```

### 15.2 Standing DCSE sequence

```text
ELIGIBLE_ROUTINE_OBJECT
  -> VALIDATE exact D05 Pass-Gate
  -> verify standing-authority scope and limits
  -> D05 routine-promotion receipt citing authority
  -> GitHub and runtime updates as applicable
  -> reconciliation receipt
```

No synchronization step independently promotes an object. D22 distributes and reconciles the D05 result.

## 16. Reconciliation procedure

For each material object:

1. resolve the D05 authority and promotion receipt;
2. resolve GitHub repository, path, commit, blob, and content hash;
3. resolve runtime registry identity through the approved adapter;
4. resolve each required distributed representation;
5. compare lifecycle and distribution states;
6. verify acknowledgments where required;
7. classify mismatches;
8. correct within approved scope;
9. isolate unresolved dependent actions;
10. issue a reconciliation receipt.

## 17. Drift taxonomy

| Drift class | Example | Required response |
|---|---|---|
| `IDENTITY_DRIFT` | Same label points to different hash | Last verified promoted identity controls; dependent use isolates. |
| `STATUS_DRIFT` | GitHub candidate but runtime says active | Correct runtime state; no promotion inferred. |
| `CONTENT_DRIFT` | Distributed file differs from canonical hash | Revoke or replace mismatched copy. |
| `AUTHORITY_DRIFT` | Promotion state lacks valid D05 authority | Revert to non-promoted state pending decision. |
| `DISTRIBUTION_DRIFT` | Target has stale version | Redistribute or revoke target access. |
| `ACKNOWLEDGMENT_DRIFT` | Insert exists but consumption is claimed | Correct claim and obtain actual acknowledgment. |
| `WORKFLOW_DRIFT` | Irrelevant deployment runs for docs-only change | Correct path filters and notification behavior. |
| `ADAPTER_DRIFT` | Schema mapping no longer matches live system | Disable affected writes and update adapter. |

## 18. Conflict resolution

When sources disagree:

1. preserve every conflicting source and identity;
2. identify promotion state and authority reference;
3. compare GitHub commit, blob, and content hash;
4. compare runtime references and adapter version;
5. identify affected consumers and deployments;
6. classify the drift type;
7. rely on the last verified promoted source;
8. correct only within approved authority;
9. record unresolved authority conflicts for DCS;
10. issue the reconciliation receipt.

## 19. Reconciliation receipt

```yaml
reconciliation_receipt:
  schema_version: "1.0"
  receipt_id: ""
  object_ref: ""
  authority_type: "DIRECT_DCS | STANDING_DCSE"
  authority_ref: ""
  promotion_receipt_ref: ""
  canonical_identity: {}
  runtime_records: []
  distributed_representations: []
  acknowledgments: []
  workflow_results: []
  mismatches: []
  corrections: []
  unresolved_findings: []
  resulting_state: ""
  accountable_identity: ""
  reconciled_at: ""
```

The receipt includes references and results, not credentials, secret values, or private reasoning.

## 20. Idempotency, retry, and revocation

- Every material distribution write uses a deterministic idempotency key when the adapter supports it.
- A retry must not create duplicate promotion, asset, queue, or acknowledgment records.
- Retry limits and backoff are adapter-defined and recorded.
- Exhausted retries move the affected distribution to a failure state without claiming delivery.
- Revocation identifies target, object, reason, effective time, and replacement or rollback source.
- Revocation of a distributed copy does not delete the canonical historical artifact.

## 21. Protected lanes and secrets

PS and PPR source content is distributed only through explicitly authorized protected adapters and scopes. Public, SC, SS, TI, DCS employment, and general model retrieval cannot receive protected payloads by inheritance or shared index.

Credentials and secret values are excluded from doctrine payloads, runtime records, logs, commits, screenshots, and handoffs. Credential incidents are contained and recorded without reproducing the value.

## 22. Degraded and offline operation

If GitHub is unavailable but a verified promoted local or offline package exists, safe read-only and reversible work may continue from that package while canonical reconciliation remains pending.

If Supabase is unavailable, GitHub canonical resolution, local validation, candidate construction, and evidence generation may continue. Runtime writes remain pending.

If D22 is unavailable:

- prohibit new promotion claims, authority-dependent distribution, public release, and irreversible synchronization;
- continue safe source recovery, evidence collection, validation, and correction;
- retrieve the last verified promoted D22 when possible;
- isolate only affected actions unless another reserved condition applies.

No runtime may fabricate successful synchronization to avoid a stop.

## 23. Implementation contract

A reusable D22 module must expose equivalent functions:

```python
resolve_authority(object_ref, d05_sources) -> AuthorityResult
resolve_canonical_identity(object_ref, github_adapter) -> CanonicalIdentity
validate_runtime_adapter(adapter) -> AdapterValidation
map_runtime_record(identity, adapter) -> RuntimeRecord
classify_change_scope(changed_paths, workflow_catalog) -> ChangeScope
dispatch_distribution(request, adapter) -> DistributionResult
verify_acknowledgment(distribution_ref) -> AcknowledgmentResult
compare_representations(identity, runtime_records, copies) -> DriftReport
reconcile_object(context) -> ReconciliationReceipt
revoke_distribution(distribution_ref, reason) -> RevocationReceipt
```

Identical verified inputs and adapter versions must produce deterministic classifications and reconciliation results.

## 24. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D22-001 | GitHub commit exists without D05 authority | Artifact remains non-promoted. |
| D22-002 | Runtime row exists without D05 authority | Row does not create authority. |
| D22-003 | Routine object satisfies standing D05 rule | Routine receipt cites exact standing authority and reconciles. |
| D22-004 | Constitutional candidate relies on standing rule | Direct DCS exact-content approval required. |
| D22-005 | Database schema adapter is unverified | Runtime writes disabled; repository-only work continues. |
| D22-006 | Mailbox row is inserted | State may be queued or delivered only as directly proven; acknowledgment is not inferred. |
| D22-007 | Target acknowledges exact hash | Distribution advances to `ACKNOWLEDGED`. |
| D22-008 | Runtime loaded hash differs | `CONTENT_DRIFT`; last verified promoted source controls. |
| D22-009 | Operational Supabase copies governance row | DCSE-DDNA authority remains controlling. |
| D22-010 | Model retrieves stale chunk | Chunk rejected for authority-dependent use and refresh requested. |
| D22-011 | Documentation-only commit triggers Vercel deployment | `WORKFLOW_DRIFT`; governance validation remains independently assessed. |
| D22-012 | Documentation-only commit triggers model repair workflow | `WORKFLOW_DRIFT`; path filters require correction. |
| D22-013 | Retry repeats same idempotency key | No duplicate material record created. |
| D22-014 | Supabase unavailable | GitHub and offline validation continue; runtime reconciliation is pending. |
| D22-015 | PS content targets general index | Distribution blocked and protected source isolated. |
| D22-016 | D22 unavailable | Authority-dependent distribution pauses; safe recovery continues. |

## 25. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| Source identifies as v7.0 with v6.9 parent | Creates native v7.1 candidate | Removes version and parent conflict. |
| Authority uses an ambiguous legacy authority label and only manual Level 0 | Aligns with D05 `DIRECT_DCS` and `STANDING_DCSE` | Preserves sole DCS authority while enabling bounded routine progression. |
| Exact physical runtime fields are mandated without verified adapter | Defines logical records and verified adapter contract | Prevents fabricated schema assumptions. |
| Candidate-to-sync sequence assumes direct approval only | Adds direct and standing D05 sequences | Aligns distribution with corrected promotion rules. |
| Distribution is treated as synchronization | Adds queued through verified-in-use states | Prevents insert, delivery, and consumption confusion. |
| Retrieval and caches lack explicit freshness behavior | Adds provenance and freshness checks | Prevents stale runtime authority. |
| Workflow side effects are not governed | Adds change-scope and path-filter controls | Prevents documentation commits from triggering unrelated builds and email floods. |
| Conflict response can stop broadly | Adds drift taxonomy and affected-action isolation | Preserves safe non-stoppage. |
| Supabase outage lacks repository-first continuation | Adds degraded and offline modes | Supports connected and disconnected operations. |
| No executable reconciliation schema or tests | Adds contracts, module functions, and D22-001 through D22-016 | Enables automation and repeatable proof. |

## 26. Candidate disposition

**Disposition:** `D22_EXECUTABLE_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate with D05, D21, GitHub workflow routing, and approved Supabase adapters; obtain exact DCS decision; run D22-001 through D22-016; reconcile the promoted result.
