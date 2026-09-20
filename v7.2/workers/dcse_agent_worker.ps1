# DCSE v7.2 Runtime Worker
#
# One short-lived worker process for one logical agent identity. The neutral
# controller starts these independently so Claude/Qwen/Codex do not serialize
# the entire queue behind one provider process.
#
# Safety boundary:
# - controller/worker owns Supabase credentials, claims, heartbeats, results
# - child AI CLI receives only the task prompt and workspace, not the service key
# - one named mutex per agent_key => default concurrency 1 per logical worker
# - claims remain atomic in dcse_cp.claim_agent_assignment
# - PS-confidential and dcs_decision_required work fail closed
# - raw child output is evidence; submit_agent_result is called by this worker

[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][string]$AgentKey,
  [Parameter(Mandatory=$true)][string]$RuntimeSurface,
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$WorkspacePath = 'C:\DS All Things\DCSE_Command_Center',
  [string]$WorkerRoot = 'C:\DS All Things\DCSE_Command_Center\v7.2\workers',
  [int]$MaxWallMinutes = 20,
  [switch]$PreflightOnly,
  [switch]$AdmissionSmoke,
  [switch]$MessagesOnly
)

$ErrorActionPreference = 'Stop'
$HostName = $env:COMPUTERNAME
$RuntimeInstance = "$RuntimeSurface@$HostName"
$SessionId = [guid]::NewGuid().ToString()
$SafeAgent = ($AgentKey -replace '[^A-Za-z0-9_-]','_')
$LogFile = Join-Path $WorkerRoot "worker_$SafeAgent.log"
$OutputDir = Join-Path $WorkerRoot 'task_output'
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

function Write-Log([string]$Message) {
  $line = "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fffK')  agent=$AgentKey runtime=$RuntimeInstance  $Message"
  for ($i = 0; $i -lt 5; $i++) {
    try {
      Add-Content -LiteralPath $LogFile -Value $line -ErrorAction Stop
      return
    } catch {
      Start-Sleep -Milliseconds 50
    }
  }
}

function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}

function Escape-SingleQuoted([string]$Value) {
  return $Value.Replace("'","''")
}

function Test-StrictTrue($Value) {
  if ($Value -is [bool]) { return $Value }
  if ($null -eq $Value) { return $false }
  $text = ([string]$Value).Trim().ToLowerInvariant()
  return ($text -eq 'true' -or $text -eq 't' -or $text -eq '1')
}

function Copy-Capabilities([hashtable]$Base, [bool]$CanClaim) {
  $copy = @{}
  foreach ($key in $Base.Keys) { $copy[$key] = $Base[$key] }
  $copy['can_claim'] = $CanClaim
  return $copy
}

function Get-HttpErrorBody($ErrorRecord) {
  if ($ErrorRecord.ErrorDetails -and $ErrorRecord.ErrorDetails.Message) { return $ErrorRecord.ErrorDetails.Message }
  if ($ErrorRecord.Exception -and $ErrorRecord.Exception.Response) {
    try {
      $stream = $ErrorRecord.Exception.Response.GetResponseStream()
      $reader = New-Object IO.StreamReader($stream)
      $body = $reader.ReadToEnd(); $reader.Close()
      if ($body) { return $body }
    } catch {}
  }
  return $ErrorRecord.Exception.Message
}

if (-not (Test-Path -LiteralPath $CredentialFile)) { throw "Credential bundle not found: $CredentialFile" }
$bundle = Import-Clixml $CredentialFile
if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') {
  throw "Credential bundle targets wrong project: $($bundle.supabase_project_ref)"
}
$SupabaseUrl = [string]$bundle.SUPABASE_URL
$ServiceKey = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
$Headers = @{
  apikey = $ServiceKey
  Authorization = "Bearer $ServiceKey"
  'Content-Type' = 'application/json'
}
$RpcBase = "$SupabaseUrl/rest/v1/rpc"
$TableBase = "$SupabaseUrl/rest/v1"

