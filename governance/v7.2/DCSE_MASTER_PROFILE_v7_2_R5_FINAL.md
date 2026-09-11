# DCSE MASTER PROFILE v7.2
## Compiled Governance Controller, Reconciled Candidate R5

**Artifact Class:** Enterprise Governance Controller
**Controller Family:** DCSE Master Profile 7.2
**Candidate Revision:** 7.2.0-CANDIDATE-R5
**Authority:** DCS
**Current Authority State:** CANDIDATE
**Readiness State:** READY_WITH_FINDINGS
**Deployment State:** STAGED
**Evolution State:** CONTROLLED
**Architecture Principle:** Structure Precedes Scale
**Execution Model:** Goal-State Orchestration + Forward/Backward/Reverse-Chain Resolution
**Integration Basis:** v7.1 authoritative Master Profile and doctrine corpus; two original independent review inputs; Claude Code R2 independent review; Gemini advisory external inspection; Claude CP R4 architectural review return `CPR4-2026-08-08` (promoted to FORMAL REVIEW INPUT by DCS 2026-08-08); DCS-directed v7.2 capability/toolset, infrastructure, and session-poller corrections.
**Predecessor:** 7.2.0-CANDIDATE-R4
**D17 Reconciliation Commit:** `98d3c6ccf1765a4aa5e9bfc0134a078696e011c8`
**Runtime Surface Manifest:** `runtime_surface_manifest.v7.2.r4.json`
**Runtime Manifest SHA-256:** `45a504d8195656758cada4834c4d67fa049b3070520ac9651a5bb2f774fe466a`
**Lane Mapping Artifact:** `lane_mappings.v7.2.r5.json` (see §11.3; hash REQUIRED_AT_BUILD)
**Finding Closure Register:** §43
**Open Evidence Items and Readiness Exit Criteria:** §44
**DCS Ratification Items:** §45

**Important:** `READY_WITH_FINDINGS` means construction is complete and every review finding is closed **in the text**, while a defined set of build-evidence artifacts remains outstanding. It does **not** make v7.2 OPERATIVE. DCS retains the authority transition. Runtime activation remains a separate deployment/cutover gate. §44 states the exact conditions under which readiness advances to `READY`.

---

# 0. CONTROLLING PURPOSE

DCSE Master Profile v7.2 SHALL establish one authoritative enterprise governance controller while preserving source doctrine provenance, lane isolation, runtime executability, independent validation, and controlled evolution.

The v7.2 architecture SHALL:

1. compile the shared governing substance of D01-D12 and D15-D22, while compiling D13/D14 only as protected identities and routing controls;
2. preserve D01 through D22 as source governance artifacts;
3. keep constitutional/controller provisions under `MP-*` identifiers rather than inventing a D00 doctrine without source authority;
4. minimize runtime context by generating authorized context packets rather than transmitting the entire governance artifact;
5. preserve D21 runtime-engine behavior and D22 source/distribution authority within the compiled controller;
6. maintain strict PS and PPR isolation;
7. preserve evidence, communication-state, promotion, rollback, database, artifact-security, capability-routing, and source-mode controls from the governing v7.1 corpus unless expressly superseded;
8. support official operative authority without implying immutable finality;
9. prevent silent governance mutation;
10. make the controller mechanically auditable;
11. classify every revision-to-revision delta, including every deletion, so that no normative rule or machine field is removed without a record.

> **R5 note (closes CPR4-011).** Item 1 narrows the R3 formulation ("compile the governing substance of D01 through D22"). That narrowing is correct and is retained. It is now classified in §4.7 as `DOCTRINE_CHANGE / NON_BREAKING / MINOR` rather than being carried as an unrecorded constitutional change. Item 11 is new in R5 and exists to prevent the class of silent deletion identified across the R3 to R4 delta.

---

# 1. CONTROLLER ARCHITECTURE

## 1.1 Canonical Model

```text
AUTHORITATIVE GOVERNANCE SOURCES
        |
        +-- Current controlling Master Profile
        +-- D01 through D22
        +-- Ratified amendments / express DCS directives (registry: §2.4)
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

Express DCS directives are a first-class authority source. They SHALL be addressable through the registry defined in §2.4. Authority SHALL NOT be established from an unregistered directive.

## 1.2 Canonical Controller Artifact vs Runtime Context Packet

**Canonical Controller Artifact** means the complete compiled governance authority.

**Runtime Context Packet** means a task-specific projection of the canonical controller.

**Controller Header** means the mandatory minimal subset included in every authorized runtime packet.

A runtime does not automatically receive the entire canonical controller. It SHALL receive the smallest sufficient authorized projection that preserves every mandatory rule dependency, Stop-Gate, lane restriction, authority reference, and evidence requirement applicable to the task.

"Smallest sufficient" is defined operationally in §1.3. It is not a discretionary judgment.

## 1.3 Context Packet Generation Contract

> **New in R5 (closes CPR4-022).**

Packet generation SHALL follow this contract. §23 fail-closed behavior governs unresolvable dependencies; this section governs dependency **discovery**, which fail-closed cannot cover because an undiscovered dependency never presents as unresolved.

**Mandatory inclusions in every packet, without exception:**

```text
Controller Header (Layer 1)
applicable Stop-Gate registry entries
applicable lane restrictions and protected-module controls
applicable authority references
applicable evidence requirements
```

**Dependency resolution:**

```text
1. Resolve the task's directly required rules.
2. Compute TRANSITIVE CLOSURE over rule dependencies.
3. Terminate closure on:
     a. all dependencies resolved, OR
     b. depth limit reached, OR
     c. dependency cycle detected.
4. On (b) or (c): fail closed, emit Stop-Gate with the dependency graph,
   the depth reached, and the termination reason.
```

The closure depth limit SHALL be recorded in the runtime manifest, not in this controller, because it is a tuning value rather than a normative guarantee. The **existence** of a limit is the normative guarantee.

**Packet manifest.** Every packet SHALL carry a manifest recording each included rule ID and its inclusion basis (`DIRECT`, `TRANSITIVE`, `MANDATORY_HEADER`, `STOP_GATE`, `LANE_CONTROL`).

**Runtime preflight.** Before execution, the runtime SHALL verify that every rule ID in its expected rule set is present in the loaded packet. A missing rule SHALL fail closed rather than proceed on the assumption that absence means non-applicability.

**Compression boundary.** Compression under §30 operates only on representation (stable references, registries, deduplication, compiled rule IDs). It SHALL NOT operate on closure membership. A rule inside the transitive closure SHALL NOT be dropped to meet a budget. Where closure and budget cannot both be satisfied, the packet fails closed and escalates; it does not silently truncate.

---

# 2. GOVERNANCE SOURCE MODEL AND FROZEN INVENTORY

## 2.1 Governing Source Set

The shared v7.2 controller source model is:

```text
D01-D12  shared governed sources
D13      PS-protected source; excluded from shared runtime loading
D14      PS-protected source; excluded from shared runtime loading
D15-D22  shared governed sources
```

There is no invented D00 doctrine. Controller rules use `MP-*` identifiers.

D13 and D14 remain source-governed protected modules. Their absence from the shared `dcse_cp.governance_directives` table is not a missing-doctrine defect. They SHALL be referenced only by identity, classification, provenance, and routing controls in the enterprise-shared controller.

## 2.2 Frozen Doctrine Inventory

D22 SHALL be identified as `D22. Source Authority and Runtime Distribution`. This naming is normative, not descriptive metadata. *(Restores the R3 §2.2 normative rule; closes CPR4-018.)*

| ID | Canonical Title | Shared Disposition | Verified SHA-256 / Source Hash |
|---|---|---|---|
| D01 | Forward Thinking | RETAIN_LAYER3 | `DA45B7AB01ED4A978167510A6B0D77106B6C7BA26747E31AF77DDAEDC8EAAE17` |
| D02 | Forward and Backward Chaining | RETAIN_LAYER3 | `CA8894F1D7E95CC22D277421A9EB0DE55EED4B41E49DC8978C152AA15DFE19C2` |
| D03 | AI Orchestration and Prompt Wrappers | SUBSUMED_IN_MP + RETAIN_LAYER3 | `083DB9EEB16B86565E7544C6D4F9314A37DAFCA921C3572472A8C928184BCA3D` |
| D04 | Command Post Communications | SUBSUMED_IN_MP + RETAIN_LAYER3 | `850CB096B1EDE8A1539AFC201F0922A58C9F086AE0F4282091CBFF139B892394` |
| D05 | Baseline and Promotion | SUBSUMED_IN_MP + RETAIN_LAYER3 | `C4912B2BB261D3CA3F1F27AE3289389D9852E65E2B141157E157D00EBEC4BAD0` |
| D06 | File System and Device Governance | RETAIN_LAYER3 | `74C03A8212BD89F2EE200F7713876E8E5ABE03125D9F282D4967C93913DCCAB0` |
| D07 | Campaign Governance | RETAIN_LAYER3 | `E81483C20D586E01BB4D31CC32998FAE92E0A5C3C557BB334879C13BEFD7B5DE` |
| D08 | Voice and Tone | RETAIN_LAYER3 | `606CAC058B76FE90A8A763CC93676FE77FCFD5B3D94AC97593A60F8414432885` |
| D09 | Brand Identity | RETAIN_LAYER3 | `096735521A5B2986C7B598AE653A836070DF93683E68139F52B46A3D9DD69555` |
| D10 | Persona Assets | RETAIN_LAYER3 | `9F9D1C72444D60CFC0F10F4C6BFF9DC0AC19C99683871B3E50D81EA035CCC1CE` |
| D11 | HTML, Wix, and App Governance | RETAIN_LAYER3 | `6E31CC245DEE4C922172F55C3AD9C5692D65E5E180CAE0BCB98814EAC5B3F516` |
| D12 | Video and Media | RETAIN_LAYER3 | `5AE4F1593D19EAE66B517A9819046980EDD011C506E0359A124B8096D79919A9` |
| D13 | DART Core | PROTECTED_MODULE | `8FF25A019954070B3AAFF53FA77324E8FA5A13D9863DE77329563F035D79662E` |
| D14 | DART PS Protected & Litigation Blueprints | PROTECTED_MODULE | `EC6B810BAD47E245CA33902AAA68C5B0D01438B017C94E47F7AFB0FD734394F8` |
| D15 | Database Administration | SUBSUMED_IN_MP + RETAIN_LAYER3 | `6A8F4A5BF66A53C902F0F74D1FD99A7FD484D2FC12F5F8CBA62E9AD9FAEC6ABD` |
| D16 | DDNA Governance | SUBSUMED_IN_MP + RETAIN_LAYER3 | `AF856F66A3A4405D27438D84150E17561A83DAA927F20A5A88DE9826EC3B7D61` |
| D17 | DART Universal Assurance Methodology | SUBSUMED_IN_MP + RETAIN_LAYER3 | `12186A59C0AEE0F83E08DBAB6E78ECFDC868E2078DE4835544164EDADBDE2392` |
| D18 | Media Production Pipeline | RETAIN_LAYER3 | `4766766707E67D055E8FE073C964F3912A4645840518F82B65BA51ABB06F218C` |
| D19 | Visual Creation Pipeline | RETAIN_LAYER3 | `C6F24726657B7D7042DAEF0353439DC923107B0F8F98AE62AB6DDADC4B480ECC` |
| D20 | Product Assembly Methodology | SUBSUMED_IN_MP + RETAIN_LAYER3 | `902EC78EA0184E8C1576BE5503EC216B5013C431F9B38DFD198795D3BDCE9B56` |
| D21 | Doctrine Runtime Engine | SUBSUMED_IN_MP + RETAIN_LAYER3 | `224EB63AE6B1EED524E642CB1B6FE934395AAF4D4338E540A3720C1E9DBE74FF` |
| D22 | Source Authority and Runtime Distribution | SUBSUMED_IN_MP + RETAIN_LAYER3 | `BE24661B9FC9C6A3E5E1D5EA9ADFA706C59AB9EF5DA925904A1BF814FD561885` |

### 2.2.1 Per-Doctrine Hash Provenance

> **New in R5 (closes CPR4-017).**

§24.1 defines five hash classes and prohibits conflating them. The column above therefore requires a declared basis per row. R4 annotated only D22 ("the R4 direct hash of the canonical v7.1 source bytes used for compilation"), leaving D01 through D21 with an undeclared basis.

The source-freeze manifest SHALL record, for **every** row above:

```text
hash_class          one of the §24.1 classes
retrieval_basis     canonical repository bytes | asset registry |
                    promotion evidence | database body
