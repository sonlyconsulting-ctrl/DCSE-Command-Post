# DCSE Doctrine D20: Product Assembly Methodology v7.1 RC3 Candidate

**Document ID:** DCSE-D20-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D20_Product_Assembly_Methodology.md`  
**Source SHA-256:** `d109caecb9f2fc92b431745216aa300bf4f39fc1759e578095d7ad30455cd722`  
**Promotion dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D05_Baseline_Promotion_v7.1_RC3_CANDIDATE.md`  
**Promotion dependency SHA-256:** `9fb13438dff5dd97d31a54b6daab58d33d7cf028b85057b27a54b6834170cd71`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D20 governs the complete product lifecycle from objective through operation and retirement. It applies to products, product features, product repairs, governed prototypes, reusable modules, public experiences, internal tools, data services, media packages, and deployment units.

D20 ensures that a product is not treated as complete merely because code exists, a page renders, a test passes, a pull request merges, or a deployment URL responds.

The lifecycle is:

```text
INTAKE
  -> DISCOVER
  -> PLAN
  -> BUILD
  -> VERIFY
  -> CORRECT
  -> PACKAGE
  -> READY_FOR_PROMOTION
  -> PROMOTE
  -> DEPLOY_OR_DISTRIBUTE
  -> OPERATE
  -> RECONCILE
  -> CLOSE_OR_RETIRE
```

## 2. Doctrine boundaries

D20 sequences product work. Specialized doctrines retain subject authority.

| Doctrine | D20 relationship |
|---|---|
| D03 | Admission, capability, assignment, and orchestration. |
| D04 | Communication, delivery, acknowledgment, and handoff receipts. |
| D05 | Lifecycle promotion, baselines, rollback, and supersession. |
| D06 | Canonical file, repository, device, and protected-storage routing. |
| D07 | Campaign and public distribution requirements. |
| D08 and D09 | Voice, tone, identity, and brand systems. |
| D11 | Web, Wix, application, responsive, and browser implementation rules. |
| D15 | Database, RLS, migration, backup, and data-integrity controls. |
| D16 | DDNA extraction and reusable-signal candidates. |
| D17 | Adversarial quality and claim analysis when applicable. |
| D18 | Media-production sub-pipeline. |
| D19 | Visual-creation sub-pipeline. |
| D21 | Doctrine routing, runtime logging, capability handling, and acceptance execution. |
| D22 | Canonical source, distribution, workflow routing, and reconciliation. |

D20 does not replace these doctrines or create independent promotion authority.

## 3. Product definition and classes

A product is a governed deliverable intended for repeated use, user interaction, client delivery, internal operation, sale, publication, deployment, or distribution.

Product classes include:

- web application;
- mobile or desktop application;
- website, landing page, or campaign experience;
- Wix page, widget, application, or integration;
- API, service, webhook, or scheduled worker;
- database-backed workflow;
- dashboard, portal, report, or analytic system;
- command-line tool, script, automation, or agent runtime;
- reusable component, library, template, or skill;
- game, quiz, simulation, or interactive learning module;
- media, visual, audio, or campaign package;
- data product, registry, model, or governed dataset;
- open-source model package or local inference workflow;
- combined or multi-platform product.

An artifact that is only historical evidence is not automatically an operational product. Its intended use must be declared.

## 4. Product declaration contract

```yaml
product_declaration:
  schema_version: "1.0"
  product_id: ""
  product_name: ""
  entity: ""
  lane: ""
  classification: ""
  product_class: ""
  objective: ""
  problem_statement: ""
  target_users: []
  user_outcomes: []
  business_outcomes: []
  scope_in: []
  scope_out: []
  platforms: []
  environments: []
  data_classes: []
  integrations: []
  accessibility_profile: ""
  release_posture: "INTERNAL | PREVIEW | PRIVATE_BETA | PUBLIC | PRODUCTION"
  commercial_posture: "NOT_APPLICABLE | INTERNAL_VALUE | FREE | PAID | MIXED"
  acceptance_criteria: []
  reserved_decisions: []
  budget_or_cost_limit_ref: ""
  authority_ref: ""
  rollback_or_discard_ref: ""
  accountable_owner: ""
  created_at: ""
```

Missing non-reserved detail is scaffolded and marked `TO_VERIFY`. Missing authority, legality, confidentiality, lane, credential, public-release, production, or spending information must be surfaced before the affected action.

## 5. Runtime modes

