# DCSE v7.1 Universal Dispatch Controller

Status: implementation candidate, production DB support applied, Windows cutover pending.

## Why this exists

The canonical `claude_code_poller.ps1` is a provider-bound serialized worker. It can see many tasks, but after it claims one it launches `claude -p` and waits for that child to exit (or hit the 20-minute timeout). That makes the scheduler unavailable to dispatch other runtimes while Claude is busy.

The v7.1 target is instead:

```text
Windows Task Scheduler
        |
        v
DCSE neutral dispatch controller (short-lived, never claims)
        |
        +--> Claude worker wrapper  ----> claude CLI
        |
        +--> Qwen worker wrapper    ----> qwen CLI
        |
        +--> Codex worker wrapper   ----> codex exec
```

The controller finishes immediately after launching eligible worker wrappers. Worker wrappers use per-agent mutexes, so default concurrency is one active task per logical agent while different agents can run in parallel.

## Control-plane ownership

The AI child process does not receive the Supabase service-role credential and does not own task state. The trusted worker wrapper owns:

1. runtime preflight;
2. registry/admission validation;
3. inbox read;
4. PS/DCS/stop-gate checks;
5. atomic claim;
6. runtime-instance heartbeat;
7. child process timeout;
8. artifact verification when `input_refs.expected_artifact` exists;
9. result submission;
10. orphaned-running-assignment recovery.

This avoids duplicate receipts caused by asking the child model and the poller to both call `submit_agent_result`.

## Runtime admission

`dcse_cp.autonomous_dispatch_admission` is fail-closed. Autonomous claim requires:

- active registry row;
- `metadata.poller_eligible=true`;
- no `automatic_task_claim` restriction;
- no `autonomous_polling` restriction.

Current intended state:

- `claude_code`: admitted (verified Windows poller path).
- `qwen_windows_cli`: preflight/admission-smoke only until host artifact verification succeeds.
- `codex`: preflight only until Windows `codex exec` sandbox compatibility is verified.
- `chatgpt`: on-demand connector/orchestration; not a local autonomous worker.

## Qwen admission evidence

On 2026-08-07 the existing smoke task `QWEN-POLLER-SMOKE-20260807-001` produced a real `qwen_windows_cli` claim and result heartbeat. That proves the control-plane identity/handoff path. The receipt itself is insufficient for full admission because it contains an empty summary and null exit code and omits the required file SHA-256.

The cutover script therefore independently verifies on the Windows host:

- `qwen --version`;
- a live Docker or Podman sandbox provider;
- `scratch/qwen_poller_hello_20260807.txt` exists;
- the smoke file contains a Qwen/poller success message;
- SHA-256 of the smoke file.

Only if all of those pass may the script remove `automatic_task_claim` / `autonomous_polling` from `qwen_windows_cli` and set `poller_eligible=true`.

## Qwen runtime policy

Qwen Code is invoked headlessly with a bounded wall time and a Windows container sandbox. The worker uses `--approval-mode auto`; policy/PS boundaries are still enforced before the child is launched.

The worker will not run Qwen autonomously if Docker/Podman is unavailable.

## Codex runtime policy

Codex remains dormant until local preflight verifies the installed CLI exposes non-interactive `exec`, `workspace-write`, and approval-policy controls. The candidate command is sandboxed and non-interactive, but no autonomous Codex claim is permitted until the host preflight is recorded.

## Results Inbox and convergence

Migrations 009/010 add:

- `dcse_cp.runtime_surface_registry`
- `dcse_cp.autonomous_dispatch_admission`
- `dcse_cp.active_stop_gates`
- `dcse_cp.agent_task_convergences`
- `dcse_cp.task_convergence_queue`
- `dcse_cp.agent_results_inbox`
- `dcse_cp.record_task_convergence(...)`

Every new receipt is queued for convergence. Raw assignment results and receipt events remain unchanged; convergence is stored as a separate versioned artifact.

The Results Inbox exposes:

- raw responder results;
- receipt history;
- responder count;
- convergence state;
- consensus/conflicts/missing evidence;
- recommended disposition;
- condensed usable draft.

`TRIB-MSJ57YX0` is the first live convergence example. Claude's original master-instruction response is preserved; ChatGPT recorded convergence v1 with `REVISE_BEFORE_RATIFICATION` and produced `docs/governance/DCSE_V71_MASTER_PROFILE_ACCOUNT_INSTRUCTION_CONVERGED_DRAFT.md`.

## Windows cutover

Canonical cutover package:

`tribunal/v7/runtime-evidence/Invoke-V71UniversalDispatchCutover.ps1`

It:

1. downloads controller/worker files pinned to an exact Git commit;
2. verifies Git blob SHA identities;
3. parses both PowerShell files before install;
4. backs up any existing controller/worker copies;
5. verifies Qwen CLI/sandbox/smoke artifact;
6. writes non-destructive smoke verification evidence;
7. conditionally admits Qwen only if evidence passes;
8. refuses scheduler cutover while the legacy poller process is actively running;
9. disables (does not delete) `DCSE_ClaudeCode_Poller`;
10. registers `DCSE_Universal_Dispatch_Controller` at one-minute cadence;
11. smoke-starts the new controller and verifies its log advances;
12. automatically rolls back to the old scheduled task on failure;
13. writes a local JSON cutover receipt.

## Rollback

Scheduler rollback is intentionally simple:

1. disable `DCSE_Universal_Dispatch_Controller`;
2. enable/start `DCSE_ClaudeCode_Poller`;
3. restore `.pre_cutover_*` controller/worker backups if needed.

The old Claude poller is preserved through cutover and is not deleted.

Database rollback requires reverting migrations 009/010 after ensuring no newer runtime surfaces/convergence records depend on them. Do not drop convergence data casually; it is evidence.

## Promotion gates

Do not promote this controller as canonical until all are true:

- Windows cutover receipt exists;
- controller cycles remain non-blocking;
- Claude can execute while Qwen is independently active/idle;
- Qwen target runtime surface is `qwen_windows_cli` with verified host/sandbox evidence;
- stale `TRIB-MSI2KCUN` is recovered as an orphan rather than left `running`;
- no duplicate scheduler is executing claims;
- Results Inbox shows raw and converged results correctly;
- independent reviewer verifies the PR, live Supabase state, host receipt, rollback, and scope boundaries.
