$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$safe = $repo.Replace('\', '/')
$failures = [System.Collections.Generic.List[string]]::new()

function Assert-Check([bool]$Condition, [string]$Name) {
  if ($Condition) { Write-Output "PASS $Name" }
  else { Write-Output "FAIL $Name"; $failures.Add($Name) }
}

$receipt = 'v7.0\00_BUILD_CONTROL\convergence\COMMUNICATION_CONVERGENCE_001\EVIDENCE_PACKET\RECEIPTS\COMMUNICATION_OPERATIONAL_GATE_001.json'
Assert-Check ((Get-FileHash -LiteralPath $receipt -Algorithm SHA256).Hash -eq '9C5D6F485566ADBC035284F74EA5BDC10AA76BF4953D4DE3AD9753ABEA8B598C') 'Gate 001 PASS receipt hash'

$jsonFailures = @()
Get-ChildItem -LiteralPath . -Recurse -File -Filter '*.json' | ForEach-Object {
  try { Get-Content -Raw -LiteralPath $_.FullName | ConvertFrom-Json | Out-Null }
  catch { $jsonFailures += $_.FullName }
}
Assert-Check ($jsonFailures.Count -eq 0) 'JSON parse validation'

$jsFailures = @()
Get-ChildItem -LiteralPath . -Recurse -File -Filter '*.js' | ForEach-Object {
  & node --check $_.FullName 2>$null
  if ($LASTEXITCODE -ne 0) { $jsFailures += $_.FullName }
}
Assert-Check ($jsFailures.Count -eq 0) 'JavaScript syntax validation'

& node '.\tests\communication_convergence_static.js'
Assert-Check ($LASTEXITCODE -eq 0) 'Communication deterministic static suite'

$secretPatterns = @(
  'sk-[A-Za-z0-9_-]{20,}',
  'sb_secret_[A-Za-z0-9_-]{20,}',
  'eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}',
  '(?i)postgres(?:ql)?://[^\s:/]+:[^\s@]+@'
)
$secretHits = @()
$scanFiles = Get-ChildItem -LiteralPath . -Recurse -File | Where-Object {
  $_.FullName -notmatch '\\.git(?:\\|$)' -and $_.Name -ne 'package-lock.json'
}
foreach ($file in $scanFiles) {
  $text = Get-Content -Raw -LiteralPath $file.FullName -ErrorAction SilentlyContinue
  foreach ($pattern in $secretPatterns) {
    if ($text -match $pattern) { $secretHits += "$($file.FullName):$pattern" }
  }
}
Assert-Check ($secretHits.Count -eq 0) 'Secret pattern scan'

$headV69 = git -c "safe.directory=$safe" rev-parse HEAD:v6.9
$mainV69 = git -c "safe.directory=$safe" rev-parse origin/main:v6.9
Assert-Check ($headV69 -eq $mainV69) 'v6.9 immutable tree'

$lockStatus = git -c "safe.directory=$safe" status --short -- package-lock.json
$lockHash = (Get-FileHash -LiteralPath 'package-lock.json' -Algorithm SHA256).Hash
Assert-Check ($lockStatus -eq '?? package-lock.json') 'package-lock remains untracked'
Assert-Check ($lockHash -eq '3CAE2CCFFC57A184BE6BD71229D2FFB9DBDB855A061ECCEB372A8078C0C3BEDC') 'package-lock remains untouched'
Assert-Check (-not (Test-Path -LiteralPath 'supabase\functions\v7-worker-auth\index.ts')) 'unsafe v7-worker-auth excluded'

Write-Output "SUMMARY failures=$($failures.Count)"
if ($failures.Count -gt 0) { exit 1 }
