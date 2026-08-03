# Run this yourself, interactively, once. Claude Code cannot run this step -
# it requires typing the actual secret value, which must never be pasted into
# chat or handled by an LLM session.
#
# Creates a DPAPI CurrentUser-protected credential bundle for an Anthropic API
# key, so the poller's spawned `claude -p` sessions can authenticate via a
# stable API key instead of the personal claude.ai Pro-subscription OAuth
# session (which silently expires with no automated recovery -- that's what
# caused the last outage).
#
# Get the key from: https://platform.claude.com/settings/workspaces/default/keys
# (the DCSEnterprise_SC key already visible there, or create a new one scoped
# for this purpose).
#
# Usage:
#   & "C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS\Register-AnthropicAPIKeyCredential.ps1"

$ErrorActionPreference = 'Stop'

$TargetDir  = 'C:\ProgramData\DCSE\secrets'
$TargetFile = Join-Path $TargetDir 'anthropic-api-key.clixml'

if (-not (Test-Path $TargetDir)) {
  New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

if (Test-Path $TargetFile) {
  $overwrite = Read-Host "Credential file already exists at $TargetFile. Overwrite? (y/N)"
  if ($overwrite -notmatch '^[Yy]') { Write-Host "Aborted."; exit 0 }
}

Write-Host "Registering Anthropic API key for unattended poller use."
Write-Host "This value is NOT displayed and NOT logged. Paste is hidden."
$apiKey = Read-Host -Prompt "ANTHROPIC_API_KEY (starts with sk-ant-api...)" -AsSecureString

$bundle = [PSCustomObject]@{
  ANTHROPIC_API_KEY = $apiKey
  dpapi_scope       = 'CurrentUser'
  registered_at_utc = (Get-Date).ToUniversalTime().ToString('o')
  windows_user      = "$env:USERDOMAIN\$env:USERNAME"
  machine           = $env:COMPUTERNAME
  purpose           = 'claude_code_poller.ps1 unattended child-session auth (replaces claude.ai OAuth dependency)'
}

$bundle | Export-Clixml -Path $TargetFile

Write-Host ""
Write-Host "Done. Credential bundle written to: $TargetFile"
Write-Host "Only the same Windows user account ($env:USERDOMAIN\$env:USERNAME) on this machine ($env:COMPUTERNAME) can decrypt it."
Write-Host "Verify with: (Import-Clixml '$TargetFile').ANTHROPIC_API_KEY.GetType()   # should show SecureString, never the plaintext"
