# DCSE Doctrine D17: DART Universal Assurance Methodology v7.1 RC3 Candidate

**Document ID:** DCSE-D17-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to entity, confidentiality, privacy, and protected-lane isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md`  
**Source SHA-256:** `ad0ff16e645b450f702fba45b6798128c02ea92b12ab4a67f69ccfa82cd69eee`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D17 defines DART as the universal DCSE assurance and resolution methodology:

1. Define;
2. Assess;
3. Resolve;
4. Test.

DART converts an objective into an evidence-backed, corrected, and verified result. It applies across governed workflows, products, websites, applications, content, employment operations, architecture, data systems, security, accessibility, media, campaigns, research, deployment, and governance.

D17 is not an authority source, promotion service, workflow scheduler, knowledge store, or protected-lane operating manual. D03 assigns capable runtimes, D05 controls promotion, D16 controls DDNA extraction and learning candidates, D20 controls product assembly, D21 controls doctrine routing and execution, and D22 controls canonical identity and distribution.

## 2. Governing principles

1. Criteria are declared before a result is judged.
2. Facts, assumptions, inferences, requirements, preferences, and unknowns remain distinguishable.
3. Assessment examines the complete operating result, not only prose or claims.
4. Identified defects are resolved when safe and authorized before escalation.
5. Testing uses objective evidence and applicable acceptance criteria.
6. A critical-reviewer profile is a test fixture, not an authority source.
7. Confidence language does not replace evidence.
8. Missing evidence produces an accurate disposition rather than an invented conclusion.
9. Findings isolate affected work unless an applicable reserved condition requires broader containment.
10. DART does not create permission, promotion, disclosure, deployment, spending, deletion, or security-exception authority.
11. External data remains external until admitted and reconciled through the applicable source controls.
12. DART and DDNA exchange references and verified candidates without duplicating authority or storage ownership.

## 3. DART run declaration

```yaml
dart_run:
  schema_version: "1.0"
  run_id: ""
  task_id: ""
  conversation_id: ""
  objective: ""
  entity: ""
  lane: ""
  artifact_class: ""
  scope_mode: "FULL | BOUNDED | NOT_REQUIRED"
  selected_phases: []
  acceptance_criteria_refs: []
  source_set_ref: ""
  doctrine_run_plan_ref: ""
  authority_refs: []
  runtime_identity: ""
  started_at: ""
```

`FULL` requires all four phases. `BOUNDED` identifies the selected phases and why omitted phases are unnecessary. `NOT_REQUIRED` records the trigger decision without performing DART.

No output may claim full DART processing unless all four phase receipts exist and the Test phase verifies their linkage.

## 4. Phase D: Define

Define establishes what is being produced, why it matters, what controls it, and how completion will be measured.

### 4.1 Required definition elements

- objective and intended use;
- scope, exclusions, and artifact class;
- entity, lane, classification, and audience;
- decision authority and execution authority;
- controlling sources and applicable doctrine;
- required inputs and known dependencies;
- facts, assumptions, inferences, preferences, and unknowns;
- functional and nonfunctional requirements;
- acceptance criteria and evidence required for each criterion;
- privacy, security, accessibility, and confidentiality constraints;
- cost, time, tool, model, and environment constraints;
- rollback, recovery, or reversibility expectation;
- output format, destination, and lifecycle target.

### 4.2 Definition contract

```yaml
definition_record:
  definition_id: ""
  objective: ""
  intended_use: ""
  artifact_class: ""
  entity: ""
  lane: ""
  classification: ""
  audience_profiles: []
  authority_refs: []
  sources: []
  facts: []
  assumptions: []
  inferences: []
  preferences: []
  unknowns: []
  requirements: []
  acceptance_criteria: []
  constraints: []
  exclusions: []
  rollback_expectation: ""
  required_evidence: []
  output_contract_ref: ""