repository_commit
repository_path
retrieval_timestamp
artifact_size_bytes
```

Status: `REQUIRED_AT_BUILD`. See §44 item OE-05. The hash values above are retained unchanged; only their declared provenance is outstanding.

D22's SHA-256 is recorded as the R5-retained R4 direct hash of the canonical v7.1 source bytes used for compilation.

## 2.3 Source Status and Compiled Authority

Source lifecycle, compiled inclusion, controller readiness, controller authority, and deployment remain independent.

A source record may be promoted-with-known-gaps and still be retained with those gaps visible. Compilation does not silently upgrade the source's historical status.

A source doctrine SHALL NOT become OPERATIVE merely because its content is compiled.

The controller SHALL preserve both:

```text
source provenance
compiled rule provenance
```

and SHALL never infer authority from file existence, repository version number, database presence, or model memory.

### 2.3.1 Machine Form

> **Restored in R5 (closes CPR4-012).** R3 §2.3 carried this vocabulary; R4 retained the prose and dropped the machine expression, leaving §3's "record that separate authority basis" requirement with no field to record into.

```json
{
  "doctrine": "D03",
  "source_status": "CANDIDATE",
  "compiled_section": "#d03",
  "compiled_status": "ACTIVE_IF_AUTHORIZED",
  "authority_inherited_from": "DCSE_MASTER_PROFILE_7.2",
  "separate_authority_basis": null
}
```

`compiled_status` vocabulary:

```text
ACTIVE_IF_AUTHORIZED   compiled content is controlling only through the
                       controller's own authority, not through its source status
