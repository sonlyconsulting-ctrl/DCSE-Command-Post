# DCSE MASTER PROFILE v7.2
## Three-Review Integrated Controller Candidate

**Artifact Class:** Enterprise Governance Controller Candidate  
**Controller Family:** DCSE Master Profile 7.2  
**Candidate Revision:** 7.2.0-CANDIDATE-R3  
**Authority:** DCS  
**Current Authority State:** CANDIDATE  
**Readiness State:** NOT_READY  
**Deployment State:** STAGED  
**Evolution State:** CONTROLLED  
**Architecture Principle:** Structure Precedes Scale  
**Execution Model:** Goal-State Orchestration  
**Integration Basis:** R2 candidate plus independent Claude Code review (2026-08-08) incorporating live operational DB cross-reference, lane topology DCS decisions, D17 identity resolution, and D01-D22 compiled section completion  
**Base Candidate Commit:** `d2d87789dbed8c31d12ada671019f6761a35762e` (R2 base)  
**R3 Correction Branch:** `claude/governance-poller-validation-ytqwz2`  
**R3 Correction Timestamp:** 2026-08-08  
**Important:** This artifact is not yet the operative controller. R3 corrects CRITICAL finding F-01 (lane registry) and blocks F-02 through F-08 identified in the Claude Code independent review. One review (Antigravity) remains before four-review convergence and DCS operative designation. Readiness state is NOT_READY pending resolution of open DCS lane decisions documented in Section 11.

---

# 0. CONTROLLING PURPOSE

DCSE Master Profile v7.2 SHALL establish one authoritative enterprise governance controller while preserving source doctrine provenance, lane isolation, runtime executability, independent validation, and controlled evolution.

The v7.2 architecture SHALL:

1. compile the governing substance of D01 through D22 into one canonical controller architecture;
2. preserve D01 through D22 as source governance artifacts;
3. keep constitutional/controller provisions under `MP-*` identifiers rather than inventing a D00 doctrine without source authority;
4. minimize runtime context by generating authorized context packets rather than transmitting the entire governance artifact;
5. preserve D21 runtime-engine behavior and D22 source/distribution authority within the compiled controller;
6. maintain strict PS and PPR isolation;
7. preserve evidence, communication-state, promotion, rollback, database, artifact-security, capability-routing, and source-mode controls from the governing v7.1 corpus unless expressly superseded;
8. support official operative authority without implying immutable finality;
9. prevent silent governance mutation;
10. make the controller mechanically auditable.

---

# 1. CONTROLLER ARCHITECTURE

## 1.1 Canonical Model

```text
AUTHORITATIVE GOVERNANCE SOURCES
        |
        +-- Current controlling Master Profile
        +-- D01 through D22
        +-- Ratified amendments / express DCS directives
        |
        v
GOVERNANCE COMPILER
        |
        +-- source inventory
        +-- authority resolution
        +-- normative extraction
        +-- duplicate analysis
        +-- conflict ledger
        +-- stable addressing
        +-- provenance hashes
        +-- lint / acceptance tests
        |
        v
DCSE MASTER PROFILE v7.2
CANONICAL CONTROLLER ARTIFACT
        |
        +-- Layer 1: Controller Header
        +-- Layer 2: Core Runtime Constitution
        +-- Layer 3: D01-D22 Compiled Sections
        +-- Layer 4: Machine Control Layer
        +-- Layer 5: Provenance / Audit Layer
        |
        v
CONTEXT COMPILER
        |
        v
AUTHORIZED RUNTIME CONTEXT PACKET
        |
        v
WORKER / RUNTIME
        |
        v
EVIDENCE -> VALIDATION -> STATE RECONCILIATION -> GOAL STATE
```

## 1.2 Canonical Controller Artifact vs Runtime Context Packet

**Canonical Controller Artifact** means the complete compiled governance authority.

**Runtime Context Packet** means a task-specific projection of the canonical controller.

**Controller Header** means the mandatory minimal subset included in every authorized runtime packet.

A runtime does not automatically receive the entire canonical controller. It SHALL receive the smallest sufficient authorized projection that preserves every mandatory rule dependency, Stop-Gate, lane restriction, authority reference, and evidence requirement applicable to the task.

---

# 2. GOVERNANCE SOURCE MODEL

## 2.1 Doctrine Set

The governed source doctrine set is:

```text
D01 through D22
```

There is no new D00 doctrine in this candidate.

Constitutional and controller-level rules are represented by `MP-*` sections.

## 2.2 D22 Title

D22 SHALL be identified as:

```text
D22. Source Authority and Runtime Distribution
```

## 2.3 Source Status vs Compiled Authority

Source doctrine lifecycle status and compiled-controller authority SHALL remain distinct.

Example:

```json
{
  "doctrine": "D03",
  "source_status": "CANDIDATE",
  "compiled_section": "#d03",
  "compiled_status": "ACTIVE_IF_AUTHORIZED",
  "authority_inherited_from": "DCSE_MASTER_PROFILE_7.2"
}
```

A source doctrine SHALL NOT become OPERATIVE merely because its content is compiled.

The compilation process SHALL preserve the source status that existed before compilation and SHALL record the authority basis for every compiled normative rule.

---

# 3. V7.1 TO V7.2 STATUS MIGRATION

Existing v7.1 source states SHALL NOT be silently upgraded.

Default migration treatment:

| v7.1 source state | v7.2 source treatment | Automatic normative promotion? |
|---|---|---|
| ACTIVE_RATIFIED | RETAINED_ACTIVE | No additional promotion required for already controlling substance |
| CANDIDATE | RETAINED_CANDIDATE | No |
| Pending approval | RETAINED_PENDING | No |
| SUPERSEDED / ARCHIVED | RETAINED_HISTORICAL | No |

Where a rule from a candidate or pending source is already made controlling by the current Master Profile or an express DCS directive, the compiler SHALL record that separate authority basis.

No lifecycle mapping alone creates new authority.

---

# 4. FOUR-DIMENSION STATE MODEL

The v7.2 controller SHALL use independent state dimensions.

## 4.1 Readiness

Recommended values:

```text
NOT_READY
READY_WITH_FINDINGS
READY
```

Readiness describes whether the artifact satisfies its build and validation criteria.

## 4.2 Authority

```text
DRAFT
CANDIDATE
OPERATIVE
SUPERSEDED
ARCHIVED
```

`OPERATIVE` means the artifact is the current official controlling framework.

## 4.3 Deployment

```text
STAGED
SYNCHRONIZING
SYNCHRONIZED
DEGRADED
ROLLED_BACK
```

Deployment describes propagation to required control surfaces.

## 4.4 Evolution

```text
CONTROLLED
FROZEN
```

The normal v7.2 posture is:

```text
Authority: OPERATIVE
Evolution: CONTROLLED
```

The phrase **Work in Progress** SHALL NOT be used as the primary state descriptor for an operative controller.

## 4.5 Change Classification

Change semantics SHALL be independent from authority state.

```text
Change Type:
  CLARIFICATION
  CORRECTION
  DOCTRINE_CHANGE
  ARCHITECTURE_CHANGE

Compatibility:
  NON_BREAKING
  BREAKING

Release Class:
  PATCH
  MINOR
  MAJOR
```

`OPERATIVE-PATCH` is not a lifecycle state.

---

# 5. ATOMIC AUTHORITY TRANSITION

