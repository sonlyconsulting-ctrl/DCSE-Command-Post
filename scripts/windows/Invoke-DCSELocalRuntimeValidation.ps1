param(
    [string]$OutputDir = ".\runtime-evidence\local-model-validation"
)

$ErrorActionPreference = 'Stop'
$taskId = 'DCSE-RUNTIME-LOCAL-VALIDATION-001'
$timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ss.fffZ')
New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null

function Write-JsonFile($name, $obj) {
    $path = Join-Path $OutputDir $name
    $obj | ConvertTo-Json -Depth 10 | Set-Content -Path $path -Encoding UTF8
    return $path
}

$result = [ordered]@{
    task_id = $taskId
    observed_at = $timestamp
    hostname = $env:COMPUTERNAME
    ps_version = $PSVersionTable.PSVersion.ToString()
    ollama = [ordered]@{}
    resources = [ordered]@{}
    smoke = [ordered]@{}
    extraction = [ordered]@{}
    classification = @()
}

# Resource preflight
$os = Get-CimInstance Win32_OperatingSystem
$cs = Get-CimInstance Win32_ComputerSystem
$result.resources = [ordered]@{
    total_memory_bytes = [int64]$cs.TotalPhysicalMemory
    free_memory_bytes = [int64]$os.FreePhysicalMemory * 1KB
    logical_processors = [int]$cs.NumberOfLogicalProcessors
}

# Ollama executable and endpoint
$ollamaCmd = Get-Command ollama -ErrorAction SilentlyContinue
$result.ollama.executable = if ($ollamaCmd) { $ollamaCmd.Source } else { $null }
if ($ollamaCmd) {
    try { $result.ollama.version = (& ollama --version 2>&1 | Out-String).Trim() } catch { $result.ollama.version_error = $_.Exception.Message }
}

try {
    $tags = Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:11434/api/tags' -TimeoutSec 10
    $result.ollama.endpoint = 'http://127.0.0.1:11434'
    $result.ollama.endpoint_status = 'reachable'
    $models = @($tags.models | ForEach-Object { $_.name })
    $result.ollama.models = $models
} catch {
    $result.ollama.endpoint = 'http://127.0.0.1:11434'
    $result.ollama.endpoint_status = 'unreachable'
    $result.ollama.endpoint_error = $_.Exception.Message
    $models = @()
}

# Restart-persistence evidence is observational only here: process/service state and boot time.
$result.ollama.boot_time = $os.LastBootUpTime.ToUniversalTime().ToString('o')
$result.ollama.processes = @(Get-Process ollama -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, StartTime)
$result.ollama.services = @(Get-Service -ErrorAction SilentlyContinue | Where-Object { $_.Name -match 'ollama' -or $_.DisplayName -match 'ollama' } | Select-Object Name, DisplayName, Status, StartType)

# Deterministic smoke and one bounded provenance extraction using the first installed model.
if ($models.Count -gt 0) {
    $model = $models[0]
    $smokePrompt = 'Return exactly: DCSE_OLLAMA_SMOKE_OK'
    try {
        $smokePayload = @{ model=$model; prompt=$smokePrompt; stream=$false } | ConvertTo-Json
        $smokeResponse = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/generate' -ContentType 'application/json' -Body $smokePayload -TimeoutSec 120
        $actual = [string]$smokeResponse.response
        $result.smoke = [ordered]@{
            model = $model
            expected = 'DCSE_OLLAMA_SMOKE_OK'
            actual = $actual.Trim()
            passed = ($actual.Trim() -eq 'DCSE_OLLAMA_SMOKE_OK')
        }
    } catch {
        $result.smoke = [ordered]@{ model=$model; passed=$false; error=$_.Exception.Message }
    }

    $source = 'DCSE provenance extraction test source: Structure Precedes Scale. Evidence Precedes Closure.'
    $extractPrompt = "From the SOURCE below, return exactly one JSON object with keys source_text, principle_1, principle_2. Do not add facts. SOURCE: $source"
    try {
        $extractPayload = @{ model=$model; prompt=$extractPrompt; stream=$false; format='json' } | ConvertTo-Json
        $extractResponse = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:11434/api/generate' -ContentType 'application/json' -Body $extractPayload -TimeoutSec 120
        $result.extraction = [ordered]@{
            model = $model
            source = $source
            response = [string]$extractResponse.response
            provenance_preserved = ([string]$extractResponse.response -match 'Structure Precedes Scale' -and [string]$extractResponse.response -match 'Evidence Precedes Closure')
        }
    } catch {
        $result.extraction = [ordered]@{ model=$model; source=$source; provenance_preserved=$false; error=$_.Exception.Message }
    }
}

foreach ($m in $models) {
    $status = if ($result.smoke.model -eq $m -and $result.smoke.passed) { 'operational' } else { 'standby' }
    $result.classification += [ordered]@{ model=$m; status=$status }
}
if ($models.Count -eq 0) {
    $result.classification += [ordered]@{ model=$null; status='blocked'; reason='no reachable Ollama model inventory' }
}

$evidencePath = Write-JsonFile 'local_runtime_validation.json' $result
$hash = (Get-FileHash -Algorithm SHA256 $evidencePath).Hash
[ordered]@{
    task_id = $taskId
    evidence_path = (Resolve-Path $evidencePath).Path
    sha256 = $hash
    observed_at = $timestamp
    endpoint_status = $result.ollama.endpoint_status
    model_count = $models.Count
    smoke_passed = $result.smoke.passed
    extraction_provenance_preserved = $result.extraction.provenance_preserved
} | ConvertTo-Json -Depth 6
