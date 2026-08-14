#!/bin/bash

# Project v7.1 Setup — Bash Implementation
# Version: 1.0
# Usage: ./setup.sh --project-name my-project --models claude qwen --github-user username --root ~/projects/my-project
# No secrets embedded; all auth via user's git session or Supabase MCP OAuth

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default values
PROJECT_NAME=""
MODELS=()
GITHUB_USER=""
PROJECT_ROOT=""
GOVERNANCE_BRANCH="governance/v7.1-owned-product-harness"
GOVERNANCE_BASE_URL="https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/${GOVERNANCE_BRANCH}/governance/v7.1"

# Functions
log_info() {
  echo -e "${GREEN}✓${NC} $1"
}

log_error() {
  echo -e "${RED}✗${NC} $1" >&2
}

log_warn() {
  echo -e "${YELLOW}⚠${NC} $1"
}

show_usage() {
  cat << EOF
Usage: $0 [OPTIONS]

Required Options:
  --project-name NAME       Project name (e.g., my-claude-ai)
  --models MODEL [...]      Space-separated models (claude, qwen, codex, chatgpt)
  --github-user USER        GitHub username
  --root PATH               Project root directory (will be created)

Examples:
  $0 --project-name my-claude-ai --models claude --github-user username --root ~/projects/my-claude-ai
  $0 --project-name multi-ai --models claude qwen --github-user username --root ~/projects/multi-ai

Environment Variables (optional):
  GITHUB_USER               GitHub username (can be set instead of --github-user)
  DEBUG=1                   Enable debug output

Note: This script requires:
  - git (already installed)
  - curl or wget (to fetch governance)
  - gh CLI (GitHub CLI) for push; user must have run 'gh auth login' first
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --project-name)
      PROJECT_NAME="$2"
      shift 2
      ;;
    --models)
      shift
      while [[ $# -gt 0 ]] && [[ ! "$1" =~ ^-- ]]; do
        MODELS+=("$1")
        shift
      done
      ;;
    --github-user)
      GITHUB_USER="$2"
      shift 2
      ;;
    --root)
      PROJECT_ROOT="$2"
      shift 2
      ;;
    --help)
      show_usage
      exit 0
      ;;
    *)
      log_error "Unknown option: $1"
      show_usage
      exit 1
      ;;
  esac
done

# Validate inputs
if [[ -z "$PROJECT_NAME" ]]; then
  log_error "Missing required option: --project-name"
  show_usage
  exit 1
fi

