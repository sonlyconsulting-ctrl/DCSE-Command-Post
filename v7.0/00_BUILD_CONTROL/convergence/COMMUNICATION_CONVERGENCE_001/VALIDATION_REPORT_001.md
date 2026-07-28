# Communication Convergence Validation Report 001

Date: 2026-07-28  
Target: Supabase staging project `liwdquzuigrlgfzgmpjp`  
Gate 001 rerun: No

## Results

| Check | Result | Evidence |
|---|---|---|
| PASS receipt SHA-256 | PASS | `9C5D6F485566ADBC035284F74EA5BDC10AA76BF4953D4DE3AD9753ABEA8B598C` |
| Deterministic static suite | PASS, 11/11 | Canonical worker, token broker, bridge, decommission payload, archived v1 source, migration set, rollback guard, v6.9 presence |
| Local CI harness | PASS, 0 failures | JSON parse, JavaScript syntax, deterministic suite, secret scan, v6.9 tree, package-lock boundary |
| GitHub/Vercel checks | PASS | PR 15 published at `f4ece675`, Vercel Ready, then merged as `6abb96fe`; PR 14 closed unmerged as superseded |
| GitHub Actions | NOT CONFIGURED | No pull-request workflow runs were returned for either head |
| RLS/RPC read-only suite | PASS, 10/10 | RLS coverage, locked search paths, app-metadata identity, queue and Gate correlations |
| Supabase security advisors | PASS WITH DOCUMENTED WARNINGS | Seven public authenticated worker RPC warnings remain identity-gated; anon execute is revoked and internal functions are service-role only |
| Secret scan | PASS | No secret-value patterns detected; names and placeholders are permitted |
| Drift check | PASS | All thirteen v7 communication migration versions, including `20260727231413`, are recorded in live history |
| Rollback validation | PASS | Transactional rollback mid-state reached; sentinel rollback restored both triggers, private schema, unique index, FK, and hardened search paths |
| Queue quiescence | PASS | No active claims, unacknowledged submissions, or dead-letter rows at verification |
| PGMQ | CONFIRMED ABSENT | Extension installed; physical queue count is zero; `v7_worker.queue_message` is authoritative |
| v6.9 immutability | PASS | `HEAD:v6.9` equals `origin/main:v6.9`, tree `2389d526615330d31adb4f879e5f8595968638e2` |
| `package-lock.json` | PASS boundary | Hash unchanged, still untracked, excluded from commit scope |
| Obsolete endpoint security | PASS | `v7-worker-auth` version 2 returns HTTP 410 for empty and caller-asserted requests; no token fields or JWT-shaped values |
| Canonical broker negative path | PASS | Missing enrollment secret returns 400; invalid enrollment secret returns 401 |
| Canonical broker positive path | PASS | Governed DPAPI enrollment returned HTTP 200; identity matched and token values were not emitted |
| SC-safe auth/task path | PASS | `v7_worker_whoami` and read-only `v7_worker_my_active_claims` returned 200; SC authorized; zero active claims |
| Worker/model regression | PASS | Current heartbeat on `claude-sonnet-5`; no recorded error; heartbeat age 27 seconds at check |
| Permission preservation | PASS | Public wrappers remain authenticated/service-role only; internal privileged functions remain service-role only; anon execute remains revoked |

## Security finding CR-SEC-001

The vulnerable staging Edge Function `v7-worker-auth` version 1 was replaced by version 2, deployment SHA-256 `d1e5964f817a0144dbad289c0546e471c9b2b63ab7df445f086cde96f3477773`. Version 2 is an inert HTTP 410 tombstone with no signing library, JWT secret, Supabase credential reference, or token-minting path.

Result: **CLOSED**. Repository, database routine/cron, and 210-task Windows Scheduler scans found no valid dependency. Endpoint, broker, heartbeat, RLS/RPC, advisor, drift, permission, and rollback validations passed. The carrier is ready for publication and merge; promotion is not effective until canonical merge.

## Tests deliberately not executed

- Gate 001 was not rerun.
- `tests/v7_worker_tests.sql` from PR 14 was not imported or run because it persists fixtures, contains misleading pass logic, and is superseded by bounded deterministic and read-only validation.
- No production SQL or deployment action was performed. The only remote mutation was replacement of the staging `v7-worker-auth` function.
