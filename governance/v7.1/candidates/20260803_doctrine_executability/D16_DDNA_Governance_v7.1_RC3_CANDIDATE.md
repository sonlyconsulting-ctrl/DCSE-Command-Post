# DCSE Doctrine D16: DDNA Governance v7.1 RC3 Candidate

**Document ID:** DCSE-D16-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D16_DDNA_Governance.md`  
**Source SHA-256:** `6365c8501e289c4516cf80001c0994b986a267a581040b8f81f34ef3fb402e8b`  
**Promotion candidate dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D05_Baseline_Promotion_v7.1_RC3_CANDIDATE.md`  
**Promotion candidate dependency SHA-256:** `9fb13438dff5dd97d31a54b6daab58d33d7cf028b85057b27a54b6834170cd71`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Runtime candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D22 reconciliation is complete.  

## 1. Purpose

D16 governs DDNA signal extraction, classification, candidate creation, feedback routing, and evidence production. DDNA captures reusable value from authorized conversations, artifacts, build records, reviews, and operational events without converting those sources into authority.

D16 governs what DDNA produces. D03 governs orchestration. D05 governs lifecycle and promotion. D21 governs runtime execution and consideration logging. D22 governs canonical identity and distribution.

## 2. Non-authority boundary

D16 may:

- identify and classify reusable signals;
- create internal candidate assets;
- generate evidence and recommendations;
- write staging records through approved adapters;
- request a D05 lifecycle evaluation;
- route accepted signals to the correct doctrine or product owner.

D16 may not independently:

- ratify or promote doctrine;
- authorize public or production release;
- expand lane, data, model, or credential access;
- convert a registry insert into authority;
- override a D05 reserved condition;
- treat model consensus or extraction confidence as promotion approval.

## 3. DDNA signal model

DDNA evaluates five signal layers.

| Layer | Question | Typical output |
|---|---|---|
| Sentiment | What verified voice, posture, preference, or friction signal exists? | Voice rule or preference candidate. |
| Logic | What workflow, decision, dependency, or routing rule exists? | Process or doctrine candidate. |
| Design | What visual, structural, or interaction pattern exists? | Design-system candidate. |
| Product | What reusable, packageable, or commercial opportunity exists? | Product or feature candidate. |
| Technical | What automation, integration, data, testing, or infrastructure implication exists? | Technical task or architecture candidate. |

Every layer must be evaluated. A layer with no supported signal is recorded as `NOT_APPLICABLE` or `NO_SUPPORTED_SIGNAL`; output is not invented merely to populate all five layers.

## 4. Source admission

### 4.1 Required source declaration

```yaml
ddna_source:
  source_id: ""
  source_type: "CONVERSATION | ARTIFACT | BUILD_LOG | REVIEW | EVENT | HYBRID"
  canonical_ref: ""
  source_hash: ""
  entity: ""
  lane: ""
  classification: ""
  authority_to_process_ref: ""
  contains_ps: false
  contains_ppr: false
  contains_secrets: false
  retention_class: ""
  admitted_at: ""
```

### 4.2 Admission rules

Before extraction, D16 must:

1. verify source availability and identity;
2. classify entity, lane, confidentiality, and release posture;
3. apply PS and PPR isolation before any cloud or cross-lane operation;
4. remove or isolate secret values;
5. confirm authority to process the source;
6. record unavailable or unverifiable source portions;
7. prohibit unsupported factual inference.

## 5. PS, PPR, confidentiality, and secrets

PS and PPR content remains inside its authorized lane and storage boundary. A mixed source must be partitioned before general DDNA processing. The public-safe or enterprise-safe portion may continue only when the separation is verifiable.

If safe partitioning is not possible:

- isolate the source;
- record `BLOCKED_RESERVED` for the affected extraction;
- preserve unrelated authorized work;
- route the required DCS decision without exposing protected content.

Secret values are never copied into DDNA output, registry payloads, receipts, prompts, commits, or summaries. Exposure triggers containment and the applicable security process without repeating the value.

## 6. Extraction triggers

D16 may activate through:

| Trigger | Condition |
|---|---|
| Direct instruction | DCS or an authorized task requests DDNA extraction. |
| Material correction | A correction reveals a reusable governance, process, or design rule. |
| Artifact creation | A substantive governed artifact is created or materially changed. |
| Repeated friction | The same verified execution defect occurs more than once. |
| Product signal | A reusable or commercial candidate is supported by evidence. |
| Scheduled sweep | An approved job evaluates eligible staged sources. |
| Session close | The runtime identifies material signals that satisfy the configured threshold. |

Triggers start evaluation. They do not guarantee that an asset will be created or promoted.

## 7. Extraction workflow

The logical workflow is:

```text
ADMIT_SOURCE
  -> CLASSIFY_BOUNDARIES
  -> PARTITION_PROTECTED_CONTENT
  -> EVALUATE_FIVE_LAYERS
  -> VERIFY_SIGNAL_SUPPORT
  -> DEDUPLICATE
  -> CLASSIFY_CANDIDATES
  -> BUILD_EVIDENCE
  -> STAGE_OUTPUTS
  -> REQUEST_D05_EVALUATION
  -> ROUTE_FEEDBACK
  -> RECONCILE
```

Failure at one layer or candidate isolates that item. Other independently supported layers continue.

## 8. Signal record contract

```yaml
ddna_signal:
  schema_version: "1.0"
  signal_id: ""
  source_ref: ""
  source_hash: ""
  layer: "SENTIMENT | LOGIC | DESIGN | PRODUCT | TECHNICAL"
  signal_type: ""
  statement: ""
  evidence_refs: []
  confidence_basis: "VERIFIED | LIKELY | UNKNOWN"
  applicability: "APPLICABLE | NOT_APPLICABLE | NO_SUPPORTED_SIGNAL"
  entity: ""
  lane: ""
  classification: ""
  restrictions: []
  duplicate_of: ""
  candidate_refs: []
  accountable_identity: ""
  created_at: ""
```

`confidence_basis` describes the evidence posture. It is not a promotion score.

## 9. Candidate asset contract

```yaml
ddna_candidate:
  schema_version: "1.0"
  candidate_id: ""
  candidate_class: "DOCTRINE | PROCESS | DESIGN | PRODUCT | TECHNICAL | CONTENT"
  title: ""
  description: ""
  source_signal_refs: []
  parent_refs: []
  entity: ""
  lane: ""
  classification: ""
  intended_audience: ""
  release_posture: "INTERNAL | PUBLIC_CANDIDATE | PRODUCTION_CANDIDATE"
  canonical_candidate_ref: ""
  content_sha256: ""
  validation_refs: []
  unresolved_findings: []
  d05_requested_transition: ""
  d05_disposition: "NOT_EVALUATED"
  rollback_or_discard_ref: ""
  accountable_identity: ""
  created_at: ""
```

## 10. Deduplication and change detection

Before creating a new candidate, D16 searches the approved source catalogs and available staging records for:

- matching canonical identity;
- identical or substantially overlapping signal;
- prior superseded candidate;
- existing remediation task;
- active doctrine or product rule already covering the issue.

The result must be one of:

- `NEW_CANDIDATE`;
- `UPDATE_EXISTING_CANDIDATE`;
- `LINK_EXISTING_ASSET`;
- `DUPLICATE_NO_NEW_ASSET`;
- `CONFLICT_REQUIRES_RECONCILIATION`.

D16 preserves source attribution and does not silently overwrite prior signal history.

## 11. Storage adapter contract

D16 defines logical record types, not guessed physical tables or local folders.

An adapter may target GitHub, DCSE-DDNA Supabase, an approved local store, or a controlled offline store only when it provides:

- verified schema or path mapping;
- permitted read and write operations;
- lane and classification enforcement;
- idempotency behavior;
- secret filtering;
- record identity and hash handling;
- error and retry behavior;
- reconciliation references.

If the database schema is unverified, database writes are disabled. Repository-based candidate creation and offline evidence generation may continue within authorized scope.

## 12. D05 lifecycle handoff

