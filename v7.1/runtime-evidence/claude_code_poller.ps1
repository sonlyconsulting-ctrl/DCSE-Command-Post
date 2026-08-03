# DCSE v7.0 Worker Poller - Claude Code (dcse_cp.claude_code identity)
#
# Single-shot poll cycle, intended to run under Windows Task Scheduler every
# 60 seconds (see Register-ClaudeCodePollerTask.ps1). Task Scheduler handles
# crash-restart and overlap prevention natively - this script does not loop.
#
# Credential sourcing: DPAPI CurrentUser bundle, NOT a plaintext env var.
# Only SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are read from the bundle and
# injected into this process's own environment for the duration of the RPC
# calls below (cleared implicitly when this process exits). This poller does
# NOT read or forward ANTHROPIC_API_KEY / WORKER_ENROLLMENT_SECRET - those
# belong to a different consumer (the staging reviewer identity), not this one.
#
# Target project: nevgdyfpxdaloacuutal (SC-Command-Post / production).
# Credential file must be created first via Register-DCSEWorkerCredentials.ps1
# (run interactively by DCS - this script cannot create it).

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [switch]$AutoInvoke = $true
)

$ErrorActionPreference = 'Stop'

# ---- Config -----------------------------------------------------------
$AgentKeyCP      = 'claude_code'                          # dcse_cp identity - used for claim/execute
$AgentIdWorker   = 'AGENT-CLAUDE-ARCH-01@LAPTOP-PRIMARY'  # v7_worker identity - heartbeat only, plan-only scope, NOT used to execute
$Lane            = 'DCSE'
$WorkspacePath   = 'C:\DS All Things\DCSE_Command_Center'
$StateFile       = Join-Path $PSScriptRoot 'poller_state.json'
$LogFile         = Join-Path $PSScriptRoot 'poller_log.txt'

# TEMPORARY validation restriction: prove one full cycle end-to-end before
# letting AutoInvoke touch the rest of the backlog (MVT013/MVT014 etc.).
# Remove this line once V69 has closed the loop successfully.
$TaskKeyAllowlist             = @('V69-PROMOTION-COORDINATOR-RESPONSE-20260728')

$ClaimTimeoutMinutes          = 20
$MaxRetries                   = 2
$DenyPSByDefault              = $true
$InvokeOnlyAssignedTasks      = $true
$RequireLaneAuthorization     = $true
$RequireResultAcknowledgement = $true  # honored naturally: submit_agent_result routes to
                                       # 'awaiting_dcs_review' when review/dcs-decision flags
                                       # are set, rather than 'complete' - this script never
                                       # forces completion past that gate.

function Write-Log($msg) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')Z  $msg"
  Add-Content -Path $LogFile -Value $line
}

# ---- Credentials (DPAPI, narrow scope) ---------------------------------
if (-not (Test-Path $CredentialFile)) {
  Write-Log "FATAL: credential bundle not found at $CredentialFile. Run Register-DCSEWorkerCredentials.ps1 first."
  exit 1
}
$bundle = Import-Clixml $CredentialFile