if [[ ${#MODELS[@]} -eq 0 ]]; then
  log_error "Missing required option: --models"
  show_usage
  exit 1
fi

if [[ -z "$GITHUB_USER" ]]; then
  GITHUB_USER="${GITHUB_USER:-}"
  if [[ -z "$GITHUB_USER" ]]; then
    log_error "Missing required option: --github-user (or set GITHUB_USER env var)"
    show_usage
    exit 1
  fi
fi

if [[ -z "$PROJECT_ROOT" ]]; then
  log_error "Missing required option: --root"
  show_usage
  exit 1
fi

# Validate models
VALID_MODELS=("claude" "qwen" "codex" "chatgpt")
for model in "${MODELS[@]}"; do
  if [[ ! " ${VALID_MODELS[@]} " =~ " ${model} " ]]; then
    log_error "Invalid model: $model. Valid models: ${VALID_MODELS[*]}"
    exit 1
  fi
done

# Create project directory
if [[ -d "$PROJECT_ROOT" ]]; then
  log_warn "Directory exists: $PROJECT_ROOT (will use existing)"
else
  mkdir -p "$PROJECT_ROOT"
  log_info "Created project directory: $PROJECT_ROOT"
fi

cd "$PROJECT_ROOT"

# Initialize .git if not already initialized
if [[ ! -d .git ]]; then
  git init
  log_info "Initialized git repository"
else
  log_warn "Git repository already initialized"
fi

# Create .claude directory
mkdir -p .claude/model-instructions

# Fetch Master Profile from GitHub (public, no auth required)
log_info "Fetching v7.1 governance from GitHub..."
MASTER_PROFILE_URL="${GOVERNANCE_BASE_URL}/DCSE_Master_Profile_v7.1.md"

mkdir -p governance/v7.1/doctrines

# Try to fetch with curl, fallback to wget
if command -v curl &> /dev/null; then
  if ! curl -s -f "$MASTER_PROFILE_URL" -o governance/v7.1/DCSE_Master_Profile_v7.1.md; then
    log_error "Failed to fetch Master Profile from: $MASTER_PROFILE_URL"
    exit 1
  fi
else
  if ! wget -q "$MASTER_PROFILE_URL" -O governance/v7.1/DCSE_Master_Profile_v7.1.md; then
    log_error "Failed to fetch Master Profile (requires curl or wget)"
    exit 1
  fi
fi
log_info "Fetched Master Profile: governance/v7.1/DCSE_Master_Profile_v7.1.md"

# Fetch Doctrines D01-D22
log_info "Fetching 22 Doctrines..."
for i in {1..22}; do
  DOCTRINE_ID=$(printf "D%02d" $i)
  DOCTRINE_URL="${GOVERNANCE_BASE_URL}/doctrines/Doctrine_${DOCTRINE_ID}.md"
  DOCTRINE_FILE="governance/v7.1/doctrines/${DOCTRINE_ID}_Doctrine.md"

  if command -v curl &> /dev/null; then
    if curl -s -f "$DOCTRINE_URL" -o "$DOCTRINE_FILE" 2>/dev/null; then
      echo -n "."
    else
      log_warn "Doctrine $DOCTRINE_ID not found (optional); skipping"
    fi
  else
    if wget -q "$DOCTRINE_URL" -O "$DOCTRINE_FILE" 2>/dev/null; then
      echo -n "."
    else
      log_warn "Doctrine $DOCTRINE_ID not found (optional); skipping"
    fi
  fi
done
echo ""
log_info "Fetched available doctrines"

# Create governance registry index
cat > governance/.governance-registry.json << 'EOF'
{
  "version": "7.1",
  "fetched_at": null,
  "doctrines": {},
  "master_profile": null
}
EOF
log_info "Created governance registry index"

# Generate model-specific instructions
for model in "${MODELS[@]}"; do
  INSTRUCTION_FILE=".claude/model-instructions/${model}-project-v7.1.md"

  # Determine model-specific parameters
  case $model in
    claude)
      ENTRY_LANE="SC"
      MAX_PARALLEL="3"
      APPROVAL_AUTHORITY="PS→DCS→L0"
      TOKEN_BUDGET="250K"
      GATE="FAIL_FAST_GATE_v7.1.md"
      ;;
    qwen)
      ENTRY_LANE="SC"
      MAX_PARALLEL="2"
      APPROVAL_AUTHORITY="PS→DCS→L0"
      TOKEN_BUDGET="150K"
      GATE="FAIL_FAST_GATE_v7.1.md"
      ;;
    codex)
      ENTRY_LANE="SC"
      MAX_PARALLEL="2"
      APPROVAL_AUTHORITY="DCS→L0"
      TOKEN_BUDGET="100K"
      GATE="MANUAL_GATE_v7.1.md"
      ;;
    chatgpt)
      ENTRY_LANE="SC"
      MAX_PARALLEL="1"
      APPROVAL_AUTHORITY="Manual (L-1)"
      TOKEN_BUDGET="50K"
      GATE="EXTERNAL_GATE_v7.1.md"
      ;;
  esac

  cat > "$INSTRUCTION_FILE" << EOFMD
# ${model^} Project v7.1 — Project-Specific Instructions

**Project:** ${PROJECT_NAME}
**Model:** ${model}
**Version:** 7.1
**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")

## Model Identity
- **Model:** ${model}
- **Entry Lane:** ${ENTRY_LANE} (Software & Code)
- **Authority Chain:** ${APPROVAL_AUTHORITY}
- **Max Parallel Tasks:** ${MAX_PARALLEL}
- **Token Budget per Task:** ${TOKEN_BUDGET}

## Governance Scope

