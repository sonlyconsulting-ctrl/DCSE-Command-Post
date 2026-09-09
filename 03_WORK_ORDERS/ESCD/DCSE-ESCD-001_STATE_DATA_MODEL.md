# ESCD STATE AND DATA MODEL

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Principle

ESCD separates conversational context from authoritative operational state. LLM transcript is never the system of record for task, approval, job, evidence, notification, or completion state.

## Core state domains

1. **principal_state**: DCS identity, linked identities, preferences, locale/timezone.
2. **mission_state**: DCSE, DCS Employment, and later approved mission domains.
3. **executive_session_state**: session open/acknowledgement/checkpoint and briefing cursor.
4. **item_state**: captured items, task taxonomy, source, status, mission, priority, due date, dependencies.
5. **project_state**: projects, milestones, objectives, linked tasks/items.
6. **job_state**: delegated execution lifecycle and executor metadata.
7. **approval_state**: requested action, authority class, decision, timestamp, scope, expiration.
8. **evidence_state**: receipts, source references, verification results, hashes/URLs where appropriate.
9. **notification_state**: intent, channel, delivery state, acknowledgement, escalation.
10. **watch_state**: monitored condition, check cadence/trigger, last state, next evaluation.
11. **decision_state**: question, alternatives, recommendation, DCS decision, rationale/evidence links.
12. **routine_state**: recurring workflow definition, recurrence, last/next run, exception policy.

## Stable identifiers

Every durable record requires a stable immutable ID. Cross-system records retain external source IDs separately. Never use mutable title/text as identity.

## Provenance minimum

Every derived ESCD record stores source system, source identifier/reference, ingestion/capture time, actor/executor, derivation method where relevant, and evidence refs. Unknown provenance is explicitly marked.

## Status contracts

### Item
`captured -> triaged -> planned -> active | waiting | watch | approval -> completed | cancelled -> archived`

### Job
`queued -> running -> waiting_approval -> completed | failed | cancelled -> archived`

### Approval
`proposed -> pending -> approved | rejected | expired | withdrawn`

### Notification
`created -> queued -> delivered | failed -> acknowledged | escalated | closed`

## Source/derived separation

Store immutable/raw source reference and normalized/derived ESCD fields separately. Re-enrichment must not overwrite original source meaning.

## History

Material state transitions emit append-oriented events containing prior state, new state, actor, timestamp, reason, and evidence reference. Current tables may materialize latest state for performance but history remains recoverable.

## Security

RLS on every exposed ESCD table. Privileged service credentials remain server-side. Cross-principal data access is denied by default. Views/RPC/security-definer functions require explicit review.

## DDNA boundary

DDNA content consumed by ESCD is referenced by governed identity/provenance. ESCD-derived observations enter DDNA only as candidate contributions and do not self-promote.

## Acceptance

Schema implementation must prove stable IDs, persistence across reload, authorized/unauthorized access, state-transition validity, append history, source preservation, approval linkage, evidence linkage, and rollback/migration behavior.