D20 supports:

| Mode | Purpose |
|---|---|
| `NEW_BUILD` | Construct a new product from approved objective. |
| `FEATURE_CHANGE` | Add or materially alter bounded product behavior. |
| `REPAIR` | Diagnose, correct, and verify an existing defect. |
| `AUDIT` | Evaluate current readiness without implementing unapproved changes. |
| `MIGRATION` | Move platform, data, runtime, or architecture. |
| `RELEASE` | Package, promote, deploy, and reconcile a verified build. |
| `RETIREMENT` | Remove use safely while preserving required history and recovery. |

The mode determines applicable phases. A repair may enter at Discover or Verify. A release may enter at Package only when earlier evidence remains current and applicable.

## 6. Phase 1: Intake and admission

### 6.1 Objective

Establish authority, identity, lane, product class, requested outcome, boundaries, and available evidence before material execution.

### 6.2 Required actions

1. normalize the request into the Product Declaration;
2. identify direct and implied deliverables;
3. identify entity and lane boundaries;
4. classify confidentiality, PS, PPR, secrets, and user-data exposure;
5. identify requested release posture;
6. identify existing repository, branch, deployment, database, and product records;
7. run D21 doctrine routing;
8. identify missing capabilities and approved fallbacks;
9. classify reserved decisions;
10. define the evidence destination.

### 6.3 Intake gate

The gate passes when the product identity, objective, lane, mode, release posture, and reserved decisions are known. Reversible scaffolding may proceed while non-reserved facts are marked `TO_VERIFY`.

## 7. Phase 2: Discovery and requirements

### 7.1 Current-state discovery

When an existing product is involved, inspect actual:

- source and branch state;
- application architecture;
- user flows and interface;
- database and migrations;
- authentication and authorization;
- integrations and external services;
- deployment configuration;
- analytics and monitoring;
- known incidents, defects, and audit findings;
- commercial configuration and support obligations.

Narrative, stale screenshots, configuration labels, and task status are not substitutes for current-state evidence.

### 7.2 Requirements

Requirements must cover applicable dimensions:

- functional behavior;
- user journeys and error recovery;
- data contracts and ownership;
- authentication and authorization;
- privacy, security, and retention;
- performance and capacity;
- responsive behavior and accessibility;
- brand, voice, and content;
- integrations and failure behavior;
- observability and support;
- commercial, licensing, pricing, and fulfillment;
- deployment, rollback, and retirement.

### 7.3 Acceptance matrix

```yaml
acceptance_item:
  acceptance_id: ""
  requirement_ref: ""
  user_or_system_outcome: ""
  verification_method: ""
  expected_result: ""
  evidence_type: ""
  severity_if_failed: ""
  responsible_capability: ""
  status: "NOT_RUN"
```

Each material requirement must be testable or explicitly identified as a DCS decision.

## 8. Phase 3: Architecture and execution plan

### 8.1 Architecture record

The plan records:

- component and service boundaries;
- data flows and trust boundaries;
- authentication and authorization paths;
- storage and retention;
- external dependencies;
- environment topology;
- build and deployment path;
- failure, retry, idempotency, and recovery behavior;
- testing strategy;
- monitoring and support ownership;
- cost drivers and limits;
- migration and rollback strategy.

### 8.2 Build versus buy versus reuse

Evaluate existing DCSE components, open-source packages, platform features, APIs, and prior artifacts before creating new infrastructure. Record:

- alternatives considered;
- license and operational implications;
- integration and vendor-lock risks;
- expected cost;
- reuse decision;
- reason for custom development when selected.

### 8.3 Execution plan

Break work into bounded increments with dependencies, acceptance items, rollback boundaries, and evidence outputs. Parallel work must not create overlapping writes or ambiguous ownership.

## 9. Phase 4: Build

### 9.1 General build controls

- preserve existing user changes and unrelated work;
- use the smallest safe change that satisfies the approved objective;
- maintain one authoritative implementation path per function;
- avoid replacement pollers, duplicate APIs, duplicate membership systems, and shadow registries without explicit architecture approval;
- validate inputs and outputs at trust boundaries;
- use dependency and secret controls appropriate to the artifact;
- keep environment-specific values outside source;
- record material decisions and deviations.

### 9.2 Interface products

Applicable interface builds must address:

