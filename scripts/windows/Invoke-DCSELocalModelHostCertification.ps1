param(
  [string]$OutputPath = "$PSScriptRoot\..\..\artifacts\runtime\local-model-host-certification.json"
)
$ErrorActionPreference = 'Stop'
$started = Get-Date
$result = [ordered]@{
  task_id = 'DCSE-RUNTIME-HOST-CERT'
  host = $env:COMPUTERNAME
  started_at = $started.ToString('o')
  read_only = $true
  ps_exposure = $false
  secret_exposure = $false
  checks = [ordered]@{}
}
function Add-Check($name,$status,$evidence,$note='') {
  $result.checks[$name] = [ordered]@{status=$status;evidence=$evidence;note=$note}
}
try {
  $os = Get-CimInstance Win32_OperatingSystem
  $boot = $os.LastBootUpTime
  Add-Check 'system_preflight' 'PASS' ([ordered]@{
    last_boot=$boot.ToString('o');
    uptime_hours=[math]::Round(((Get-Date)-$boot).TotalHours,2);
    total_memory_gb=[math]::Round($os.TotalVisibleMemorySize/1MB,2);
    free_memory_gb=[math]::Round($os.FreePhysicalMemory/1MB,2)
  })

  $ollama = Get-Command ollama -ErrorAction SilentlyContinue
  if(-not $ollama){ Add-Check 'ollama_executable' 'BLOCKED' $null 'ollama executable not found'; throw 'OLLAMA_NOT_FOUND' }
  $ver = (& ollama --version 2>&1 | Out-String).Trim()
  Add-Check 'ollama_executable' 'PASS' ([ordered]@{path=$ollama.Source;version=$ver})

  try {
    $tags = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -Method Get -TimeoutSec 10
    $models = @($tags.models | ForEach-Object { [ordered]@{name=$_.name;size=$_.size;modified_at=$_.modified_at} })
    Add-Check 'ollama_endpoint_inventory' 'PASS' ([ordered]@{endpoint='http://127.0.0.1:11434';models=$models})
  } catch {
    Add-Check 'ollama_endpoint_inventory' 'BLOCKED' $null $_.Exception.Message
    throw
  }

  $startupEvidence = [ordered]@{services=@();run_keys=@();scheduled_tasks=@();process=@()}
  $startupEvidence.services = @(Get-CimInstance Win32_Service | Where-Object {$_.Name -match 'ollama' -or $_.DisplayName -match 'ollama'} | Select-Object Name,State,StartMode,PathName)
  $runPaths = @('HKCU:\Software\Microsoft\Windows\CurrentVersion\Run','HKLM:\Software\Microsoft\Windows\CurrentVersion\Run')
  foreach($rp in $runPaths){ if(Test-Path $rp){ $p=Get-ItemProperty $rp; foreach($prop in $p.PSObject.Properties){ if(($prop.Name -notmatch '^PS') -and ("$($prop.Value)" -match 'ollama')){ $startupEvidence.run_keys += [ordered]@{path=$rp;name=$prop.Name;value=$prop.Value} } } } }
  $startupEvidence.scheduled_tasks = @(Get-ScheduledTask -ErrorAction SilentlyContinue | Where-Object {$_.TaskName -match 'ollama' -or $_.TaskPath -match 'ollama'} | Select-Object TaskName,TaskPath,State)
  $startupEvidence.process = @(Get-Process ollama -ErrorAction SilentlyContinue | Select-Object Id,StartTime,Path)
  $persist = ($startupEvidence.services.Count -gt 0 -or $startupEvidence.run_keys.Count -gt 0 -or $startupEvidence.scheduled_tasks.Count -gt 0)
  Add-Check 'restart_persistence_configuration' ($(if($persist){'PASS'}else{'UNKNOWN'})) $startupEvidence 'PASS means an autostart mechanism is present; a future reboot receipt is still stronger evidence.'

  if($models.Count -eq 0){ Add-Check 'deterministic_smoke' 'BLOCKED' $null 'No installed models'; throw 'NO_MODELS' }
  $model = $models[0].name
  $smokeBody = @{model=$model;prompt='Return exactly: DCSE_LOCAL_MODEL_OK';stream=$false} | ConvertTo-Json -Compress
  $smoke = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -ContentType 'application/json' -Body $smokeBody -TimeoutSec 120
  $exact = (($smoke.response).Trim() -eq 'DCSE_LOCAL_MODEL_OK')
  Add-Check 'deterministic_smoke' ($(if($exact){'PASS'}else{'FAIL'})) ([ordered]@{model=$model;response=($smoke.response).Trim();done=$smoke.done})

  $source = 'DCSE sample provenance record: Alpha=7; Beta=11; Owner=SYSTEM; Publication=false.'
  $prompt = "From the source below, output one-line JSON only with keys alpha,beta,owner,publication. Do not infer. SOURCE: $source"
  $extBody = @{model=$model;prompt=$prompt;stream=$false;format='json'} | ConvertTo-Json -Compress
  $ext = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -ContentType 'application/json' -Body $extBody -TimeoutSec 120
  $parsed = $null; try{$parsed=$ext.response|ConvertFrom-Json}catch{}
  $extractPass = $parsed -and ($parsed.alpha -eq 7) -and ($parsed.beta -eq 11) -and ($parsed.owner -eq 'SYSTEM') -and ($parsed.publication -eq $false)
  Add-Check 'governed_extraction_with_provenance' ($(if($extractPass){'PASS'}else{'FAIL'})) ([ordered]@{model=$model;source=$source;response=$ext.response;provenance='inline deterministic certification fixture'})

  $operational = $exact -and $extractPass
  Add-Check 'model_classification' 'PASS' ([ordered]@{model=$model;classification=$(if($operational){'operational'}else{'blocked'})})
} catch {
  $result.error = $_.Exception.Message
}
$result.completed_at = (Get-Date).ToString('o')
$result.overall_status = $(if(($result.checks.Values | Where-Object {$_.status -in @('FAIL','BLOCKED')}).Count -eq 0){'PASS'}else{'PARTIAL'})
$dir = Split-Path $OutputPath -Parent
if($dir -and -not (Test-Path $dir)){ New-Item -ItemType Directory -Path $dir -Force | Out-Null }
$result | ConvertTo-Json -Depth 8 | Set-Content -Path $OutputPath -Encoding UTF8
$result | ConvertTo-Json -Depth 8