D16 produces candidates and evidence. D05 decides the lifecycle transition.

### 12.1 D16-authorized operational states

D16 may record:

- `SOURCE_ADMITTED`;
- `EXTRACTING`;
- `SIGNALS_VERIFIED`;
- `CANDIDATE_STAGED`;
- `READY_FOR_D05_EVALUATION`;
- `CORRECTING`;
- `DEFERRED_NONBLOCKING`;
- `BLOCKED_CAPABILITY`;
- `BLOCKED_RESERVED`.

These states do not imply promotion.

### 12.2 D05-controlled states

`PROMOTED`, `RELEASED`, `SUPERSEDED`, `ROLLED_BACK`, and final lifecycle reconciliation require the applicable D05 authority and D22 evidence.

### 12.3 Routine standing authority

An internal DDNA candidate may advance automatically only when a DCS-approved standing rule expressly covers its object class, Pass-Gate, evidence, limits, and rollback. The D05 receipt must cite that rule.

Doctrine changes, constitutional changes, authority changes, protected-lane changes, and uncovered public or production releases require direct DCS review under D05.

## 13. Feedback routing

Verified candidates route by subject:

| Signal | Default destination |
|---|---|
| Sentiment and voice | D08 or the applicable persona and communications owner. |
| Logic and orchestration | D03, D21, or the applicable workflow owner. |
| Design and interface | D09, D11, D19, or product design owner. |
| Product | D20 and the owning product lane. |
| Technical and database | D06, D15, D21, or the owning system. |
| Source and distribution | D22. |
| Baseline and promotion | D05. |

Routing creates a candidate or task. It does not modify the destination doctrine automatically.

## 14. Capability-based execution

D16 assigns work by required capability, access, cost, and risk rather than a fixed named model.

An execution receipt records:

```yaml
runtime_identity:
  runtime_name: ""
  model_id: ""
  model_exposed: true
  capabilities_used: []
  access_methods: []
  limitations: []
  self_validation: false
```

If the runtime does not expose its model identifier, `model_exposed` is `false` and the model is not guessed. A missing preferred runtime triggers capable reassignment or bounded fallback, not automatic global stoppage.

## 15. Quality controls

Each output must pass the applicable checks:

- source identity verified;
- evidence references retrievable;
- lane and classification correct;
- PS and PPR isolation verified;
- secrets excluded;
- statements separated into verified, likely, and unknown;
- candidate deduplicated;
- canonical candidate identity assigned;
- D05 transition request correctly classified;
- rollback or discard path recorded;
- adapter result acknowledged rather than merely inserted.

An unsupported signal is corrected or removed. D16 does not fill gaps with plausible narrative.

## 16. Session-close behavior

At closeout, D16 performs a bounded surface check:

1. identify material reusable signals;
2. identify repeated corrections or friction;
3. identify product or automation candidates;
4. identify source, lane, or confidentiality risks;
5. stage supported candidates or record that no material candidate exists;
6. include DDNA references in the general closeout receipt.

The closeout check does not require a new asset for every conversation. A mailbox insert is not delivery, and a registry insert is not consumption or promotion.

## 17. Error and degraded-mode protocol

| Condition | Required behavior |
|---|---|
| Source unavailable | Record exact gap; continue only with verified available material. |
| One signal layer fails | Isolate that layer; continue independent layers. |
| Database adapter invalid | Disable database writes; use repository or approved offline evidence mode. |
| Preferred model unavailable | Reassign by capability or use approved fallback. |
| Protected content detected | Partition or isolate affected source; preserve unrelated work. |
| Candidate conflicts with promoted doctrine | Preserve both; route D22 reconciliation; promoted source controls. |
| D05 unavailable | Stage evidence only; do not promote; recover last verified D05. |
| D16 unavailable | Do not invent DDNA policy; continue non-DDNA task work that does not depend on it. |

## 18. DDNA run receipt

