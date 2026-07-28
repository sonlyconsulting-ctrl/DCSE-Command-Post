param(
  [Parameter(Mandatory=$true)][string]$RepoRoot,
  [Parameter(Mandatory=$true)][string]$SupabaseUrl,
  [Parameter(Mandatory=$true)][string]$SupabaseAnonKey,
  [Parameter(Mandatory=$true)][string]$WorkerAgentId,
  [Parameter(Mandatory=$true)][SecureString]$WorkerEnrollmentSecret,
  [Parameter(Mandatory=$true)][SecureString]$AnthropicApiKey,
  [string]$Model = 'claude-sonnet-4-20250514',
  [string]$TaskName = 'DCSE-V7-Communication-Worker'
)

$ErrorActionPreference = 'Stop'
$worker = Join-Path $RepoRoot 'workers\claude-reviewer-operational.js'
if (-not (Test-Path $worker)) { throw "Worker not found: $worker" }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Node.js is required.' }

$base = Join-Path $env:ProgramData 'DCSE\v7-worker'
$logDir = Join-Path $base 'logs'
New-Item -ItemType Directory -Force -Path $base,$logDir | Out-Null

function Unsecure([SecureString]$s) {
  $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($s)
  try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
  finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

$secret = Unsecure $WorkerEnrollmentSecret
$apiKey = Unsecure $AnthropicApiKey
$envPath = Join-Path $base 'worker.env.json'
$cfg = [ordered]@{
  SUPABASE_URL = $SupabaseUrl
  SUPABASE_ANON_KEY = $SupabaseAnonKey
  WORKER_AGENT_ID = $WorkerAgentId
  WORKER_ENROLLMENT_SECRET = $secret
  ANTHROPIC_API_KEY = $apiKey
  CLAUDE_REVIEWER_MODEL = $Model
  WORKER_POLL_MS = '30000'
  WORKER_HEARTBEAT_MS = '15000'
}
$cfg | ConvertTo-Json | Set-Content -Encoding UTF8 $envPath

# Restrict the credential file to SYSTEM, Administrators, and the current account.
icacls $envPath /inheritance:r | Out-Null
icacls $envPath /grant:r "SYSTEM:(F)" "Administrators:(F)" "$env:USERNAME:(R)" | Out-Null

$runner = Join-Path $base 'run-worker.ps1'
@"
`$ErrorActionPreference = 'Stop'
`$cfg = Get-Content '$envPath' -Raw | ConvertFrom-Json
`$cfg.PSObject.Properties | ForEach-Object { [Environment]::SetEnvironmentVariable(`$_.Name, [string]`$_.Value, 'Process') }
`$log = Join-Path '$logDir' ('worker-' + (Get-Date -Format 'yyyyMMdd') + '.log')
Set-Location '$RepoRoot'
while (`$true) {
  try {
    & node '$worker' *>> `$log
  } catch {
    (`$(Get-Date -Format o) + ' supervisor_error ' + `$_) | Add-Content `$log
  }
  Start-Sleep -Seconds 10
}
"@ | Set-Content -Encoding UTF8 $runner

$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$runner`""
$triggerStartup = New-ScheduledTaskTrigger -AtStartup
$triggerLogin = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero)
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($triggerStartup,$triggerLogin) -Settings $settings -Principal $principal -Force | Out-Null
Start-ScheduledTask -TaskName $TaskName
Start-Sleep -Seconds 5

$task = Get-ScheduledTask -TaskName $TaskName
$info = Get-ScheduledTaskInfo -TaskName $TaskName
[pscustomobject]@{
  TaskName = $TaskName
  State = $task.State
  LastRunTime = $info.LastRunTime
  LastTaskResult = $info.LastTaskResult
  Worker = $worker
  CredentialFile = $envPath
  LogDirectory = $logDir
}
