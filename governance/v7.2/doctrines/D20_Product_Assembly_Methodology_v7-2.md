# DCSE Doctrine D20: Product Assembly Methodology

**Document ID:** DCSE-D20  
**Version:** v7.2  
**Created Date/Time:** 2026-07-25T23:00:00-04:00  
**Last Doc Modified Date/Time:** 2026-09-10T15:22:00-04:00  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Classification:** INTERNAL  
**Lane:** DCSE/ALL  
**Canonical File:** D20_Product_Assembly_Methodology_v7-2.md  
**Parent Document:** DCSE_Master_Profile_v7-2.md  
**Doctrine Description:** D20 governs the end-to-end DCSE product and system assembly methodology from intake through deployment and reusable-pattern capture. v7.2 adds the controlling Reuse Before Redesign requirement so validated architectures, components, integrations, configurations, workflows, and implementation patterns are searched, evaluated, reused, adapted, or composed before redesign is authorized.

---

## 1. Product Assembly as Consolidated Methodology

A product in DCSE is any deliverable that reaches a user, client, internal operator, governed system, or public audience, including web applications, embedded widgets, standalone HTML tools, dashboards, calculators, landing pages, API endpoints, packaged media, automation modules, AI-assisted workflows, governed data products, and branded content systems.

D20 sequences the work. Related doctrines retain their specialized authority. D20 shall not be used to bypass D05 promotion, D06 routing, D09 brand controls, D11 technical implementation standards, D16 DDNA governance, D21 runtime controls, or D22 source-authority and runtime-distribution controls.

---

## 2. Controlling Principle: Reuse Before Redesign

### 2.1 Mandatory Reuse Evaluation

Before designing, configuring, integrating, or implementing a product or technical capability, DCSE shall determine whether a previously validated architecture, component, integration, configuration pattern, workflow, implementation, schema, adapter, deployment pattern, test harness, or governed process satisfies all or part of the requirement.

**Reuse Before Redesign is mandatory.** Proven solutions shall be reused, duplicated, composed, or adapted when appropriate. Reconstruction from scratch requires a material justification based on changed requirements, security, compatibility, scale, performance, maintainability, cost, governance, obsolescence, or demonstrated deficiency.

### 2.2 Successful Implementation Knowledge Shall Not Be Rediscovered

Once a Vercel, Supabase, GitHub, API, MCP, plugin, connector, authentication, environment-variable, secrets/Vault, storage, CRUD, deployment, testing, rollback, registry, DDNA, Tribunal, or comparable technology pattern has been successfully implemented and validated, the reusable architecture and configuration requirements shall be captured so later work begins from that proven baseline.

Secret values shall never be copied into reusable patterns. Capture only secret requirements, names or roles, approved storage locations, injection mechanisms, access boundaries, and validation procedures.

### 2.3 Reuse Decision

Every material build shall classify relevant prior solutions as one or more of:

- **REUSE:** use the validated solution substantially as-is.
- **ADAPT:** retain the proven architecture and modify bounded elements.
- **COMPOSE:** combine multiple validated capabilities.
- **REDESIGN:** replace or rebuild only where evidence demonstrates a material reason.

The decision and justification become part of the product or system evidence record.

### 2.4 Persistence and Provenance

Reusable implementation knowledge shall have one canonical artifact home and governed references to related state and evidence according to D22:

- GitHub stores versioned source and governed artifacts.
- Supabase stores structured state, registries, relationships, runtime status, integrity metadata, and canonical references.
- Tribunal stores material decision, approval, execution, validation, exception, and promotion evidence.
- Approved object storage stores large or binary artifacts where Git is not the appropriate canonical surface.
- Approved Vault or secret-management surfaces store secret values.

A GitHub commit, Supabase row, Tribunal receipt, model statement, local file, or deployment does not independently create authority unless the governing promotion and source-authority rules are satisfied.

---

## 3. Product Assembly Lifecycle

### 3.1 Phase 1: Intake

Objective: Define exactly what is being built, for which entity, destination, audience, constraints, and authority before implementation begins.

Required actions:

1. Define product/system name and governed identifier.
2. Define entity/lane, audience, destination, product type, platform, constraints, dependencies, and required approvals.
3. Identify applicable doctrine through the current doctrine routing mechanism.
4. Identify integration requirements including Supabase, GitHub, Tribunal, deployment, APIs, storage, authentication, plugins, MCP services, and external systems.
5. Establish evidence state and known assumptions.

