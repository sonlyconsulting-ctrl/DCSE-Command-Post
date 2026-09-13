# ESCD MVP 006 Recovery and Full CRUD / Attachments Build Receipt

- **Date:** 2026-09-13
- **Branch:** `feature/escd-minimal-mvp-006`
- **Repo:** `sonlyconsulting-ctrl/DCSE-Command-Post`
- **Base Deployments:**
  - Fix 1 Deployment: `dpl_GN8p9XX8PHYSVwGbKoSSen4zmSbq`
  - Fix 2 Deployment: `dpl_ArgumrKNHia4Y9HAsPr8eDqVKozw`
- **Live URL:** `https://sc-command-post.vercel.app/escd`
- **Production Host:** `https://www.sonlyconsulting.com`

---

## Fix 1: Runtime Auth Configuration Restoration
- **Task ID:** `DCSE-ESCD-RECOVERY-AUDIT-20260913-001`
- **Root Cause:** Vercel environment variables (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DDNA_SUPABASE_URL`, `DDNA_SUPABASE_SERVICE_ROLE_KEY`) existed only in Preview scope, leaving Production scope unpopulated and throwing `auth_configuration_missing`.
- **Resolution:** Added all five Supabase variables to Production scope on `sc-command-post` via Vercel CLI/API, verified environment attachment, and triggered redeployment.
- **Tribunal Receipt:** `TRIBUNAL_SESSION_REPORT_20260913_AG_ESCD_AUTH_CONFIG_RESTORED.json`
- **Supabase Tracking Record ID:** `faf8fec0-6212-4fec-92a1-23f8b3326cf0`

---

## Fix 2: Full Dashboard CRUD, Assets Parity, DDNA Schema, & File Uploads
- **Task ID:** `DCSE-ESCD-CRUD-ATTACHMENTS-20260913-002`
- **Key Changes Implemented:**
  1. **Full CRUD for All Tabs:**
     - First column tabs (Workflows, Metrics, Deliverables, Actions, Evidence, Governance): Selecting edit now opens a full modal dialog allowing title, status, priority, description, and file attachment management, plus deletion/archiving.
     - Assets Tab Parity: Created dedicated Add Asset card, unified detail modal, edit and delete functionality.
     - DDNA Sources Tab: Created dedicated Add DDNA card, edit and delete functionality, and background job log inspector.
  2. **DDNA Schema Resolution:**
     - Updated PostgREST queries from invalid `dcse_ddna_legacy` to active `dcse_cp`, resolving 406 Not Acceptable errors.
  3. **Universal File Upload & Persistence:**
     - Added `POST /api/mvp/upload` supporting Supabase Storage bucket `escd-files` with automatic fallback to data URIs.
     - Added file attachment manager inside `<dialog id="recordModal">` with live upload, open/download preview, and removal.
     - Added file pickers directly on the initial creation forms across item types.
  4. **Contract and Unit Testing:**
     - Added `apps/escd/tests/test_mvp_crud_attachments.py` covering all CRUD operations, schema routing, and file attachment persistence.
     - All 209 unit and contract tests passing (`pytest apps/escd/tests`).
- **Tribunal Receipt:** `TRIBUNAL_SESSION_REPORT_20260913_AG_ESCD_CRUD_DDNA_SCHEMA_ATTACHMENTS.json`
- **Supabase Tracking Record ID:** `4be59f72-28c6-45cd-8f41-4e5f27179891`

---

## Verification & Operational Sign-off
- `/escd` and `/escd/app` verified live 200 OK.
- UI bundles verified to serve modal and CRUD/upload handlers.
- Tribunal receipts synchronized across Command Center and repository inboxes.
- Supabase tracking entries recorded in `public.items`.
