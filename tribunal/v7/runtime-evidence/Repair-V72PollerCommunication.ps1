# DCSE v7.2 bounded poller communication recovery
#
# Goal: restore the neutral universal controller and wake path without
# re-enabling provider-specific legacy pollers.
#
# This script is intentionally host-local because Windows Task Scheduler and
# DPAPI credentials cannot be manipulated from cloud-only control surfaces.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$InstallRoot = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS',
  [string]$WorkspacePath = 'C:\DS All Things\DCSE_Command_Center',
  [string]$ControllerTaskName = 'DCSE_Universal_Dispatch_Controller',
  [string]$WakeProbeTaskName = 'DCSE_Universal_Dispatch_WakeProbe',
  [string]$LegacyPollerTaskName = 'DCSE_ClaudeCode_Poller',
  [string]$LegacyMonitorTaskName = 'DCSE_PollerHealthMonitor'
)

$ErrorActionPreference = 'Stop'
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$ReceiptPath = Join-Path $InstallRoot "V7_2_POLLER_COMMUNICATION_RECOVERY_$Timestamp.json"

function Stage([string]$Message) { Write-Host "[V7.2 COMM] $Message" }

function Parse-OrThrow([string]$Path) {
  $tokens = $null
  $errors = $null
  [Management.Automation.Language.Parser]::ParseFile($Path, [ref]$tokens, [ref]$errors) | Out-Null
  if ($errors -and $errors.Count -gt 0) {
    throw "PowerShell parse failed for $Path : $($errors | ForEach-Object { $_.Message } | Out-String)"
  }
}

function Backup-And-Copy([string]$Source, [string]$Destination) {
  if (-not (Test-Path -LiteralPath $Source)) { throw "Source missing: $Source" }
  Parse-OrThrow $Source
  if (Test-Path -LiteralPath $Destination) {
    Copy-Item -LiteralPath $Destination -Destination "$Destination.pre_v72_comm_$Timestamp.bak" -Force
  }
  Copy-Item -LiteralPath $Source -Destination $Destination -Force
}

if (-not (Test-Path -LiteralPath $CredentialFile)) { throw "Credential bundle missing: $CredentialFile" }
if (-not (Test-Path -LiteralPath $InstallRoot)) { throw "Install root missing: $InstallRoot" }

$SourceRoot = $PSScriptRoot
$SourceController = Join-Path $SourceRoot 'dcse_dispatch_controller.ps1'
$SourceWorker = Join-Path $SourceRoot 'dcse_agent_worker.ps1'
$SourceWakeProbe = Join-Path $SourceRoot 'dcse_wake_probe.ps1'
$ControllerPath = Join-Path $InstallRoot 'dcse_dispatch_controller.ps1'
$WorkerPath = Join-Path $InstallRoot 'dcse_agent_worker.ps1'
$WakeProbePath = Join-Path $InstallRoot 'dcse_wake_probe.ps1'

Stage 'Validating and installing current neutral controller, worker, and wake probe with backups.'
Backup-And-Copy $SourceController $ControllerPath
Backup-And-Copy $SourceWorker $WorkerPath
Backup-And-Copy $SourceWakeProbe $WakeProbePath
Parse-OrThrow $ControllerPath
Parse-OrThrow $WorkerPath
Parse-OrThrow $WakeProbePath

# Preserve rollback artifacts but keep provider-specific schedulers disabled.
foreach ($legacyName in @($LegacyPollerTaskName, $LegacyMonitorTaskName)) {
  $legacy = Get-ScheduledTask -TaskName $legacyName -ErrorAction SilentlyContinue
  if ($legacy -and $legacy.State -eq 'Running') {
    Stop-ScheduledTask -TaskName $legacyName -ErrorAction SilentlyContinue
  }
  if ($legacy -and $legacy.State -ne 'Disabled') {
    Disable-ScheduledTask -TaskName $legacyName -ErrorAction SilentlyContinue | Out-Null
  }
}
Stage 'Legacy Claude poller and legacy self-heal monitor preserved as disabled rollback-only tasks.'

$currentIdentity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$principal = New-ScheduledTaskPrincipal -UserId $currentIdentity -LogonType Interactive -RunLevel Highest

