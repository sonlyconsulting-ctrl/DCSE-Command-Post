# Project v7.1 Setup — PowerShell Implementation (Windows)
# Version: 1.0
# Usage: .\setup.ps1 -ProjectName "my-project" -Models @("claude", "qwen") -GitHubUser "username" -ProjectRoot "C:\projects\my-project"
# No secrets embedded; all auth via user's git session or Supabase MCP OAuth

param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName,

    [Parameter(Mandatory = $true)]
    [string[]]$Models,

    [Parameter(Mandatory = $true)]
    [string]$GitHubUser,

    [Parameter(Mandatory = $true)]
    [string]$ProjectRoot,

    [string]$GovernanceBranch = "governance/v7.1-owned-product-harness",
    [switch]$Help
)

# Functions
function Write-Info {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
    exit 1
}

function Write-Warn {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Show-Usage {
    Write-Host @"
Usage: .\setup.ps1 -ProjectName <name> -Models <models> -GitHubUser <username> -ProjectRoot <path>

Required Parameters:
  -ProjectName NAME       Project name (e.g., my-claude-ai)
  -Models MODEL [...]     Array of models: @("claude", "qwen", "codex", "chatgpt")
  -GitHubUser USER        GitHub username
  -ProjectRoot PATH       Project root directory (will be created)

Examples:
  .\setup.ps1 -ProjectName "my-claude-ai" -Models @("claude") -GitHubUser "username" -ProjectRoot "C:\projects\my-claude-ai"
  .\setup.ps1 -ProjectName "multi-ai" -Models @("claude", "qwen") -GitHubUser "username" -ProjectRoot "C:\projects\multi-ai"

Environment Variables (optional):
  GITHUB_USER             GitHub username (used if -GitHubUser not provided)

Requirements:
  - git (Windows Git Bash or GitHub CLI)
  - PowerShell 5.1+
  - gh CLI for push (run 'gh auth login' first)

Note: This script requires no secrets embedded. All auth via user's browser session.
"@
}

if ($Help) {
    Show-Usage
    exit 0
}

# Validate inputs
$ValidModels = @("claude", "qwen", "codex", "chatgpt")
foreach ($model in $Models) {
    if ($model -notin $ValidModels) {
        Write-Error-Custom "Invalid model: $model. Valid models: $($ValidModels -join ', ')"
    }
}

if (-not $ProjectName) {
    Write-Error-Custom "Missing required parameter: -ProjectName"
}

if ($Models.Count -eq 0) {
    Write-Error-Custom "Missing required parameter: -Models"
}

if (-not $GitHubUser) {
    Write-Error-Custom "Missing required parameter: -GitHubUser"
}

if (-not $ProjectRoot) {
    Write-Error-Custom "Missing required parameter: -ProjectRoot"
}

$GovernanceBaseUrl = "https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/$GovernanceBranch/governance/v7.1"

# Create project directory
if (-not (Test-Path $ProjectRoot)) {
    New-Item -ItemType Directory -Path $ProjectRoot | Out-Null
    Write-Info "Created project directory: $ProjectRoot"
} else {
    Write-Warn "Directory exists: $ProjectRoot (will use existing)"
}

Set-Location $ProjectRoot

# Initialize git if not already initialized
if (-not (Test-Path .git)) {
    git init
    Write-Info "Initialized git repository"
} else {
    Write-Warn "Git repository already initialized"
}

# Create .claude directory
if (-not (Test-Path ".\.claude\model-instructions")) {
    New-Item -ItemType Directory -Path ".\.claude\model-instructions" -Force | Out-Null
}

# Fetch Master Profile from GitHub (public, no auth required)
Write-Info "Fetching v7.1 governance from GitHub..."

$MasterProfileUrl = "$GovernanceBaseUrl/DCSE_Master_Profile_v7.1.md"
if (-not (Test-Path ".\governance\v7.1")) {
    New-Item -ItemType Directory -Path ".\governance\v7.1\doctrines" -Force | Out-Null
}

try {
    $MasterProfile = Invoke-WebRequest -Uri $MasterProfileUrl -UseBasicParsing -ErrorAction Stop
    $MasterProfile.Content | Out-File -FilePath ".\governance\v7.1\DCSE_Master_Profile_v7.1.md" -Encoding UTF8
    Write-Info "Fetched Master Profile: governance\v7.1\DCSE_Master_Profile_v7.1.md"
} catch {
    Write-Error-Custom "Failed to fetch Master Profile from: $MasterProfileUrl`nError: $_"
}

# Fetch Doctrines D01-D22
Write-Info "Fetching 22 Doctrines..."
$DoctrinesFetched = 0

for ($i = 1; $i -le 22; $i++) {
    $DoctrineId = "D{0:D2}" -f $i
    $DoctrineUrl = "$GovernanceBaseUrl/doctrines/Doctrine_$DoctrineId.md"
    $DoctrineFile = ".\governance\v7.1\doctrines\${DoctrineId}_Doctrine.md"

    try {
        $DoctrineFetch = Invoke-WebRequest -Uri $DoctrineUrl -UseBasicParsing -ErrorAction Stop
        $DoctrineFetch.Content | Out-File -FilePath $DoctrineFile -Encoding UTF8
        Write-Host "." -NoNewline -ForegroundColor Green
        $DoctrinesFetched++
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
}

Write-Host ""
Write-Info "Fetched $DoctrinesFetched available doctrines"

# Create governance registry index
$GovernanceRegistry = @{
    version       = "7.1"
    fetched_at    = $null
    doctrines     = @{}
    master_profile = $null
} | ConvertTo-Json

$GovernanceRegistry | Out-File -FilePath ".\governance\.governance-registry.json" -Encoding UTF8
Write-Info "Created governance registry index"

# Generate model-specific instructions
foreach ($model in $Models) {
    $InstructionFile = ".\.claude\model-instructions\$model-project-v7.1.md"

    # Determine model-specific parameters
    switch ($model) {
        "claude" {
            $EntryLane = "SC"
            $MaxParallel = "3"
            $ApprovalAuthority = "PS→DCS→L0"
            $TokenBudget = "250K"
            $Gate = "FAIL_FAST_GATE_v7.1.md"
        }
        "qwen" {
            $EntryLane = "SC"
            $MaxParallel = "2"
            $ApprovalAuthority = "PS→DCS→L0"
            $TokenBudget = "150K"
            $Gate = "FAIL_FAST_GATE_v7.1.md"
        }
        "codex" {
            $EntryLane = "SC"
            $MaxParallel = "2"
            $ApprovalAuthority = "DCS→L0"
            $TokenBudget = "100K"
            $Gate = "MANUAL_GATE_v7.1.md"
        }
        "chatgpt" {
            $EntryLane = "SC"
            $MaxParallel = "1"
            $ApprovalAuthority = "Manual (L-1)"
            $TokenBudget = "50K"
            $Gate = "EXTERNAL_GATE_v7.1.md"
        }
    }

    $ModelCapitalized = $model.Substring(0, 1).ToUpper() + $model.Substring(1)
    $CreatedDate = (Get-Date -Format "O")
    $NowDate = Get-Date -Format "yyyy-MM-dd"

    $InstructionContent = @"
# $ModelCapitalized Project v7.1 — Project-Specific Instructions

**Project:** $ProjectName
**Model:** $model
**Version:** 7.1
**Created:** $CreatedDate

## Model Identity
- **Model:** $model
- **Entry Lane:** $EntryLane (Software & Code)
- **Authority Chain:** $ApprovalAuthority
- **Max Parallel Tasks:** $MaxParallel
- **Token Budget per Task:** $TokenBudget

## Governance Scope

This project is governed by:
- DCSE Master Profile v7.1
- All 22 Doctrines (D01-D22) in \`governance\v7.1\doctrines\`
- $model-specific task intake patterns
- First Assignment $Gate

## Task Intake

- **Task Source:** SC-Command-Post Supabase \`project_plans\` table
- **Poll Interval:** 30 seconds
- **Max Task Age Before Timeout:** 300 seconds
- **Required Fields:** title, lane, task_type, priority, created_by_label

## Authority & Approvals

| Action | Allowed | Notes |
|--------|---------|-------|
| Approve own code reviews | YES | PS-level authority |
| Promote personas | NO | DCS Level 0 only |
| Bypass gate checks | NO | Non-negotiable |
| Push to main | YES | After PR approval |
| Modify governance | NO | Must notify DCS Level 0 |

## Incident Response

1. **Detect Governance Violation** → Pause execution immediately
2. **Log Incident** → Insert row into \`governance_violations\` table (via Supabase MCP)
3. **Notify DCS L0** → Email sonlyconsulting@gmail.com with incident ID
4. **Await Approval** → Do not resume until explicit approval received
5. **Resume** → Continue from paused state

## GitHub Repository

**Repo:** https://github.com/$GitHubUser/$ProjectName
**Branch:** claude/project-v7-1-setup-l2t95z
**Setup Date:** $NowDate

## Key Links

- [Master Profile](../governance/v7.1/DCSE_Master_Profile_v7.1.md)
- [Governance Registry](../governance/.governance-registry.json)
- [Onboarding Manifest](../onboarding/model-manifests/$model-manifest.json)
- [Task Intake Pattern](../onboarding/FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md)

## Next Steps

1. Push this project to GitHub:
   ``````bash
   cd "$ProjectRoot"
   git add .
   git commit -m "v7.1 Setup: $ProjectName initialized for $model"
   git push -u origin claude/project-v7-1-setup-l2t95z
   ``````

2. Create pull request (or CLI will do this automatically)

3. Register with Supabase SC-Command-Post:
   - Project metadata inserted into \`projects\` table
   - Model mapping added to \`project_models\` table
   - Governance doctrines indexed in \`governance_registry\` table

4. Monitor task intake:
   - Project agent polls \`project_plans\` table every 30s
   - First task triggers FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md
   - On pass: task assigned and executed
   - On fail: task failed, incident created, DCS notified

---

**Auto-Generated by Project v7.1 Setup** | $CreatedDate
"@

    $InstructionContent | Out-File -FilePath $InstructionFile -Encoding UTF8
    Write-Info "Generated $model instructions: $InstructionFile"
}

# Create model manifests
if (-not (Test-Path ".\onboarding\model-manifests")) {
    New-Item -ItemType Directory -Path ".\onboarding\model-manifests" -Force | Out-Null
}

foreach ($model in $Models) {
    $ManifestFile = ".\onboarding\model-manifests\$model-manifest.json"
    $CreatedDate = (Get-Date -Format "O")

    $ManifestContent = @{
        version       = "7.1"
        model         = $model
        project_name  = $ProjectName
        github_repo   = "https://github.com/$GitHubUser/$ProjectName"
        github_branch = "claude/project-v7-1-setup-l2t95z"
        created_at    = $CreatedDate
        status        = "onboarding"
        governance    = @{
            version           = "7.1"
            profile           = "governance\v7.1\DCSE_Master_Profile_v7.1.md"
            doctrines_count   = 22
            doctrines_path    = "governance\v7.1\doctrines\"
        }
        task_intake   = @{
            source                = "sc_command_post.project_plans"
            filter                = "model_name = '$model' AND status = 'pending'"
            poll_interval_seconds = 30
            max_task_age_seconds  = 300
        }
        gates         = @{
            first_assignment = "FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md"
            authority        = "PS→DCS→L0"
        }
    } | ConvertTo-Json

    $ManifestContent | Out-File -FilePath $ManifestFile -Encoding UTF8
    Write-Info "Generated manifest: $ManifestFile"
}

# Create onboarding checklist
$ChecklistContent = @"
# Project v7.1 Onboarding Checklist

## Pre-Deployment

- [ ] All governance files fetched and present in \`governance\v7.1\\`
- [ ] Model instructions generated for all models
- [ ] Model manifests created in \`onboarding\model-manifests\\`
- [ ] Git repository initialized
- [ ] No secrets in git history (check \`git log -S <pattern>\`)

## Deployment

- [ ] Pushed to GitHub: \`git push -u origin claude/project-v7-1-setup-l2t95z\`
- [ ] Pull request created (automatically or manually)
- [ ] PR passes CI checks (if applicable)
- [ ] PR reviewed and approved

## Post-Deployment

- [ ] Registered with Supabase SC-Command-Post
  - [ ] Project record inserted (\`projects\` table)
  - [ ] Model mappings created (\`project_models\` table)
  - [ ] Governance doctrines indexed (\`governance_registry\` table)
- [ ] Task intake polling verified
- [ ] First task assignment triggered (FAIL_FAST_GATE)
- [ ] Incident response team notified (DCS Level 0)

## Ongoing

- [ ] Monitor governance registry for updates
- [ ] Review task execution logs weekly
- [ ] Update doctrines when governance changes
- [ ] Audit access and approvals quarterly

---

**Created:** $(Get-Date -Format 'o')
"@

$ChecklistContent | Out-File -FilePath ".\onboarding\onboarding-checklist.md" -Encoding UTF8
Write-Info "Created onboarding checklist"

# Create .gitignore if not present
if (-not (Test-Path ".gitignore")) {
    $GitignoreContent = @"
# Secrets (never commit)
.env
.env.local
.env.*.local
*.key
*.pem
.claude/settings.local.json

# Build/Runtime (optional)
node_modules/
dist/
build/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"@
    $GitignoreContent | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Info "Created .gitignore"
}

# Create initial README
if (-not (Test-Path "README.md")) {
    $ModelsString = $Models -join ", "
    $ReadmeContent = @"
# $ProjectName

**v7.1 Project Setup** for multi-AI models (Claude, Qwen, Codex, ChatGPT)

## Quick Start

1. **Fetch governance** (already done):
   \`\`\`bash
   ls -la governance\v7.1\
   \`\`\`

2. **Review model instructions**:
   \`\`\`bash
   cat .\.claude\model-instructions\<model>-project-v7.1.md
   \`\`\`

3. **Push to GitHub**:
   \`\`\`bash
   git add .
   git commit -m "v7.1 Setup: $ProjectName initialized"
   git push -u origin claude/project-v7-1-setup-l2t95z
   \`\`\`

4. **Register with Supabase** (Claude will do this):
   - Project metadata → \`projects\` table
   - Model mappings → \`project_models\` table
   - Governance registry → \`governance_registry\` table

## Structure

\`\`\`
.
├── .claude\
│   ├── model-instructions\
│   │   ├── claude-project-v7.1.md
│   │   ├── qwen-project-v7.1.md
│   │   ├── codex-project-v7.1.md
│   │   └── chatgpt-project-v7.1.md
│   └── settings.json
├── governance\
│   ├── v7.1\
│   │   ├── DCSE_Master_Profile_v7.1.md
│   │   ├── doctrines\
│   │   │   ├── D01_Doctrine.md
│   │   │   └── ... D02-D22
│   │   └── schemas\
│   └── .governance-registry.json
├── onboarding\
│   ├── FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md
│   ├── model-manifests\
│   │   ├── claude-manifest.json
│   │   └── ... qwen, codex, chatgpt
│   └── onboarding-checklist.md
└── README.md
\`\`\`

## Governance

- **Master Profile:** \`governance\v7.1\DCSE_Master_Profile_v7.1.md\`
- **Doctrines (D01-D22):** \`governance\v7.1\doctrines\\`
- **Authority:** DCS Level 0 (sonlyconsulting@gmail.com)

## Support

For issues or questions, contact DCS Level 0 directly.

---

**Created:** $(Get-Date -Format 'o')
**Auto-generated by Project v7.1 Setup**
"@
    $ReadmeContent | Out-File -FilePath "README.md" -Encoding UTF8
    Write-Info "Created README.md"
} else {
    Write-Warn "README.md already exists; skipping"
}

# Initialize git and commit
$Status = git status --porcelain 2>$null
if ($Status) {
    git add .
    $ModelsCommit = $Models -join ", "
    git commit -m "v7.1 Setup: $ProjectName initialized for $ModelsCommit"
    Write-Info "Committed initial project setup"
} else {
    Write-Warn "No changes to commit; project already initialized"
}

# Final summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Project v7.1 Setup Complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project:       $ProjectName"
Write-Host "Models:        $($Models -join ', ')"
Write-Host "GitHub User:   $GitHubUser"
Write-Host "Location:      $ProjectRoot"
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. cd `"$ProjectRoot`""
Write-Host "  2. git push -u origin claude/project-v7-1-setup-l2t95z"
Write-Host "  3. Monitor: https://github.com/$GitHubUser/$ProjectName/pulls"
Write-Host ""
Write-Host "Governance:" -ForegroundColor Yellow
$DocCount = (Get-ChildItem ".\governance\v7.1\doctrines" -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "  - Fetched: Master Profile + $DocCount doctrines"
Write-Host "  - Models: $($Models -join ', ')"
Write-Host ""
Write-Host "Ready for task intake from SC-Command-Post Supabase." -ForegroundColor Green
Write-Host ""
