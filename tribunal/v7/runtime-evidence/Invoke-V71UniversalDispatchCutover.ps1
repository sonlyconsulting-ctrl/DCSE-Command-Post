# DCSE v7.1 Universal Dispatch Controller cutover
#
# Installs the pinned neutral controller + worker wrapper, verifies the existing
# Qwen smoke artifact, optionally admits Qwen only after host evidence passes,
# and replaces the active schedule while preserving the legacy Claude task as
# immediate rollback. Does not delete the old poller.

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
$RepoCommit='a890aba38f318cb1691a13113c30ccb7a6fd0429'
$ControllerBlob='c2834bf6a84649135183849736d70a50b851ad72'
$WorkerBlob='08f2dac0f04f526c3eec405089104ef86f132050'
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

if (-not (Test-Path $CredentialFile)) { throw "Credential bundle missing: $CredentialFile" }
if (-not (Test-Path $InstallRoot)) { throw "Install root missing: $InstallRoot" }

$bundle=Import-Clixml $CredentialFile
if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') { throw 'Wrong Supabase project in credential bundle.' }
$SupabaseUrl=[string]$bundle.SUPABASE_URL
$ServiceKey=SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
$Headers=@{apikey=$ServiceKey;Authorization="Bearer $ServiceKey";'Content-Type'='application/json'}
$ReadHeaders=$Headers.Clone(); $ReadHeaders['Accept-Profile']='dcse_cp'
$WriteHeaders=$Headers.Clone(); $WriteHeaders['Content-Profile']='dcse_cp'; $WriteHeaders['Prefer']='return=representation'

# Download exact pinned controller/worker and verify Git blob identities.
Invoke-WebRequest -UseBasicParsing -Uri $ControllerUrl -OutFile $TempController
Invoke-WebRequest -UseBasicParsing -Uri $WorkerUrl -OutFile $TempWorker
$controllerSha=Get-GitBlobSha1 ([IO.File]::ReadAllBytes($TempController))
$workerSha=Get-GitBlobSha1 ([IO.File]::ReadAllBytes($TempWorker))
if($controllerSha -ne $ControllerBlob){ throw "Controller blob mismatch: $controllerSha" }
if($workerSha -ne $WorkerBlob){ throw "Worker blob mismatch: $workerSha" }
Parse-OrThrow $TempController
Parse-OrThrow $TempWorker

$backupController=$null; $backupWorker=$null
if(Test-Path $ControllerPath){ $backupController="$ControllerPath.pre_cutover_$Timestamp.bak"; Copy-Item $ControllerPath $backupController -Force }
if(Test-Path $WorkerPath){ $backupWorker="$WorkerPath.pre_cutover_$Timestamp.bak"; Copy-Item $WorkerPath $backupWorker -Force }
Copy-Item $TempController $ControllerPath -Force
Copy-Item $TempWorker $WorkerPath -Force

# Host Qwen verification: executable, version, Windows sandbox provider, existing smoke artifact.
$qwenCmd=Get-Command qwen -ErrorAction SilentlyContinue
$qwenVersion=$null; $sandboxProvider=$null; $smokeExists=$false; $smokeHash=$null; $smokeContent=$null; $smokeVerified=$false
if($qwenCmd){
  try { $qwenVersion=((& $qwenCmd.Source --version 2>&1)|Out-String).Trim() } catch {}
  $sandboxProvider=Get-QwenSandboxProvider
}
if(Test-Path $SmokePath){
  $smokeExists=$true
  $smokeHash=(Get-FileHash -LiteralPath $SmokePath -Algorithm SHA256).Hash.ToLowerInvariant()
  $smokeContent=(Get-Content -LiteralPath $SmokePath -Raw)
  $smokeVerified=([bool]$qwenCmd -and [bool]$qwenVersion -and [bool]$sandboxProvider -and $smokeContent.Length -gt 0 -and $smokeContent -match '(?i)qwen' -and $smokeContent -match '(?i)poller')
}

