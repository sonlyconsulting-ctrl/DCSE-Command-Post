# DCSE AGY Supabase Discovery Certification Packet v1

**Task ID:** DCSE-ORCH-20260908-007  
**Parent:** DCSE-ORCH-20260908-006 / GitHub Issue #56  
**Lane:** DCSE / Command Post / SYSTEM  
**Task type:** Runtime admission certification  
**Action:** Prove AGY provider execution through the governed control-plane lifecycle using a bounded read-only Supabase discovery workload  
**Status:** EXECUTION READY / NOT YET CERTIFIED

## Preflight Validation

**Authority/source:** Current GitHub governance, Issue #56, provider-neutral inter-agent contract candidate, Antigravity runtime admission addendum.  
**Execution surface:** `agy.exe` 1.1.27 verified by v1.1 smoke test.  
**Systems/access:** SC-Command-Post project `nevgdyfpxdaloacuutal`, Command Post worker/claim surface, local AGY CLI, linked Supabase CLI Management API access.  
**Secret exposure:** PROHIBITED.  
**PS exposure:** NO. PS lane access must remain denied.  
**Approval need:** No approval for bounded read-only certification within existing authorization. Any write/remediation beyond certification bootstrap, governance promotion, public release, PS access, or authority expansion requires escalation.  
**Rollback:** terminate claim/process, release or fail claim according to state machine, preserve evidence, and drop the temporary bootstrap function after successful enrollment. No certification task may perform production DDL or DML.

## Verified source executable asset

`enterprise_discovery.ts`

- path: `C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\dcse-command-post\scripts\enterprise_discovery.ts`
- SHA256: `F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`
- size: `12667`
- LastWriteTime: `2026-09-08 00:55:58` local operator time
- registry asset: `DCSE-AUTO-SUPABASE-DISCOVERY-001`
- registry status: `Review / PENDING`

## Verified AGY process behavior

The v1.1 smoke test established:

- AGY version: `1.1.27`
- noninteractive `--print`: PASS
- JSON status: `SUCCESS`
- exact response assertion: `DCSE_AGY_SMOKE_OK`
- successful exit code: `0`
- invalid flag exit code: `2`
- bounded parent-process timeout path: PASS
- sandbox execution: PASS for nominal smoke

## Live control-plane preparation

Prepared in SC-Command-Post:

- `v7-worker-token` Edge Function is deployed using its custom enrollment authentication path.
- JWT-derived worker API and public RPC bridges are installed.
- `v7_worker.agent_identity` supports `google` as a model family.
- worker identity `antigravity` is registered `approved`.
- authorized lanes: `DCSE`, `SYSTEM`.
- authorized task types: `database`, `discovery`, `validation`, `script`.
- approval mode: `read-only`.
- PS authority: none.
- production DB write authority: none.
- publication/deployment/destructive/credential-access authority: none.

A temporary service-role-only function `v7_worker.bootstrap_antigravity_enrollment()` exists only to generate a worker enrollment secret server-side and return it once to the privileged linked Supabase CLI caller. The plaintext secret is for process-memory use only and must never be printed, persisted to a file, copied to chat, placed in GitHub/Tribunal, or written to logs. Drop the temporary function immediately after successful enrollment.

## Certification queue item

The live worker queue contains:

- task: `DCSE-ORCH-20260908-007`
- queue message: `1008`
- lane: `SYSTEM`
- task type: `discovery`
- priority: `10`
- eligible approved worker: `antigravity` only

The runtime packet instructs AGY to perform read-only metadata discovery through the linked Supabase CLI and return a compact JSON inventory. It explicitly prohibits file changes, DDL, DML, auth changes, GitHub changes, deployments, publication, destructive action, PS access, and credential-value exposure.

## Required lifecycle evidence

1. TASK: `DCSE-ORCH-20260908-007` is present in the Command Post task registry and queue.
2. ENROLL: the AGY worker obtains a host-local enrollment credential without credential disclosure.
3. TOKEN: `v7-worker-token` issues an agent-bound session.
4. IDENTITY: `v7_worker_whoami` resolves `antigravity`.
5. HEARTBEAT: a real host/runtime heartbeat is persisted.
6. CLAIM: queue message `1008` is claimed by `antigravity` with a live lease.
7. EXECUTE: dispatcher invokes `agy.exe` noninteractively with the bounded read-only packet.
8. RESULT: result submission persists against the live claim.
9. VALIDATE: deterministic checks reconcile the output with live database state and verify lane/secret/write protections.
10. CLOSE: claim/task/result evidence is reconciled and the temporary bootstrap function is removed.

## Deterministic acceptance checks

- source asset hash equals `F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`
- AGY runtime version is recorded from the host
- token issuance succeeds without secret disclosure
- JWT identity is `antigravity`
- heartbeat timestamp falls inside the execution window
- claim ID exists for `DCSE-ORCH-20260908-007`
- claim agent is `antigravity`
- runtime surface is `agy_windows_cli`
- process invocation is noninteractive
- process timeout is bounded
- output parses as structured JSON
- reported metadata is independently reconciled against live Supabase state
- no production database write occurred in the AGY task
- no PS resource access occurred
- no credential value appears in persisted output
- result submission references the live claim
- temporary enrollment bootstrap function is dropped after successful enrollment

## Stop gates

Stop rather than bypass if enrollment, token issuance, JWT identity, heartbeat, claim, AGY execution, or result submission fails. Do not substitute direct service-role execution for a failed worker path. Do not broaden Antigravity authority to make certification pass.

## Exit criteria

PASS only when a real Command Post queue item reaches AGY without manual relay of task content, AGY executes the bounded discovery, a result is persisted against the governed claim, deterministic validation reconciles the result with live state, no prohibited access/write is evidenced, and the temporary bootstrap surface is removed. Registry insertion or manual CLI invocation alone is insufficient.