PROTECTED_REFERENCE    identity and routing compiled; body excluded (D13/D14)
HISTORICAL_ONLY        retained for provenance; not controlling
```

`authority_inherited_from` SHALL be populated for every doctrine whose disposition includes `SUBSUMED_IN_MP`.

`separate_authority_basis` SHALL be populated where §3 applies, and SHALL cite a registered directive from §2.4.

## 2.4 Express DCS Directive Registry

> **New in R5 (closes CPR4-023).**

§1.1 names express DCS directives as a top-level authority source, and §3 requires the compiler to record a separate authority basis where a directive makes a candidate or pending rule controlling. Neither is addressable without a registry, and §2.3 prohibits establishing authority from file existence, repository state, database presence, or model memory. Absent a registry, an operator can only rely on a prohibited basis.

Registry artifact: `dcs_express_directives.v7.2.json`. Named and hashed per §24. Status: `REQUIRED_AT_BUILD` (see §44, OE-04).

Required fields per directive:

```text
directive_id
issued_at            ISO-8601
issuing_authority    DCS
directive_text
affected_sections    controller sections and/or D-numbers
incorporation_commit
status               ACTIVE | INCORPORATED | SUPERSEDED | WITHDRAWN
supersedes           directive_id or null
```

Rules:

- A directive not present in the registry SHALL NOT establish authority.
- A directive with status `ACTIVE` and no `incorporation_commit` is binding but not yet compiled, and SHALL be surfaced by the governance linter as an open item.
- Directive identifiers are immutable and reserved under §9.

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

Where a rule from a candidate or pending source is already made controlling by the current Master Profile or an express DCS directive, the compiler SHALL record that separate authority basis in `separate_authority_basis` per §2.3.1, citing a registered directive per §2.4.

No lifecycle mapping alone creates new authority.

---

# 4. FOUR-DIMENSION STATE MODEL

The v7.2 controller SHALL use independent state dimensions.

## 4.1 Readiness

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

## 4.6 State Transition Rules

> **New in R5 (closes CPR4-021).** R3 and R4 both enumerated state values without defining transitions. This is operationally immediate: R5 itself enters `READY_WITH_FINDINGS`, a state R4 provided no route out of.

### 4.6.1 Readiness Transitions

| From | To | Trigger | Required Evidence | Authority |
|---|---|---|---|---|
| NOT_READY | READY_WITH_FINDINGS | build complete, findings open | build-readiness test results with open findings enumerated | Build authority |
| NOT_READY | READY | build complete, no findings | all build-readiness tests PASS or formally dispositioned | Build authority, DCS confirmation |
| READY_WITH_FINDINGS | READY | every open finding closed | per-finding closure record; build-readiness suite re-run | DCS |
| READY_WITH_FINDINGS | NOT_READY | a CRITICAL finding is opened, or open findings exceed the disposition window | finding record | DCS or governance linter |
| READY | NOT_READY | regression detected, or source-freeze invalidated | lint or acceptance-test failure record | Governance linter, automatic |

**Finding closure record.** A finding is closed when there exists a record containing: finding ID, closing change (section and text), evidence reference, closing authority, and timestamp. A finding SHALL NOT be closed by assertion.

**Disposition window.** An open finding without a recorded disposition SHALL be surfaced by the linter after 30 days and SHALL escalate to DCS. Readiness does not silently degrade; DCS decides.

### 4.6.2 Authority Transitions

| From | To | Trigger | Constraint |
|---|---|---|---|
| DRAFT | CANDIDATE | construction begins under governed build | reversible |
| CANDIDATE | DRAFT | build withdrawn | permitted; record reason |
| CANDIDATE | OPERATIVE | DCS operative designation per §42 | atomic; requires §5 fields and §26 rollback record |
| OPERATIVE | SUPERSEDED | a successor becomes OPERATIVE | automatic and simultaneous with the successor transition |
| SUPERSEDED | ARCHIVED | administrative action after retention period | retention period recorded in the runtime manifest; not reversible |
| SUPERSEDED | OPERATIVE | rollback per §26 | permitted only through the recorded rollback procedure |
| ARCHIVED | any | prohibited | terminal |

### 4.6.3 Deployment Transitions

| From | To | Trigger |
|---|---|---|
| STAGED | SYNCHRONIZING | push to control surfaces begins |
| SYNCHRONIZING | SYNCHRONIZED | every mandatory surface acknowledges the controller identity |
| SYNCHRONIZING | DEGRADED | any mandatory surface fails to acknowledge |
| DEGRADED | SYNCHRONIZED | fault remediated, surface re-deployed, health probe confirms, evidence recorded |
| any | ROLLED_BACK | rollback executed per §26 |

**Atomicity.** Aggregate `SYNCHRONIZED` SHALL NOT be recorded while any mandatory enforcement surface is unacknowledged. Partial synchronization across mandatory surfaces is `DEGRADED`, not `SYNCHRONIZED`. Evidence and closeout surfaces per §6 are excluded from this constraint.

### 4.6.4 Evolution Transitions

| From | To | Trigger |
|---|---|---|
| CONTROLLED | FROZEN | express DCS freeze order, recorded end-of-life, or security/compliance hold |
| FROZEN | CONTROLLED | express DCS unfreeze order, or expiry of a recorded time-bound freeze |

While `FROZEN`, the artifact MAY receive security and emergency corrections tagged as such, and SHALL NOT receive feature additions, behavior changes to existing rules, or source recompilation.

## 4.7 Revision Delta Classification

> **New in R5 (closes CPR4-011, and encodes the structural lesson of the R3 to R4 delta).**

Every revision SHALL be diffed against its predecessor for **deleted normative sentences and deleted machine fields**, not only for added content. Every delta, including every deletion, SHALL carry a §4.5 classification.

R4 to R5 delta classification:

| Delta | Change Type | Compatibility | Release Class |
|---|---|---|---|
| §0 item 1 scope narrowing (inherited from R4, previously unclassified) | DOCTRINE_CHANGE | NON_BREAKING | MINOR |
| §0 item 11 added | CLARIFICATION | NON_BREAKING | MINOR |
| §1.3 packet generation contract added | ARCHITECTURE_CHANGE | NON_BREAKING | MINOR |
| §2.2.1 hash provenance requirement added | CORRECTION | NON_BREAKING | PATCH |
| §2.3.1 machine form restored | CORRECTION | NON_BREAKING | PATCH |
| §2.4 directive registry added | ARCHITECTURE_CHANGE | NON_BREAKING | MINOR |
| §4.6 state transitions added | ARCHITECTURE_CHANGE | NON_BREAKING | MINOR |
| §4.7 delta classification added | CLARIFICATION | NON_BREAKING | MINOR |
| §6.1 timing split into constitutional and manifest values | CORRECTION | NON_BREAKING | PATCH |
| §11.3 lane mappings populated | CORRECTION | NON_BREAKING | PATCH |
| §12 protected-module machine fields restored | CORRECTION | NON_BREAKING | PATCH |
| §24 immutable-hash production list restored | CORRECTION | NON_BREAKING | PATCH |
| §25.1 validator independence defined | DOCTRINE_CHANGE | NON_BREAKING | MINOR |
| §30 fit rule restored | CORRECTION | NON_BREAKING | PATCH |
| §31 readiness gate restored | CORRECTION | NON_BREAKING | PATCH |
| §31 MP72-002/012/044/045 restated | CORRECTION | NON_BREAKING | PATCH |
| §31 MP72-060 to MP72-073 added | CLARIFICATION | NON_BREAKING | MINOR |
| §37 dated obligation converted to durable obligation | CORRECTION | NON_BREAKING | PATCH |
| §39 reduced to cross-reference | CORRECTION | NON_BREAKING | PATCH |
| §40.2 repair termination added | CORRECTION | NON_BREAKING | PATCH |

Aggregate R4 to R5 release class: **MINOR**. No `BREAKING` change is introduced. No rule present in R4 is removed; R5 restores rules that R3 contained and R4 dropped.

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

**In-flight coordination.** In-flight tasks at the moment of transition are governed by §27. A task SHALL NOT observe a controller version change mid-execution. Where a task cannot complete under its pinned controller before cutover, it SHALL be migrated per §27 with a recorded migration receipt, or held.

---

# 6. RUNTIME SURFACE MANIFEST AND SESSION ACTIVATION

The mandatory runtime-surface requirements are frozen in:

```text
runtime_surface_manifest.v7.2.r4.json
SHA-256 45a504d8195656758cada4834c4d67fa049b3070520ac9651a5bb2f774fe466a
```

The manifest distinguishes **controller readiness** from **runtime cutover**.

Required surface classes include:

```text
SOURCE_AUTHORITY
CONTROL_STATE
RUNTIME_ENFORCEMENT
RUNTIME_WAKE
CONTROL_INTERFACE
EVIDENCE_CLOSEOUT
```

Current mandatory cutover surfaces include:

1. GitHub canonical controller source;
2. Supabase `dcse_cp` control state;
3. Windows `DCSE_Universal_Dispatch_Controller`;
4. the governed Windows runtime worker;
5. the Windows lightweight wake probe;
6. Command Post dispatch when web dispatch is enabled.

Tribunal synchronization remains an evidence/closeout surface and does not independently create controller authority.

## 6.1 Session Runtime Contract

The v7.2 poller is **session-based**, not 24/7 model execution.

This section is the single normative statement of the poller contract. §39 is explanatory and SHALL NOT restate normative content. *(Closes CPR4-005.)*

### 6.1.1 Constitutional Invariants

These are normative guarantees. Changing them requires a controller version change.

```text
- the controller is a session runtime, not a 24/7 model process
- minimum continuous inactivity before sleep: NOT LESS THAN 60 minutes
- the 60-minute floor is a DCS minimum; a runtime may remain active longer
- the floor SHALL NOT be automatically reduced without express DCS authority
- a wake probe SHALL NOT launch a model when no work exists
- an actionable event resets the inactivity window
```

### 6.1.2 Manifest Configuration Values

> **Relocated in R5 (closes CPR4-004).** R4 §6.1 placed these in the constitutional body while R4 §18.2 simultaneously required deployment-specific timing values to live in the runtime manifest. R5 resolves the contradiction in favor of §18.2, which is the rule R3 and R4 both carried.

The following are configuration, recorded in `runtime_surface_manifest.v7.2.r4.json` with provenance to the verified implementation and DCS-approved operational policy:

```text
active poll interval          currently 60 seconds
wake-probe interval           currently 5 minutes (candidate)
heartbeat interval
wall-time limit
health-monitor interval
context closure depth limit   (per §1.3)
```

Changing any of these within authorized operational bounds does not require a controller version change unless it alters a normative guarantee in §6.1.1.

### 6.1.3 Sleep Preconditions

The active controller may sleep only after at least 60 continuous minutes in which all are true:

```text
no claimable assignments
no running workers
no pending recovery
no unconsumed wake request
no actionable event/dispatch activity
```

### 6.1.4 Actionable Event Enumeration

This is the single authoritative list. An event of any of these types resets the inactivity window.

```text
new task assignment
DCS instruction
actionable comment
review complete
result submitted
handoff ready
recovery event
explicit dashboard/manual wake
```

*(R5 adopts the union of the two non-identical lists carried in R4 §6.1 and R4 §39. `recovery event` and `explicit dashboard/manual wake` appeared only in §39; both are retained.)*

Events that do **not** reset the window:

```text
log-only events with no state change
informational comments requiring no action
query-only interactions with no execution requested
```

## 6.2 Cutover Gate

`Readiness=READY` does not imply runtime activation.

Before `Authority=OPERATIVE`, every mandatory cutover surface SHALL acknowledge the operative controller identity and provide required host/API evidence.

Legacy provider-specific pollers are `ROLLBACK_ONLY` unless explicitly reclassified.

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

Each source doctrine retains its identity, source status, provenance, and internal addressing.

## Layer 4. Machine Control Layer

Contains:

- doctrine registry;
- lane registry and lane mappings;
- rule registry;
- Stop-Gate registry;
- protected-module registry;
- artifact-security classes;
- source modes;
- capability-routing metadata;
- communication-state model;
- context packet schema and packet manifest schema;
- receipt schema;
- state-transition records;
- express DCS directive registry.

**Layer 4 integrity rule.** A control that the context compiler must evaluate SHALL be expressed as a machine field in this layer. Prose statement alone is insufficient. *(New in R5; encodes the root cause behind CPR4-008 and CPR4-012.)*

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
- rollback metadata;
- incorporated external review returns.

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

## 8.1 Precedence Hierarchy

Where the controlling hierarchy must be applied, precedence is:

```text
1. Express DCS directive, registered per §2.4
2. D13/D14 PS protection and PPR protection controls
3. Stop-Gate rules
4. MP-* constitutional controller rules
5. D01-D22 source doctrine
```

Within tier 5, a conflict between two source doctrines SHALL be entered in the conflict ledger and dispositioned. It SHALL NOT be resolved by doctrine number, recency, or apparent specificity.

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

This reservation rule applies equally to acceptance-test identifiers (`MP72-*`), Stop-Gate identifiers, directive identifiers, and finding identifiers.

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

# 11. DUAL LANE REGISTRY AND MAPPING

Two different concepts are kept separate and explicitly mapped:

1. **Governance / business lanes** defined by the Master Profile and doctrine firewall.
2. **Runtime dispatch lanes** actually used by the v7.1 control plane.

## 11.1 Governance / Business Domain Registry

```text
DCSE
DCS
SC
SS
TI
PS
PPR
INFRA/TECH
```

DCS SHALL be treated primarily as the sovereign authority identity. Its appearance in the historical governance-lane inventory SHALL NOT by itself create an autonomous runtime dispatch lane.

PS and PPR remain protected regardless of runtime-lane mapping.

## 11.2 Verified Runtime Dispatch Lane Registry

Claude's R2 review verified that the live v7.1 control plane currently uses or authorizes runtime lanes including:

```text
DCSE
PS
SC
SS
TSL
TRIBUNAL
DDNA
RAG
SYSTEM
```

These runtime values SHALL NOT be rejected merely because they are not all constitutional business lanes. In particular, `TRIBUNAL`, `DDNA`, `RAG`, and `SYSTEM` are technical/runtime routing domains; `TSL` is a live operational product lane.

## 11.3 Lane Mapping

> **Populated in R5 (closes CPR4-009).** R4 §11.3 specified `lane_mappings` as an empty array and carried the dispositions as prose. R4 named and hashed the runtime surface manifest but gave the equally load-bearing lane mapping neither. R5 populates the mapping from R4's own stated dispositions and requires it to be bound as a named, hashed artifact.

Mapping artifact: `lane_mappings.v7.2.r5.json`. Hash status: `REQUIRED_AT_BUILD` (see §44, OE-03).

| Runtime Dispatch Lane | Controlling Governance Authority | Class | Basis | Status |
|---|---|---|---|---|
| DCSE | DCSE | ENTERPRISE | constitutional business lane | MAPPED |
| PS | PS | PROTECTED | protected lane; D13/D14 addressable only here | MAPPED |
| SC | SC | BUSINESS | constitutional business lane | MAPPED |
| SS | SS | BUSINESS | constitutional business lane | MAPPED |
| TSL | DCSE | PRODUCT | live product lane retained during migration; not a constitutional lane | MAPPED, MIGRATION_SCOPED |
| TRIBUNAL | INFRA/TECH | TECHNICAL | evidence and closeout routing domain | MAPPED |
| DDNA | DCSE (D16 DDNA Governance) | TECHNICAL | governed by D16 | MAPPED |
| RAG | INFRA/TECH | TECHNICAL | retrieval routing domain | MAPPED |
| SYSTEM | INFRA/TECH | TECHNICAL | system routing domain | MAPPED |

Governance domains without a runtime dispatch lane:

| Governance Domain | Runtime Lane | Basis |
|---|---|---|
| DCS | NONE | authority identity; no autonomous dispatch lane by default |
| PPR | NONE | protected; no autonomous dispatch lane |
| TI | NONE | governance domain retained; absence of a live lane does not delete the domain |
| INFRA/TECH | indirect | maps to TRIBUNAL, RAG, SYSTEM where source evidence supports it |

Not promoted:

```text
FAMILY   not a constitutional enterprise lane in this candidate.
         Family products remain governed product domains until
         separately authorized.
