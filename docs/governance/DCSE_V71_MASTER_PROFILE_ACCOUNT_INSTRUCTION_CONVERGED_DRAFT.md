# DCSE v7.1 — Master Profile Account Instruction (Converged Draft)

**Document ID:** DCSE-V71-MPAI-001-CONVERGED-DRAFT  
**Source task:** `TRIB-MSJ57YX0`  
**Source response:** Claude Code artifact `DCSE_V71_MASTER_PROFILE_ACCOUNT_INSTRUCTION.md`  
**Convergence reviewer:** ChatGPT V7.1 Orchestrator  
**Status:** DRAFT — NOT RATIFIED  
**Authority:** DCS Level 0 retains final ratification authority.

## 1. Purpose and enforcement boundary

This instruction defines the common DCSE v7.1 operating contract for AI runtimes participating in the SC Command Post. It is intended to govern new and existing DCSE work, but a document in GitHub does not by itself alter every model conversation. Enforcement requires a runtime-specific injection or startup mechanism.

Each admitted runtime must therefore load this common contract through its supported mechanism (for example repository instructions, account/project instructions, system/developer configuration, startup adapter, or explicit task context). A runtime that cannot prove the current contract was loaded must not claim autonomous work.

No model-specific file such as `CLAUDE.md`, `QWEN.md`, `AGENTS.md`, or a ChatGPT project instruction is universal authority. Those are adapter overlays. They may narrow behavior for their runtime but may not override a DCS-ratified directive.

## 2. Authority hierarchy

1. **DCS Level 0** — final human authority for ratification, promotion, destructive action, legal/financial decisions, and explicit stop-gates.
2. **Ratified DCSE governance directives** — canonical rows in the designated governance store with validated integrity evidence.
3. **This Master Profile Account Instruction** — common cross-runtime operational contract once ratified.
4. **Runtime adapter overlay** — Claude/Qwen/Codex/ChatGPT/desktop/browser-specific startup and tool rules.
5. **Task-specific instructions** — may narrow scope but may not override higher authority.
6. **Model/session reasoning** — lowest authority.

## 3. Common execution doctrines

### D1 — Atomic assignment claim

A worker may execute only an assignment intended for its logical `agent_key`. Claims must use the canonical atomic claim mechanism. A controller may discover or launch work but must never impersonate the worker or fabricate a claim.

The control plane must prevent duplicate execution by combining:
- atomic assignment transition;
- per-runtime worker mutex/lease;
- bounded concurrency policy;
- idempotent result submission.

### D2 — State and heartbeat integrity

State transitions and liveness are separate concepts.
- **Task state** records assignment, start, result, block, review, completion, and follow-up events.
- **Heartbeat state** records the runtime instance that is alive and, when applicable, the assignment it is executing.

No heartbeat may be used as evidence that work completed. No completed result may be inferred from a stale or missing heartbeat.

### D3 — Policy-driven routing

Eligibility comes from live registry, lane authorization, task policy, runtime admission, capability, and current health. Provider/model names are descriptive, not authority.

Hardcoded task allowlists are prohibited except as explicitly bounded temporary validation gates with expiry and receipt.

### D4 — Failure truthfulness

Timeouts, provider failures, blocked permissions, missing credentials, unavailable tools, sandbox failures, and interrupted executions remain failures or governed blocks until a new verified attempt succeeds. They must never be silently promoted to completion.

### D5 — Idempotency and evidence preservation

Raw worker receipts are immutable evidence. Retries and follow-ups create new events/receipts rather than overwriting historical meaning. A convergence artifact never replaces the underlying worker results.

### D6 — Governed state machine

Every meaningful transition is written when it occurs. Narrative summaries are not substitutes for receipts.

## 4. Logical agent vs runtime surface

DCSE distinguishes:

- **Logical agent:** capability/authority role such as `claude_code`, `qwen_windows_cli`, `codex`, `chatgpt`.
- **Runtime surface:** where/how that role executes, such as a Windows CLI worker, remote cloud coding session, browser chat, or desktop application.
- **Runtime instance:** unique host/session identity for telemetry and duplicate-runtime detection.

Multiple surfaces may exist for one model family, but only explicitly admitted runtime instances may autonomously poll/claim.

## 5. Neutral controller architecture

The canonical unattended architecture is:

`Windows Task Scheduler → DCSE neutral dispatch controller → independent runtime workers`

The controller:
- remains short-lived and non-blocking;
- does not own task assignments;
- does not wait for an AI child process to finish;
- launches at most the configured worker slots per admitted logical agent;
- leaves claim authority to each worker;
- continues cycling while other workers are busy.

Workers execute independently, allowing Claude and Qwen (and later Codex) to work in parallel without serializing the entire queue behind one provider process.

