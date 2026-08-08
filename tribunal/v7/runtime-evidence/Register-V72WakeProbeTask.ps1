# Register the DCSE v7.2 lightweight wake probe.
# This task does not launch a model unless a live wake request exists.
# It never enables a provider-specific legacy poller.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$WakeProbePath = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS\dcse_wake_probe.ps1',
  [string]$WakeProbeTaskName = 'DCSE_Universal_Dispatch_WakeProbe',
  [string]$ControllerTaskName = 'DCSE_Universal_Dispatch_Controller'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $CredentialFile)) {
  throw "Credential bundle missing: $CredentialFile"
}
if (-not (Test-Path -LiteralPath $WakeProbePath)) {
  throw "Wake probe script missing: $WakeProbePath"
}

$actionArgs = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$WakeProbePath`" -CredentialFile `"$CredentialFile`" -ControllerTaskName `"$ControllerTaskName`""
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $actionArgs
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(10) -RepetitionInterval (New-TimeSpan -Minutes 5)
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -DontStopOnIdleEnd -ExecutionTimeLimit (New-TimeSpan -Minutes 2)
$principal = New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Highest

Register-ScheduledTask -TaskName $WakeProbeTaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'DCSE v7.2 neutral wake probe. Checks Supabase every 5 minutes and starts only DCSE_Universal_Dispatch_Controller when a live wake exists.' -Force | Out-Null

Start-ScheduledTask -TaskName $WakeProbeTaskName
$task = Get-ScheduledTask -TaskName $WakeProbeTaskName
$info = Get-ScheduledTaskInfo -TaskName $WakeProbeTaskName

[ordered]@{
  ok = $true
  host = $env:COMPUTERNAME
  task_name = $WakeProbeTaskName
  task_state = $task.State.ToString()
  last_run_time = $info.LastRunTime.ToUniversalTime().ToString('o')
  next_run_time = $info.NextRunTime.ToUniversalTime().ToString('o')
  controller_task = $ControllerTaskName
  legacy_poller_enabled = $false
} | ConvertTo-Json -Depth 5
