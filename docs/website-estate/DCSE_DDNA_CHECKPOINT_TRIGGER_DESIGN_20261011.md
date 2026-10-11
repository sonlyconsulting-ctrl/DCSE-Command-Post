# DDNA checkpoint-trigger continuity design (candidate)
Task: DCSE-DDNA-CONTINUITY-AUDIT-20261011-01 | 2026-10-11 | V7.3 operative | Status: DESIGN RECORDED, RUNTIME NOT ENABLED

## DCS proposal
Participating AI models make incremental GitHub checkpoints and end-of-task/session updates; each accepted checkpoint initiates DDNA extraction and writes a run receipt even when no new signals. Intended benefits: coverage, observability, backlog detection and reduced idle database risk. User proposal is approved as direction for design; no unscoped production mutations.

## Architecture
1. Every participating runtime emits a versioned, idempotent checkpoint envelope with task ID, model/runtime identity, session/source locator, lane, source hash, sequence, event type, UTC time and allowed evidence pointers. Do not put full protected conversation text, credentials or PS evidence in GitHub.
2. GitHub checkpoint is a durable audit pointer, not the exclusive trigger. Authenticated webhook/queue enqueues an extraction job, and periodic reconciler discovers missed checkpoints, retries, dead letters and stale sessions. A GitHub Action can dispatch to a secured backend, never embed privileged Supabase keys in public artifacts or client code.
3. Worker validates authorization and lane, fetches approved source via secure broker, performs five-layer DDNA extraction, deduplicates on source/version/processor, stores candidate provenance, and returns receipt. Promotion is separately governed.
4. Receipt statuses: RECEIVED, RUNNING, SUCCEEDED_WITH_EXTRACTIONS, NO_NEW_SIGNALS, SKIPPED_POLICY, FAILED, TIMED_OUT. Include started_at, finished_at, source hash, extracted count, error class, retry count, worker version, persistence readback status. Never call timestamp-only run SUCCESS.
5. Independent scheduled synthetic checks measure database accessibility, worker heartbeats, queue lag, completed vs eligible session coverage, connections/storage/I-O and quotas; alert on failures. An idle heartbeat cannot guarantee prevention of hibernation or replace provider plan/availability guarantees.
6. No assumption that ChatGPT or every third-party AI model exposes automatic end-of-session hooks. Integrate each actual runtime separately; where absent, use task-level checkpoint with explicit capture coverage gap.

## Current evidence
SC Command Post DDNA extraction runs: 5, latest 2026-07-13; characteristics: 11, latest 2026-07-13; source queue: 129, latest 2026-08-07; conversation registry: 19, latest 2026-09-15. Queue status: 119 queued, 10 review. Dedicated DCSE-DDNA project management status ACTIVE_HEALTHY but SQL readback timed out 2026-10-11. These observations do not establish end-to-end continuity.

## Gates and DCL
Verify operative v7.3 manifest and task-routed D03/D05/D16/D21; identify canonical schema, producer hooks, GitHub Actions runner, Supabase RLS/service access, monitoring target, secrets custody, plan limits, backup and rollback. Stage through nonproduction, exercise no-new-signal and failed-worker paths, prove readback and independently validate before enabling production. No database, workflow, or deployment changes executed by this record. Status PARTIAL; DCS Level 0 retains reserved release authority.