```

Each runtime lane SHALL map to controlling governance authority without silently redefining the constitutional lane model.

Unknown or conflicting lane mappings SHALL first emit a `MIGRATION_REQUIRED` receipt containing the legacy value, attempted mapping, controlling source, and remediation route. If no safe mapping is verified, execution then enters `LANE_MAPPING_STOP_GATE`.

This migration receipt prevents silent rejection of legacy/in-flight tags while preserving fail-closed behavior. It SHALL NOT authorize an unknown lane.

## 11.4 Test Rule

MP72-003 SHALL compare the compiled governance registry against the authoritative source inventory **and** compare the runtime dispatch registry against the frozen live control-plane inventory. A self-referential test against R5's own list is prohibited.

**Generalized.** No acceptance test SHALL assert its own conclusion. Every test SHALL verify against evidence external to the controller's own assertion of the fact under test. *(Generalized in R5 from MP72-003 to all tests; bound by MP72-065; closes CPR4-006 at the level of principle.)*

---

# 12. D13/D14, PS, AND PPR PROTECTED MODULE FIREWALL

Enterprise-shared runtime context SHALL NOT contain substantive PS case facts, case identifiers, evidence details, damages, witnesses, litigation dates, comparator details, protected litigation strategy, or DART-PS substantive facts.

The shared controller SHALL contain only the abstract firewall, identity, provenance, and routing rules required to protect PS/PPR.

D13 and D14 are explicitly protected source modules:

```json
{
  "protected_modules": {
    "D13": {
      "title": "DART Core",
      "lane": "PS",
      "classification": "PS-PROTECTED",
      "default_load": false,
      "shared_body_compile": false,
      "cross_lane_export": false,
      "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
    },
    "D14": {
      "title": "DART PS Protected & Litigation Blueprints",
      "lane": "PS",
      "classification": "PS-PROTECTED",
      "default_load": false,
      "shared_body_compile": false,
      "cross_lane_export": false,
      "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
    },
    "PPR": {
      "lane": "PPR",
      "classification": "PROTECTED",
      "default_load": false,
      "shared_body_compile": false,
      "cross_lane_export": false,
      "unauthorized_access_action": "GOVERNANCE_STOP_GATE"
    }
  }
}
```

> **R5 restoration (closes CPR4-008).** R3 §12 carried `cross_lane_export` and `unauthorized_access_action` on protected entries. R4 dropped `unauthorized_access_action` from all entries and `cross_lane_export` from D13 and D14, leaving the control as prose only. Per the §7 Layer 4 integrity rule, a control the context compiler must evaluate cannot live in prose. R4's `shared_body_compile` is a genuine improvement and is retained alongside the restored fields, not instead of them.

D13/D14 remain addressable by authorized PS runtime packets but are not emitted into the enterprise-shared controller body.

D17 is **not** a PS-protected replacement for D13/D14. D17 is the universal enterprise DART assurance methodology and may be loaded across authorized non-PS lanes.

Any attempt to inject protected D13/D14 material into a non-PS interactive or autonomous context SHALL fail closed and emit a sanitization/security receipt.

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

Every mandatory runtime surface SHALL be able to report the controller version and the `artifact_sha256` it is enforcing.

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

# 17. D17 UNIVERSAL DART AND D15 DATABASE GOVERNANCE, SOURCE CONFLICT CLOSED

## 17.1 D17 Identity, RESOLVED

The recurring D17 conflict is closed.

Authoritative evidence establishes:

```text
Supabase promoted directive:
  D17 = DART Universal Assurance Methodology
  promotion_status = PROMOTED
  recorded promoted-source checksum =
    568a8f2b3b2f8a960ebcf30dc94679dbb66f94a51aa2a51a0a0f86dc1da633f1

Verified asset registry:
  D17_DART_Universal_Methodology.md
  SHA-256 =
    12186A59C0AEE0F83E08DBAB6E78ECFDC868E2078DE4835544164EDADBDE2392
  hash_verified = true
  promotion_status = PROMOTED

Authoritative v7.1 repository source:
  governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md
```

The conflicting repository path:

```text
docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md
```

was a July 29 database-security artifact with an incorrect D17 title. Its content belongs under the D15 database-governance subject area, not D17.

On 2026-08-07 that path was converted to a noncanonical compatibility tombstone in commit:

```text
98d3c6ccf1765a4aa5e9bfc0134a078696e011c8
```

The tombstone explicitly prohibits loading or compiling it as D17.

Therefore:

```json
{
  "stop_gate_id": "SOURCE_IDENTITY_CONFLICT_D17",
  "status": "RESOLVED",
  "canonical_d17": "D17_DART_Universal_Methodology.md",
  "database_governance": "D15",
  "blocks_readiness": false
}
```

**Regression detection.** The resolution is closed, and it remains closed only so long as it is mechanically detectable. MP72-012 therefore verifies the three independent conditions on which the resolution rests, rather than restating the conclusion. See §31 MP72-012 and §36.

## 17.2 D17 Universal DART Compilation

D17 defines the enterprise assurance sequence:

```text
DEFINE
ASSESS
RESOLVE
TEST
```

D17 operates as a universal methodology across governed DCSE work.

Protected litigation-specific DART sources remain D13/D14 and are not compiled into the shared D17 section.

## 17.3 D15 Database Governance

D15 remains the controlling database-administration doctrine.

Database work SHALL preserve, as applicable:

- migration-controlled changes;
- RLS and access-control design;
- least privilege;
- explicit grants;
- safe privileged-function controls;
- positive and negative authorization testing;
- security/performance review;
- rollback and idempotency;
- data-quality/integrity checks;
- schema-drift detection;
- post-change verification;
- independent validation when required, per §25.1.

Supabase registration or successful DDL execution alone is not proof of D15 compliance.

---

# 18. CAPABILITY-BASED ASSIGNMENT AND RUNTIME SURFACE CLASSES

Capability-based model and runtime assignment SHALL be preserved.

Logical agent identity, model backend, runtime surface, runtime instance, host, and dispatch lane SHALL remain distinct concepts.

No runtime SHALL be considered autonomously executable solely because it is registered.

## 18.1 Runtime Surface Classes

v7.2 SHALL recognize at least two governed runtime classes:

```text
AUTONOMOUS_CLAIMING
INTERACTIVE_NON_CLAIMING
```

### AUTONOMOUS_CLAIMING

An autonomous surface SHALL require:

- registered logical agent identity;
- verified runtime surface;
- authorized lane/capability;
- poller/admission eligibility;
- current heartbeat;
- database-authoritative atomic claim;
- Stop-Gate evaluation;
- bounded execution;
- receipt submission.

It SHALL NOT fabricate a claim or bypass admission merely because a user requested execution.

### INTERACTIVE_NON_CLAIMING

A legitimate interactive surface MAY execute bounded work under direct DCS/user-session authority even when `can_claim=false`.

Such work SHALL:

- identify itself as `INTERACTIVE_NON_CLAIMING`;
- never represent the session as a poller claim;
- preserve lane/firewall controls;
- identify the runtime surface and execution basis in its receipt;
- use a receipt type such as `DIRECTED_EXECUTION` or `INTERACTIVE_REVIEW`;
- remain ineligible for unattended autonomous claim unless separately admitted.

Examples observed in Claude's review evidence include `remote_cloud_ccr` and browser-chat surfaces with `can_claim=false`. Their existence does not invalidate the poller model; it requires a separate receipting path.

## 18.2 Poller Operational Contract

The constitutional controller SHALL govern poller **invariants**, while deployment-specific timing values SHALL be frozen in a runtime manifest unless DCS ratifies them as constitutional values.

Mandatory invariants:

```text
- recurring wake/scheduler mechanism
- per-runtime admission evaluation
- atomic claim
- bounded execution
- intermediate heartbeat during long-running work
- stale/orphan recovery
- health monitoring
- fail-closed admission and Stop-Gates
- immutable result evidence
- no duplicate provider-specific scheduler architecture
```

The exact scheduler interval, heartbeat interval, wall-time limit, and health-monitor interval SHALL be recorded in the operative runtime manifest with provenance to the verified implementation and DCS-approved operational policy. §6.1.2 enumerates the current set. This section and §6.1 are consistent; §6.1.1 holds the guarantees, §6.1.2 holds the configuration.

Changing a timing parameter within authorized operational bounds does not require a constitutional version change unless it alters a normative guarantee.

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

Unknown or unreconciled hash semantics SHALL fail closed for equivalence comparison, per §24.1.

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

The absence of a supporting artifact SHALL be recorded as `UNKNOWN`, not as a defect and not as a pass.

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

Independent validation remains separate from implementation authority. Independence criteria are defined in §25.1.

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

Fail-closed governs unresolvable dependencies. Dependency **discovery** is governed by the transitive closure contract in §1.3, because an undiscovered dependency never presents as unresolved.

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
  "stop_gates": [],
  "packet_manifest": []
}
```

Not every metadata field must be transmitted verbatim into a model prompt, but the control plane SHALL retain the complete compilation record.