# Register or replace the neutral controller. It is a single-shot controller
# invoked once per minute while active. MultipleInstances IgnoreNew prevents
# overlapping controller instances.
$controllerArgs = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$ControllerPath`" -CredentialFile `"$CredentialFile`" -WorkspacePath `"$WorkspacePath`" -WorkerRoot `"$InstallRoot`""
$controllerAction = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $controllerArgs
$controllerTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(15) -RepetitionInterval (New-TimeSpan -Minutes 1)
$controllerSettings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 5)

$existingController = Get-ScheduledTask -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
if ($existingController -and $existingController.State -eq 'Running') {
  Stage "$ControllerTaskName is currently running. Existing registration retained; installed script files were refreshed for the next cycle."
} else {
  Register-ScheduledTask -TaskName $ControllerTaskName -Action $controllerAction -Trigger $controllerTrigger -Settings $controllerSettings -Principal $principal -Description 'DCSE v7.2 neutral universal dispatch controller. Provider-independent controller only.' -Force | Out-Null
  Stage "$ControllerTaskName registered/enabled at 60-second cadence."
}

# Register the lightweight wake probe every five minutes.
$probeArgs = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$WakeProbePath`" -CredentialFile `"$CredentialFile`" -ControllerTaskName `"$ControllerTaskName`""
$probeAction = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $probeArgs
$probeTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(5) -RepetitionInterval (New-TimeSpan -Minutes 5)
$probeSettings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
Register-ScheduledTask -TaskName $WakeProbeTaskName -Action $probeAction -Trigger $probeTrigger -Settings $probeSettings -Principal $principal -Description 'DCSE v7.2 lightweight wake probe. Starts only the neutral universal controller when a live Supabase wake request exists.' -Force | Out-Null
Stage "$WakeProbeTaskName registered/enabled at five-minute cadence."

# Start the probe immediately. An already-created live wake request should be
# ACKNOWLEDGED and then CONSUMED only after controller start is verified.
$controllerBefore = Get-ScheduledTaskInfo -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
$controllerBeforeRun = if ($controllerBefore) { $controllerBefore.LastRunTime } else { [DateTime]::MinValue }
Start-ScheduledTask -TaskName $WakeProbeTaskName
Stage 'Wake probe started immediately.'

$deadline = (Get-Date).AddSeconds(30)
$controllerStarted = $false
$controllerState = $null
$controllerLastRun = $controllerBeforeRun
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 1
  $controller = Get-ScheduledTask -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  $controllerInfo = Get-ScheduledTaskInfo -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  if ($controller) { $controllerState = $controller.State.ToString() }
  if ($controllerInfo) { $controllerLastRun = $controllerInfo.LastRunTime }
  if (($controller -and $controller.State -eq 'Running') -or ($controllerInfo -and $controllerInfo.LastRunTime -gt $controllerBeforeRun)) {
    $controllerStarted = $true
    break
  }
}

# If no live wake was present, directly smoke-start the neutral controller.
# This does not launch a provider model by itself; the controller only launches
# workers that Supabase reports as admitted and eligible.
if (-not $controllerStarted) {
  Stage 'No controller start observed from wake probe within 30 seconds. Performing one neutral controller smoke start.'
  Start-ScheduledTask -TaskName $ControllerTaskName
  Start-Sleep -Seconds 3
  $controllerInfo = Get-ScheduledTaskInfo -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  $controller = Get-ScheduledTask -TaskName $ControllerTaskName -ErrorAction SilentlyContinue
  if ($controller) { $controllerState = $controller.State.ToString() }
  if ($controllerInfo) { $controllerLastRun = $controllerInfo.LastRunTime }
  $controllerStarted = (($controller -and $controller.State -eq 'Running') -or ($controllerInfo -and $controllerInfo.LastRunTime -gt $controllerBeforeRun))
}

$probeTask = Get-ScheduledTask -TaskName $WakeProbeTaskName
$probeInfo = Get-ScheduledTaskInfo -TaskName $WakeProbeTaskName
$controllerTask = Get-ScheduledTask -TaskName $ControllerTaskName
$controllerInfo = Get-ScheduledTaskInfo -TaskName $ControllerTaskName

$receipt = [ordered]@{
  receipt_type = 'V7_2_POLLER_COMMUNICATION_RECOVERY'
  generated_at = [DateTime]::UtcNow.ToString('o')
  host = $env:COMPUTERNAME
  user = $currentIdentity
  controller_task = $ControllerTaskName
  controller_state = $controllerTask.State.ToString()
  controller_last_run_time = $controllerInfo.LastRunTime.ToUniversalTime().ToString('o')
  controller_last_task_result = $controllerInfo.LastTaskResult
  controller_start_verified = $controllerStarted
  wake_probe_task = $WakeProbeTaskName
  wake_probe_state = $probeTask.State.ToString()
  wake_probe_last_run_time = $probeInfo.LastRunTime.ToUniversalTime().ToString('o')
  wake_probe_last_task_result = $probeInfo.LastTaskResult
  legacy_poller_state = (Get-ScheduledTask -TaskName $LegacyPollerTaskName -ErrorAction SilentlyContinue).State.ToString()
  legacy_monitor_state = (Get-ScheduledTask -TaskName $LegacyMonitorTaskName -ErrorAction SilentlyContinue).State.ToString()
  controller_path = $ControllerPath
  worker_path = $WorkerPath
  wake_probe_path = $WakeProbePath
  secrets_exposed = $false
}

$receipt | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $ReceiptPath -Encoding UTF8
Stage "Recovery receipt written: $ReceiptPath"
$receipt | ConvertTo-Json -Depth 10

if (-not $controllerStarted) { exit 20 }
exit 0
