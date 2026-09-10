# Implementation Plan v5: GoTime Phase B Intake Quarantine & Promotion Gate

## Goal Description
Implement the Intake Quarantine staging layer and DCS-only Promotion Gate (Phase B) to prevent raw, unreviewed markdown notes or Tribunal JSON records from writing directly into active project management tables. We will enforce a strict review workflow:
1.  **Ingestion:** Raw intake is written *only* to the quarantine table.
2.  **Audit:** The expanded scanner v2 scans the input and flags PS matches for `HOLD` status.
3.  **Human Review:** Standard users see only redacted previews or counts. Only authorized DCS admins can view and promote.
4.  **Promotion:** DCS-only promotion route executes writes to active PM tables using server-side `service_role`.

---

## User Review Required

> [!IMPORTANT]
> **Human Reviewer Identity:** The database connection uses `service_role` for writes, but the application layer enforces that the human executor must be explicitly authorized as `DCS` (via environment secret-key or configuration flag `ENABLE_DCS_PROMOTE=true` in development). Anonymous or standard authenticated users cannot promote.
>
> **Promotion Constraints:** The promote API acts *only* on existing quarantine records. Direct writes of raw markdown or Tribunal JSON to active PM tables remain completely blocked.
>
> **Long-Term Design:** We have drafted the `cp_reviewer_access` table model to map user IDs to specific lane permissions (DCS, PS_REVIEWER, CP_VALIDATOR) for a future deployment phase.

---

## Proposed Changes

### Component 1: Database Staging & Staged Reviewer Schema

#### [MODIFY] [schema.prisma](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/dcse-command-post/prisma/schema.prisma)
Add the `GotimeIntakeQuarantine` model mapping to `public.gotime_intake_quarantine`:
```prisma
model GotimeIntakeQuarantine {
  id                    String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  sourceType            String    @map("source_type") @db.VarChar(50)
  rawPayload            Json      @map("raw_payload")
  scanStatus            String    @default("PENDING") @map("scan_status") @db.VarChar(50)
  psLeakageFlag         Boolean   @default(false) @map("ps_leakage_flag")
  quarantineReason      String?   @map("quarantine_reason") @db.Text
  promoted              Boolean   @default(false)
  promotedToProjectId   String?   @map("promoted_to_project_id") @db.Uuid
  promotedAt            DateTime? @map("promoted_at") @db.Timestamptz(6)
  createdAt             DateTime? @default(dbgenerated("now()")) @map("created_at") @db.Timestamptz(6)
  updatedAt             DateTime? @default(dbgenerated("now()")) @map("updated_at") @db.Timestamptz(6)

  @@map("gotime_intake_quarantine")
}
```

#### [NEW] [CP_RLS_002_QUARANTINE_TABLE_AND_RLS.sql](file:///C:/Users/dsead/.gemini/antigravity/brain/352dd795-ab10-42cb-8a09-781353802adc/CP_RLS_002_QUARANTINE_TABLE_AND_RLS.sql)
*   Draft the SQL DDL to create the table `gotime_intake_quarantine`.
*   Enable and force Row Level Security (RLS) on it, restricting access exclusively to `service_role`.

---

### Component 2: Next.js API Routes (Phase B)

#### [NEW] [/api/quarantine/submit/route.ts](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/api/quarantine/submit/route.ts)
*   HTTP Method: `POST`
*   Takes raw input payload (markdown text or Tribunal JSON) and inserts it into `gotime_intake_quarantine` with status `RAW_RECEIVED`.
*   Triggers the leakage scanner v2.
*   Assigns status: `FLAGGED_PS_HOLD` (if match found), `FLAGGED_REVIEW_HOLD`, or `CLEARED_FOR_DCS_REVIEW` (if clean).
*   Enforces that PS-flagged items are held in database quarantine and blocks auto-promotion.

#### [NEW] [/api/quarantine/promote/route.ts](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/api/quarantine/promote/route.ts)
*   HTTP Method: `POST`
*   Parameters: `quarantine_id`, `destination_project_id`.
*   Checks if the requester is DCS-authorized (verifies environment flag `ENABLE_DCS_PROMOTE=true` or matches secret header key).
*   Reads the quarantine record.
*   If clean, promotes metadata into `pm_workstreams` and `pm_tasks` using server-side `service_role`.
*   If flagged with PS, rejects promotion unless a separate `PS-lane-review-override` is explicitly signed off.
*   Creates an audit record in `pm_activity_log`.

---

### Component 3: Frontend Intake UI Integration

#### [MODIFY] [page.tsx](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/apps/web/src/app/cp/gotime/page.tsx)
*   Update **Intake tab** to:
    *   Enable the input textarea and "Submit Intake" button.
    *   Send submissions via `POST /api/quarantine/submit`.
    *   Show a list of quarantined items with status labels (`CLEARED_FOR_DCS_REVIEW`, `FLAGGED_PS_HOLD`).
    *   Apply cosmetic redactions (`[REDACTED PS HOLD]`) to the titles/bodies in the UI, ensuring no raw flagged content enters the browser state.
    *   Add a "Promote to Work Order" button next to quarantined records. Render it disabled unless DCS credentials/authorization are verified.

---

### Component 4: Long-Term Design Blueprint

#### [NEW] [GOTIME_INTAKE_QUARANTINE_POLICY_RECONCILIATION.md](file:///C:/Users/dsead/.gemini/antigravity/brain/352dd795-ab10-42cb-8a09-781353802adc/GOTIME_INTAKE_QUARANTINE_POLICY_RECONCILIATION.md) (Update)
*   Add the SQL DDL blueprint for the `cp_reviewer_access` table mapping user IDs and reviewer keys to specific lanes (`DCS`, `PS_REVIEWER`, `EMPLOYMENT_REVIEWER`).

---

## Verification Plan

We will expand [`run_all_tests.ts`](file:///C:/DS%20All%20Things/DCSE_Command_Center/DCSE_CP_Project/dcse-command-post/run_all_tests.ts) to execute the 7 required verification tests:

### Automated Test Specifications
1.  **Test 1 (Clean Ingest):** Non-PS intake enters quarantine and resolves to status `CLEARED_FOR_DCS_REVIEW`.
2.  **Test 2 (PS Ingest Hold):** PS intake (e.g. contains "docket 8:23-cv-00489") enters quarantine and resolves to status `FLAGGED_PS_HOLD`.
3.  **Test 3 (Unauthenticated Promote):** Anonymous request to `/api/quarantine/promote` fails with status `401 Unauthorized`.
4.  **Test 4 (Standard Authenticated Promote):** Ordinary authenticated user promotion request fails with status `403 Forbidden`.
5.  **Test 5 (DCS Clear Promote):** DCS-authorized request successfully promotes a `CLEARED_FOR_DCS_REVIEW` item into a work order.
6.  **Test 6 (DCS PS Promote Block):** DCS-authorized request fails to promote a `FLAGGED_PS_HOLD` record unless explicit override is provided.
7.  **Test 7 (Network Leak Check):** Verifies that querying the dashboard API returns only safe counts/redacted previews of quarantined items, with raw payload structures omitted.
