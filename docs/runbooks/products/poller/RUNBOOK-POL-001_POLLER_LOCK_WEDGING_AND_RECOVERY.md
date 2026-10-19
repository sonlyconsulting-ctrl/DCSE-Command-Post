# RUNBOOK-POL-001: Poller Mutex Lock Contention & Orphan Worker Recovery

**Classification:** OPERATIONAL RUNBOOK · HIGH PRIORITY  
**Governing Standard:** DCSE Master Profile v7.3 // DCS-DIR-20260916-001  
**Historical Incident Record:** `_Tribunal_Inbox/DCSE-CP-POLLER-RUNTIME-RECOVERY-20260917-H01_EVIDENCE.md`  
**Primary Surface:** Windows Task Scheduler (`LAPTOP-74UF76GB`), PowerShell 7+, Supabase `dcse_cp` schema  
**Conformity Target:** 98%+ Operator Success Rate  

---

## 1. Problem Statement & Error Signature

When agent workers (`antigravity`, `claude_code`, or `codex`) poll the Supabase control plane for assignments, an ungraceful shutdown, hung network socket, or unhandled exception can leave an OS mutex or database advisory lock held indefinitely.

### Observable Symptoms:
1. **Worker Log Flood:**  
   `worker_antigravity.log` repeatedly logs 60+ entries per hour:
   ```text
   SKIP ... task lock held by mutex DCSE_AgentMessages_antigravity
   ```
2. **Control Plane Stagnation:**  
   Tasks in `dcse_cp.agent_tasks` remain in `assigned` or `running` status with zero progress updates, while heartbeats go silent (>10 minutes).
3. **Ghost Writer Heartbeats:**  
   Legacy or duplicate scheduled tasks continue sending unauthorized heartbeats from untracked background processes (`claude_code:unspecified-host`).

---

## 2. Instant Diagnostic Command (CLI)

Run this command in PowerShell 7+ on the host (`LAPTOP-74UF76GB`) to inspect running poller processes and scheduled tasks:

```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "dcse_agent_worker|claude_code_poller|dcse_dispatch" } | Select-Object ProcessId, Name, CreationDate, CommandLine | Format-Table -AutoSize
Get-ScheduledTask -TaskName "DCSE_*" | Select-Object TaskName, State, LastTaskResult | Format-Table -AutoSize
```

### Expected Output:
- **HEALTHY:** Single `DCSE_DispatchController` process running, tasks show `Ready` or `Running` with `LastTaskResult = 0`.
- **WEDGED:** A worker process older than 30 minutes with identical `ProcessId` persisting across dispatch cycles.

---

## 3. Remediation & Recovery Procedure

### Step 1: Kill Wedged Worker Processes (CLI)
Terminate any hanging agent worker processes without killing the dispatch controller:

```powershell
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "dcse_agent_worker.ps1" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force; Write-Host "Terminated wedged worker PID: $($_.ProcessId)" }
```

### Step 2: Clear Stale Host Mutexes & Reset Locks (CLI)
Force release the local OS synchronization mutexes:

```powershell
[System.Threading.Mutex]::OpenExisting("Global\DCSE_AgentMessages_antigravity").Close() 2>$null
[System.Threading.Mutex]::OpenExisting("Global\DCSE_AgentMessages_codex").Close() 2>$null
```

### Step 3: Reconcile Task State in Supabase Control Plane
If a task was left stranded in `running` state by a killed process, submit a truthful status update via the control plane API or run the recovery SQL script:

```sql
UPDATE dcse_cp.agent_tasks
SET status = 'awaiting_dcs',
    result_payload = jsonb_build_object('error', 'POL_LOCK_TIMEOUT', 'recovered_by', 'RUNBOOK-POL-001', 'timestamp', NOW())
WHERE status = 'running' 
  AND updated_at < NOW() - INTERVAL '30 minutes';
```

---

## 4. Verification Gate

Verify that the dispatch cycle cleanly resumes and executes preflight without skipping:

```powershell
powershell.exe -ExecutionPolicy Bypass -File "v7.0\09_WORKERS\dcse_dispatch_controller.ps1" -RunOnce
Get-Content "v7.0\09_WORKERS\dispatch_controller.log" -Tail 10
```

### Success Signature:
```text
PREFLIGHT_PASS: All agent channels cleared. Mutex released. Dispatch cycle completed in <1.2s.
```

---

## 5. Permanent Prevention Standard
1. **Separate Message & Task Locks:** Never combine message ACK queues with heavy execution task locks (enforced in C1 update).
2. **Heartbeat Auto-Retirement:** Any unregistered worker identity pinging the control plane is automatically assigned `retired_writer` status by `dcse_cp.agent_heartbeat(...)`.
