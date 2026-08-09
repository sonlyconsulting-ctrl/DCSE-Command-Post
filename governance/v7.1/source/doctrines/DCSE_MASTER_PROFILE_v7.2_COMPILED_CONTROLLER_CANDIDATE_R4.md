# DCSE MASTER PROFILE v7.2
## Compiled Governance Controller — Build-Complete Candidate R4

**Artifact Class:** Enterprise Governance Controller  
**Controller Family:** DCSE Master Profile 7.2  
**Candidate Revision:** 7.2.0-CANDIDATE-R4  
**Authority:** DCS  
**Current Authority State:** CANDIDATE  
**Readiness State:** READY  
**Deployment State:** STAGED  
**Evolution State:** CONTROLLED  
**Architecture Principle:** Structure Precedes Scale  
**Execution Model:** Goal-State Orchestration + Forward/Backward/Reverse-Chain Resolution  
**Integration Basis:** v7.1 authoritative Master Profile and doctrine corpus; two original independent review inputs; Claude Code R2 independent review; Gemini advisory external inspection; DCS-directed v7.2 capability/toolset, infrastructure, and session-poller corrections.  
**D17 Reconciliation Commit:** `98d3c6ccf1765a4aa5e9bfc0134a078696e011c8`  
**Runtime Surface Manifest:** `runtime_surface_manifest.v7.2.r4.json`  
**Runtime Manifest SHA-256:** `45a504d8195656758cada4834c4d67fa049b3070520ac9651a5bb2f774fe466a`  
**Important:** `READY` means the controller construction/source-validation gate has passed. It does **not** make v7.2 OPERATIVE. DCS retains the authority transition. Runtime activation remains a separate deployment/cutover gate.

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

D22's SHA-256 above is the R4 direct hash of the canonical v7.1 source bytes used for compilation.

## 2.3 Source Status and Compiled Authority

Source lifecycle, compiled inclusion, controller readiness, controller authority, and deployment remain independent.

A source record may be promoted-with-known-gaps and still be retained with those gaps visible. Compilation does not silently upgrade the source's historical status.

The controller SHALL preserve both:

```text
source provenance
compiled rule provenance
```

and SHALL never infer authority from file existence, repository version number, database presence, or model memory.

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

```text
active poll interval             60 seconds
wake-probe interval candidate     5 minutes
minimum continuous inactivity    60 minutes
```

The 60-minute inactivity value is a DCS minimum. A runtime may remain active longer. It may not automatically reduce the minimum below 60 minutes without DCS authority.

The active controller may sleep only after at least 60 continuous minutes in which all are true:

```text
no claimable assignments
no running workers
no pending recovery
no unconsumed wake request
no actionable event/dispatch activity
```

Actionable Control Plane activity includes task assignment, DCS instruction, review completion, result submission, handoff-ready events, and operational comments requiring action.

A wake probe SHALL NOT launch a model when no work exists.

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

# 11. DUAL LANE REGISTRY AND MAPPING

R2 conflated two different concepts that the reviews exposed:

1. **Governance / business lanes** defined by the Master Profile and doctrine firewall.
2. **Runtime dispatch lanes** actually used by the v7.1 control plane.

v7.2 SHALL keep them separate and SHALL require an explicit mapping.

## 11.1 Governance / Business Domain Registry

The source-governance inventory identified in the prior reviews includes:

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

## 11.3 Mapping Requirement

The compiler SHALL maintain:

```json
{
  "governance_domains": [],
  "runtime_dispatch_lanes": [],
  "lane_mappings": []
}
```

Each runtime lane SHALL map to controlling governance authority without silently redefining the constitutional lane model.

Required migration dispositions include:

