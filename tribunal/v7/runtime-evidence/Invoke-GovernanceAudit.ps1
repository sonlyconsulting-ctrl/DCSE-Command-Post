param(
    [string]$RepoRoot = "C:\DS All Things\DCSE_Governance_Audit",
    [string]$ReportOutput = "C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\tribunal\v7\GOVERNANCE_STRUCTURAL_AUDIT_REPORT.md",
    [switch]$DownloadFirst
)

$ErrorActionPreference = 'Stop'

if ($DownloadFirst) {
    if (Test-Path $RepoRoot) { Remove-Item -Recurse -Force $RepoRoot }
    git clone --branch governance/v7.1-owned-product-harness --single-branch `
        https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post.git $RepoRoot
}

if (-not (Test-Path $RepoRoot)) {
    Write-Error "Repo root not found: $RepoRoot"
    exit 1
}

# Zone rules
$ProhibitedInZone = @{
    'execution' = @('PROMOTED','AUTHORITATIVE')
    'evidence'  = @('PROMOTED','AUTHORITATIVE')
}

$ProhibitedStrings = @{
    'execution' = @('AUTHORITATIVE_UNTIL_FURTHER_NOTICE')
    'evidence'  = @('AUTHORITATIVE_UNTIL_FURTHER_NOTICE')
}

function Get-ZoneFromPath([string]$rel) {
    $p = $rel.Replace('\','/').ToLower()
    if     ($p -match 'tribunal/v7/')                          { return 'evidence' }
    elseif ($p -match 'governance/v7\.1/(execution|instructions)/') { return 'execution' }
    elseif ($p -match 'governance/v7\.1/source/')              { return 'source' }
    elseif ($p -match 'governance/v7\.1/')                     { return 'authority' }
    else                                                       { return 'other' }
}

function Get-Frontmatter([string]$path) {
    $raw = Get-Content $path -Raw -ErrorAction SilentlyContinue
    if (-not $raw -or $raw -notmatch '(?s)^---\r?\n(.+?)\r?\n---') { return $null }
    $fm = @{}
    foreach ($line in ($Matches[1] -split "`n")) {
        if ($line -match '^\s*([\w_]+)\s*:\s*(.+)$') {
            $fm[$Matches[1].Trim()] = $Matches[2].Trim()
        }
    }
    return $fm
}

$ScanPaths = @(
    (Join-Path $RepoRoot 'governance\v7.1'),
    (Join-Path $RepoRoot 'tribunal\v7')
)

$Files = @()
foreach ($sp in $ScanPaths) {
    if (Test-Path $sp) {
        $Files += Get-ChildItem -Path $sp -Recurse -Include '*.md','*.yaml','*.yml','*.json' |
                  Where-Object { -not $_.PSIsContainer }
    }
}

$AllResults  = @()
$TotalPass   = 0
$TotalFail   = 0
$TotalWarn   = 0

