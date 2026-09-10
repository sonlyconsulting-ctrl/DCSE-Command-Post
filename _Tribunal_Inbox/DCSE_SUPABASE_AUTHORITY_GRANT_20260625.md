# DCSE SUPABASE AUTHORITY GRANT
**Doc ID:** DCSE-TRIBUNAL/AUTH-GRANT/SUPABASE/20260625-001
**Classification:** ACTIVE — AUTHORITY RECORD
**Issued by:** DCS (Level 0 Authority)
**Recipient:** Claude CP (CTO / Strategic Technical Architect)
**Date:** 2026-06-25
**Session scope:** This grant is session-scoped unless DCS issues a standing charter amendment.

---

## Grant Statement

DCS/DCSE hereby grants Claude CP direct execution authority over Supabase project activities via the connected Supabase MCP.

This grant authorizes Claude CP to:

- Execute SQL migrations via `apply_migration` against authorized Supabase projects
- Execute SQL queries via `execute_sql` for schema verification, confirmation queries, and inspection
- List tables, extensions, branches, and project state via MCP read tools
- Coordinate sub-agent execution of Supabase MCP tools where Claude CP issues the task and confirms the output

This grant does not authorize:

- Credential rotation or service key changes (AG/DBA path remains required)
- Deletion of production data or tables without a separate DCS authorization
- Execution against any Supabase project not explicitly named in a task packet
- PS schema population — ps_schema is a boundary layer; no PS content enters it without DCS Level 0 PS bridge authorization

---

## Active Project Authorization

**Remote project:** `nevgdyfpxdaloacuutal` (cp.sonlyconsulting.com backend)

Authorized for: Step 3 schema migrations (routing_log, dcse_rag_vectors, ps_schema) and all subsequent build steps in DCSE_CP_PROJECT_EXECUTION_SPEC_v1.0.md.

---

## Audit Trail Requirement

Per delegated authority rules, every Supabase MCP execution by Claude CP must be logged in CP_Session_Log.md with:
- Action taken
- SQL or tool used
- Confirmation result
- Date and session reference

AG reviews the CP_Session_Log.md audit trail entries at next AG session.

---

## Standing Record

This grant is posted to _Tribunal_Inbox for inclusion in the next git push and status announcement per DCS instruction.

**DCS Level 0 Authorization confirmed in session: 2026-06-25**
**Claude CP authority receipt: DCSE-TRIBUNAL/AUTH-GRANT/SUPABASE/20260625-001**