Exactly one principal Master Profile version SHALL be the current enterprise controller except during an explicitly authorized migration condition.

An operative designation SHALL identify:

- prior controller version;
- new controller version;
- exact new controller hash;
- DCS authorization;
- effective timestamp;
- mandatory runtime activation surfaces.

At the effective transition:

```text
new controller  -> OPERATIVE
prior controller -> SUPERSEDED
```

The authority changes constitute one logical governance transaction.

Machine form:

```json
{
  "authority_transition": {
    "from": "7.1",
    "to": "7.2.0",
    "controller_hash": "SHA256",
    "effective_at": "ISO-8601-TIMESTAMP",
    "authorized_by": "DCS",
    "transaction_state": "COMMITTED"
  }
}
```

No runtime may infer controlling authority solely from the highest version number.

---

# 6. MINIMUM RUNTIME ACTIVATION

Authority declaration and infrastructure closeout are distinct, but an OPERATIVE controller SHALL be available on every control surface designated as mandatory for runtime enforcement.

The build SHALL derive the exact mandatory runtime surfaces from the actual v7.1 architecture.

At minimum, the model distinguishes:

```text
GitHub canonical source / authority record
Supabase control-plane state
Runtime controller activation surface(s)
Tribunal / archival evidence surface
```

Tribunal or archival synchronization may remain pending without automatically nullifying operative authority.

A missing mandatory runtime enforcement surface SHALL block the effective authority transition.

See Section 31 (Mandatory Runtime Surfaces) for the enumerated surface set grounded in live operational data.

---

# 7. FIVE CONTROLLER LAYERS

## Layer 1. Controller Header

Always-loaded high-value controls:

- controller identity and exact version;
- controller hash;
- authority state;
- DCS authority;
- governing hierarchy;
- lane firewall;
- Stop-Gate behavior;
- reasoning-state discipline;
- evidence-over-narrative rule;
- runtime context compilation requirements.

## Layer 2. Core Runtime Constitution

Candidate sections:

```text
MP-00 Controller Metadata
MP-01 Authority and Precedence
MP-02 Identity and Operating Posture
MP-03 Goal-State Execution Authority
MP-04 Runtime Orchestration
MP-05 Evidence and Verification
MP-06 Lane Isolation
MP-07 Stop-Gates
MP-08 Security and Privacy
MP-09 State, Promotion, and Authority Transition
MP-10 Change Control
MP-11 Completion, Rollback, and Closeout
MP-12 Runtime Distribution and Drift Control
```

## Layer 3. D01-D22 Compiled Sections

Each source doctrine retains its identity, source status, provenance, and internal addressing. See Section 17 (D01-D22 Compiled Sections) for the full enumeration.

## Layer 4. Machine Control Layer

Contains:

- doctrine registry;
- lane registry;
- rule registry;
- Stop-Gate registry;
- protected-module registry;
- artifact-security classes;
- source modes;
- capability-routing metadata;
- communication-state model;
- context packet schema;
- receipt schema;
- state-transition records.

## Layer 5. Provenance / Audit Layer

Contains:

- immutable source hashes;
- compilation manifest;
- many-to-many rule provenance;
- conflict ledger;
- supersession map;
- rule retirement map;
- compiler version;
- lint results;
- acceptance-test results;
- rollback metadata.

---

# 8. AUTHORITY AND CONFLICT RESOLUTION

Semantic deduplication SHALL NOT resolve conflicting normative rules merely by selecting apparently stronger language.

Every normative conflict SHALL be:

1. identified;
2. entered in the conflict ledger;
3. resolved under the controlling authority hierarchy; or
4. expressly dispositioned by DCS when the existing hierarchy is insufficient.

Conflict ledger example:

```json
{
  "conflict_id": "GC-001",
  "rules": ["D03§04.2", "D05§02.1"],
  "classification": "NORMATIVE_CONFLICT",
  "disposition": "RESOLVED",
  "resolution_authority": "MP§01.3",
  "replacement_rule": "MP§04.7"
}
```

Goal-state authorization SHALL NOT be interpreted as authority to silently rewrite constitutional rules.

Routine implementation may continue under approved authority.

A governance conflict that changes sovereign authority, lane boundaries, mandatory protections, or constitutional meaning requires explicit governance disposition.

---

# 9. STABLE RULE ADDRESSING

Human citation grammar:

```text
MP§05.4
D03§04.2
D03§07.3(a)
```

Machine identifier grammar:

```text
MP-05.4
D03-04.2
D03-07.3-a
```

Relationship:

```json
{
  "rule_id": "D03-04.2",
  "citation": "D03§04.2"
}
```

Rule identifiers are immutable identifiers.

A repealed, superseded, merged, or deprecated rule identifier SHALL remain permanently reserved and SHALL NOT be reused for an unrelated rule.

Replacement relationships SHALL be recorded explicitly.

---

# 10. MODAL LANGUAGE

Normative language SHALL be normalized:

```text
SHALL      mandatory
SHALL NOT  prohibited
MAY        permitted
SHOULD     rebuttable/default expectation
SHOULD NOT rebuttable disfavor
```

The governance linter SHALL flag ambiguous mandatory provisions written only as recommendation language.

---

# 11. LANE REGISTRY

## 11.1 R3 Correction Notice

**R3 CRITICAL CORRECTION — Finding F-01:** The R2 candidate lane registry did not include or route the following lanes that carry active tasks in the live operational database (`dcse_cp.agent_tasks`, queried 2026-08-08): SYSTEM (54 tasks), TSL (11 tasks), TRIBUNAL (2 tasks), DDNA (1 task). RAG has zero tasks but is used as a routing label. This omission was a CRITICAL finding because the governance registry diverged from runtime reality without disposition. R3 applies the DCS lane topology decision recorded below (2026-08-08).

## 11.2 DCS Lane Topology Decision (2026-08-08)

**DCS ruling:** DCSE is the enterprise operational infrastructure lane. SC and SS are the product/service/content enterprise lanes. All routing labels that do not name a distinct enterprise lane are absorbed by the appropriate enterprise lane based on function.

## 11.3 Enterprise Lane Registry

```json
{
  "lanes": {
    "DCSE": {
      "type": "enterprise_operational_infrastructure",
      "description": "Operational governance, command infrastructure, DDNA, AI orchestration, runtime systems, poller, tribunal workflow",
      "absorbs_routing_labels": ["SYSTEM", "TRIBUNAL", "DDNA", "RAG", "TSL", "INFRA/TECH", "TI"],
      "task_count_2026_08_08": 20,
      "routing_label_task_count_2026_08_08": {
        "SYSTEM": 54,
        "TSL": 11,
        "TRIBUNAL": 2,
        "DDNA": 1,
        "RAG": 0
      }
    },
    "SC": {
      "type": "enterprise_product_service_content",
      "description": "Sonly Consulting product and service delivery, client-facing builds, campaign assets",
      "task_count_2026_08_08": 3
    },
    "SS": {
      "type": "enterprise_product_service_content",
      "description": "Smoove Spots service and content delivery, storytelling, media, culture-facing brand",
      "task_count_2026_08_08": 11
    },
    "PS": {
      "type": "protected_litigation",
      "classification": "CONFIDENTIAL",
      "cross_lane_export": false,
      "dcs_load_required": true
    },
    "PPR": {
      "type": "protected_private_research",
      "classification": "PROTECTED",
      "cross_lane_export": false,
      "dcs_load_required": true
    }
  }
}
```

