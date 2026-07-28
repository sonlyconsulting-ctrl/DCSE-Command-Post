# DCSE V7 Convergence Review 001 — Communication

Date: 2026-07-28  
Repository: `C:\DS All Things\DCSE_Command_Center\DCSE_V7_Runtime`  
Branch: `chatgpt/v7-foundation-runtime-compiler`  
Gate 001: PASS, independently hash-verified  
Promotion recommendation: **READY FOR CANONICAL MERGE**

## Canonical communication artifacts

- Queue authority: `v7_worker.queue_message`. The `pgmq` extension is installed, but `pgmq.meta` contains zero queues and `pgmq` has no physical message/archive tables.
- Claims: `v7_worker.task_claim` through the verified JWT-bound worker RPC surface.
- Results: `v7_worker.result_submission` bridged to `dcse_cp.agent_task_events`.
- Identity: `app_metadata.agent_id` resolved by `v7_worker_private.session_agent_id`; `user_metadata` is not used.
- Token broker: `supabase/functions/v7-worker-token/index.ts`, requiring an enrollment secret whose database copy is bcrypt-hashed.
- Bridge entry point: `supabase/functions/v7-result-bridge/index.ts`, with the database bridge remaining authoritative.
- Durable worker: `workers/claude-reviewer-operational.js`, installed through `scripts/windows/install-dcse-communication-worker.ps1`.
- Migration lineage: thirteen PR 14 communication migrations imported unchanged for auditability.
- Rollback: `supabase/rollback/v7_restricted_rpc_rollback.sql`; the known destructive type reversion is commented out.

## PR 14 and PR 15 joint review

PR 14 is mergeable but is not a valid wholesale merge candidate. Its 32 commits combine the communication system with later Runtime, Rule, Skill, Workflow, Acceptance, Promotion, and Completion implementations. It also changes an unrelated Vow & Go migration. Only the bounded communication artifacts in the copy plan are eligible for this wave.

PR 15 is the convergence carrier. Its Gate scripts, installer, operational worker, and v7 candidate control artifacts are the correct closeout base. Its PR description is stale because it still reports B1 and B5 as pending; the PASS receipt proves both for the staging Claude worker.

## Duplicate, obsolete, and unsafe artifacts

- No byte-identical duplicates existed in the 70-file initial inventory.
- The cycle-one duplicate is operational evidence, not a file duplicate. Claims 32 and 33 and submissions 31 and 32 are preserved; both are acknowledged and closed.
- `workers/claude-reviewer-worker.js` is superseded by the deployed operational worker.
- Gate 001 runbook, SQL, and one-shot PowerShell are ARCHIVE after PASS and must not be rerun.
- The original `v7-worker-auth` version 1 was obsolete and unsafe. CR-SEC-001 replaced it in staging with version 2, a deny-all HTTP 410 tombstone containing no signing or credential path. Caller-asserted and empty requests both return 410 with no token-shaped data.
- The old deployment guide is unsafe operational guidance: it presents the obsolete endpoint as the token source and includes destructive queue and database rollback instructions.

## Material contradictions preserved

1. The early PR 14 communication receipt says autonomy and bridging were BLOCKED. Later O1 and B3/B4 receipts pass their narrower preview checks. Gate 001 subsequently proves a real durable worker cycle and supersedes the B1/B5 blockers for staging only.
2. Earlier convergence evidence recorded `20260727231413_v7_capture_prod_hotfixes_and_search_path.sql` as missing from live migration history. The post-remediation migration list contains version `20260727231413`; the earlier contradiction is preserved here as resolved drift history.
3. Supabase security advisors warn that seven public `SECURITY DEFINER` worker RPCs are executable by `authenticated`. Their inner functions require an approved identity derived from immutable `app_metadata`; `anon` execute remains revoked and the internal functions remain service-role only. The warning is intentional and documented, and CR-SEC-001 is separately closed.
4. Gate cycle one was reclaimed after the first acknowledgment window. The second result is preserved as evidence; the completion marker containment prevents further reclaim.

## Validation state

- PASS receipt hash: verified.
- Live heartbeat: current at read-only verification.
- RLS: enabled on every `v7_worker` table; policies and grants cataloged.
- RPC: identity is JWT app-metadata-bound; internal privileged functions are service-role only and use empty `search_path`.
- Queue: no active claims, no unacknowledged submissions, no dead-letter rows at verification.
- v6.9: tree hash equals `origin/main` and remains immutable.
- Package lock: untouched, untracked, empty root lockfile; origin actor cannot be proven from filesystem evidence. Its form is consistent with an accidental root-level npm invocation. Disposition is preserve-untracked and exclude from promotion commits.
- Endpoint security: `v7-worker-auth` version 2 returns HTTP 410 for empty and caller-asserted requests; no token fields or JWT-shaped values are returned.
- Canonical broker: missing and invalid enrollment secrets return 400/401; the DPAPI-governed staging enrollment produced HTTP 200 without disclosing credentials or tokens.
- SC-safe path: authenticated `v7_worker_whoami` and read-only `v7_worker_my_active_claims` both returned HTTP 200; the identity is approved for SC and had zero active claims.
- Drift: all thirteen v7 communication migrations are recorded in live history.
- Rollback: transactional rollback mid-state was reached and rollback restored the private schema, triggers, unique index, foreign key, execute revocations, and locked search path.
- Worker: current heartbeat remained live on `claude-sonnet-5` with no recorded error.

## Gate decision

CR-SEC-001 is CLOSED. The bounded communication convergence carrier is ready for publication and canonical merge. Communication promotion becomes effective only after that merge; production activation remains unclaimed, and the Runtime Compiler branch must be created from the canonical post-promotion commit.

No production DDL, v6.9 change, credential disclosure, branch deletion, or later-subsystem implementation occurred in this review.
