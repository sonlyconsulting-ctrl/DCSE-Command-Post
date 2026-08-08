# DCSE v7.2 neutral wake probe
#
# Purpose:
#   - Run without launching any model when no work is waiting.
#   - Consume dcse_cp.poller_wake_requests directed to the universal controller.
#   - Mark expired requests EXPIRED.
#   - ACKNOWLEDGE an active wake before starting the controller.
#   - Mark the wake CONSUMED only after Windows Task Scheduler proves the
#     DCSE_Universal_Dispatch_Controller started.
#
# This script must never enable a provider-specific legacy poller.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$ControllerTaskName = 'DCSE_Universal_Dispatch_Controller',
  [string]$TargetRuntime = 'DCSE_Universal_Dispatch_Controller',
  [int]$ControllerStartTimeoutSeconds = 20
)

$ErrorActionPreference = 'Stop'
$LogFile = Join-Path $PSScriptRoot 'dcse_wake_probe.log'

function Write-Log([string]$Message) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')Z  $Message"
  Add-Content -LiteralPath $LogFile -Value $line
}

function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}

function Clone-ObjectToHashtable($Object) {
  $h = @{}
  if ($Object) {
    foreach ($p in $Object.PSObject.Properties) { $h[$p.Name] = $p.Value }
  }
  return $h
}

if (-not (Test-Path -LiteralPath $CredentialFile)) {
  Write-Log "FATAL: credential bundle missing at $CredentialFile"
  exit 2
}

$bundle = Import-Clixml -LiteralPath $CredentialFile
if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') {
  Write-Log 'FATAL: credential bundle points to the wrong Supabase project.'
  exit 3
}

$SupabaseUrl = [string]$bundle.SUPABASE_URL
$ServiceKey = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
if (-not $SupabaseUrl -or -not $ServiceKey) {
  Write-Log 'FATAL: Supabase URL or service key missing from credential bundle.'
  exit 4
}

$ReadHeaders = @{
  apikey = $ServiceKey
  Authorization = "Bearer $ServiceKey"
  'Content-Type' = 'application/json'
  'Accept-Profile' = 'dcse_cp'
}
$WriteHeaders = @{
  apikey = $ServiceKey
  Authorization = "Bearer $ServiceKey"
  'Content-Type' = 'application/json'
  'Content-Profile' = 'dcse_cp'
  Prefer = 'return=minimal'
}
$TableBase = "$SupabaseUrl/rest/v1"

function Patch-Wake([string]$Id, [hashtable]$Fields) {
  $body = $Fields | ConvertTo-Json -Depth 20 -Compress
  Invoke-RestMethod -Method Patch -Uri "$TableBase/poller_wake_requests?id=eq.$Id" -Headers $WriteHeaders -Body $body -TimeoutSec 20 | Out-Null
}

# Retire expired REQUESTED rows first so they cannot block the oldest-first queue.
try {
  $nowIso = [DateTime]::UtcNow.ToString('o')
  $encodedNow = [Uri]::EscapeDataString($nowIso)
  $expired = Invoke-RestMethod -Method Get -Uri "$TableBase/poller_wake_requests?status=eq.REQUESTED&expires_at=lt.$encodedNow&select=id&limit=50" -Headers $ReadHeaders -TimeoutSec 20
  foreach ($row in @($expired)) {
    if ($row.id) {
      Patch-Wake ([string]$row.id) @{ status = 'EXPIRED'; updated_at = [DateTime]::UtcNow.ToString('o') }
      Write-Log "EXPIRED: wake request id=$($row.id)"
    }
  }
} catch {
  Write-Log "WARNING: could not retire expired wake requests: $($_.Exception.Message)"
}

# Select one live wake. If none exists, exit without starting the controller or any model.
try {
  $nowIso = [DateTime]::UtcNow.ToString('o')
  $encodedNow = [Uri]::EscapeDataString($nowIso)
  $target = [Uri]::EscapeDataString($TargetRuntime)
  $wakeRows = Invoke-RestMethod -Method Get -Uri "$TableBase/poller_wake_requests?status=eq.REQUESTED&target_runtime=eq.$target&expires_at=gt.$encodedNow&order=requested_at.asc&limit=1" -Headers $ReadHeaders -TimeoutSec 20
} catch {
  Write-Log "FATAL: wake query failed: $($_.Exception.Message)"
  exit 5
}

