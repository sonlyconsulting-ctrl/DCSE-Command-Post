# DCSE Command Post — Database Schema Audit
**Project:** SC SportsSociety (`nevgdyfpxdaloacuutal`)  
**Audit Date:** 2026-05-18  
**Branch:** `claude/audit-database-schema-Hs457`  
**Status:** Findings documented — DCS approval required before any remediation is applied

---

## 1. Existing Tables

| Table | RLS Enabled | Policy Count | Finding |
|---|---|---|---|
| `public.dcse_plan_inbox` | ✅ Yes | 4 | OK |
| `public.dcse_plan_reviews` | ✅ Yes | 3 | OK |
| `public.pm_artifacts` | ✅ Yes | — | OK |
| `public.dcse_ddna_signals` | ❌ No | 0 | **CRITICAL — RLS missing** |
| `public.model_activity_log` | ❌ No | — | **CRITICAL — RLS missing** |

---

## 2. Critical Findings

### 2.1 RLS Disabled on `dcse_ddna_signals`
- Table holds AI model sentiment and logic signals; exposure without RLS allows any authenticated (or anon) role to read all rows.
- **Remediation:** Enable RLS and add read/write policies scoped to service-role and authorised model agents.
- **Gate:** Requires DCS approval before migration `0002` is applied.

### 2.2 RLS Disabled on `model_activity_log`
- Audit log table. Without RLS, any caller can INSERT or SELECT arbitrary rows, undermining audit integrity.
- **Remediation:** Enable RLS; restrict INSERT to service-role only; restrict SELECT to admin/DCS roles.
- **Gate:** Requires DCS approval before migration `0003` is applied.

### 2.3 Missing Tables
Three tables identified as required by the DCSE governance model are absent:

| Table | Purpose |
|---|---|
| `ddna_extraction_runs` | Tracks each DDNA extraction job execution, result, and artefact links |
| `ai_agent_registry` | Canonical registry of model agents authorised to write to DCSE tables |
| `realtime_state_sync` | Stores ephemeral realtime collaboration state (broadcast channel snapshots) |

- **Remediation:** Migration `0004` creates these tables with RLS enabled from the start.
- **Gate:** Requires DCS approval before migration `0004` is applied.

### 2.4 Cron Job `ddna-extractor-daily` Not Configured
- `pg_cron` job exists in function registry but `schedule` and `timezone` are unset; job status is **not found**.
- Activating the cron job triggers writes to `ddna_extraction_runs` (missing) and JWT-authenticated edge function calls.
- **Remediation:** Migration `0005` creates the cron schedule after missing tables are in place.
- **Gate:** Requires DCS approval + JWT provisioning for the edge function service account before `0005` is applied.

---

## 3. Infrastructure Snapshot

| Area | Status |
|---|---|
| Indexes | 12 (no action required) |
| Storage buckets | `dcse_assets` present |
| Edge functions | `dcse_trigger_ddna_extraction` present |
| Environment variables | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`, `SUPABASE_ANON_KEY` — all present |

---

## 4. Remediation Migrations (Pending DCS Approval)

All migration files are located in `supabase/migrations/`. They are **inert until manually run** by a DCS-approved operator.

| Migration | Scope | DCS Gate |
|---|---|---|
| `0001_baseline_comment.sql` | No-op baseline marker | None |
| `0002_rls_dcse_ddna_signals.sql` | Enable RLS + policies on `dcse_ddna_signals` | Required |
| `0003_rls_model_activity_log.sql` | Enable RLS + policies on `model_activity_log` | Required |
| `0004_missing_tables.sql` | Create `ddna_extraction_runs`, `ai_agent_registry`, `realtime_state_sync` | Required |
| `0005_cron_ddna_extractor.sql` | Register `ddna-extractor-daily` pg_cron job | Required + JWT provisioning |

---

## 5. Action Items for DCS

- [ ] Review and approve migration `0002` (RLS on `dcse_ddna_signals`)
- [ ] Review and approve migration `0003` (RLS on `model_activity_log`)
- [ ] Confirm column schema for `ddna_extraction_runs`, `ai_agent_registry`, `realtime_state_sync` before approving `0004`
- [ ] Provision JWT / service-account credentials for edge function before approving `0005`
- [ ] Confirm cron schedule timezone for `ddna-extractor-daily`
