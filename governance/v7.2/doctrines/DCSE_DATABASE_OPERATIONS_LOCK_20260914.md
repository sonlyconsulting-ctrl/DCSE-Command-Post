# DCSE Database Operations / DBA Operating Baseline

**Document ID:** DCSE-DBA-OPS-LOCK-20260914  
**Date:** 2026-09-14  
**Status:** LOCKED BY DCS / OPERATIVE-PATCH BASELINE  
**Lane:** DCSE / Command Post / Database Operations  
**Authority:** DCS Level 0  
**Scope:** SC-Command-Post Supabase production and future DCSE database workloads

## 1. Governing Principle

Database health, recoverability, performance, scale, security, and retention are governance concerns.

Supabase/Postgres is not merely implementation plumbing. It carries durable DCSE state, ESCD conversations and operations, evidence, tasks, subjects, knowledge, agent/worker state, product data, audit state, and supporting application data.

**Structure Precedes Scale.**

## 2. Verified Current-State Snapshot

As verified 2026-09-14:

- Project: `SC-Command-Post`
- Project ref: `nevgdyfpxdaloacuutal`
- Region: `us-east-2`
- Status: `ACTIVE_HEALTHY`
- PostgreSQL: 17.6.1
- Supabase organization plan: Free
- Database size: approximately 66 MB
- Current connections observed: 4 idle, 1 active, 2 internal/other
- Largest observed relation: `dcse_cp.relay_listener_events`, approximately 44,948 live rows / 18 MB
- Storage logical object volume observed:
  - avatars: approximately 16 MB
  - sc-feedback-files: approximately 6.5 MB
  - escd-files: approximately 82 KB

Cumulative database statistics observed since stats reset:
- ~10.65 million committed transactions
- ~22,201 rolled-back transactions
- ~158k inserts
- ~998k updates
- ~66k deletes
- 0 recorded deadlocks
- 0 recorded conflicts
- approximately 1 TB cumulative temporary-file I/O, which is query work spill and is not database storage size

## 3. Immediate Recovery Posture

Current Free-plan recovery posture is insufficient for the growing importance of DCSE production state.

Until a paid backup tier is adopted, the minimum required posture is:

1. scheduled logical PostgreSQL backup using supported Supabase CLI / `pg_dump`;
2. encrypted off-site backup retention;
3. separate Supabase Storage-object backup because database backups preserve Storage metadata but not deleted Storage object bytes;
4. defined retention policy;
5. documented restore runbook;
6. regular restore verification.

Target baseline:

- daily logical database backup;
- Storage-object backup;
- at least 7-day short-term retention plus 30-day rolling retention where operationally practical;
- monthly restore drill;
- recorded backup age, verification result, and restore-test evidence.

## 4. DBA Operating Duties

### Capacity and Growth
Track:
- total DB size;
- table/index size;
- row growth;
- Storage growth;
- high-growth event/audit tables;
- WAL/write intensity where available;
- 30/90/180-day growth forecast.

### Performance
Track:
- top/slow queries;
- temporary-file spills;
- sequential-scan hotspots;
- cache-hit behavior;
- connection/pool utilization;
- locks/deadlocks;
- autovacuum/analyze activity;
- query-plan regressions.

### Index Management
Review:
- unindexed foreign keys;
- duplicate indexes;
- unused indexes;
- vector/RAG indexes;
- index bloat;
- query-driven index justification.

No blind bulk index creation or removal is authorized.

### Security / RLS
Review:
- tables with RLS enabled but no policy;
- redundant/multiple permissive policies;
- RLS init-plan inefficiencies;
- SECURITY DEFINER execution exposure;
- extension placement;
- API/database role grants;
- secret and key rotation posture.

### Backup / Restore / DR
Maintain:
- logical DB backups;
- Storage-object backups;
- off-site retention;
- restore runbooks;
- RPO/RTO targets;
- periodic restore certification;
- proof that backup artifacts are actually restorable.

### Retention / Archival
Define lifecycle/retention before event volume scales for:
- orchestration events;
- relay/listener history;
- agent heartbeats;
- audit logs;
- temporary worker/queue state;
- transient operational diagnostics.

Archive before destructive deletion where evidence value exists.

### Schema Governance
Require:
- DDL through migrations;
- development/branch validation before production where supported;
- migration drift detection;
- forward-fix / rollback plan;
- schema ownership and provenance;
- independent validation after structural changes.

### Integrity
Perform periodic checks for:
- foreign-key integrity;
- orphan records;
- duplicate records;
- sequence/identity health;
- expected constraints;
- migration consistency;
- table/index integrity where warranted.

### Cost / Scale
Track triggers for:
- Free → Pro;
- compute-size increase;
- connection pooling changes;
- PITR;
- read replicas;
- Storage/CDN growth;
- Realtime load;
- log-drain/external observability.

## 5. Current Advisor Baseline

As observed 2026-09-14, Supabase performance advisor reports include:

- 115 unindexed foreign keys;
- 92 RLS init-plan inefficiencies;
- 42 multiple permissive-policy cases;
- 9 duplicate-index groups;
- 127 indexes currently reported unused;
- 6 tables without primary keys.

These are triage inputs, not blanket authorization for mass changes.

Security advisor also reports:
- 24 RLS-enabled tables with no policy;
- 1 extension-in-public warning (`pg_net`);
- public/authenticated SECURITY DEFINER exposure requiring review;
- leaked-password protection disabled.

All remediation must be evidence-driven and staged.

## 6. Priority DCSE/ESCD Scale Path

Prioritize DBA review on:
- `dcse_cp.escd_operation_turns`
- `dcse_cp.escd_operation_events`
- `dcse_cp.conversation_turns`
- `dcse_cp.escd_subject_links`
- `dcse_cp.escd_knowledge_records`
- agent/worker tables
- `dcse_cp.relay_listener_events`

These are expected to grow with persistent ESCD and orchestration.

## 7. Scale Stages

### NOW
- ~66 MB database
- controlled internal workloads
- Free plan
- establish backup, restore, monitoring, and retention discipline

### NEXT
- persistent ESCD conversation/event growth
- multiple local/cloud workers
- more product traffic
- review Pro plan, managed daily backups, connection/index/RLS tuning

### GROWTH
- consumer traffic + TSL + persistent RAG + multi-agent activity
- review compute sizing
- partitioning/retention
- PITR if justified by recovery value
- stronger observability

### MATURE
- meaningful revenue/customer-state dependency
- formal RPO/RTO
- tested disaster recovery
- possible read replicas
- external log/metric retention
- restore certification

## 8. Command Post DBA Health Module

Desired operational dashboard fields:

- DB size
- growth trend
- largest tables
- row growth
- Storage size
- connection count/utilization
- cache hit
- temp usage
- slow/top queries
- dead tuples
- last vacuum/analyze
- backup age
- last backup verification
- last restore test
- security-advisor count
- performance-advisor count
- RPO/RTO status
- plan/tier
- scale-trigger state

## 9. Locked Decision

The immediate priority is not database disk capacity.

The immediate priority is **production-grade recoverability and governed DBA discipline before ESCD persistence and product workloads scale further**.

No mass remediation of advisor findings is authorized by this lock.

Next actions should be:
1. establish/verify logical DB backup;
2. establish Storage-object backup;
3. define retention;
4. perform first restore drill;
5. implement DBA Health/Capacity monitoring;
6. triage high-value ESCD/worker performance and security findings;
7. define economic trigger for Supabase Pro/PITR.

**LOCKED BY DCS — 2026-09-14**
