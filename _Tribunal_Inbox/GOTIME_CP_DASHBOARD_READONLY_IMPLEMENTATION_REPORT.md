# GOTIME CP DASHBOARD READONLY IMPLEMENTATION REPORT

**Ref:** GoTime Phase 4 UI Build  
**Date:** 2026-07-02  
**Status:** IMPLEMENTED (Read-Only Surface)

---

## 1. UI Architecture & Navigation
We have built a dedicated project management surface located at the route:
📄 `/cp/gotime` (`DCSE_ASSET_PORTAL_APP/apps/web/src/app/cp/gotime/page.tsx`)

This page integrates seamlessly with the existing Consulting Portal header, authentication check, and theme styles.

---

## 2. Core Dashboard Tab Layout
To avoid full Jira complexity, the UI is organized into tabs with specific dashboards:

*   **Active Projects Grid:** Displays code, name, lane, classification, status, target date, and a red indicator if `psLockFlag` is enabled.
*   **Workstreams List:** Shows parent projects, lane codes, objective, and a blocked warning flag.
*   **Kanban Task Board:** Organizes tasks by status columns (`not_started`, `in_progress`, `completed`, `blocked`). Tasks feature color-coded tags for priority (P0/P1/P2) and target lanes.
*   **Blockers Register:** Lists blocker title, description, unblock condition, and severity (High/Medium/Low).
*   **Deliverables Register:** Displays artifact name, type, local/source file paths, and SHA256 hashes.
*   **Intake & Command Room (Read-Only):** A mock coordination room detailing a chat thread history and intake box. All input elements, pasted text boxes, file drops, and "Generate Work Orders" buttons are rendered in disabled states with tooltips explaining the read-only phase.

---

## 3. Real-Time Supabase Integration
The page uses the `@supabase/supabase-js` client to fetch records:
1.  **Projects:** `supabase.from('pm_projects').select('*')`
2.  **Workstreams:** `supabase.from('pm_workstreams').select('*')`
3.  **Tasks:** `supabase.from('pm_tasks').select('*')`
4.  **Blockers:** `supabase.from('pm_blockers').select('*')`
5.  **Artifacts:** `supabase.from('pm_artifacts').select('*')`

---

## 4. Visual Lane & Security Indicators
*   **PS Firewall Indication:** Any item where `lane_code = 'PS'` or `primary_lane = 'PS'` is intercepted in the UI. If RLS returns it, the title is redacted (`[REDACTED PS CASE FILE]`) and details are hidden, showing a lock icon.
*   **Color coding:**
    *   `STOP_GATE` / `CONFIDENTIAL_PS` / `P0` -> **Red**
    *   `DCS_REVIEW` / `BLOCKED` -> **Amber**
    *   `APPROVED` / `COMPLETED` -> **Green**
    *   `CP` / `SC` / `DCS_EMPLOYMENT` -> **Blue / Neutral**
