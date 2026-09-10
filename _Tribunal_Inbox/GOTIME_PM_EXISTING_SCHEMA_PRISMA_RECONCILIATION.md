# GOTIME PM EXISTING SCHEMA PRISMA RECONCILIATION

**Ref:** GoTime Phase 1 Introspection  
**Date:** 2026-07-02  
**Status:** COMPLETE (Introspected & Mapped)

---

## 1. Database Introspection Findings
An inspection of the Supabase PostgreSQL database revealed that the project management backbone tables and `cp_lanes` were previously created via raw SQL migrations but never imported into `schema.prisma`. 

We have successfully extracted the exact column names, constraints, and datatypes for the following tables:
*   `cp_lanes` (CP Lane Registry)
*   `cp_entities` (Entity Registry)
*   `pm_projects` (Core Projects)
*   `pm_workstreams` (Project Workstreams)
*   `pm_tasks` (Project Tasks)
*   `pm_closeouts` (Task/Project Closeouts)
*   `pm_decisions` (DCS Decisions)
*   `pm_blockers` (Execution Blockers)
*   `pm_risks` (Risk Registers)
*   `pm_artifacts` (Execution Deliverables)
*   `pm_model_handoffs` (Model Handoffs & Agent Tasks)
*   `pm_activity_log` (Operational Activity Logs)

---

## 2. Prisma Model Mappings
Below is the exact schema representation of these tables mapped to Prisma syntax, preserving relations and database naming constraints (`@@map`, `@map`):

