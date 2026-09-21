# DCSE v7.3 Canonical Database Schema Baseline Standard

**Task ID:** DCSE-V73-SCHEMA-BASELINE-20260921-01  
**Status:** CANONICAL OPERATIVE BASELINE  
**Authority:** DCS Level 0 Approved  
**Effective Date:** 2026-09-21  
**Lanes:** Architecture / Database Administration / Governance  
**Controlling Doctrines:** Doctrine D15 (Database Administration v7.2/v7.3 Alignment), Doctrine D22 (Source Authority and Runtime Distribution)  
**Artifact Manifest:** `governance/v7.3/schema/DCSE_V73_CANONICAL_SCHEMA_INVENTORY_MANIFEST_20260921.json`  
**Authoritative DDL Baseline:** `supabase/schema/DCSE_V73_CANONICAL_DDL_BASELINE_20260921.sql`  

---

## 1. Purpose & Mandate

This standard establishes the unified, versioned, canonical database schema baseline for the DCSE enterprise. Under **Doctrine D15** and **Doctrine D22**, database schemas, tables, enums, functions, and policies must have a definitive canonical source in GitHub `origin/main` rather than existing as fragmented, unversioned, or ad-hoc states in live PostgreSQL instances.

This baseline resolves historical schema fragmentation across legacy Prisma definitions, raw migrations, and ad-hoc scripts, establishing a single authoritative DDL reference.

---

## 2. Dual-Database Architectural Topology

The estate operates across two distinct Supabase PostgreSQL instances with strict role segregation:

1. **`DCSE-DDNA` Supabase (Constitutional & Knowledge Registry):**
   * **Role:** Stores constitutional authority records, canonical doctrine linkage, registry records, extracted DDNA signals, knowledge files, prompts, and relationship graphs.
   * **Write Policy:** Strict DBA stop-gate; mutations occur only via verified promotion and administrative synchronization pipelines.
   * **Isolation:** Isolated from operational user chatter and high-frequency poller transactions.

2. **`SC-Command-Post` Supabase (Operational & Application State):**
   * **Role:** Stores runtime tasks, worker inboxes, agent coordination queues, consumer profiles, credit ledgers (`scn_ledger`), and application data (TSL, Vow & Go, Smoove Spots).
   * **Write Policy:** Transaction-bound execution, authenticated worker leases, and consumer application RPCs.
   * **Reference Integrity:** References DCSE-DDNA authority by canonical ID/key; does not independently create doctrine authority.

---

## 3. Schema Structure & Inventory

The canonical baseline inventories **103 total cataloged tables** across four primary schemas:

* **`public` (82 Models / Tables):**
  * Core Governance & Registry: `Doctrine`, `Entity`, `Persona`, `Profile`, `Instruction`, `Product`, `Service`, `OperationalAsset`, `Workflow`, `AppModule`, `ContentAsset`, `KnowledgeFile`, `PromptAsset`, `RegistryRecord`, `AuditLog`.
  * Command Post Project Management: `PmProjects`, `PmWorkstreams`, `PmTasks`, `PmDecisions`, `PmArtifacts`, `PmActivityLog`.
  * Operational State: `profiles`, `scn_ledger`, `dcse_plan_inbox`, `dcse_plan_reviews`, `dcse_eod_runs`, `dcse_eod_assets`, `dcse_runtime_hosts`.
* **`dcse_cp` (3 Tables):**
  * Agent Coordination: `agent_registry`, `agent_tasks`, `agent_task_events`.
* **`v7_worker` (9 Tables):**
  * Worker Runtime: `agent_identity`, `task_claim`, `heartbeat`, `result_submission`, `bridge_receipt`, `queue_message`, `dead_letter`, `cost_ledger`, `stop_gate`.
* **`family_vow_go` (9 Tables):**
  * Application Domain: `wedding_settings`, `wedding_events`, `guests`, `budget_items`, `vendors`, `music_items`, `content_chapters`, `external_integrations`, `admin_feedback`.

---

## 4. Change Control & Promotion Rules (Class R4)

Under the **DCSE v7.3 Vercel & Supabase Release Standard (PR #169)**:

1. **All Schema Modifications Are Class R4 (Critical):**
   * Any change to database schemas, tables, column definitions, enums, triggers, RLS policies, or `SECURITY DEFINER` functions is strictly classified as **R4**.
2. **Explicit Level 0 Authorization Required:**
   * No database migration may be executed against live production Supabase instances without explicit DCS Level 0 approval.
3. **Mandatory Preflight Artifacts:**
   * An R4 migration packet must include:
     * Idempotent SQL migration script.
     * Verified SQL rollback script.
     * Automated role-matrix test verification.
     * Tribunal promotion receipt.
4. **Git Canonical Precedence (D22 §3.1):**
   * Migrations must be committed to GitHub `origin/main` before or concurrently with verified execution by Antigravity (AG).

---

## 5. Outstanding Database Debt Register

The following items are formally cataloged for resolution under the upcoming **Class R4 Database Remediation Package (DCSE-SUPABASE-IO-HARDENING-20260917)**:
* **Unindexed Foreign Keys:** 117 instances (to be prioritized and indexed based on `pg_stat_statements` hot paths).
* **Unused Indexes:** 130 instances (to be dropped to eliminate write amplification and preserve Disk I/O budget).
* **Missing Primary Keys:** 6 tables requiring explicit surrogate or natural primary keys.
* **Security Definer Function Authorization:** Restriction of `public.grant_tsl_reward` and `dcse_cp.get_agent_inbox`.