- semantic structure;
- responsive behavior based on content and supported devices;
- keyboard operation;
- visible focus;
- readable contrast;
- screen-reader semantics;
- reduced motion;
- loading, empty, error, success, offline, and permission states;
- consistent design tokens;
- clear primary and secondary actions;
- prevention of destructive accidental actions;
- first-use and recovery guidance.

The default web target is the applicable promoted accessibility standard, with WCAG 2.2 AA as the v7.1 baseline unless a stricter rule applies.

### 9.3 Data-backed products

Database access may occur directly from a client only when the approved architecture and RLS policies make that path safe. D20 does not require unnecessary mediation APIs.

Applicable controls include:

- verified schema and migrations;
- RLS and role matrix;
- authentication and authorization separation;
- least privilege;
- idempotency and concurrency behavior;
- audit events;
- backup and recovery;
- data retention and deletion;
- synthetic-data testing where protected production data is unnecessary;
- Supabase Security and Performance Advisor review before production promotion.

### 9.4 API, worker, and automation products

Applicable controls include:

- authenticated and authorized entry points;
- bounded input schema;
- rate and resource limits;
- idempotency and duplicate suppression;
- retry and timeout policy;
- heartbeat and liveness evidence where scheduled;
- single-instance or concurrency control where overlap is unsafe;
- structured errors without secret leakage;
- dead-letter or failure recovery;
- attributable execution and result receipts.

### 9.5 Media and visual sub-pipelines

D18 and D19 activate when their product classes apply. Their outputs enter the D20 acceptance matrix and package manifest. Generation does not bypass brand, accessibility, rights, provenance, or release checks.

## 10. Phase 5: Verify

### 10.1 Verification principle

Testing is selected by product class, architecture, data, risk, and release posture. Inapplicable tests are recorded as `NOT_APPLICABLE` with a reason. No fixed checklist is falsely reported as passed.

### 10.2 Test profiles

| Profile | Applies to | Minimum concerns |
|---|---|---|
| Unit | Functions, components, rules, transformations | Expected, boundary, failure, and idempotency behavior. |
| Integration | APIs, databases, services, adapters | Contract, authorization, failure, retry, and data consistency. |
| End-to-end | User or system journeys | Golden path, failure path, recovery, and state persistence. |
| Visual | Rendered interfaces and media | Layout, brand, content, states, responsive behavior. |
| Accessibility | User interfaces and content | Keyboard, focus, semantics, contrast, text alternatives, motion. |
| Security | Trust boundaries and sensitive operations | Secrets, authn, authz, injection, XSS, CSRF, CORS, CSP, uploads, dependencies. |
| Data integrity | Database and data products | Constraints, RLS, migrations, concurrency, reconciliation, backup, recovery. |
| Performance | User-critical and resource-sensitive flows | Response time, payload, rendering, throughput, resource limits. |
| Regression | Existing behavior affected by change | Previously passing critical paths and repaired defect. |
| Compatibility | Supported browsers, devices, embeds, and runtimes | Supported environment matrix. |
| Resilience | Workers, integrations, and remote services | Timeout, retry, degraded mode, duplicate events, restart, and recovery. |
| Commercial | Paid or distributed products | Entitlement, payment boundary, fulfillment, cancellation, terms, support. |

### 10.3 Live preview and first human contact

Any product with a human-visible interface must be exercised through an appropriate preview or target environment. Evidence may include screenshots, interaction traces, accessibility results, console and network results, or an attributable manual receipt.

Source inspection and type checking alone do not prove interface behavior.

### 10.4 Security severity

The following remain blocking when applicable and unresolved:

- credential or secret exposure;
- authentication bypass;
- authorization or RLS failure;
- exploitable injection or unsafe rendering;
- protected-lane leakage;
- destructive behavior outside approved procedure;
- irrecoverable data-integrity risk;
- public or production release without required security evidence.

Other findings are classified by actual severity and handled under D05.

### 10.5 Verification receipt

```yaml
verification_receipt:
  schema_version: "1.0"
  product_ref: ""
  build_ref: ""
  environment_ref: ""
  test_profile: ""
  test_results: []
  evidence_refs: []
  findings: []
  not_applicable: []
  regression_scope: []
  accountable_validator: ""
  self_validation: false
  disposition: ""
  completed_at: ""
```

## 11. Phase 6: Correct and reverify

Correction is a first-class phase, not an exception.

For each failed acceptance item:

1. reproduce or verify the finding;
2. identify root cause and affected scope;
3. determine whether correction is within standing authority;
4. implement the smallest safe correction;
5. rerun the failed test;
6. run affected regression tests;
7. update evidence and unresolved findings;
8. continue until passing, deferred under an applicable rule, or blocked by a reserved condition.

Correctable defects within approved scope do not require repeated conversational approval. A material architecture replacement, destructive operation, security exception, or other reserved decision routes through D05.

## 12. Phase 7: Package

### 12.1 Package contents

An applicable package contains:

- exact source and build identity;
- product declaration;
- requirements and acceptance matrix;
- architecture and dependency record;
- build and configuration artifacts;
- database migrations and rollback when applicable;
- validation and correction receipts;
- security and lane results;
- licenses and third-party notices;
- environment and deployment configuration references;
- operating, monitoring, support, and rollback instructions;
- release notes and known limitations;
- commercial-readiness record when applicable;
- D21 Doctrine Run Plan and consideration references;
- D05 readiness request;
- D22 distribution manifest.

### 12.2 Package manifest

```yaml
product_package:
  schema_version: "1.0"
  package_id: ""
  product_ref: ""
  version: ""
  release_candidate: ""
  repository: ""
  branch_or_tag: ""
  commit_sha: ""
  included_artifacts: []
  included_hashes: []
  dependencies: []
  migrations: []
  validation_refs: []
  findings: []
  licenses: []
  deployment_targets: []
  operation_refs: []
  rollback_ref: ""
  distribution_manifest_ref: ""
  accountable_identity: ""
  packaged_at: ""
```

### 12.3 Registry behavior

Registration uses a verified D22 adapter. A failed or unavailable database adapter does not erase the package. It leaves runtime registration `PENDING_ADAPTER` while GitHub candidate evidence remains available.

No guessed table, field, or successful insert may be reported.

## 13. Phase 8: Promotion readiness and promotion

D20 assembles the product evidence. D05 decides promotion.

### 13.1 Routine promotion

Routine evidence, bounded internal artifacts, sequential BOW transitions, and other eligible product states may advance under an exact DCS-approved standing DCSE rule when every D05 condition is satisfied.

### 13.2 Direct DCS promotion

Direct approval is required for D05 reserved conditions, including uncovered production or public release, material architecture replacement, material spending, security exception, authority expansion, and lane-boundary change.

### 13.3 Non-authority rule

A validator recommendation, passing test suite, preview, merge, deployment, registry row, poller event, or model consensus does not independently promote the product.

## 14. Phase 9: Deploy or distribute

### 14.1 Pre-deployment controls

- verify promoted or expressly authorized release state;
- verify target environment and account;
- verify configuration and secret references;
- verify migration and rollback order;
- verify maintenance or user-impact plan;
- verify monitoring and responsible owner;
- verify D22 workflow eligibility so unrelated products do not deploy.

### 14.2 Deployment strategies

Use the safest strategy appropriate to the product:

- preview or staging;
- private beta;
- canary;
- phased rollout;
- blue-green;
- feature flag;
- direct bounded release;
- file or package distribution.

### 14.3 Production verification

Verify the deployed target rather than relying solely on build evidence:

- health and availability;
- critical user or system path;
- authentication and authorization;
- data and migration state;
- console, network, server, and worker errors;
- analytics or event flow where applicable;
- external integration behavior;
- accessibility and responsive behavior for visible products;
- rollback readiness.

The product is not announced or broadly distributed until the applicable release verification passes.

## 15. Phase 10: Operate, learn, and improve

### 15.1 Operating record

```yaml
product_operation:
  product_ref: ""
  environment_ref: ""
  owner: ""
  support_channel: ""
  health_signals: []
  alerts: []
  service_targets: []
  usage_metrics: []
  cost_metrics: []
  incident_refs: []
  backup_ref: ""
  recovery_test_ref: ""
  review_cadence: ""
  retirement_conditions: []
```

### 15.2 Feedback

Operational evidence may create:

- defect or remediation tasks;
- usability improvements;
- performance and cost improvements;
- security actions;
- DDNA candidates under D16;
- product roadmap changes;
- support or documentation updates.

Feedback is evidence for a new change cycle. It does not silently modify the promoted baseline.

## 16. Commercial readiness

Paid, monetized, licensed, sponsored, or lead-generating products must address:

- offer and target customer;
- pricing and entitlement;
- payment-provider boundary;
- fulfillment and access delivery;
- cancellation, refund, and support process;
- terms, privacy, disclosures, and claim support;
- licensing and intellectual-property rights;
- analytics and conversion measurement;
- customer-data handling;
- operating cost and margin assumptions;
- launch and rollback plan.