---

# 24. PROVENANCE AND HASH SEMANTICS

Provenance SHALL support many-to-one and one-to-many compilation.

Each compiled rule record SHALL be able to identify:

```text
source doctrine
canonical path
source SHA-256 where available
repository blob/object identifier
promoted-source checksum where present
source rule/section
compiled rule ID
compiled controller hash
```

## 24.1 Hash Types

Hash types SHALL NOT be conflated.

```text
artifact_sha256:
  SHA-256 of exact canonical source bytes.

repository_blob_id:
  repository-native object identifier; currently Git SHA-1 semantics where applicable.

promoted_source_checksum:
  checksum preserved in governance_directives promotion evidence.
  It is not assumed to equal the database body SHA-256.

database_body_sha256:
  optional direct SHA-256 of the current database body text.

semantic_content_hash:
  optional normalized hash only when the normalization algorithm is versioned.

UNKNOWN_HASH_SEMANTICS:
  a hash whose byte basis and algorithm are not established.
  It SHALL NOT be compared to any other hash class as if equivalence
  were established, and it SHALL be reconciled or dispositioned before
  it can support any acceptance test.
```

> **R5 restoration (closes CPR4-020).** R4 resolved the specific `governance_directives.checksum` question empirically, which is a genuine improvement and is retained below. The general fallback class was removed alongside it, leaving no defined handling for the next hash of unknown semantics. R5 reinstates the class without disturbing the specific finding.

The build verified that current `governance_directives.checksum` values are not hashes of the database `body` field. The controller therefore preserves them as `promoted_source_checksum` rather than mislabeling them as body or file hashes.

Exact artifact SHA-256 values are frozen in the doctrine inventory for D01-D22. Protected D13/D14 hashes may be visible as provenance but their bodies remain excluded from shared runtime context.

A reviewer SHOULD NOT reopen a source identity conflict merely because two different documented hash classes differ. This is guidance per DCS disposition RAT-03, not a binding constraint. A reviewer who identifies evidence meeting a §36 reopening condition SHALL raise it.

## 24.2 Immutable Build Output Hashes

> **Restored and extended in R5 (closes CPR4-002).** R3 §24 carried this requirement. R4 dropped it. Its absence is the direct cause of R4 naming and hashing exactly one sidecar artifact and zero others, and of readiness being claimed with no retained test output.

The build SHALL produce immutable hashes for:

```text
every source artifact
the canonical compiled controller
the machine manifest
the rule registry
the context compiler release
the governance lint output
the mechanical acceptance-test output
the lane mapping artifact
the express DCS directive registry
every external review return incorporated into the convergence ledger
```

An artifact required by an acceptance test SHALL be named and hashed. A test SHALL NOT assert a fact about an artifact that the build is not required to produce and retain.

## 24.3 Source Freeze Manifest

> **Restored in R5 (closes CPR4-002 and CPR4-017).**

The source-freeze manifest SHALL identify, per artifact:

```text
which byte sequence was hashed
the algorithm
the hash class per §24.1
the repository commit
the path
the retrieval timestamp
the artifact size
```

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
    "runtime_surface": "RUNTIME",
    "independence_basis": "INDEPENDENCE_CLASS",
    "validation_result": "APPROVE"
  }
}
```

A pre-validation receipt MAY omit a validator only when its receipt type explicitly states `PRE_VALIDATION`.

No artifact SHALL be represented as independently validated with a null or anonymous validator.

## 25.1 Validator Independence Criteria

> **New in R5 (closes CPR4-016).** R4 stated three times what independence is not (§22, §25, §38.1) and never what it is. The entire evidence model rests on validated receipts, so its central term cannot remain undefined. **This section requires DCS ratification; see §45, item RAT-02.**

A validator satisfies independence when **all** of the following hold:

```text
IC-1  distinct logical agent identity from the executor
IC-2  distinct runtime instance from the executor
IC-3  no shared execution context with the executor for the artifact
      under validation
IC-4  the validator is not the producer of the artifact under validation,
      nor of the evidence offered in its support
IC-5  the validator has independent read access to the acceptance criteria
      as recorded before execution began
```

**Independence classes.** The receipt SHALL record which class applies:

```text
IC_FULL_SEPARATION
  distinct agent, distinct model backend, distinct runtime instance,
  no shared context.

IC_OPERATOR_SCOPED
  distinct agent and runtime instance under a single human operator,
  no shared execution context. This is the ordinary DCSE case for a
  solo-practitioner multi-agent operation.

IC_HUMAN_VALIDATED
  DCS or a designated human validates directly.

IC_INSUFFICIENT
  criteria not met. The receipt SHALL NOT claim independent validation
  and SHALL be typed PRE_VALIDATION.
```

**Ratification question for DCS.** Whether `IC_OPERATOR_SCOPED` is sufficient for a given artifact class is a DCS determination, not a reviewer determination. The default recorded here, pending ratification, is:

```text
GOVERNANCE_DOCUMENT   IC_HUMAN_VALIDATED required
DATABASE_CHANGE       IC_HUMAN_VALIDATED required (per D15 and §38.1)
PUBLIC_UI             IC_HUMAN_VALIDATED required (Agentic Level 1)
BACKEND_SERVICE       IC_OPERATOR_SCOPED sufficient
INTERNAL_UI           IC_OPERATOR_SCOPED sufficient
LOCAL_SCRIPT          IC_OPERATOR_SCOPED sufficient
MEDIA_ASSET           IC_OPERATOR_SCOPED sufficient
COMMUNICATION         IC_OPERATOR_SCOPED sufficient
```

A validator that cannot record an independence class SHALL NOT be recorded as a validator.

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
- the same mandatory rule stated in two sections with non-identical content;
- orphan references;
- missing D01-D22 sections;
- invalid Stop-Gate IDs;
- undefined lanes;
- unmapped runtime lanes;
- PPR or PS firewall violations;
- protected-module entries missing a required machine field;
- deprecated-rule references;
- broken anchors;
- inconsistent human/machine rule IDs;
- unclassified normative rules;
- missing source hashes;
- missing hash-class declaration;
- missing provenance;
- unresolved conflict-ledger entries;
- version/hash mismatch;
- controller-state mismatch;
- ambiguous modal language;
- missing rollback data;
- missing mandatory-runtime activation evidence;
- self-referential acceptance tests;
- dated obligations lacking defined lapse behavior;
- registered directives with status ACTIVE and no incorporation commit;
- revision deltas lacking a §4.5 classification;
- open findings past the disposition window.

The lint output SHALL be produced as a named, hashed artifact per §24.2.

---

# 29. BUILD PIPELINE AND FROZEN DOCTRINE DISPOSITION

Hard dependency sequence:

```text
1. Freeze source inventory and exact hash classes
2. Resolve source identities and lifecycle authority
3. Stop on unresolved CRITICAL source-identity conflicts
4. Extract / retain normative rules
5. Classify rules and modal language
6. Detect duplicates
7. Detect normative conflicts
8. Resolve/disposition conflicts
9. Assign stable machine IDs and human citations
10. Build MP core
11. Compile shared D01-D12 and D15-D22 sections
12. Register D13/D14 as protected modules without shared-body compilation
13. Build governance-domain and runtime-lane registries plus mappings
14. Build capability/toolset/runtime-surface registries
15. Generate provenance and conflict ledger
16. Generate context compiler and reverse-chain diagnostic rules
17. Freeze mandatory-runtime-surface manifest
18. Validate internal references and protected modules
19. Diff against predecessor revision for deleted rules and machine fields;
    classify every delta per §4.7
20. Run governance lint and mechanical build tests
21. Produce and hash all build outputs per §24.2
22. Independent/advisory review as directed by DCS
23. Produce readiness disposition per §31 gate
24. DCS authority designation
25. Verify mandatory runtime activation
26. Atomic authority transition
27. Synchronize remaining evidence/control surfaces
28. Closeout and reconciliation
```

## 29.1 Frozen Doctrine Disposition

```text
D01 RETAIN_LAYER3
D02 RETAIN_LAYER3 + MP reasoning primitive
D03 RETAIN_LAYER3 + SUBSUMED_IN_MP
D04 RETAIN_LAYER3 + SUBSUMED_IN_MP
D05 RETAIN_LAYER3 + SUBSUMED_IN_MP
D06 RETAIN_LAYER3
D07 RETAIN_LAYER3
D08 RETAIN_LAYER3
D09 RETAIN_LAYER3
D10 RETAIN_LAYER3
D11 RETAIN_LAYER3
D12 RETAIN_LAYER3
D13 PROTECTED_MODULE
D14 PROTECTED_MODULE
D15 RETAIN_LAYER3 + SUBSUMED_IN_MP
D16 RETAIN_LAYER3 + SUBSUMED_IN_MP
D17 RETAIN_LAYER3 + SUBSUMED_IN_MP
D18 RETAIN_LAYER3
D19 RETAIN_LAYER3
D20 RETAIN_LAYER3 + SUBSUMED_IN_MP
D21 RETAIN_LAYER3 + SUBSUMED_IN_MP
D22 RETAIN_LAYER3 + SUBSUMED_IN_MP
```

No D01-D22 doctrine is silently dropped.

`PROTECTED_MODULE` means the source identity and firewall are compiled, but protected substantive body content is not placed into the shared controller.

---

# 30. TOKEN / CONTEXT ECONOMY AND BENCHMARK CLASSES

Token economy is an architectural requirement, and it SHALL be benchmarked rather than guessed.

The compiler SHALL measure:

- unconditional Controller Header tokens;
- task governance packet tokens;
- doctrine/rule references selected;
- task/evidence reserve;
- total context occupancy;
- retrieval latency where applicable.

Benchmark classes:

```text
STANDARD   approximately 32k context
EXTENDED   approximately 128k context
MASSIVE    approximately 1M+ context
```

## 30.1 Acceptance Rule

> **Restored in R5 (closes CPR4-007).** R3 §30 carried a normative fit rule enforced by a fit test. In responding to Gemini G-04 on fixed token targets, R4 adopted benchmark classes (correct) and simultaneously downgraded MP72-044 from a fit test to a definition test (an overcorrection). R5 keeps the classes and restores the fit rule, parameterized per class.

> For each defined benchmark class, the Controller Header and the required task governance packet SHALL fit inside that class budget after reserving the approved task/evidence budget, without dropping any mandatory rule dependency.

The Controller Header remains the smallest always-on layer. Layer-3 doctrine sections are progressively disclosed by task, lane, artifact class, and Stop-Gate needs.

No mandatory rule may be deleted solely to meet a token target. Compression SHALL prefer stable references, registries, deduplication, and compiled rule IDs over semantic weakening, and SHALL NOT operate on transitive closure membership per §1.3.

Where closure and budget cannot both be satisfied for a task in a given class, the packet SHALL fail closed and escalate. It SHALL NOT silently truncate.

---

# 31. MECHANICAL ACCEPTANCE AND CUTOVER TESTS

R5 separates **build-readiness tests** from **operative cutover tests**.

## 31.1 Readiness Gate

> **Restored in R5 (closes CPR4-001).** R3 §31 opened with this gate. R4 removed it and substituted a permission stating what `READY` does not require, leaving no rule stating what it does require. R4 then asserted `READY`. The gate is restored here, correctly re-scoped to the build-readiness list only, which is the architecturally sound half of R4's build/cutover split.

**Readiness SHALL NOT become `READY` until every build-readiness test in §31.2 returns PASS or carries a recorded formal disposition.**

Operative cutover tests in §31.3 do not gate readiness. They gate authority transition per §42.

A test result SHALL be recorded in the mechanical acceptance-test output artifact, named and hashed per §24.2. Readiness SHALL NOT be established by assertion in the controller header.

Where build-readiness tests pass but defined findings remain open, readiness is `READY_WITH_FINDINGS` per §4.6.1, and §44 enumerates the open items.

## 31.2 Build-Readiness Tests

```text
MP72-001  D01-D22 inventory complete; no invented D00 dependency
MP72-002  PPR is present in the governance-domain registry and is protected
          with default_load=false and cross_lane_export=false
