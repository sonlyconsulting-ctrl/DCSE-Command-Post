# CLAUDE.md — DCSE Command Post

## v7.1 Governance Mandate (Read First — Applies to Every Session)

This section binds every Claude Code session that touches this repository — new conversations and continued ones alike. It is not a reminder to be re-negotiated per chat; it is a standing instruction, same as the rest of this file.

**The six doctrines, and what each one requires of this session specifically** (this D1–D6 labeling is the working set this file uses operationally; as of 2026-08-05 it has not been found registered in `dcse_cp.governance_directives` — see "DDNA authority" below before treating it as DCS-ratified):

1. **D1 — Atomic Single-Instance Lease.** Before claiming or acting on a Tribunal task, check for an existing lease/lock rather than assuming none exists.
2. **D2 — Heartbeat Separation.** State transitions get logged as they happen, independently per task — not reconstructed after the fact from memory.
3. **D3 — Policy Routing.** Task eligibility comes from the policy table (`get_eligible_policy_tasks` or equivalent), never from a hardcoded allowlist in this session's own reasoning.
4. **D4 — Provider Failure Handling.** A failed or timed-out step is reported as failed. It is never silently upgraded to "completed" to make a task look finished.
5. **D5 — Idempotency.** Before writing a receipt or marking anything complete, check whether a terminal receipt already exists for that task. Re-running work must not fabricate a second, different outcome.
6. **D6 — State Machine Transitions.** Every state change is written to a receipt file or DB row at the time it happens, with a timestamp — not summarized afterward as a narrative.

**The rule underneath all six, stated plainly:** a claim of "done," "verified," "passed," or "complete" is only true in this project if it is backed by something checkable — a receipt file, a Supabase row, a command's actual output, a rendered screenshot. If it isn't checkable, say what's actually known and what isn't, instead of asserting completion. This project has already had one incident (documented in `tribunal/v7/runtime-evidence/`) of an agent (Qwen) reporting task completion it had not performed. Do not repeat that failure mode. When resuming after context compaction, re-derive status from evidence files and Supabase state, not from a summarized recollection of what was "probably" done.

**Where to check governance state before starting new work:**
- `tribunal/v7/runtime-evidence/` — B1-* evidence files and receipt JSON.
- `tribunal/v7/BOW-*` — completed Bounded Outcome Work packages and their findings.
- Supabase `dcse_cp` schema, `agent_tasks` / `agent_task_events` tables — live task and event state.
- Governance branch: `governance/v7.1-promotion-metadata-reconciliation`.

**Scope and limits, stated honestly:** this file is read automatically by any Claude Code session working in this repository, which makes it a durable mechanism for Claude specifically. It has no effect on other models or tools (Qwen, Codex, or any other agent) unless a human explicitly gives it to them — this file cannot reach across tools on its own. For any claim made by a non-Claude agent, verify it the same way this section requires Claude to verify its own claims: against a receipt, a DB row, or other checkable evidence, not against the agent's self-report. Where a doctrine can be enforced mechanically instead of relying on any agent's compliance — e.g. `trg_enforce_task_completion_contract` at the database layer — prefer that over instruction-following every time.

**DDNA authority, and what "the truth" actually requires here:** per `01_GOVERNANCE/DCSE_GOVERNANCE_MILESTONE_DDNA_HUB_ACTIVATION_20260709.md` (Rule 003, "Single Authority Reference Model"), canonical governance directives reside in DCSE-DDNA — the `dcse_cp.governance_directives` table and related DDNA objects in this same Supabase project (`nevgdyfpxdaloacuutal`). This file is an operational reference and pointer, not a competing source of authority, and must not be treated as one.

That authority is conditional on ratification, not automatic by virtue of living in a DDNA-labeled table. **Current state as of 2026-08-08 (verified against live DB):** `dcse_cp.governance_directives` contains D01-D22 all promoted, a `MASTER_PROFILE` row at `status: operative` / `promotion_status: OPERATIVE` designating DCSE Master Profile v7.2 R4, and `MP72_POLLER_SESSION_RUNTIME` at `status: promoted`. `dcse_cp.ddna_characteristics` is a separate table holding SC brand-voice extraction rules, not governance doctrine. Always query the DB directly rather than relying on this file's snapshot — the state has changed substantially since earlier sessions.

**D17 identity (corrected):** The canonical D17 is `D17 -- DART Universal Assurance Methodology` (promoted in DB, source file `governance/v7.1/source/doctrines/D17_DART_Universal_Methodology.md`). The file at `docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md` carries an incorrect D17 label — its subject (Supabase security implementation) is a separate doctrine that needs its own identifier. Do not cite the `docs/governance/` file as authoritative for D17; cite the DB row and the `governance/v7.1/source/doctrines/` file.