Simulated payment success, invented customer demand, or unverified commercial claims are prohibited.

## 17. Product-specific data integrity

Each product defines its domain integrity profile. Examples include:

- sports products: provider identity, league and season mapping, event freshness, scores, status transitions, duplicate events, timezone, postponement, cancellation, and stale-data labeling;
- family products: guardian and child membership scope, consent, private storage, age-appropriate behavior, and role-matrix enforcement;
- campaign products: claim support, link integrity, audience, tracking consent, and publication state;
- governance products: authority, hash, lifecycle, delivery, and acknowledgment integrity;
- employment products: source accuracy, current contact controls, opportunity status, and public-safe facts.

The domain profile becomes part of the acceptance matrix and regression suite.

## 18. Environments and data

Development, test, staging, preview, and production environments must be distinguishable. A preview URL must not silently use production credentials or mutate production data.

Test data should be synthetic or purpose-created when production data is unnecessary. Synthetic data must preserve the shapes, roles, boundary cases, and failure conditions needed for valid testing without impersonating actual users or protected facts.

Production data use requires applicable authority, privacy, minimization, and cleanup controls.

## 19. Cost and resource management

The plan identifies expected use of:

- model tokens and API costs;
- hosting and build minutes;
- storage and bandwidth;
- third-party APIs;
- media generation;
- monitoring and support;
- local compute constraints.

Use the lowest-cost capable runtime that satisfies accuracy, access, risk, and completion requirements. Escalate to higher-cost capability when evidence shows the lower-cost option is insufficient.

Material new spending remains reserved to DCS. Existing bounded budgets may be consumed under their recorded limits.

## 20. Product completion contract

A product is complete only when the applicable conditions are proven:

```yaml
product_completion:
  objective_satisfied: false
  acceptance_matrix_complete: false
  critical_paths_pass: false
  applicable_security_pass: false
  applicable_accessibility_pass: false
  applicable_data_integrity_pass: false
  regression_pass: false
  package_complete: false
  promotion_state: ""
  deployment_state: ""
  production_verification: "NOT_APPLICABLE"
  operational_owner_recorded: false
  rollback_verified: false
  github_state_reconciled: false
  runtime_state_reconciled: false
  unresolved_findings: []
  disposition: "INCOMPLETE"
```

`COMPLETE_WITH_REMEDIATION` is permitted only when the applicable D05 rule expressly allows the remaining findings and creates owned remediation tasks.

## 21. Failure, degraded mode, and non-stoppage

| Condition | Required response |
|---|---|
| Preferred model unavailable | Reassign by capability or use approved fallback. |
| One integration unavailable | Continue independent work; stage adapter or integration evidence. |
| Database adapter unavailable | Disable affected writes; continue repository and test work. |
| Preview unavailable | Diagnose and recover; continue non-preview verification; do not claim interface completion. |
| Test failure | Enter Correct; rerun affected and regression tests. |
| Nonblocking finding | Create remediation and continue when D05 permits. |
| Reserved condition | Isolate affected action and obtain required DCS decision. |
| D20 unavailable | Use applicable specialized doctrines and verified plan; prohibit unsupported completion claims. |

Missing D20 does not globally stop safe unrelated work.

## 22. Retirement

Retirement requires:

- retirement reason and authority;
- user, client, and dependency impact;
- data export, retention, and deletion plan;
- integration and credential revocation;
- deployment removal;
- archive and baseline preservation;
- successor or redirect when applicable;
- rollback window;
- D05 lifecycle transition;
- D22 reconciliation.

## 23. Implementation contract

A reusable D20 module must expose equivalent functions:

```python
declare_product(request, context) -> ProductDeclaration
select_mode(product, request) -> ProductMode
discover_current_state(product, adapters) -> DiscoveryReport
build_acceptance_matrix(requirements, doctrine_plan) -> AcceptanceMatrix
build_execution_plan(product, discovery, requirements) -> ExecutionPlan
classify_test_profiles(product, architecture, release_posture) -> TestPlan
record_build(build_context) -> BuildRecord
run_verification(test_plan, adapters) -> VerificationReceipt
plan_correction(findings, authority_context) -> CorrectionPlan
build_package(product, evidence) -> ProductPackage
request_d05_promotion(package, evidence) -> PromotionRequest
build_distribution_manifest(package, targets) -> DistributionManifest
verify_deployment(target, test_plan) -> DeploymentReceipt
build_completion_receipt(context) -> CompletionReceipt
```

