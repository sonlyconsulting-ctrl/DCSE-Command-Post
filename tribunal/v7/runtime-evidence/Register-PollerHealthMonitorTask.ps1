# Registers poller_health_monitor.ps1 as its own independent Windows Scheduled
# Task -- deliberately separate from DCSE_ClaudeCode_Poller so it keeps
# watching even if that task gets disabled again.

$ErrorActionPreference = 'Stop'

$TaskName        = 'DCSE_PollerHealthMonitor'
$ScriptPath      = Join-Path $PSScriptRoot 'poller_health_monitor.ps1'
$CredentialFile  = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml'

if (-not (Test-Path $CredentialFile)) {
  Write-Error "Credential bundle not found: $CredentialFile"
  exit 1
}

# See Register-ClaudeCodePollerTask.ps1 for why this goes through a VBS
# launcher rather than powershell.exe -WindowStyle Hidden directly.
$VbsLauncher = Join-Path $PSScriptRoot 'Run-PollerHealthMonitor-Hidden.vbs'
$Action  = New-ScheduledTaskAction -Execute 'wscript.exe' -Argument "//B `"$VbsLauncher`""

$Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) `
             -RepetitionInterval (New-TimeSpan -Minutes 5)

$Settings = New-ScheduledTaskSettingsSet `
              -MultipleInstances IgnoreNew `
              -StartWhenAvailable `
              -DontStopOnIdleEnd `
              -ExecutionTimeLimit (New-TimeSpan -Minutes 2)

$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger `
  -Settings $Settings -Principal $Principal `
  -Description 'DCSE v7.1 poller health monitor - checks DCSE_ClaudeCode_Poller state + heartbeat staleness every 5 min, self-heals if disabled' `
  -Force

Write-Host "Registered scheduled task: $TaskName"