**D1–D6 operational poller doctrines (CLAUDE.md runtime set) are still not separately registered** in `dcse_cp.governance_directives`. Those six doctrines (Atomic Lease, Heartbeat Separation, Policy Routing, Provider Failure Handling, Idempotency, State Machine Transitions) are distinct from the enterprise governance set D01-D22 and have no individual DB rows. They remain operative only as CLAUDE.md instructions and `MP72_POLLER_SESSION_RUNTIME` doctrine.

The operating rule this implies: DDNA outranks this file or any other repository's governance claim once a directive is actually promoted — a `candidate` or `observed` row is a proposal, not settled doctrine, and must be verified against its live `status`/`promotion_status` before being relied on, the same as any other unverified claim this file requires checking. Query `dcse_cp.governance_directives` directly (Supabase MCP) rather than assuming its contents from this file's snapshot.

## Project Overview

SC Agent OS v1.3: a single-file Vercel serverless Node.js application serving both API endpoints and a full HTML/CSS/JS dashboard UI. The entire application lives in `apps/sc-agent-os/api/index.js` (~2750 lines). A root `api/index.js` proxy re-exports it for Vercel's function detection.

**Stack:** Node.js serverless function on Vercel, Supabase (PostgreSQL + RLS), no framework, no bundler, no test runner currently configured.

**Supabase project:** `nevgdyfpxdaloacuutal` — schema `dcse_cp` with 24 tables.

## Repository Layout

```
api/index.js                    # Root proxy: re-exports apps/sc-agent-os/api/index.js
vercel.json                     # Root Vercel config (rewrites all routes to /api)
apps/sc-agent-os/api/index.js   # THE application (all handlers + full HTML UI)
apps/sc-agent-os/migrations/    # SQL migrations 001-006
apps/sc-agent-os/docs/          # Governance docs, specs, implementation status
01_GOVERNANCE/                  # DCS governance artifacts
02_ARCHITECTURE/                # Architecture docs
03_WORK_ORDERS/                 # Build orders
```

## Code Review Instructions

### Architecture

The app is a single `module.exports` handler that routes by URL pathname. Each route calls a `handle*` function. The HTML UI is a template literal (`const HTML`) embedded in the same file.

Key handler functions and their API routes:
- `handleChat` — `/api/chat` (multi-provider LLM proxy)
- `handleTribunalInbox` — `/api/tribunal/inbox` (GET: task list + stats)
- `handleTribunalDispatch` — `/api/tribunal/dispatch` (POST: create task)
- `handleTribunalReceipt` — `/api/tribunal/receipt` (POST: record event)
- `handleTribunalStatus` — `/api/tribunal/status` (POST: update task status)
- `handleRuntime` — `/api/runtime` (GET: runtime health)
- `handleRuntimeSmoke` — `/api/runtime/smoke` (POST: smoke test)
- `handlePersonas` — `/api/personas` (CRUD)
- `handleAssets` — `/api/assets` (CRUD)
- `handleAgentOps` — `/api/agentops` (GET: agent operations)
- `handleDBA` — `/api/dba` (GET: database admin)
- `handleAPIKeys` — `/api/apikeys` (GET: API key status)
- `handleAssurance` — `/api/assurance` (GET: assurance loop)
- `handleDCSQueue` — `/api/dcsqueue` (GET: DCS decision queue)
- `handleReceipts` — `/api/receipts` (GET: receipts/evidence)

### What to Check in Code Review

1. **Input validation before DB access** — All POST handlers must validate required fields BEFORE checking `SUPABASE_KEY`. Bad payloads should get 400, not 503.

2. **SQL injection** — All Supabase queries use the `@supabase/supabase-js` client (parameterized). Verify no raw string interpolation into SQL.

3. **Secret exposure** — `SUPABASE_SERVICE_ROLE_KEY` and provider API keys must never appear in:
   - The HTML template literal
   - Console.log output
   - API response bodies
   - Error messages sent to clients

4. **CORS headers** — All handlers set `Access-Control-Allow-Origin: *`. Review whether this is appropriate for each endpoint.

5. **Status codes** — Verify correct HTTP status codes:
   - 200 for successful GET
   - 201 for successful POST that creates a resource
   - 400 for validation failures
   - 503 for missing database connection
   - 500 for unhandled errors

6. **Supabase column names** — The `dcse_cp.agent_tasks` table uses `created_by_label` (not `created_by`) and `dcse_cp.agent_task_events` uses `event_summary` (not `summary`). The API code maps between request body field names and DB column names.

7. **Valid enums** — Verify that status and lane values match the allowed sets:
   - Lanes: `DCSE, PS, SC, SS, TSL, TRIBUNAL, DDNA, RAG, SYSTEM`
   - Statuses: `planned, assigned, running, blocked, completed, needs_review, handoff_ready, parallel_review, awaiting_dcs, approved, rejected, archived`

8. **Error handling** — Each handler wraps DB operations in try/catch and returns JSON error responses. Verify no stack traces leak to clients.

### What NOT to Flag

- The single-file architecture is intentional (Vercel serverless constraint).
- The inline HTML template is intentional (no build step needed).
- `Access-Control-Allow-Origin: *` is currently accepted for preview deployments.
- External font CDN links in the HTML are accepted.