```

### 4.3 Completion scaffolding

When intent is clear, the runtime creates reversible missing structure such as headings, checklists, schemas, test placeholders, or manifest fields. It must not invent a fact, authority, credential, consent, approval, public-release decision, protected-data classification, deployment result, or final status.

## 5. Source and external-data controls

### 5.1 Source classes

| Class | Meaning | DART treatment |
| --- | --- | --- |
| Canonical | Verified promoted source with exact identity | May control within scope. |
| Governed evidence | Verified receipt, record, test, or artifact | Supports findings within measured scope. |
| User supplied | Material supplied for the current task | Preserve provenance and validate material claims. |
| External | Information outside the verified DCSE canonical source set | Record retrieval, freshness, reliability, rights, and corroboration. |
| Model generated | Generated analysis, summary, or proposal | Candidate reasoning only until verified. |
| Unknown | Source identity or integrity cannot be established | Do not treat as fact. |

### 5.2 External source record

```yaml
external_source:
  source_id: ""
  title: ""
  publisher_or_provider: ""
  url_or_reference: ""
  retrieved_at: ""
  published_at: ""
  source_type: ""
  relevance: ""
  freshness_requirement: ""
  reliability_basis: ""
  corroboration_state: "UNREVIEWED | SINGLE_SOURCE | CORROBORATED | CONFLICTED"
  permitted_use: ""
  privacy_classification: ""
  content_hash_or_snapshot_ref: ""
  role: "EVIDENCE | CONTEXT | LEAD"
```

Retrieval does not promote or absorb external information into DDNA. D16 source admission, D05 promotion, and D22 reconciliation remain separate actions.

## 6. Phase A: Assess

Assess evaluates the defined work against its sources, criteria, constraints, operating environment, and foreseeable failure conditions.

### 6.1 Universal assessment dimensions

- factual accuracy and provenance;
- requirement coverage;
- internal consistency;
- unsupported or overstated claims;
- privacy and confidentiality;
- authorization and lane isolation;
- security and abuse resistance;
- accessibility and usability;
- data integrity and migration behavior;
- failure modes, edge cases, and degraded operation;
- reversibility, rollback, and recovery;
- performance, reliability, and stability;
- cost, resource use, and maintainability;
- compatibility and regression risk;
- audience, channel, brand, and presentation fit;
- licensing, permitted use, and third-party obligations;
- deployment, monitoring, support, and retirement readiness;
- status, delivery, acknowledgment, and completion-claim accuracy.

### 6.2 Claim definition

A claim is a factual, quantitative, security, performance, commercial, compliance, readiness, delivery, operational, or status assertion that could influence a decision, release, deployment, purchase, promotion, or public representation.

Claims are validated in proportion to consequence. Routine descriptive language does not require individual claim records unless its accuracy materially affects the result.

### 6.3 Assessment finding

```yaml
assessment_finding:
  finding_id: ""
  definition_id: ""
  criterion_ref: ""
  category: ""
  condition: ""
  evidence_refs: []
  source_quality: "VERIFIED | SUPPORTED | UNVERIFIED | CONFLICTED"
  severity: "CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL"
  likelihood: ""
  consequence: ""
  affected_scope: []
  privacy_or_security_effect: ""
  rollback_effect: ""
  resolution_required: false
  blocks_intended_use: false
  blocks_promotion: false
```

Assessment does not label a safe difference of preference as a defect. The finding must identify the violated criterion, evidence conflict, or material risk.

## 7. Phase R: Resolve

Resolve corrects defects, reconciles conflicts, implements bounded mitigation, and routes only decisions that cannot be made under current authority.

### 7.1 Resolution order

1. verify that the finding is valid;
2. retrieve available controlling information;
3. identify safe correction options;
4. select the least expansive option that satisfies the criterion;
5. preserve pre-state and rollback or recovery evidence;
6. apply the correction within current authority;
7. retest the affected criterion;
8. record residual effects;
9. route only unresolved authority choices or reserved actions.

### 7.2 Resolution outcomes

| Outcome | Meaning |
| --- | --- |
| CORRECTED | Defect corrected and targeted test passed. |
| MITIGATED | Risk reduced within scope; residual risk remains recorded. |
| ACCEPTED_CONDITION | Condition is intentional and supported by authority and evidence. |
| DEFERRED | Resolution has an identified owner, dependency, and next action. |
| ISOLATED | Affected operation or artifact cannot proceed safely; unrelated work continues. |
| AUTHORITY_DECISION_REQUIRED | Material alternatives remain outside current authority. |
| UNRESOLVED | No verified correction or safe mitigation is available. |

### 7.3 Resolution record

```yaml
resolution_record:
  resolution_id: ""
  finding_id: ""
  selected_outcome: ""
  options_considered: []
  selected_action: ""
  selection_basis: ""
  authority_ref: ""
  pre_state_ref: ""
  change_refs: []
  rollback_or_recovery_ref: ""
  targeted_test_refs: []
  residual_risk: ""
  next_actor: ""
  next_action: ""
  due_or_recheck_condition: ""