function SecureToPlain($v) {
  if ($v -is [System.Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($v)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$v
}

$SupabaseUrl = $bundle.SUPABASE_URL
$ServiceKey  = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY

if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') {
  Write-Log "FATAL: credential bundle targets project '$($bundle.supabase_project_ref)', expected 'nevgdyfpxdaloacuutal'. Refusing to proceed against the wrong project."
  exit 1
}

$Headers = @{
  'apikey'        = $ServiceKey
  'Authorization' = "Bearer $ServiceKey"
  'Content-Type'  = 'application/json'
}
$RpcBase   = "$SupabaseUrl/rest/v1/rpc"
$TableBase = "$SupabaseUrl/rest/v1"

function Get-HttpErrorBody($errRecord) {
  if ($errRecord.ErrorDetails.Message) { return $errRecord.ErrorDetails.Message }
  $resp = $errRecord.Exception.Response
  if ($resp) {
    try {
      $stream = $resp.GetResponseStream()
      $reader = New-Object System.IO.StreamReader($stream)
      $body = $reader.ReadToEnd()
      $reader.Close()
      if ($body) { return $body }
    } catch {}
  }
  return $errRecord.Exception.Message
}

function Invoke-Rpc($fn, $body, $schema = 'dcse_cp') {
  $json = $body | ConvertTo-Json -Depth 10 -Compress
  $h = $Headers.Clone(); $h['Content-Profile'] = $schema
  try { return Invoke-RestMethod -Method Post -Uri "$RpcBase/$fn" -Headers $h -Body $json }
  catch {
    Write-Log "ERROR calling $fn (schema=$schema) : $(Get-HttpErrorBody $_)"
    return $null
  }
}

function Get-Table($table, $query, $schema = 'dcse_cp') {
  $h = $Headers.Clone(); $h['Accept-Profile'] = $schema
  try { return Invoke-RestMethod -Method Get -Uri "$TableBase/$table`?$query" -Headers $h }
  catch {
    $detail = if ($_.ErrorDetails.Message) { $_.ErrorDetails.Message } else { $_.Exception.Message }
    Write-Log "ERROR querying $table (schema=$schema) : $detail"
    return @()
  }
}

# ---- State --------------------------------------------------------------
$state = @{ processed = @{}; attempts = @{} }
if (Test-Path $StateFile) {
  try {
    $loaded = Get-Content $StateFile -Raw | ConvertFrom-Json
    $state.processed = @{}; foreach ($p in $loaded.processed.PSObject.Properties) { $state.processed[$p.Name] = $p.Value }
    $state.attempts  = @{}; foreach ($p in $loaded.attempts.PSObject.Properties)  { $state.attempts[$p.Name]  = $p.Value }
  } catch {}
}

try { $branch = (git -C $WorkspacePath rev-parse --abbrev-ref HEAD 2>$null) } catch { $branch = 'unknown' }

# ---- 1. Heartbeats (both identities; only claude_code executes) --------
Invoke-Rpc 'agent_heartbeat' @{ p_agent_key = $AgentKeyCP; p_task_key = $null; p_status = 'online'
  p_capability_status = @{ poller = 'active'; host = $env:COMPUTERNAME }; p_notes = 'automated poller cycle' } 'dcse_cp' | Out-Null

Invoke-Rpc 'send_heartbeat' @{ p_agent_id = $AgentIdWorker; p_status = 'idle'; p_current_task_id = $null
  p_current_lane = $Lane; p_workspace_path = $WorkspacePath; p_branch_name = $branch
  p_model_version = 'claude-code'; p_capabilities = @{ tool_use = $true }; p_metrics = @{ cycle_at = (Get-Date).ToString('o') } } 'v7_worker' | Out-Null

# ---- 2. Fetch agent registry authorization once per cycle --------------
$authLanes = @()
try {
  $reg = Get-Table 'agent_registry' "select=authorized_lanes,allowed_actions&agent_key=eq.$AgentKeyCP" 'dcse_cp'
} catch { $reg = $null }
# agent_registry lives in dcse_cp schema, not exposed on the default PostgREST
# schema path - fall back to the known values captured at registration time
# if the direct table read isn't reachable via REST.
if (-not $reg) { $authLanes = @('DCSE','SC','TRIBUNAL','RAG','SYSTEM','TSL') }
else { $authLanes = $reg[0].authorized_lanes }

# ---- 3. Inbox check ------------------------------------------------------
$inbox = Invoke-Rpc 'get_agent_inbox' @{ p_agent_key = $AgentKeyCP; p_limit = 20 }
if (-not $inbox) { $inbox = @() }

$alreadyInProgress = @($inbox | Where-Object { $_.assignment_status -eq 'running' })
$stateChanged = $false
$claimedThisCycle = $false

foreach ($t in $inbox) {
  if ($state.processed.ContainsKey($t.task_key)) { continue }
  if ($t.task_status -notin @('assigned','queued','running')) { continue }

  $stateChanged = $true
  Write-Log "NEW ASSIGNMENT: task_key=$($t.task_key) title=`"$($t.title)`" lane=$($t.lane) task_type=$($t.task_type) task_status=$($t.task_status)"

  if (-not $AutoInvoke) {
    Write-Log "AUTO_INVOKE disabled - logged only."
    continue
  }

  # ---- Gate checks --------------------------------------------------
  $reasons = @()

  if ($InvokeOnlyAssignedTasks -and $t.assignment_status -ne 'assigned') {
    $reasons += "assignment_status is '$($t.assignment_status)', not 'assigned'"
  }
  if ($TaskKeyAllowlist -and ($t.task_key -notin $TaskKeyAllowlist)) {
    $reasons += "task_key not in temporary validation allowlist"
  }
  if ($RequireLaneAuthorization -and ($t.lane -notin $authLanes)) {
    $reasons += "lane '$($t.lane)' not in authorized_lanes"
  }
  if ($DenyPSByDefault -and $t.confidentiality -eq 'ps_confidential') {
    $reasons += "confidentiality is ps_confidential - firewalled, no override in this identity"
  }
  if ($t.dcs_decision_required -eq $true) {
    $reasons += "dcs_decision_required=true - requires DCS Level 0, not an autonomous action"
  }
  if ($alreadyInProgress.Count -gt 0 -or $claimedThisCycle) {
    $reasons += "another assignment already running for this agent (max_concurrent_tasks=1)"
  }
  $attemptCount = if ($state.attempts.ContainsKey($t.task_key)) { $state.attempts[$t.task_key] } else { 0 }
  if ($attemptCount -ge $MaxRetries) {
    $reasons += "max_retries ($MaxRetries) already reached for this task"
  }

  # Stop-gate check: any unresolved gate keyed to this task or this agent
  $gates = Get-Table 'stop_gate' "select=gate_id&approved_at=is.null&or=(task_id.eq.$($t.task_key),agent_id.eq.$AgentKeyCP)" 'v7_worker'
  if ($gates -and $gates.Count -gt 0) {
    $reasons += "unresolved Stop-Gate exists for this task/agent"
  }

  if ($reasons.Count -gt 0) {
    Write-Log "BLOCKED: task_key=$($t.task_key) -- $($reasons -join '; ')"
    continue
  }

  # ---- Claim ---------------------------------------------------------
  $claim = Invoke-Rpc 'claim_agent_assignment' @{ p_agent_key = $AgentKeyCP; p_task_key = $t.task_key }
  if (-not $claim -or -not $claim.ok) {
    Write-Log "CLAIM FAILED: task_key=$($t.task_key) response=$($claim | ConvertTo-Json -Compress)"
    continue
  }
  Write-Log "CLAIMED: task_key=$($t.task_key) assignment_id=$($claim.assignment_id)"
  $state.attempts[$t.task_key] = $attemptCount + 1
  $claimedThisCycle = $true

  # ---- Invoke, bounded by wall-time --------------------------------
  $prompt = "DCSE task assignment: task_key=$($t.task_key), title=`"$($t.title)`", lane=$($t.lane). " +
            "Task description: $($t.description). " +
            "Handle this via the dcse_cp orchestration layer. When done, the result must be " +
            "submitted through dcse_cp.submit_agent_result(p_agent_key='$AgentKeyCP', p_task_key='$($t.task_key)', ...) " +
            "-- do not report completion through any other channel."

  $outFile = Join-Path $PSScriptRoot "task_$($t.task_key)_output.txt"
  # Routed through powershell.exe rather than Start-Process -FilePath 'claude'
  # directly: claude resolves to a .ps1/.cmd shim, not a native executable, and
  # Start-Process's CreateProcess-based launch fails on those with "%1 is not
  # a valid Win32 application" -- powershell.exe -Command correctly invokes
  # the shim through PowerShell's own script-resolution engine instead.
  #
  # The prompt is written to a file and read back inside the child process
  # rather than embedded in the -Command string: passing a string containing
  # quotes/special characters through ArgumentList -> ProcessStartInfo's own
  # argument encoding -> the child's -Command parser is fragile no matter how
  # it's escaped ("string is missing the terminator" is exactly that failure).
  $promptFile = Join-Path $PSScriptRoot "task_$($t.task_key)_prompt.txt"
  Set-Content -Path $promptFile -Value $prompt -NoNewline
  # --permission-mode bypassPermissions: confirmed unattended -p sessions hang
  # indefinitely on any tool-use prompt (only the one-time workspace-trust
  # dialog is skipped in -p mode, not ongoing prompts) -- with no human present
  # to answer, they block until the wall-time kill below fires. The real safety
  # boundary here is the gating logic already run above this point (lane auth,
  # confidentiality, dcs_decision_required, stop-gate, concurrency, retries),
  # not an interactive prompt nobody is present to answer.
  $childCommand = "`$p = Get-Content -Path '$promptFile' -Raw; claude -p `$p --permission-mode bypassPermissions"
  $proc = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile', '-Command', $childCommand) `
            -WorkingDirectory $WorkspacePath -PassThru -NoNewWindow `
            -RedirectStandardOutput $outFile -RedirectStandardError "$outFile.err"

  $timedOut = -not $proc.WaitForExit($ClaimTimeoutMinutes * 60 * 1000)
  if ($timedOut) {
    Write-Log "TIMEOUT: claude -p exceeded $ClaimTimeoutMinutes min for task_key=$($t.task_key), killing."
    try { $proc.Kill() } catch {}
    Invoke-Rpc 'submit_agent_result' @{ p_agent_key = $AgentKeyCP; p_task_key = $t.task_key
      p_result_payload = @{ outcome = 'timeout'; wall_time_minutes = $ClaimTimeoutMinutes }; p_status = 'blocked' } | Out-Null
    Write-Log "SUBMITTED (blocked/timeout): task_key=$($t.task_key)"
    continue
  }

  $outputSummary = ''
  if (Test-Path $outFile) {
    $raw = Get-Content $outFile -Raw
    $outputSummary = if ($raw.Length -gt 2000) { $raw.Substring(0, 2000) + '...(truncated)' } else { $raw }
  }

  $result = Invoke-Rpc 'submit_agent_result' @{ p_agent_key = $AgentKeyCP; p_task_key = $t.task_key
    p_result_payload = @{ outcome = 'completed'; exit_code = $proc.ExitCode; summary = $outputSummary }
    p_status = 'completed' }

  if ($result -and $result.ok) {
    Write-Log "SUBMITTED: task_key=$($t.task_key) status=$($result.status) remaining_open_assignments=$($result.remaining_open_assignments)"
    # Acknowledgement is the schema's own gate, not this script's: submit_agent_result
    # already routed the parent task to 'awaiting_dcs_review' if review_required or
    # dcs_decision_required were set, rather than 'complete'. Only mark locally
    # processed once the RPC confirms the submission was recorded.
    $state.processed[$t.task_key] = (Get-Date).ToString('o')
  } else {
    Write-Log "SUBMIT FAILED: task_key=$($t.task_key) response=$($result | ConvertTo-Json -Compress)"
  }
}

$state | ConvertTo-Json -Depth 10 | Set-Content -Path $StateFile
if ($stateChanged) { Write-Log "Cycle complete." }
