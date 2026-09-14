# ESCD Orchestration v1 — Antigravity Finalize and Execute

**Task ID:** ESCD-ORCH-V1-20260913-001  
**Authority:** DCS  
**Lane:** DCSE / ESCD  
**Goal:** Finalize the first production-capable ESCD orchestration loop without making Vercel the orchestration core.

## Read first

1. Canonical repository: `sonlyconsulting-ctrl/DCSE-Command-Post`.
2. Current authoritative DCS direction is the ESCD Orchestration Turn Contract in this branch.
3. Supabase migration `20260914034207_escd_orchestration_exchange_v1` is already applied to production project `nevgdyfpxdaloacuutal`.
4. First durable packet already exists: `TURN-F8097456A9CE`.
5. Local worker registry contains `DCS-WINDOWS-OLLAMA-01` in OFFLINE state.
6. Do not change Vercel deployment architecture as part of this task. Vercel remains a UI/API hosting surface only.

## Source-package reconciliation

Do not merge PR #103 or #104 as-is.

Use the latest supplied orchestrator archive whose SHA-256 is:

`c9a562a0aae0df93aace85d7870be64711464953ea2204e8a7cf9e340cba2abb`

Required archive evidence:
- `dcse/adapters.py` exists.
- `def verify_result` exists in `dcse/adapters.py`.
- canonical packets exist only under `tasks/queue/`.
- `tasks/operations/stage_lifecycle.md` is absent in this archive; do not reintroduce documentation claiming four stages until code/tests implement those stages.
- `dcse/rulebase.py` must be package-local and must not depend on `/home/claude/desk`.

Close PR #103 as superseded.
Close PR #104 with a note that its root queue layout was adopted but the branch was not merged because it carried stale engine/adapter assumptions.

## Before importing orchestrator code

Repair and independently verify the canonical Operative Rules Engine v0.2 artifact. The existing promoted tar.gz was reported truncated. Rebuild from the intact verified blueprint, verify extraction and hashes, then reconcile the reported 15-vs-148 rule count before using "zero collisions" as evidence.

Do not downgrade any operative v0.2 rule into candidate state.

## Workstream A — Core Orchestrator

Implement the full turn lifecycle:

INGRESS → PRECONDITION → EXECUTION → POSTCONDITION → AUDIT → RESPONSE → TERMINAL

The Orchestrator is the only component allowed to advance control.

Every provider/tool return envelope must include at least:

```json
{
  "turn_id": "uuid-or-turn-key",
  "control": "RETURN_TO_ORCHESTRATOR",
  "payload": {},
  "provider": "ollama|openai|gemini|openrouter|...",
  "model": "...",
  "confidence": 0.0,
  "evidence_refs": []
}
```

Run `verify_result` on every provider/tool return before state advancement.

No provider may call the next provider/tool directly.

Add bounded-step/retry/time safeguards and duplicate-state detection.

## Workstream B — Supabase Exchange

Use the existing production structures:

- `dcse_cp.conversations`
- `dcse_cp.conversation_turns`
- `dcse_cp.escd_runtime_workers`
- `dcse_cp.escd_operation_turns`
- `dcse_cp.escd_operation_events`

Worker claims are through:

`dcse_cp.escd_claim_next_turn(worker_key, lease_seconds)`

Provider/tool returns are recorded through:

`dcse_cp.escd_record_return(...)`

Do not expose service-role credentials to browser code.

Supabase is authoritative state. Realtime is notification only. Implement Realtime subscription for UI updates if practical; retain safe polling fallback.

## Workstream C — Ollama Local Worker

Create a persistent Python worker on the DCS Windows/WSL execution surface.

The worker:
1. authenticates to Supabase using a server/worker credential, never a browser key;
2. heartbeats `DCS-WINDOWS-OLLAMA-01`;
3. claims a turn;
4. sends the bounded provider packet to local Ollama;
5. validates Ollama's structured result;
6. records RETURN control+payload;
7. returns control to the Orchestrator;
8. continues only as directed by Orchestrator state/rules;
9. records failures honestly and releases/terminates stale work.

Do not attempt to reach `localhost:11434` from Vercel.

Ollama is an inference provider, not the orchestrator and not governance authority.

## Workstream D — ESCD API and UI

Current production chat flow directly calls `chat(provider,messages)`. Replace that operational path.

`POST /api/mvp/chat` may remain as a compatibility endpoint, but it must create/continue an ESCD operation turn rather than directly handing the conversation to a model.

Implement API operations equivalent to:
- create turn / Send;
- read active turn/status/events;
- Continue/Resume a WAITING_USER turn;
- Stop/Cancel an active turn.

UI changes:
- **Send** starts a new operational turn.
- **Stop** appears while active work is running.
- **Continue/Resume** appears only for WAITING_USER / resumable escalated state.
- Add an operation-status strip: turn key, stage/state, current provider/worker, Stop or Continue control.
- Final answer is shown only after Orchestrator response composition/validation.
- Preserve the conversation after turn completion.

Provider selector becomes a preference/hint to the Orchestrator, not a direct bypass around it.

## Workstream E — Remote / Multi-model Providers

OpenAI, Gemini, OpenRouter, Claude/Codex-compatible workers, and future providers must implement the same request/return contract.

Different models may work on independent implementation branches, but:
- one integration owner controls the final branch;
- each model gets disjoint file scope where possible;
- each handoff includes tests/evidence;
- no model self-promotes its own change;
- final acceptance is independent of the producer.

Suggested split:
- Agent 1: core orchestrator/stages/return contract/tests.
- Agent 2: ESCD API + UI Send/Stop/Continue/status strip.
- Agent 3: Ollama local worker + provider adapter.
- Agent 4: Supabase client/realtime/polling integration + security tests.
- Independent final auditor: cross-branch integration, rule coverage, end-to-end acceptance.

## First end-to-end acceptance

Use existing bootstrap turn:

`TURN-F8097456A9CE`

Expected objective:
- inspect canonical task queue;
- identify next runnable task;
- return disposition/evidence;
- do not execute HOLD_DCS or STALE_RECONCILE tasks.

Expected result at current queue state: T-002 should be identified as READY/auto, but the bootstrap turn itself is inspect-only and must not execute T-002.

Evidence must show:

DCS request → Supabase turn → worker claim → Ollama request → Ollama RETURN(control+payload) → Orchestrator validation → rules evaluation → response composition → conversation transcript write → COMPLETE → ESCD UI displays answer.

## Acceptance tests

Must include:
1. provider RETURN with missing control fails;
2. provider RETURN with empty payload fails;
3. tool/model cannot directly advance another provider;
4. invalid turn transition fails;
5. terminal state sets terminal timestamp;
6. WAITING_USER exposes Continue/Resume;
7. Send creates a new turn;
8. Stop results in governed CANCELLED transition;
9. session remains open after turn COMPLETE;
10. Ollama worker can go offline/reconnect without losing a queued turn;
11. no browser/service-role secret exposure;
12. remote providers and Ollama normalize to the same return contract;
13. bootstrap turn completes and UI shows its evidence-backed answer.

## Exit criteria

Do not call ESCD Orchestration v1 complete until:
- all above tests pass;
- first bootstrap turn completes through the real worker/provider path;
- independent audit verifies state/event evidence;
- code and database migration are committed to canonical GitHub;
- no stale duplicate task queues remain;
- PR #103/#104 are closed with provenance notes;
- repaired Rules Engine artifact is readable and rule counts reconciled.

