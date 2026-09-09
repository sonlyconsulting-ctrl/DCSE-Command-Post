# ESCD REQUIREMENTS REGISTRY

**Task ID:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Artifact:** Requirements and identity contract  
**Status:** LOCKED CANDIDATE FOR IMPLEMENTATION  
**Supersedes working product name:** Aegis  

## 1. Identity contract

The personal/executive assistant is named **ESCD**. ESCD is intentionally the inverse relationship of DCSE.

- **DCSE** is the enterprise strategy, architecture, governance, portfolio, capability, opportunity, and cross-entity control environment.
- **ESCD** is the DCS-facing executive/personal operating layer that turns governed enterprise state, commitments, communications, tasks, decisions, routines, projects, watch conditions, and knowledge into what DCS needs to know, decide, remember, or do next.

Working distinction:

> DCSE governs the enterprise. ESCD serves the executive.

ESCD is not a replacement for DCSE Command Post. It is a governed consumer/operator surface connected to the Command Post control plane.

The prior name `Aegis` is historical implementation lineage only. Existing branches/files/code using Aegis must not be mass-renamed while active work is unreviewed. Renaming is a controlled refactor after the implementation checkpoint is preserved.

## 2. Product boundary

ESCD MUST:

- present a standalone, mobile-friendly personal/executive assistant experience
- use Command Post governance, approvals, evidence, orchestration, and source boundaries
- maintain persistent executive/task/job state independent of chat transcript
- support general executive/personal-assistant duties first, with DCSE as a governed mission context
- provide executive briefing, task/project management, inbox/pins, reminders, calendar awareness, communications triage, approvals, follow-up, research/workflow initiation, routines, monitoring, and governed delegation
- expose provenance and distinguish fact, recommendation, proposed action, approval, execution, and evidence
- remain advisory by default while taking bounded delegated actions under the autonomy contract
- support product/project make, fix, review, release, monitor, and recurring operating workflows through reusable workflow templates

ESCD MUST NOT:

- become a second enterprise governance authority
- treat LLM transcript as authoritative state
- silently promote DDNA/RAG/model output to doctrine or authority
- bypass Command Post stop-gates
- expose secrets or privileged credentials to browser/model/logs
- infer successful execution without evidence
- absorb specialized DCS Employment workflow logic into the ESCD core build

## 3. Build boundary decision

DCS Employment is tabled from the ESCD core implementation and becomes a separately governed build/integration module. ESCD may surface Employment-derived items later through a defined interface, but employment-specific opportunity, resume, submission, rate, interview, and follow-up logic is not part of the ESCD core acceptance contract.

## 4. Requirements classification

### MUST: executive kernel

R-001 Dedicated ESCD operating surface with DCS identity and responsive desktop/Android-class layout.

R-002 One DCS principal with supported identity mapping where current authentication safely supports linked identities.

R-003 Persistent executive state independent of model conversation history.

R-004 Core mission: general DCS executive/personal-assistant operations with governed DCSE context.

R-005 Inbox/Pins/Backlog intake with provenance and deduplication support.

R-006 Task and project records with priority, state, dependencies, dates, source, mission/context, and evidence references.

R-007 Durable job lifecycle: `queued -> running -> waiting_approval -> completed | failed | cancelled -> archived`.

R-008 Executive briefing derived from persisted state: changes, completions, approvals, highest-value next action, blockers, calendar conflicts, waiting items, and watch conditions.

R-009 Deterministic next-best-action engine with transparent score/reason factors.

R-010 Approval queue with explicit action state and no approval bypass.

R-011 Evidence/receipt linkage for consequential execution.

R-012 Command Post relationship/deep link and reuse of existing Agent OS capabilities where safe.

R-013 RLS/least-privilege protection on exposed ESCD state.

R-014 In-app notification intents/provider abstraction; Android push remains unverified until device-tested.

R-015 Reload/session restoration without losing authoritative executive state.