if (-not $wakeRows -or @($wakeRows).Count -eq 0) {
  Write-Log 'IDLE: no live wake request. Controller not started.'
  exit 0
}

$wake = @($wakeRows)[0]
$wakeId = [string]$wake.id
$metadata = Clone-ObjectToHashtable $wake.metadata
$metadata['wake_probe_host'] = $env:COMPUTERNAME
$metadata['wake_probe_seen_at'] = [DateTime]::UtcNow.ToString('o')

$task = Get-ScheduledTask -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
if (-not $task) {
  $metadata['wake_probe_error'] = 'universal_controller_task_missing'
  Patch-Wake $wakeId @{
    status = 'FAILED'
    metadata = $metadata
    updated_at = [DateTime]::UtcNow.ToString('o')
  }
  Write-Log "FAILED: $ControllerTaskName is not registered. wake_id=$wakeId"
  exit 6
}

if ($task.State -eq 'Disabled') {
  Enable-ScheduledTask -TaskName $ControllerTaskName | Out-Null
  Write-Log "ENABLE: $ControllerTaskName was disabled and is now enabled."
}

$beforeInfo = Get-ScheduledTaskInfo -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
$beforeLastRun = if ($beforeInfo) { $beforeInfo.LastRunTime } else { [DateTime]::MinValue }

# Contract: acknowledge before controller start.
$ackAt = [DateTime]::UtcNow.ToString('o')
$metadata['wake_probe_ack_at'] = $ackAt
Patch-Wake $wakeId @{
  status = 'ACKNOWLEDGED'
  acknowledged_at = $ackAt
  acknowledged_host = $env:COMPUTERNAME
  metadata = $metadata
  updated_at = $ackAt
}
Write-Log "ACKNOWLEDGED: wake_id=$wakeId target=$TargetRuntime"

try {
  Start-ScheduledTask -TaskName $ControllerTaskName
} catch {
  $metadata['wake_probe_error'] = "controller_start_failed: $($_.Exception.Message)"
  Patch-Wake $wakeId @{
    status = 'FAILED'
    metadata = $metadata
    updated_at = [DateTime]::UtcNow.ToString('o')
  }
  Write-Log "FAILED: Start-ScheduledTask failed for $ControllerTaskName. wake_id=$wakeId error=$($_.Exception.Message)"
  exit 7
}

$deadline = (Get-Date).AddSeconds($ControllerStartTimeoutSeconds)
$verifiedStart = $false
$observedState = $null
$observedLastRun = $beforeLastRun
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 1
  $state = Get-ScheduledTask -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  $info = Get-ScheduledTaskInfo -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  if ($state) { $observedState = $state.State.ToString() }
  if ($info) { $observedLastRun = $info.LastRunTime }
  if (($state -and $state.State -eq 'Running') -or ($info -and $info.LastRunTime -gt $beforeLastRun)) {
    $verifiedStart = $true
    break
  }
}

if (-not $verifiedStart) {
  $metadata['wake_probe_error'] = 'controller_start_not_verified_before_timeout'
  $metadata['controller_observed_state'] = $observedState
  $metadata['controller_last_run_time'] = if ($observedLastRun) { $observedLastRun.ToUniversalTime().ToString('o') } else { $null }
  Patch-Wake $wakeId @{
    status = 'FAILED'
    metadata = $metadata
    updated_at = [DateTime]::UtcNow.ToString('o')
  }
  Write-Log "FAILED: controller start not verified within ${ControllerStartTimeoutSeconds}s. wake_id=$wakeId state=$observedState"
  exit 8
}

$consumedAt = [DateTime]::UtcNow.ToString('o')
$metadata['wake_probe_verified_start'] = $true
$metadata['wake_probe_consumed_at'] = $consumedAt
$metadata['controller_observed_state'] = $observedState
$metadata['controller_last_run_time'] = if ($observedLastRun) { $observedLastRun.ToUniversalTime().ToString('o') } else { $null }
Patch-Wake $wakeId @{
  status = 'CONSUMED'
  consumed_at = $consumedAt
  metadata = $metadata
  updated_at = $consumedAt
}
Write-Log "CONSUMED: wake_id=$wakeId controller_start_verified=true state=$observedState"
exit 0