**Quality Gate:** No material implementation proceeds without sufficient intake framing.

### 3.2 Reuse-Before-Redesign Gate

Before Build, search existing DCSE repositories, registries, approved baselines, DDNA records, Tribunal evidence, product assets, templates, workflows, integrations, prior deployments, and validated technical implementations.

For each relevant candidate, determine REUSE, ADAPT, COMPOSE, or REDESIGN. If REDESIGN is selected, state the material reason.

**Quality Gate:** Build from scratch without a documented reuse evaluation is nonconforming.

### 3.3 Phase 2: Build

Objective: Construct the product according to approved requirements and applicable doctrine.

Requirements include, as applicable:

- composable and reusable component architecture;
- explicit frontend/backend/data contracts;
- backend mediation for sensitive operations;
- no secret values in client code or public artifacts;
- Supabase RLS and authorization appropriate to the access model;
- input validation at system boundaries;
- entity voice/brand compliance;
- accessible semantic structure;
- controlled external integrations;
- preservation of proven architecture unless change is justified.

Outputs: working build, component documentation, integration configuration, dependency map, and reuse decision record.

### 3.4 Phase 3: Test

Objective: Verify functional behavior, user-visible behavior, security boundaries, integration behavior, accessibility targets, and first-human-contact quality.

For browser-renderable products, live preview is mandatory before completion can be claimed. Testing shall include the applicable subset of:

- functional golden path and error paths;
- responsive visual verification;
- console/network/server-log review;
- accessibility checks;
- secret and credential exposure scan;
- input and output boundary validation;
- authorization/RLS verification;
- injection and XSS controls;
- entity/publication firewall review;
- integration and rollback tests.

**Quality Gate:** Material failures return to Build for correction and retest.

### 3.5 Phase 4: Package

Objective: Prepare the validated product and its evidence for governed promotion and deployment.

Required packaging includes as applicable:

- canonical source/artifact placement;
- version and hash information;
- registry records;
- dependency and integration documentation;
- provenance and source references;
- distribution/deployment manifest;
- reusable-pattern candidate identification.

Supabase registry records shall reference canonical GitHub/object-storage artifacts rather than substitute for them where D22 identifies another canonical source.

### 3.6 Phase 5: Promote

Objective: move validated candidate content to its authorized lifecycle state under D05 and controlling Level 0 authority.

Promotion evidence shall identify the exact artifact/version, canonical source, integrity evidence, approving authority, effective time, and applicable registry/Tribunal references.

No AI model, agent, GitHub merge, Supabase write, Tribunal receipt, or deployment self-promotes content absent controlling authority.

### 3.7 Phase 6: Deploy

Objective: deploy the promoted product to its target execution surface and verify actual runtime behavior.

Production verification shall include the applicable golden-path, security, network, integration, accessibility, monitoring, and rollback checks. Deployment state is execution evidence, not doctrine authority.

### 3.8 Phase 7: Capture Reusable Pattern

After successful implementation and verification, determine what should be retained as reusable enterprise capability.

Capture, as applicable:

- architecture pattern;
- component or module;
- schema or migration pattern;
- GitHub workflow;
- Supabase integration pattern;
- environment-variable requirements without values;
- Vault/secret injection pattern without values;
- API/MCP/plugin/connector configuration pattern;
- deployment configuration;
- test and validation procedure;
- rollback procedure;
- operational lessons and known limits.

Register the reusable capability and its canonical source so future work can discover it before redesign.

---

## 4. Persistence Routing for D20 Artifacts

D20 delegates canonical-source and runtime-distribution decisions to D22. The controlling operating shorthand is:

> **GitHub stores versioned artifacts. Supabase stores structured state and registries. Tribunal stores decision and execution evidence. Object storage stores large/binary assets. Vault stores secret values. Each governed object has one canonical home and governed references to the others.**

Incoming material shall follow:

`INGEST -> CLASSIFY -> AUTHORITY/LANE CHECK -> DUPLICATE/REUSE CHECK -> CANONICAL DESTINATION -> REGISTER -> LINK SOURCE/HASH -> TRIBUNAL RECEIPT WHEN GOVERNANCE-SIGNIFICANT`

Agents and models shall not independently invent a persistence destination when an applicable routing rule exists.

---

## 5. Testing Depth by Product Type

