# Production Version Alignment Report
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Deployment Verification

---

## Current Deployment State

| Environment | Status | Version | Branch |
|------------|--------|---------|--------|
| Production | LIVE | SC Agent OS v1.3 (PR #8 merge) | `main` at `ad2f82d` |
| Preview | READY | SC Agent OS v1.3 + PR #9 | `claude/dcs-packet-trial-confirm-jwuzsy` at `9f174fe` |

---

## Production (main) Contents

Merged via PR #8 (squash merge `ad2f82d`):

| Component | Present | Version |
|-----------|---------|---------|
| SC Agent OS v1.3 full rewrite | YES | Baseline |
| 19 UI panels | YES | All functional |
| Multi-provider chat proxy | YES | Anthropic, OpenAI, Gemini, Qwen, Ollama |
| Personas API | YES | Full CRUD |
| Assets API | YES | Full CRUD |
| Runtime Health API | YES | GET + smoke test |
| Agent Ops API | YES | Read-only |
| DBA Console API | YES | Schema introspection |
| API Keys Admin API | YES | Server-side status check |
| Assurance Loop API | YES | A0-A8 gate checks |
| DCS Queue API | YES | Decision queue |
| Receipts API | YES | Evidence records |

---

## Preview (PR #9) Delta

Changes in PR #9 not yet in production:

| Component | Change | Files |
|-----------|--------|-------|
| Tribunal Dispatch API | NEW: 4 endpoints (inbox, dispatch, receipt, status) | `index.js` |
| Input validation order | FIX: validate before DB check in POST handlers | `index.js` |
| Root Vercel config | NEW: rewrites for API routing | `vercel.json` |
| Root API proxy | NEW: re-exports handler for Vercel function detection | `api/index.js` |
| Migration 005 | Security remediation SQL | `migrations/005_*` |
| Migration 006 | Move vector extension to extensions schema | `migrations/006_*` |
| Security disposition | Documentation of residual findings | `docs/IMPLEMENTATION_STATUS.md` |
| CLAUDE.md | Agent review/test instructions | `CLAUDE.md` |
| .gitignore | Exclude node_modules and env files | `.gitignore` |

---

## Supabase Schema Alignment

| Schema Object | Supabase State | Code References | Aligned |
|--------------|----------------|-----------------|---------|
| `dcse_cp.agent_tasks` | LIVE (24 columns) | `handleTribunalInbox/Dispatch/Status` | YES |
| `dcse_cp.agent_task_events` | LIVE | `handleTribunalReceipt` | YES |
| `dcse_cp.agent_task_assignments` | LIVE | `handleAgentOps` | YES |
| `dcse_cp.agent_registry` | LIVE | `handleAgentOps` | YES |
| `dcse_cp.dcse_personas` | LIVE (6 seeds) | `handlePersonas` | YES |
| `dcse_cp.dcse_assets` | LIVE (7 items) | `handleAssets` | YES |
| `dcse_cp.ddna_ollama_jobs` | LIVE | `handleRuntime` | YES |
| `dcse_cp.assurance_gates` | LIVE | `handleAssurance` | YES |
| Migration 005 | APPLIED | Security remediation | YES |
| Migration 006 | APPLIED | vector extension move | YES |

---

## Vercel Configuration Alignment

| Setting | Value | Status |
|---------|-------|--------|
| Project ID | `prj_a9pbcrfvQczbmH2Cr1S2Q08p2975` | Verified |
| Team | `sonlyconsulting-ctrls-projects` | Verified |
| Root directory | Not set (uses repo root) | Requires root `vercel.json` + `api/index.js` proxy |
| `SUPABASE_URL` | Set in Vercel env vars | Verified |
| `SUPABASE_SERVICE_ROLE_KEY` | Set in Vercel env vars | Verified |
| Deployment Protection | SSO enabled on previews | Active |
| Production domains | `sonlyconsulting.com`, `www.sonlyconsulting.com` | Active |

---

## Version Alignment Gaps

| Gap | Severity | Description |
|-----|----------|-------------|
| PR #9 not merged | MEDIUM | Tribunal dispatch API, validation fixes, and Vercel routing not in production |
| Tribunal PR list hardcoded | LOW | `TRIBUNAL_PRS` array shows stale PR data vs live GitHub state |
| localStorage panels vs Supabase | HIGH | 6 panels use browser storage instead of authoritative DB |
| Agent Dock vs agent_registry | LOW | Static 12-agent list vs dynamic `dcse_cp.agent_registry` |

---

## Merge Readiness (PR #9)

| Check | Status |
|-------|--------|
| Vercel Preview builds | PASSING (Ready) |
| Local API validation (10/10) | PASSING |
| Supabase E2E lifecycle | PASSING |
| Merge conflicts | NONE |
| PR state | Draft (requires DCS to mark ready + merge) |
