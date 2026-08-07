# DCSE v7.1 Universal Dispatch Controller cutover
#
# Installs the exact current neutral controller + worker wrapper, verifies Qwen
# host prerequisites, and registers the recurring neutral controller while
# preserving the legacy Claude task as rollback-only. No silent wait loops.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$InstallRoot = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS',
  [string]$WorkspacePath = 'C:\DS All Things\DCSE_Command_Center',
  [string]$OldTaskName = 'DCSE_ClaudeCode_Poller',
  [string]$NewTaskName = 'DCSE_Universal_Dispatch_Controller',
  [bool]$AdmitQwenAfterVerifiedSmoke = $true
)

$ErrorActionPreference='Stop'

# NON-REGRESSION PIN: this commit contains the corrected per-agent admission
# lookup plus the currently reviewed worker. Do not point this back to an older
# cutover/controller commit.
$RepoCommit='31c5e1c9a66bf3deef8abf605ff156a10c39a119'
$ControllerBlob='cd393b495dfafaf8cbc5cf0568219989954f7e08'
$WorkerBlob='c602031a9ab05dd4babd4b8bdaba0ac8af25c4de'
$ControllerName='dcse_dispatch_controller.ps1'
$WorkerName='dcse_agent_worker.ps1'
$ControllerUrl="https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/$RepoCommit/tribunal/v7/runtime-evidence/$ControllerName"
$WorkerUrl="https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/$RepoCommit/tribunal/v7/runtime-evidence/$WorkerName"
$ControllerPath=Join-Path $InstallRoot $ControllerName
$WorkerPath=Join-Path $InstallRoot $WorkerName
$Timestamp=Get-Date -Format 'yyyyMMdd_HHmmss'
$ReceiptPath=Join-Path $InstallRoot "V7_1_UNIVERSAL_DISPATCH_CUTOVER_$Timestamp.json"
$TempController=Join-Path $env:TEMP "$ControllerName.$Timestamp.tmp"
$TempWorker=Join-Path $env:TEMP "$WorkerName.$Timestamp.tmp"
$SmokeTaskKey='QWEN-POLLER-SMOKE-20260807-001'
$SmokeRelative='scratch\qwen_poller_hello_20260807.txt'
$SmokePath=Join-Path $WorkspacePath $SmokeRelative

