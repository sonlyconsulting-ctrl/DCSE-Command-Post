# V7.1 BOW-003 Active Execution Ledger

**Workstream:** TSL Production Remediation  
**Parent evidence task:** `V7_1_BOW_003_TSL_AUDIT_INVENTORY`  
**Audit state:** Complete  
**Product state:** `NON_PASS`  
**Ledger state:** `ACTIVE_REMEDIATION`

## Execution objective

Close the verified TSL security, canonical-source, identity, favorites, sports-data, deployment, recovery, privacy, and commercial-readiness gaps.

## Work packages

| ID | Work package | Eligible executor | Required evidence | Acceptance gate |
|---|---|---|---|---|
| B3-01 | Inventory exposed views and privileged functions | Qwen static analysis plus Supabase executor | Object and grant matrix | Complete exposed-surface inventory |
| B3-02 | Remediate security-definer view and functions | Supabase executor | Migration, role tests, advisor results | No unauthorized invocation |
| B3-03 | Reconcile canonical TSL application source | GitHub-capable executor | Canonical branch, build, commit | Reproducible governed source |
| B3-04 | Consolidate `profiles` and `global_users` | Qwen patch, Supabase executor apply | Migration and reference tests | One governed identity model |
| B3-05 | Consolidate favorites models | Qwen patch, executor apply | Migration and API tests | One favorites source of truth |
| B3-06 | Build sports feed freshness and coverage controls | Qwen Coder | Provider tests, scheduler, receipts | Defined active-sport coverage and freshness |
| B3-07 | Complete product E2E, privacy, deployment, and rollback tests | Host and browser capable executor | Test suite and deployment receipt | All release tests pass |
| B3-08 | Independent security and readiness review | Codex or independent reviewer | Exact-commit reconciliation | TSL readiness changes from `NON_PASS` |

## Historical execution log

| UTC | Event | Result |
|---|---|---|
| 2026-08-03 02:41 | BOW-003 created | Initially sequenced after BOW-002 |
| 2026-08-03 06:00 | Claude assignment created | Later blocked |
| 2026-08-03 07:34 | Credential failure diagnosed | Persistent exhausted API key removed |
| 2026-08-03 08:07 | Execution timed out | No successful Claude output |
| 2026-08-03 09:25 | Codex recovery completed | PR #36 merged; audit accepted |
| 2026-08-03 10:22 | Closeout receipt recorded | Product remained `NON_PASS` |

## Active event log contract

Each change must bind its conversation and turn to a B3 work package, branch, commit, migration, test run, advisor result, deployment target, rollback, review, and promotion receipt.

## Promotion state

`BLOCKED_PENDING_SECURITY_AND_PRODUCT_REMEDIATION`. Audit completion does not authorize production release.