MP72-003  governance-domain registry matches authoritative source model
MP72-004  runtime-dispatch registry matches frozen v7.1 runtime inventory
MP72-005  runtime lanes map to authority or emit MIGRATION_REQUIRED then Stop-Gate
MP72-006  DCS authority cannot become an autonomous dispatch lane by inference
MP72-007  TSL remains routable without constitutional-lane invention
MP72-008  TRIBUNAL/DDNA/RAG/SYSTEM remain routable
MP72-009  no PS substantive facts in enterprise-shared controller
MP72-010  D13 default_load=false / shared_body_compile=false
MP72-011  D14 default_load=false / shared_body_compile=false
MP72-012  the canonical D17 artifact at the recorded repository path hashes to
          the frozen inventory value; the asset registry records
          hash_verified=true; and the noncanonical path resolves to the
          tombstone at the recorded commit
MP72-013  all D01-D22 have compiler dispositions
MP72-014  D21 runtime responsibilities mapped
MP72-015  D22 authority/distribution/drift mapped
MP72-016  D04 communication states preserved
MP72-017  D05 promotion/rollback controls mapped
MP72-018  D15 database-governance controls mapped
MP72-019  capability-routing/poller boundaries mapped
MP72-020  autonomous and interactive non-claiming classes validate
MP72-021  artifact-security classes mapped
MP72-022  source modes mapped
MP72-023  source lifecycle migration model complete
MP72-024  human/machine rule-ID grammar validates
MP72-025  retired rule, test, Stop-Gate, directive, and finding IDs cannot be
          silently reused
MP72-026  unresolved CRITICAL normative conflicts = 0
MP72-027  compiled normative rules have provenance
MP72-028  doctrine exact-hash/source-hash classes are frozen and each row
          declares its hash class and retrieval basis
MP72-029  Git blob IDs, source checksums, DB body hashes, and SHA-256 are not
          conflated
MP72-030  context compiler fails closed on unresolved lane mapping
MP72-031  context compiler fails closed on missing mandatory dependency
MP72-032  context packets record controller/rule-set identity
MP72-033  validated receipts identify executor and validator separately
MP72-034  interactive receipts do not fabricate autonomous claims
MP72-035  rollback model exists
MP72-036  backward-compatibility policy exists
MP72-037  readiness and authority states remain independent
MP72-038  atomic authority transition requires exact controller identity
MP72-039  runtime-surface manifest frozen and versioned
MP72-041  poller manifest records the active cadence and the 60-minute minimum
          inactivity guarantee, with constitutional guarantees and manifest
          configuration values recorded separately
MP72-042  governance lint contains no unresolved CRITICAL finding
MP72-043  external review ERROR findings corrected or dispositioned
MP72-044  for each defined benchmark class, the measured Controller Header plus
          mandatory task governance packet fits within the class budget after
          reserving the approved task/evidence budget, with zero mandatory rule
          dependencies dropped
MP72-046  review-convergence ledger preserved
MP72-047  Antigravity removed from required review count by DCS
MP72-048  every incorporated external advisory result is retained as a named,
          hashed artifact
MP72-049  interactive context sanitization rejects protected PS injection
MP72-050  material workflows require a governed toolset or TOOLSET_EXCEPTION
MP72-051  paid-plan process knowledge creates portability debt until captured/waived
MP72-052  model/runtime self-check requires evidence
MP72-053  maintenance work is first-class governed work
MP72-054  reverse-chain diagnostic isolates first broken dependency before
          forward remediation
MP72-055  poller actionable events reset the runtime activity window
MP72-060  readiness is not READY unless every build-readiness test returns PASS
          or carries a recorded formal disposition
MP72-061  the build produces immutable hashes for every output listed in §24.2
MP72-062  every incorporated external review return is retained by hash and each
          of its required return items is individually dispositioned
MP72-063  no mandatory rule is stated in two sections with non-identical
          normative content
MP72-064  constitutional timing guarantees are distinguished from manifest
          configuration values, and configuration values are not stated
          normatively in the controller body
MP72-065  no acceptance test asserts its own conclusion
MP72-066  every protected-module registry entry carries default_load,
          cross_lane_export, shared_body_compile, and unauthorized_access_action
MP72-067  the lane-mapping artifact is populated, named, and hashed
MP72-068  every revision-to-revision delta, including every deletion of a
          normative sentence or machine field, carries a §4.5 classification
MP72-069  reverse-chain repair terminates on depth limit or cycle detection and
          emits a Stop-Gate receipt with the dependency graph
MP72-070  validator independence criteria are defined, satisfiable, and recorded
          as an independence class on every validated receipt
MP72-071  the controller contains no dated obligation lacking defined lapse
          behavior
MP72-072  the express DCS directive registry exists, is hashed, and is
          referenced from the authoritative source model
MP72-073  context packet generation records transitive dependency closure and
          the runtime performs a preflight rule-set presence check
```

## 31.3 Operative Cutover Tests

```text
MP72-040  mandatory runtime surfaces acknowledge the operative controller identity
MP72-045  controller version and artifact_sha256 reconcile across GitHub,
          Supabase, host/runtime, and required control surfaces, using the hash
          classes defined in §24.1 without conflation
MP72-056  Windows wake probe starts controller from a durable wake request
          without launching a model when no work exists
MP72-057  active controller remains eligible for at least 60 minutes of
          continuous inactivity before sleep
MP72-058  Dispatch -> claim -> heartbeat -> receipt -> convergence ->
          Results Inbox passes
MP72-059  restart/orphan recovery and rollback evidence passes
```

Build-readiness may be `READY` while operative cutover tests remain pending, because deployment and authority are independent state dimensions. This permission operates only after the §31.1 gate is satisfied; it is not a substitute for it.

---

# 32. REVIEW CONVERGENCE STATE

R5 incorporates five evidence streams:

```text
Review Input A                        formal
Review Input B                        formal
Claude Code R2 independent review     formal
Gemini advisory external inspection   advisory
Claude CP R4 architectural review     promoted to FORMAL REVIEW INPUT by DCS 2026-08-08
```

Antigravity is not required for this convergence cycle by DCS decision.

Corrections retained from the earlier reviews include source-grounding, firewall, D21/D22, lifecycle, rollback, provenance, rule-ID, runtime-class, lane-registry, hash-semantics, and acceptance-test corrections.

Claude's former F-01 lane concern is resolved by the dual registry.

Claude/Gemini's former D17 concern is resolved by canonical source evidence and repository reclassification.

Gemini's required corrections are dispositioned:

```text
G-01 D17 identity conflict:
  RESOLVED

G-02 runtime surface manifest:
  RESOLVED_FOR_BUILD
  runtime activation evidence remains a deployment/cutover gate

G-03 legacy/unmapped execution tags:
  RESOLVED
  MIGRATION_REQUIRED receipt precedes Stop-Gate

G-04 context benchmark targets:
  INTEGRATED_AS_BENCHMARK_CLASSES
  R5 note: the classes are retained; the fit test removed in R4 is restored
  at §30.1 and MP72-044. Adopting the classes did not require removing the
  fit requirement.