## 11.4 Routing Label Dispositions

The following labels appear in `dcse_cp.agent_tasks` but are NOT enterprise lane identifiers in this registry. Each has an explicit routing disposition:

| Routing Label | Live Task Count | Disposition | Routes To | Note |
|---|---|---|---|---|
| SYSTEM | 54 | Internal operational label | DCSE | System-level infrastructure tasks; not a separate enterprise lane |
| TSL | 11 | Demoted from R2 draft; now dispositioned | DCSE | TSL operational tasks route to DCSE infrastructure lane |
| TRIBUNAL | 2 | Governance operational subdomain | DCSE | Tribunal workflow is DCSE operational function |
| DDNA | 1 | Data governance subdomain | DCSE | DDNA extraction is DCSE operational function |
| RAG | 0 | Operational infrastructure label | DCSE | Routes to DCSE; retain label, zero current tasks |
| INFRA/TECH | 0 | Consolidated | DCSE | Renamed/superseded by DCSE operational lane |

## 11.5 DCS Identity Classification

**DCS** is the enterprise authority identity (the sovereign), not a dispatch lane. DCS tasks represent decisions requiring DCS-level resolution and SHALL be tracked as DCS decisions in the governance decision queue, not as worker dispatch tasks in `dcse_cp.agent_tasks`. DCS is removed from the dispatch lane registry.

## 11.6 TI Classification

**TI** (Training/Instruction) appears in the R2 lane registry with no v7.1 source grounding found. Under the R3 DCS topology decision, TI is treated as an operational training subdomain routing to DCSE until a source-grounded TI lane definition is produced by DCS. If TI requires separate enterprise lane status, a distinct source-grounded designation is required before the next review.

## 11.7 MP72-003 Alignment

Acceptance test MP72-003 is updated in Section 34 to validate against the R3 DCS-designated lane set:

```text
Enterprise lanes: DCSE, SC, SS, PS, PPR
Routing label dispositions: documented in Section 11.4
DCS identity: not a dispatch lane
```

---

# 12. PS AND PPR FIREWALL

Enterprise-shared runtime context SHALL NOT contain substantive PS case facts, case identifiers, evidence details, damages, witnesses, litigation dates, comparator details, or DART-PS substantive facts.

The shared controller SHALL contain only the abstract firewall and routing rules required to protect PS.

PPR SHALL remain protected and isolated from unauthorized public, product, or commercial use.

Machine representation:

```json
{
  "protected_modules": {
    "PS-DART": {
      "lane": "PS",
      "classification": "CONFIDENTIAL",
      "default_load": false,
      "cross_lane_export": false,
      "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
    },
    "PPR": {
      "lane": "PPR",
      "classification": "PROTECTED",
      "default_load": false,
      "cross_lane_export": false,
      "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
    }
  }
}
```

PS-specific rules remain addressable within the architecture but may be emitted only into PS-authorized context packets.

---

# 13. D21 RUNTIME ENGINE RECONCILIATION

D21 remains a retained source doctrine.

Its operative runtime-engine responsibilities SHALL be compiled into the v7.2 controller rather than discarded.

The compiled runtime engine SHALL preserve, where supported by the governing source:

- doctrine routing;
- Doctrine Run Plan generation;
- DCL generation;
- capability validation;
- security controls;
- promotion guard;
- reconciliation;
- source-mode behavior;
- executability wrappers;
- artifact-security classification;
- runtime admission and Stop-Gates.

The v7.2 Context Compiler SHALL be the compiled implementation surface for D21 routing logic.

D21 source identity and provenance remain auditable even when its runtime behavior is represented by `MP-*` controller rules.

---

# 14. D22 SOURCE AUTHORITY AND RUNTIME DISTRIBUTION

D22 remains the source authority for canonical identity, runtime distribution, drift detection, and reconciliation unless expressly superseded.

The v7.2 controller SHALL record:

```json
{
  "distribution": {
    "canonical_controller": "repository/path",
    "controller_version": "7.2.0",
    "controller_hash": "SHA256",
    "compiler_version": "VERSION",
    "effective_at": "ISO-8601-TIMESTAMP"
  }
}
```

Every mandatory runtime surface SHALL be able to report the controller version and hash it is enforcing.

A mismatch SHALL create a drift event.

Drift SHALL not be silently reconciled by selecting the newest file.

The canonical D22 authority procedure SHALL determine reconciliation.

---

# 15. D04 COMMUNICATION STATES

The v7.2 deployment model SHALL NOT collapse D04 communication states.

The following communication states remain separately observable where applicable:

```text
CREATED
STORED
DISPATCHED
DELIVERED
CONSUMED
ACKNOWLEDGED
ACCEPTED
PROMOTED
```

These states describe communication/delivery progression.

They are independent from:

- readiness;
- controller authority;
- deployment synchronization.

---

# 16. D05 PROMOTION, BASELINE, AND ROLLBACK

The v7.2 state model replaces overloaded single-state promotion semantics but does not silently delete D05 promotion, baseline, recovery, or rollback controls.

During compilation, D05 SHALL be mapped into:

- readiness validation;
- authority designation;
- deployment synchronization;
- rollback;
- recovery;
- evidence requirements.

Any D05 rule that conflicts with the new architecture SHALL enter the conflict ledger rather than being silently discarded.

---

# 17. D01-D22 COMPILED SECTIONS

**R3 Correction — Finding F-05:** R2 contained compiled sections only for D04, D05, D15, D21, and D22. Thirteen additional doctrines (D01-D03, D06-D14, D16-D20) had no compiled section, causing acceptance test MP72-001 to fail. R3 adds compiled sections for all remaining doctrines. D13 and D14 are PS-protected and receive firewall stubs only. D15 is correctly labeled (not D17). D17 receives a full compiled section as the DART Universal Methodology (correcting F-02 identity error in R2).

## D01 — Forward Thinking

**Source:** `governance/v7.1/source/doctrines/D01_Forward_Thinking.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- All DCSE communication, reasoning, and content generation SHALL prioritize forward-looking clarity over negative restriction (Executive Penthouse Philosophy).
- Every prohibited action SHALL be accompanied by the permitted path forward.
- Words "impossible" or "restricted" SHALL be used only when a hard security boundary requires direct negative constraint.
- A reasoning step that reaches a stop condition SHALL immediately pivot to the next authorized state and path.
- Unresolved blocking conditions SHALL be escalated rather than left as terminal negatives.

## D02 — Forward and Backward Chaining

**Source:** `governance/v7.1/source/doctrines/D02_Forward_Backward_Chaining.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Non-trivial work SHALL use both forward and backward chaining together (see Section 22 for the goal-state orchestration model that applies these protocols).
- Forward chaining: derive outputs step-by-step from validated antecedent rules and harvested facts. Each derivation step SHALL log the active rule ID that justified it.
- Backward chaining: from the target goal state, enumerate acceptance criteria, required evidence, and required actions to expose the current gap.
- No derivation step SHALL be presented as complete without tracing to a named source or rule.
- Quality gates SHALL be applied at both production (forward) and validation (backward) phases.

## D03 — AI Orchestration and Prompt Wrappers

