# ESCD OPERATING WORKFLOW AND PROCESS STREAM

**Task ID:** DCSE-ESCD-001  
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD is a continuous executive operating stream, not a collection of disconnected assistant features. Every input moves through a common governed lifecycle while mission-specific workflows may extend it.

## Universal ESCD lifecycle

`CAPTURE -> NORMALIZE -> DEDUPLICATE -> CLASSIFY -> ENRICH -> PRIORITIZE -> ROUTE -> PLAN -> AUTHORIZE -> EXECUTE -> VERIFY -> EVIDENCE -> BRIEF -> FOLLOW-UP -> CLOSE/ARCHIVE -> LEARN-CANDIDATE`

### 1. Capture
Accept a pin, message, email-derived commitment, calendar item, GitHub/Tribunal signal, DCS instruction, assistant observation, recurring trigger, or connector event. Preserve original source/provenance.

### 2. Normalize
Create a stable ESCD item ID and normalize minimum metadata without overwriting source meaning.

### 3. Deduplicate
Compare against active/completed items and linked external records. Link duplicates rather than destroying provenance.

### 4. Classify
Assign task taxonomy, mission, sensitivity/lane, and preliminary approval class.

### 5. Enrich
Resolve dates, people, dependencies, source evidence, related projects, revenue relevance, and missing information from approved sources. Mark unknowns.

### 6. Prioritize
Apply deterministic next-best-action scoring. Preserve DCS overrides.

### 7. Route
Choose DCS, ESCD internal execution, Command Post workflow, model/agent/tool, DCS Employment, or another entity handoff.

### 8. Plan
For non-trivial work, define objective, steps, dependencies, executor, evidence, rollback, and exit criteria.

### 9. Authorize
Apply the autonomy contract A0-A4 before execution.

### 10. Execute
Perform only the authorized action. Maintain job state independently of chat transcript.

### 11. Verify
Confirm actual result. A tool call, draft, or model statement is not completion evidence by itself.

### 12. Evidence
Write receipt/event/evidence reference proportional to consequence.

### 13. Brief
Update executive state so ESCD can explain what changed, what completed, what needs approval, blockers, and next-best action.

### 14. Follow-up
Create any verified next commitment, deadline, response watch, retry, or dependency.

### 15. Close/Archive
Close only when exit criteria are met. Preserve provenance and evidence.

### 16. Learn-Candidate
Extract reusable preference, pattern, rule, template, or knowledge only as a candidate. Route governed knowledge to DDNA/RAG/rule processes; do not self-promote.

## Core workflow families

### Daily executive cycle

`SESSION OPEN -> STATE RECONCILIATION -> OVERNIGHT/RECENT CHANGES -> TODAY COMMITMENTS -> APPROVALS -> REVENUE/EMPLOYMENT -> BLOCKERS -> NEXT BEST ACTION -> DCS OVERRIDE -> WORK STREAM`

### Inbox/pin cycle

`CAPTURE -> SOURCE LINK -> DEDUPE -> CLASSIFY -> PRIORITIZE -> ROUTE -> TASK/REFERENCE/ARCHIVE`

### Employment opportunity cycle

`DISCOVER/RECEIVE -> VERIFY -> FIT ASSESS -> DEADLINE/RATE/LOCATION -> PRIORITIZE -> CUSTOMIZE MATERIAL -> REVIEW -> APPROVE SUBMISSION -> SUBMIT -> RECEIPT -> FOLLOW-UP -> INTERVIEW/OFFER/CLOSE`

External submission remains approval-gated unless a future explicit delegation says otherwise.

### Communication cycle

`RECEIVE -> TRIAGE -> CONTEXT -> ACTION/REPLY NEED -> DRAFT -> DCS APPROVAL WHEN REQUIRED -> SEND -> VERIFY -> FOLLOW-UP`

### Delegated job cycle

`CANDIDATE -> PLAN -> AUTONOMY CLASS -> QUEUED -> RUNNING -> WAITING_APPROVAL if required -> COMPLETED/FAILED/CANCELLED -> VERIFY -> EVIDENCE -> ARCHIVE`

### Decision cycle

`QUESTION -> EVIDENCE -> ALTERNATIVES -> TRADEOFFS -> ADVERSARIAL REVIEW -> RECOMMENDATION -> DCS DECISION -> RECORD -> EXECUTE if authorized -> VERIFY`

### DDNA contribution cycle

`OBSERVATION/ARTIFACT -> PROVENANCE -> EXTRACT -> CLASSIFY -> DUPLICATE/CONFLICT CHECK -> CANDIDATE -> GOVERNED VALIDATION/PROMOTION PROCESS`

ESCD consumes governed DDNA knowledge but does not make DDNA content authoritative merely by using it.

## Process controls

- Preserve stable IDs across handoffs.
- Separate source state from derived assistant state.
- Every consequential state transition has provenance.
- Do not create duplicate tasks for the same commitment merely because multiple systems report it.
- Route material conflicts to decision/approval rather than silently resolving them.
- Retry only within the autonomy contract.
- A blocked item must identify the smallest action needed to unblock it.
- Closeout must create the next action when the underlying commitment continues.

## Stream model

ESCD should continuously maintain five executive queues:

1. **NOW**: highest-value actionable work.
2. **APPROVAL**: consequential actions waiting on DCS.
3. **WAITING**: dependencies, replies, external conditions, scheduled events.
4. **WATCH**: monitored conditions/deadlines/status changes.
5. **BACKLOG**: valid but currently lower-value work.

Completed work leaves the active queues and remains evidence-linked in history.

## Anti-loop control

An item must not repeatedly return to NOW merely because it is old. Priority requires actionability. Blocked/waiting work routes to WAITING/WATCH with an explicit trigger. Failed work uses bounded retry and then escalates with evidence. This prevents assistant-generated activity from displacing higher-value DCS work.