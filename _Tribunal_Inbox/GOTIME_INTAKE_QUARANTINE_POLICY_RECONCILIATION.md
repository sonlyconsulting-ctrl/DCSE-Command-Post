# GOTIME INTAKE QUARANTINE POLICY RECONCILIATION

**Ref:** GoTime Phase B Policy Reconciliation  
**Date:** 2026-07-02  
**Status:** **APPROVED DIRECTION**

---

## 1. Role Reconciliation (DCS Human Gate)
In this phase, we reconcile the database-level security with human identity verification:
*   **Database Execution:** Runs exclusively via `service_role` (which bypasses RLS) on the server side.
*   **Reviewer Identity:** The actual human reviewer must be `DCS`.
*   **Server Enforcement:** The server-side promote route (`/api/quarantine/promote`) will verify that the incoming request carries valid DCS authorization (e.g. environment key `ENABLE_DCS_PROMOTE=true` or equivalent validation token). General authenticated users are blocked from triggering promotion.

---

## 2. Ingestion Status Lifecycles

 Quarantined records will move through these explicit statuses:

*   `RAW_RECEIVED`: Intake is saved in database quarantine prior to scanning.
*   `SCAN_PENDING`: Ingestion is running scanner v2 checks.
*   `FLAGGED_PS_HOLD`: Scanner v2 detected PS litigation keywords. Held for DCS review.
*   `FLAGGED_REVIEW_HOLD`: General policy or validation holds.
*   `CLEARED_FOR_DCS_REVIEW`: Clean non-PS intake cleared for DCS dashboard review.
*   `DCS_APPROVED_FOR_PROPOSAL`: DCS signs off on promotion to proposal.
*   `PROMOTED`: Record has been successfully written into the active PM tables.
*   `REJECTED`: Promotion rejected by DCS.
*   `ARCHIVED`: Stale or historic quarantine records.

---

## 3. Long-Term Reviewer Access Table Design (`cp_reviewer_access`)

To transition to a multi-role reviewer model in a later phase, we propose the following table design:

```sql
CREATE TABLE public.cp_reviewer_access (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    reviewer_key VARCHAR(100) UNIQUE NOT NULL, -- 'DCS', 'PS_REVIEWER_01'
    reviewer_name VARCHAR(100) NOT NULL,
    lane_code VARCHAR(20) NOT NULL, -- 'DCS', 'PS', 'CP', 'SC', 'EMPLOYMENT'
    can_review BOOLEAN DEFAULT FALSE,
    can_promote BOOLEAN DEFAULT FALSE,
    can_view_flagged BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row-Level Security
ALTER TABLE public.cp_reviewer_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.cp_reviewer_access FORCE ROW LEVEL SECURITY;

-- Block public reads
CREATE POLICY "service_role_reviewer_policy" 
    ON public.cp_reviewer_access 
    FOR ALL 
    TO service_role 
    USING (true);
```

### Initial Permitted Access:
1.  **DCS Reviewer:** `lane_code = 'DCS'`, `can_review = true`, `can_promote = true`, `can_view_flagged = true`.
2.  **Future PS Reviewer:** (To be authorized) `lane_code = 'PS'`, `can_view_flagged = true`.