```

Gemini's recommended interactive context sanitization test is retained as MP72-049.

Claude CP R4 review return `CPR4-2026-08-08` is incorporated. All 25 findings are closed in the text of this revision. See §43 for the closure register and §44 for outstanding evidence.

---

# 33. EXTERNAL ADVISORY INSPECTIONS

## 33.1 Gemini Inspection

Gemini's advisory external inspection returned:

```text
PASS_WITH_REQUIRED_CORRECTIONS
recommended state at inspection time: NOT_READY
```

That disposition applied to R3.

R4 integrated the material required corrections identified by Gemini. R5 retains them and restores the fit test that R4 removed while integrating G-04.

**Evidence retention requirement.** *(New in R5; closes CPR4-003.)* The Gemini return SHALL be retained as a named, hashed artifact per §24.2, and each item required by the R3 §36 mandate SHALL be individually dispositioned:

```text
per-finding fields (9)          G-01 to G-04 dispositioned in §32
A. top 5 residual risks         DISPOSITION REQUIRED
B. facts Gemini could not verify DISPOSITION REQUIRED
C. apparent overcorrections     DISPOSITION REQUIRED
D. missing acceptance tests     DISPOSITION REQUIRED
E. recommended next state       recorded above
```

Items A through D show no trace in R4 or R5. Either they were returned and not carried forward, or they were not returned against the mandate. Both are recordable facts and one of them is a finding. Status: `UNKNOWN`, open at §44 OE-01.

An external inspection does not designate any controller state.

## 33.2 Claude CP R4 Architectural Review

Return `CPR4-2026-08-08`, 25 findings (3 CRITICAL, 9 ERROR, 11 WARNING, 2 PASS). Posture: **FORMAL REVIEW INPUT**, promoted by DCS on 2026-08-08.

Disposition: `PASS_WITH_REQUIRED_CORRECTIONS`, recommended state `READY_WITH_FINDINGS`.

All findings are closed in R5 text. Three carry outstanding evidence rather than outstanding text; see §44.

---

# 34. CURRENT DISPOSITION

```json
{
  "controller_family": "7.2",
  "candidate_version": "7.2.0-CANDIDATE-R5",
  "predecessor": "7.2.0-CANDIDATE-R4",
  "readiness": "READY_WITH_FINDINGS",
  "authority": "CANDIDATE",
  "deployment": "STAGED",
  "evolution": "CONTROLLED",
  "formal_review_inputs": 4,
  "advisory_inspections": ["GEMINI_CLOSED_INCORPORATED"],
  "promoted_to_formal": ["CPR4_2026-08-08"],
  "antigravity_required": false,
  "open_critical_source_gates": [],
  "review_findings_closed_in_text": 25,
  "evidence_items_produce_at_runtime": 5,
  "dcs_ratification_items_closed": 4,
  "runtime_cutover_gate": "PENDING",
  "operative": false
}
```

R5 is the reconciled v7.2 controller candidate.

`READY_WITH_FINDINGS` means construction is complete and every review finding is closed in the text, with a defined set of build-evidence artifacts outstanding at §44. It does not authorize cutover.

Only DCS may transition `authority` to `OPERATIVE`, and only after the operative cutover requirements are satisfied or expressly dispositioned by DCS within the constitutional boundary.

---

# 35. CONTROLLING PRINCIPLE

**One operative controller.**

**D01-D22 retained as source governance artifacts unless explicitly dispositioned otherwise.**

**MP constitutional rules remain MP rules, not an invented D00 doctrine.**

**Governance/business domains and runtime-dispatch lanes are separate registries connected by explicit mappings.**

**A live runtime lane is not silently deleted because it is not a constitutional business lane.**

**A governance domain is not silently converted into an autonomous dispatch lane.**

**PS and PPR remain protected.**

**D21 execution semantics and D22 distribution authority survive compilation.**

**D17 is fixed as the DART Universal Assurance Methodology; the former Supabase-security mislabel is noncanonical and governed by D15 subject authority.**

**Readiness, authority, deployment, and evolution remain independent, and each transition is defined.**

**Autonomous claiming and interactive directed execution remain distinct runtime classes.**

**Context compilation fails closed, and dependency discovery is closed transitively.**

**Hash semantics are explicit, and unknown semantics fail closed.**

**A control the compiler must evaluate lives in the machine layer, not in prose.**

**No acceptance test asserts its own conclusion.**

**Every normative rule remains traceable to immutable source evidence.**

**Every deletion is classified. No rule leaves silently.**

**Evidence outranks narrative.**

**Independent review validates without stopping authorized remediation.**

**No silent governance mutation.**

**Structure Precedes Scale.**

---

# 36. REVIEW BASELINE

The R3 Gemini inspection mandate is complete and retained in review history.

R5 SHOULD NOT ask another reviewer to rediscover the already resolved D17 identity issue. This is guidance, not a binding constraint, per DCS disposition RAT-03.

Future review of D17 SHOULD begin from these fixed facts:

```text
D17 = DART Universal Assurance Methodology
D15 = Database Administration
D13/D14 = PS-protected DART sources
historical D17 Supabase-security path = noncanonical tombstone
```

A future conflict may be opened only by new evidence showing a governing-source change, hash mismatch, unauthorized mutation, or explicit DCS amendment.

Review activity SHALL focus on new revision deltas, mechanical-test evidence, runtime cutover, and any newly discovered source conflict.

## 36.1 Scope Constraint Safeguard

> **New in R5 (closes CPR4-013).** This section and §24.1 both constrain reviewer behavior. That is defensible and efficient, and it was adopted in R4 before the resolution was mechanically detectable, which left the reopening conditions with no sensor attached.

This section binds review **scope**, not review **authority**. A reviewer who identifies evidence meeting any reopening condition above SHALL raise it, and SHALL NOT treat this section as a bar to doing so.

The reopening conditions are detectable only through MP72-012, which R5 has restated to verify three independent external conditions rather than restate its own conclusion. A scope constraint SHALL NOT be adopted or retained unless the corresponding detector is proven to fail correctly.

---

# 37. CAPABILITY INDEPENDENCE AND TOOLSET OPERATIONS

Paid AI plans and proprietary tools are capability accelerators, not constitutional dependencies.

DCSE owns its governance, prompts/instructions, artifacts, workflow definitions, task state, evidence, DDNA, acceptance criteria, tool-selection logic, and maintenance controls.

Every new material workflow SHALL have:

```text
governed toolset
OR
recorded TOOLSET_EXCEPTION
```

The controller SHALL select capabilities by task need, lane, security, availability, evidence history, quality, cost, portability, and validation needs rather than by vendor identity alone.

Initial toolset classes include:

```text
TS_IDEA_TO_OPERATIVE
TS_CODE_BUILD_TRIAD
TS_RESEARCH_DDNA
TS_PRODUCT_BUILD
TS_CONTENT_CAMPAIGN
TS_KNOWLEDGE_DOCUMENT
TS_MAINTENANCE_SELF_CHECK
TS_PORTABILITY_EXIT
```

## 37.1 Portability Obligation

> **Corrected in R5 (closes CPR4-014).** R4 embedded a hard date ("By 2026-10-03 DCSE SHALL test continuity...") in constitutional doctrine with no defined behavior on lapse. On the day the date passes untested, the controller contains a false normative statement and no rule says whether that is a lint ERROR, a Stop-Gate, a readiness regression, or nothing.

DCSE SHALL maintain and periodically evidence workflow-level continuity of its defined core workflows without relying on OpenAI or Claude paid-plan-only paths.

The **target date and review cadence** are operational values recorded in the runtime manifest, not constitutional values. The current recorded target is 2026-10-03.

**Lapse behavior.** If a recorded portability target passes without evidence:

```text
the governance linter SHALL raise a WARNING
the item SHALL be surfaced to DCS for disposition
DCS SHALL either record new evidence, set a new target,
  or record an express waiver
readiness SHALL NOT change automatically
```

This is workflow-level parity, not a requirement that one open model equal every frontier model capability.

Completed material work SHALL be evaluated for reusable-process/DDNA extraction.

---

# 38. INFRASTRUCTURE CONTROL LAYERS

The execution ecosystem SHALL include explicit infrastructure disciplines beneath agent/tool selection.

## 38.1 DBA / Data Plane

D15 governs:

```text
schema and migration authority
RLS and access control
data contracts
integrity and data quality
query/performance observability
Realtime/RPC/data-service boundaries
backup/restore/rollback
retention and lifecycle
schema drift
independent validation
```

A code-writing agent may prepare database work but does not automatically become the sole independent validator. Whether a given validator qualifies is determined by the independence criteria and classes in §25.1. `DATABASE_CHANGE` currently defaults to `IC_HUMAN_VALIDATED`, pending DCS ratification per §45 RAT-02.

## 38.2 Repository / Git Lifecycle

Workers SHALL use a governed lifecycle:

```text
status
fetch
inspect remote/base
branch or worktree
edit
test
atomic evidence-bearing commit
fetch/reconcile
retest
push when handoff/review/CI/backup requires
PR/review
merge
post-merge reconciliation
```

Blind pull/overwrite is prohibited.

Receipts SHALL bind durable work to the exact commit and tests actually run.

## 38.3 Deployment, Observability, and Recovery

Runtime/deployment work SHALL record:

```text
deployed identity
health
logs/telemetry
dependency state
rollback
restart/recovery
drift
post-deploy validation
```

A dashboard warning without remediation ownership is not a maintenance strategy.

---

# 39. SESSION POLLER AND CLAUDE COMMUNICATION (EXPLANATORY)

> **Reduced to explanatory in R5 (closes CPR4-005).** R4 stated the poller contract normatively in both §6.1 and §39 with non-identical actionable-event lists (six items versus eight). Two compliant implementations would diverge. §6.1 is now the single normative statement. This section explains it and adds no normative content.

The neutral controller is a session runtime. The normative contract is §6.1.

DCS operational instructions intended for autonomous Claude execution SHALL be represented through the governed task/poller/receipt path rather than an untracked direct-session instruction. This is the one normative rule retained in this section, because it governs communication routing rather than poller timing.

Explanatory summary of §6.1:

- Control Plane wake and activity sources are enumerated at §6.1.4.
- An actionable event resets the inactivity window (§6.1.1).
- The lightweight wake probe checks for actionable work and durable wake requests and does not invoke a model when no work exists (§6.1.1).
- The neutral controller may stop after not less than 60 continuous minutes of verified inactivity (§6.1.1, §6.1.3).
- Timing configuration values are held in the runtime manifest (§6.1.2).

This session design provides responsive execution without requiring 24/7 model processes.

---

# 40. REVERSE-CHAIN DIAGNOSTIC ENGINE

For gap analysis and troubleshooting, the controller SHALL support reverse diagnosis in addition to D01/D02 forward/backward reasoning.

Sequence:

```text
Required Goal State
  | reverse
