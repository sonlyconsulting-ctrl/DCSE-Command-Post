param(
  [string]$OutputPath = 'v7.0\00_BUILD_CONTROL\convergence\COMMUNICATION_CONVERGENCE_001\INITIAL_FILE_INVENTORY_001.csv',
  [switch]$CurrentTree
)

$ErrorActionPreference = 'Stop'
$repo = (Get-Location).Path
$safe = $repo.Replace('\', '/')
$outputAbsolute = [System.IO.Path]::GetFullPath((Join-Path $repo $OutputPath))
if ($CurrentTree) {
  $prefix = $repo.TrimEnd('\') + '\'
  $paths = @(Get-ChildItem -LiteralPath . -Recurse -Force -File |
    Where-Object { $_.FullName -notmatch '\\.git(?:\\|$)' -and $_.FullName -ne $outputAbsolute } |
    ForEach-Object { $_.FullName.Substring($prefix.Length).Replace('\','/') })
} else {
  $tracked = @(git -c "safe.directory=$safe" ls-tree -r --name-only HEAD)
  $paths = @($tracked)
  if (Test-Path -LiteralPath 'package-lock.json') {
    $paths += 'package-lock.json'
  }
}

function Get-Classification([string]$Path) {
  if ($Path -eq 'package-lock.json') { return 'REVIEW' }
  if ($Path -like 'v6.9/*') { return 'FINAL' }
  if ($Path -like 'v7.0/00_BUILD_CONTROL/convergence/COMMUNICATION_CONVERGENCE_001/EVIDENCE_PACKET/SOURCE_RECEIPTS/*') { return 'ARCHIVE' }
  if ($Path -like 'v7.0/00_BUILD_CONTROL/convergence/COMMUNICATION_CONVERGENCE_001/EVIDENCE_PACKET/*') { return 'FINAL' }
  if ($Path -like 'v7.0/00_BUILD_CONTROL/convergence/COMMUNICATION_CONVERGENCE_001/*') { return 'FINAL' }
  if ($Path -like 'supabase/functions/v7-*') { return 'ACTIVE' }
  if ($Path -like 'supabase/decommission/v7-worker-auth/*') { return 'ACTIVE' }
  if ($Path -like 'supabase/migrations/*_v7_*') { return 'ACTIVE' }
  if ($Path -like 'supabase/rollback/v7-worker-auth-v1/*') { return 'ARCHIVE' }
  if ($Path -like 'supabase/rollback/*') { return 'REVIEW' }
  if ($Path -like 'supabase/seed/*') { return 'SUPPORT' }
  if ($Path -like 'scripts/ci/*' -or $Path -like 'scripts/governance/*' -or $Path -like 'tests/communication_convergence_*') { return 'SUPPORT' }
  if ($Path -like 'v7.0/*') { return 'REVIEW' }
  if ($Path -like '_Public_Builds/*') { return 'FINAL' }
  if ($Path -like '_Tribunal_Inbox/*') { return 'ARCHIVE' }
  if ($Path -eq 'workers/claude-reviewer-operational.js') { return 'ACTIVE' }
  if ($Path -eq 'scripts/windows/install-dcse-communication-worker.ps1') { return 'ACTIVE' }
  if ($Path -eq 'scripts/windows/Invoke-DCSECommunicationOperationalGate001.ps1') { return 'ARCHIVE' }
  if ($Path -eq 'tests/communication_operational_gate_001.sql') { return 'ARCHIVE' }
  if ($Path -eq 'docs/COMMUNICATION_GATE_001_QWEN_LOCAL_EXECUTION.md') { return 'ARCHIVE' }
  if ($Path -eq 'agent-os/v1/index.html') { return 'SUPERSEDED' }
  if ($Path -in @('api/index.js','apps/sc-agent-os/api/index.js','apps/sc-agent-os/package.json','apps/sc-agent-os/vercel.json','vercel.json')) { return 'ACTIVE' }
  if ($Path -like 'apps/sc-agent-os/migrations/*') { return 'ACTIVE' }
  if ($Path -like 'supabase/migrations/*') { return 'ACTIVE' }
  return 'SUPPORT'
}

function Get-Lineage([string]$Path) {
  if ($Path -eq 'package-lock.json') { return 'Untracked orphan lockfile; created 2026-07-28T02:48:31Z; no Git history' }
  if ($Path -like 'v6.9/*') { return 'Immutable v6.9 baseline; tree 2389d526615330d31adb4f879e5f8595968638e2' }
  if ($Path -like 'supabase/decommission/v7-worker-auth/*') { return 'CR-SEC-001 governed decommission payload' }
  if ($Path -like 'supabase/rollback/v7-worker-auth-v1/*') { return 'Exact staging deployment v1 source captured for CR-SEC-001 audit and restricted rollback' }
  if ($Path -like 'supabase/functions/v7-*' -or $Path -like 'supabase/migrations/*_v7_*' -or $Path -like 'supabase/rollback/*' -or $Path -like 'supabase/seed/*' -or $Path -eq '02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md') { return 'Bounded import from PR 14; reconciled against staging' }
  if ($Path -like 'v7.0/00_BUILD_CONTROL/convergence/COMMUNICATION_CONVERGENCE_001/*') { return 'Convergence Review 001 governed artifact' }
  if ($Path -like 'v7.0/*' -or $Path -in @('workers/claude-reviewer-operational.js','scripts/windows/install-dcse-communication-worker.ps1','scripts/windows/Invoke-DCSECommunicationOperationalGate001.ps1','tests/communication_operational_gate_001.sql','docs/COMMUNICATION_GATE_001_QWEN_LOCAL_EXECUTION.md')) { return 'PR 15 / chatgpt/v7-foundation-runtime-compiler' }
  return 'origin/main baseline'
}

function Get-Disposition([string]$Path, [string]$Class) {
  if ($Path -eq 'package-lock.json') { return 'PRESERVE_UNTRACKED; DO_NOT_COMMIT; DO_NOT_DELETE' }
  if ($Class -eq 'ARCHIVE') { return 'PRESERVE; reference from convergence record; do not execute post-Gate-001' }
  if ($Class -eq 'SUPERSEDED') { return 'PRESERVE_IN_PLACE; exclude from communication promotion authority' }
  if ($Class -eq 'FINAL') { return 'PRESERVE_IN_PLACE; immutable' }
  return 'PRESERVE_IN_PLACE'
}

$rows = foreach ($path in ($paths | Sort-Object -Unique)) {
  $native = Join-Path $repo ($path.Replace('/', '\'))
  $item = Get-Item -LiteralPath $native
  $class = Get-Classification $path
  $hash = if ($path -like '*/HASH_MANIFEST.sha256') { 'DERIVED_AFTER_INVENTORY' } else { (Get-FileHash -LiteralPath $native -Algorithm SHA256).Hash }
  [pscustomobject]@{
    path = $path
    bytes = $item.Length
    sha256 = $hash
    classification = $class
    lineage = Get-Lineage $path
    duplicate_group = ''
    proposed_name = [System.IO.Path]::GetFileName($path)
    proposed_destination = $path
    disposition = Get-Disposition $path $class
  }
}

if ($CurrentTree) {
  $outputRelative = $outputAbsolute.Substring(($repo.TrimEnd('\') + '\').Length).Replace('\','/')
  $rows += [pscustomobject]@{
    path = $outputRelative
    bytes = ''
    sha256 = 'SELF_REFERENTIAL_EXCLUDED'
    classification = 'FINAL'
    lineage = 'Convergence Review 001 governed artifact'
    duplicate_group = ''
    proposed_name = [System.IO.Path]::GetFileName($outputRelative)
    proposed_destination = $outputRelative
    disposition = 'PRESERVE_IN_PLACE; self hash excluded by design'
  }
}

$rows | Export-Csv -LiteralPath $OutputPath -NoTypeInformation -Encoding UTF8

[pscustomobject]@{
  output = (Resolve-Path -LiteralPath $OutputPath).Path
  file_count = $rows.Count
  byte_identical_duplicate_groups = @($rows | Group-Object sha256 | Where-Object Count -gt 1).Count
  counts = $rows | Group-Object classification | Sort-Object Name | ForEach-Object { "$($_.Name)=$($_.Count)" }
}
