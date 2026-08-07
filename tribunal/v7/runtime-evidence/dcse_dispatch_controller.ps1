# DCSE v7.1 Neutral Dispatch Controller
#
# Single-shot scheduler cycle. This controller NEVER claims task assignments and
# NEVER waits for AI child execution. It only launches short-lived per-runtime
# worker wrappers. Each wrapper owns a per-agent mutex, atomic claim, heartbeat,
# child execution, result verification, and submit_agent_result.
#
# Intended final scheduler topology:
#   Windows Task Scheduler (every ~60s)
#       -> dcse_dispatch_controller.ps1
#           -> dcse_agent_worker.ps1 -AgentKey claude_code
#           -> dcse_agent_worker.ps1 -AgentKey qwen_windows_cli
#           -> dcse_agent_worker.ps1 -AgentKey codex
#
# Result: one controller manages many queues while Claude/Qwen/Codex can execute
# in parallel. Default concurrency remains one active worker per logical agent.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$WorkerScript = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS\dcse_agent_worker.ps1',
  [string]$WorkspacePath = 'C:\DS All Things\DCSE_Command_Center',
  [string]$WorkerRoot = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS'
)

$ErrorActionPreference = 'Stop'
$LogFile = Join-Path $WorkerRoot 'dispatch_controller.log'

function Write-Log([string]$Message) {
  Add-Content -LiteralPath $LogFile -Value "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ss.fffK')  $Message"
}

function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}

function Get-HttpErrorBody($ErrorRecord) {
  if ($ErrorRecord.ErrorDetails -and $ErrorRecord.ErrorDetails.Message) { return $ErrorRecord.ErrorDetails.Message }
  return $ErrorRecord.Exception.Message
}

function Quote-ProcessArgument([string]$Value) {
  if ($null -eq $Value) { return '""' }
  return '"' + ($Value -replace '"','\"') + '"'
}

if (-not (Test-Path -LiteralPath $CredentialFile)) { throw "Credential bundle not found: $CredentialFile" }
if (-not (Test-Path -LiteralPath $WorkerScript)) { throw "Worker script not found: $WorkerScript" }

$mutex = New-Object Threading.Mutex($false,'Local\DCSE_UniversalDispatchController')
$lockHeld = $false
try {
  $lockHeld = $mutex.WaitOne(0)
  if (-not $lockHeld) { Write-Log 'SKIP prior controller cycle still active'; exit 0 }

  $bundle = Import-Clixml $CredentialFile
  if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') {
    throw "Credential bundle targets wrong project: $($bundle.supabase_project_ref)"
  }
  $SupabaseUrl = [string]$bundle.SUPABASE_URL
  $ServiceKey = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
  $Headers = @{
    apikey=$ServiceKey
    Authorization="Bearer $ServiceKey"
    'Content-Type'='application/json'
    'Accept-Profile'='dcse_cp'
  }

  try {
    # Ask PostgREST/Postgres to evaluate the boolean. Windows PowerShell never
    # deserializes admitted_for_autonomous_claim for the controller decision.
    $admissions = @(Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/autonomous_dispatch_admission?select=agent_key,admission_status" -Headers $Headers)
    $admittedRows = @(Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/autonomous_dispatch_admission?admitted_for_autonomous_claim=eq.true&select=agent_key" -Headers $Headers)
    $admittedKeys = @($admittedRows | ForEach-Object { [string]$_.agent_key })
  } catch {
    Write-Log "FATAL admission view unavailable: $(Get-HttpErrorBody $_)"
    exit 2
  }

  $adapters = @(
    @{ AgentKey='claude_code'; RuntimeSurface='claude_code_windows_cli'; PreflightWhenDormant=$false; AdmissionSmoke=$false },
    @{ AgentKey='qwen_windows_cli'; RuntimeSurface='qwen_windows_cli'; PreflightWhenDormant=$true; AdmissionSmoke=$true },
    @{ AgentKey='codex'; RuntimeSurface='codex_windows_cli'; PreflightWhenDormant=$true; AdmissionSmoke=$false }
  )

  foreach ($adapter in $adapters) {
    $row = $admissions | Where-Object { $_.agent_key -eq $adapter.AgentKey } | Select-Object -First 1
    if (-not $row) {
      Write-Log "SKIP agent=$($adapter.AgentKey) no admission row"
      continue
    }

    $isAdmitted = ($admittedKeys -contains [string]$adapter.AgentKey)
    $mode = 'normal'
    $switches = @()

    if (-not $isAdmitted) {
      if (-not $adapter.PreflightWhenDormant) {
        Write-Log "SKIP agent=$($adapter.AgentKey) not admitted for autonomous claim admission_status=$($row.admission_status)"
        continue
      }
      $switches += '-PreflightOnly'
      $mode = 'preflight'
      if ($adapter.AdmissionSmoke) {
        $switches += '-AdmissionSmoke'
        $mode = 'preflight+admission-smoke'
      }
    }

    # Windows PowerShell Start-Process does not reliably preserve spaces when an
    # ArgumentList array is flattened. Build one explicitly quoted command line.
    $argLine = @(
      '-NoProfile',
      '-ExecutionPolicy Bypass',
      '-File ' + (Quote-ProcessArgument $WorkerScript),
      '-AgentKey ' + (Quote-ProcessArgument $adapter.AgentKey),
      '-RuntimeSurface ' + (Quote-ProcessArgument $adapter.RuntimeSurface),
      '-CredentialFile ' + (Quote-ProcessArgument $CredentialFile),
      '-WorkspacePath ' + (Quote-ProcessArgument $WorkspacePath),
      '-WorkerRoot ' + (Quote-ProcessArgument $WorkerRoot)
    ) -join ' '
    if ($switches.Count -gt 0) { $argLine += ' ' + ($switches -join ' ') }

    try {
      $proc = Start-Process -FilePath 'powershell.exe' -ArgumentList $argLine -WindowStyle Hidden -PassThru
      Write-Log "LAUNCHED agent=$($adapter.AgentKey) runtime=$($adapter.RuntimeSurface) mode=$mode admitted=$isAdmitted pid=$($proc.Id)"
    } catch {
      Write-Log "LAUNCH_FAILED agent=$($adapter.AgentKey) detail=$($_.Exception.Message)"
    }
  }

  Write-Log 'Cycle complete; controller did not wait for workers.'
  exit 0
}
finally {
  if ($lockHeld) { try { $mutex.ReleaseMutex() } catch {} }
  $mutex.Dispose()
}
