# DCSE Command Post Project Management Architecture Specification (Phase 2)
**Document Version:** 2.0.0  
**Authority:** DCS / Tribunal  
**Target Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`  
**Target Components:** `cp_validation/CommandPostShell.jsx`, Supabase `dcse_cp` schema, PostgREST API  
**Status:** SPECIFIED / SECONDARY PRIORITY (Queued for execution following ESCD Phase 1)

---

## 1. Executive Summary

This specification defines the enterprise grade Project Management (PM) architecture for the DCSE Command Post. While ESCD provides operational task execution and conversational item capture, the Command Post serves as the executive cockpit for multi-lane portfolio governance across all DCSE properties:
- **SC (S-Only Consulting)**: Flagship intellectual property, curriculum systems (SC-CTJ), and commercial checkout.
- **SS (SportSociety)**: Health, fitness, and movement education programs (SS-PTJ).
- **TSL (Tedo's Sports Lounge)**: Interactive sports media platform and predictive analytics.
- **DCSE (Core)**: Executive orchestration, agent workforces (AG, Claude, Codex, Qwen), and infrastructure.
- **TI & FAMILY**: Private institutional assets and family governance.

Phase 1 deployed the Projects status view into ESCD (`apps/escd`), enabling immediate tracking of the 10 authoritative canonical projects and their task rollups. Phase 2 scales `CommandPostShell.jsx` from a static placeholder into a reactive, database-backed enterprise PM console powered by dedicated relational tables (`pm_projects`, `pm_tasks`, `pm_blockers`, `pm_risks`).

---

## 2. Relational Database Architecture (Supabase / Postgres)

Phase 2 introduces four dedicated relational tables in the `dcse_cp` schema. These tables provide referential integrity, automated rollup views, and row-level security (RLS) policies enforcing DCS operator authority.

### 2.1 Schema DDL

```sql
-- Schema: dcse_cp
-- Authority: DCS / Tribunal

-- 1. Projects Table
CREATE TABLE IF NOT EXISTS dcse_cp.pm_projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_key VARCHAR(64) UNIQUE NOT NULL, -- e.g. 'PROJ-SC-CTJ', 'PROJ-SS-PTJ'
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    lane VARCHAR(32) NOT NULL DEFAULT 'DCSE', -- 'SC', 'SS', 'DCSE', 'TSL', 'TI', 'FAMILY'
    owner VARCHAR(64) NOT NULL DEFAULT 'DCS', -- e.g. 'Claude Design', 'AG', 'Codex', 'Operator'
    status VARCHAR(32) NOT NULL DEFAULT 'active', -- 'active', 'waiting', 'watch', 'completed', 'archived'
    priority INT NOT NULL DEFAULT 80, -- 0 to 100
    target_delivery_at TIMESTAMPTZ,
    repo_url VARCHAR(255),
    active_pr_number INT,
    evidence_refs JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Indexing for fast lane and status queries
CREATE INDEX IF NOT EXISTS idx_pm_projects_lane ON dcse_cp.pm_projects(lane);
CREATE INDEX IF NOT EXISTS idx_pm_projects_status ON dcse_cp.pm_projects(status);
CREATE INDEX IF NOT EXISTS idx_pm_projects_priority ON dcse_cp.pm_projects(priority DESC);

-- 2. Tasks Table (Relational Work Items)
CREATE TABLE IF NOT EXISTS dcse_cp.pm_tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES dcse_cp.pm_projects(id) ON DELETE CASCADE,
    task_key VARCHAR(64) UNIQUE NOT NULL, -- e.g. 'TASK-CTJ-201'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    assigned_agent VARCHAR(64) DEFAULT 'unassigned', -- 'AG', 'Claude', 'Codex', 'Qwen', 'DCS'
    status VARCHAR(32) NOT NULL DEFAULT 'todo', -- 'todo', 'in_progress', 'review', 'done', 'blocked'
    priority INT NOT NULL DEFAULT 50,
    due_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pm_tasks_project_id ON dcse_cp.pm_tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_pm_tasks_status ON dcse_cp.pm_tasks(status);

