# DCSE v7.1 - quiesce recurring legacy poller + legacy health monitor, then invoke universal cutover
[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$OldTaskName = 'DCSE_ClaudeCode_Poller',
  [string]$OldHealthTaskName = 'DCSE_PollerHealthMonitor',
  [string]$CutoverUrl = 'https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/97cf0208161b2a0f4702931a521a2d5ba675acc9/tribunal/v7/runtime-evidence/Invoke-V71UniversalDispatchCutover.ps1',
  [int]$RecentAssignmentMinutes = 30
)

$ErrorActionPreference='Stop'

function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}

function Get-DescendantProcessIds([int[]]$RootIds, $ProcessRows) {
  $seen = New-Object 'System.Collections.Generic.HashSet[int]'
  $queue = New-Object 'System.Collections.Generic.Queue[int]'
  foreach($rootId in $RootIds){ if($seen.Add($rootId)){ $queue.Enqueue($rootId) } }
  while($queue.Count -gt 0){
    $parent=$queue.Dequeue()
    foreach($row in $ProcessRows | Where-Object { $_.ParentProcessId -eq $parent }){
      $child=[int]$row.ProcessId
      if($seen.Add($child)){ $queue.Enqueue($child) }
    }
  }
  return @($seen)
}

if(-not (Test-Path -LiteralPath $CredentialFile)){ throw "Credential bundle missing: $CredentialFile" }
$bundle=Import-Clixml $CredentialFile
if($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal'){ throw 'Wrong Supabase project in credential bundle.' }
$SupabaseUrl=[string]$bundle.SUPABASE_URL
$ServiceKey=SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
$ReadHeaders=@{apikey=$ServiceKey;Authorization="Bearer $ServiceKey";'Accept-Profile'='dcse_cp'}

# Safety gate: refuse to quiesce if any assignment has transitioned recently and is still running.
$running=@(Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_task_assignments?status=eq.running&select=id,updated_at&order=updated_at.desc" -Headers $ReadHeaders)
$cutoff=(Get-Date).ToUniversalTime().AddMinutes(-1*$RecentAssignmentMinutes)
$recent=@($running | Where-Object { $_.updated_at -and ([datetime]$_.updated_at).ToUniversalTime() -gt $cutoff })
if($recent.Count -gt 0){
  throw "Refusing cutover: $($recent.Count) running assignment(s) updated within the last $RecentAssignmentMinutes minutes."
}

# Prevent both the one-minute poll trigger and its five-minute self-heal monitor from racing the cutover.
$old=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
$oldHealth=Get-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue
$healthWasEnabled=$false
if($oldHealth){
  $healthWasEnabled=($oldHealth.State -ne 'Disabled')
  Disable-ScheduledTask -TaskName $OldHealthTaskName | Out-Null
  Stop-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue
}
if($old){
  Disable-ScheduledTask -TaskName $OldTaskName | Out-Null
  Stop-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 2

# Kill ONLY the legacy poller/health-monitor process trees. Do not kill unrelated interactive Claude/Qwen sessions.
$rows=@(Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId,Name,CommandLine)
$seedRows=@($rows | Where-Object {
  $_.CommandLine -and (
    $_.CommandLine -match '(?i)claude_code_poller\.ps1' -or
    $_.CommandLine -match '(?i)Run-ClaudeCodePoller-Hidden\.vbs' -or
    $_.CommandLine -match '(?i)poller_health_monitor\.ps1' -or
    $_.CommandLine -match '(?i)Run-PollerHealthMonitor-Hidden\.vbs'
  )
})
$seedIds=@($seedRows | ForEach-Object { [int]$_.ProcessId })
if($seedIds.Count -gt 0){
  $treeIds=Get-DescendantProcessIds -RootIds $seedIds -ProcessRows $rows
  foreach($processId in ($treeIds | Sort-Object -Descending)){
    try { Stop-Process -Id $processId -Force -ErrorAction Stop } catch {}
  }
}

Start-Sleep -Seconds 2
$old=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
if($old -and $old.State -eq 'Running'){ throw "Legacy task $OldTaskName remains Running after disable/stop." }

# Run the pinned reversible cutover now that legacy restart paths are quiesced.
$cutover=Join-Path $env:TEMP 'Invoke-V71UniversalDispatchCutover.ps1'
try {
  Invoke-WebRequest -UseBasicParsing -Uri $CutoverUrl -OutFile $cutover
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $cutover
  if($LASTEXITCODE -ne 0){ throw "Universal cutover returned exit code $LASTEXITCODE" }
}
catch {
  # Inner cutover restores the old poller on failure. Restore its legacy health monitor too if it was previously enabled.
  if($healthWasEnabled -and (Get-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue)){
    Enable-ScheduledTask -TaskName $OldHealthTaskName | Out-Null
  }
  throw
}

# Successful universal cutover intentionally leaves the Claude-specific legacy health monitor disabled.
