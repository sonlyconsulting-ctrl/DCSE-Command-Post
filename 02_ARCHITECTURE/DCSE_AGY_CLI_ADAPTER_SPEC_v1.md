# DCSE AGY CLI Adapter Specification v1

**Task:** DCSE-ORCH-20260908-005  
**Lane:** DCSE / Command Post  
**Status:** CANDIDATE / READY FOR IMPLEMENTATION  
**Depends on:** `DCSE_INTER_AGENT_CONTRACT_v1.md`

## Verified runtime evidence

As of 2026-09-08, operator-supplied local discovery verified:

- executable: `C:\Users\dsead\AppData\Local\agy\bin\agy.exe`
- version: `1.1.12`
- noninteractive execution: `--print` / `-p` / `--prompt`
- structured output: `--output-format text|json|stream-json`
- final-result schema enforcement: `--json-schema`
- workspace extension: `--add-dir`
- model selection: `--model`
- session continuation: `--continue`, `--conversation`
- timeout: `--print-timeout`, default reported as `5m0s`
- sandbox mode: `--sandbox`
- execution mode: `--mode accept-edits|plan`
- permission bypass flag exists: `--dangerously-skip-permissions`
- exit-code semantics: UNKNOWN until tested

The Antigravity `language_server.exe` is not the task-dispatch executable and must not be used by this adapter.

## Security posture

The adapter must default to bounded execution. It must never add `--dangerously-skip-permissions` unless a future controlling policy explicitly authorizes that behavior for a narrowly scoped task. Read-only certification work should use sandbox and/or plan controls where they satisfy the task.

Secrets must be supplied only through approved runtime mechanisms and must never be serialized into task envelopes, command logs, artifacts, receipts, GitHub, or Tribunal.

## Invocation model

Conceptual bounded invocation:

```text
agy.exe --print "<task instruction>" \
  --output-format json \
  --json-schema "<result schema path or schema>" \
  --print-timeout <bounded duration> \
  --add-dir "<authorized workspace>" \
  --sandbox
```

Exact process construction must use an argument array/process API rather than shell-concatenating untrusted task text.

For a read-only discovery task, prefer `--mode plan` only if runtime testing proves that plan mode still permits the required read-only terminal/database discovery actions. Otherwise enforce read-only behavior through task policy, sandbox restrictions, database read-only credentials/session, allowed roots, and deterministic post-execution checks. Do not guess.

## Adapter interface

### `probe()`

- resolve configured executable
- execute `agy --version`
- verify supported minimum version policy when defined
- return executable path, version, timestamp and probe status

### `capabilities()`

Return normalized capabilities such as:

- `noninteractive_prompt`
- `structured_json`
- `json_schema_final_result`
- `sandbox`
- `workspace_add_dir`
- `model_selection`
- `session_resume`
- `bounded_timeout`

### `health()`

Return runtime reachability and last successful probe. Health does not equal admission.

### `execute(task, context)`

1. Revalidate allowed roots and policy decision.
2. Materialize the provider-neutral result schema without secrets.
3. Construct argument array.
4. Spawn `agy.exe` with bounded timeout and controlled working directory.
5. Capture stdout/stderr separately.
6. Capture actual process exit code.
7. Parse JSON output.
8. Verify required artifact paths exist inside allowed roots.
9. Hash artifacts.
10. Return normalized ResultEnvelope.

### `normalizeResult()`

Map provider output into the DCSE ResultEnvelope. Preserve raw provider/model/session identifiers when supplied. Never infer missing identifiers.

### `cancel()`

Terminate only the process/session owned by the current claim. Record cancellation evidence and final process state.

## Exit-code certification

Because `agy --help` does not document exit-code semantics, implementation must include bounded empirical tests:

1. successful print task
2. invalid flag
3. schema failure if reproducible safely
4. timeout
5. permission-denied/sandbox denial if reproducible safely

Record observed process exit codes. Do not generalize undocumented semantics beyond tested cases without evidence.

## First certification workload

Use the existing read-only Supabase enterprise discovery script:

`C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\dcse-command-post\scripts\enterprise_discovery.ts`

Verified operator evidence:

- SHA256: `F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`
- size: `12667` bytes
- LastWriteTime: `2026-09-08 00:55:58` local operator time

Certification requirements:

- no database writes, migrations, deletes, DDL or remediation
- no `auth.users` row disclosure
- no storage object contents
- no secret/environment-value logging
- permission-denied results retained as boundary evidence
- JSON manifest and Markdown narrative output
- hashes for all produced artifacts
- deterministic acceptance report
- execution receipt
- real worker heartbeat and governed claim before runtime is marked admitted

## Gemini CLI

A separate Gemini CLI was also operator-verified on 2026-09-08:

- command resolves through npm shim under the user's roaming npm path
- version `0.56.0`
- headless mode `--prompt`
- structured output `--output-format text|json|stream-json`
- model selection `--model`
- session support `--resume`, `--session-file`, `--session-id`
- sandbox `--sandbox`
- approval controls include `--approval-mode default|auto_edit|yolo|plan`
- policy inputs `--policy` and `--admin-policy`

Gemini must receive its own provider adapter. Do not route Gemini through the AGY adapter merely because Antigravity may use Gemini-family models internally.

## Promotion gate

This specification is not proof that the adapter is live. Promotion requires implemented code, tests, runtime heartbeat, successful governed claim, artifact production, deterministic validation and receipt reconciliation.