foreach ($File in $Files) {
    $RelPath = $File.FullName.Substring($RepoRoot.Length).TrimStart('\','/')
    $Zone    = Get-ZoneFromPath $RelPath
    if ($Zone -eq 'other') { continue }

    $Content = Get-Content $File.FullName -Raw -ErrorAction SilentlyContinue
    $FM      = Get-Frontmatter $File.FullName
    $Checks  = @()
    $FP = 0; $FF = 0; $FW = 0

    # C1 - Frontmatter present
    if ($FM -ne $null) {
        $Checks += @{ N=1; Label='Frontmatter present'; Status='PASS'; Detail='' }; $FP++
    } else {
        $Checks += @{ N=1; Label='Frontmatter present'; Status='FAIL'; Detail='No --- block. Add dcse_zone, dcse_authority_level, dcse_promoted_by.' }; $FF++
    }

    # C2 - dcse_zone declared and matches path
    if ($FM -and $FM.ContainsKey('dcse_zone')) {
        $dz = $FM['dcse_zone']
        if ($dz -eq $Zone) {
            $Checks += @{ N=2; Label='dcse_zone matches path zone'; Status='PASS'; Detail="zone: $dz" }; $FP++
        } else {
            $Checks += @{ N=2; Label='dcse_zone matches path zone'; Status='FAIL'; Detail="Declared=$dz PathZone=$Zone mismatch" }; $FF++
        }
    } elseif ($FM -ne $null) {
        $Checks += @{ N=2; Label='dcse_zone declared'; Status='FAIL'; Detail='dcse_zone field missing' }; $FF++
    } else {
        $Checks += @{ N=2; Label='dcse_zone declared'; Status='SKIP'; Detail='No frontmatter' }
    }

    # C3 - dcse_authority_level declared
    $AuthLevel = $null
    if ($FM -and $FM.ContainsKey('dcse_authority_level')) {
        $AuthLevel = $FM['dcse_authority_level']
        $Checks += @{ N=3; Label='dcse_authority_level declared'; Status='PASS'; Detail="level: $AuthLevel" }; $FP++
    } elseif ($FM -ne $null) {
        $Checks += @{ N=3; Label='dcse_authority_level declared'; Status='FAIL'; Detail='dcse_authority_level missing' }; $FF++
    } else {
        $Checks += @{ N=3; Label='dcse_authority_level declared'; Status='SKIP'; Detail='No frontmatter' }
    }

    # C4 - Zone/authority level consistency
    if ($AuthLevel -and $ProhibitedInZone.ContainsKey($Zone)) {
        if ($ProhibitedInZone[$Zone] -contains $AuthLevel) {
            $Checks += @{ N=4; Label='Zone/authority consistency'; Status='FAIL'; Detail="$AuthLevel prohibited in $Zone zone" }; $FF++
        } else {
            $Checks += @{ N=4; Label='Zone/authority consistency'; Status='PASS'; Detail='' }; $FP++
        }
    } elseif ($AuthLevel) {
        $Checks += @{ N=4; Label='Zone/authority consistency'; Status='PASS'; Detail='' }; $FP++
    } else {
        $Checks += @{ N=4; Label='Zone/authority consistency'; Status='SKIP'; Detail='No authority level' }
    }

    # C5 - PROMOTED requires promotion fields
    if ($AuthLevel -eq 'PROMOTED') {
        $missing = @()
        if (-not ($FM.ContainsKey('dcse_promoted_by')))    { $missing += 'dcse_promoted_by' }
        if (-not ($FM.ContainsKey('dcse_promotion_date'))) { $missing += 'dcse_promotion_date' }
        if ($missing.Count -eq 0) {
            $Checks += @{ N=5; Label='PROMOTED has promotion fields'; Status='PASS'; Detail='' }; $FP++
        } else {
            $Checks += @{ N=5; Label='PROMOTED has promotion fields'; Status='FAIL'; Detail="Missing: $($missing -join ', ')" }; $FF++
        }
    } else {
        $Checks += @{ N=5; Label='PROMOTED has promotion fields'; Status='PASS'; Detail='Not PROMOTED - not required' }; $FP++
    }

    # C6 - Internal version contradiction
    if ($Content -match 'Status:\s*CANDIDATE PENDING') {
        if ($FM -and $FM.ContainsKey('dcse_v71_adoption_note')) {
            $Checks += @{ N=6; Label='Internal version contradiction'; Status='PASS'; Detail='Adoption note overrides internal CANDIDATE status' }; $FP++
        } else {
            $Checks += @{ N=6; Label='Internal version contradiction'; Status='FAIL'; Detail='File declares CANDIDATE PENDING with no V7.1 adoption override in frontmatter' }; $FF++
        }
    } else {
        $Checks += @{ N=6; Label='Internal version contradiction'; Status='PASS'; Detail='' }; $FP++
    }

    # C7 - Prohibited authority strings
    $found = @()
    if ($ProhibitedStrings.ContainsKey($Zone) -and $Content) {
        foreach ($pat in $ProhibitedStrings[$Zone]) {
            if ($Content -match $pat) { $found += $pat }
        }
    }
    if ($found.Count -gt 0) {
        $Checks += @{ N=7; Label='No prohibited authority strings'; Status='FAIL'; Detail="Found: $($found -join '; ')" }; $FF++
    } else {
        $Checks += @{ N=7; Label='No prohibited authority strings'; Status='PASS'; Detail='' }; $FP++
    }

    # C8 - Master Profile reference (authority zone non-MP files only)
    if ($Zone -eq 'authority' -and $File.Extension -eq '.md') {
        if ($File.Name -match 'Master_Profile') {
            $Checks += @{ N=8; Label='Master Profile reference'; Status='PASS'; Detail='This IS the Master Profile' }; $FP++
        } elseif ($Content -match 'Master.Profile|DCSE_Master_Profile') {
            $Checks += @{ N=8; Label='Master Profile reference'; Status='PASS'; Detail='' }; $FP++
        } else {
            $Checks += @{ N=8; Label='Master Profile reference'; Status='WARN'; Detail='Authority-zone file has no Master Profile reference - verify subordination' }; $FW++
        }
    }

    $TotalPass += $FP; $TotalFail += $FF; $TotalWarn += $FW

    $Status = if ($FF -gt 0) { 'NON-PASS' } elseif ($FW -gt 0) { 'WARN' } else { 'PASS' }

    $AllResults += [PSCustomObject]@{
        File    = $RelPath
        Zone    = $Zone
        Checks  = $Checks
        Pass    = $FP
        Fail    = $FF
        Warn    = $FW
        Status  = $Status
    }
}

# Build markdown report
$lines = [System.Collections.Generic.List[string]]::new()
$RunDate = (Get-Date).ToString('yyyy-MM-dd HH:mm')
$NPCount = ($AllResults | Where-Object Status -eq 'NON-PASS').Count
$WNCount = ($AllResults | Where-Object Status -eq 'WARN').Count
$PSCount = ($AllResults | Where-Object Status -eq 'PASS').Count

$lines.Add("# DCSE Governance Structural Audit Report")
$lines.Add("**Run:** $RunDate")
$lines.Add("**Repo:** $RepoRoot")
$lines.Add("**Branch:** governance/v7.1-owned-product-harness (local clone)")
$lines.Add("**Files scanned:** $($AllResults.Count)")
$lines.Add("**Check totals:** PASS=$TotalPass  FAIL=$TotalFail  WARN=$TotalWarn")
$lines.Add("**File totals:** PASS=$PSCount  NON-PASS=$NPCount  WARN=$WNCount")
$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## Summary Table")
$lines.Add("")
$lines.Add("| Status | Zone | File |")
$lines.Add("|---|---|---|")
foreach ($r in ($AllResults | Sort-Object Status,Zone,File)) {
    $lines.Add("| $($r.Status) | $($r.Zone) | $($r.File) |")
}
$lines.Add("")
$lines.Add("---")
$lines.Add("")
$lines.Add("## Detail: NON-PASS and WARN Files")
$lines.Add("")
foreach ($r in ($AllResults | Where-Object { $_.Status -ne 'PASS' } | Sort-Object Zone,File)) {
    $lines.Add("### $($r.File)")
    $lines.Add("Zone: $($r.Zone) | Status: $($r.Status) | PASS=$($r.Pass) FAIL=$($r.Fail) WARN=$($r.Warn)")
    $lines.Add("")
    $lines.Add("| Check | Label | Result | Detail |")
    $lines.Add("|---|---|---|---|")
    foreach ($c in $r.Checks) {
        $lines.Add("| $($c.N) | $($c.Label) | $($c.Status) | $($c.Detail) |")
    }
    $lines.Add("")
}
$lines.Add("---")
$lines.Add("*Generated by Invoke-GovernanceAudit.ps1 v1.1 -- DCSE-DCSE-GOV-20260804-GOVERNANCE-AUDIT-001*")

$lines | Set-Content -Path $ReportOutput -Encoding UTF8

Write-Host "================================================"
Write-Host " DCSE Governance Structural Audit Complete"
Write-Host " Files scanned : $($AllResults.Count)"
Write-Host " PASS          : $PSCount"
Write-Host " NON-PASS      : $NPCount"
Write-Host " WARN          : $WNCount"
Write-Host " Report        : $ReportOutput"
Write-Host "================================================"
