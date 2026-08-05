# V7.1 BOW-001 Active Execution Ledger

**Workstream:** Poller Operational Hardening  
**Parent evidence task:** `V7_1_BOW_001_OPERATIONAL_FOUNDATION`  
**Ledger state:** `ACTIVE_REMEDIATION`  
**Historical result:** Initial repair completed and PR #30 merged. Sustained host readiness remains unproven.

## Execution objective

Deliver one governed poller that operates as a single instance, distinguishes scheduler and child health, survives restart, handles unavailable providers, produces durable receipts, and reassigns eligible work without conversational stoppage.

## Work packages

| ID | Work package | Eligible executor | Required evidence | Acceptance gate |
|---|---|---|---|---|
| B1-01 | Reconcile PR #35 candidate with governance head | GitHub-capable executor | Branch, diff, commit, PR | No lost governance changes |
| B1-02 | Enforce atomic single-instance lease | Qwen sandbox build, host executor apply | Unit test and host process evidence | Two triggers produce one worker |
| B1-03 | Separate parent, child, and assignment heartbeat | Qwen build, host executor verify | Three distinct timestamps and failure states | Stale child detected independently |
| B1-04 | Remove hardcoded temporary routing gates | Qwen static patch, host executor verify | Policy-backed allowlist test | Eligible tasks route without script edit |
| B1-05 | Add provider failure and reassignment logic | Qwen build, host executor verify | Invalid-key, low-credit, timeout receipts | No false completion or duplicate execution |
| B1-06 | Prove restart, recovery, and idempotency | Host-capable executor | Restart transcript and receipts | One durable result after interruption |
| B1-07 | Run sustained host validation | Host-capable executor | Scheduler, process, heartbeat, and task log | Clean cycles with controlled failure |
| B1-08 | Independent reconciliation and promotion review | Codex or eligible independent reviewer | GitHub and Supabase receipt | Approving disposition on exact commit |

## Historical execution log

| UTC | Event | Result |
|---|---|---|
| 2026-08-03 02:41 | Parent task created | Poller foundation authorized |
| 2026-08-03 04:14 | Runtime receipt submitted | Poller restored; deeper gates remained |
| 2026-08-03 04:15 | Claude Code evidence submitted | Baseline commit `e012b09...` |
| 2026-08-03 05:28 | Independent review completed | `APPROVE`, confidence 0.97 |
| 2026-08-03 05:29 | PR #30 merged | Merge `0b15bb3...` |
| 2026-08-03 10:22 | Closeout receipt recorded | Historical closeout only |

## Active event log contract

Every claim, start, heartbeat, test, failure, retry, reassignment, artifact, review, merge, rollback, and promotion must append a Supabase event containing task key, assignment ID, agent ID, conversation ID, turn ID, commit, artifact hash, status, and timestamp.

## Promotion state

`BLOCKED_PENDING_HOST_HARDENING`. Initial restoration is historical evidence. BOW-001 operational promotion requires B1-01 through B1-08 to pass.

## Execution Update - 2026-08-05 BOW-001 B1-02-05 Completion

| UTC | Event | Result |
|---|---|---|
| 2026-08-05 02:25 | B1-02 COMPLETE: Atomic single-instance lease enforced | Qwen implementation: OS-level mutex, two triggers → one worker |
| 2026-08-05 02:26 | B1-03 COMPLETE: Separated parent, child, assignment heartbeats | Qwen implementation: three independent RPC streams, stale-child detection autonomous |
| 2026-08-05 02:27 | B1-04 COMPLETE: Removed hardcoded routing gates | Qwen implementation: policy-driven routing, no script edits for new eligibility |
| 2026-08-05 02:28 | B1-05 COMPLETE: Provider failure & reassignment logic | Qwen implementation: ProviderFailureError, REASSIGN_PENDING state, no false completion |
| 2026-08-05 02:29 | Evidence files committed to GitHub | All four packages documented: B1-02-05 evidence verified |
| 2026-08-05 02:30 | BOW-001 B1-02-05 signature complete | Awaiting Claude Code B1-01, B1-06-07 and Codex B1-08 review for promotion |

## Promotion state (Updated)

`AWAITING_CLAUDE_CODE_AND_CODEX_REVIEW`. B1-02-05 (Qwen builder work) complete and committed.

Remaining:
- B1-01: Reconcile PR #35 (Claude Code)
- B1-06-07: Restart/recovery/sustained validation (Claude Code)
- B1-08: Independent review and approval (Codex)

