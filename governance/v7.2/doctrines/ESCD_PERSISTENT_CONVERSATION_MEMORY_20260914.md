# ESCD Persistent Conversation, Classification, and Subject Memory

**Directive ID:** ESCD-MEMORY-20260914-001  
**Authority:** DCS explicit direction, 2026-09-14  
**Status:** OPERATIVE-PATCH requirement  
**Lane:** DCSE / ESCD / Rules Engineering

## Purpose

ESCD conversations are not disposable chat transcripts. They are durable evidence streams that may produce governed tasks, ideas, knowledge, assets, DDNA candidates, decisions, projects, subject relationships, and operational turns.

## Locked behavior

1. **Every meaningful Send or Orchestrate user turn is persisted.** The browser is a surface, not the source of truth.
2. **Conversation and operation remain distinct objects.** Conversation preserves what was said. Operation preserves what the system did with a request.
3. **Closing a browser session does not destroy the conversation.** Authorized users recover prior conversations through ESCD History and resume from the persisted transcript.
4. **Classification does not force every message into a Task.** Valid primary categories are CHAT_ONLY, TASK, IDEA, KNOWLEDGE, ASSET, DDNA, DECISION, and PROJECT.
5. **Greetings and ordinary questions may remain CHAT_ONLY.** Persistence does not imply promotion.
6. **Automatic materialization is currently limited to high-confidence TASK, IDEA, and KNOWLEDGE classifications.** Threshold: 0.85 unless explicitly overridden by DCS.
7. **ASSET, DDNA, DECISION, and PROJECT classifications remain candidates until their domain-specific creation rules are completed.**
8. **Subject resolution precedes build-on reasoning where possible.** A request such as "Vow & Go" resolves to the persistent subject anchor and its linked task/evidence instead of starting from zero.
9. **Facts and frames remain separate.** A conversation turn, a classification, a subject, and a materialized object are different records linked by provenance.
10. **Repeated discussion does not by itself create duplicate operational objects.** Object materialization requires an explicit durable-object signal, not merely use of the Orchestrate button.
11. **Provider/model output is candidate reasoning until accepted by the Orchestrator and applicable rules.**
12. **No synthetic provider success may be presented as real provider inference.** Offline simulation must not be used in production evidence.
13. **Final responses and provider/tool returns are persisted with control, payload, evidence references, rule evidence, provider/model/worker identity, and terminal state.**
14. **History is part of the operating model.** A reopened conversation must reconstruct transcript, classifications, subjects, and prior operation turns from Supabase.

## Canonical database objects

Transcript:
- `dcse_cp.conversations`
- `dcse_cp.conversation_turns`

Operational control:
- `dcse_cp.escd_operation_turns`
- `dcse_cp.escd_operation_events`
- `dcse_cp.escd_runtime_workers`

Build-on memory:
- `dcse_cp.escd_subjects`
- `dcse_cp.escd_subject_links`
- `dcse_cp.escd_turn_classifications`
- `dcse_cp.escd_knowledge_records`

## First subject anchor

`Vow & Go` is the first explicit subject anchor.

Aliases include:
- vow and go
- vow n go
- vow go
- ss vow and go
- ss vow n go

The subject is linked to the existing ESCD item `347cb648-6140-40f2-91b5-8a0639fc21e8` ("SS Vow and Go").

## Retrieval rule

When a new turn resolves to an existing subject, the Orchestrator should retrieve prior subject links, relevant active items, durable knowledge, prior operations, and evidence before generating a new response.

## Acceptance

A browser may close and reopen. After reauthentication, ESCD History must locate the conversation, restore the transcript, retain its subject links/classifications, and permit a new governed turn to build on prior state without relying on browser memory.