**Source:** `governance/v7.1/source/doctrines/D03_AI_Orchestration.md`  
**Source Version:** v7.0  
**Source Status:** CANDIDATE PENDING DCS LEVEL 0 PROMOTION  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Work SHALL be routed to models based on documented capability assignment; ad-hoc model selection without capability basis is prohibited.
- Model delegation matrix: Claude (CTO function — architecture, narrative, governance reconciliation), Codex (bounded repository implementation, database work under approved task scope), Qwen Coder (rapid validation loop, syntax/schema checks), Gemini (drive-state diagnostics, visual checks), ChatGPT (daemon management, packager scripts). No assignment is permanent; routing follows the operative task and scope.
- Minimum Effective Context (MEC) SHALL be enforced: a model SHALL receive only the governance packet authorized for its task, not the entire controller.
- STOPGATE SHALL trigger when a required doctrine resource is missing or unreadable.
- Codex has no self-authorization, secret-disclosure, or cross-lane expansion authority.
- No model may approve its own output, promote a persona, or bypass DCS authority.

## D04 — Communication States

Compiled in full at Section 15.

## D05 — Promotion, Baseline, and Rollback

Compiled in full at Section 16.

## D06 — File System and Device Governance

**Source:** `governance/v7.1/source/doctrines/D06_File_System.md`  
**Source Version:** v7.0  
**Source Status:** CANDIDATE PENDING DCS LEVEL 0 PROMOTION  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE and PS Command Center  

**Core compiled rules:**
- All active controlled files SHALL reside in the designated 14-directory hub layout (00_Authority through 13_Archive). Cross-directory contamination is prohibited.
- The PS Spoke (DS Litigation) SHALL remain firewalled from the cloud-synced Hub. Files referencing active Pro Se litigation SHALL be quarantined and routed offline immediately upon detection.
- Historical resume files under PTGC All Things subfolders are evidentiary material for active litigation and SHALL NOT be subject to bulk automated cleanup pipelines.
- Automated ingestion scripts SHALL classify incoming files before routing; unclassified files SHALL not be auto-promoted.
- Cleanup actions SHALL proceed through the seven-stage File Governance Pipeline and require Level 0 approval before execution.
- Device governance: sensitive data and git authority actions SHALL NOT occur on non-secure staging nodes. The Device Governance Matrix governs per-node allowed commands and restrictions.

## D07 — Campaign Governance

**Source:** `governance/v7.1/source/doctrines/D07_Campaign_Governance.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** SC, SS, DCS  

**Core compiled rules:**
- Campaign files (websites, landing pages, email sequences, social media, video scripts, SEO/GEO/AEO assets) SHALL remain free of internal architectural documentation, database schemas, and private litigation facts.
- Em and en dashes SHALL NOT appear in web metadata, SEO descriptions, or structured data fields (causes indexing errors).
- Readability standards: public landing pages SHALL target Grade 6-8 reading level; social sequences SHALL maintain conversational clarity; email pipelines SHALL be calibrated to audience persona tone profiles.
- Search optimization (SEO/GEO/AEO) standards SHALL be applied to all public digital assets before release.
- SC and SS campaign materials SHALL remain entity-firewalled; SC business-focused tone SHALL NOT bleed into SS storytelling or vice versa.

## D08 — Voice and Tone

**Source:** `governance/v7.1/source/doctrines/D08_Voice_Tone.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Each enterprise lane SHALL maintain its distinct voice register without blending.
  - DCSE: precise, clinical, structure-forward, non-self-referential.
  - DCS: direct, measured, senior, selective; highlights enterprise systems and consulting outcomes.
  - SC: approachable executive authority, framework-driven, implementation-focused.
  - SS: narrative-driven, soulful, reflective, metaphor-rich.
  - PS: formal federal court register, objective, evidence-focused, highly detailed.
- Zero drift SHALL be enforced: any asset that blends lane voices requires correction before release.
- ElevenLabs voiceover configuration SHALL follow lane-specific pronunciation and cadence rules from the operative D08 source.
- The "Morgan Freeman meets Michael B. Jordan" archetype applies to the DCS voice register: slow-paced authority with modern relevance.

## D09 — Brand Identity

**Source:** `governance/v7.1/source/doctrines/D09_Brand_Identity.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Controlled brand terms (DCS, DCSE, Sonly Consulting, Smoove Spots, Critical Thinkers Journey/CTJ, GET YOUR THINK ON!™/GYTO) SHALL remain uniform across all public systems. Variations require DCS authorization.
- GYTO SHALL be restricted to internal use and SHALL be automatically suppressed from public-facing assets unless explicitly authorized by DCS.
- Brand color palette (Gold, Deep Navy, Emerald, Silver, Earth, specific hex anchors) SHALL be applied consistently across all lane assets. Deviations require DCS approval.
- Composition constraints for generative art models are governed by D09 source and the D19 Visual Creation Pipeline methodology.
- Public marks (GET YOUR THINK ON!™) carry trademark parameters governed by the operative D09 source.

## D10 — Persona Assets

**Source:** `governance/v7.1/source/doctrines/D10_Persona_Assets.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** SC, SS  

**Core compiled rules:**
- All SC and SS public assets SHALL be calibrated against the 17 defined target personas from the operative D10 source.
- Tone density, motivational framing, and layout complexity SHALL match the target persona's documented profile.
- No persona data SHALL appear in PS lane assets or litigation filings.
- Persona definitions are DCS-controlled; new personas require DCS authorization before use in production assets.

## D11 — HTML, Wix, and App Governance