function Invoke-Rpc([string]$Name, [hashtable]$Body) {
  $h = $Headers.Clone(); $h['Content-Profile'] = 'dcse_cp'
  try {
    $res = Invoke-RestMethod -Method Post -Uri "$RpcBase/$Name" -Headers $h -Body ($Body | ConvertTo-Json -Depth 20 -Compress) -TimeoutSec 30
    if ($res -is [array]) { return $res }
    elseif ($null -ne $res -and $null -ne $res.value -and $res.value -is [array]) { return $res.value }
    return $res
  } catch {
    Write-Log "RPC_ERROR name=$Name detail=$(Get-HttpErrorBody $_)"
    return $null
  }
}

function Get-Table([string]$Table, [string]$Query) {
  $h = $Headers.Clone(); $h['Accept-Profile'] = 'dcse_cp'
  try {
    $res = Invoke-RestMethod -Method Get -Uri "$TableBase/$Table`?$Query" -Headers $h -TimeoutSec 30
    if ($res -is [array]) { return @($res) }
    elseif ($null -ne $res -and $null -ne $res.value -and $res.value -is [array]) { return @($res.value) }
    return @($res)
  } catch {
    Write-Log "TABLE_ERROR table=$Table detail=$(Get-HttpErrorBody $_)"
    return @()
  }
}

function Send-Heartbeat([string]$Status, $TaskKey, [hashtable]$Capabilities, [string]$Notes) {
  $body = @{
    p_agent_key = $AgentKey
    p_task_key = $TaskKey
    p_status = $Status
    p_capability_status = $Capabilities
    p_notes = $Notes
    p_runtime_surface = $RuntimeSurface
    p_runtime_instance = $RuntimeInstance
    p_host = $HostName
    p_session_id = $SessionId
  }
  return Invoke-Rpc 'agent_heartbeat' $body
}

function Get-Admission() {
  $rows = Get-Table 'autonomous_dispatch_admission' "agent_key=eq.$AgentKey&select=*"
  if ($rows.Count -eq 0) { return $null }
  return $rows[0]
}

function Test-ServerAdmitted() {
  $rows = Get-Table 'autonomous_dispatch_admission' "agent_key=eq.$AgentKey&select=agent_key,admitted_for_autonomous_claim"
  if ($rows.Count -eq 0) {
    Write-Log "ADMISSION_DEBUG rows=0"
    return $false
  }
  $flag = $rows[0].admitted_for_autonomous_claim
  $admitted = $false
  if ($flag -is [bool]) {
    $admitted = $flag
  }
  elseif ($null -ne $flag) {
    $admitted = ([string]$flag).Trim().ToLowerInvariant() -in @('true','t','1','yes')
  }
  Write-Log "ADMISSION_DEBUG rows=$($rows.Count) flag=$flag admitted=$admitted"
  return $admitted
}

function Get-CliInfo() {
  $commandName = switch ($AgentKey) {
    'claude_code' { 'claude' }
    'qwen_windows_cli' { 'qwen' }
    'codex' { 'codex' }
    'antigravity' { 'agy' }
    default { throw "No runtime adapter registered for agent_key=$AgentKey" }
  }
  $cmd = Get-Command $commandName -ErrorAction Stop
  $path = if ($cmd.Source) { $cmd.Source } else { $cmd.Path }
  $version = ''
  try { $version = ((& $path --version 2>&1) | Out-String).Trim() } catch { $version = "version_probe_failed: $($_.Exception.Message)" }
  return @{ command = $commandName; path = $path; version = $version }
}

function Get-QwenSandboxProvider() {
  foreach ($name in @('docker','podman')) {
    $cmd = Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) { continue }
    if ($name -eq 'docker' -and -not [System.IO.File]::Exists('\\.\pipe\docker_engine')) { continue }
    try {
      $p = Start-Process -FilePath $cmd.Source -ArgumentList 'info' -NoNewWindow -PassThru -RedirectStandardOutput $null -RedirectStandardError $null
      if (-not $p.WaitForExit(3000)) {
        try { Stop-Process -Id $p.Id -Force } catch {}
        continue
      }
      if ($p.ExitCode -eq 0) { return $name }
    } catch {}
  }
  return $null
}

