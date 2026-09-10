# GOTIME CP DASHBOARD SAFE API SPECIFICATION

**Ref:** GoTime Phase 4 API Spec  
**Date:** 2026-07-02  
**Status:** PROPOSED API PROTOCOL  

---

## 1. Protocol Definition
*   **Endpoint:** `/api/gotime/dashboard`
*   **Method:** `GET`
*   **Access:** Authenticated user session only (Next.js server-side checks).
*   **Backend Client:** Supabase Service Role client (to securely query count stats and run allowlist filters).

---

## 2. Server-Side Filtering & Allowlist Rules

The API route executes separate database queries for each PM entity and enforces the following field limitations:

### 1. Projects Query (`pm_projects`)
*   **SQL Filter:** `primary_lane IS DISTINCT FROM 'PS' OR primary_lane IS NULL`
*   **Allowed Columns:** `id`, `project_code`, `project_name`, `entity_code`, `primary_lane`, `classification`, `status`, `priority`, `start_date`, `target_date`, `created_at`
*   **Forbidden Columns:** (Omitted from SELECT query) None

### 2. Workstreams Query (`pm_workstreams`)
*   **SQL Filter:** `lane_code IS DISTINCT FROM 'PS' OR lane_code IS NULL`
*   **Allowed Columns:** `id`, `project_id`, `workstream_code`, `workstream_name`, `lane_code`, `status`, `priority`, `blocked_flag`
*   **Forbidden Columns:** `objective`, `exit_criteria`

### 3. Tasks Query (`pm_tasks`)
*   **SQL Filter:** `lane_code IS DISTINCT FROM 'PS' OR lane_code IS NULL`
*   **Allowed Columns:** `id`, `project_id`, `workstream_id`, `task_code`, `task_title`, `lane_code`, `entity_code`, `status`, `priority`, `assigned_to`, `model_role`, `task_type`, `due_date`
*   **Forbidden Columns:** `description`, `completion_notes`

### 4. Blockers Query (`pm_blockers`)
*   **SQL Filter:** `lane_code IS DISTINCT FROM 'PS' OR lane_code IS NULL`
*   **Allowed Columns:** `id`, `project_id`, `task_id`, `blocker_code`, `blocker_title`, `lane_code`, `blocker_status`, `created_at`
*   **Forbidden Columns:** `blocker_description`, `unblock_condition`

### 5. Artifacts Query (`pm_artifacts`)
*   **SQL Filter:** `lane_code IS DISTINCT FROM 'PS' OR lane_code IS NULL`
*   **Allowed Columns:** `id`, `project_id`, `task_id`, `artifact_code`, `artifact_name`, `artifact_type`, `lane_code`, `version_label`, `status`, `created_at`
*   **Forbidden Columns:** `local_path`, `source_path`, `hash_sha256`, `notes`, `payload`

---

## 3. Example JSON Response Payload

```json
{
  "success": true,
  "projects": [
    {
      "id": "a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d",
      "project_code": "CP_PM_MODULE_V1",
      "project_name": "DCSE Command Post Project Manager Module",
      "entity_code": "DCSE",
      "primary_lane": "SC",
      "classification": "CONFIDENTIAL",
      "status": "active",
      "priority": 3,
      "start_date": "2026-06-01",
      "target_date": "2026-07-24"
    }
  ],
  "workstreams": [],
  "tasks": [],
  "blockers": [],
  "artifacts": [],
  "stats": {
    "activeProjects": 1,
    "blockedItems": 0,
    "dcsReview": 0,
    "psFirewallHolds": 2, 
    "due7Days": 0
  }
}
```
*Note: `psFirewallHolds` represents only the count of projects where `primary_lane = 'PS'` (calculated securely server-side), preventing any exposure of case titles.*
