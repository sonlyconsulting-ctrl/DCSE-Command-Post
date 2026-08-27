# Sandbox Test Evidence — V7_1_ACTION_1_POLLER_HARDENING

Task key: `V7_1_ACTION_1_POLLER_HARDENING`
Scope: the four sandbox-verifiable tests named in this task's own
`policy_flags.required_tests` — `python_import_resolution`,
`static_authorization_checks`, `idempotency_unit_test`,
`receipt_schema_validation`. Run entirely in a Linux sandbox: no Windows
host, no Task Scheduler, no live credentials, no production writes.

## Evidence coverage acknowledgment

Reviewed against the exact baseline this task's `input_refs.baseline_sha256`
points to (`08326db8...`, `tribunal/v7/job_tribunal_poller_v7.py`), plus its
three companion modules and `claude_code_poller.ps1`
(`input_refs.worker_poller_sha256`, `c19c82d2...`) — all present in this
repo at `v7.1/`. Did not have access to `DESKTOP-PG1JATE`, Windows Task
Scheduler state, or the live poller host; those items in
`governance/v7.1/QWEN_CODER_POLLER_REPAIR_AND_TEST_CONTRACT.md` (Task
Scheduler firing, live heartbeat write, restart recovery, network/outage
simulation) are **not** covered here and require the actual host.

## Root cause statement (of the stalled task, not the poller)

Live `dcse_cp` query state at time of review:

- `V7_1_ACTION_1_POLLER_HARDENING` was handed to Qwen Coder twice
  (04:23 and 04:31 UTC) via `agent_task_events`. No acknowledgment, receipt,
  or any event followed.
- `dcse_cp.relay_listener_events` has zero rows ever for Qwen Coder's
  agent ID — no automated listener has ever polled this project for it.
- `docs/COMMUNICATION_GATE_001_QWEN_LOCAL_EXECUTION.md` describes the setup
  needed to give Qwen a real scheduled-task listener, targeted at the
  **staging** project (`liwdquzuigrlgfzgmpjp`), not production. Nothing
  indicates this gate was ever run against production.

Conclusion: the task did not stall mid-execution — there was never a live
Qwen worker consuming it. Reassignment/direct execution, not waiting, is
the correct next step (matches the second DCS handoff's own instruction:
"do not wait for host access").

## Separate finding: unversioned production hotfix

The 04:46 UTC receipt claimed a TOCTOU fix to `dcse_cp.claim_agent_assignment`
(status-guarded atomic UPDATE replacing a SELECT-then-UPDATE race). Verified
via `pg_get_functiondef()` against the live function: **the fix is real and
correctly implemented.** However it exists only in production — no migration
file, no PR, no review — which is the same defect class already tracked in
this repo as D11 (see `20260727231413_v7_capture_prod_hotfixes_and_search_
path.sql`) and directly contradicts this task's own
`production_changes:false` / `test_before_patch:true` policy flags.
Captured as `20260803090212_v7_1_capture_claim_agent_assignment_toctou_fix.sql`
(a no-op against current prod state — pure version-control catch-up).

## Component classification

| Component | Classification | Notes |
|---|---|---|
| `job_tribunal_poller_v7.py` + adapters + state machine | RETAIN | Imports cleanly, authorization gate and state machine hold up under adversarial inputs (see tests). Candidate/file-packet system, not the live Supabase-backed path. |
| `claude_code_poller.ps1` (Supabase-backed operational poller) | RETAIN | `claim_agent_assignment` RPC verified atomic in production. Not exercised end-to-end here (needs live host). |
| `claim_agent_assignment` (Postgres RPC) | RETAIN, now versioned | Correct logic; was unversioned prod drift, now captured. |
| Qwen Coder automated listener | REPLACE / not yet built | No evidence it has ever run against production. `COMMUNICATION_GATE_001` targets staging only. |

## Tests executed and results

`python3 -m unittest discover -s v7.1/tribunal/v7/tests -v` — **19/19 pass**,
covering:

- **python_import_resolution**: all 4 v7 modules import cleanly; all 12
  names the poller imports from the state machine and adapters resolve.
- **static_authorization_checks**: rejects missing `authorization` block,
  non-`GO` decision, unapproved worker, invalid sandbox value, out-of-range
  timeout, working directory outside the allow-root, path-traversal and
  absolute `expected_outputs`, and prompts under the 20-character floor.
  Accepts a fully valid packet.
- **idempotency_unit_test**: a second pass over an unchanged source with a
  terminal receipt returns `IDEMPOTENT_SKIP` and the same receipt path; a
  changed source (different `source_sha256`) is correctly *not* skipped;
  `run_once` over two packets returns the same task-ID set on repeated runs.
- **receipt_schema_validation**: `new_receipt()` output has all required
  fields and the correct initial state; illegal state transitions
  (`RECEIVED` → `COMPLETED` directly) raise `GovernanceError`;
  `verify_worker_result()` rejects a task-ID mismatch and rejects a
  declared-but-not-actually-written expected output (fail closed, never a
  false completion).

## Files changed

- `v7.1/tribunal/v7/tests/test_poller_v7_sandbox.py` (new)
- `v7.1/tribunal/v7/tests/SANDBOX_TEST_EVIDENCE_V7_1_ACTION_1.md` (new, this file)
- `supabase/migrations/20260803090212_v7_1_capture_claim_agent_assignment_toctou_fix.sql` (new)

No existing poller source was modified. No production data or schema was
changed by this work (the migration file documents existing state; it was
not applied).

## Rollback

Revert the three files above. The migration is additive/idempotent
(`create or replace`) and matches what's already live, so there is nothing
to roll back in the database itself.

## Unresolved blockers (require the Windows host)

- Task Scheduler firing/state, live heartbeat write, restart recovery,
  network/Supabase/GitHub outage simulation — all require
  `LAPTOP-74UF76GB` or equivalent.
- Whether an automated Qwen Coder listener should be stood up against
  production, or whether Qwen is intended to be driven manually/in-session
  instead — a scope decision, not a technical blocker.

## Recommendation

RETAIN the existing poller architecture and the `claim_agent_assignment`
fix (now versioned). Do not build a second poller. Resolve the Qwen
listener gap by either running `COMMUNICATION_GATE_001` against production
or by explicitly changing how Qwen-directed tasks are dispatched — DCS
decision, not a coder decision.