Required Acceptance Evidence
  |
Required State
  |
Required Transition
  |
Responsible Component / Agent / Tool
  |
Dependencies
  |
FIRST dependency not VERIFIED
```

The system then:

```text
classify VERIFIED / LIKELY / UNKNOWN / ASSUMPTION
repair the smallest bounded broken edge
forward-chain the correction
re-run the reverse proof
continue until a termination condition in §40.2 is met
```

The diagnostic engine SHALL prefer the earliest broken dependency over broad speculative troubleshooting.

## 40.2 Repair Loop Termination

> **New in R5 (closes CPR4-015).** R4 §40 instructed the loop to "continue until goal-state evidence closes," which is unbounded by construction. Negative case: A is missing; repairing A surfaces B; repairing B surfaces C; C depends on A. The loop runs indefinitely, consuming budget under §37 cost controls with no receipt, because no termination event exists to receipt.

The repair loop SHALL terminate when any of the following is true:

```text
T-1  every dependency is VERIFIED and goal-state evidence closes
T-2  the repair depth limit is reached
T-3  a dependency cycle is detected
T-4  a Stop-Gate is triggered by the repair itself
```

On T-2, T-3, or T-4 the engine SHALL emit a Stop-Gate receipt containing:

```text
the dependency graph as resolved
the repair depth reached
the termination condition
the last VERIFIED dependency
the first dependency not VERIFIED
```

The repair depth limit is a manifest configuration value per §6.1.2. The **existence** of a limit is a constitutional guarantee.

A terminated repair loop is a governed outcome, not a failure. It escalates; it does not retry silently.

---

# 41. BUILD CONFIRMATION RECORD

R5 construction is confirmed on the following basis:

```text
D01-D22 source identities inventoried
D13/D14 protected-source treatment explicit, with full machine fields restored
D17 identity conflict closed, with a non-self-referential regression detector
D15 database authority preserved
D21 runtime engine preserved
D22 source/distribution authority preserved
dual governance/runtime lane model retained, with mappings populated
Gemini required corrections incorporated, with the G-04 fit test restored
CPR4 review findings closed in text: 25 of 25
runtime-surface requirements manifest frozen
60-minute minimum poller inactivity guarantee retained as constitutional
poller configuration values relocated to the runtime manifest
toolset/capability independence retained, dated obligation converted to durable
reverse-chain diagnostic primitive completed with termination criteria
readiness gate restored
immutable build-output hash production restored
state transition rules defined for all four dimensions
no DCS operative transition inferred
```

Construction completion does not equal deployment completion.

Host runtime implementation, wake-probe installation, end-to-end dispatch evidence, runtime reconciliation, and atomic operative cutover remain deployment/authority activities.

**Construction completion also does not equal evidence completion.** §44 enumerates the artifacts that must exist before readiness advances to `READY`.

---

# 42. DCS OPERATIVE GATE

R5 becomes the controlling enterprise Master Profile only when DCS records an operative designation that binds:

```text
exact R5 artifact hash
exact repository commit/path
effective timestamp
superseded controller identity
runtime manifest identity
lane mapping artifact identity
cutover disposition
rollback target
```

The operative transition SHALL be atomic in governance state, per §4.6.2 and §5.

Until then:

```text
v7.1      = controlling authority
v7.2 R5   = READY_WITH_FINDINGS candidate
```

No model, repository commit, Supabase row, deployment, review result, or version number independently changes that authority.

---

# 43. FINDING CLOSURE REGISTER

Closure of Claude CP review return `CPR4-2026-08-08`. A finding is closed when the closing change exists in this text with a stated section. Findings whose closure additionally requires an artifact are marked and carried at §44.

| Finding | Severity | Closing Section | Closure Type | Evidence Outstanding |
|---|---|---|---|---|
| CPR4-001 | CRITICAL | §31.1, MP72-060 | Rule restored | OE-02 (test output) |
| CPR4-002 | CRITICAL | §24.2, §24.3, MP72-061 | Rule restored | OE-02 |
| CPR4-003 | CRITICAL | §33.1, MP72-062 | Rule added | OE-01 (Gemini return) |
| CPR4-004 | ERROR | §6.1.1, §6.1.2, §18.2, MP72-064 | Contradiction resolved | none |
| CPR4-005 | ERROR | §6.1.4, §39, MP72-063 | Duplication resolved | none |
| CPR4-006 | ERROR | §31.2 MP72-012, §11.4, MP72-065 | Test restated | none |
| CPR4-007 | ERROR | §30.1, MP72-044 | Fit rule restored | none |
| CPR4-008 | ERROR | §12, §7 Layer 4 rule, MP72-066 | Machine fields restored | none |
| CPR4-009 | ERROR | §11.3, MP72-067 | Mapping populated | OE-03 (artifact hash) |
| CPR4-010 | ERROR | §31.3 MP72-045 | Test restated | none |
| CPR4-011 | ERROR | §0 item 11, §4.7, MP72-068 | Classification added | none |
| CPR4-012 | ERROR | §2.3.1 | Machine form restored | none |
| CPR4-013 | WARNING | §36.1, §24.1 safeguard | Safeguard added | RAT-03 |
| CPR4-014 | WARNING | §37.1, MP72-071 | Obligation converted | none |
| CPR4-015 | WARNING | §40.2, MP72-069 | Termination defined | none |
| CPR4-016 | WARNING | §25.1, §38.1, MP72-070 | Criteria defined | RAT-02 |
| CPR4-017 | WARNING | §2.2.1, MP72-028 | Requirement added | OE-05 (per-row data) |
| CPR4-018 | WARNING | §2.2 | Normative rule restored | none |
| CPR4-019 | WARNING | §31.2 MP72-002 | Test restored | none |
| CPR4-020 | WARNING | §24.1, §20 | Class reinstated | none |
| CPR4-021 | WARNING | §4.6 | Transitions defined | none |
| CPR4-022 | WARNING | §1.3, §23, §30.1, MP72-073 | Contract defined | none |
| CPR4-023 | WARNING | §2.4, §1.1, MP72-072 | Registry defined | OE-04 (registry artifact) |
| CPR4-024 | INFO | §32, §34 | Confirmed correct, retained | none |
| CPR4-025 | INFO | §9, §31 | Confirmed correct, extended | none |

**Closed in text: 25 of 25.**
**Requiring artifact evidence before readiness advances: 5.**
**Requiring DCS ratification: 4 (see §45).**

---

# 44. OPEN EVIDENCE ITEMS AND READINESS EXIT CRITERIA

Readiness is `READY_WITH_FINDINGS`. Per §4.6.1, it advances to `READY` when every item below is produced at runtime and the §31.2 suite is re-run. DCS has dispositioned all five items as `PRODUCE_AT_RUNTIME` (2026-08-08). These are agent-producible build artifacts, not manual paperwork.

| ID | Item | Required By | Closes | Status |
|---|---|---|---|---|
| OE-01 | Gemini return retained as a named, hashed artifact, with mandate items A, B, C, D individually dispositioned | §33.1, MP72-062 | CPR4-003 | PRODUCE_AT_RUNTIME |
| OE-02 | Governance lint output and mechanical acceptance-test output produced as named, hashed artifacts | §24.2, MP72-061, MP72-042 | CPR4-001, CPR4-002 | PRODUCE_AT_RUNTIME |
| OE-03 | `lane_mappings.v7.2.r5.json` produced and hashed from §11.3 | §11.3, MP72-067 | CPR4-009 | PRODUCE_AT_RUNTIME |
| OE-04 | `dcs_express_directives.v7.2.json` produced and hashed | §2.4, MP72-072 | CPR4-023 | PRODUCE_AT_RUNTIME |
| OE-05 | Per-doctrine hash class and retrieval basis recorded for D01 through D21 | §2.2.1, MP72-028 | CPR4-017 | PRODUCE_AT_RUNTIME |

**Note on OE-01 and OE-02.** If these artifacts already exist and were simply not surfaced to the review, closure is a documentation action rather than an engineering one. The distinction matters for scheduling, not for the gate.

**Note on the disposition path.** Any item above MAY instead be closed by an express DCS disposition recorded per §2.4, in which case readiness may advance with the disposition on record. That is the "or carries a recorded formal disposition" branch of the §31.1 gate, and it is DCS's to exercise.

---

# 45. DCS RATIFICATION ITEMS

Four decisions in R5 belong to DCS and were not made by the reviewer. Each is recorded with the reviewer's default so that R5 is operable in the interim, and each default is reversible.

| ID | Item | Reviewer Default in R5 | DCS Decision Required |
|---|---|---|---|
| RAT-01 | Authority posture of review return `CPR4-2026-08-08` | ADVISORY | **PROMOTED TO FORMAL REVIEW INPUT** by DCS 2026-08-08 |
| RAT-02 | Validator independence: is `IC_OPERATOR_SCOPED` sufficient, and for which artifact classes | Defaults in §25.1 | **DEFAULTS ACCEPTED** by DCS 2026-08-08 |
| RAT-03 | Reviewer scope constraints at §24.1 and §36 | Retained with §36.1 safeguard | **DOWNGRADED TO GUIDANCE** by DCS 2026-08-08. SHALL NOT changed to SHOULD NOT in §24.1 and §36. |
| RAT-04 | Readiness posture of R5 | `READY_WITH_FINDINGS` | **READY_WITH_FINDINGS ACCEPTED** by DCS 2026-08-08. Evidence items at §44 set to PRODUCE_AT_RUNTIME. |

All four ratification items are closed by DCS disposition.

---

**END OF CONTROLLER**