```text
DCS:
  authority identity; no autonomous dispatch lane by default.

INFRA/TECH:
  governance domain; runtime implementation may map to SYSTEM only when source/evidence supports that mapping.

TRIBUNAL / DDNA / RAG / SYSTEM:
  runtime technical lanes; retain operationally while their controlling governance parent/authority is recorded.

TSL:
  existing live runtime/product lane; retain during migration. It SHALL NOT be deleted by fail-closed compilation merely because it was not a constitutional lane in an earlier source inventory.

TI:
  retain as a governance domain where supported by the Master Profile; absence of a live dispatch lane does not delete the governance domain.

FAMILY:
  not promoted to a constitutional enterprise lane by this candidate. Family products remain governed product domains until separately authorized.
```

Unknown or conflicting lane mappings SHALL first emit a `MIGRATION_REQUIRED` receipt containing the legacy value, attempted mapping, controlling source, and remediation route. If no safe mapping is verified, execution then enters `LANE_MAPPING_STOP_GATE`.

This migration receipt prevents silent rejection of legacy/in-flight tags while preserving fail-closed behavior. It SHALL NOT authorize an unknown lane.

## 11.4 Test Rule

MP72-003 SHALL compare the compiled governance registry against the authoritative source inventory **and** compare the runtime dispatch registry against the frozen live control-plane inventory. A self-referential test against R4's own list is prohibited.

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
      "shared_body_compile": false
    },
    "D14": {
      "title": "DART PS Protected & Litigation Blueprints",
      "lane": "PS",
      "classification": "PS-PROTECTED",
      "default_load": false,
      "shared_body_compile": false
    },
    "PPR": {
      "classification": "PROTECTED",
      "default_load": false,
      "cross_lane_export": false
    }
  }
}
```

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

# 17. D17 UNIVERSAL DART AND D15 DATABASE GOVERNANCE — SOURCE CONFLICT CLOSED

## 17.1 D17 Identity — RESOLVED

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

MP72-012 is satisfied.

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
- independent validation when required.

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

The exact scheduler interval, heartbeat interval, wall-time limit, and health-monitor interval SHALL be recorded in the operative runtime manifest with provenance to the verified implementation and DCS-approved operational policy.

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
```

The build verified that current `governance_directives.checksum` values are not hashes of the database `body` field. The controller therefore preserves them as `promoted_source_checksum` rather than mislabeling them as body or file hashes.

Exact artifact SHA-256 values are frozen in the doctrine inventory for D01-D22. Protected D13/D14 hashes may be visible as provenance but their bodies remain excluded from shared runtime context.

A reviewer SHALL NOT reopen a source identity conflict merely because two different documented hash classes differ.

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
19. Run governance lint and mechanical build tests
20. Independent/advisory review as directed by DCS
21. Produce readiness disposition
22. DCS authority designation
23. Verify mandatory runtime activation
24. Atomic authority transition
25. Synchronize remaining evidence/control surfaces
26. Closeout and reconciliation
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

Token economy is an architectural requirement, but it SHALL be benchmarked rather than guessed.

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

For each class, acceptance testing SHALL demonstrate that mandatory governance can coexist with a useful task/evidence reserve.

The Controller Header remains the smallest always-on layer. Layer-3 doctrine sections are progressively disclosed by task, lane, artifact class, and Stop-Gate needs.

No mandatory rule may be deleted solely to meet a token target. Compression SHALL prefer stable references, registries, deduplication, and compiled rule IDs over semantic weakening.

---

# 31. MECHANICAL ACCEPTANCE AND CUTOVER TESTS

R4 separates **build-readiness tests** from **operative cutover tests**.

### Build-readiness tests

