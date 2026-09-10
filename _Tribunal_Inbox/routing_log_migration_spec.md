# DCSE-CP DBA MIGRATION FILE — STEP 1B
**Document ID:** DCSE-CP/MIG/20260624-001
**Status:** PENDING EXECUTION AUTHORIZATION
**Migration File Path:** [003_add_routing_log.sql](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/dcse-command-post/prisma/migrations/003_add_routing_log.sql)
**Target Database ID:** `nevgdyfpxdaloacuutal`

Following the feedback and approval conditions from the Claude CP (CTO) review, the migration script has been built and saved.

## Resolution of Review Conditions

- **C1 & C3 (Append-only & UPDATE/DELETE policies):** Addressed. Added explicit RLS policies for `UPDATE` and `DELETE` that evaluate to `false` (blocking all non-service-role mutations), and added documentation headers detailing the append-only design.
- **C2 (Users FK Verification):** Addressed. Database inspection confirmed `public.users` exists and uses `id` as the primary key UUID (mapped correctly in the schema foreign key constraint).
- **Lanes Alignment:** Added `DCS` and `TI` to the permitted `source_lane` CHECK constraints.
- **C4 (Deliverable Route):** Created the file at `prisma/migrations/003_add_routing_log.sql`.

---

### Migration File SQL Source

```sql
-- =========================================================
-- STEP 1B - MODEL ROUTER LOG SCHEMA & SECURITY POLICIES
-- Target database path: public.routing_log
-- Rationale: Supports model routing decisions and preserves audit footprints
-- Governance Context: Append-only ledger. UPDATE/DELETE operations strictly blocked.
-- PS Firewall Context: Hard database block on source_lane != 'PS'
-- =========================================================

-- 1. Create the routing_log table
CREATE TABLE IF NOT EXISTS public.routing_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    record_id UUID, -- Optional soft link to registry records
    record_type VARCHAR(100) NOT NULL,
    source_lane VARCHAR(10) NOT NULL CHECK (source_lane IN ('SC', 'SS', 'DCSE', 'DCS', 'TI', 'PUBLIC')),
    target_reviewer VARCHAR(50) NOT NULL CHECK (target_reviewer IN (
        'CLAUDE_CP', 'QWEN_CCO', 'GEMINI', 'CODEX', 'AG', 'CHATGPT_MAIN', 'CLAUDE_CODE', 'QWEN_CODER'
    )),
    review_type VARCHAR(100) NOT NULL,
    routing_packet JSONB NOT NULL,
    created_by UUID REFERENCES public.users(id) ON DELETE SET NULL, -- Maps to public.users(id) confirmed in target instance
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    -- Hard PS stop constraint at the database table level (Dual protection with source_lane check)
    CONSTRAINT ps_firewall_hard_stop CHECK (source_lane != 'PS')
);

-- 2. Indexing for fast search and aggregation
CREATE INDEX IF NOT EXISTS idx_routing_log_target ON public.routing_log(target_reviewer);
CREATE INDEX IF NOT EXISTS idx_routing_log_lane ON public.routing_log(source_lane);
CREATE INDEX IF NOT EXISTS idx_routing_log_record ON public.routing_log(record_id);

-- 3. Enable Row-Level Security (RLS)
ALTER TABLE public.routing_log ENABLE ROW LEVEL SECURITY;

-- 4. Create SELECT and INSERT policies (Strict exclusion of PS)
CREATE POLICY select_routing_log ON public.routing_log
    FOR SELECT
    USING (source_lane != 'PS');

CREATE POLICY insert_routing_log ON public.routing_log
    FOR INSERT
    WITH CHECK (source_lane != 'PS');

-- 5. Explicitly deny all UPDATE and DELETE operations at RLS level (Enforces append-only design)
CREATE POLICY update_routing_log ON public.routing_log
    FOR UPDATE
    USING (false)
    WITH CHECK (false);

CREATE POLICY delete_routing_log ON public.routing_log
    FOR DELETE
    USING (false);
```

---
**Prepared By:** Antigravity (DBA Node)
**Target:** Ready for execution authorization.