function Stage([string]$Message) { Write-Host "[V7.1] $Message" }
function Get-GitBlobSha1([byte[]]$Bytes) {
  $header=[Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)`0")
  $combined=New-Object byte[] ($header.Length+$Bytes.Length)
  [Array]::Copy($header,0,$combined,0,$header.Length)
  [Array]::Copy($Bytes,0,$combined,$header.Length,$Bytes.Length)
  $sha=[Security.Cryptography.SHA1]::Create()
  try { return (($sha.ComputeHash($combined)|ForEach-Object{$_.ToString('x2')}) -join '') }
  finally { $sha.Dispose() }
}
function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr=[Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}
function Parse-OrThrow([string]$Path) {
  $tokens=$null; $errors=$null
  [Management.Automation.Language.Parser]::ParseFile($Path,[ref]$tokens,[ref]$errors)|Out-Null
  if ($errors -and $errors.Count -gt 0) {
    throw "PowerShell parse failed for $Path : $($errors | ForEach-Object {$_.Message} | Out-String)"
  }
}
function Clone-ObjectToHashtable($Object) {
  $h=@{}
  if ($Object) { foreach($p in $Object.PSObject.Properties){ $h[$p.Name]=$p.Value } }
  return $h
}
function Get-QwenSandboxProvider {
  foreach($name in @('docker','podman')) {
    $cmd=Get-Command $name -ErrorAction SilentlyContinue
    if (-not $cmd) { continue }
    try { & $cmd.Source info *> $null; if($LASTEXITCODE -eq 0){ return $name } } catch {}
  }
  return $null
}
function Get-SingleRestRow([string]$Uri,[hashtable]$Headers) {
  $response=Invoke-RestMethod -Method Get -Uri $Uri -Headers $Headers -TimeoutSec 20
  if($null -eq $response){ return $null }
  if($response -is [System.Array]){
    if($response.Count -ne 1){ return $null }
    return $response[0]
  }
  if($response.PSObject.Properties['id'] -and $response.id -is [System.Array]){
    if(@($response.id).Count -ne 1){ return $null }
    $row=[ordered]@{}
    foreach($p in $response.PSObject.Properties){
      $values=@($p.Value)
      $row[$p.Name]=if($values.Count -gt 0){$values[0]}else{$null}
    }
    return [pscustomobject]$row
  }
  return $response
}

if (-not (Test-Path $CredentialFile)) { throw "Credential bundle missing: $CredentialFile" }
if (-not (Test-Path $InstallRoot)) { throw "Install root missing: $InstallRoot" }

$bundle=Import-Clixml $CredentialFile
if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') { throw 'Wrong Supabase project in credential bundle.' }
$SupabaseUrl=[string]$bundle.SUPABASE_URL
$ServiceKey=SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
$Headers=@{apikey=$ServiceKey;Authorization="Bearer $ServiceKey";'Content-Type'='application/json'}
$ReadHeaders=$Headers.Clone(); $ReadHeaders['Accept-Profile']='dcse_cp'
$WriteHeaders=$Headers.Clone(); $WriteHeaders['Content-Profile']='dcse_cp'; $WriteHeaders['Prefer']='return=representation'

Stage "Downloading pinned controller/worker from $RepoCommit"
Invoke-WebRequest -UseBasicParsing -Uri $ControllerUrl -OutFile $TempController -TimeoutSec 30
Invoke-WebRequest -UseBasicParsing -Uri $WorkerUrl -OutFile $TempWorker -TimeoutSec 30
$controllerSha=Get-GitBlobSha1 ([IO.File]::ReadAllBytes($TempController))
$workerSha=Get-GitBlobSha1 ([IO.File]::ReadAllBytes($TempWorker))
if($controllerSha -ne $ControllerBlob){ throw "Controller blob mismatch: $controllerSha" }
if($workerSha -ne $WorkerBlob){ throw "Worker blob mismatch: $workerSha" }
Parse-OrThrow $TempController
Parse-OrThrow $TempWorker
Stage 'Pinned files verified and PowerShell parsed'

$backupController=$null; $backupWorker=$null
if(Test-Path $ControllerPath){ $backupController="$ControllerPath.pre_cutover_$Timestamp.bak"; Copy-Item $ControllerPath $backupController -Force }
if(Test-Path $WorkerPath){ $backupWorker="$WorkerPath.pre_cutover_$Timestamp.bak"; Copy-Item $WorkerPath $backupWorker -Force }
Copy-Item $TempController $ControllerPath -Force
Copy-Item $TempWorker $WorkerPath -Force
Stage 'Current controller/worker installed with backups preserved'

# Host Qwen verification: executable, version, Windows sandbox provider, existing smoke artifact.
$qwenCmd=Get-Command qwen -ErrorAction SilentlyContinue
$qwenVersion=$null; $sandboxProvider=$null; $smokeHash=$null; $smokeContent=$null; $smokeVerified=$false
if($qwenCmd){
  try { $qwenVersion=((& $qwenCmd.Source --version 2>&1)|Out-String).Trim() } catch {}
  $sandboxProvider=Get-QwenSandboxProvider
}
if(Test-Path $SmokePath){
  $smokeHash=(Get-FileHash -LiteralPath $SmokePath -Algorithm SHA256).Hash.ToLowerInvariant()
  $smokeContent=(Get-Content -LiteralPath $SmokePath -Raw)
  $smokeVerified=([bool]$qwenCmd -and [bool]$qwenVersion -and [bool]$sandboxProvider -and $smokeContent.Length -gt 0 -and $smokeContent -match '(?i)qwen' -and $smokeContent -match '(?i)poller')
}
Stage "Qwen preflight cli=$qwenVersion sandbox=$sandboxProvider smoke_verified=$smokeVerified"

# Add a non-destructive host-verification event to the existing smoke task.
$taskUri="$SupabaseUrl/rest/v1/agent_tasks?task_key=eq.$SmokeTaskKey&select=id,status&limit=1"
$taskRow=Get-SingleRestRow $taskUri $ReadHeaders
if($taskRow){
  $preview=if($smokeContent -and $smokeContent.Length -gt 500){$smokeContent.Substring(0,500)}else{$smokeContent}
  $event=@{
    task_id=$taskRow.id; event_type='review'; actor_label='V7.1 Universal Dispatch Cutover';
    event_summary=if($smokeVerified){'Qwen Windows smoke artifact independently verified on host'}else{'Qwen Windows smoke artifact verification incomplete'};
    event_payload=@{verified=$smokeVerified;artifact=$SmokeRelative;sha256=$smokeHash;content_preview=$preview;qwen_version=$qwenVersion;sandbox_provider=$sandboxProvider;host=$env:COMPUTERNAME;controller_commit=$RepoCommit}
  }|ConvertTo-Json -Depth 10 -Compress
  Invoke-RestMethod -Method Post -Uri "$SupabaseUrl/rest/v1/agent_task_events" -Headers $WriteHeaders -Body $event -TimeoutSec 20|Out-Null
}

$qwenAdmitted=$false
if($AdmitQwenAfterVerifiedSmoke -and $smokeVerified){
  $regUri="$SupabaseUrl/rest/v1/agent_registry?agent_key=eq.qwen_windows_cli&select=id,restricted_actions,metadata&limit=1"
  $reg=Get-SingleRestRow $regUri $ReadHeaders
  if(-not $reg){throw 'qwen_windows_cli registry row missing or ambiguous'}
  $restricted=@($reg.restricted_actions|Where-Object{$_ -notin @('automatic_task_claim','autonomous_polling')})
  $metadata=Clone-ObjectToHashtable $reg.metadata
  $metadata['poller_eligible']=$true
  $metadata['automatic_claim_eligible']=$true
  $metadata['admission_status']='VERIFIED_WINDOWS_SMOKE'
  $metadata['verified_runtime_surface']='qwen_windows_cli'
  $metadata['verified_host']=$env:COMPUTERNAME
  $metadata['verified_cli_version']=$qwenVersion
  $metadata['verified_sandbox_provider']=$sandboxProvider
  $metadata['verified_smoke_sha256']=$smokeHash
  $patch=@{restricted_actions=$restricted;metadata=$metadata;updated_at=(Get-Date).ToUniversalTime().ToString('o')}|ConvertTo-Json -Depth 20 -Compress
  Invoke-RestMethod -Method Patch -Uri "$SupabaseUrl/rest/v1/agent_registry?id=eq.$($reg.id)" -Headers $WriteHeaders -Body $patch -TimeoutSec 20|Out-Null
  $qwenAdmitted=$true
  Stage 'Qwen registry admission reconciled from verified host evidence'
}

# No silent wait. This script assumes the caller has already quiesced legacy
# execution. If not, fail immediately and preserve the installed-file backups.
$oldTask=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
$oldTaskWasEnabled=($oldTask -and $oldTask.State -ne 'Disabled')
if($oldTask -and $oldTask.State -eq 'Running'){
  throw "Legacy task $OldTaskName is Running. Quiesce it first; no scheduler cutover attempted."
}

try {
  if($oldTask){ Disable-ScheduledTask -TaskName $OldTaskName|Out-Null }

  Stage "Registering $NewTaskName"
  Unregister-ScheduledTask -TaskName $NewTaskName -Confirm:$false -ErrorAction SilentlyContinue
  $action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ControllerPath`" -CredentialFile `"$CredentialFile`" -WorkspacePath `"$WorkspacePath`" -WorkerRoot `"$InstallRoot`""
  $trigger=New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(20) -RepetitionInterval (New-TimeSpan -Minutes 1)
  $principal=New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Highest
  $settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
  Register-ScheduledTask -TaskName $NewTaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force|Out-Null

  $controllerLog=Join-Path $InstallRoot 'dispatch_controller.log'
  $beforeLogTime=if(Test-Path $controllerLog){(Get-Item $controllerLog).LastWriteTimeUtc}else{[datetime]::MinValue}
  Stage 'Smoke-starting neutral controller once'
  Start-ScheduledTask -TaskName $NewTaskName
  $deadline=(Get-Date).AddSeconds(20)
  do {
    Start-Sleep -Seconds 2
    $logAdvanced=(Test-Path $controllerLog) -and ((Get-Item $controllerLog).LastWriteTimeUtc -gt $beforeLogTime)
  } while(-not $logAdvanced -and (Get-Date) -lt $deadline)
  if(-not $logAdvanced){ throw 'New controller did not advance dispatch_controller.log within 20 seconds.' }
  Stage 'Controller smoke log advanced; recurring task registered'
}
catch {
  Stage "CUTOVER FAILED: $($_.Exception.Message) -- restoring prior state"
  Disable-ScheduledTask -TaskName $NewTaskName -ErrorAction SilentlyContinue|Out-Null
  if($oldTaskWasEnabled -and (Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue)){
    Enable-ScheduledTask -TaskName $OldTaskName|Out-Null
    Start-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
  }
  if($backupController){Copy-Item $backupController $ControllerPath -Force}
  if($backupWorker){Copy-Item $backupWorker $WorkerPath -Force}
  throw
}
finally {
  Remove-Item $TempController,$TempWorker -Force -ErrorAction SilentlyContinue
}

