# DCSE v7.2 Runtime Harmony, Task Traceability, and Navigable Closeout Directive

**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Authority:** DCS Level 0  
**Original Effective Date:** 2026-09-05  
**Amended Effective Date:** 2026-09-10  
**Lane:** DCSE Governance  
**Original Directive ID:** DCS-DIR-20260905-001  
**Amendment Directive ID:** DCS-DIR-20260910-001  
**Canonical File:** DCSE_Runtime_Harmony_Task_Traceability_and_Navigable_Closeout_v7-2.md

## Purpose

Correct runtime drift across model and agent surfaces by enforcing the operative DCSE Master Profile v7.2 R5 authority, requiring mandatory task traceability at intake, requiring evidence-backed navigable closeout at completion, and preserving DCS control over subsequent work prioritization.

This directive establishes a mirrored lifecycle contract:

`INTAKE -> EXECUTION -> VALIDATION -> CLOSEOUT -> NAVIGABLE EVIDENCE -> NEXT-WORK PRIORITY`

The intake declaration and final closeout are two ends of the same governed transaction. A substantive task is not properly governed if either end is missing.

## 1. Operative Authority

`DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md` is OPERATIVE under `DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md` and its DCS authority designation.

Any embedded `CANDIDATE-R5` label in the controller is build-stage provenance only and does not reduce the controller's current OPERATIVE authority.

Compiled v7.2 rules with status `ACTIVE_IF_AUTHORIZED` are enforced through the operative R5 controller when routed to a task. Historical source-state labels remain provenance and do not defeat authority inherited from the operative controller or an active registered DCS directive.

## 2. Mandatory Task Traceability and Intake Declaration

Every substantive task SHALL establish, before execution:

- task ID;
- lane and entity;
- task type and destination;
- requested action and artifact type;
- authority holder and authority source;
- executing model or agent;
- systems and access level;
- secret exposure;
- PS exposure;
- approval requirement;
- rollback or recovery requirement where applicable;
- expected deliverables;
- exit criteria.

Every substantive task SHALL surface a concise `Preflight Validation` record before execution and SHALL produce or preserve the D21 Doctrine Consideration Log before closeout.

A handoff between models, agents, tools, or runtimes SHALL preserve the originating task ID. A child task may receive a new task ID only when it records the parent task ID and preserves the authority and source chain.

A task that cannot establish the required declaration is `BLOCKED` or `PARTIAL`; it SHALL NOT silently proceed as v7.2 compliant.

## 3. Mandatory Navigable Final Reporting and Closeout

Every substantive DCSE closeout SHALL provide a concise final report that is both human-readable and directly navigable to the available evidence surfaces.

The final report SHALL state:

1. **What was accomplished.** Identify the requested outcome and the actual completed outcome.
2. **What changed.** Identify material changes to artifacts, runtime state, governance, dependencies, architecture, configuration, or commitments.
3. **Goal status.** State whether the governing goal remains unchanged, shifted, narrowed, expanded, blocked, or completed.
4. **Goal-change reasoning.** If the goal changed, state what changed and why. If it did not change, state why the original goal remains valid when that determination is material to subsequent work.
5. **Evidence and direct navigation.** Provide direct links or resolvable references, where available and authorized, to the applicable canonical GitHub artifact/commit/PR/issue, Supabase registry or runtime record, Tribunal receipt/evidence packet, Command Post view, ESCD work item, deployment/preview, related doctrine, and rollback/history record.
6. **Validation status.** Distinguish VERIFIED, PARTIAL, BLOCKED, DRIFT, UNKNOWN, or other governed states. Do not represent evidence that was not actually checked as verified.
7. **Unresolved dependencies or findings.** Surface only material unresolved items and identify whether they block the next action.
8. **Recommended next body of work.** Rank the next reasonable work item or compact work set using current evidence, dependencies, urgency, leverage, time-to-market, business/revenue value, reuse potential, risk reduction, and readiness.

Final reporting SHALL comply with the active Completion Evidence Collector and Closure Integrity requirements. The navigable closeout requirement complements those controls by making the evidence immediately usable from desktop, tablet, mobile, Command Post, ESCD, or another approved application surface.

Where a direct link cannot be generated, provide the most specific governed locator available, such as repository + path + commit SHA, project/schema/table + record key, Tribunal receipt identifier, deployment ID, or ESCD work-item ID.

Secret values, private credentials, hidden access architecture, and unauthorized protected material SHALL NOT be embedded in closeout links or reports.

## 4. ESCD Next-Work Prioritization and DCS Interruption Control

At substantive closeout, ESCD or the controlling orchestration surface SHOULD generate a default ranked next-work recommendation when meaningful work remains.

The default prioritization order is:

1. critical governance, security, authority, or integrity defects;
2. blockers whose resolution unlocks multiple downstream items;
3. revenue or materially strategic work already in motion;
4. high-leverage reusable capability work;
5. committed projects with dependencies or deadlines;
6. maintenance, cleanup, backlog, and optimization;
7. exploratory work.

