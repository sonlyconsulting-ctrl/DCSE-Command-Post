# Runtime adapter requirements for autonomous polling (Codex, desktop clients)

Written under task_key=V7_1_POLLER_RESULT_ACCESS_UI_FIX_20260807. Answers: what
would it take for Codex and desktop clients to poll `dcse_cp` without producing
false heartbeats or duplicate claims, given the runtime-identity fix in
migrations 007/008 (`runtime_surface` / `runtime_instance` / `host` / `session_id`
on `dcse_cp.agent_heartbeats`, threaded through `agent_heartbeat`,
`claim_agent_assignment`, and `submit_agent_result`).

## Current state (as of this task)

- **Claude Code CLI on Windows host** — the only verified autonomous poller.
  `v7.0/09_WORKERS/claude_code_poller.ps1`, registered under Windows Task
  Scheduler (`Register-ClaudeCodePollerTask.ps1`), runs every ~60s, heartbeats
  with `runtime_surface='cli_windows_poller'`, claims work via
  `claim_agent_assignment`, executes `claude -p` unattended, and reports
  through `submit_agent_result`. Credentials come from a DPAPI CurrentUser
  bundle scoped to this host/user only.
- **ChatGPT** — on-demand connector only. Does not autonomously poll; a human
  or another system invokes it per-request. No heartbeat identity needed
  because it never claims a `dcse_cp` assignment on its own initiative.
- **Codex** — has an `agent_registry` row (`agent_key='codex'`) and has
  submitted at least one heartbeat/result historically, but there is no
  scheduled process anywhere in this repo that invokes it autonomously. It is
  registered but not live.
- **Claude Chat (browser) / Claude Desktop** — interactive-only today. No
  poller exists for either.

## What a Codex adapter needs

Codex is a distinct **logical agent role** (`agent_key='codex'`), not another
runtime surface of `claude_code`, so it does not reuse `claude_code`'s
`agent_registry` row. To go from "registered" to "actually polling" it needs:

1. **A scheduled invoker analogous to `claude_code_poller.ps1`.** Same shape:
   read `dcse_cp.get_agent_inbox(p_agent_key='codex')`, run the same gate
   checks (lane authorization, `dcs_decision_required`, confidentiality,
   stop-gates, retry/concurrency caps), claim via `claim_agent_assignment`,
   invoke the Codex CLI/API non-interactively with a wall-time bound, and
   report via `submit_agent_result`. The gating logic, not runtime trust, is
   what keeps this safe unattended — that principle carries over unchanged.
2. **Its own credential scope**, not a copy of the Claude worker's DPAPI
   bundle. `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` can be shared (same
   project), but whatever invokes the Codex CLI (an OpenAI/Codex API key or
   local session) must be provisioned and stored separately, following the
   same "narrow scope, host-local secret store" pattern the poller comment
   block documents.
3. **`runtime_surface` values of its own.** The check constraint added in
   migration 007 only enumerates Claude-family surfaces
   (`cli_windows_poller`, `remote_cloud_ccr`, `chat_browser`, `desktop_app`,
   `worker_v7`, `unspecified`) because that's what this task scoped. Before a
   Codex poller goes live, extend that CHECK constraint (or generalize it to
   a lookup table) with Codex-appropriate values, e.g. `codex_cli_scheduled`,
   `codex_api_ondemand`. Do not reuse a Claude `runtime_surface` value for a
   different `agent_key` — the whole point of separating logical role from
   runtime surface is that each (agent_key, runtime_surface) pair means one
   specific thing.
4. **A `runtime_instance` that is unique per host/process**, exactly like the
   poller's `cli_windows_poller@$COMPUTERNAME`, so if a second Codex poller is
   ever stood up on a second host, both show up as distinct rows in
   `dcse_cp.agent_runtime_surfaces` instead of overwriting each other — that
   was the whole failure mode this task fixed for Claude.

## What desktop clients (Claude Desktop, and by extension a hypothetical Codex
## desktop client) need

Desktop/chat clients are **interactive by nature** — a human is present. They
should not be wired into the unattended-polling path at all:

1. **No Task Scheduler / cron entry.** An interactive session should only
   call `agent_heartbeat` / `claim_agent_assignment` when a human explicitly
   drives it to (e.g. DCS opens Claude Desktop and asks it to check the
   inbox), not on a timer. Otherwise a desktop app left open becomes an
   accidental second poller for the same lane.
2. **`runtime_surface='desktop_app'`** (or `'chat_browser'` for the browser
   surface) on every heartbeat/claim/submit call it does make, so the
   Command Center can see "this task was worked interactively from a desktop
   session," never conflated with the CLI poller's automated runs.
3. **A distinct `runtime_instance` per device/session** (e.g.
   `desktop_app@<device-id>:<session-id>`), not a static value, so two people
   (or one person on two machines) both running Claude Desktop don't collide
   under one row.
4. **The `max_concurrent_tasks=1` / claim-timeout gates still apply per
   agent_key**, so an interactive desktop claim and the CLI poller's
   automated claim cannot both be "running" for `claude_code` at once —
   `claim_agent_assignment`'s atomic UPDATE already enforces this at the
   assignment level; the runtime-identity fix in this task makes it visible
   *which* surface holds the claim, it doesn't change who's allowed to hold
   it.

## Summary

No autonomous poller should exist for ChatGPT (by design), Claude Chat, or
Claude Desktop today. Codex needs a new scheduled adapter script (Codex's own
version of `claude_code_poller.ps1`) plus a `runtime_surface` vocabulary
extension before it can safely poll unattended. Until that adapter exists,
Codex's `agent_registry` row should be treated as registered-but-dormant, and
the Command Center UI should not show it as an active autonomous poller.