```yaml
ddna_run_receipt:
  schema_version: "1.0"
  run_id: ""
  source_refs: []
  admitted_sources: []
  excluded_sources: []
  layer_results: []
  signal_refs: []
  candidate_refs: []
  duplicate_refs: []
  protection_events: []
  validation_results: []
  d05_requests: []
  adapter_results: []
  unresolved_findings: []
  accountable_identity: ""
  started_at: ""
  completed_at: ""
  disposition: ""
```

## 19. Implementation contract

A reusable D16 module must expose equivalent functions:

```python
admit_source(source, authority_context) -> SourceAdmission
classify_boundaries(source) -> BoundaryResult
partition_protected_source(source, boundary_result) -> PartitionResult
extract_signals(source, layer_catalog) -> list[Signal]
verify_signal(signal, evidence) -> ValidationResult
deduplicate_signal(signal, catalogs) -> DeduplicationResult
build_candidate(signals, candidate_class) -> Candidate
validate_candidate(candidate) -> ValidationResult
stage_records(records, adapter) -> AdapterResult
request_d05_transition(candidate, evidence) -> PromotionRequest
route_feedback(candidate, doctrine_catalog) -> RoutingResult
build_run_receipt(context) -> DDnaRunReceipt
```

Identical verified inputs and catalogs must produce deterministic classifications. Generative wording may vary only where wording is not used as identity, evidence, or authority.

## 20. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D16-001 | Supported source contains signals in two layers | Two supported layers emitted; other layers recorded without invented content. |
| D16-002 | Mixed PS and SC source | PS portion isolates; SC portion continues only after verified partition. |
| D16-003 | Secret appears in source | Secret excluded; containment event recorded without repeating value. |
| D16-004 | Existing candidate covers the signal | Existing asset linked; no duplicate created. |
| D16-005 | Database schema is unverified | Database writes disabled; repository or offline staging continues. |
| D16-006 | Internal candidate matches standing D05 rule | D05 evaluates routine transition and records authority reference. |
| D16-007 | Candidate changes doctrine | Direct DCS exact-content approval required under D05. |
| D16-008 | Public candidate lacks standing authority | Remains ready for D05 review; no release. |
| D16-009 | Named model unavailable | Capable attributable fallback selected. |
| D16-010 | Runtime model identity is hidden | `model_exposed: false`; no model invented. |
| D16-011 | One layer extraction fails | Failed layer isolates; independent layers continue. |
| D16-012 | Registry insert succeeds but no acknowledgment exists | Insert recorded; delivery and consumption remain unconfirmed. |
| D16-013 | Candidate conflicts with promoted doctrine | Promoted doctrine controls; D22 reconciliation requested. |
| D16-014 | Source evidence is insufficient | Signal marked unknown or removed; no fabricated candidate. |
| D16-015 | No material signal exists | Valid no-candidate receipt issued. |
| D16-016 | D05 unavailable | Evidence stages; promotion remains prohibited; safe extraction may continue. |

## 21. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| D16 identifies internally as v6.9 | Creates native v7.1 candidate | Removes runtime-version conflict. |
| Fixed local Hub paths control all output | Uses verified storage adapters and logical record types | Supports connected and disconnected execution without invented paths. |
| D16 defines separate Level 0 and Level 1 gates | Routes every promotion decision through D05 | Eliminates competing authority. |
| All five layers must produce content | Requires evaluation but permits evidenced no-signal results | Prevents fabricated filler. |
| Named models appear in signal examples | Uses capability-based assignment and honest provenance | Avoids vendor dependency. |
| Quality failure halts all extraction | Isolates affected layer or candidate | Preserves safe non-stoppage. |
| Registry write is treated as workflow completion | Separates insertion, acknowledgment, consumption, and promotion | Prevents false reporting. |
| Session close requires physical Tribunal file | Uses approved closeout and communication adapters | Removes unverified local dependency. |
| Feedback loop can appear to modify doctrine directly | Creates routed candidates subject to D05 | Protects constitutional authority. |

## 22. Candidate disposition

**Disposition:** `D16_EXECUTABLE_CANDIDATE_PENDING_D05_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate against D05, D03, D21, D22, lane controls, and approved adapters; obtain exact DCS decision; run D16-001 through D16-016.
