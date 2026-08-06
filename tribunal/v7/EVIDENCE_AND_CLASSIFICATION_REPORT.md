# V7_1_ACTION_1_POLLER_HARDENING — Phase 1/2 Evidence and Classification Report

Executor for this pass: Claude Code, acting under the `poller.fallback: "manual authenticated
agent session"` clause in `DCSE_MANIFEST.yaml` — Qwen Coder (`agent_key: qwen_coder`) has no
recorded rows in `dcse_cp.agent_heartbeats` at all, so it has no live task-transport connection
to act on this task. This pass performs the Phase 1 (evidence/location audit) and Phase 2
(reproduce-before-patch, read-only only) steps of
`governance/v7.1/QWEN_CODER_POLLER_REPAIR_AND_TEST_CONTRACT.md`. No `--dispatch`, no credential
access, no scheduled-task state change was performed.

## Phase 1: Evidence and location audit

All files the intake decision (`POLLER_SOURCE_INTAKE_AND_BASELINE_DECISION.md`) listed as
uploaded evidence were located on-disk on this machine (host running this session) and staged
into this branch at `tribunal/v7/`. Verified byte-for-byte identical, via `diff`, against the
copies inside `V7_1_POLLER_AND_TRILOGY_HANDOFF.tar.gz` (outer SHA-256
`ece318ead4732dd3c3370166517398477289c82e5a1ecf7cb75b77bbf6bfac13`, matches its `.sha256`
sidecar; inner manifest self-reports as a partial ChatGPT-side export).

| File | Prior on-disk path | Status |
|---|---|---|
| `job_tribunal_poller_v7.py` | `_Tribunal_Inbox\` | Found, staged |
| `tribunal_v7_state_machine.py` | `_Tribunal_Inbox\` | Found, staged (was flagged "missing" in intake doc — it was not; only untracked) |
| `tribunal_v7_codex_adapter.py` | `_Tribunal_Inbox\` | Found, staged (same correction) |
| `tribunal_v7_fable_adapter.py` | `_Tribunal_Inbox\` | Found, staged (same correction) |
| `TRIBUNAL_POLLER_V7_README.md` | `_Tribunal_Inbox\` | Found, staged as `README.md` |
| `claude_code_poller.ps1` | `v7.0\09_WORKERS\` | Found, staged as evidence |
| `poller_state.json` | `v7.0\09_WORKERS\` | Found, staged as evidence (not canonical config, per intake doc) |
| `poller_log.txt` | `v7.0\09_WORKERS\` | Found, staged as evidence |
| `TRIBUNAL_20260721_POLLER_V7_PREFLIGHT_RESPONSE.snapshot.json` | `_Tribunal_Inbox\_Daily\2026-07-21\` | Found, staged as evidence |

No file content was modified from its original on-disk state. None of the legacy v6-style
variants or the quarantine-suffixed files were touched, staged, or activated.

## Phase 2: Reproduction (read-only)

Queried Windows Task Scheduler on the host (`Get-ScheduledTask` / `Get-ScheduledTaskInfo`,
read-only, no state change):

| Task | State | Last result | Missed runs | Notes |
|---|---|---|---|---|
| `DCSE_ClaudeCode_Poller` | **Disabled** | `267014` (`SCHED_S_TASK_NOT_SCHEDULED_TO_RUN`) | **7,585** | Trigger itself is still `Enabled: True` with an active recurring schedule (`StartBoundary 2026-07-28T15:34:44-04:00`). The task-level disable is what stopped it, not the trigger. |
| `DCSE-V7-Communication-Worker` | Ready | `0xC000013A` (`STATUS_CONTROL_C_EXIT`) | 0 | Separate SC-Command-Post worker, last run terminated abnormally (7/30). Not in scope for this task per the intake doc's split, noted for awareness. |
| `DCSE_PollerV7_Smoke_20260723_2019` | Ready | `267014` | 0 | One-off smoke test, ran once 7/24, no recurring schedule. Not the production poller. |

**Root cause (reproduction target #1, confirmed):** `DCSE_ClaudeCode_Poller` — the scheduled
task registered by `Register-ClaudeCodePollerTask.ps1` — is disabled at the task level. Its
trigger is intact and would fire on schedule if the task were re-enabled. This alone accounts
for the outage; 7,585 missed runs indicates it has been off for an extended period.

**Not yet reproduced (require live execution, out of scope for a read-only pass):**
targets #2–6 from the contract (PS1 authentication/heartbeat write, atomic task-claim behavior,
temporary allowlist blocking, credential decryption, whether the v7 Python candidate's imports
resolve at runtime). These require either a controlled `--audit`-only run or static import
resolution, neither of which was executed in this pass to avoid any live side effects without
a separate, explicit go-ahead.

## Phase 3: Classification (preliminary)

| Component | Classification | Basis |
|---|---|---|
| `job_tribunal_poller_v7.py` + adapters/state machine | RETAIN | Matches intake doc's "Governed v7 candidate" / "REPAIR BASELINE" disposition. Present, unmodified, imports not yet runtime-verified. |
| `claude_code_poller.ps1` | RETAIN, TEST | Per intake doc disposition. Not executed in this pass. |
| `DCSE_ClaudeCode_Poller` scheduled task | WRAP | Re-enabling the existing task (no architecture change) is sufficient to restore transport, pending the untested items above. |
| Legacy `job_tribunal_poller.py` variants, `start_tribunal_poller_20260604.cmd` | RETAIN AS EVIDENCE ONLY | Unchanged from intake doc disposition; not staged into this branch. |

## Unresolved blockers

- Task Scheduler re-enable is an operational action outside a read-only audit; not performed
  in this pass.
- Live `--audit`-mode run of `job_tribunal_poller_v7.py` to confirm import resolution and
  authorization-block handling not performed in this pass.
- Qwen Coder heartbeat gap is unexplained — worth a direct check of whatever process is
  supposed to be running it, separate from this poller.

## Recommendation

Re-enabling `DCSE_ClaudeCode_Poller` is a state change (`bounded_infrastructure_repair`,
operationally authorized per the manifest) but is being left for explicit sign-off rather than
performed silently in this pass, since it resumes live, unattended task execution. Everything
else in this report is read-only evidence.