```

DART does not broaden access, disable a control, claim delivery, invent approval, or mark work complete merely to clear a finding.

## 8. Phase T: Test

Test verifies the corrected deliverable against the declared acceptance criteria and intended operating context.

### 8.1 Test classes

Tests may include:

- source and factual verification;
- requirement traceability;
- positive and negative authorization tests;
- security and privacy tests;
- accessibility inspection and interaction tests;
- functional and integration tests;
- regression and compatibility tests;
- performance and resilience tests;
- rollback and recovery tests;
- deployment and monitoring checks;
- audience, channel, voice, and brand checks;
- evidence, receipt, and reconciliation checks.

### 8.2 Objective audience test

The deliverable passes its audience test only when it satisfies the declared acceptance criteria, required evidence, applicable doctrine tests, and documented needs of the authorized audience. A critical-reviewer profile may be used as a test fixture but cannot create requirements, authority, or indefinite work.

### 8.3 Dispositions

| Disposition | Required condition |
| --- | --- |
| PASS | All blocking criteria pass and no unresolved blocking finding remains. |
| PASS_WITH_CORRECTIONS | Intended use is permitted, but recorded nonblocking corrections remain. |
| FAIL | One or more blocking criteria fail. |
| INSUFFICIENT_EVIDENCE | Required evidence is absent, invalid, inaccessible, or inconclusive. |

General confidence labels are not final dispositions. Confidence may be recorded only for a specific inference or probabilistic classification with its basis, missing evidence, and effect if incorrect.

### 8.4 Verification receipt

```yaml
dart_verification_receipt:
  receipt_id: ""
  run_id: ""
  definition_ref: ""
  assessment_refs: []
  resolution_refs: []
  acceptance_results: []
  positive_tests: []
  negative_tests: []
  regression_tests: []
  rollback_or_recovery_tests: []
  evidence_coverage: ""
  unresolved_material_items: []
  disposition: "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE"
  intended_use_allowed: false
  promotion_ready: false
  authority_refs: []
  verified_at: ""
```

`promotion_ready` is evidence for D05. It is not promotion.

## 9. Trigger system

### 9.1 Explicit triggers

D17 is selected when:

- DCS directs DART use;
- a registered workflow, skill, task type, or artifact profile declares D17;
- an approved acceptance plan requires D17;
- a promotion or readiness packet requires independent assurance.

Specific skill names must not be hardcoded in doctrine. A skill activates D17 through verified metadata such as `required_doctrines: [D17]`.

### 9.2 Implicit triggers

The D21 trigger catalog should select full or bounded D17 when work includes:

- website, application, service, automation, or product build;
- UI, UX, accessibility, or customer-journey evaluation;
- architecture, technology, provider, model, or vendor selection;
- database, RLS, RPC, migration, security, privacy, or credential change;
- deployment, rollback, recovery, incident, or operational-readiness decision;
- employment role intake, opportunity validation, application asset, negotiation, or interview preparation;
- campaign, brand, public content, commercial claim, pricing, or publication;
- media, visual, audio, or video production;
- external research, market analysis, source verification, or data acquisition;
- governance, audit, promotion, status, delivery, or completion assertion.

### 9.3 Deterministic trigger record

```yaml
dart_trigger_decision:
  decision_id: ""
  task_id: ""
  catalog_version: ""
  catalog_hash: ""
  matched_rules: []
  triggering_characteristics: []
  scope_mode: "FULL | BOUNDED | NOT_REQUIRED"
  selected_phases: []
  reason: ""
  recorded_in_dcl: true