| Product Type | Functional | Visual | Console/Network | Accessibility | Cybersecurity | Entity Firewall | Live Preview |
|---|---|---|---|---|---|---|---|
| Web App | Full | Full | Full | Full | Full | Full | Required |
| Embedded Widget | Full | Full in host context | Full | Full | Full | Full | Required |
| Standalone HTML | Full | Full | Console | Full | Secrets + XSS | Full | Required |
| Dashboard | Full | Full | Full | Full | Full + authorization/RLS | Full | Required |
| Landing Page | Golden path | Full | Network | Full | Secrets | Full | Required |
| API Endpoint | Full | N/A | Server logs | N/A | Full | Full | N/A |
| Backend Script | Unit/integration | N/A | Logs | N/A | Secrets + injection | Full | N/A |
| Packaged Media | Manifest | Brand QA | N/A | Metadata/alt support | Metadata scan | Full | If web-renderable |
| AI/Agent Module | Full contract | Applicable UI | Full | Applicable UI | Full authority/tool boundary review | Full | If web-renderable |

---

## 6. Cybersecurity Quick Reference

1. No secret values in client code, prompts, doctrine, GitHub artifacts, Tribunal receipts, or ordinary Supabase content.
2. Validate user and machine inputs at boundaries.
3. Sanitize rendered content against injection and XSS.
4. Parameterize database queries.
5. Apply restrictive CORS and authentication where applicable.
6. Use approved server-side mediation for privileged operations.
7. Use HTTPS for production network endpoints.
8. Scan governed artifacts for credential patterns before publication or promotion.
9. Use only public/publishable client credentials where explicitly supported; privileged keys remain server-side or in approved secret stores.
10. Validate uploaded file type, size, content, ownership, and destination before ingestion.

Material secret exposure or unauthorized privileged access is a hard stop.

---

## 7. Tier and Promotion Authority

DCS Level 0 retains final promotion authority for doctrine and other authority-bearing enterprise artifacts unless a later controlling directive explicitly delegates that authority.

AI models and agents may research, draft, compare, test, validate, and recommend within authorized scope. They do not acquire promotion authority merely through access to GitHub, Supabase, Tribunal, local files, deployment systems, or orchestration tools.

---

## 8. Trigger Mechanism

D20 activates when DCSE is designing, assembling, materially changing, testing, packaging, promoting, deploying, or capturing reusable capability for a product/system.

The operative sequence is:

`INTAKE -> SEARCH PROVEN SOLUTIONS -> REUSE/ADAPT/COMPOSE/REDESIGN DECISION -> BUILD -> TEST -> PACKAGE -> PROMOTE -> DEPLOY -> CAPTURE REUSABLE PATTERN`

When only a bounded phase is requested, execute only that phase plus required upstream authority/evidence checks.

---

## 9. Related Doctrine

- D03 AI Orchestration: model/agent orchestration boundaries.
- D04 Command Post Communications: communications and Tribunal operational routing.
- D05 Baseline Promotion: promotion and baseline controls.
- D06 File System: physical/local file classification and routing.
- D07 Campaign Governance: distribution/publication controls.
- D09 Brand Identity: entity brand controls.
- D11 HTML/Wix/App: web/app implementation standards.
- D16 DDNA Governance: structured/provenanced enterprise knowledge controls.
- D17 DART Core: adversarial analysis when applicable.
- D18 Media Production Pipeline: media sub-pipeline.
- D19 Visual Creation Pipeline: visual sub-pipeline.
- D21 Doctrine Runtime Engine: runtime validation and execution controls.
- D22 Source Authority and Runtime Distribution: controlling canonical-source, registry, synchronization, drift, and persistence-routing doctrine.

---

## 10. Error-Catch Protocol

If the operative D20 v7.2 file is missing, unreadable, or mismatched with its registered canonical reference:

1. Halt authority-sensitive D20 execution rather than infer missing rules.
2. Classify the condition as source-authority DRIFT under D22.
3. Preserve the conflicting sources and hashes.
4. Use the last verified promoted source until reconciliation is complete.
5. Record the reconciliation and validation evidence through the governed Tribunal/registry process.

---

## 11. v7.2 Promotion Record

The Reuse Before Redesign amendment and this v7.2 D20 consolidation were explicitly **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 on 2026-09-10**. No additional candidate approval gate applies to this exact promoted content. Administrative synchronization across GitHub, Supabase registries, Tribunal evidence, DDNA references, and the v7.2 master/index does not constitute a new approval decision.