function Test-StopGate($Task) {
  $taskKeyEsc = [uri]::EscapeDataString([string]$Task.task_key)
  $agentEsc = [uri]::EscapeDataString($AgentKey)
  $rows = Get-Table 'active_stop_gates' "select=gate_id,task_id,agent_id,gate_type,description&or=(task_id.eq.$taskKeyEsc,agent_id.eq.$agentEsc)"
  return ($rows.Count -gt 0)
}

function Get-ExpectedArtifactEvidence($Task) {
  $refs = $Task.input_refs
  if (-not $refs) { return $null }
  $relative = $null
  try { $relative = [string]$refs.expected_artifact } catch {}
  if (-not $relative) { return $null }
  $full = Join-Path $WorkspacePath $relative
  if (-not (Test-Path -LiteralPath $full)) {
    return @{ expected_artifact=$relative; exists=$false }
  }
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $full).Hash.ToLowerInvariant()
  return @{ expected_artifact=$relative; exists=$true; sha256=$hash; full_path=$full }
}

function Restore-StaleRunningAssignments($Inbox, [hashtable]$BaseCapabilities) {
  $cutoff = (Get-Date).ToUniversalTime().AddMinutes(-1 * ($MaxWallMinutes + 5))
  foreach ($running in @($Inbox | Where-Object { $_.assignment_status -eq 'running' })) {
    $updated = $null
    try { $updated = [datetimeoffset]::Parse([string]$running.updated_at) } catch { continue }
    if ($updated.UtcDateTime -gt $cutoff) { continue }

    $taskIdEsc = [uri]::EscapeDataString([string]$running.task_id)
    $freshCutoff = [uri]::EscapeDataString((Get-Date).ToUniversalTime().AddMinutes(-3).ToString('o'))
    $fresh = Get-Table 'agent_heartbeats' "select=id&task_id=eq.$taskIdEsc&last_seen_at=gte.$freshCutoff"
    if ($fresh.Count -gt 0) { continue }

    $payload = @{
      outcome='orphaned_assignment_recovered'
      prior_assignment_status='running'
      stale_since=[string]$running.updated_at
      recovery_runtime_surface=$RuntimeSurface
      recovery_runtime_instance=$RuntimeInstance
    }
    $result = Invoke-Rpc 'submit_agent_result' @{
      p_agent_key=$AgentKey; p_task_key=$running.task_key; p_result_payload=$payload; p_status='blocked';
      p_runtime_surface=$RuntimeSurface; p_runtime_instance=$RuntimeInstance; p_host=$HostName; p_session_id=$SessionId
    }
    if ($result -and $result.ok) {
      Write-Log "RECOVERED_ORPHAN task=$($running.task_key)"
      Send-Heartbeat 'online' $null (Copy-Capabilities $BaseCapabilities $false) "orphaned assignment recovered: $($running.task_key)" | Out-Null
    } else {
      Write-Log "ORPHAN_RECOVERY_FAILED task=$($running.task_key)"
    }
  }
}