```

Trigger selection must not depend solely on model intuition. If catalog access fails, D21 may use a recorded fallback catalog without expanding protected access or authority.

### 9.4 Visibility

DART activation is always recorded in the Doctrine Consideration Log. A user-facing announcement is required only when activation materially changes scope, time, cost, access, output, or a pending authority decision.

## 10. Full and bounded DART

Full DART is required for material release, promotion, public claims, security-sensitive change, architecture decision, employment submission, commercial release, production deployment, and any task whose acceptance plan requires all phases.

Bounded DART may be used for routine refinement, internal drafting, low-risk comparison, or targeted retest. The run must identify the selected phases and may not claim full DART completion.

A small task is not exempt merely because its output is short. Consequence, not length, controls assurance scope.

## 11. Domain workflow and skill integration

A domain workflow is an executable profile, not automatically a doctrine.

```yaml
domain_workflow:
  workflow_id: ""
  version: ""
  goals: []
  triggers: []
  required_inputs: []
  stages: []
  required_doctrines: []
  capability_requirements: []
  permissions: []
  external_source_rules: []
  output_contracts: []
  acceptance_tests: []
  privacy_controls: []
  rollback_or_recovery: []
  evidence_contract_ref: ""
```

Gemini, Claude, ChatGPT, Qwen, local models, scripts, or future runtimes may execute the same workflow through admitted adapters. Provider identity does not redefine the workflow or its goals.

## 12. DART and DDNA coordination

D16 and D17 operate in a controlled sequence with bounded parallel preparation:

```text
D21 route
  -> D16 source admission and extraction
  -> D17 Define
  -> D17 Assess
  -> D17 Resolve
  -> D17 Test
  -> D16 verified learning candidate
  -> D05 lifecycle decision
  -> D22 reconciliation and distribution
