# DCSE V7.1 Claude Poller Runtime Sync
#
# Purpose:
#   Replace the stale Windows worker copy with the exact allowlist-free poller
#   promoted to main at commit d5ead62093982632b7612e4748c182a036220314,
#   restart the existing scheduled task, and verify that an already assigned
#   test task becomes claimable.
#
# This script does not switch the user's working branch, expose credentials,
# create a replacement poller, or bypass task authorization.

[CmdletBinding()]
param(
  [string]$PollerTaskName = 'DCSE_ClaudeCode_Poller',
  [string]$TargetPollerPath = 'C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS\claude_code_poller.ps1',
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [string]$TestTaskKey = 'TRIB-MSI2KCUN',
  [int]$ClaimWaitSeconds = 120
)

$ErrorActionPreference = 'Stop'
$CanonicalCommit = 'd5ead62093982632b7612e4748c182a036220314'
$CanonicalBlobSha = 'daae619a3bc71016fede9cdd29341b51ac68356b'
$CanonicalUrl = "https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/$CanonicalCommit/tribunal/v7/runtime-evidence/claude_code_poller.ps1"
$Timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$TargetDirectory = Split-Path -Parent $TargetPollerPath
$BackupPath = "$TargetPollerPath.pre_v71_sync_$Timestamp.bak"
$TempPath = Join-Path $env:TEMP "dcse_claude_code_poller_$Timestamp.ps1"
$ReceiptPath = Join-Path $TargetDirectory "V7_1_POLLER_RUNTIME_SYNC_RECEIPT_$Timestamp.json"

function Get-GitBlobSha1([byte[]]$Bytes) {
  $header = [Text.Encoding]::ASCII.GetBytes("blob $($Bytes.Length)`0")
  $combined = New-Object byte[] ($header.Length + $Bytes.Length)
  [Array]::Copy($header, 0, $combined, 0, $header.Length)
  [Array]::Copy($Bytes, 0, $combined, $header.Length, $Bytes.Length)
  $sha = [Security.Cryptography.SHA1]::Create()
  try {
    return (($sha.ComputeHash($combined) | ForEach-Object { $_.ToString('x2') }) -join '')
  } finally {
    $sha.Dispose()
  }
}