**Source:** `governance/v7.1/source/doctrines/D11_HTML_Wix_App.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Every interactive HTML module SHALL maintain an explicit, serializable state object with defined states (draft, review, confirmed, rejected, conflict, blocked, archived). No silenced failures.
- Browser-facing code SHALL use only public-safe anonymous keys. Secret provider keys (Anthropic, Google, OpenAI, Supabase service-role) SHALL never appear in browser code.
- Iframe sandboxing and postMessage dynamic sizing SHALL be enforced for all embedded widgets.
- CSS styling SHALL use the token stack defined in D11 source; brand color tokens must not be hardcoded.
- Responsive layout standards (mobile, tablet, desktop breakpoints) SHALL be enforced before release.
- Application smoke tests SHALL pass before deployment (see D20 Product Assembly methodology for the full gate).

## D12 — Video and Media

**Source:** `governance/v7.1/source/doctrines/D12_Video_Media.md`  
**Source Version:** v6.9 Update Candidate  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Every automated or supervised video build SHALL initiate with a Video Build Declaration specifying target entity, content series, audience, public/internal status, assigned AI models, and agentic authorization level.
- Entity isolation is enforced: SC content = executive warmth and business clarity; SS content = soulful cinematic storytelling; TI = instructional/procedural; PS = precise, document-grade, strictly offline.
- GYTO SHALL be suppressed from all public-facing video scripts, captions, thumbnails, and metadata unless explicitly authorized by DCS.
- Video production execution methodology is governed by D18 (Media Production Pipeline).
- Visual production methodology is governed by D19 (Visual Creation Pipeline).
- D12 remains the governance authority; D18 and D19 are its execution methodologies.

## D13 — DART Core (PS-PROTECTED)

**Source:** `governance/v7.1/source/doctrines/D13_DART_Core.md`  
**Source Status:** PS-PROTECTED  
**Compiled Status:** PS-LOCK — FIREWALL ONLY  
**Lane:** PS  

This section is a firewall stub. D13 substantive content SHALL NOT appear in enterprise-shared governance packets. D13 is accessible only in PS-authorized context packets when DCS PS mode is active.

```json
{
  "module": "D13",
  "classification": "PS-PROTECTED",
  "default_load": false,
  "cross_lane_export": false,
  "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
}
```

## D14 — DART PS Protected (PS-PROTECTED)

**Source:** `governance/v7.1/source/doctrines/D14_DART_PS_Protected.md`  
**Source Status:** PS-PROTECTED  
**Compiled Status:** PS-LOCK — FIREWALL ONLY  
**Lane:** PS  

This section is a firewall stub. D14 substantive content SHALL NOT appear in enterprise-shared governance packets. D14 is accessible only in PS-authorized context packets when DCS PS mode is active.

```json
{
  "module": "D14",
  "classification": "PS-PROTECTED",
  "default_load": false,
  "cross_lane_export": false,
  "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
}
```

## D15 — Database Administration and Security

**Source:** `governance/v7.1/source/doctrines/D15_Database_Admin.md`  
**Source Version:** (confirm from source)  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE/ALL  

**R3 Note:** R2 Section 17 was labeled "DATABASE GOVERNANCE" but referenced D15 controls without naming D15. Separately, the file `docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md` incorrectly used the D17 identifier for Supabase security implementation. D15 is the canonical source for database administration doctrine. The Supabase security file requires a separate doctrine number assigned by DCS.

**Core compiled rules** (from R2 Section 17, now correctly attributed to D15):
- Database changes SHALL preserve migration-controlled changes, RLS and access control, parameterized queries, least privilege, evidence of execution, rollback path, post-change verification, and security/performance review.
- The v7.2 controller SHALL NOT treat Supabase registration as equivalent to database governance compliance.
- The full Supabase security and automation doctrine (tables requiring RLS, SECURITY DEFINER standards, automation gates, promotion lifecycle) is governed by the Supabase doctrine pending its DCS identifier assignment (see Section 36 — Open DCS Items).

## D16 — DDNA Governance

**Source:** `governance/v7.1/source/doctrines/D16_DDNA_Governance.md`  
**Source Version:** v6.9  
**Source Status:** DCSE Authorized Pending Approval  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** ALL  

**Core compiled rules:**
- Every DCSE session, transcript, build log, or artifact is a source of structured signal. DDNA extraction SHALL capture all five signal layers: Sentiment, Logic, Design, Product, and Technical. No layer is optional.
- DDNA extraction SHALL follow the 12-step extraction sequence defined in the operative D16 source.
- DDNA outputs SHALL be routed to canonical save destinations by output type. Unsaved DDNA exhaust represents governance debt.
- Approval gates govern DDNA asset promotion; raw extracted signals are not automatically promoted to doctrine.
- DDNA outputs feed back into the doctrine and product registry through the feedback loop defined in D16.
- D16 governs what agents produce. D03 governs how agents behave. These are complementary and not overlapping.
- The DDNA lane is a DCSE operational subdomain per the R3 lane topology decision (Section 11). DDNA governance functions route under the DCSE enterprise lane.

## D17 — DART Universal Methodology

**Source:** `governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md`  
**Source Version:** v6.9  
**Source Status:** ACTIVE_RATIFIED  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE/ALL  
**DB Row:** `dcse_cp.governance_directives`, key `D17`, promotion_status: promoted  

**R3 Correction — Finding F-02:** R2 did not include a compiled section for D17 DART Universal Methodology despite D17 being promoted in `dcse_cp.governance_directives`. The file `docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md` was incorrectly labeled D17 — that file's subject (Supabase security) is a separate unnumbered doctrine pending DCS identifier assignment. Canonical D17 = DART Universal Assurance Methodology.

**Core compiled rules:**
- DART is a four-phase adversarial analysis framework applicable to any domain where a position must be defended, a claim substantiated, or a decision must survive scrutiny.
- Phases: **Discovery** (gather/classify/map all relevant evidence before forming any position) → **Attack** (stress-test every claim by actively looking for weaknesses and counterarguments) → **Rebuttal** (build pre-emptive defenses for every identified vulnerability) → **Trial** (final validation; output must survive presentation to its toughest audience).
- DART activates explicitly (user directive) or implicitly (task involves defending a position, evaluating credibility, adversarial preparation, or claim validation).
- On activation, the model SHALL announce: "DART Universal activated. Running Discovery > Attack > Rebuttal > Trial."
- Five universal quality gates: Source Tracing, Attack Survival, Consistency Check, Audience Calibration, Confidence Declaration. All five SHALL pass before delivery.
- All DART-processed outputs SHALL include the tag: "Processed under DART Universal Methodology — DCSE Proprietary."
- PS Escalation Gate: if DART processing encounters Pro Se litigation content, halt, announce escalation to DART PS-Applied (D13/D14), verify PS mode authorization, and stop if not authorized.
- Tier access: Tier 1 Sovereign — full DART Universal + D13/D14 on PS demand; Tier 2 Internal Collaborator — DART Universal only; Tier 3 External Product Build — methodology description (Section 2 of D17 source) only.

## D18 — Media Production Pipeline

**Source:** `governance/v7.1/source/doctrines/D18_Media_Production_Pipeline.md`  
**Source Version:** v6.9  
**Source Status:** ACTIVE_RATIFIED  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE/ALL  

**Core compiled rules:**
- D18 is the execution methodology for video, audio, motion graphics, and multimedia production. D12 (Video & Media) remains the governance authority.
- The four-phase production pipeline: Brief → Pre-Production → Production → Post-Production and QA.
- Every phase has defined inputs, outputs, quality gates, and model-duty assignments per the operative D18 source.
- QA gates SHALL be non-negotiable; no media deliverable is complete without QA gate passage.
- Entity isolation from D12 (SC, SS, PS, TI, DCSE voice registers) applies throughout all D18 pipeline phases.

## D19 — Visual Creation Pipeline

**Source:** `governance/v7.1/source/doctrines/D19_Visual_Creation_Pipeline.md`  
**Source Version:** v6.9  
**Source Status:** ACTIVE_RATIFIED  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE/ALL  

**Core compiled rules:**
- D19 is the consolidated execution methodology for image, graphic, and visual asset creation. Source governance for visual rules remains distributed across D12 (visual prompt standards), D09 (brand color palette), and D11 (CSS token implementation).
- Five-phase pipeline: Brief → Prompt Engineering → Generation → Brand QA → Format Delivery.
- Brief SHALL specify entity, target audience, intended channel, and required brand tokens before prompt engineering begins.
- Brand QA gate: all generated visuals SHALL pass color palette, typography, and brand-term compliance checks against the operative D09 palette before delivery.
- Generated images SHALL not be promoted to production assets without explicit Brand QA gate passage.

## D20 — Product Assembly Methodology

**Source:** `governance/v7.1/source/doctrines/D20_Product_Assembly_Methodology.md`  
**Source Version:** v7.0  
**Source Status:** CANDIDATE PENDING DCS LEVEL 0 PROMOTION  
**Compiled Status:** ACTIVE_IF_AUTHORIZED  
**Lane:** DCSE/ALL  

**Core compiled rules:**
- D20 is the consolidated execution methodology for the full product lifecycle. Source governance remains distributed across D05 (promotion gates), D06 (file routing), D11 (HTML/Wix standards), and D07 (campaign distribution).
- Six-phase pipeline: Intake → Build → Test → Package → Promote → Deploy.
- Test phase is non-negotiable: Live Preview Mandate (from D21 Section 6) and cybersecurity baseline SHALL both pass before packaging.
- No product may be promoted or deployed without a passing D20 Test gate and promotion gate evidence.
- Products are: web applications, Wix-embedded widgets, standalone HTML tools, dashboards, calculators, landing pages, API endpoints, packaged media, and branded content systems.

## D21 — Runtime Engine

Compiled in full at Section 13.

## D22 — Source Authority and Runtime Distribution

Compiled in full at Section 14.

---

# 18. CAPABILITY-BASED ASSIGNMENT

Capability-based model and runtime assignment SHALL be preserved.

The compiler SHALL retain source-grounded capability routing, reasoning-level controls, poller boundaries, and admission requirements.

Logical agent identity, runtime surface, host/runtime instance, and model backend SHALL remain distinct concepts.

No runtime SHALL be considered autonomously executable solely because it is registered.

---

# 19. ARTIFACT SECURITY CLASSES

The compiled controller SHALL preserve artifact-scoped security selection.

The D21 artifact classes SHALL remain available to the control plane, including:

```text
GOVERNANCE_DOCUMENT
PUBLIC_UI
INTERNAL_UI
BACKEND_SERVICE
DATABASE_CHANGE
LOCAL_SCRIPT
MEDIA_ASSET
COMMUNICATION
```

Additional classes require governed extension, not silent invention.

---

# 20. SOURCE MODES AND DEGRADED OPERATION

The v7.2 runtime engine SHALL preserve the source-mode behavior currently governed by D21, including:

```text
REGISTRY_PRIMARY
REPOSITORY_READ_ONLY
OFFLINE_VERIFIED
```

The compiler SHALL define what operations are permitted and prohibited in each mode based on source doctrine.

Unknown or unresolved source authority SHALL fail closed for governance mutation or promotion.

---

# 21. REASONING STATES

Required reasoning states:

```text
VERIFIED
LIKELY
UNKNOWN
ASSUMPTION
```

`ASSUMPTION` is an explicit v7.2 extension.

Legacy v7.1 artifacts using only VERIFIED / LIKELY / UNKNOWN remain valid.

An assumption SHALL be labeled and SHALL NOT silently become VERIFIED.

---

# 22. GOAL-STATE ORCHESTRATION

For non-trivial work, forward and backward chaining SHALL be used together.

Forward:

```text
Current State
-> Evidence
-> Authorized Actions
-> Intermediate State
-> Goal State
```

Backward:

```text
Goal State
-> Acceptance Criteria
-> Required Evidence
-> Required Actions
-> Current Gap
```

Once DCS approves the objective and boundaries, execution authority persists until:

1. goal state is achieved;
2. the objective materially changes;
3. execution would exceed authorized boundaries;
4. a legitimate Stop-Gate occurs;
5. a protected, irreversible, or sovereign decision requires DCS.

A worker discovering an in-scope defect SHALL normally:

```text
detect -> diagnose -> remediate -> test -> record -> continue
```

Independent validation remains separate from implementation authority.

---

# 23. CONTEXT COMPILER: FAIL-CLOSED

Context compilation SHALL fail closed.

Failure to resolve any of the following SHALL NOT be interpreted as absence of restriction:

- lane;
- controlling authority;
- mandatory rule dependency;
- Stop-Gate;
- protected module;
- security class;
- source mode;
- capability requirement.

A context packet SHALL preserve sufficient compilation identity to reconstruct the rules used at execution time.

Minimum retained metadata:

```json
{
  "controller_family": "7.2",
  "controller_version": "7.2.0",
  "controller_hash": "SHA256",
  "context_packet_id": "UUID",
  "compiled_at": "ISO-8601-TIMESTAMP",
  "compiler_version": "VERSION",
  "rule_set_hash": "SHA256",
  "lane": "LANE",
  "authority_refs": [],
  "stop_gates": []
}
```

Not every metadata field must be transmitted verbatim into a model prompt, but the control plane SHALL retain the complete compilation record.

---

# 24. PROVENANCE MODEL

Provenance SHALL support many-to-one and one-to-many compilation.

Example:

```json
{
  "rule_id": "MP-05.4",
  "sources": [
    {
      "artifact": "D03_AI_Orchestration.md",
      "source_hash": "SHA256",
      "source_rule": "D03§..."
    },
    {
      "artifact": "D05_Baseline_Promotion.md",
      "source_hash": "SHA256",
      "source_rule": "D05§..."
    }
  ],
  "compiled_hash": "SHA256"
}
```

The build SHALL produce immutable hashes for:

- every source artifact;
- the canonical compiled controller;
- machine manifest;
- rule registry;
- context compiler release;
- acceptance-test output.

---

# 25. RECEIPTS

Executor and validator SHALL be structurally distinct.

Validated receipt example:

```json
{
  "task_id": "TASK-001",
  "controller_version": "7.2.0",
  "controller_hash": "SHA256",
  "lane": "DCSE",
  "authority": ["MP§03.2"],
  "executor": {
    "agent": "AGENT_KEY",
    "runtime_surface": "RUNTIME",
    "runtime_instance": "INSTANCE"
  },
  "result": "COMPLETED",
  "evidence": [],
  "validator": {
    "agent": "VALIDATOR_KEY",
    "validation_result": "APPROVE"
  }
}
```

A pre-validation receipt MAY omit a validator only when its receipt type explicitly states `PRE_VALIDATION`.

No artifact SHALL be represented as independently validated with a null or anonymous validator.

---

# 26. ROLLBACK MODEL

Every operative transition SHALL have a rollback record before effective cutover.

Required rollback fields:

- prior operative controller version and hash;
- new controller version and hash;
- reason for transition;
- affected sources;
- rollback trigger conditions;
- rollback procedure;
- mandatory runtime surfaces;
- post-rollback verification;
- Supabase/GitHub/runtime reconciliation;
- Tribunal/evidence receipt where applicable.

Rollback SHALL restore the last known authorized controller, not merely the highest available version.

A failed deployment synchronization SHALL not silently change authority.

---

# 27. BACKWARD COMPATIBILITY

v7.1 receipts, DCLs, Doctrine Run Plans, promotion records, and evidence remain valid historical records under the controller version that created them.

In-flight work at the v7.2 effective transition SHALL follow one of two explicit policies:

```text
PINNED_COMPLETION
Complete under the controller hash recorded when the task was accepted.

