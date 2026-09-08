param(
  [Parameter(Mandatory=$true)][ValidateSet('gemini','claude','other')][string]$Validator,
  [string]$OutputPath = "$PSScriptRoot\..\..\artifacts\validation\methodology-independent-validation-request.md"
)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$emp = Join-Path $repo 'governance\v7.2\methodologies\DCSE_METH_DCS_Employment_Opportunity_Package_v1.md'
$thumb = Join-Path $repo 'governance\v7.2\methodologies\DCSE_METH_Thumbnail_Cover_Asset_Production_v1.md'
$packet = Join-Path $repo 'governance\v7.2\validation\DCSE_INDEPENDENT_VALIDATION_PACKET_EMP_THUMB_20260908.md'
foreach($p in @($emp,$thumb,$packet)){ if(-not(Test-Path $p)){ throw "Missing required artifact: $p" } }
$hashes = @{
  employment=(Get-FileHash $emp -Algorithm SHA256).Hash
  thumbnail=(Get-FileHash $thumb -Algorithm SHA256).Hash
  packet=(Get-FileHash $packet -Algorithm SHA256).Hash
}
$content = @"
# Independent Validation Handoff

Validator requested: $Validator
Generated: $((Get-Date).ToString('o'))
Repository: $repo
PS exposure: false
Credential exposure: false

Read and independently validate these exact files:
1. $emp
   SHA256: $($hashes.employment)
2. $thumb
   SHA256: $($hashes.thumbnail)
3. Validation protocol: $packet
   SHA256: $($hashes.packet)

Return only a completed validator receipt matching the YAML schema in the protocol. The validator must identify model/system/runtime and must not claim independence if it participated in originating or controlling these methodologies.
"@
$dir=Split-Path $OutputPath -Parent
if($dir -and -not(Test-Path $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
Set-Content -Path $OutputPath -Value $content -Encoding UTF8
$content