```text
MP72-001  D01-D22 inventory complete; no invented D00 dependency
MP72-002  PPR protection present
MP72-003  governance-domain registry matches authoritative source model
MP72-004  runtime-dispatch registry matches frozen v7.1 runtime inventory
MP72-005  runtime lanes map to authority or emit MIGRATION_REQUIRED then Stop-Gate
MP72-006  DCS authority cannot become an autonomous dispatch lane by inference
MP72-007  TSL remains routable without constitutional-lane invention
MP72-008  TRIBUNAL/DDNA/RAG/SYSTEM remain routable
MP72-009  no PS substantive facts in enterprise-shared controller
MP72-010  D13 default_load=false / shared_body_compile=false
MP72-011  D14 default_load=false / shared_body_compile=false
MP72-012  canonical D17 resolves to DART Universal Assurance Methodology
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
MP72-025  retired rule IDs cannot be silently reused
MP72-026  unresolved CRITICAL normative conflicts = 0
MP72-027  compiled normative rules have provenance
MP72-028  doctrine exact-hash/source-hash classes are frozen
MP72-029  Git blob IDs, source checksums, DB body hashes, and SHA-256 are not conflated
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
MP72-041  poller manifest records 60s active cadence and 60-minute minimum inactivity
MP72-042  governance lint contains no unresolved CRITICAL finding
MP72-043  Gemini ERROR findings corrected or dispositioned
MP72-044  controller packet benchmark classes defined
MP72-046  review-convergence ledger preserved
MP72-047  Antigravity removed from required review count by DCS
MP72-048  Gemini advisory result recorded
MP72-049  interactive context sanitization rejects protected PS injection
MP72-050  material workflows require a governed toolset or TOOLSET_EXCEPTION
MP72-051  paid-plan process knowledge creates portability debt until captured/waived
MP72-052  model/runtime self-check requires evidence
MP72-053  maintenance work is first-class governed work
MP72-054  reverse-chain diagnostic isolates first broken dependency before forward remediation
MP72-055  poller actionable events reset the runtime activity window
```

### Operative cutover tests

```text
MP72-040  mandatory runtime surfaces acknowledge the operative controller identity
MP72-045  controller identity reconciles across GitHub, Supabase, host/runtime, and required control surfaces
MP72-056  Windows wake probe starts controller from a durable wake request without launching a model when no work exists
MP72-057  active controller remains eligible for at least 60 minutes of continuous inactivity before sleep
MP72-058  Dispatch -> claim -> heartbeat -> receipt -> convergence -> Results Inbox passes
MP72-059  restart/orphan recovery and rollback evidence passes
```

Build-readiness may be `READY` while operative cutover tests remain pending, because deployment and authority are independent state dimensions.

---

# 32. REVIEW CONVERGENCE STATE

R4 incorporates four evidence streams:

```text
Review Input A
Review Input B
Claude Code R2 independent review
Gemini advisory external inspection
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
  INTEGRATED_AS_ADVISORY_BENCHMARK_CLASSES
```

Gemini's recommended interactive context sanitization test is added as MP72-049.

---

# 33. GEMINI INSPECTION — CLOSED AND INCORPORATED

Gemini's advisory external inspection returned:

```text
PASS_WITH_REQUIRED_CORRECTIONS
recommended state at inspection time: NOT_READY
```

That disposition applied to R3.

R4 integrates the material required corrections identified by Gemini:

- D17 source identity is resolved;
- the misleading D17 database-security path is reclassified;
- the runtime-surface manifest is frozen;
- unmapped legacy tags emit `MIGRATION_REQUIRED`;
- context benchmark classes are defined;
- interactive PS-context sanitization is added to mechanical testing.

The Gemini inspection is therefore **CLOSED AS INCORPORATED ADVISORY EVIDENCE**.

It does not itself designate R4 OPERATIVE.

---

# 34. CURRENT DISPOSITION — BUILD COMPLETE

```json
{
  "controller_family": "7.2",
  "candidate_version": "7.2.0-CANDIDATE-R4",
  "readiness": "READY",
  "authority": "CANDIDATE",
  "deployment": "STAGED",
  "evolution": "CONTROLLED",
  "formal_review_inputs": 3,
  "external_advisory_inspection": "GEMINI_CLOSED_INCORPORATED",
  "antigravity_required": false,
  "open_critical_source_gates": [],
  "runtime_cutover_gate": "PENDING",
  "operative": false
}
```

R4 is the build-complete v7.2 controller candidate.

`READY` means its source/construction gate is complete. It does not authorize cutover.

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

**Readiness, authority, deployment, and evolution remain independent.**