Identical verified inputs, catalogs, and adapter versions must produce deterministic classifications and gates.

## 24. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D20-001 | New product request has clear objective but missing non-reserved structure | Reversible Product Declaration scaffolded with `TO_VERIFY`; work continues. |
| D20-002 | Request lacks production authority | Build and test may proceed; production action isolates. |
| D20-003 | Existing product audit relies only on task narrative | Current repository, runtime, and deployment evidence required. |
| D20-004 | Supabase client uses verified RLS safely | Direct client access permitted; unnecessary mediation API not required. |
| D20-005 | Database-backed product lacks RLS verification | Production readiness fails; correction required. |
| D20-006 | Interface compiles but is not previewed | Interface completion remains unproven. |
| D20-007 | Test fails within approved correction scope | Correct and reverify without new conversational approval. |
| D20-008 | Correction requires architecture replacement | Route reserved D05 decision. |
| D20-009 | Nonblocking registry hygiene finding remains | Remediation task created; progression follows D05 standing rule. |
| D20-010 | Runtime registry adapter is unavailable | GitHub package persists; runtime registration is `PENDING_ADAPTER`. |
| D20-011 | Documentation-only change triggers application deploy | D22 `WORKFLOW_DRIFT`; applicable governance validation remains separate. |
| D20-012 | Sports event feed is stale | Product-specific integrity test fails and stale state is disclosed. |
| D20-013 | Paid product uses simulated successful payment | Commercial readiness fails. |
| D20-014 | Named model is unavailable | Capable attributable fallback selected. |
| D20-015 | Deployment succeeds but critical path fails | Rollback or correction activates; release not complete. |
| D20-016 | Product lacks operating owner or rollback | Completion remains `INCOMPLETE`. |
| D20-017 | Product has allowed minor findings with owned remediation | `COMPLETE_WITH_REMEDIATION` only under exact D05 rule. |
| D20-018 | PS content appears in general product source | Protected content isolates; general build continues only after verified partition. |
| D20-019 | Preview uses production credentials unexpectedly | Security failure; affected environment blocked and contained. |
| D20-020 | Product retirement requested | Data, dependency, credential, archive, rollback, D05, and D22 controls execute. |

## 25. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| Six phases end at deployment | Adds discovery, planning, correction, operation, reconciliation, and retirement | Covers the complete product lifecycle. |
| Product classes focus on web and Wix | Adds services, scripts, data, games, media, local models, and combined products | Matches actual DCSE builds. |
| Intake requires complete structure before work | Adds reversible scaffolding and reserved-fact boundaries | Prevents unnecessary stoppage without fabrication. |
| All database access routed through backend APIs | Permits verified client access with RLS | Avoids duplicate mediation architecture. |
| Fixed responsive, font, security, and test rules apply universally | Uses product, risk, and artifact profiles | Prevents false or irrelevant compliance. |
| All test failures block everything | Adds severity, correction, remediation, and affected-action isolation | Supports safe progress. |
| Registry write is mandatory before promotion | Uses verified D22 adapter and `PENDING_ADAPTER` fallback | Prevents database availability from erasing valid package evidence. |
| Promotion requires manual Level 0 every time | Uses corrected D05 direct and standing authority | Reduces repeated approvals while preserving DCS authority. |
| No commercial-readiness phase | Adds entitlement, payment, claims, licensing, support, privacy, and economics | Supports real product launch. |
| No operations or ownership contract | Adds monitoring, support, cost, incident, backup, and recovery ownership | Prevents deploy-and-abandon behavior. |
| No domain data-integrity profiles | Adds sports, family, campaign, governance, and employment examples | Makes complex products testable. |
| No environment and synthetic-data rules | Adds environment separation and representative safe testing | Protects production and privacy. |
| Missing D20 globally halts | Adds specialized-doctrine fallback and bounded continuation | Preserves safe non-stoppage. |
| No executable completion schema | Adds completion contract, module functions, and D20-001 through D20-020 | Enables automation and auditable closeout. |

## 26. Candidate disposition

**Disposition:** `D20_COMPLETE_PRODUCT_ASSEMBLY_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate against D03 through D22, run D20-001 through D20-020, obtain exact DCS decision, promote through D05, and reconcile through D22.
