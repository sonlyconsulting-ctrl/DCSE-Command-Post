# ESCD Production Database Recovery & Golden Baseline Runbook

**Document ID:** `RUNBOOK-ESCD-DB-RECOVERY-001`  
**Governing Standard:** DCSE v7.2 Operational Continuity  
**Classification:** OPERATIONAL RUNBOOK / SYSTEM RECOVERY  
**Golden Baseline Commit:** `1b9a101`  
**Golden Baseline Git Tag:** `baseline/escd-mvp-0.7.2-golden-working-20260920` (alias: `v0.7.2-escd-golden`)  
**Production Deployment ID:** `dpl_DDjdD7jiK2jhzh74U4viF1U39w4g`  
**Production URL:** [https://sc-escd.vercel.app](https://sc-escd.vercel.app)  
**Date Established:** 2026-09-20  

---

## 1. Executive Summary & Incident Anatomy

During periods of high background activity or unoptimized cron schedules on Supabase, the managed PostgreSQL database instance (`nevgdyfpxdaloacuutal.supabase.co` on AWS `t4g.nano` with 512 MB RAM) can exhaust its AWS burst Disk I/O credit budget.

### Symptoms Observed:
1. **Frontend:** Displays `Database temporarily unreachable (database_temporarily_unreachable)` or hangs on login / token refresh.
2. **API Layer:** Vercel serverless edge functions return `HTTP 504 Gateway Timeout` or `HTTP 500: {"error":"internal_error"}` when backend PostgREST queries take $>10$ seconds.
3. **Database Metrics:** PostgreSQL cache hit ratio drops from normal healthy levels ($\ge 99\%$) down to $\sim 80\%$, forcing repeated physical disk reads that deplete I/O burst credits.

### Root Causes Discovered:
1. **`cron.job_run_details` Bloat & Missing Index:**  
   The `pg_cron` background job history accumulated thousands of rows. The recurring update query:
   ```sql
   UPDATE cron.job_run_details SET status = $1, return_message = $2 WHERE status IN ($3, $4);
   ```
   was unindexed on `status`, taking **3,750 ms per execution** via sequential table scans on disk.
2. **Cascading Serverless Edge Timeouts:**  
   In `apps/escd/runtime/mvp_data.py`, checking 6 model providers sequentially with a 12s socket timeout required up to $6 \times 12\text{s} = 72\text{s}$ during a database stall, instantly exceeding Vercel's 10-15s function execution limit.

---

## 2. Inherent Codebase Protections (Active in Baseline `1b9a101`)

The codebase incorporates permanent resilience patterns so a stalled database cannot crash the frontend:
1. **In-Memory Circuit Breaker:** `_SUPABASE_RPC_FAIL_UNTIL` in `mvp_data.py` trips for 30 seconds upon any RPC timeout or database error, immediately returning cached/fallback configuration for subsequent requests in $0$ ms.
2. **Aggressive Socket Timeouts:**
   - RPC queries: reduced from 12s to **3s**.
   - User authentication: reduced from 15s to **5s**.
   - Token RLS checks: reduced from 10s to **4s**.
   - Total degraded latency dropped from **72 seconds** to **$< 3.5$ seconds**.
3. **Public Unauthenticated Auth Config:** `GET /api/mvp/auth-config` serves Supabase credentials without requiring database roundtrips, preventing login deadlocks.
4. **Structured 503/504 Handling:** Socket timeouts and network errors are caught and surfaced as `HTTP 503` ("Authentication service temporarily unreachable") or `HTTP 504`, allowing the frontend to render actionable maintenance banners rather than crashing.

---

## 3. Step-by-Step Diagnostic & Recovery Procedure ("If There's a Next Time")

Follow these steps in sequence if ESCD reports database unreachability or high latency:

### Step 1: Check Supabase Health & Project Status
1. Navigate to the Supabase Project Dashboard:  
   **URL:** [https://supabase.com/dashboard/project/nevgdyfpxdaloacuutal](https://supabase.com/dashboard/project/nevgdyfpxdaloacuutal)
2. Review the project status indicator:
   - If status is **Paused**, click **Restore project**.
   - If status is **Unhealthy** or **Degraded**, proceed to Step 2.
3. Open **Project Settings $\rightarrow$ Database** or **Reports $\rightarrow$ Database** to check **Disk IO Budget** and **CPU Usage**.

### Step 2: Restart Database Compute
1. In the Supabase Dashboard, go to **Project Settings $\rightarrow$ General** or **Database**.
2. Click **Restart database** (Fast reboot).
3. Wait 60–90 seconds for PostgreSQL and PostgREST to reinitialize.
> [!NOTE]
> Immediately after a restart, the compute upgrade prompt or certain metric cards in the Supabase UI may appear temporarily unavailable while the instance re-attaches EBS storage and rebuilds memory caches. This normalizes within 2–3 minutes.

### Step 3: Run Maintenance SQL in Supabase SQL Editor
Once the database is reachable, open the **SQL Editor** in Supabase and execute the following maintenance script:

```sql
-- 1. Check current cache hit ratio (should be >= 99%)
SELECT 
  sum(heap_blks_read) as heap_read,
  sum(heap_blks_hit)  as heap_hit,
  round((sum(heap_blks_hit)::numeric / nullif(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100), 2) as cache_hit_ratio
FROM pg_statio_user_tables;

-- 2. Truncate bloated cron logs to free disk I/O and shared buffers
TRUNCATE TABLE cron.job_run_details;

-- 3. Ensure status index exists to prevent 3,750ms sequential scans
CREATE INDEX IF NOT EXISTS idx_cron_job_run_details_status 
ON cron.job_run_details (status);

-- 4. Inspect active cron jobs and schedules
SELECT jobid, schedule, command, active 
FROM cron.job;

-- 5. Check top disk I/O queries via pg_stat_statements
SELECT 
  round((blk_read_time + blk_write_time)::numeric, 2) as io_time_ms,
  calls,
  round(mean_exec_time::numeric, 2) as mean_ms,
  substr(query, 1, 80) as short_query
FROM pg_stat_statements
ORDER BY (blk_read_time + blk_write_time) DESC
LIMIT 10;
```

### Step 4: Compute Upgrade Path (If Workload Outgrows Nano)
If Disk I/O exhaustion recurs frequently:
1. In Supabase Dashboard, go to **Project Settings $\rightarrow$ Add-ons $\rightarrow$ Compute Size**.
2. Select **Micro** (1 GB RAM, 2x shared_buffers) or **Small** (2 GB RAM).
3. Apply changes (causes an automated 1–2 minute zero-downtime or brief maintenance failover).

---

## 4. Golden Working Baseline & Fast Revert Guide

The codebase at commit `1b9a101` represents a fully verified, production-tested golden baseline.

### Verified Functionalities in this Baseline:
- **Google OAuth Login:** Full authentication loop verified with seamless session persistence.
- **Multi-Model Selection Catalog:** ChatGPT, Claude, Qwen, and Gemini provider tabs active with client-side credential binding.
- **Resilient Circuit Breaker:** Graceful degradation without 500 error storms during backend latency.
- **Automated Tests:** 71/71 tests passing (`python -m pytest apps/escd/tests -v`).

### How to Revert to this Baseline:

#### Option A: Git Local & Remote Restoration
To reset or branch off this exact golden state:
```bash
# Fetch latest tags
git fetch origin --tags

# Checkout the verified golden tag directly
git checkout baseline/escd-mvp-0.7.2-golden-working-20260920

# Or reset active branch to this commit
git reset --hard 1b9a101
```

#### Option B: Instant Production Rollback via Vercel CLI
If an unauthorized or broken deployment is pushed to production, immediately repoint the production alias `https://sc-escd.vercel.app` back to the golden deployment:
```bash
# Instant alias promote to golden deployment
npx vercel alias set dpl_DDjdD7jiK2jhzh74U4viF1U39w4g sc-escd.vercel.app
```

---

## 5. Artifact & Receipt Cross-References
- **Git Commit:** `1b9a101`
- **Git Tags:** `baseline/escd-mvp-0.7.2-golden-working-20260920`, `v0.7.2-escd-golden`
- **Canonical Registry Item (Task):** `CANON-160` (ESCD Internal Error Remediation)
- **Canonical Registry Item (Knowledge):** `CANON-161` (Circuit Breaker Architecture)
- **Canonical Registry Item (Knowledge):** `CANON-162` (Database Recovery Runbook)
- **Tribunal Receipt:** `_Tribunal_Inbox/TRIBUNAL_MILESTONE_20260920_ESCD_GOLDEN_BASELINE_AND_RECOVERY_RUNBOOK.md`
