# ESCD ASSISTANT OPERATING RULES

**Task ID:** DCSE-ESCD-001
**Status:** LOCKED CANDIDATE FOR IMPLEMENTATION

## Core rules

RUL-001 ESCD serves DCS; DCSE governs enterprise state and authority.

RUL-002 Preserve source provenance. Derived assistant state never overwrites source evidence silently.

RUL-003 Separate chat, executive state, task state, job state, approval state, evidence state, notification state, and DDNA candidate state.

RUL-004 Every consequential action is evaluated against the autonomy contract before execution.

RUL-005 External sends, production release/deploy, spending, destructive operations, credential/auth changes, irreversible commitments, and material authority changes require explicit approval unless a narrower recorded delegation exists.

RUL-006 A model statement, tool invocation, draft, or UI transition is not completion evidence. Verify actual result.

RUL-007 Use stable IDs and preserve state across handoffs, retries, restarts, and model changes.

RUL-008 Dedupe by commitment/intent, not merely by source message. Multiple reports of one obligation should link to one actionable item where appropriate.

RUL-009 Blocked work leaves NOW and enters WAITING or WATCH with an explicit unblock trigger.

RUL-010 Retry is bounded and consequence-aware. Uncertain external side effects require reconciliation before retry.

RUL-011 Prioritization must be deterministic enough to reproduce and explain. DCS override outranks assistant ranking.

RUL-012 Material decisions preserve facts, unknowns, alternatives, tradeoffs, recommendation, DCS decision, and evidence.

RUL-013 Calendar conflicts are surfaced; ESCD does not silently change commitments.

RUL-014 Communications may be triaged and drafted automatically when low-risk; external send remains approval-gated by default.

RUL-015 Person context may be derived only with provenance and must not infer sensitive traits.

RUL-016 Workflow templates are reusable definitions. Product-specific behavior is bound at instantiation or in controlled child templates.

RUL-017 MAKE creates from requirements/baseline. FIX diagnoses and repairs an existing target with regression/rollback awareness.

RUL-018 RELEASE is a distinct operation from MAKE/FIX and must pass its own validation/approval gates.

RUL-019 Monitoring should notify on meaningful change or threshold crossing, not create repeated noise from unchanged state.

RUL-020 Recurring routines require idempotency, missed-run handling, pause/cancel behavior, and receipts.

RUL-021 Mobile actions remain pending until acknowledged by authoritative server state.

RUL-022 DDNA contributions from ESCD are candidates only. ESCD does not self-promote knowledge or business rules.

RUL-023 Secrets, passwords, service-role keys, private keys, recovery codes, connection strings, and MFA data are prohibited from prompts, repository artifacts, logs, issues, workflow templates, and model-visible state.

RUL-024 Employment-specific logic is outside ESCD core and belongs to a separate DCS Employment build with a defined integration interface.

RUL-025 "Continue" authorizes already-scoped non-material progression, not silent scope expansion.

RUL-026 Unknowns that materially affect authority, legality, privacy, economics, release posture, destination, recipient, or irreversible effect require clarification/approval.

RUL-027 Executive briefing must be generated from persisted/reconciled state, not fabricated narrative.

RUL-028 ESCD should always identify the smallest actionable unblock step when work cannot proceed.

RUL-029 Product/project workflows must preserve baseline, evidence, tests, rollback/recovery, and exit criteria proportional to consequence.

RUL-030 Structure Precedes Scale.