**Autonomous claiming and interactive directed execution remain distinct runtime classes.**

**Context compilation fails closed.**

**Hash semantics are explicit.**

**Every normative rule remains traceable to immutable source evidence.**

**Evidence outranks narrative.**

**Independent review validates without stopping authorized remediation.**

**No silent governance mutation.**

**Structure Precedes Scale.**

---

# 36. REVIEW BASELINE AFTER GEMINI

The R3 Gemini inspection mandate is complete and retained in review history.

R4 SHALL NOT ask another reviewer to rediscover the already resolved D17 identity issue.

Future review of D17 SHALL begin from these fixed facts:

```text
D17 = DART Universal Assurance Methodology
D15 = Database Administration
D13/D14 = PS-protected DART sources
historical D17 Supabase-security path = noncanonical tombstone
```

A future conflict may be opened only by new evidence showing a governing-source change, hash mismatch, unauthorized mutation, or explicit DCS amendment.

Review activity SHALL focus on new R4 deltas, mechanical-test evidence, runtime cutover, and any newly discovered source conflict.

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

By 2026-10-03 DCSE SHALL test continuity of its defined core workflows without relying on OpenAI or Claude paid-plan-only paths.

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

A code-writing agent may prepare database work but does not automatically become the sole independent validator.

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

# 39. SESSION POLLER, EVENT WAKE, AND CLAUDE COMMUNICATION

The neutral controller is a session runtime.

DCS operational instructions intended for autonomous Claude execution SHALL be represented through the governed task/poller/receipt path rather than an untracked direct-session instruction.

Control Plane wake/activity sources include:

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

An actionable event resets the 60-minute inactivity window.

The lightweight wake probe checks for actionable work and durable wake requests. It does not invoke a model when no work exists.

The neutral controller may stop after **not less than 60 continuous minutes** of verified inactivity.

This session design provides responsive execution without requiring 24/7 model processes.

---

# 40. REVERSE-CHAIN DIAGNOSTIC ENGINE

For gap analysis and troubleshooting, the controller SHALL support reverse diagnosis in addition to D01/D02 forward/backward reasoning.

Sequence:

```text
Required Goal State
  ↓ reverse
Required Acceptance Evidence
  ↓
Required State
  ↓
Required Transition
  ↓
Responsible Component / Agent / Tool
  ↓
Dependencies
  ↓
FIRST dependency not VERIFIED
```

The system then:

```text
classify VERIFIED / LIKELY / UNKNOWN / ASSUMPTION
repair the smallest bounded broken edge
forward-chain the correction
re-run the reverse proof
continue until goal-state evidence closes
```

The diagnostic engine SHALL prefer the earliest broken dependency over broad speculative troubleshooting.

---

# 41. BUILD CONFIRMATION RECORD

R4 construction is confirmed on the following basis:

```text
D01-D22 source identities inventoried
D13/D14 protected-source treatment explicit
D17 identity conflict closed
D15 database authority preserved
D21 runtime engine preserved
D22 source/distribution authority preserved
dual governance/runtime lane model retained
Gemini required corrections incorporated
runtime-surface requirements manifest frozen
60-minute minimum poller inactivity rule incorporated
toolset/capability independence incorporated
reverse-chain diagnostic primitive incorporated
no DCS operative transition inferred
```

Construction completion does not equal deployment completion.

Host runtime implementation, wake-probe installation, end-to-end dispatch evidence, runtime reconciliation, and atomic operative cutover remain deployment/authority activities.

---

# 42. DCS OPERATIVE GATE

R4 becomes the controlling enterprise Master Profile only when DCS records an operative designation that binds:

```text
exact R4 artifact hash
exact repository commit/path
effective timestamp
superseded controller identity
runtime manifest identity
cutover disposition
rollback target
```

The operative transition SHALL be atomic in governance state.

Until then:

```text
v7.1 = controlling authority
v7.2 R4 = READY candidate
```

No model, repository commit, Supabase row, deployment, review result, or version number independently changes that authority.