MIGRATED_EXECUTION
Recompile the task under v7.2 and record the migration receipt.
```

The default SHALL be derived from source governance and risk classification during compilation.

No task may silently switch controller versions mid-execution.

---

# 28. GOVERNANCE LINTER

Severity taxonomy:

```text
INFO
WARNING
ERROR
CRITICAL
```

Gate behavior:

```text
CRITICAL -> authority/readiness gate blocked
ERROR    -> readiness blocked unless formally dispositioned
WARNING  -> allowed only with documented disposition
INFO     -> non-blocking
```

Required lint checks include:

- duplicate mandatory rules;
- conflicting mandatory rules;
- orphan references;
- missing D01-D22 sections;
- invalid Stop-Gate IDs;
- undefined lanes;
- PPR or PS firewall violations;
- deprecated-rule references;
- broken anchors;
- inconsistent human/machine rule IDs;
- unclassified normative rules;
- missing source hashes;
- missing provenance;
- unresolved conflict-ledger entries;
- version/hash mismatch;
- controller-state mismatch;
- ambiguous modal language;
- missing rollback data;
- missing mandatory-runtime activation evidence.

---

# 29. BUILD PIPELINE

Hard dependency sequence:

```text
1. Freeze source inventory and hashes
2. Resolve source authority/status
3. Extract normative rules
4. Classify rules and modal language
5. Detect duplicates
6. Detect normative conflicts
7. Resolve/disposition conflicts
8. Assign stable machine IDs and human citations
9. Build MP core
10. Compile D01-D22 sections
11. Build machine registries
12. Generate provenance and conflict ledger
13. Generate context compiler rules
14. Validate internal references and protected modules
15. Run governance lint
16. Run mechanical acceptance tests
17. Independent review
18. Produce readiness disposition
19. DCS authority designation
20. Verify mandatory runtime activation
21. Atomic authority transition
22. Synchronize remaining evidence/control surfaces
23. Closeout and reconciliation
```

Phases 5 and 6 MAY run in parallel after rule extraction.

Stable production IDs SHALL NOT be finalized until conflicts affecting identity have been resolved or dispositioned.

---

# 30. TOKEN / CONTEXT ECONOMY

Token economy SHALL be measurable without imposing an arbitrary fixed token number before source inventory.

The build SHALL record:

- Controller Header token count;
- minimum supported runtime context budget;
- reserved task/evidence budget;
- maximum allowed governance packet budget per supported runtime class;
- actual packet size for acceptance-test tasks.

Acceptance rule:

> The Controller Header and required task governance packet SHALL fit inside the smallest supported runtime context budget after reserving the approved task/evidence budget, without dropping mandatory rule dependencies.

Compression SHALL never remove a mandatory rule solely to meet a token target.

---

# 31. MANDATORY RUNTIME SURFACES

**R3 Correction — Finding F-06:** R2 described mandatory runtime surfaces abstractly in Section 6 but did not enumerate them from operational evidence. R3 enumerates surfaces from `dcse_cp.runtime_surface_registry` (queried 2026-08-08) and records the DCS designation required by MP72-030.

## 31.1 Enumerated Surfaces (Queried 2026-08-08)

| Surface | Family | Can Claim | Polling Mode | Enabled |
|---|---|---|---|---|
| claude_code_windows_cli | claude | YES | scheduled | YES |
| cli_windows_poller | claude | YES | scheduled | YES |
| codex_windows_cli | openai | YES | scheduled | YES |
| qwen_windows_cli | qwen | YES | scheduled | YES |
| chat_browser | claude | no | interactive | YES |
| controller_windows | dcse | no | controller | YES |
| desktop_app | claude | no | interactive | YES |
| remote_cloud_ccr | claude | no | interactive | YES |
| unspecified | legacy | no | legacy | YES |
| worker_v7 | dcse | no | legacy | YES |

## 31.2 Mandatory Surface Designation for MP72-030

**Claiming surfaces** (can_claim = YES): `claude_code_windows_cli`, `cli_windows_poller`, `codex_windows_cli`, `qwen_windows_cli` — these surfaces are designated **mandatory** for MP72-030 activation gate purposes. Each SHALL acknowledge the operative controller hash before effective cutover.

**Non-claiming surfaces** (can_claim = no): `chat_browser`, `controller_windows`, `desktop_app`, `remote_cloud_ccr`, `unspecified`, `worker_v7` — designated **activation-optional** for MP72-030; read-only acknowledgment is acceptable.

## 31.3 Poller Contract Grounding

**R3 Correction — Finding F-08:** The Windows scheduled poller operates under the `MP72_POLLER_SESSION_RUNTIME` governance directive (row present in `dcse_cp.governance_directives`, `status: promoted`). The R2 candidate contained no compiled section grounding the poller operational contract. R3 records:

```json
{
  "poller_contract": {
    "governing_directive": "MP72_POLLER_SESSION_RUNTIME",
    "directive_status": "promoted",
    "surfaces": ["claude_code_windows_cli", "cli_windows_poller"],
    "operational_rules": [
      "D1: check for existing lease before claiming (Atomic Single-Instance Lease)",
      "D2: log state transitions as they happen, not reconstructed (Heartbeat Separation)",
      "D3: task eligibility from policy table only, not hardcoded allowlist (Policy Routing)",
      "D4: failed/timed-out steps reported as failed, never silently upgraded (Provider Failure Handling)",
      "D5: check for terminal receipt before writing; no duplicate outcomes (Idempotency)",
      "D6: every state change written to receipt or DB row with timestamp (State Machine Transitions)"
    ],
    "rpc_contract": {
      "claim_agent_assignment": "always call with full 6-arg signature to avoid PostgreSQL overload ambiguity",
      "submit_agent_result": "always call with full 8-arg signature to avoid PostgreSQL overload ambiguity"
    }
  }
}
```

---

# 32. MECHANICAL ACCEPTANCE TESTS

The candidate SHALL not become readiness `READY` until the following tests pass or are formally dispositioned where allowed.

```text
MP72-001  D01-D22 inventory complete; no invented D00 dependency
          [R3: compiled sections present for D01-D22 in Section 17; D13/D14 as PS-lock stubs]

