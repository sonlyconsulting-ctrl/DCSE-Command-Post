# Supabase read-only operational baseline audit
Task: DCSE-SC-SS-SITES-20261010-01 | Date: 2026-10-11 UTC | Status: PARTIAL, NOT PRODUCTION CERTIFICATION
Authority: v7.3 operative by DCS Level 0 2026-09-21 continuity designation. D15/D16/D21. No mutations performed.

## Scope
Supabase projects: SC-Command-Post nevgdyfpxdaloacuutal (us-east-2), DCSE-DDNA uutpzaiqymyufljdgdaa (us-east-1). Both project-list entries reported ACTIVE_HEALTHY. DDNA deeper advisors returned hibernation and database connection timeout; do not infer end-to-end health.

## SC Command Post readback
Read-only SQL at 2026-10-11 04:19 UTC: 227 tables across schemas including managed internal schemas, 374 pg_policies, 200 RLS-enabled and 27 RLS-disabled tables. All 27 disabled tables observed in managed schemas auth/net/pgmq/realtime/supabase_functions/supabase_migrations/vault, not evidence of an exposed application table without RLS. pg_cron and pg_stat_statements installed. 16 active sessions at snapshot versus max_connections 60. This is not a peak-capacity guarantee.
Five cron jobs: v7_worker_dispatcher_recovery active (5 min, latest succeeded); v7_worker_result_bridge_cycle inactive (last succeeded Sep 16); tsl-sports-sync-5m active (latest succeeded); tsl-hourly-settlement active (latest succeeded); dcse_agent_message_maintenance active (every minute, latest succeeded). Success status does not verify downstream work outcomes.
Security advisor: 27 RLS-enabled tables without policies (may be intentional deny-all); 5 anon-executable SECURITY DEFINER functions, plus pg_net extension in public. Inspect complete advisor output and role access before any change. https://supabase.com/docs/guides/database/database-linter?lint=0028_anon_security_definer_function_executable
Performance advisor: 119 foreign keys without covering indexes; workload-sensitive triage required. https://supabase.com/docs/guides/database/database-linter?lint=0001_unindexed_foreign_keys
Seven active Edge Functions observed, including dcse-agent-relay and dcse-relay. JWT verification false on some privileged surfaces; verify authorization within code before remediation.

## Open assurance gates
1. DDNA hibernation vs ACTIVE_HEALTHY contradiction, query timeout and service-level recovery; repeat controlled health readback.
2. Identify all public-facing SECURITY DEFINER grants, invocation paths and privileges; propose least-privilege remediation after compatibility testing.
3. RLS policy matrix by role and schema, provenance/uniqueness constraints, dedupe tests, and canonical DDL drift.
4. Confirm independent monitoring/alert routing, quota/I-O/storage/connection thresholds, backup/PITR entitlement, recovery drills, and operational owner. Existing cron is NOT independent uptime monitoring.
5. Capture current workload and index statistics before selecting FK indexes; avoid blanket creation.
6. Review inactive result bridge job for deliberate disablement vs orchestration break; do not re-enable without approval.

## DCL
Applied: read-only project inventory, advisor scans, migrations, extensions, edge inventory, catalog SQL and cron run history. Excluded: secrets, auth user rows, PS content, production writes, migrations. Missing: DDNA deep readback, monitoring/backup evidence, complete policy and function review, independent validation. Status PARTIAL; no release/promotion claim.
