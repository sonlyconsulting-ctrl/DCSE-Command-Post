# DCSE v7.1 Poller Health Monitor
#
# Separate, independent Windows Scheduled Task from DCSE_ClaudeCode_Poller
# itself -- the whole point is to keep watching even if the poller task gets
# disabled again (that exact failure mode caused a ~5 day / 7,585-missed-run
# outage before this monitor existed; see tribunal/v7/EVIDENCE_AND_CLASSIFICATION_REPORT.md).
#
# Runs every 5 minutes. Two checks:
#   1. Is DCSE_ClaudeCode_Poller Enabled? If not, re-enable it (self-heal the
#      exact failure already seen once) and log a SELF_HEAL line.
#   2. Is the claude_code heartbeat in dcse_cp.agent_heartbeats fresh (<5 min)?
#      If not, log a WARNING line and a receipt-style event tied to the poller
#      hardening task, so it's visible in Supabase, not just a local file
#      nobody is looking at.
#
# Credential handling matches claude_code_poller.ps1 exactly: DPAPI CurrentUser
# bundle, only SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY read into this
# process's own memory for the duration of the check, never logged.

[CmdletBinding()]
param(
  [string]$CredentialFile = 'C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml',
  [int]$StalenessThresholdSeconds = 300
)

$ErrorActionPreference = 'Stop'
$LogFile = Join-Path $PSScriptRoot 'poller_health_monitor_log.txt'
$PollerTaskName = 'DCSE_ClaudeCode_Poller'
$PollerHardeningTaskId = '6d2c4d6d-4617-40ef-85d7-7312142de609'
$ClaudeCodeAgentId = '28bf7e25-924c-47b6-aa47-b21f8b52c16f'

function Write-Log($msg) {
  $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')Z  $msg"
  Add-Content -Path $LogFile -Value $line
}

# ---- 1. Scheduled task state --------------------------------------------
$selfHealed = $false
$taskForceStarted = $false
try {
  $task = Get-ScheduledTask -TaskName $PollerTaskName -ErrorAction Stop
  if ($task.State -eq 'Disabled') {
    Enable-ScheduledTask -TaskName $PollerTaskName | Out-Null
    $selfHealed = $true
    Write-Log "SELF_HEAL: $PollerTaskName was Disabled, re-enabled automatically."
  }
  # Additional restore: if task is enabled but not currently running (Ready state)
  # and heartbeat is stale, force-start a new cycle immediately.
  # Covers the case where the poller finished but left a degraded heartbeat
  # (e.g. a long claude -p run completed but no subsequent cycle fired yet).
  if ($task.State -eq 'Ready') {
    # We set $taskForceStarted = $true here tentatively; actual force-start
    # happens below after the heartbeat staleness check confirms it's needed.
    $taskReadyForForceStart = $true
  }
} catch {
  Write-Log "ERROR: could not query/enable scheduled task $PollerTaskName -- $($_.Exception.Message)"
}

# ---- 2. Heartbeat staleness ------------------------------------------------
if (-not (Test-Path $CredentialFile)) {
  Write-Log "FATAL: credential bundle not found at $CredentialFile."
  exit 1
}
$bundle = Import-Clixml $CredentialFile
function SecureToPlain($v) {
  if ($v -is [System.Security.SecureString]) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($v)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
  }
  return [string]$v
}
$SupabaseUrl = $bundle.SUPABASE_URL
$ServiceKey  = SecureToPlain $bundle.SUPABASE_SERVICE_ROLE_KEY
$Headers = @{ 'apikey' = $ServiceKey; 'Authorization' = "Bearer $ServiceKey"; 'Content-Type' = 'application/json' }

try {
  $h = $Headers.Clone(); $h['Accept-Profile'] = 'dcse_cp'
  $rows = Invoke-RestMethod -Method Get -Uri "$SupabaseUrl/rest/v1/agent_heartbeats?agent_id=eq.$ClaudeCodeAgentId&select=last_seen_at,heartbeat_status" -Headers $h
  if (-not $rows -or $rows.Count -eq 0) {
    Write-Log "WARNING: no heartbeat row found for claude_code at all."
  } else {
    $lastSeen = [DateTime]::Parse($rows[0].last_seen_at).ToUniversalTime()
    $stale = (Get-Date).ToUniversalTime() - $lastSeen
    if ($stale.TotalSeconds -gt $StalenessThresholdSeconds) {
      Write-Log "WARNING: heartbeat stale by $([int]$stale.TotalSeconds)s (threshold ${StalenessThresholdSeconds}s). self_healed_task=$selfHealed"

      # Force-start the poller if it is in Ready state (enabled but not running).
      # This is the primary continuous-operation restore path: the poller ran,
      # finished (or timed out), but Task Scheduler hasn't fired the next 60-second
      # cycle yet, leaving the heartbeat stale. Force-starting kicks off a fresh
      # cycle immediately rather than waiting up to 60s for the scheduler.
      if ($taskReadyForForceStart) {
        try {
          Start-ScheduledTask -TaskName $PollerTaskName
          $taskForceStarted = $true
          Write-Log "SELF_HEAL: force-started $PollerTaskName (was Ready, heartbeat stale)."
        } catch {
          Write-Log "ERROR: force-start of $PollerTaskName failed -- $($_.Exception.Message)"
        }
      }

      $rpcH = $Headers.Clone(); $rpcH['Content-Profile'] = 'dcse_cp'
      $eventBody = @{
        p_agent_key = 'claude_code'; p_task_key = $null; p_status = 'degraded'
        p_capability_status = @{
          poller_monitor      = 'stale_heartbeat_detected'
          staleness_seconds   = [int]$stale.TotalSeconds
          self_healed         = $selfHealed
          force_started       = $taskForceStarted
        }
        p_notes = "health monitor: heartbeat stale $([int]$stale.TotalSeconds)s, self_healed=$selfHealed, force_started=$taskForceStarted"
      } | ConvertTo-Json -Compress
      try { Invoke-RestMethod -Method Post -Uri "$SupabaseUrl/rest/v1/rpc/agent_heartbeat" -Headers $rpcH -Body $eventBody | Out-Null } catch {}
    } else {
      Write-Log "OK: heartbeat fresh ($([int]$stale.TotalSeconds)s old)."
    }
  }
} catch {
  Write-Log "ERROR calling Supabase: $($_.Exception.Message)"
}
