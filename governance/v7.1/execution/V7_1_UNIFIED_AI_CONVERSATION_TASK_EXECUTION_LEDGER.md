# V7.1 Unified AI Conversation and Task Execution Ledger

**Purpose:** Drive and record every governed AI conversation, task, assignment, execution event, artifact, review, decision, and promotion.  
**Current compliance:** `NON_PASS`  
**Verified gap:** Supabase contains four conversation records and five conversation turns. This does not represent every AI interaction.

## Governing principle

No AI conversation is operationally authoritative until it is registered. No task is complete until its registered conversation, execution events, artifacts, tests, review, and promotion state reconcile.

## Required identity chain

Every AI interaction must carry:

`conversation_id → turn_id → directive_id → task_key → assignment_id → agent_id → event_id → artifact_id → review_id → promotion_id`

A conversation can create multiple tasks. A task can cite multiple turns. Every operational claim must resolve through this chain.

## Conversation registration

At session start, create or resume a `dcse_cp.conversations` row with:

- stable external reference;
- source system and exact model or agent identity;
- lane and confidentiality;
- purpose and governing authority version;
- operator or originating system;
- start timestamp and status.

Every user and agent message must append one `conversation_turns` row containing sequence, role, timestamp, bounded summary or approved content, content hash, lane classification, referenced task keys, decisions, and artifacts. PS content remains isolated and confidential.

## Task creation rule

Any turn that requests execution, changes scope, accepts risk, makes a decision, reports a blocker, or claims completion must create or reference a task event. Pure discussion may remain conversation-only, but it still requires a turn record.

## State model

| State | Meaning |
|---|---|
| `REGISTERED` | Conversation or task exists |
| `PLANNED` | Scope, outputs, tests, dependencies, and capability defined |
| `ASSIGNED` | Eligible executor selected |
| `CLAIMED` | Executor accepted the assignment |
| `EXECUTING` | Tool-backed work started |
| `EVIDENCE_SUBMITTED` | Retrievable artifacts and results recorded |
| `VALIDATING` | Tests and reconciliation underway |
| `CORRECTION_REQUIRED` | One or more acceptance tests failed |
| `ACCEPTED` | Evidence satisfies the task contract |
| `PROMOTED_TO_GOVERNANCE` | Reviewed result merged to governance branch |
| `PROMOTED_TO_MAIN` | Release baseline merged to `main` |
| `DEPLOYED` | Target environment deployment verified |
| `ROLLED_BACK` | Verified rollback executed |
| `BLOCKED` | Defined blocker and recovery path recorded |

## Mandatory event types

Every task must record creation, assignment, claim, start, heartbeat, evidence submission, test result, failure, retry, reassignment, correction, review, decision, receipt, merge, promotion, deployment, rollback, and closeout when applicable.

## Model and agent rules

- Route by verified capability, access, cost, and risk, not model name alone.
- Qwen Coder may build and test bounded artifacts but cannot claim live host or database execution without tool evidence.
- Claude Code may execute host work only when the poller, credentials, and receipt path prove current capability.
- Codex may execute connector-backed work and independent review when it did not produce the evidence being reviewed.
- No model may independently approve its own material implementation.
- Provider unavailability triggers reassignment or bounded queuing without stopping unrelated tasks.

## Completion contract

Completion requires:

- original and completed scope match;
- successful assignment result;
- retrievable output references;
- artifact hashes;
- required test results;
- rollback instructions;
- GitHub and Supabase reconciliation;
- attributable independent validation when required;
- successor remediation tasks for accepted findings;
- exact promotion state.

Structural validation must be supplemented by semantic validation. Expected field names do not prove that the delivered artifact concerns the assigned product.

## BOW workstream routing

| Workstream | Active ledger | Current state |
|---|---|---|
| BOW-001 | `V7_1_BOW_001_ACTIVE_EXECUTION_LEDGER.md` | Host hardening pending |
| BOW-002 | `V7_1_BOW_002_ACTIVE_EXECUTION_LEDGER.md` | 30 registry findings pending |
| BOW-003 | `V7_1_BOW_003_ACTIVE_EXECUTION_LEDGER.md` | TSL `NON_PASS` remediation |
| BOW-004 | `V7_1_BOW_004_ACTIVE_EXECUTION_LEDGER.md` | CTJ `NON_PASS` remediation |

## Required implementation work

1. Register every active and future AI session in `conversations`.
2. Capture every turn or a governed bounded representation in `conversation_turns`.
3. Add stable linkage fields or mapping records between turns, tasks, assignments, events, artifacts, reviews, and promotions.
4. Enforce task completion and conversation closeout contracts.
5. Add dashboard views for unregistered turns, orphan tasks, unreceipted claims, unreconciled commits, and blocked promotions.
6. Add exportable execution logs by conversation, agent, model, task, product, lane, date, and promotion.
7. Prove the system with one complete conversation-to-promotion test and one failure-to-reassignment test.

## Closeout rule

Every AI session closes with a final conversation turn, referenced task states, GitHub commits where files changed, Supabase event and artifact inserts, unresolved blockers, next tasks, and explicit reconciliation status. A chat statement alone cannot close a governed session.
