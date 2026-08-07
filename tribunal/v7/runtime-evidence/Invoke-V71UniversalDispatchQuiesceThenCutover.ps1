# DCSE v7.1 - quiesce recurring legacy poller + legacy health monitor, then invoke universal cutover
[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$OldTaskName = 'DCSE_ClaudeCode_Poller',
  [string]$OldHealthTaskName = 'DCSE_PollerHealthMonitor',
  [string]$CutoverUrl = 'https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/d9db82c282fde4ceaf826a6666b63e3251ba4267/tribunal/v7/runtime-evidence/Invoke-V71UniversalDispatchCutover.ps1',
  [int]$RecentAssignmentMinutes = 30
)

$ErrorActionPreference='Stop'
function Stage([string]$Message){ Write-Host "[V7.1 QUIESCE] $Message" }

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

# Safety gate: query at most one recently updated running assignment and inspect
# raw JSON so Windows PowerShell cannot collapse an array into property arrays.
$cutoff=(Get-Date).ToUniversalTime().AddMinutes(-1*$RecentAssignmentMinutes).ToString('o')
$cutoffEsc=[uri]::EscapeDataString($cutoff)
$recentUri="$SupabaseUrl/rest/v1/agent_task_assignments?status=eq.running&updated_at=gte.$cutoffEsc&select=id,updated_at&limit=1"
Stage 'Checking for legitimate recent running assignments'
$recentResponse=Invoke-WebRequest -UseBasicParsing -Method Get -Uri $recentUri -Headers $ReadHeaders -TimeoutSec 20
$recentContent=([string]$recentResponse.Content).Trim()
if($recentContent -and $recentContent -ne '[]'){
  throw "Refusing cutover: a running assignment was updated within the last $RecentAssignmentMinutes minutes."
}

$old=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
$oldHealth=Get-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue
$oldWasEnabled=($old -and $old.State -ne 'Disabled')
$healthWasEnabled=($oldHealth -and $oldHealth.State -ne 'Disabled')

Stage 'Disabling legacy health monitor and Claude poll trigger'
if($oldHealth){
  Disable-ScheduledTask -TaskName $OldHealthTaskName | Out-Null
  Stop-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue
}
if($old){
  Disable-ScheduledTask -TaskName $OldTaskName | Out-Null
  Stop-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
}

Start-Sleep -Seconds 1

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
  Stage "Stopping legacy poller process tree roots=$($seedIds -join ',')"
  $treeIds=Get-DescendantProcessIds -RootIds $seedIds -ProcessRows $rows
  foreach($processId in ($treeIds | Sort-Object -Descending)){
    try { Stop-Process -Id $processId -Force -ErrorAction Stop } catch {}
  }
}

Start-Sleep -Seconds 1
$old=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
if($old -and $old.State -eq 'Running'){ throw "Legacy task $OldTaskName remains Running after disable/stop." }

# Run the exact reconciled reversible cutover now that legacy restart paths are quiesced.
$cutover=Join-Path $env:TEMP 'Invoke-V71UniversalDispatchCutover.ps1'
try {
  Stage 'Downloading reconciled universal cutover'
  Invoke-WebRequest -UseBasicParsing -Uri $CutoverUrl -OutFile $cutover -TimeoutSec 30
  Stage 'Invoking universal cutover'
  & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $cutover -CredentialFile $CredentialFile
  if($LASTEXITCODE -ne 0){ throw "Universal cutover returned exit code $LASTEXITCODE" }
  Stage 'Universal cutover completed'
}
catch {
  Stage "Cutover failed: $($_.Exception.Message) -- restoring pre-quiesce scheduler state"
  if($oldWasEnabled -and (Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue)){
    Enable-ScheduledTask -TaskName $OldTaskName | Out-Null
    Start-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
  }
  if($healthWasEnabled -and (Get-ScheduledTask -TaskName $OldHealthTaskName -ErrorAction SilentlyContinue)){
    Enable-ScheduledTask -TaskName $OldHealthTaskName | Out-Null
  }
  throw
}
finally {
  Remove-Item -LiteralPath $cutover -Force -ErrorAction SilentlyContinue
}

# Successful universal cutover intentionally leaves both Claude-specific legacy
# scheduler components disabled as rollback-only artifacts.