$oldNow=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
$newNow=Get-ScheduledTask -TaskName $NewTaskName -ErrorAction SilentlyContinue
$receipt=[ordered]@{
  receipt_type='V7_1_UNIVERSAL_DISPATCH_CUTOVER'
  generated_at=(Get-Date).ToUniversalTime().ToString('o')
  host=$env:COMPUTERNAME
  controller_commit=$RepoCommit
  controller_blob_sha=$ControllerBlob
  worker_blob_sha=$WorkerBlob
  old_task=$OldTaskName
  old_task_state=if($oldNow){$oldNow.State.ToString()}else{'MISSING'}
  new_task=$NewTaskName
  new_task_state=if($newNow){$newNow.State.ToString()}else{'MISSING'}
  qwen_cli_version=$qwenVersion
  qwen_sandbox_provider=$sandboxProvider
  qwen_smoke_artifact=$SmokeRelative
  qwen_smoke_sha256=$smokeHash
  qwen_smoke_verified=$smokeVerified
  qwen_admitted=$qwenAdmitted
  rollback="Disable $NewTaskName; restore .pre_cutover backups; restore $OldTaskName only if it was enabled before cutover."
  secrets_exposed=$false
}
$receipt|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $ReceiptPath -Encoding UTF8
Stage "Cutover receipt: $ReceiptPath"
$receipt|ConvertTo-Json -Depth 10
