# ESCD / Polar host supervisor helper.
# This is NOT a standalone poller. Dot-source it from the existing scheduled Polar/poller cycle.
# It never logs or returns the Supabase service-role credential.

Set-StrictMode -Version Latest

function Invoke-EscdPolarHostSupervisor {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory=$true)][string]$SupabaseUrl,
    [Parameter(Mandatory=$true)][string]$ServiceKey,
    [Parameter(Mandatory=$true)][string]$WorkspacePath,
    [ValidateSet('ON_DEMAND','ALWAYS_ON')][string]$Mode = 'ON_DEMAND',
    [string]$WorkerKey = 'DCS-WINDOWS-OLLAMA-01',
    [string]$WorkerScript = '',
    [string]$OllamaModel = 'qwen2.5-coder:latest'
  )

  $result = [ordered]@{
    host = $env:COMPUTERNAME
    mode = $Mode
    worker_key = $WorkerKey
    action = 'NONE'
    reason = ''
    turn_key = $null
    process_id = $null
  }

  if (-not $WorkerScript) {
    if ($env:DCSE_ESCD_WORKER_SCRIPT) {
      $WorkerScript = $env:DCSE_ESCD_WORKER_SCRIPT
    } else {
      $WorkerScript = Join-Path $WorkspacePath 'apps\escd\runtime\ollama_worker.py'
    }
  }

  $headers = @{
    'apikey' = $ServiceKey
    'Authorization' = ('Bearer ' + $ServiceKey)
    'Accept-Profile' = 'dcse_cp'
    'Content-Type' = 'application/json'
  }

  function Get-DcseRows([string]$table,[string]$query) {
    try {
      $uri = $SupabaseUrl + '/rest/v1/' + $table + '?' + $query
      $rows = Invoke-RestMethod -Method Get -Uri $uri -Headers $headers -TimeoutSec 30
      return @($rows)
    } catch {
      return @()
    }
  }

  $hostLabel = [uri]::EscapeDataString($env:COMPUTERNAME)
  $hostRows = Get-DcseRows 'runtime_host_registry' ('select=host_key,enabled,execution_eligible,dispatch_eligible,security_state,operating_mode&host_label=eq.' + $hostLabel + '&limit=1')
  if (-not $hostRows -or $hostRows.Count -eq 0) {
    $result.action = 'HOLD'
    $result.reason = 'HOST_NOT_REGISTERED'
    return [pscustomobject]$result
  }

  $hostRecord = $hostRows[0]
  if (-not $hostRecord.enabled -or -not $hostRecord.execution_eligible -or $hostRecord.security_state -ne 'VERIFIED') {
    $result.action = 'HOLD'
    $result.reason = ('HOST_NOT_ELIGIBLE:' + $hostRecord.security_state)
    return [pscustomobject]$result
  }

  $pending = Get-DcseRows 'escd_operation_turns' 'select=id,turn_key,state,provider_preference,created_at&state=eq.REQUESTED&order=created_at.asc&limit=1'
  if ($pending.Count -gt 0) { $result.turn_key = $pending[0].turn_key }

  if ($Mode -eq 'ON_DEMAND' -and $pending.Count -eq 0) {
    $result.action = 'IDLE'
    $result.reason = 'NO_PENDING_ESCD_WORK'
    return [pscustomobject]$result
  }

  $workerProcs = @()
  try {
    $workerProcs = @(Get-CimInstance Win32_Process -ErrorAction Stop | Where-Object { $_.CommandLine -and $_.CommandLine -match 'ollama_worker\.py' })
  } catch {}

  if ($workerProcs.Count -gt 0) {
    $result.action = 'RUNNING'
    $result.reason = 'ESCD_WORKER_ALREADY_RUNNING'
    $result.process_id = $workerProcs[0].ProcessId
    return [pscustomobject]$result
  }

  if (-not (Test-Path $WorkerScript)) {
    $result.action = 'HOLD'
    $result.reason = ('WORKER_SCRIPT_MISSING:' + $WorkerScript)
    return [pscustomobject]$result
  }

  $ollamaReady = $false
  try {
    Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 3 | Out-Null
    $ollamaReady = $true
  } catch {}

  if (-not $ollamaReady) {
    $ollama = Get-Command ollama.exe -ErrorAction SilentlyContinue
    if (-not $ollama) { $ollama = Get-Command ollama -ErrorAction SilentlyContinue }
    if (-not $ollama) {
      $result.action = 'HOLD'
      $result.reason = 'OLLAMA_EXECUTABLE_NOT_FOUND'
      return [pscustomobject]$result
    }

    try {
      Start-Process -FilePath $ollama.Source -ArgumentList @('serve') -WindowStyle Hidden | Out-Null
      Start-Sleep -Seconds 2
      Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 5 | Out-Null
      $ollamaReady = $true
    } catch {
      $result.action = 'HOLD'
      $result.reason = 'OLLAMA_START_FAILED'
      return [pscustomobject]$result
    }
  }

  $python = Get-Command python.exe -ErrorAction SilentlyContinue
  if (-not $python) { $python = Get-Command python -ErrorAction SilentlyContinue }
  if (-not $python) {
    $result.action = 'HOLD'
    $result.reason = 'PYTHON_NOT_FOUND'
    return [pscustomobject]$result
  }

  $priorUrl = $env:SUPABASE_URL
  $priorKey = $env:SUPABASE_SERVICE_ROLE_KEY
  $priorWorker = $env:ESCD_WORKER_KEY
  $priorModel = $env:OLLAMA_MODEL

  try {
    $env:SUPABASE_URL = $SupabaseUrl
    $env:SUPABASE_SERVICE_ROLE_KEY = $ServiceKey
    $env:ESCD_WORKER_KEY = $WorkerKey
    $env:OLLAMA_MODEL = $OllamaModel

    $argList = @('"' + $WorkerScript + '"')
    if ($Mode -eq 'ON_DEMAND') { $argList += '--once' }

    $proc = Start-Process -FilePath $python.Source -ArgumentList $argList -WorkingDirectory $WorkspacePath -WindowStyle Hidden -PassThru
    $result.action = 'STARTED'
    if ($Mode -eq 'ON_DEMAND') { $result.reason = 'ON_DEMAND_ESCD_WORKER' } else { $result.reason = 'ALWAYS_ON_ESCD_WORKER' }
    $result.process_id = $proc.Id
    return [pscustomobject]$result
  } finally {
    $env:SUPABASE_URL = $priorUrl
    $env:SUPABASE_SERVICE_ROLE_KEY = $priorKey
    $env:ESCD_WORKER_KEY = $priorWorker
    $env:OLLAMA_MODEL = $priorModel
  }
}