This categorical order is not absolute. Each candidate SHALL be evaluated against relevant evidence including:

- business or mission value;
- urgency and deadline;
- dependency impact;
- time-to-market;
- revenue relevance;
- reuse and composability;
- risk reduction;
- effort and readiness;
- evidence quality;
- opportunity cost;
- whether another committed item is waiting on it.

The recommended next-work state SHALL support at minimum:

`CONTINUE | SKIP | DEFER | REORDER | INTERRUPT`

DCS retains Level 0 authority to select, skip, defer, reorder, or interrupt the recommended sequence at any time. An interruption does not invalidate the prior ranking; it creates a new controlling priority decision and SHALL be reflected in the subsequent task intake record.

ESCD SHALL NOT silently reinterpret a DCS-defined goal. Goal shifts must be explicit and attributable.

## 5. Model and Agent Harmony

All governed model and agent surfaces SHALL resolve authority from the same operative chain:

1. R5 operative designation;
2. DCSE Master Profile v7.2 R5;
3. `dcs_express_directives.v7.2.json`;
4. D22 source and authority reconciliation;
5. D21 doctrine routing and task declaration;
6. this task-traceability and navigable-closeout directive;
7. universal onboarding/access controls;
8. task-routed doctrines and assignment.

No model or agent may self-assign constitutional authority, invent a permanent role, silently waive preflight, silently waive closeout, or substitute its own summary for the operative authority chain.

A surface that cannot load or verify this chain SHALL report `UNSYNCHRONIZED` or `DEGRADED` and SHALL NOT claim full v7.2 compliance for authority-sensitive work.

## 6. Persistence and Evidence Routing

The final report SHALL use the operative v7.2 D22 persistence model rather than allowing each model or agent to invent a destination.

- **GitHub:** versioned canonical artifacts and governed source.
- **DCSE-DDNA Supabase:** constitutional runtime authority, artifact, provenance, relationship, lifecycle, and structured DDNA registry/state.
- **SC Command Post Supabase:** operational/application state with governed references to DCSE authority.
- **Tribunal:** governance-significant decisions, validation, promotion, exceptions, reconciliation, and closeout evidence.
- **Object Storage:** large or binary governed assets where Git is unsuitable.
- **Vault / approved secret stores:** secret values only.

A closeout report MAY link to several surfaces, but each governed object SHALL retain one canonical home as determined by D22.

## 7. Completion State and Evidence Navigation Contract

The default human-facing closeout pattern is:

```text
COMPLETED / CURRENT STATE
  -> WHAT CHANGED
  -> GOAL STATUS + WHY
  -> VALIDATION / UNRESOLVED ITEMS
  -> NEXT RECOMMENDED BODY OF WORK
  -> DCS CONTROL: CONTINUE | SKIP | DEFER | REORDER | INTERRUPT
  -> EVIDENCE / JUMP LINKS:
       GitHub | Supabase | Tribunal | CP Dashboard | ESCD | Deployment | Related Doctrine | Rollback/History
```

This is a semantic contract, not a mandatory visual layout. Command Post, ESCD, mobile, tablet, desktop, API, and future application surfaces may render it differently while preserving the same fields and authority boundaries.

## 8. Supersession and Exceptions

This consolidated v7.2 file preserves and supersedes the operative content of `DCSE_V7_2_RUNTIME_HARMONY_AND_PS_PUBLICATION_DIRECTIVE_20260905.md` as the current canonical file for this directive family.

It additionally supersedes any current runtime practice that:

1. omits mandatory task intake metadata or Preflight Validation for substantive work;
2. reports substantive completion without evidence-backed final reporting;
3. leaves available GitHub, Supabase, Tribunal, Command Post, ESCD, deployment, doctrine, or rollback evidence unnecessarily undiscoverable from the closeout report;
4. silently changes a governing goal;
5. allows an agent or model to treat its recommended next-work sequence as overriding DCS priority authority.

This directive does not waive confidentiality, secret handling, access governance, public-release review, evidence integrity, DCS reserved authority, lane boundaries, or task-specific Stop-Gates.

## 9. Enforcement

Runtime manifests, project instructions, agent onboarding, model wrappers, task packets, Tribunal receipts, Completion Evidence packets, Command Post views, ESCD work items, and other control surfaces SHALL reconcile to this directive.

A stale surface remains an observable synchronization defect and SHALL be reported rather than silently treated as compliant.

## 10. Promotion Record

The navigable final-reporting, goal-status, evidence-linking, and ESCD next-work prioritization amendment was explicitly **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 on 2026-09-10**.

No additional candidate approval gate applies to this exact amendment. Mechanical synchronization and evidence collection do not constitute a second approval decision.

Structure Precedes Scale.