MP72-002  PPR lane present and protected
          [R3: PPR retained in Section 11.3]

MP72-003  Operative lane set validates: DCSE, SC, SS, PS, PPR (enterprise); routing labels
          dispositioned per Section 11.4; DCS is authority identity not dispatch lane
          [R3: UPDATED from R2 to reflect DCS lane topology decision 2026-08-08]
          [OPEN: TI disposition pending v7.1 source grounding — see Section 36]

MP72-004  TSL/FAMILY not silently promoted to enterprise lanes
          [R3: TSL dispositioned as DCSE routing label in Section 11.4; FAMILY not present]

MP72-005  No PS case-specific substantive content in enterprise-shared packet
          [R3: PS sections are firewall stubs only]

MP72-006  PS protected module default_load=false
          [R3: confirmed in Section 12]

MP72-007  PPR protected module default_load=false
          [R3: confirmed in Section 12]

MP72-008  D21 runtime responsibilities mapped
          [R3: Section 13]

MP72-009  D22 canonical/distribution/drift controls mapped
          [R3: Section 14]

MP72-010  D04 communication states preserved
          [R3: Section 15]

MP72-011  D05 promotion/rollback controls mapped
          [R3: Section 16]

MP72-012  D15 database-governance controls mapped
          [R3: Section 17, D15 entry, now correctly labeled]

MP72-013  capability-routing/poller boundaries mapped
          [R3: Section 18; poller contract grounded at Section 31.3]

MP72-014  artifact-security classes mapped
          [R3: Section 19]

MP72-015  source modes mapped
          [R3: Section 20]

MP72-016  source lifecycle migration table complete
          [R3: Section 3]

MP72-017  human and machine rule-ID grammar validates
          [R3: Section 9]

MP72-018  retired rule IDs cannot be reused
          [R3: Section 9, rule identifiers are immutable]

MP72-019  unresolved normative conflicts = 0 CRITICAL
          [OPEN: conflict ledger not yet executed; full lint pass required before READY]

MP72-020  every compiled normative rule has provenance
          [OPEN: provenance hashes not yet recorded; required before READY]

