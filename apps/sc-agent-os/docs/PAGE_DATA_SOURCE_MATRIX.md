# Page Data Source Matrix
**Audit ID:** Code-Review-OS-Auth-Sources-20260716
**Entity:** SC
**Classification:** Compliance Audit

---

## Purpose

Maps every UI panel in SC Agent OS v1.3 to its data source, identifying which panels use authoritative backend (Supabase) versus browser-local storage (localStorage). Per DCSE doctrine, operational state must source from the authoritative database. Static labels and layout are acceptable as HTML constants.

---

## Panel Data Source Map

| Panel | Data Source | Storage Type | DCSE Compliant | Notes |
|-------|-----------|-------------|----------------|-------|
| Agent Chat + Voice | User input + LLM API response | Transient (session) | YES | Stateless relay via `/api/chat` |
| DDNA Harvest | localStorage (`sc_ddna_scores`, `sc_ddna_notes`) | Browser-local | NO | Scores and notes should persist in Supabase |
| RAG/Source | localStorage (`sc_rag_sources`) | Browser-local | NO | Source registry should be in Supabase |
| Task Queue | localStorage (`sc_tasks`) | Browser-local | NO | Must route through `dcse_cp.agent_tasks` |
| Portfolio | localStorage (`sc_portfolio`) | Browser-local | NO | Must use Supabase system of record |
| Tribunal | Hardcoded array (`TRIBUNAL_PRS`) | Static HTML | NO | Should query GitHub API or Supabase cache |
| Dispatch | Supabase via `/api/tribunal/dispatch` | Backend DB | YES | Full CRUD through API |
| Agent Dock | Static config (12 agents) | Static HTML | PARTIAL | Agent registry exists in `dcse_cp.agent_registry` but panel uses static list |
| Personas | Supabase via `/api/personas` | Backend DB | YES | Full CRUD |
| Assets | Supabase via `/api/assets` | Backend DB | YES | Full CRUD |
| Runtime Health | Supabase + Ollama via `/api/runtime` | Backend DB + live check | YES | Mixed authoritative sources |
| Runtime Smoke | Supabase via `/api/runtime/smoke` | Backend DB | YES | Writes smoke test results |
| DBA Console | Supabase via `/api/dba` | Backend DB | YES | Schema introspection |
| API Keys Admin | Supabase + env vars via `/api/apikeys` | Backend (server env) | YES | Server-side key status check |
| Assurance Loop | Supabase via `/api/assurance` | Backend DB | YES | A0-A8 gate checks |
| Agent Ops | Supabase via `/api/agentops` | Backend DB | YES | Agent task/event queries |
| Phase Gate Board | Static HTML + localStorage references | Browser-local | NO | Should query `dcse_cp` phase gate tables |
| DCS Queue | Supabase via `/api/dcsqueue` | Backend DB | YES | Decision queue |
| Receipts | Supabase via `/api/receipts` | Backend DB | YES | Evidence/receipt records |
| Config Console | Static HTML | Static | PARTIAL | Display-only, no CRUD |

---

## Compliance Summary

| Category | Count | Panels |
|----------|-------|--------|
| Fully Compliant (Backend DB) | 10 | Dispatch, Personas, Assets, Runtime, Smoke, DBA, API Keys, Assurance, Agent Ops, DCS Queue, Receipts |
| Partially Compliant | 2 | Agent Dock, Config Console |
| Non-Compliant (localStorage) | 6 | Task Queue, Portfolio, DDNA Harvest, RAG/Source, Phase Gate Board, Tribunal |
| Stateless (No persistence needed) | 1 | Agent Chat |

---

## localStorage Keys in Use (Client-Side)

| Key | Panel | Contains | Risk |
|-----|-------|----------|------|
| `sc_tasks` | Task Queue | Task objects (id, name, status, lane) | Operational data not in system of record |
| `sc_portfolio` | Portfolio | Portfolio items (id, name, url, status) | Build order not in system of record |
| `sc_ddna_scores` | DDNA Harvest | Numeric scores (8 dimensions) | Scoring data ephemeral across browsers |
| `sc_ddna_notes` | DDNA Harvest | Timestamped notes array | Audit trail not in system of record |
| `sc_rag_sources` | RAG/Source | Source objects (name, type, status) | Source registry not centralized |
| `sc_dispatch` | Dispatch | Dispatch packet objects | Redundant with Supabase (migration artifact) |
| `sc_anthropic_key` | Chat | Anthropic API key | **SECURITY: plaintext key in browser storage** |
| `sc_openai_key` | Chat | OpenAI API key | **SECURITY: plaintext key in browser storage** |
| `sc_google_key` | Chat | Google API key | **SECURITY: plaintext key in browser storage** |
| `sc_qwen_key` | Chat | Qwen/DashScope API key | **SECURITY: plaintext key in browser storage** |

---

## Static Data Arrays (Hardcoded in HTML)

| Variable | Panel | Contains | Should Source From |
|----------|-------|----------|--------------------|
| `TRIBUNAL_PRS` | Tribunal | 4 PR objects with title, branch, status, URL | GitHub API or Supabase PR cache |
| Default `tasks` array | Task Queue | 5 seed tasks | `dcse_cp.agent_tasks` |
| Default `portfolio` array | Portfolio | 4 seed items | Supabase portfolio table |
| Default `ragSources` array | RAG/Source | 4 seed sources | Supabase RAG source table |
| Default `dispatchPackets` array | Dispatch | 2 seed packets | `dcse_cp.agent_tasks` (already migrated) |