-- 3. Blockers Table (Stop-Gate Tracking)
CREATE TABLE IF NOT EXISTS dcse_cp.pm_blockers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES dcse_cp.pm_projects(id) ON DELETE CASCADE,
    task_id UUID REFERENCES dcse_cp.pm_tasks(id) ON DELETE SET NULL,
    blocker_description TEXT NOT NULL,
    severity VARCHAR(16) NOT NULL DEFAULT 'HIGH', -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    blocking_dependency VARCHAR(128), -- e.g. 'Stripe Webhook Secret', 'Claude Design PR Review'
    status VARCHAR(32) NOT NULL DEFAULT 'active', -- 'active', 'resolved', 'waived'
    identified_by VARCHAR(64) NOT NULL DEFAULT 'Tribunal',
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_pm_blockers_project_id ON dcse_cp.pm_blockers(project_id);
CREATE INDEX IF NOT EXISTS idx_pm_blockers_status ON dcse_cp.pm_blockers(status);

-- 4. Risks & Mitigations Table
CREATE TABLE IF NOT EXISTS dcse_cp.pm_risks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES dcse_cp.pm_projects(id) ON DELETE CASCADE,
    risk_title VARCHAR(255) NOT NULL,
    impact_level VARCHAR(16) NOT NULL DEFAULT 'MEDIUM', -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    probability VARCHAR(16) NOT NULL DEFAULT 'MEDIUM',
    mitigation_strategy TEXT,
    contingency_plan TEXT,
    owner VARCHAR(64) NOT NULL DEFAULT 'DCS',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- 5. Materialized Rollup View for Executive Dashboards
CREATE OR REPLACE VIEW dcse_cp.v_project_summary AS
SELECT 
    p.id,
    p.project_key,
    p.title,
    p.lane,
    p.owner,
    p.status,
    p.priority,
    p.target_delivery_at,
    p.repo_url,
    p.active_pr_number,
    COUNT(t.id) AS total_tasks,
    COUNT(t.id) FILTER (WHERE t.status = 'done') AS completed_tasks,
    COUNT(t.id) FILTER (WHERE t.status IN ('todo', 'in_progress', 'review')) AS open_tasks,
    COUNT(b.id) FILTER (WHERE b.status = 'active') AS active_blockers_count,
    COUNT(r.id) AS identified_risks_count,
    CASE 
        WHEN COUNT(t.id) = 0 THEN 0
        ELSE ROUND((COUNT(t.id) FILTER (WHERE t.status = 'done')::numeric / COUNT(t.id)::numeric) * 100, 1)
    END AS completion_percent
FROM dcse_cp.pm_projects p
LEFT JOIN dcse_cp.pm_tasks t ON p.id = t.project_id
LEFT JOIN dcse_cp.pm_blockers b ON p.id = b.project_id
LEFT JOIN dcse_cp.pm_risks r ON p.id = r.project_id
GROUP BY p.id;
```

---

## 3. UI Component Architecture: `CommandPostShell.jsx`

In `cp_validation/CommandPostShell.jsx`, the navigation currently contains:
```jsx
{ id: 'pm', label: 'Project Mgmt', icon: 'FolderKanban' }
```
When selected, it renders a placeholder card:
```jsx
{activeTab === 'pm' && <PlaceholderCard title="Project Management" desc="Portfolio task rollups, milestone tracking, and cross-lane delivery status." />}
```

### 3.1 React Component Hierarchy

In Phase 2, this placeholder is replaced by `ProjectManagementView`:

```
<ProjectManagementView>
  ├── <PortfolioHeaderSummary>
  │     ├── Total Initiatives KPI
  │     ├── Critical In-Flight KPI (P90)
  │     ├── Active Blockers KPI (Alert Badge)
  │     └── Aggregate Completion % KPI
  │
  ├── <PortfolioFilterToolbar>
  │     ├── Lane Filter Pills (All, SC, SS, DCSE, TSL, TI)
  │     ├── Status Filter (All, In-Flight, Waiting, Watch, Completed)
  │     ├── Sort Control (Priority, Due Date, Progress)
  │     └── Search Input (Project Key, Title, Owner)
  │
  ├── <ProjectCardGrid> (or Kanban Board View)
  │     └── <ProjectCard>
  │           ├── Lane & Priority Badges
  │           ├── Project Key & Title
  │           ├── Owner & Active PR Link (GitHub deep link)
  │           ├── Progress Bar (% Complete with Task Count)
  │           ├── Blocker Callout (Red alert box if active blockers exist)
  │           ├── Scope Summary Text
  │           └── Quick Action Buttons:
  │                 ├── "Inspect Tasks" (Expands inline task drawer)
  │                 ├── "Log Blocker" (Opens blocker modal)
  │                 └── "Tribunal Sync" (Emits snapshot receipt)
  │
  └── <TaskDetailDrawer> (Slide-over panel)
        ├── Nested pm_tasks list with drag/drop or status toggles
        ├── Add Task inline form
        └── Linked Evidence & Artifacts
