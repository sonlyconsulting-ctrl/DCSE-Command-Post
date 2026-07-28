#requires -Version 7.0
[CmdletBinding()]
param(
  [string]$RepoRoot = "C:\DS All Things\DCSE_Command_Center\DCSE-Command-Post",
  [string]$Branch = "chatgpt/v7-foundation-runtime-compiler",
  [string]$SupabaseUrl = "https://liwdquzuigrlgfzgmpjp.supabase.co",
  [string]$AgentId = "AGENT-CLAUDE-REVIEWER-01@STAGING",
  [string]$TaskName = "DCSE-Communication-Worker",
  [string]$CredentialPath = "$env:ProgramData\DCSE\worker-credentials.clixml",
  [string]$ReceiptPath = "$env:ProgramData\DCSE\receipts\COMMUNICATION_OPERATIONAL_GATE_001.json"
)

$ErrorActionPreference = 'Stop'

function Assert-Administrator {
  $principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
  if (-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    throw 'Run this script from PowerShell 7 as Administrator.'
  }
}

function Read-RequiredSecret([string]$Prompt) {
  $value = Read-Host $Prompt -AsSecureString
  if ($value.Length -eq 0) { throw "$Prompt is required." }
  return $value
}

function ConvertTo-PlainText([Security.SecureString]$Secure) {
  $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secure)
  try { [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
  finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
}

function Save-WorkerCredentials {
  $dir = Split-Path $CredentialPath -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $anon = Read-RequiredSecret 'Supabase anon key'
  $enrollment = Read-RequiredSecret 'Worker enrollment secret'
  $anthropic = Read-RequiredSecret 'Anthropic API key'
  [pscustomobject]@{
    SupabaseAnonKey = $anon
    WorkerEnrollmentSecret = $enrollment
    AnthropicApiKey = $anthropic
    AgentId = $AgentId
    SupabaseUrl = $SupabaseUrl
    CreatedAt = (Get-Date).ToUniversalTime().ToString('o')
  } | Export-Clixml -Path $CredentialPath
  icacls $CredentialPath /inheritance:r /grant:r "$env:USERNAME:(R,W)" | Out-Null
}

function Load-WorkerCredentials {
  if (-not (Test-Path $CredentialPath)) { Save-WorkerCredentials }
  Import-Clixml -Path $CredentialPath
}

function Invoke-TokenTest($Creds) {
  $body = @{
    agent_id = $AgentId
    enrollment_secret = ConvertTo-PlainText $Creds.WorkerEnrollmentSecret
  } | ConvertTo-Json
  $headers = @{ apikey = ConvertTo-PlainText $Creds.SupabaseAnonKey; Authorization = "Bearer $(ConvertTo-PlainText $Creds.SupabaseAnonKey)" }
  $uri = "$SupabaseUrl/functions/v1/v7-worker-token"
  $resp = Invoke-RestMethod -Method Post -Uri $uri -Headers $headers -ContentType 'application/json' -Body $body
  if (-not $resp.access_token) { throw 'Worker token issuance failed.' }
  $resp.access_token
}

function Ensure-Repository {
  if (-not (Test-Path "$RepoRoot\.git")) { throw "Repository not found: $RepoRoot" }
  Push-Location $RepoRoot
  try {
    git fetch origin --prune
    git checkout $Branch
    git pull --ff-only origin $Branch
    if ($LASTEXITCODE -ne 0) { throw 'Git synchronization failed.' }
  } finally { Pop-Location }
}

function Ensure-Dependencies {
  Push-Location $RepoRoot
  try {
    if (Test-Path package-lock.json) { npm ci } else { npm install }
    if ($LASTEXITCODE -ne 0) { throw 'npm dependency installation failed.' }
  } finally { Pop-Location }
}

function Write-Launcher($Creds) {
  $dcseDir = "$env:ProgramData\DCSE"
  New-Item -ItemType Directory -Force -Path $dcseDir | Out-Null
  $launcher = Join-Path $dcseDir 'Start-DCSECommunicationWorker.ps1'
  $content = @"
`$ErrorActionPreference = 'Stop'
`$c = Import-Clixml '$CredentialPath'
function P([Security.SecureString]`$s){ `$p=[Runtime.InteropServices.Marshal]::SecureStringToBSTR(`$s); try{[Runtime.InteropServices.Marshal]::PtrToStringBSTR(`$p)}finally{[Runtime.InteropServices.Marshal]::ZeroFreeBSTR(`$p)} }
`$env:SUPABASE_URL = '$SupabaseUrl'
`$env:SUPABASE_ANON_KEY = P `$c.SupabaseAnonKey
`$env:WORKER_AGENT_ID = '$AgentId'
`$env:WORKER_ENROLLMENT_SECRET = P `$c.WorkerEnrollmentSecret
`$env:ANTHROPIC_API_KEY = P `$c.AnthropicApiKey
`$env:WORKER_POLL_MS = '30000'
`$env:WORKER_HEARTBEAT_MS = '15000'
Set-Location '$RepoRoot'
node workers/claude-reviewer-operational.js *>> '$env:ProgramData\DCSE\communication-worker.log'
"@
  Set-Content -Path $launcher -Value $content -Encoding UTF8
  $launcher
}

function Install-ScheduledTask([string]$Launcher) {
  $action = New-ScheduledTaskAction -Execute 'pwsh.exe' -Argument "-NoLogo -NoProfile -ExecutionPolicy Bypass -File `"$Launcher`""
  $trigger1 = New-ScheduledTaskTrigger -AtStartup
  $trigger2 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
  $trigger2.Repetition.Interval = 'PT5M'
  $settings = New-ScheduledTaskSettingsSet -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Days 3650)
  $principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType S4U -RunLevel Highest
  Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger @($trigger1,$trigger2) -Settings $settings -Principal $principal -Force | Out-Null
  Start-ScheduledTask -TaskName $TaskName
}

function Wait-ForHeartbeat([int]$Seconds = 90) {
  $deadline = (Get-Date).AddSeconds($Seconds)
  do {
    Start-Sleep -Seconds 5
    $log = "$env:ProgramData\DCSE\communication-worker.log"
    if ((Test-Path $log) -and (Select-String -Path $log -Pattern 'heartbeat' -Quiet)) { return $true }
  } while ((Get-Date) -lt $deadline)
  return $false
}

function Write-Receipt([hashtable]$Data) {
  $dir = Split-Path $ReceiptPath -Parent
  New-Item -ItemType Directory -Force -Path $dir | Out-Null
  $Data | ConvertTo-Json -Depth 8 | Set-Content -Path $ReceiptPath -Encoding UTF8
}

Assert-Administrator
Ensure-Repository
Ensure-Dependencies
$creds = Load-WorkerCredentials
$null = Invoke-TokenTest $creds
$launcher = Write-Launcher $creds
Install-ScheduledTask $launcher
$heartbeat = Wait-ForHeartbeat

$receipt = [ordered]@{
  gate_id = 'COMMUNICATION_OPERATIONAL_GATE_001'
  executed_at = (Get-Date).ToUniversalTime().ToString('o')
  host = $env:COMPUTERNAME
  user = $env:USERNAME
  branch = $Branch
  supabase_url = $SupabaseUrl
  agent_id = $AgentId
  scheduled_task = $TaskName
  credential_file = $CredentialPath
  token_test = 'PASS'
  scheduled_task_installed = $true
  heartbeat_observed_in_log = $heartbeat
  secrets_logged = $false
  status = $(if ($heartbeat) { 'READY_FOR_DB_CYCLE_TEST' } else { 'STOP_GATE_NO_HEARTBEAT' })
}
Write-Receipt $receipt
Write-Host "Receipt: $ReceiptPath"
if (-not $heartbeat) { throw 'Worker installed, but no heartbeat was observed in the local log.' }
Write-Host 'B1 credential injection and B5 durable host installation completed. Proceed with two correlated DB cycles and restart verification.'
