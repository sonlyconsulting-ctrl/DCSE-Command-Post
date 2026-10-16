# CLAUDE.md — DCSE Command Post

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

---

## Operative v7.3 Governance, D15 Confinement & Authority

### 1. Canonical Governance Source
The canonical cross-product governance plane is **`sonlyconsulting-ctrl/DCSE-Control-Plane`** (`main`). Operative authority is **DCSE v7.3** (ratified by DCS Level 0 on 2026-09-20).

### 2. Authority`n- Only v7.3 is operative. All earlier material is archived, carries no authority, and must not be queried, read, written to, or referenced.`n- Approval record: `authority/decisions/v7.3/DCS_APPROVAL_V73_BASELINE_AND_D15_20261010.md` in DCSE-Control-Plane.`n`n### 3. Database Confinement Rules (Doctrine D15)
- **Target Project:** `nevgdyfpxdaloacuutal` (`SC-Command-Post`).
- **Mandatory Schema:** `dcse_cp` exclusively.
- **Mandatory Headers:** All queries and client calls must pass `'Accept-Profile': 'dcse_cp'` and `'Content-Profile': 'dcse_cp'`.
- **Prohibited Objects:** The PostgreSQL `public` schema and legacy table `public.dcse_asset_registry` are STRICTLY BANNED.
- **Fail-Closed Rule:** If a table or object is missing in `dcse_cp`, HALT IMMEDIATELY. Do NOT search `public`. Report the missing schema definition.
- **Asset Registration:** Master product and asset registers live in Git (`DCSE-Control-Plane/products/PRODUCT_AND_ENTITY_REGISTER.md`) and ESCD (`apps/escd/runtime/escd_canonical_convergence_registry.json`), NOT in legacy SQL tables.

### 4. Poller & Universal Dispatch Governance
- The legacy script `job_tribunal_poller_v7.py` is RETIRED. Do NOT attempt to run it or report Step 5 as blocked.
- The active runtime controller is `DCSE_DispatchController` running automatically on a 1-minute cadence.
- Inserting a record into `dcse_cp.poller_wake_requests` with `status = 'REQUESTED'` satisfies the wake requirement.

### 5. Operative Decision Workflow (The Authorized 4-Step Sequence)
Whenever a product, asset, or DCS decision is approved, execute this exact 4-step sequence:
1. **Step 1 — Evidence Artifacts:** Create Manifest, Receipt, and Summary in `tribunal/`.
2. **Step 2 — Git Commit & Push:** Commit and push artifacts to the designated branch.
3. **Step 3 — Supabase `dcse_cp` Task & Wake:** Insert active task into `dcse_cp.agent_tasks` and wake record into `dcse_cp.poller_wake_requests` (schema `dcse_cp` only).
4. **Step 4 — ESCD Co-Registration:** Register the item in `apps/escd/runtime/escd_canonical_convergence_registry.json` (`CANON-XXX`).
