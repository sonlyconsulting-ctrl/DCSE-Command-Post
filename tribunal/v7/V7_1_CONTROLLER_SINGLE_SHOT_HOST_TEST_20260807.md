# V7.1 Universal Controller — Single-Shot Host Test

Date: 2026-08-07
Host: LAPTOP-74UF76GB

## Observed host result

The neutral controller executed once and returned immediately. `dispatch_controller.log` recorded three launch attempts followed by `Cycle complete; controller did not wait for workers.` This proves the controller itself is non-blocking and does not serialize the global scheduler behind an AI child process.

Observed launch log before correction:

- `claude_code` -> `claude_code_windows_cli`, mode `normal`
- `qwen_windows_cli` -> `qwen_windows_cli`, incorrectly mode `normal`
- `codex` -> `codex_windows_cli`, incorrectly mode `normal`

No new worker heartbeat or running assignment appeared in Supabase after that cycle.

## Root causes isolated

1. Admission booleans returned through PowerShell/PostgREST were being cast with loose `[bool]` semantics. The controller now uses strict true parsing.
2. Worker launch arguments included paths containing spaces (`C:\DS All Things\...`). The controller now builds an explicitly quoted process command line before calling `Start-Process`.
3. Admission must not depend solely on client parsing. Migration `011_enforce_autonomous_claim_admission.sql` now makes `dcse_cp.claim_agent_assignment` fail closed for non-admitted runtimes, with only the explicitly flagged Qwen admission-smoke exception.

## Live DB guard verification

After migration 011:

- Codex non-admitted claim -> `runtime_not_admitted`
- Qwen non-smoke non-admitted claim -> `runtime_not_admitted`

## Legacy state

Before this host test, `DCSE_ClaudeCode_Poller` and `DCSE_PollerHealthMonitor` were manually disabled/stopped. Stale task `TRIB-MSI2KCUN` was reconciled from orphaned `running` to `blocked`. Live running-assignment count was verified as zero before the single-shot controller test.

## Remaining host gate

Re-run one single-shot controller cycle with the corrected controller. Expected modes:

- Claude: `normal`, admitted true
- Qwen: `preflight+admission-smoke`, admitted false until host preflight is satisfied
- Codex: `preflight`, admitted false

Do not register the recurring universal scheduled task until those modes and worker heartbeat/preflight logs are verified.