# --- DCSE message bus (DCS-DIR-20260916-001) ---------------------------------
# Delivery contract: lease -> write to agent inbox file -> hash -> ack with
# receipt. Any failure NACKs so the server requeues or dead-letters. The
# message pump never executes work; execution_authorized is always false.
function Invoke-MessagePump() {
  $inboxDir = Join-Path $WorkerRoot (Join-Path 'agent_inbox' $SafeAgent)
  New-Item -ItemType Directory -Force -Path $inboxDir | Out-Null
  $msgs = @(Invoke-Rpc 'claim_agent_messages' @{ p_agent_key=$AgentKey; p_runtime_instance=$RuntimeInstance; p_lease_seconds=300; p_limit=20 })
  $delivered = 0
  $cliVersion = $null
  foreach ($m in $msgs) {
    if (-not $m -or -not $m.id) { continue }
    try {
      $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ')
      $file = Join-Path $inboxDir ("{0}_{1}.json" -f $stamp, $m.id)
      $record = [ordered]@{
        message_id = $m.id; correlation_id = $m.correlation_id; reply_to = $m.reply_to
        sender = $m.sender; recipient_agent_key = $m.recipient_agent_key
        subject = $m.subject; body = $m.body; message_class = $m.message_class
        lane = $m.lane; execution_authorized = $false; dcs_decision_ref = $m.dcs_decision_ref
        expires_at = $m.expires_at; delivered_at = (Get-Date).ToUniversalTime().ToString('o')
        how_to_reply = "scripts\dcse_msg.ps1 -Reply $($m.id) -From $AgentKey -Body '<text>'"
      }
      $record | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $file -Encoding UTF8
      $sha = (Get-FileHash -Algorithm SHA256 -LiteralPath $file).Hash.ToLowerInvariant()
      if ($null -eq $cliVersion) {
        try { $cliVersion = (Get-CliInfo).version } catch { $cliVersion = "unavailable: $($_.Exception.Message)" }
      }
      $receipt = @{
        receipt_type = 'worker_delivery_receipt'
        agent_key = $AgentKey; runtime_surface = $RuntimeSurface; runtime_instance = $RuntimeInstance
        host = $HostName; session_id = $SessionId; cli_version = $cliVersion
        delivered_file = $file; delivered_sha256 = $sha
        execution_performed = $false
        note = 'Delivered to agent inbox by trusted worker wrapper. Agent content replies arrive as reply messages.'
      }
      $ack = Invoke-Rpc 'ack_agent_message' @{ p_message_id=$m.id; p_agent_key=$AgentKey; p_runtime_instance=$RuntimeInstance; p_receipt=$receipt }
      if ($ack -and $ack.ok) { $delivered++; Write-Log "MESSAGE_ACKED id=$($m.id) sha256=$sha" }
      else { Write-Log "MESSAGE_ACK_FAILED id=$($m.id) response=$($ack | ConvertTo-Json -Compress)" }
    } catch {
      Write-Log "MESSAGE_DELIVERY_FAILED id=$($m.id) error=$($_.Exception.Message)"
      Invoke-Rpc 'nack_agent_message' @{ p_message_id=$m.id; p_agent_key=$AgentKey; p_runtime_instance=$RuntimeInstance; p_reason=[string]$_.Exception.Message } | Out-Null
    }
  }
  return $delivered
}

# Message delivery runs under its OWN lock, before the task lock, so a long or
# hung task on this agent can never block governed communication.
$msgMutex = New-Object Threading.Mutex($false, "Local\DCSE_AgentMessages_$SafeAgent")
$msgLock = $false
try {
  $msgLock = $msgMutex.WaitOne(0)
  if ($msgLock) {
    $deliveredCount = Invoke-MessagePump
    if ($deliveredCount -gt 0) {
      Send-Heartbeat 'online' $null @{ poller='message_pump'; can_claim=$false; host=$HostName } "delivered $deliveredCount message(s) via dcse_cp.agent_messages" | Out-Null
    }
    if ($MessagesOnly) { Write-Log "MESSAGES_ONLY delivered=$deliveredCount" }
  }
} catch {
  Write-Log "MESSAGE_PUMP_ERROR $($_.Exception.Message)"
} finally {
  if ($msgLock) { try { $msgMutex.ReleaseMutex() } catch {} }
  $msgMutex.Dispose()
}
if ($MessagesOnly) { exit 0 }

