# DCSE AGY Local Execution Packet

**Task:** DCSE-ORCH-20260908-006  
**Purpose:** Execute the bounded local tests required before the live Command Post certification run.

Run from the repository root on the authorized Windows host:

`C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project`

## Step 1. Synchronize canonical main

```powershell
git checkout main
git pull origin main
```

Do not switch to a provider-specific branch for this certification unless DCS explicitly directs it.

## Step 2. Verify local discovery asset hash

The canonical local script is nested under `dcse-command-post`:

```powershell
Get-FileHash .\dcse-command-post\scripts\enterprise_discovery.ts -Algorithm SHA256
```

Expected SHA256:

`F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`

If the hash differs, STOP. Do not certify a different script under this packet. Do not create or copy a second script into the repository root merely to satisfy the path check.

## Step 3. Run bounded AGY CLI smoke tests

```powershell
node .\workers\agy-cli-smoke-test.js | Tee-Object .\agy-cli-smoke-result.json
```

Smoke suite v1.1 establishes observed exit behavior for version, successful noninteractive print, invalid flag and bounded timeout. The nominal success probe remains sandboxed and now permits a 90-second AGY print window with a 120-second outer process bound. It must return exit code 0 and response `DCSE_AGY_SMOKE_OK` to pass.

Review the output before worker activation.

## Step 4. Worker prerequisites

The AGY worker follows the existing worker-token/RPC pattern and requires the approved runtime environment variables already used by the control plane:

- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `WORKER_ENROLLMENT_SECRET`
- optional `WORKER_AGENT_ID`
- optional `AGY_EXECUTABLE`
- optional `AGY_MODEL`

Do not paste secret values into GitHub, Tribunal, chat, logs or this packet.

## Step 5. Start AGY worker only after successful smoke-test review

```powershell
node .\workers\agy-cli-operational.js
```

Expected startup behavior is a worker identity check followed by heartbeat and claim polling. Do not use `--dangerously-skip-permissions`.

## Step 6. Certification observation

The live certification is not complete until control-plane evidence shows:

- authorized AG/Antigravity identity
- `agy_windows_cli` heartbeat
- governed task claim
- noninteractive AGY execution
- required discovery artifacts
- artifact hashes
- deterministic validation
- persisted receipt/result
- claim closure/reconciliation

If the worker cannot authenticate, claim, heartbeat or execute, record the exact error and STOP rather than bypassing the control plane.

## Safety

No Supabase remediation, DDL, DML, migrations, deletes, PS access, credential changes or publication are authorized by this packet.
