# Project v7.1 Setup — Automated Multi-Model Project Initialization

**Version:** 1.0  
**Purpose:** Credential-safe, automated setup for Claude, Qwen, Codex, or ChatGPT projects  
**No secrets embedded** — all auth via user's git session and Supabase MCP OAuth

---

## Quick Start

### macOS / Linux (Bash)
```bash
# Prerequisites: git, curl or wget, gh CLI (optional, for push)
# One-time: gh auth login (user's terminal, opens browser)

# Usage
bash .github/project-v7-1-setup/setup.sh \
  --project-name my-claude-ai \
  --models claude \
  --github-user your-username \
  --root ~/projects/my-claude-ai

# Output: Project initialized, ready to push
```

### Windows (PowerShell)
```powershell
# Prerequisites: PowerShell 5.1+, git, gh CLI (optional)
# One-time: gh auth login

# Usage
.\\.github\project-v7-1-setup\setup.ps1 `
  -ProjectName "my-claude-ai" `
  -Models @("claude") `
  -GitHubUser "your-username" `
  -ProjectRoot "C:\projects\my-claude-ai"

# Output: Project initialized, ready to push
```

### Multi-Model Example
```bash
# Initialize for both Claude and Qwen
bash setup.sh \
  --project-name multi-ai \
  --models claude qwen \
  --github-user username \
  --root ~/projects/multi-ai
```

---

## What It Does

1. **Fetches v7.1 Governance** (Public GitHub, no auth)
   - Master Profile (DCSE_Master_Profile_v7.1.md)
   - All 22 Doctrines (D01-D22)

2. **Generates Model Instructions**
   - Claude, Qwen, Codex, ChatGPT
   - Task intake patterns per model
   - Authority & approval rules
   - Incident response procedures

3. **Creates Project Structure**
   - `.claude/model-instructions/` — model-specific guidance
   - `governance/v7.1/` — fetched governance docs
   - `onboarding/model-manifests/` — project metadata per model
   - `.gitignore` — prevents secret commits
   - `README.md` — project overview

4. **Initializes Git**
   - Stages files
   - Commits with message: `"v7.1 Setup: <project-name> initialized for <models>"`
   - Ready to push

---

## Parameters

### Required
- `--project-name` (Bash) or `-ProjectName` (PowerShell)  
  Project identifier (e.g., `my-claude-ai`)

- `--models` (Bash) or `-Models` (PowerShell)  
  Space-separated list: `claude qwen codex chatgpt`

- `--github-user` (Bash) or `-GitHubUser` (PowerShell)  
  GitHub username (used to build repo URL)

- `--root` (Bash) or `-ProjectRoot` (PowerShell)  
  Local directory path (will be created if missing)

### Optional (Bash)
- `--help` — Show usage help
- `DEBUG=1` — Enable debug output

---

## Output Structure

```
<project-root>/
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
│   │   │   ├── D02_Doctrine.md
│   │   │   └── ... D03-D22
│   │   └── schemas/
│   └── .governance-registry.json
├── onboarding/
│   ├── FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE.md
│   ├── model-manifests/
│   │   ├── claude-manifest.json
│   │   └── ... qwen, codex, chatgpt
│   └── onboarding-checklist.md
├── .gitignore
├── README.md
└── .git/
```

---

## Security & Privacy

✅ **No Secrets Embedded**
- GitHub reads use public URLs (no PAT in command)
- GitHub writes use user's existing `gh auth login` session
- Supabase auth uses MCP OAuth (transparent, user-initiated once)

✅ **Secrets Protection**
- `.gitignore` blocks `.env`, `*.key`, `*.pem`, `settings.local.json`
- Setup script never logs API keys or credentials
- All auth flows happen in user's browser

✅ **Audit Trail**
- Each project tracked in Supabase `projects` table
- Governance doctrines indexed (with checksums)
- All task events logged automatically

---

## Next Steps (After Setup)

### 1. Push to GitHub
```bash
cd <project-root>
git push -u origin claude/project-v7-1-setup-l2t95z
```

### 2. Create Pull Request
```bash
# Automatic (via gh CLI, if logged in)
gh pr create --draft \
  --title "v7.1 Setup: <project-name>" \
  --body "Project initialized for $(cat .claude/model-instructions/* | grep 'Model:' | cut -d: -f2 | tr '\n' ',')"

# Or: Create manually in GitHub UI
```

### 3. Register with Supabase SC-Command-Post
- Claude will insert records into:
  - `projects` table (project metadata)
  - `project_models` table (model mappings)
  - `governance_registry` table (doctrine checksums)

### 4. Start Task Intake
- Project polls `project_plans` table every 30 seconds
- First task triggers FIRST_ASSIGNMENT_READINESS_AND_FAIL_FAST_GATE
- Tasks route to assigned model(s)

### 5. Monitor
- View task status: Supabase `project_plans` table
- Check governance compliance: `governance_registry` table
- Incident log: `governance_violations` table

---

## Troubleshooting

### "git: command not found"
Install git: https://git-scm.com/download

### "curl: command not found" (Bash only)
Install curl or wget, or use PowerShell version instead

### "gh: command not found" (optional, for push)
Install GitHub CLI: https://cli.github.com/

### "Permission denied" (Bash setup.sh)
Make script executable:
```bash
chmod +x .github/project-v7-1-setup/setup.sh
```

### Governance fetch failed
- Verify internet connection
- Check firewall (raw.githubusercontent.com must be accessible)
- Verify branch name: `governance/v7.1-owned-product-harness`

---

## Design Details

For full architecture documentation, see:  
[Project_v7.1_Setup_Architecture.md](../../../docs/Project_v7.1_Setup_Architecture.md)

Key points:
- 4-layer architecture (Governance → Auth → Scaffolding → Supabase)
- Credential-safe by design (no secrets in scripts)
- Reusable for Claude, Qwen, Codex, ChatGPT projects
- Fully automated (human-free after setup)

---

## Support

**Questions?** Contact DCS Level 0: sonlyconsulting@gmail.com

**Issues?** File a GitHub issue in the project repo

**Contributing?** Submit a PR with improvements (follow v7.1 governance)

---

**Auto-generated by Project v7.1 Setup** | v1.0