MP72-021  source hashes present for all compiled sources
          [OPEN: source hashes not yet recorded; required before READY]

MP72-022  context compiler fails closed on unknown lane
          [R3: Section 23]

MP72-023  context compiler fails closed on missing mandatory dependency
          [R3: Section 23]

MP72-024  context packet records controller/rule-set identity
          [R3: Section 23]

MP72-025  validated receipts identify executor and validator separately
          [R3: Section 25]

MP72-026  rollback package validates
          [OPEN: rollback record not yet produced; required before operative transition]

MP72-027  backward-compatibility policy validates
          [R3: Section 27]

MP72-028  readiness and authority states remain independent
          [R3: Section 4]

MP72-029  authority transition contains effective timestamp and exact hash
          [OPEN: not yet produced; required before operative transition]

MP72-030  mandatory runtime surfaces acknowledge operative hash before effective cutover
          [R3: surfaces enumerated at Section 31; claiming surfaces designated mandatory;
           acknowledgment not yet collected — gate remains open until OPERATIVE transition]

MP72-031  lint contains no CRITICAL finding
          [OPEN: lint pass not yet executed]

MP72-032  all ERROR findings resolved or formally dispositioned
          [OPEN: lint pass not yet executed; R3 corrects known CRITICAL/ERROR findings from
           independent review but full lint has not run]

MP72-033  controller header fits measured runtime packet budget
          [OPEN: token measurement not yet performed]

MP72-034  controller hash matches GitHub, Supabase, and required runtime activation surfaces
          [OPEN: hash not yet finalized; required before operative transition]

MP72-035  four-review convergence artifact exists before final DCS operative designation
          [OPEN: one review remaining — Antigravity; convergence artifact not yet produced]
```

---

# 33. THREE-REVIEW INTEGRATION STATE

This revision incorporates three review inputs.

R1 and R2 accepted corrections (from R2 Section 32) are carried forward without change.

**R3 accepted corrections (Claude Code independent review, 2026-08-08):**

1. Lane registry replaced with DCS-grounded topology: enterprise lanes DCSE, SC, SS, PS, PPR; routing labels SYSTEM/TSL/TRIBUNAL/DDNA/RAG/INFRA-TECH dispositioned under DCSE; DCS reclassified as authority identity.
2. D17 identity corrected: DART Universal Methodology (not Supabase security); compiled section added.
3. Supabase security doctrine flagged as incorrectly labeled D17; pending separate DCS doctrine number assignment.
4. D01-D20 compiled sections added to Section 17 (previously absent, causing MP72-001 failure).
5. Runtime surfaces enumerated from live DB (Section 31) with MP72-030 mandatory designation.
6. Poller operational contract grounded in MP72_POLLER_SESSION_RUNTIME (Section 31.3).
7. TI lane flagged as lacking v7.1 source grounding; treated as DCSE operational subdomain pending resolution.
8. D15 correctly labeled in compiled section (was unlabeled in R2 Section 17).

**R3 findings carried forward as open (require additional DCS disposition or build work):**

- Conflict ledger not yet executed (MP72-019, MP72-031).
- Source and compilation hashes not yet recorded (MP72-020, MP72-021, MP72-034).
- Rollback package not yet produced (MP72-026).
- Token measurement not yet performed (MP72-033).
- TI lane grounding pending (MP72-003 partial; see Section 36).
- Supabase security doctrine number pending (see Section 36).

---

# 34. REMAINING REVIEW GATE

This candidate SHALL be sent to:

```text
Antigravity
```

Claude Code has completed its review (incorporated as R3 corrections above).

Each reviewer SHALL return:

- VERIFIED findings;
- LIKELY findings;
- UNKNOWN items;
- severity;
- exact rule/section affected;
- source/evidence basis;
- required correction;
- final disposition.

The remaining review SHALL be reconciled with the three already received.

No reviewer narrative alone constitutes promotion.

The four-review convergence artifact SHALL preserve:

- all four raw reviews;
- consensus findings;
- conflicts among reviewers;
- accepted corrections;
- rejected recommendations with rationale;
- unresolved evidence gaps;
- final candidate hash.

---

# 35. CURRENT DISPOSITION

```json
{
  "controller_family": "7.2",
  "candidate_version": "7.2.0-CANDIDATE-R3",
  "readiness": "NOT_READY",
  "authority": "CANDIDATE",
  "deployment": "STAGED",
  "evolution": "CONTROLLED",
  "reviews_received": 3,
  "reviews_required_for_convergence": 4,
  "remaining_reviewers": ["antigravity"],
  "r3_corrections_applied": [
    "F-01: lane registry — DCS topology decision applied",
    "F-02: D17 identity — DART section added; Supabase file flagged",
    "F-05: missing D01-D20 compiled sections added",
    "F-06: mandatory runtime surfaces enumerated from DB",
    "F-08: poller contract grounded in MP72_POLLER_SESSION_RUNTIME"
  ],
  "open_blockers": [
    "lint pass not yet executed (MP72-019, MP72-031, MP72-032)",
    "source hashes not yet recorded (MP72-020, MP72-021)",
    "rollback package not produced (MP72-026)",
    "authority transition record not produced (MP72-029)",
    "surface acknowledgment not yet collected (MP72-030)",
    "controller hash not finalized (MP72-034)",
    "four-review convergence artifact pending (MP72-035)",
    "TI lane grounding pending (Section 36)",
    "Supabase security doctrine number pending (Section 36)"
  ],
  "operative": false
}
```

---

# 36. OPEN DCS ITEMS (Pending Resolution)

The following items require DCS disposition before this candidate can achieve readiness `READY` or move to operative designation. These are not blocking the four-review convergence but SHALL be resolved before final DCS operative designation.

| Item | Description | Blocking? |
|---|---|---|
| TI lane grounding | TI (Training/Instruction) is in R2 registry with no v7.1 source-grounded definition. Is TI a distinct enterprise lane (requiring source document and DCS designation) or confirmed as DCSE operational subdomain? | MP72-003 partial |
| Supabase security doctrine number | `docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md` requires a doctrine number that is not D17. Suggested D23 or next available number. DCS assignment required. | Named reference integrity |
| TSL routing confirmation | TSL is dispositioned as DCSE routing label in Section 11.4. Is this confirmed as permanent disposition, or does TSL require its own enterprise lane definition? | MP72-003 partial |
| RAG disposition | RAG has zero active tasks and is used as a routing label. Keep with DCSE routing, or retire the label entirely? | Label registry hygiene |
| DCS decision queue routing | DCS tasks currently appearing in `dcse_cp.agent_tasks` with `lane: DCSE` or `lane: SYSTEM` — should a separate DCS decision queue be established, or does the existing `handleDCSQueue` endpoint handle this? | Operational |

---

# 37. CONTROLLING PRINCIPLE

**One operative controller.**

**D01-D22 retained as source governance artifacts.**

**MP constitutional rules remain MP rules, not an invented D00 doctrine.**

**PS and PPR remain protected.**

**D21 execution semantics and D22 distribution authority survive compilation.**

**Readiness, authority, deployment, and evolution remain independent.**

**Context compilation fails closed.**

**Every normative rule remains traceable to immutable source evidence.**

**Evidence outranks narrative.**

**Independent review validates without stopping authorized remediation.**

**No silent governance mutation.**

**Structure Precedes Scale.**