R-016 Double-test release discipline: functional/integration, repair, adversarial/E2E/regression, objective score >=95 and no failed hard gate.

R-017 Reusable workflow-template engine supporting make/fix/review/release/monitor/routine patterns without hard-coding one product.

R-018 Decision records with alternatives, evidence, recommendation, authority, decision, execution link, and follow-up.

R-019 Contact/person context separated from raw communications and source-of-truth contact systems.

R-020 Calendar conflict detection and meeting-preparation behavior.

R-021 Email/message triage rules with approval-gated external sends.

R-022 Command grammar that converts natural-language intent into explicit operation + target + context + authority class before consequential execution.

### SHOULD: near-term assistant capability

R-101 Calendar-aware daily agenda and conflict surfacing.

R-102 Email/message triage, follow-up extraction, draft preparation, and approval-gated external sending.

R-103 Recurring routines and scheduled work with receipts.

R-104 Contact/person context with source boundaries.

R-105 File/document retrieval and work-product routing.

R-106 Cross-source deduplication for pins, tasks, GitHub, Tribunal, calendar, communications, and assistant-created candidates.

R-107 Workflow templates for repeatable personal, project, product, operational, make/fix, review, release, and monitoring processes.

R-108 User-visible explanation of why an item is prioritized.

R-109 Recovery/retry controls for failed delegated jobs.

R-110 Mobile quick actions for capture, defer, approve, reject, done, snooze, and open-source.

R-111 DDNA candidate-ingestion interface with provenance/conflict handling and no self-promotion.

### LATER: expansion candidates

R-201 Voice-first assistant interaction.

R-202 Rich Android push actions.

R-203 Broader personal-life mission domains.

R-204 Additional personas/avatar presentation.

R-205 Multi-user/delegated human collaboration.

R-206 Broader autonomous connector execution after evidence demonstrates safe bounded operation.

R-207 Specialized DCS Employment integration after its independent build reaches its own acceptance gate.

## 5. Assistant task taxonomy

Every ESCD item SHOULD resolve to one primary task class and may carry secondary tags.

1. **CAPTURE**: pin, note, idea, request, commitment, observation.
2. **TRIAGE**: classify, deduplicate, prioritize, route, defer, reject.
3. **PLAN**: project, milestone, dependency, schedule, preparation.
4. **MAKE**: create a new product, asset, system, workflow, document, component, or deliverable.
5. **FIX**: diagnose, repair, remediate, reconcile, restore, or correct an existing item.
6. **DO**: bounded internal execution or delegated job not better classified as MAKE/FIX.
7. **DECIDE**: recommendation, alternatives, tradeoffs, DCS decision required.
8. **APPROVE**: external/consequential action waiting for explicit authority.
9. **COMMUNICATE**: email, message, follow-up, meeting preparation, draft/send.
10. **RESEARCH**: retrieve, compare, verify, summarize, evidence gather.
11. **DCSE**: enterprise strategy, governance, capability, portfolio, Command Post work.
12. **ROUTINE**: recurring/scheduled personal or executive activity.
13. **MONITOR**: condition watch, deadline, response, status, runtime, opportunity.
14. **REVIEW**: validation, QA, adversarial check, reconciliation, closeout.
15. **RELEASE**: prepare, validate, gate, publish/deploy/promote when authorized.
16. **ARCHIVE**: completed/inactive material retained with provenance.

Minimum routing attributes: `task_class`, `context`, `source`, `priority`, `urgency`, `value_relevance`, `approval_class`, `status`, `owner/executor`, `dependencies`, `due_at`, `evidence_refs`, `created_at`, `updated_at`.

## 6. Acceptance principle

A requirement is not satisfied because a screen, prompt, model statement, or placeholder exists. It is satisfied only by reproducible implementation evidence appropriate to the requirement.

Any conflict with current operative governance, security controls, or verified runtime state must be surfaced rather than silently reconciled.