## Testing Instructions

### Local API Testing (No Network Required)

Start the server locally:
```bash
cd apps/sc-agent-os
node -e "
const http = require('http');
const handler = require('./api/index.js');
http.createServer(handler).listen(3000, () => console.log('http://localhost:3000'));
"
```

Note: Without `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` env vars, DB-dependent endpoints return 503. Input validation tests still work.

### Test Matrix (10-Point Validation)

Run these against `http://localhost:3000`:

| # | Test | Method | Endpoint | Expected |
|---|------|--------|----------|----------|
| 1 | Inbox returns stats | GET | `/api/tribunal/inbox` | 200 with `stats` object |
| 2 | Dispatch without DB | POST | `/api/tribunal/dispatch` | 503 (no DB) with valid payload |
| 3 | Missing title | POST | `/api/tribunal/dispatch` | 400 `title required` |
| 4 | Invalid status value | POST | `/api/tribunal/status` | 400 `Invalid status` |
| 5 | Missing task_id on status | POST | `/api/tribunal/status` | 400 `task_id and status required` |
| 6 | Missing status field | POST | `/api/tribunal/status` | 400 `task_id and status required` |
| 7 | Malformed JSON body | POST | `/api/tribunal/dispatch` | 500 |
| 8 | Runtime health | GET | `/api/runtime` | 200 |
| 9 | Dependency failure msg | GET | `/api/runtime` | Response contains dependency info |
| 10 | UI HTML serves | GET | `/` | 200 with HTML containing `SC Agent OS` |

### Example curl Commands

```bash
# Test 1: GET inbox
curl -s http://localhost:3000/api/tribunal/inbox | jq .

# Test 3: Missing title (expect 400)
curl -s -X POST http://localhost:3000/api/tribunal/dispatch \
  -H 'Content-Type: application/json' \
  -d '{"lane":"SYSTEM"}' | jq .

# Test 4: Invalid status (expect 400)
curl -s -X POST http://localhost:3000/api/tribunal/status \
  -H 'Content-Type: application/json' \
  -d '{"task_id":"00000000-0000-0000-0000-000000000000","status":"bogus"}' | jq .

# Test 7: Malformed JSON (expect 500)
curl -s -X POST http://localhost:3000/api/tribunal/dispatch \
  -H 'Content-Type: application/json' \
  -d 'not json' | jq .

# Test 10: UI serves
curl -s http://localhost:3000/ | grep -o 'SC Agent OS'
```

### E2E Testing Against Supabase

For full lifecycle testing with a live Supabase connection, set env vars and run:

```bash
export SUPABASE_URL=https://nevgdyfpxdaloacuutal.supabase.co
export SUPABASE_SERVICE_ROLE_KEY=<key from Vercel env vars>
```

Then test the full dispatch lifecycle:
1. POST `/api/tribunal/dispatch` with title, lane, task_type, priority
2. Verify task appears in GET `/api/tribunal/inbox`
3. POST `/api/tribunal/status` with `status: assigned`, then `running`
4. POST `/api/tribunal/receipt` with `event_type: completed`
5. Verify final state in GET `/api/tribunal/inbox`
6. Clean up test records via Supabase MCP `execute_sql`

### Playwright UI Testing

Playwright is available for browser-based testing. Use the pre-installed Chromium:

```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  args: ['--no-sandbox']
});
```

UI tests should verify:
- Dashboard loads with "SC Agent OS" title
- Each panel button activates its corresponding panel
- No browser console errors on panel activation
- Dispatch panel renders form fields
- Agent Ops panel renders agent table

### Vercel Preview Testing

Preview deployments have Vercel Deployment Protection (SSO). To test previews:
- Use `mcp__Vercel__get_access_to_vercel_url` to obtain a share token
- Authenticate via `?_vercel_share=<token>` query parameter
- Note: The environment proxy may block direct HTTPS to `.vercel.app` domains

## Security Constraints (Enforced)

- No secrets in client code, logs, GitHub, or CP task payloads
- Provider credentials and SUPABASE_SERVICE_ROLE_KEY must remain server-side
- An agent may not approve its own output, promote a persona, or bypass DCS authority
- No direct-to-main push without DCS authorization
- No PS content in any dispatch or build
- No family or minor content in public GitHub repositories

## Deployment

- **Vercel project:** `sc-command-post` (prj_a9pbcrfvQczbmH2Cr1S2Q08p2975)
- **Team:** sonlyconsulting-ctrls-projects
- **Required env vars:** `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`
- **Production domains:** sonlyconsulting.com, www.sonlyconsulting.com
- Root `vercel.json` rewrites all routes to `/api`
- Root `api/index.js` proxies to `apps/sc-agent-os/api/index.js`

## Branch Policy

- Feature branches: `claude/<descriptor>`
- PRs target `main`
- Squash merge only
- No force push to main
