# GOTIME CP DASHBOARD SECURITY REWORK REPORT

**Ref:** GoTime Phase 4 Security Hardening  
**Date:** 2026-07-02  
**Status:** COMPLETED SPECIFICATIONS  

---

## 1. Identified Vulnerability (App-Layer Redaction Failure)
In the initial read-only implementation of `/cp/gotime`, the dashboard component (`page.tsx`) fetched records directly from the database using:
```typescript
const { data } = await supabase.from('pm_projects').select('*');
```

This client-side request was identified as unsafe because:
1.  **Direct Database Pull:** It pulled all rows (including PS-lane rows) and all columns directly into the browser memory.
2.  **Cosmetic Redaction:** The React UI visually replaced PS details with labels like `[LOCKED PS CASE OUTLINE]`. However, the full unredacted JSON payloads remained visible in the browser's developer tools (Network and State tabs).
3.  **Credential Dependency:** Relying solely on RLS for client-side queries creates a single point of failure. If the database policies are misconfigured (e.g. standard `USING (true)` select policy), the browser gains access to sensitive data immediately.

---

## 2. Implemented Mitigation (Layered Defense Model)
To eliminate this risk, we have redesigned the data flow to enforce a **layered defense** structure:

```
[Browser Client]
       │
       ▼  Fetch /api/gotime/dashboard (Column Allowlist Only)
[Next.js Server API]
       │
       ▼  Filter: lane IS DISTINCT FROM 'PS'
[PostgreSQL Database (RLS Enabled)]
```

### Layer 1: Database RLS (CP-RLS-001)
*   Disables public anonymous selects.
*   Enforces `primary_lane IS DISTINCT FROM 'PS'` for all authenticated database connections.

### Layer 2: Server-Side API Middleware
*   A dedicated Next.js API route (`/api/gotime/dashboard`) mediates all requests.
*   The server-side route explicitly filters out PS rows at the query level before parsing.
*   The route enforces a strict **column allowlist** (e.g. returning only `id`, `project_code`, `status`, `target_date`) and drops sensitive fields like `descriptions`, `local_path`, and `raw_payload`.

### Layer 3: Redacted Metadata Summaries
*   For PS monitoring, the server API only returns aggregated integers (e.g. `ps_count: 2`) via a safe count query. No row metadata is ever exposed to the client.
