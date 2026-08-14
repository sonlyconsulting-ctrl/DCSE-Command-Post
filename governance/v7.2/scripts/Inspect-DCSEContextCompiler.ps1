[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateScript({ Test-Path -LiteralPath $_ -PathType Leaf })]
    [string]$LogPath,

    [switch]$Follow,
    [switch]$Summary,
    [string]$Phase,
    [string]$TaskId
)

$requiredPhases = @(
    'TASK_DECLARATION',
    'AUTHORITY_RESOLUTION',
    'LANE_RESOLUTION',
    'DIRECT_RULE_SELECTION',
    'TRANSITIVE_DEPENDENCY',
    'FIREWALL_DECISION',
    'CONFLICT_DISPOSITION',
    'CLOSURE_COMPLETE',
    'PACKET_BUILD',
    'RUNTIME_PREFLIGHT',
    'EXECUTION_DECISION'
)

function Convert-CompilerLine {
    param([string]$Line)
    if ([string]::IsNullOrWhiteSpace($Line)) { return }
    try {
        $event = $Line | ConvertFrom-Json -ErrorAction Stop
    }
    catch {
        [pscustomobject]@{
            timestamp = $null
            task_id = $null
            phase = 'INVALID_JSON'
            decision = 'FAIL'
            source_id = $null
            rule_id = $null
            reason = $_.Exception.Message
        }
        return
    }

    if ($TaskId -and $event.task_id -ne $TaskId) { return }
    if ($Phase -and $event.phase -ne $Phase) { return }

    [pscustomobject]@{
        timestamp = $event.timestamp
        task_id = $event.task_id
        packet_id = $event.context_packet_id
        phase = $event.phase
        decision = $event.decision
        status = $event.status
        source_id = $event.source_id
        rule_id = $event.rule_id
        inclusion_basis = $event.inclusion_basis
        reason = $event.reason
    }
}

if ($Follow) {
    Get-Content -LiteralPath $LogPath -Wait | ForEach-Object {
        Convert-CompilerLine -Line $_
    } | Format-Table -AutoSize -Wrap
    return
}

$events = @(Get-Content -LiteralPath $LogPath | ForEach-Object {
    Convert-CompilerLine -Line $_
})

if ($Summary) {
    $present = @($events.phase | Where-Object { $_ } | Sort-Object -Unique)
    $missing = @($requiredPhases | Where-Object { $_ -notin $present })
    [pscustomobject]@{
        LogPath = (Resolve-Path -LiteralPath $LogPath).Path
        EventCount = $events.Count
        FailedEvents = @($events | Where-Object decision -eq 'FAIL').Count
        StopEvents = @($events | Where-Object decision -eq 'STOP').Count
        UnknownEvents = @($events | Where-Object status -eq 'UNKNOWN').Count
        MissingRequiredPhases = ($missing -join ', ')
        Preflight = (($events | Where-Object phase -eq 'RUNTIME_PREFLIGHT' | Select-Object -Last 1).decision)
        ExecutionDecision = (($events | Where-Object phase -eq 'EXECUTION_DECISION' | Select-Object -Last 1).decision)
    } | Format-List
    return
}

$events | Format-Table -AutoSize -Wrap
