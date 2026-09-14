# DCSE v7.2 — ESCD Orchestration Turn Contract

**Directive ID:** ESCD-ORCH-TURN-20260913-001  
**Authority:** DCS explicit direction, 2026-09-13  
**Governance status:** OPERATIVE-PATCH requirement  
**Runtime implementation status:** PARTIAL — database controls are live; orchestrator/UI/provider integration remains to be completed and independently validated.  
**Lane:** DCSE / ESCD / Rules Engineering

## Purpose

This amendment closes the control-loop gap between ESCD, the DCSE Python Orchestrator, local/remote model providers, capability adapters, and the user-facing conversation.

## Locked rules

1. **ORCH-001 — Orchestrator owns control.** Every ESCD operational turn is owned by the DCSE Orchestrator. A model, tool, adapter, or sub-operation may not directly continue the workflow by invoking another provider/tool outside orchestrator dispatch.

2. **ORCH-002 — Control and payload return together.** Every provider/tool RETURN must include a recognized control state and a non-empty structured payload. A bare "done", prose-only completion claim, or control-only return is invalid.

3. **ORCH-003 — Session and turn are different lifecycles.** An ESCD conversation may remain open while each operational turn reaches a defined state.

4. **ORCH-004 — Defined terminal/waiting states.** A turn must resolve to COMPLETE, WAITING_USER, ESCALATED, REFUSED, FAILED, or CANCELLED. No turn may remain unbounded.

5. **ORCH-005 — Durable state outranks transport.** Supabase is the durable exchange/state ledger. WebSockets/Realtime, Vercel requests, local process memory, provider chat state, and UI state are notification/transport surfaces and are not operational truth.

6. **ORCH-006 — Return packets are validated before continuation.** The Orchestrator validates schema, turn/correlation identity, control state, payload, evidence references, and applicable rule conditions before advancing a turn.

7. **ORCH-007 — Local Ollama is reached through a local worker.** A cloud-hosted ESCD/Vercel runtime must not attempt to reach the user's local Ollama endpoint through localhost. Ollama access occurs through an authorized local DCSE Python worker which claims durable turns from Supabase and returns results through the same contract.

8. **ORCH-008 — Provider neutrality.** Ollama, OpenAI, Gemini, OpenRouter, Claude/Codex-compatible workers, and future providers use the same return envelope and do not become governance authorities.

9. **ORCH-009 — Bounded loops.** Orchestration has explicit maximum steps/retries/time/cost or equivalent guardrails. Bound exhaustion results in ESCALATED or FAILED, never silent recursion.

10. **ORCH-010 — User Continue/Resume is contextual.** Send starts a new turn. Stop requests cancellation of the active turn. Continue/Resume is shown only when the current turn is WAITING_USER or otherwise explicitly resumable.

## Canonical stages

The target execution lifecycle is:

INGRESS → PRECONDITION → EXECUTION → POSTCONDITION → AUDIT → RESPONSE → TERMINAL

Documentation must not claim a stage as implemented unless runtime code and tests enforce it.

## Supabase implementation

Production migration: `20260914034207_escd_orchestration_exchange_v1`

Existing canonical session/transcript structures are reused:

- `dcse_cp.conversations`
- `dcse_cp.conversation_turns`

New operational structures:

- `dcse_cp.escd_runtime_workers`
- `dcse_cp.escd_operation_turns`
- `dcse_cp.escd_operation_events`

The event ledger is append-only to authenticated users. Authenticated DCS may read; operational writes are performed by service-authorized orchestrator workers. RETURN events are rejected unless control and non-empty payload are both present.

## First durable packet

Bootstrap turn: `TURN-F8097456A9CE`

It requests inspection of the canonical task queue and return of the next runnable task/disposition/evidence without executing HOLD_DCS or STALE_RECONCILE work. The registered local worker `DCS-WINDOWS-OLLAMA-01` is intentionally OFFLINE until the worker software is wired and validated.

## Promotion criterion

The runtime side of these rules becomes fully implemented only after an end-to-end ESCD turn proves:

DCS request → durable turn → worker claim → provider request → provider RETURN(control+payload) → rule evaluation → response composition → durable response/transcript → UI display → terminal turn state.