$mutexName = "Local\DCSE_AgentWorker_$SafeAgent"
$mutex = New-Object Threading.Mutex($false,$mutexName)
$lockHeld = $false
try {
  $lockHeld = $mutex.WaitOne(0)
  if (-not $lockHeld) {
    Write-Log 'SKIP another worker process already owns this agent mutex'
    exit 0
  }

  $cli = $null
  try { $cli = Get-CliInfo }
  catch {
    Send-Heartbeat 'blocked' $null @{ poller='preflight'; can_claim=$false; cli_available=$false } "CLI preflight failed: $($_.Exception.Message)" | Out-Null
    Write-Log "PREFLIGHT_FAILED $($_.Exception.Message)"
    exit 2
  }

  $sandboxProvider = $null
  if ($AgentKey -eq 'qwen_windows_cli') {
    $sandboxProvider = Get-QwenSandboxProvider
    if (-not $sandboxProvider) {
      Send-Heartbeat 'blocked' $null @{ poller='preflight'; can_claim=$false; cli_available=$true; cli_version=$cli.version; sandbox_provider=$null } 'Qwen CLI found but Docker/Podman sandbox provider is unavailable or not running.' | Out-Null
      Write-Log 'PREFLIGHT_FAILED qwen sandbox provider unavailable'
      exit 3
    }
  }

  if ($AgentKey -eq 'codex') {
    try {
      $help = ((& $cli.path exec --help 2>&1) | Out-String)
      if ($help -notmatch 'workspace-write') { throw 'codex exec help does not advertise workspace-write sandbox' }
      if ($help -notmatch '--ephemeral') { throw 'codex exec help does not advertise ephemeral mode' }
      if ($help -notmatch '(?m)-c|--config') { throw 'codex exec help does not advertise config overrides required for approval_policy=never' }
    } catch {
      Send-Heartbeat 'blocked' $null @{ poller='preflight'; can_claim=$false; cli_available=$true; cli_version=$cli.version } "Codex noninteractive/sandbox preflight failed: $($_.Exception.Message)" | Out-Null
      Write-Log "PREFLIGHT_FAILED codex $($_.Exception.Message)"
      exit 4
    }
  }

  $admission = Get-Admission
  if (-not $admission) {
    Send-Heartbeat 'blocked' $null @{ poller='preflight'; can_claim=$false; cli_version=$cli.version } 'No dispatch admission row exists.' | Out-Null
    exit 5
  }

  $isAdmitted = Test-ServerAdmitted
  $cap = @{ poller = if ($PreflightOnly -or (-not $isAdmitted)) { 'preflight' } else { 'active' }; can_claim=$isAdmitted; cli_version=$cli.version; host=$HostName }
  if ($sandboxProvider) { $cap.sandbox_provider = $sandboxProvider }

  if ($PreflightOnly -and -not $AdmissionSmoke) {
    Send-Heartbeat 'online' $null $cap 'runtime preflight successful; claim disabled' | Out-Null
    Write-Log "PREFLIGHT_PASS cli=$($cli.path) version=$($cli.version) sandbox=$sandboxProvider"
    exit 0
  }

  $inbox = @(Invoke-Rpc 'get_agent_inbox' @{ p_agent_key=$AgentKey; p_limit=20 })
  Restore-StaleRunningAssignments $inbox $cap
  $inbox = @(Invoke-Rpc 'get_agent_inbox' @{ p_agent_key=$AgentKey; p_limit=20 })

  if ($inbox.Count -eq 0) {
    Send-Heartbeat 'idle' $null $cap 'no assigned work' | Out-Null
    Write-Log 'IDLE no inbox assignments'
    exit 0
  }

  $candidates = @($inbox | Where-Object { $_.assignment_status -eq 'assigned' -and $_.task_status -in @('assigned','queued') })
  if (-not $isAdmitted) {
    if (-not $AdmissionSmoke) {
      Send-Heartbeat 'online' $null $cap 'runtime preflight successful; autonomous claim not admitted' | Out-Null
      Write-Log 'NOT_ADMITTED no claim attempted'
      exit 0
    }
    $candidates = @($candidates | Where-Object { Test-StrictTrue $_.policy_flags.runtime_admission_smoke })
  }

  if ($candidates.Count -eq 0) {
    Send-Heartbeat 'idle' $null $cap 'no eligible assignments' | Out-Null
    Write-Log 'IDLE no eligible assignments'
    exit 0
  }

  $task = $candidates | Sort-Object priority,created_at | Select-Object -First 1

  $reasons = @()
  if ($task.confidentiality -eq 'ps_confidential') { $reasons += 'PS confidentiality firewall' }
  if (Test-StrictTrue $task.dcs_decision_required) { $reasons += 'dcs_decision_required=true' }
  if ($admission.authorized_lanes -and ($task.lane -notin @($admission.authorized_lanes))) { $reasons += "lane '$($task.lane)' not authorized" }
  if (Test-StopGate $task) { $reasons += 'unresolved stop-gate' }
  if ($reasons.Count -gt 0) {
    Send-Heartbeat 'blocked' $task.task_key (Copy-Capabilities $cap $false) ($reasons -join '; ') | Out-Null
    Write-Log "BLOCKED task=$($task.task_key) reasons=$($reasons -join '; ')"
    exit 6
  }

  $claim = Invoke-Rpc 'claim_agent_assignment' @{
    p_agent_key=$AgentKey
    p_task_key=$task.task_key
    p_runtime_surface=$RuntimeSurface
    p_runtime_instance=$RuntimeInstance
    p_host=$HostName
    p_session_id=$SessionId
  }
  if (-not $claim -or -not $claim.ok) {
    Write-Log "CLAIM_FAILED task=$($task.task_key) response=$($claim | ConvertTo-Json -Compress)"
    exit 0
  }

  Write-Log "CLAIMED task=$($task.task_key) assignment=$($claim.assignment_id)"
  Send-Heartbeat 'working' $task.task_key (Copy-Capabilities $cap $true) 'worker executing claimed assignment' | Out-Null

  $prompt = @"
DCSE v7.2 task assignment.
Logical agent: $AgentKey
Task key: $($task.task_key)
Title: $($task.title)
Lane: $($task.lane)
Description:
$($task.description)

Execution contract:
- Work only inside the configured workspace unless the task explicitly authorizes otherwise.
- Do not access PS-confidential material.
- Do not request, print, log, or transmit Supabase/service/API credentials.
- Do not call dcse_cp claim/heartbeat/result RPCs yourself; the trusted worker wrapper owns control-plane state.
- Complete the bounded task, verify what you changed, and return a concise final report with artifacts/tests/known gaps.
- Do not claim success for unverified work.
"@

  $promptFile = Join-Path $OutputDir "$($task.task_key)_$SafeAgent.prompt.txt"
  $outFile = Join-Path $OutputDir "$($task.task_key)_$SafeAgent.stdout.txt"
  $errFile = Join-Path $OutputDir "$($task.task_key)_$SafeAgent.stderr.txt"
  Set-Content -LiteralPath $promptFile -Value $prompt -Encoding UTF8

  $cmdEsc = Escape-SingleQuoted $cli.path
  $promptEsc = Escape-SingleQuoted $promptFile
  $workspaceEsc = Escape-SingleQuoted $WorkspacePath

  switch ($AgentKey) {
    'claude_code' {
      $childScript = "`$p=Get-Content -LiteralPath '$promptEsc' -Raw; & '$cmdEsc' -p `$p --permission-mode bypassPermissions"
    }
    'qwen_windows_cli' {
      $childScript = "`$p=Get-Content -LiteralPath '$promptEsc' -Raw; & '$cmdEsc' -p `$p --output-format json --approval-mode auto --sandbox=$sandboxProvider --max-wall-time $($MaxWallMinutes)m"
    }
    'codex' {
      # Codex 0.145.x exposes approval policy through config overrides in exec.
      $childScript = "`$p=Get-Content -LiteralPath '$promptEsc' -Raw; & '$cmdEsc' exec --ephemeral --sandbox workspace-write -c 'approval_policy=`"never`"' -C '$workspaceEsc' `$p"
    }
    'antigravity' {
      # DCS-DIR-20260916-001: permission bypass only when the task explicitly
      # declares workspace-write; otherwise fail closed.
      if ([string]$task.policy_flags.sandbox -ne 'workspace-write') {
        Invoke-Rpc 'submit_agent_result' @{
          p_agent_key=$AgentKey; p_task_key=$task.task_key; p_result_payload=@{ outcome='blocked_unenforceable_sandbox'; detail='agy cannot enforce read-only; task must declare policy_flags.sandbox=workspace-write' }; p_status='blocked';
          p_runtime_surface=$RuntimeSurface; p_runtime_instance=$RuntimeInstance; p_host=$HostName; p_session_id=$SessionId
        } | Out-Null
        Write-Log "BLOCKED task=$($task.task_key) reason=agy read-only sandbox unenforceable"
        exit 9
      }
      $childScript = "`$p=Get-Content -LiteralPath '$promptEsc' -Raw; & '$cmdEsc' --prompt `$p --dangerously-skip-permissions"
    }
  }

  $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($childScript))
  $proc = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-EncodedCommand',$encoded) -WorkingDirectory $WorkspacePath -PassThru -NoNewWindow -RedirectStandardOutput $outFile -RedirectStandardError $errFile
  $deadline = (Get-Date).AddMinutes($MaxWallMinutes)
  $nextHeartbeat = (Get-Date).AddSeconds(45)
  $timedOut = $false
  while (-not $proc.HasExited) {
    if ((Get-Date) -ge $deadline) { $timedOut=$true; break }
    if ((Get-Date) -ge $nextHeartbeat) {
      Send-Heartbeat 'working' $task.task_key (Copy-Capabilities $cap $true) 'worker child process active' | Out-Null
      $nextHeartbeat = (Get-Date).AddSeconds(45)
    }
    Start-Sleep -Seconds 3
    $proc.Refresh()
  }

  if ($timedOut) {
    try { Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue } catch {}
    $resultPayload = @{ outcome='timeout'; wall_time_minutes=$MaxWallMinutes; runtime_surface=$RuntimeSurface; runtime_instance=$RuntimeInstance; stdout_path=$outFile; stderr_path=$errFile }
    Invoke-Rpc 'submit_agent_result' @{
      p_agent_key=$AgentKey; p_task_key=$task.task_key; p_result_payload=$resultPayload; p_status='blocked';
      p_runtime_surface=$RuntimeSurface; p_runtime_instance=$RuntimeInstance; p_host=$HostName; p_session_id=$SessionId
    } | Out-Null
    Write-Log "TIMEOUT task=$($task.task_key)"
    exit 7
  }

  $proc.WaitForExit()
  $stdout = if (Test-Path -LiteralPath $outFile) { Get-Content -LiteralPath $outFile -Raw } else { '' }
  $stderr = if (Test-Path -LiteralPath $errFile) { Get-Content -LiteralPath $errFile -Raw } else { '' }
  $summary = $stdout
  if ($summary.Length -gt 6000) { $summary = $summary.Substring(0,6000) + '...(truncated; full stdout retained on host)' }
  $artifactEvidence = Get-ExpectedArtifactEvidence $task

  $status = if ($proc.ExitCode -eq 0) { 'completed' } else { 'blocked' }
  if ($artifactEvidence -and -not (Test-StrictTrue $artifactEvidence.exists)) { $status='blocked' }
  $resultPayload = @{
    outcome = if ($status -eq 'completed') { 'completed' } else { 'runtime_failed_or_unverified' }
    exit_code = $proc.ExitCode
    summary = $summary
    stderr = if ($stderr.Length -gt 2000) { $stderr.Substring(0,2000) + '...(truncated)' } else { $stderr }
    runtime_surface = $RuntimeSurface
    runtime_instance = $RuntimeInstance
    runtime_command = $cli.command
    runtime_version = $cli.version
    stdout_path = $outFile
    stderr_path = $errFile
    artifact_evidence = $artifactEvidence
  }
  if ($sandboxProvider) { $resultPayload.sandbox_provider=$sandboxProvider }

  $submitted = Invoke-Rpc 'submit_agent_result' @{
    p_agent_key=$AgentKey; p_task_key=$task.task_key; p_result_payload=$resultPayload; p_status=$status;
    p_runtime_surface=$RuntimeSurface; p_runtime_instance=$RuntimeInstance; p_host=$HostName; p_session_id=$SessionId
  }
  if (-not $submitted -or -not $submitted.ok) {
    Write-Log "SUBMIT_FAILED task=$($task.task_key)"
    exit 8
  }

  Write-Log "SUBMITTED task=$($task.task_key) status=$status exit=$($proc.ExitCode)"
  exit 0
}
finally {
  if ($lockHeld) { try { $mutex.ReleaseMutex() } catch {} }
  $mutex.Dispose()
}

