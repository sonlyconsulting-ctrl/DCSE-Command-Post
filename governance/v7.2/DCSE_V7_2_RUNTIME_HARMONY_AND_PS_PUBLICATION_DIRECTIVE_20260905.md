# DCSE v7.2 Runtime Harmony and PS Publication Boundary Directive

Status: ACTIVE DCS EXPRESS DIRECTIVE
Authority: DCS Level 0
Effective date: 2026-09-05
Lane: DCSE Governance
Directive ID: DCS-DIR-20260905-001

## Purpose

Correct runtime drift across model and agent surfaces by enforcing the operative DCSE Master Profile v7.2 R5 authority, restoring mandatory task traceability, and narrowing the former case-specific PS isolation rule to the publication boundary now required after case conclusion.

## 1. Operative authority

`DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md` is OPERATIVE under `DCSE_V7_2_R5_OPERATIVE_DESIGNATION_20260808.md` and its DCS authority designation.

Any embedded `CANDIDATE-R5` label in the controller is build-stage provenance only and does not reduce the controller's current OPERATIVE authority.

Compiled v7.2 rules with status `ACTIVE_IF_AUTHORIZED` are enforced through the operative R5 controller when routed to a task. Historical source-state labels remain provenance and do not defeat authority inherited from the operative controller or an active registered DCS directive.

## 2. Mandatory task traceability

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

## 3. Model and agent harmony

All governed model and agent surfaces SHALL resolve authority from the same operative chain:

1. R5 operative designation;
2. DCSE Master Profile v7.2 R5;
3. `dcs_express_directives.v7.2.json`;
4. D22 source and authority reconciliation;
5. D21 doctrine routing and task declaration;
6. universal onboarding/access controls;
7. task-routed doctrines and assignment.

No model or agent may self-assign constitutional authority, invent a permanent role, silently waive preflight, or substitute its own summary for the operative authority chain.

A surface that cannot load or verify this chain SHALL report `UNSYNCHRONIZED` or `DEGRADED` and SHALL NOT claim full v7.2 compliance for authority-sensitive work.

## 4. PS publication boundary after case conclusion

The former standing rule requiring strict PS isolation from all non-PS internal work is narrowed by this directive.

PS-origin material remains confidential and protected from public spill. Unless DCS expressly authorizes otherwise, PS-origin facts, evidence, litigation strategy, case analysis, party-specific allegations, or protected case material SHALL NOT be used in public-facing:

- Sonly Consulting content;
- Smoove Spots content;
- The Initiative content;
- websites or public web applications;
- campaigns, social media, marketing, advertising, investor materials, or movement narratives;
- public product copy or external communications.

Internal, private, governance, archival, systems, operational, or analytical use is not blocked merely because material originated in PS, provided confidentiality, purpose limitation, and access controls are maintained.

The prior PS Stop-Gate remains applicable when PS-origin material is about to enter public-facing content without express DCS authorization. It is not a standing bar against internal/private use after case conclusion.

If DCS activates a new legal matter or expressly reactivates case-specific PS isolation, the stricter matter-specific firewall controls for that matter.

## 5. Supersession and exceptions

This directive supersedes conflicting standing language only to these extents:

1. any current-state label treating v7.2 R5 itself as merely candidate for authority purposes;
2. any runtime practice omitting task ID, preflight validation, or D21 traceability for substantive work;
3. any blanket PS isolation rule that blocks internal/private use solely because the source originated in the concluded PS matter.

This directive does not waive confidentiality, secret handling, access governance, public-release review, evidence integrity, DCS reserved authority, or new-matter legal isolation controls.

## 6. Enforcement

Runtime manifests, project instructions, agent onboarding, model wrappers, task packets, Tribunal receipts, and other control surfaces SHALL reconcile to this directive. A stale surface remains an observable synchronization defect and SHALL be reported rather than silently treated as compliant.

Structure Precedes Scale.
