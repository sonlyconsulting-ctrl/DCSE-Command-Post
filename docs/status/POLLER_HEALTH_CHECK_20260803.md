# Poller Health Check

Check date: `2026-08-03`
Reporting node: `Claude Code (cloud session)`
Authority: `DCS/DCSE`
Classification: `DCSE Internal / Runtime Health / PS Firewall Active`
Sources: GitHub (`sonlyconsulting-ctrl/DCSE-Command-Post`), Supabase (`nevgdyfpxdaloacuutal`)

## 1. Scope Note

No component literally versioned `v7.1` exists in the repository or in Supabase. The versioned worker/poller system present is `v7` (schema `v7_worker`, migrations dated 2026-07-27) plus a `v7.0` build-control/convergence archive (`v7.0/00_BUILD_CONTROL/`). This report is scoped to that `v7` runtime. If a distinct `v7.1` poller exists outside GitHub/Supabase (e.g. on the Windows Command Center host), it was not reachable from this cloud session and is not covered below.

Two independent poller mechanisms were found and checked:

1. **`v7_worker` task-claim poller** — the Node.js worker in `workers/claude-reviewer-operational.js`, which polls `v7_worker.claim_next_task` every `WORKER_POLL_MS` (default 30s) and sends a heartbeat every `WORKER_HEARTBEAT_MS` (default 15s) via the `v7_worker_heartbeat` RPC into `v7_worker.heartbeat` / `v7_worker.agent_identity`.
2. **`dcse_cp` relay-listener heartbeat poller** — an externally-driven heartbeat feed into `dcse_cp.agent_heartbeats` / `dcse_cp.relay_listener_events`, keyed by `agent_key` (`claude_code`, `codex`, `chatgpt`). No source code implementing this feed's self-heal/monitor logic exists in this repository; it is written by a process outside the codebase.

## 2. Verified — `v7_worker` Poller

| Agent identity | Registry status | Last heartbeat | Age at check time |
|---|---|---|---|
| `AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY` | **suspended** | 2026-08-03 07:46:58Z | ~17 min |
| `AGENT-QWEN-CODER-01@LAPTOP-PRIMARY` | approved | never | — |
| `AGENT-DETERMINISTIC-VALIDATOR-01@LAPTOP-PRIMARY` | approved | never | — |

Finding: `AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY` is actively sending heartbeats (`status: idle`, ~1/min cadence, consistent with the worker script) even though its `agent_identity.status` is `suspended`. A suspended worker actively polling is a governance discrepancy — `v7_worker.claim_next_task` should be confirmed to reject claims for suspended identities; heartbeating alone does not claim tasks, but the live liveness signal contradicts the suspended state and should be reconciled or explained.

The Qwen Coder and Deterministic Validator worker identities are registered/approved but have **no heartbeat on record** — their pollers have not started in this environment. This matches Issue #17's note that "current local v7 worker identities have no recent heartbeat" for those roles.

## 3. Verified — `dcse_cp` Relay-Listener Heartbeat Poller

Current state (`dcse_cp.agent_heartbeats`, most recent row per agent):

| agent_key | heartbeat_status | last_seen_at | notes |
|---|---|---|---|
| `claude_code` | **degraded** | 2026-08-03 07:57:05Z | `poller_monitor: stale_heartbeat_detected`, `staleness_seconds: 607`, `self_healed: false` |
| `codex` | result_submitted | 2026-07-28 21:01:14Z | ~5 days stale |
| `chatgpt` | online | 2026-07-09 06:18:09Z | ~25 days stale; listener noted as `manual_sql_poll` |

Trailing-24h event volume for `claude_code` (`dcse_cp.relay_listener_events`, 174 heartbeat events total):

| Status | Count | Share |
|---|---|---|
| online | 164 | 94.3% |
| degraded | 5 | 2.9% |
| working | 3 | 1.7% |
| result_submitted | 2 | 1.1% |

Finding: the `claude_code` poller is healthy the large majority of the time, but its **most recent recorded state is `degraded`**, and the row's own embedded self-heal monitor reported it detected the stale heartbeat and did **not** recover automatically (`self_healed: false`). This is the current, unresolved condition as of the check.

`codex` and `chatgpt` heartbeats are days-to-weeks old. Per Issue #17 these are on-demand/cloud-sandbox agents rather than always-on daemons, so staleness alone is not necessarily a fault — but neither shows a graceful "stopped"/"offline" terminal state, so they cannot be distinguished from a silently-dead poller using this table alone.

## 4. Assessment

- No poller is fully down; the `v7_worker` claim-poller for the Claude architecture role and the `dcse_cp` heartbeat poller for `claude_code` are both actively reporting.
- One live defect: the `claude_code` relay-listener heartbeat is currently in `degraded`/unresolved status with `self_healed: false` and no code in this repository implements the recovery logic that row references — the self-heal capability is either external or not yet built.
- One governance discrepancy: `AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY` is heartbeating while its registry status is `suspended`.
- Two pollers (Qwen Coder, Deterministic Validator) have never reported — expected if those workers have not been started in this environment, but unverified either way from here.

## 5. Recommended Next Actions

1. DCS/operator to confirm on the Windows Command Center host whether the `claude_code` degraded/self-heal-failed condition has since cleared, since this cloud session cannot reach that host directly.
2. Reconcile the `suspended` status vs. active heartbeats for `AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY` — either the suspension should stop the heartbeat loop, or the registry status is stale and should be updated.
3. If a `v7.1` poller revision is intended, confirm its location (this repo, Tribunal Relay repo, or local-only) so a future check can cover it directly.

No secrets, credentials, or PS content were read or written in the course of this check.