```prisma
model CpLanes {
  laneCode    String   @id @map("lane_code")
  laneName    String   @map("lane_name")
  description String?
  restricted  Boolean  @default(false)
  createdAt   DateTime @default(now()) @map("created_at") @db.Timestamptz

  projects     PmProjects[]
  workstreams  PmWorkstreams[]
  tasks        PmTasks[]
  closeouts    PmCloseouts[]
  decisions    PmDecisions[]
  blockers     PmBlockers[]
  risks        PmRisks[]
  artifacts    PmArtifacts[]
  handoffs     PmModelHandoffs[]
  activityLogs PmActivityLog[]

  @@map("cp_lanes")
}

model CpEntities {
  entityCode  String   @id @map("entity_code")
  entityName  String   @map("entity_name")
  description String?
  createdAt   DateTime @default(now()) @map("created_at") @db.Timestamptz

  projects     PmProjects[]

  @@map("cp_entities")
}

model PmProjects {
  id                 String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectCode        String    @unique @map("project_code")
  projectName        String    @map("project_name")
  entityCode         String?   @map("entity_code")
  primaryLane        String?   @map("primary_lane")
  classification     String    @default("CONFIDENTIAL")
  status             String    @default("active")
  priority           Int       @default(3)
  purpose            String?
  scope              String?
  ownerLabel         String    @default("DCS") @map("owner_label")
  psLockFlag         Boolean   @default(false) @map("ps_lock_flag")
  secretRiskFlag     Boolean   @default(false) @map("secret_risk_flag")
  mixedLaneFlag      Boolean   @default(false) @map("mixed_lane_flag")
  startDate          DateTime? @map("start_date") @db.Date
  targetDate         DateTime? @map("target_date") @db.Date
  createdAt          DateTime  @default(now()) @map("created_at") @db.Timestamptz
  updatedAt          DateTime  @default(now()) @map("updated_at") @db.Timestamptz

  lane               CpLanes?  @relation(fields: [primaryLane], references: [laneCode], onDelete: Restrict, onUpdate: Cascade, map: "pm_projects_primary_lane_fkey")
  entity             CpEntities? @relation(fields: [entityCode], references: [entityCode], onDelete: Restrict, onUpdate: Cascade, map: "pm_projects_entity_code_fkey")

  workstreams        PmWorkstreams[]
  tasks              PmTasks[]
  closeouts          PmCloseouts[]
  decisions          PmDecisions[]
  blockers           PmBlockers[]
  risks              PmRisks[]
  artifacts          PmArtifacts[]
  handoffs           PmModelHandoffs[]
  activityLogs       PmActivityLog[]

  @@map("pm_projects")
}

model PmWorkstreams {
  id             String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId      String   @map("project_id") @db.Uuid
  workstreamCode String   @map("workstream_code")
  workstreamName String   @map("workstream_name")
  laneCode       String?  @map("lane_code")
  status         String   @default("active")
  priority       Int      @default(3)
  objective      String?
  exitCriteria   String?  @map("exit_criteria")
  blockedFlag    Boolean  @default(false) @map("blocked_flag")
  createdAt      DateTime @default(now()) @map("created_at") @db.Timestamptz
  updatedAt      DateTime @default(now()) @map("updated_at") @db.Timestamptz

  project        PmProjects @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_workstreams_project_id_fkey")
  lane           CpLanes?   @relation(fields: [laneCode], references: [laneCode], map: "pm_workstreams_lane_code_fkey")
  tasks          PmTasks[]

  @@unique([projectId, workstreamCode], map: "pm_workstreams_project_id_workstream_code_key")
  @@map("pm_workstreams")
}

model PmTasks {
  id                     String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId              String    @map("project_id") @db.Uuid
  workstreamId           String?   @map("workstream_id") @db.Uuid
  taskCode               String    @map("task_code")
  taskTitle              String    @map("task_title")
  laneCode               String?   @map("lane_code")
  entityCode             String?   @map("entity_code")
  status                 String    @default("not_started")
  priority               Int       @default(3)
  assignedTo             String?   @map("assigned_to")
  modelRole              String?   @map("model_role")
  taskType               String    @default("execution") @map("task_type")
  description            String?
  dueDate                DateTime? @map("due_date") @db.Date
  psLockFlag             Boolean   @default(false) @map("ps_lock_flag")
  secretRiskFlag         Boolean   @default(false) @map("secret_risk_flag")
  mixedLaneFlag          Boolean   @default(false) @map("mixed_lane_flag")
  stopGateFlag           Boolean   @default(false) @map("stop_gate_flag")
  validationRequired     Boolean   @default(false) @map("validation_required")
  opusValidationRequired Boolean   @default(false) @map("opus_validation_required")
  completionNotes        String?   @map("completion_notes")
  createdAt              DateTime  @default(now()) @map("created_at") @db.Timestamptz
  updatedAt              DateTime  @default(now()) @map("updated_at") @db.Timestamptz

  project                PmProjects @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_tasks_project_id_fkey")
  workstream             PmWorkstreams? @relation(fields: [workstreamId], references: [id], onDelete: SetNull, map: "pm_tasks_workstream_id_fkey")
  lane                   CpLanes?   @relation(fields: [laneCode], references: [laneCode], map: "pm_tasks_lane_code_fkey")

  closeouts              PmCloseouts[]
  blockers               PmBlockers[]
  risks                  PmRisks[]
  artifacts              PmArtifacts[]
  handoffs               PmModelHandoffs[]
  activityLogs           PmActivityLog[]

  @@unique([projectId, taskCode], map: "pm_tasks_project_id_task_code_key")
  @@map("pm_tasks")
}

model PmCloseouts {
  id            String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId     String?   @map("project_id") @db.Uuid
  taskId        String?   @map("task_id") @db.Uuid
  closeoutCode  String?   @map("closeout_code")
  closeoutTitle String    @map("closeout_title")
  laneCode      String?   @map("lane_code")
  status        String    @default("draft")
  verified      String?
  likely        String?
  unknown       String?
  exceptions    String?
  blockers      String?
  nextActions   String?   @map("next_actions")
  run2Status    String?   @map("run2_status")
  createdAt     DateTime  @default(now()) @map("created_at") @db.Timestamptz

  project       PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_closeouts_project_id_fkey")
  task          PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_closeouts_task_id_fkey")
  lane          CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_closeouts_lane_code_fkey")

  @@map("pm_closeouts")
}

model PmDecisions {
  id             String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId      String?   @map("project_id") @db.Uuid
  decisionCode   String?   @map("decision_code")
  decisionTitle  String    @map("decision_title")
  decisionStatus String    @default("proposed") @map("decision_status")
  laneCode       String?   @map("lane_code")
  decisionText   String    @map("decision_text")
  rationale      String?
  authorityLabel String    @default("DCS") @map("authority_label")
  decidedAt      DateTime? @map("decided_at") @db.Timestamptz
  createdAt      DateTime  @default(now()) @map("created_at") @db.Timestamptz

  project        PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_decisions_project_id_fkey")
  lane           CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_decisions_lane_code_fkey")

  @@map("pm_decisions")
}

model PmBlockers {
  id                 String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId          String?   @map("project_id") @db.Uuid
  taskId             String?   @map("task_id") @db.Uuid
  blockerCode        String?   @map("blocker_code")
  blockerTitle       String    @map("blocker_title")
  laneCode           String?   @map("lane_code")
  blockerStatus      String    @default("open") @map("blocker_status")
  blockerDescription String?   @map("blocker_description")
  unblockCondition   String?   @map("unblock_condition")
  createdAt          DateTime  @default(now()) @map("created_at") @db.Timestamptz
  resolvedAt         DateTime? @map("resolved_at") @db.Timestamptz

  project            PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_blockers_project_id_fkey")
  task               PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_blockers_task_id_fkey")
  lane               CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_blockers_lane_code_fkey")

  @@map("pm_blockers")
}

model PmRisks {
  id              String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId       String?  @map("project_id") @db.Uuid
  taskId          String?  @map("task_id") @db.Uuid
  riskCode        String?  @map("risk_code")
  riskTitle       String   @map("risk_title")
  laneCode        String?  @map("lane_code")
  severity        String   @default("medium")
  probability     String   @default("medium")
  riskStatus      String   @default("open") @map("risk_status")
  riskDescription String?  @map("risk_description")
  mitigation      String?
  ownerLabel      String?  @default("DCS") @map("owner_label")
  createdAt       DateTime @default(now()) @map("created_at") @db.Timestamptz

  project         PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_risks_project_id_fkey")
  task            PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_risks_task_id_fkey")
  lane            CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_risks_lane_code_fkey")

  @@map("pm_risks")
}

model PmArtifacts {
  id             String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId      String?  @map("project_id") @db.Uuid
  taskId         String?  @map("task_id") @db.Uuid
  artifactCode   String?  @map("artifact_code")
  artifactName   String   @map("artifact_name")
  artifactType   String   @map("artifact_type")
  laneCode       String?  @map("lane_code")
  localPath      String?  @map("local_path")
  sourcePath     String?  @map("source_path")
  hashSha256     String?  @map("hash_sha256")
  versionLabel   String?  @map("version_label")
  status         String   @default("draft")
  psLockFlag     Boolean  @default(false) @map("ps_lock_flag")
  secretRiskFlag Boolean  @default(false) @map("secret_risk_flag")
  mixedLaneFlag  Boolean  @default(false) @map("mixed_lane_flag")
  notes          String?
  createdAt      DateTime @default(now()) @map("created_at") @db.Timestamptz
  payload        Json?    @db.JsonB

  project        PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_artifacts_project_id_fkey")
  task           PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_artifacts_task_id_fkey")
  lane           CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_artifacts_lane_code_fkey")

  @@map("pm_artifacts")
}

model PmModelHandoffs {
  id                 String    @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId          String?   @map("project_id") @db.Uuid
  taskId             String?   @map("task_id") @db.Uuid
  fromModel          String?   @map("from_model")
  toModel            String    @map("to_model")
  handoffType        String    @map("handoff_type")
  laneCode           String?   @map("lane_code")
  promptPath         String?   @map("prompt_path")
  handoffSummary     String?   @map("handoff_summary")
  validationRequired Boolean   @default(false) @map("validation_required")
  status             String    @default("pending")
  createdAt          DateTime  @default(now()) @map("created_at") @db.Timestamptz
  completedAt        DateTime? @map("completed_at") @db.Timestamptz

  project            PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_model_handoffs_project_id_fkey")
  task               PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_model_handoffs_task_id_fkey")
  lane               CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_model_handoffs_lane_code_fkey")

  @@map("pm_model_handoffs")
}

model PmActivityLog {
  id             String   @id @default(dbgenerated("gen_random_uuid()")) @db.Uuid
  projectId      String?  @map("project_id") @db.Uuid
  taskId         String?  @map("task_id") @db.Uuid
  eventType      String   @map("event_type")
  eventTitle     String   @map("event_title")
  laneCode       String?  @map("lane_code")
  eventDetail    String?  @map("event_detail")
  createdByLabel String?  @default("DCS") @map("created_by_label")
  createdAt      DateTime @default(now()) @map("created_at") @db.Timestamptz

  project        PmProjects? @relation(fields: [projectId], references: [id], onDelete: Cascade, map: "pm_activity_log_project_id_fkey")
  task           PmTasks?    @relation(fields: [taskId], references: [id], onDelete: SetNull, map: "pm_activity_log_task_id_fkey")
  lane           CpLanes?    @relation(fields: [laneCode], references: [laneCode], map: "pm_activity_log_lane_code_fkey")

  @@map("pm_activity_log")
}
```
