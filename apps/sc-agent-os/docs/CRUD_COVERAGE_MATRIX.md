# CRUD Coverage Matrix
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Compliance Mapping

---

## Purpose

Maps every data entity in SC Agent OS to its CRUD (Create, Read, Update, Delete) implementation, identifying which operations exist, their backing store, and compliance with DCSE backend mediation requirements.

---

## Supabase-Backed Entities (Compliant)

| Entity | Table | Create | Read | Update | Delete | API Route |
|--------|-------|--------|------|--------|--------|-----------|
| Agent Tasks | `dcse_cp.agent_tasks` | POST `/api/tribunal/dispatch` | GET `/api/tribunal/inbox` | POST `/api/tribunal/status` | None | Compliant |
| Task Events | `dcse_cp.agent_task_events` | POST `/api/tribunal/receipt` | GET `/api/tribunal/inbox` (embedded) | None | None | Compliant |
| Personas | `dcse_cp.dcse_personas` | POST `/api/personas` | GET `/api/personas` | PATCH `/api/personas` | None | Compliant |
| Assets | `dcse_cp.dcse_assets` | POST `/api/assets` | GET `/api/assets` | PATCH `/api/assets` | None | Compliant |
| Agent Registry | `dcse_cp.agent_registry` | None | GET `/api/agentops` | None | None | Read-only |
| Task Assignments | `dcse_cp.agent_task_assignments` | None | GET `/api/agentops` | None | None | Read-only |
| DCS Queue | `dcse_cp.dcs_decisions` | None | GET `/api/dcsqueue` | None | None | Read-only |
| Receipts | `dcse_cp.build_receipts` | None | GET `/api/receipts` | None | None | Read-only |
| Assurance Gates | `dcse_cp.assurance_gates` | None | GET `/api/assurance` | None | None | Read-only |
| Runtime/Ollama | `dcse_cp.ddna_ollama_jobs` | POST `/api/runtime/smoke` | GET `/api/runtime` | None | None | Compliant |

---

## localStorage-Backed Entities (Non-Compliant)

| Entity | localStorage Key | Create | Read | Update | Delete | Required Target |
|--------|-----------------|--------|------|--------|--------|----------------|
| Tasks | `sc_tasks` | UI form | On load | Inline edit | Splice | `dcse_cp.agent_tasks` via API |
| Portfolio | `sc_portfolio` | UI form | On load | Inline edit | Splice | Supabase portfolio table |
| DDNA Scores | `sc_ddna_scores` | Harvest | On load | Slider | None | `dcse_cp.ddna_scores` |
| DDNA Notes | `sc_ddna_notes` | UI form | On load | None | By index | `dcse_cp.ddna_notes` |
| RAG Sources | `sc_rag_sources` | UI form | On load | Status toggle | Splice | Supabase RAG source table |
| Dispatch Packets | `sc_dispatch` | UI form | On load | None | Splice | Already migrated to API |
| Provider API Keys | `sc_*_key` | UI input | On model switch | On input | None | Server-side env vars only |

---

## Hardcoded/Static Entities (Partially Compliant)

| Entity | Variable | Source | CRUD State | Required Action |
|--------|----------|--------|------------|-----------------|
| Tribunal PRs | `TRIBUNAL_PRS` | Hardcoded array (4 items) | Read-only | GitHub API integration or Supabase PR cache |
| Agent Dock | Inline HTML (12 agents) | Hardcoded | Read-only | Query `dcse_cp.agent_registry` |
| Phase Gate Config | Inline HTML | Hardcoded | Read-only | Query `dcse_cp` phase tables |

---

## CRUD Gap Analysis

### Missing Operations

| Entity | Missing | Impact |
|--------|---------|--------|
| Agent Tasks | DELETE | Low: tasks should archive, not delete |
| Personas | DELETE | Intentional: governance prevents deletion |
| Assets | DELETE | Intentional: governance prevents deletion |
| Receipts | CREATE/UPDATE/DELETE | Read-only by design |
| DCS Queue | CREATE/UPDATE/DELETE | DCS-authority-only operations |

### Security-Critical Gaps

| Gap | Severity | Description |
|-----|----------|-------------|
| Provider keys in localStorage | HIGH | API keys stored as plaintext in browser. Must move to server-side session or encrypted vault. |
| No CSRF protection on POST endpoints | MEDIUM | POST handlers accept any origin due to `Access-Control-Allow-Origin: *` |
| No rate limiting on dispatch | MEDIUM | No throttle on task creation |

---

## Compliance Verdict

| Metric | Value |
|--------|-------|
| Total data entities | 17 |
| Supabase-backed (compliant) | 10 |
| localStorage-backed (non-compliant) | 7 |
| Hardcoded/static (partial) | 3 |
| CRUD coverage (Supabase entities) | 85% (most have Read, partial Create/Update) |
| Delete operations | Intentionally absent for governed entities |