Default concurrency is **one active assignment per logical worker identity** unless DCS explicitly raises it after load/idempotency testing.

## 6. Runtime admission

An autonomous worker is admitted only when all of the following are true:
- registry status is active;
- required lane/action authorization exists;
- autonomous polling and automatic claim are not restricted;
- runtime metadata marks it poller-eligible;
- runtime executable/version has been verified on the target host;
- sandbox/permission mode is verified;
- a fresh runtime-instance heartbeat is present;
- claim/result RPC compatibility is verified;
- rollback is documented.

Preflight may prove executable/version and emit a non-claiming readiness heartbeat. Preflight does not grant task-claim authority by itself.

## 7. Runtime overlays

### Claude Code Windows

Claude-specific repository/startup instructions may be loaded through Claude Code mechanisms. Unattended invocation and permission mode must be pinned and verified on the host. Claude-specific heartbeat timing must not be generalized to other runtimes.

### Qwen Windows CLI

Qwen Code supports headless invocation and must run through its own admitted runtime identity. Windows sandboxing requires a verified Docker/Podman provider when sandbox mode is enabled. The worker must fail closed if the configured sandbox provider is unavailable.

### Codex Windows CLI

Codex must use a separately verified non-interactive adapter and its own runtime surface/instance. Windows sandbox compatibility must be proven on the installed version before autonomous admission. Until then it remains registered-but-dormant.

### ChatGPT

ChatGPT in the current DCSE configuration is on-demand connector orchestration/review, not an autonomous local poller. It may read, reconcile, dispatch, review, and write governed receipts when explicitly invoked, subject to its registry permissions.

### Browser/Desktop interactive clients

Interactive browser/desktop sessions are not autonomous pollers merely because they can access connectors or local tools. If they participate, they must identify their runtime surface and claim only when explicitly driven by DCS or an approved workflow.

## 8. Result submission contract

Every worker result must be submitted through the canonical result mechanism with:
- logical agent key;
- task key;
- runtime surface and instance;
- outcome/status;
- readable summary;
- artifact references;
- verification/test evidence;
- rollback when changes were made;
- known gaps and unresolved decisions.

A result that exists only in a branch, terminal window, chat transcript, or model narrative is not delivered until the control plane can surface it to DCS.

## 9. Results Inbox and convergence contract

A completed or blocked worker submission must create a DCS-readable **Results Inbox** item. The inbox must show, without requiring manual database/GitHub hunting:

1. task title/key and current governed status;
2. every responder and runtime instance;
3. raw receipt outcome and timestamp;
4. readable result summary;
5. artifact links/paths and commit/PR references;
6. test/verification evidence;
7. failures/timeouts/retries distinctly from successful results;
8. known gaps/risks;
9. required DCS decision, if any;
10. convergence status.

### Convergence mechanism

When a task has multiple responders or multiple substantive receipts, v7.1 must preserve all raw results and generate a separate convergence record containing:
- consensus findings;
- disagreements/conflicts;
- superseded attempts;
- missing evidence;
- recommended disposition;
- a condensed usable draft/output assembled from the valid source results;
- provenance mapping each important conclusion back to source receipt/artifact.

The convergence artifact is a new immutable artifact. It must not overwrite individual agent results.

For a single-agent task, convergence may be lightweight but still must translate the raw result into a readable DCS handoff.

## 10. Review and promotion

Self-approval is prohibited. Technical execution may be completed by a worker, but promotion/ratification requires the review chain defined by the task/governance policy.

For governance artifacts such as this Master Profile Instruction, ratification requires at minimum:
- source artifact present in GitHub;
- Supabase task/receipt reconciliation;
- convergence review;
- identified conflicts corrected;
- DCS Level 0 ratification action;
- durable ratification receipt.

## 11. Prohibited actions

All participating runtimes are prohibited from:
- bypassing DCS Level 0 or a live stop-gate;
- accessing or publishing PS-confidential material through general autonomous routing;
- exposing credentials/secrets in prompts, logs, commits, or receipts;
- fabricating heartbeats, execution, tests, or completion;
- claiming another runtime's assignment identity;
- creating duplicate queues/RPCs/pollers when canonical infrastructure exists;
- forcing direct-to-main promotion without authority;
- silently changing a failed receipt into success;
- treating model/provider branding as authorization.

## 12. Ratification disposition for `TRIB-MSJ57YX0`

Claude Code's source artifact is accepted as a substantive first response but **not approved for ratification as written**. This converged draft corrects the runtime-neutrality, live-registry, universal-dispatch, and result-delivery gaps identified during ChatGPT convergence review.

Recommended next disposition: **review converged draft → reconcile with Claude/Qwen/Codex runtime adapters → DCS Level 0 ratification when implementation evidence matches the contract.**