```

Parallel source extraction or independent assessment is permitted when each stream uses the same declared source set, lane, classification, and task identity. Results join before Resolve.

D16 produces signals and knowledge candidates. D17 produces findings, resolutions, tests, and dispositions. Neither creates promotion authority.

Deduplication uses source identity, content hash, normalized claim or finding ID, task ID, main theme, entity, lane, and candidate lineage. Protected or confidential material is isolated before either doctrine processes it.

## 13. Stop, isolation, and rollback boundary

DART considers whether a condition affects authorization, confidentiality, privacy, security, accessibility, public release, destructive action, deployment, rollback, recovery, or final status.

DART may recommend `ISOLATED` or `AUTHORITY_DECISION_REQUIRED`. D21 applies affected-action isolation and applicable Stop-Gates. D05 controls promotion and rollback authority.

Missing D17 isolates only work whose assurance requirement cannot otherwise be satisfied. Unrelated safe work continues. A runtime must not manufacture a DART receipt from memory.

## 14. Output and branding boundary

DART evidence is recorded in internal metadata or receipts. A mandatory visible proprietary tag must not be inserted into every customer, public, employment, product, or operational deliverable.

Visible branding, notices, confidentiality markings, and public attribution follow the applicable artifact, brand, publication, privacy, and distribution controls.

## 15. Runtime interfaces

```text
select_dart_scope(task_declaration, trigger_catalog) -> DartTriggerDecision
define_work(task_declaration, sources, criteria) -> DefinitionRecord
assess_work(definition, artifact, evidence) -> AssessmentFindings
resolve_findings(findings, authority, capabilities) -> ResolutionRecords
test_result(definition, artifact, resolutions, test_plan) -> DartVerificationReceipt
emit_learning_candidate(receipt, sources) -> DDNAFeedbackCandidate
```

## 16. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D17-001 | D17 source is selected | Four phases resolve as Define, Assess, Resolve, Test. |
| D17-002 | Source contains legacy legal phase terms | Static gate fails. |
| D17-003 | Task lacks acceptance criteria | Define creates reversible scaffolding and records missing authority-sensitive facts. |
| D17-004 | External market source is used | Retrieval, freshness, reliability, rights, and corroboration are recorded. |
| D17-005 | Model-generated summary is fluent | It remains candidate analysis until verified. |
| D17-006 | Claim affects public pricing | Evidence and permitted-use checks are required. |
| D17-007 | Preference differs from output | No defect is created without a violated criterion or material risk. |
| D17-008 | Security finding has safe bounded fix | Resolve applies within authority, preserves pre-state, and retests. |
| D17-009 | Proposed fix broadens database access | Resolution is rejected or routed for authority and security review. |
| D17-010 | Rollback is required but untested | Test cannot return PASS. |
| D17-011 | Accessibility criterion fails | Disposition reflects the failed intended-use criterion. |
| D17-012 | Evidence is unavailable | Disposition is INSUFFICIENT_EVIDENCE. |
| D17-013 | Nonblocking correction remains | PASS_WITH_CORRECTIONS identifies criterion, owner, and next action. |
| D17-014 | General confidence is high but tests fail | Disposition remains FAIL. |
| D17-015 | Critical-reviewer profile adds a new demand | Demand is not treated as authority or acceptance criterion. |
| D17-016 | Registered skill declares D17 | D21 selects D17 from verified skill metadata. |
| D17-017 | Unregistered example skill name appears | Doctrine does not infer execution rights or capability. |
| D17-018 | Product build is material | Full DART is selected unless an approved acceptance plan proves bounded scope. |
| D17-019 | Routine low-risk retest occurs | Bounded DART records selected phases and cannot claim full completion. |
| D17-020 | DART activates without material user impact | DCL records it without mandatory conversational announcement. |
| D17-021 | DDNA and DART process same source | Outputs remain distinct and deduplicate by declared identifiers. |
| D17-022 | Protected source appears | Affected content is isolated before general processing. |
| D17-023 | DART recommends stopping | D21 evaluates the actual reserved condition; DART does not create authority. |
| D17-024 | D17 is unavailable | Only assurance-dependent work is isolated. |

## 17. Cross-doctrine boundaries

- D01 governs constructive next-state reasoning.
- D02 governs forward derivation and backward proof.
- D03 assigns admitted capabilities.
- D04 governs communication and delivery evidence.
- D05 governs promotion, rollback, and supersession.
- D06 governs file and device evidence.
- D08 through D12 govern artifact-specific voice, brand, persona, application, and media controls.
- D15 governs database and data-service security.
- D16 governs DDNA source admission, extraction, and learning candidates.
- D18 and D19 govern media and visual pipelines.
- D20 governs complete product assembly and readiness.
- D21 governs routing, execution, isolation, and doctrine consideration.
- D22 governs canonical identity, runtime reference, distribution, and reconciliation.

## 18. Source correction record

| Source condition | RC3 correction | Reason |
| --- | --- | --- |
| Legal and adversarial phase vocabulary | Define, Assess, Resolve, Test | Establishes a universal operational method. |
| Position-defense framing | Assurance, correction, and verification | Covers products, operations, content, employment, and governance. |
| Subjective toughest-audience requirement | Declared criteria and authorized audience | Prevents indefinite or invented requirements. |
| General confidence rating | Objective disposition and evidence coverage | Prevents confidence from replacing proof. |
| Fixed example skill names | Registry-driven workflow metadata | Avoids fictional capabilities and stale names. |
| Narrow implicit triggers | Versioned enterprise trigger catalog | Covers current DCSE work classes consistently. |
| Mandatory activation announcement | DCL record plus material-impact notice | Preserves auditability without conversational noise. |
| Global halt on protected material | Pre-processing isolation and D21 routing | Protects boundaries while unrelated work continues. |
| Mandatory visible proprietary tag | Artifact-specific branding control | Prevents inappropriate labels on public or employment outputs. |
| DART and DDNA overlap undefined | Distinct outputs, sequence, deduplication, and feedback | Prevents duplicated authority and learning drift. |

## 19. Candidate status

This candidate is correction evidence only. It does not replace the active D17, activate a workflow, promote DDNA learning, or change runtime routing until DCS promotes the exact artifact or exact diff and D22 records the authoritative representation.