# Add a non-destructive host-verification event to the existing smoke task.
$taskRows=@(Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_tasks?task_key=eq.$SmokeTaskKey&select=id,status" -Headers $ReadHeaders)
if($taskRows.Count -gt 0){
  $preview=if($smokeContent -and $smokeContent.Length -gt 500){$smokeContent.Substring(0,500)}else{$smokeContent}
  $event=@{
    task_id=$taskRows[0].id; event_type='review'; actor_label='V7.1 Universal Dispatch Cutover';
    event_summary=if($smokeVerified){'Qwen Windows smoke artifact independently verified on host'}else{'Qwen Windows smoke artifact verification incomplete'};
    event_payload=@{verified=$smokeVerified;artifact=$SmokeRelative;sha256=$smokeHash;content_preview=$preview;qwen_version=$qwenVersion;sandbox_provider=$sandboxProvider;host=$env:COMPUTERNAME;controller_commit=$RepoCommit}
  }|ConvertTo-Json -Depth 10 -Compress
  Invoke-RestMethod -Method Post -Uri "$SupabaseUrl/rest/v1/agent_task_events" -Headers $WriteHeaders -Body $event|Out-Null
}

$qwenAdmitted=$false
if($AdmitQwenAfterVerifiedSmoke -and $smokeVerified){
  $reg=@(Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_registry?agent_key=eq.qwen_windows_cli&select=id,restricted_actions,metadata" -Headers $ReadHeaders)
  if($reg.Count -eq 0){throw 'qwen_windows_cli registry row missing'}
  $restricted=@($reg[0].restricted_actions|Where-Object{$_ -notin @('automatic_task_claim','autonomous_polling')})
  $metadata=Clone-ObjectToHashtable $reg[0].metadata
  $metadata['poller_eligible']=$true
  $metadata['automatic_claim_eligible']=$true
  $metadata['admission_status']='VERIFIED_WINDOWS_SMOKE'
  $metadata['verified_runtime_surface']='qwen_windows_cli'
  $metadata['verified_host']=$env:COMPUTERNAME
  $metadata['verified_cli_version']=$qwenVersion
  $metadata['verified_sandbox_provider']=$sandboxProvider
  $metadata['verified_smoke_sha256']=$smokeHash
  $patch=@{restricted_actions=$restricted;metadata=$metadata;updated_at=(Get-Date).ToUniversalTime().ToString('o')}|ConvertTo-Json -Depth 20 -Compress
  Invoke-RestMethod -Method Patch -Uri "$SupabaseUrl/rest/v1/agent_registry?id=eq.$($reg[0].id)" -Headers $WriteHeaders -Body $patch|Out-Null
  $qwenAdmitted=$true
}

# Do not cut over while the legacy scheduled process is actively executing.
$oldTask=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue
if($oldTask -and $oldTask.State -eq 'Running'){
  $deadline=(Get-Date).AddSeconds(120)
  do { Start-Sleep -Seconds 5; $oldTask=Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue } while($oldTask.State -eq 'Running' -and (Get-Date) -lt $deadline)
  if($oldTask.State -eq 'Running'){ throw "Legacy task $OldTaskName is still Running; controller files installed but scheduler cutover was not attempted." }
}

$rollbackNeeded=$false
try {
  if($oldTask){ Disable-ScheduledTask -TaskName $OldTaskName|Out-Null; $rollbackNeeded=$true }

  Unregister-ScheduledTask -TaskName $NewTaskName -Confirm:$false -ErrorAction SilentlyContinue
  $action=New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ControllerPath`" -CredentialFile `"$CredentialFile`" -WorkspacePath `"$WorkspacePath`" -WorkerRoot `"$InstallRoot`""
  $trigger=New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(20) -RepetitionInterval (New-TimeSpan -Minutes 1)
  $principal=New-ScheduledTaskPrincipal -UserId ([Security.Principal.WindowsIdentity]::GetCurrent().Name) -LogonType Interactive -RunLevel Highest
  $settings=New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 5)
  Register-ScheduledTask -TaskName $NewTaskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force|Out-Null

  $controllerLog=Join-Path $InstallRoot 'dispatch_controller.log'
  $beforeLogTime=if(Test-Path $controllerLog){(Get-Item $controllerLog).LastWriteTimeUtc}else{[datetime]::MinValue}
  Start-ScheduledTask -TaskName $NewTaskName
  Start-Sleep -Seconds 12
  $newInfo=Get-ScheduledTaskInfo -TaskName $NewTaskName
  $logAdvanced=(Test-Path $controllerLog) -and ((Get-Item $controllerLog).LastWriteTimeUtc -gt $beforeLogTime)
  if(-not $logAdvanced){ throw 'New controller did not advance dispatch_controller.log during smoke start.' }
  $rollbackNeeded=$false
}
catch {
  Disable-ScheduledTask -TaskName $NewTaskName -ErrorAction SilentlyContinue|Out-Null
  if($oldTask){ Enable-ScheduledTask -TaskName $OldTaskName|Out-Null; Start-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue }
  if($backupController){Copy-Item $backupController $ControllerPath -Force}
  if($backupWorker){Copy-Item $backupWorker $WorkerPath -Force}
  throw
}
finally {
  Remove-Item $TempController,$TempWorker -Force -ErrorAction SilentlyContinue
}

$receipt=[ordered]@{
  receipt_type='V7_1_UNIVERSAL_DISPATCH_CUTOVER'
  generated_at=(Get-Date).ToUniversalTime().ToString('o')
  host=$env:COMPUTERNAME
  controller_commit=$RepoCommit
  controller_blob_sha=$ControllerBlob
  worker_blob_sha=$WorkerBlob
  old_task=$OldTaskName
  old_task_state=(Get-ScheduledTask -TaskName $OldTaskName -ErrorAction SilentlyContinue).State.ToString()
  new_task=$NewTaskName
  new_task_state=(Get-ScheduledTask -TaskName $NewTaskName -ErrorAction SilentlyContinue).State.ToString()
  qwen_cli_version=$qwenVersion
  qwen_sandbox_provider=$sandboxProvider
  qwen_smoke_artifact=$SmokeRelative
  qwen_smoke_sha256=$smokeHash
  qwen_smoke_verified=$smokeVerified
  qwen_admitted=$qwenAdmitted
  rollback="Disable $NewTaskName; enable/start $OldTaskName; restore .pre_cutover backups if required."
  secrets_exposed=$false
}
$receipt|ConvertTo-Json -Depth 10|Set-Content -LiteralPath $ReceiptPath -Encoding UTF8
$receipt|ConvertTo-Json -Depth 10