This project is governed by:
- DCSE Master Profile v7.1
- All 22 Doctrines (D01-D22) in \`governance/v7.1/doctrines/\`
- ${model}-specific task intake patterns
- First Assignment ${GATE}

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

**Repo:** https://github.com/${GITHUB_USER}/${PROJECT_NAME}
**Branch:** claude/project-v7-1-setup-l2t95z
**Setup Date:** $(date -u +"%Y-%m-%d")

## Key Links

- [Master Profile](../governance/v7.1/DCSE_Master_Profile_v7.1.md)
- [Governance Registry](../governance/.governance-registry.json)
- [Onboarding Manifest](../onboarding/model-manifests/${model}-manifest.json)
- [Task Intake Pattern](../onboarding/FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md)

## Next Steps

1. Push this project to GitHub:
   \`\`\`bash
   cd ${PROJECT_ROOT}
   git add .
   git commit -m "v7.1 Setup: ${PROJECT_NAME} initialized for ${model}"
   git push -u origin claude/project-v7-1-setup-l2t95z
   \`\`\`

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

**Auto-Generated by Project v7.1 Setup** | $(date)
EOFMD

  log_info "Generated ${model} instructions: $INSTRUCTION_FILE"
done

# Create model manifests
mkdir -p onboarding/model-manifests

for model in "${MODELS[@]}"; do
  MANIFEST_FILE="onboarding/model-manifests/${model}-manifest.json"

  cat > "$MANIFEST_FILE" << EOFJ
{
  "version": "7.1",
  "model": "${model}",
  "project_name": "${PROJECT_NAME}",
  "github_repo": "https://github.com/${GITHUB_USER}/${PROJECT_NAME}",
  "github_branch": "claude/project-v7-1-setup-l2t95z",
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "status": "onboarding",
  "governance": {
    "version": "7.1",
    "profile": "governance/v7.1/DCSE_Master_Profile_v7.1.md",
    "doctrines_count": 22,
    "doctrines_path": "governance/v7.1/doctrines/"
  },
  "task_intake": {
    "source": "sc_command_post.project_plans",
    "filter": "model_name = '${model}' AND status = 'pending'",
    "poll_interval_seconds": 30,
    "max_task_age_seconds": 300
  },
  "gates": {
    "first_assignment": "FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md",
    "authority": "PS→DCS→L0"
  }
}
EOFJ

  log_info "Generated manifest: $MANIFEST_FILE"
done

# Create onboarding checklist
cat > onboarding/onboarding-checklist.md << 'EOF'
# Project v7.1 Onboarding Checklist

## Pre-Deployment

- [ ] All governance files fetched and present in \`governance/v7.1/\`
- [ ] Model instructions generated for all models
- [ ] Model manifests created in \`onboarding/model-manifests/\`
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

**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF
log_info "Created onboarding checklist"

# Create .gitignore if not present
if [[ ! -f .gitignore ]]; then
  cat > .gitignore << 'EOF'
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
EOF
  log_info "Created .gitignore"
fi

# Create initial README
if [[ ! -f README.md ]]; then
  cat > README.md << 'EOF'
# ${PROJECT_NAME}

**v7.1 Project Setup** for multi-AI models (Claude, Qwen, Codex, ChatGPT)

## Quick Start

1. **Fetch governance** (already done):
   ```bash
   ls -la governance/v7.1/
   ```

2. **Review model instructions**:
   ```bash
   cat .claude/model-instructions/<model>-project-v7.1.md
   ```

3. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "v7.1 Setup: ${PROJECT_NAME} initialized"
   git push -u origin claude/project-v7-1-setup-l2t95z
   ```

4. **Register with Supabase** (Claude will do this):
   - Project metadata → \`projects\` table
   - Model mappings → \`project_models\` table
   - Governance registry → \`governance_registry\` table

## Structure

```
.
├── .claude/
│   ├── model-instructions/
│   │   ├── claude-project-v7.1.md
│   │   ├── qwen-project-v7.1.md
│   │   ├── codex-project-v7.1.md
│   │   └── chatgpt-project-v7.1.md
│   └── settings.json
├── governance/
│   ├── v7.1/
│   │   ├── DCSE_Master_Profile_v7.1.md
│   │   ├── doctrines/
│   │   │   ├── D01_Doctrine.md
│   │   │   └── ... D02-D22
│   │   └── schemas/
│   └── .governance-registry.json
├── onboarding/
│   ├── FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md
│   ├── model-manifests/
│   │   ├── claude-manifest.json
│   │   └── ... qwen, codex, chatgpt
│   └── onboarding-checklist.md
└── README.md
```

## Governance

- **Master Profile:** \`governance/v7.1/DCSE_Master_Profile_v7.1.md\`
- **Doctrines (D01-D22):** \`governance/v7.1/doctrines/\`
- **Authority:** DCS Level 0 (sonlyconsulting@gmail.com)

## Support

For issues or questions, contact DCS Level 0 directly.

---

**Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
**Auto-generated by Project v7.1 Setup**
EOF
  log_info "Created README.md"
else
  log_warn "README.md already exists; skipping"
fi

# Initialize git and commit
if ! git status &> /dev/null; then
  git init
  log_info "Initialized git repository"
fi

# Check if changes exist
if [[ -n $(git status --porcelain) ]]; then
  git add .
  git commit -m "v7.1 Setup: ${PROJECT_NAME} initialized for $(echo ${MODELS[@]})"
  log_info "Committed initial project setup"
else
  log_warn "No changes to commit; project already initialized"
fi

# Final summary
echo ""
echo "=========================================="
echo -e "${GREEN}Project v7.1 Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Project:       $PROJECT_NAME"
echo "Models:        $(echo ${MODELS[@]})"
echo "GitHub User:   $GITHUB_USER"
echo "Location:      $PROJECT_ROOT"
echo ""
echo "Next Steps:"
echo "  1. cd $PROJECT_ROOT"
echo "  2. git push -u origin claude/project-v7-1-setup-l2t95z"
echo "  3. Monitor: https://github.com/$GITHUB_USER/$PROJECT_NAME/pulls"
echo ""
echo "Governance:"
echo "  - Fetched: Master Profile + $(ls -1 governance/v7.1/doctrines/ 2>/dev/null | wc -l) doctrines"
echo "  - Models: $(for m in ${MODELS[@]}; do echo -n "$m, "; done | sed 's/, $//')"
echo ""
echo "Ready for task intake from SC-Command-Post Supabase."
echo ""