function SecureToPlain($Value) {
  if ($Value -is [Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Value)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$Value
}

function Get-ExistingBlobSha([string]$Path) {
  if (-not (Test-Path $Path)) { return $null }
  return Get-GitBlobSha1 ([IO.File]::ReadAllBytes($Path))
}

if (-not (Test-Path $CredentialFile)) {
  throw "Credential bundle not found: $CredentialFile"
}
if (-not (Test-Path $TargetDirectory)) {
  throw "Target directory not found: $TargetDirectory"
}

$beforeBlobSha = Get-ExistingBlobSha $TargetPollerPath
Invoke-WebRequest -Uri $CanonicalUrl -OutFile $TempPath -UseBasicParsing
$downloadedBytes = [IO.File]::ReadAllBytes($TempPath)
$downloadedBlobSha = Get-GitBlobSha1 $downloadedBytes
if ($downloadedBlobSha -ne $CanonicalBlobSha) {
  throw "Downloaded poller blob mismatch. Expected $CanonicalBlobSha, got $downloadedBlobSha"
}

$task = Get-ScheduledTask -TaskName $PollerTaskName -ErrorAction Stop
try { Stop-ScheduledTask -TaskName $PollerTaskName -ErrorAction SilentlyContinue } catch {}

if (Test-Path $TargetPollerPath) {
  Copy-Item -Path $TargetPollerPath -Destination $BackupPath -Force
}
Copy-Item -Path $TempPath -Destination $TargetPollerPath -Force
$afterBlobSha = Get-ExistingBlobSha $TargetPollerPath
if ($afterBlobSha -ne $CanonicalBlobSha) {
  if (Test-Path $BackupPath) { Copy-Item $BackupPath $TargetPollerPath -Force }
  throw "Installed poller blob mismatch. Rolled back. Expected $CanonicalBlobSha, got $afterBlobSha"
}

# Remove only the test key from local idempotency state. Preserve every other
# processed or retry record.
$statePath = Join-Path $TargetDirectory 'poller_state.json'
if (Test-Path $statePath) {
  try {
    $state = Get-Content $statePath -Raw | ConvertFrom-Json
    if ($state.processed -and $state.processed.PSObject.Properties.Name -contains $TestTaskKey) {
      $state.processed.PSObject.Properties.Remove($TestTaskKey)
    }
    if ($state.attempts -and $state.attempts.PSObject.Properties.Name -contains $TestTaskKey) {
      $state.attempts.PSObject.Properties.Remove($TestTaskKey)
    }
    $state | ConvertTo-Json -Depth 20 | Set-Content $statePath
  } catch {
    throw "Poller installed, but local state correction failed: $($_.Exception.Message)"
  }
}

Enable-ScheduledTask -TaskName $PollerTaskName | Out-Null
Start-ScheduledTask -TaskName $PollerTaskName

$bundle = Import-Clixml $CredentialFile
$SupabaseUrl = [string]$bundle.SUPABASE_URL
$ServiceKey = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
if ($bundle.supabase_project_ref -and $bundle.supabase_project_ref -ne 'nevgdyfpxdaloacuutal') {
  throw "Credential bundle targets the wrong Supabase project."
}
$Headers = @{
  apikey = $ServiceKey
  Authorization = "Bearer $ServiceKey"
  'Content-Type' = 'application/json'
  'Accept-Profile' = 'dcse_cp'
}

$deadline = (Get-Date).AddSeconds($ClaimWaitSeconds)
$taskRow = $null
$assignmentRow = $null
$claimDisposition = 'CLAIM_PENDING'
do {
  $taskRows = Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_tasks?task_key=eq.$TestTaskKey&select=id,status,assigned_agent_id,updated_at" -Headers $Headers
  if ($taskRows -and $taskRows.Count -gt 0) {
    $taskRow = $taskRows[0]
    $assignmentRows = Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_task_assignments?task_id=eq.$($taskRow.id)&select=id,status,result_payload,updated_at" -Headers $Headers
    if ($assignmentRows -and $assignmentRows.Count -gt 0) {
      $assignmentRow = $assignmentRows[0]
      if ($assignmentRow.status -in @('running','completed','blocked','needs_review','approved')) {
        $claimDisposition = 'CLAIM_OBSERVED'
        break
      }
    }
  }
  Start-Sleep -Seconds 5
} while ((Get-Date) -lt $deadline)

$receipt = [ordered]@{
  receipt_type = 'V7_1_POLLER_RUNTIME_SYNC'
  generated_at = (Get-Date).ToUniversalTime().ToString('o')
  host = $env:COMPUTERNAME
  scheduled_task = $PollerTaskName
  target_path = $TargetPollerPath
  canonical_commit = $CanonicalCommit
  canonical_git_blob_sha = $CanonicalBlobSha
  before_git_blob_sha = $beforeBlobSha
  installed_git_blob_sha = $afterBlobSha
  backup_path = if (Test-Path $BackupPath) { $BackupPath } else { $null }
  test_task_key = $TestTaskKey
  task_status = $taskRow.status
  assignment_status = $assignmentRow.status
  assignment_id = $assignmentRow.id
  disposition = $claimDisposition
  rollback = "Stop $PollerTaskName; restore $BackupPath to $TargetPollerPath; restart task."
  secrets_exposed = $false
}
$receipt | ConvertTo-Json -Depth 10 | Set-Content $ReceiptPath

if ($taskRow) {
  $eventHeaders = $Headers.Clone()
  $eventHeaders['Prefer'] = 'return=minimal'
  $eventBody = @{
    task_id = $taskRow.id
    event_type = 'host_sync'
    actor_label = 'V7.1 Poller Runtime Sync'
    event_summary = "Canonical poller installed; $claimDisposition"
    event_payload = @{
      canonical_commit = $CanonicalCommit
      canonical_git_blob_sha = $CanonicalBlobSha
      before_git_blob_sha = $beforeBlobSha
      installed_git_blob_sha = $afterBlobSha
      assignment_status = $assignmentRow.status
      receipt_path = $ReceiptPath
    }
  } | ConvertTo-Json -Depth 10 -Compress
  Invoke-RestMethod -Method Post -Uri "$SupabaseUrl/rest/v1/agent_task_events" -Headers $eventHeaders -Body $eventBody | Out-Null
}

Remove-Item $TempPath -Force -ErrorAction SilentlyContinue
$receipt | ConvertTo-Json -Depth 10

if ($claimDisposition -ne 'CLAIM_OBSERVED') { exit 2 }
exit 0