```

### 3.2 State Management & Realtime Synchronization

Phase 2 leverages Supabase Realtime channel subscriptions on `dcse_cp.pm_projects` and `dcse_cp.pm_tasks`. When an agent (such as AG or Claude Code) pushes updates or logs work completions via the API or GitHub actions, the Command Post UI updates reactively without requiring a page reload.

---

## 4. API Endpoints & Contract Integration

Phase 2 exposes dedicated REST routes through PostgREST and Next.js / API edge handlers:
1. `GET /rest/v1/v_project_summary`: Retrieves the executive overview with precomputed rollups.
2. `GET /rest/v1/pm_tasks?project_id=eq.{id}`: Retrieves tasks for a selected project.
3. `POST /rest/v1/pm_blockers`: Logs a new blocker with Tribunal notification.
4. `PATCH /rest/v1/pm_projects?id=eq.{id}`: Updates project status, priority, or owner.

### 4.1 Automated Rollup Synchronization with ESCD

To ensure perfect two-way interoperability:
- Projects created or updated in ESCD (`apps/escd/api/mvp.py`) with `context: "project"` are synchronized with `pm_projects`.
- Tasks tagged with a project key (e.g. `PROJ-SC-CTJ`) automatically link into the project task rollup.
- Blocker tags (e.g. `"blocker:..."` in `source_refs`) trigger high-visibility alerts across both ESCD and Command Post.

---

## 5. Rollout Plan & Execution Milestones

| Milestone | Scope | Dependencies | Target Status |
| :--- | :--- | :--- | :--- |
| **M1: ESCD Phase 1** | Runtime canonical projects, `/api/mvp/projects` endpoint, Projects UI tab with status filters and rollups | None (In-memory + PostgREST escd_items) | **COMPLETE (PR #186)** |
| **M2: Supabase Schema** | Execute DDL migration for `pm_projects`, `pm_tasks`, `pm_blockers`, and `v_project_summary` | Supabase SQL console or migration runner | **SPECIFIED (Phase 2)** |
| **M3: Shell Integration** | Replace `PlaceholderCard` in `CommandPostShell.jsx` with `ProjectManagementView` | M2 Schema verification | **SPECIFIED (Phase 2)** |
| **M4: Realtime Sync** | Supabase Realtime broadcast and Tribunal receipt automation | M3 Shell deployment | **SPECIFIED (Phase 2)** |

---

## 6. Tribunal Evidence & Verification Checklist

Before Phase 2 promotion to production:
- [ ] DDL scripts executed and validated against Supabase `nevgdyfpxdaloacuutal`.
- [ ] RLS policies confirmed preventing unauthorized write access to portfolio tables.
- [ ] `CommandPostShell.jsx` passes static lint check (zero em dash, en dash, or undefined variables).
- [ ] Local build test passes cleanly (`npm run build`).
- [ ] Mobile responsive layout verified on 375px viewport (drawer collapsible).
- [ ] Tribunal execution receipt filed in `_Tribunal_Inbox/`.
