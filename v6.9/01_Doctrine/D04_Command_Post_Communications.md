# DCSE Doctrine D04: Command Post Communications

**Document ID:** DCSE-D04  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T19:27:00-04:00
**Last Version/Release Date/Time:** 2026-06-21T15:22:37-04:00  
**Status:** DCSE Authorized version Pending Approval  
**Classification:** INTERNAL  
**Lane:** DCSE  
**Canonical file:** D04_Command_Post_Communications.md  
**Doctrine Description:** The Command Post Communications Doctrine (D04) regulates the local and remote exchange of operational state packets. It defines the structured JSON schemas utilized in the 05_Tribunal_Inbox communications bus and details the headless Git synchronization rules mapping local state to private remote repositories. By governing polling intervals, conflict resolution rules, and status flag updates, this doctrine ensures real-time operational coordination between distributed agents and command systems.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. Dual Inbox Architecture

The DCSE ecosystem operates two distinct Tribunal Inbox locations. Both are active. They serve different functions and must never be conflated.

### 1.1 Operational Inbox (Daemon-Monitored)
```
C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox
```
This is the live relay. The poller daemon watches this path. All active `TRIBUNAL_*.json` files live at its root for immediate poller detection. Subdirectories `_Daily\YYYY-MM-DD\` and `_Weekly\YYYY-W##\` hold dated snapshots and DCS interjection logs for human review. This inbox is separate from the v6.9 Hub and is not governed by the 14-directory layout. It is the operational nerve center — write here when a packet needs immediate poller pickup.

**Live editing rule:** modify root-level `TRIBUNAL_*.json` files directly to trigger poller detection. Do not move active files into dated subfolders until the packet status is `Completed` or `Archive`.

### 1.2 Hub Inbox (Doctrine-Structured)
```
C:\DS All Things\DCSE_Command_Center\v6.9\05_Tribunal_Inbox
```
This is the v6.9 Hub's structured packet bus. It receives STOPGATE files, ERR_MISSING_DOCTRINE logs, DDNA Surface Notices, and model update reports per D03 Sections 5.3, 8.3, and D16 Section 9. It is governed by the 14-directory layout (D06). It is not daemon-monitored by default — it is a receipt and alert layer for the doctrine ecosystem.

**Write rule:** agents writing compliance packets, error logs, or doctrine impact reports target the Hub Inbox. Agents writing operational coordination packets, task relay instructions, or active session packets target the Operational Inbox.

### 1.3 Packet Schema (Both Inboxes)
Every packet must contain:

```json
{
  "packet_id": "TRIBUNAL-[YYYYMMDD]-[AGENT]-[SHORT_LABEL]",
  "timestamp": "[ISO 8601 UTC]",
  "sender_id": "[model or agent name]",
  "target_inbox": "OPERATIONAL | HUB",
  "priority": "High | Standard | Low",
  "status": "Pending | Active | Completed | Blocked",
  "lane": "SC | SS | PS | DCSE | EMP | CROSS",
  "payload": {}
}
```

`target_inbox` is required so any agent reading a packet knows which system produced it and where the response should route.

---

## 2. GitHub Operations

This section governs all Git push, pull, branch, and conflict operations across the DCSE ecosystem. Agents that interact with GitHub must follow these rules exactly. Ambiguous Git operations are a compliance failure, not a judgment call.

### 2.0 Model-to-Source Routing Table

This table is the first thing any frontier model reads before any pull, file load, or session open action. It answers exactly one question: **where do I get my doctrine from?**

Every model has a designated access method based on whether it can execute git commands directly (CLI-capable) or must receive files through an upload interface (web-bound). No model guesses its source. No model defaults to pre-training knowledge when this table is available.

| Model | Interface Type | Primary Source | Branch | Fallback Source | Upload Path |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Claude (CTO)** | CLI / API | `git pull origin v69` | `v69` | Local: `v6.9\01_Doctrine\` | N/A — CLI access |
| **Gemini** | Web / API | GitHub raw file URL | `v69` | Operator upload | `01_Doctrine\` files uploaded to Gem |
| **ChatGPT** | Web / Custom GPT | Operator upload | `v69` | GitHub raw URL | `01_Doctrine\` files uploaded to GPT |
| **Qwen Coder** | CLI / API | `git pull origin v69` | `v69` | Local: `v6.9\01_Doctrine\` | N/A — CLI access |
| **Codex / o-series** | API | `git pull origin v69` | `v69` | Local: `v6.9\01_Doctrine\` | N/A — CLI access |
| **NotebookLM** | Web upload only | Operator upload | `v69` | N/A | `01_Doctrine\` files uploaded as sources |
| **Any new model** | Confirm before use | Operator assigns | `v69` | Halt until confirmed | N/A until confirmed |

**Branch rule:** all models pull from `v69` until the operator promotes to `main`. When `main` is promoted, this table is updated and all models switch to `main`. No model pulls from `dev` or `feature/` branches — those are write-only for agents.

**GitHub raw URL pattern for web-bound models:**
```
https://raw.githubusercontent.com/sonlyconsulting-ctrl/DCSE-Command-Post/v69/v6.9/01_Doctrine/D03_AI_Orchestration.md
```
Replace the filename to access any doctrine file directly. Web-bound models that cannot git pull use this URL pattern to fetch the latest committed version of any doctrine file.

**Staleness rule:** if a web-bound model's uploaded files are older than the last commit on `v69`, the model must notify the operator before proceeding. A model operating on stale doctrine is non-compliant. The operator re-uploads the updated files before the session continues.
### 2.10 v69 Candidate Mirror Rule

The `v69` branch of `DCSE-Command-Post` is the candidate-published mirror of the approved local v6.9 Hub. After DCS Level 0 approval, the mirror scope includes the full Git-eligible local `C:\DS All Things\DCSE_Command_Center\v6.9\` tree, including support, review, archive, receipt, and auxiliary source folders required for doctrine reconciliation.

The candidate mirror does not create promotion authority. `main` remains stable/promoted only after a separate DCS decision under D05. The `v69` branch is reviewable candidate evidence and source distribution, not final doctrine authority by existence.

Permanent no-Git exclusions in Section 2.6 still control. Credentials, quarantine files, and PS litigation material do not enter GitHub merely because they exist inside or near the local Hub. If a requested full-tree mirror encounters an excluded file, the agent records the exclusion in the Tribunal receipt and continues with the Git-eligible mirror set unless DCS issues a separate explicit override and safe repository destination.

Mirror verification must compare path coverage and content equivalence for all Git-eligible files. Text files may be normalized for CRLF/LF line endings during Git transport, but substantive content drift is non-compliant and requires a `TRIBUNAL_DOCTRINE_DRIFT_[...]` packet before further pushes.

### 2.1 Repository Map

| Repository | Purpose | Primary Branch | Agent Write Access |
| :--- | :--- | :--- | :--- |
| `DCSE-Tribunal-Relay` | Operational Inbox sync relay | `main` | Poller daemon only |
| `DCSE-CP-Project` | SC lanes, product assets, Command Post | `main` | Claude (CTO), Qwen (validation) |
| `DCSE-v6.9-Doctrine` | v6.9 Hub doctrine files (D01-D16) | `main` | Claude (CTO) only |

If a repository is not listed here, no agent may push to it without explicit Level 0 operator authorization. Authorization does not carry over to unlisted repos.

### 2.2 Branch Strategy

```
main          → Stable, promoted, human-approved state only.
               Nothing merges to main without Level 0 sign-off.

dev           → Active agent work in progress. All agent commits
               land here first. Claude, Qwen, Gemini write to dev.

feature/[label] → Isolated work on a specific lane, doctrine file,
                  or product (e.g. feature/d16-ddna, feature/ctj-html-v2).
                  Opened by operator or CTO agent. Merged to dev when
                  complete. Never merged directly to main.

hotfix/[label] → Urgent correction to main (e.g. STOPGATE resolution,
                 credential exposure patch). Requires Level 0 approval
                 before merge. Bypasses dev.

release/[vX.Y] → Staging branch for version promotion. Created from dev
                 when a baseline promotion (D05) is triggered. Merged to
                 main only after full pipeline audit.
```

**Rule:** no agent may push directly to `main` at any time for any reason. All agent work lands on `dev` or a `feature/` branch. The operator merges to `main`.

### 2.3 Push Protocol

Before any push, the agent runs this sequence:

```
1. Confirm branch is NOT main.
   git branch --show-current
   → If output is "main": STOP. Do not push. Alert operator.

2. Confirm working tree is clean (no unintended staged files).
   git status

3. Stage only the specific files changed in this session.
   git add [file1] [file2] ...
   → Never use "git add ." or "git add -A" without operator confirmation.
   → Never stage .env, credential files, or PS litigation material.

4. Commit with a structured message.
   git commit -m "[AGENT] [LANE] [ACTION]: [short description]
   Doctrine refs: [D03, D06, ...]
   Approval level: [0 | 1 | 2]"

5. Push to the correct remote branch.
   git push origin [branch-name]

6. Write a push receipt to the Operational Inbox.
   File: TRIBUNAL_GITHUB_PUSH_[YYYYMMDD]_[AGENT]_[LABEL].json
```

### 2.4 Pull Protocol

Before any agent begins work in a session, it must pull the latest state from the correct branch:

```
1. Confirm current branch matches the intended work branch.
   git branch --show-current

2. Fetch remote state without merging.
   git fetch origin

3. Check for upstream changes.
   git log HEAD..origin/[branch] --oneline
   → If changes exist: review before merging. Do not auto-merge.

4. Pull with rebase to keep history clean.
   git pull --rebase origin [branch]

5. If rebase conflicts occur:
   → Do NOT force-resolve. Write a conflict notice to the Operational Inbox.
   → File: TRIBUNAL_GIT_CONFLICT_[YYYYMMDD]_[AGENT]_[LABEL].json
   → Halt work on the affected files until operator resolves.
```

### 2.5 Conflict Resolution Rules

| Conflict Type | Rule |
| :--- | :--- |
| Agent vs Agent (same branch) | Local state wins. Remote is backed up to `10_Archive\Git_Conflicts\` before reset. |
| Agent vs Operator (any branch) | Operator state wins. No exceptions. Agent writes a conflict receipt and halts. |
| Doctrine file conflict | HALT all work on the affected doctrine file. Write ERR_DOCTRINE_CONFLICT to Hub Inbox. Operator resolves manually. |
| PS litigation file conflict | IMMEDIATE STOPGATE. Do not attempt resolution. Alert operator. |

### 2.6 What Never Goes Into Git

The following are permanently excluded from all repositories regardless of branch:

```
- .env files containing live credentials
- Supabase service role keys or anon keys (even rotated)
- Any file with PS litigation keywords in content or filename
  ("seals", "823cv489", "dart", "pro se") unless repo is explicitly
  the PS offline Spoke and is not synced to any cloud
- Files from C:\DS Litigation (offline Spoke — never touches Hub Git)
- __pycache__/ and .venv/ directories
- Any file flagged .QUARANTINE in the Operational Inbox
```

If a credential or PS file is accidentally staged, run:
```
git reset HEAD [file]   ← unstage before commit
git rm --cached [file]  ← remove if already committed
```
Then write a credential exposure notice to the Hub Inbox immediately.

### 2.8 Git-Tribunal Concurrency Rule (Hard Enforcement)

**Every GitHub push and every Tribunal receipt are a single atomic operation. They are never separated.**

This rule has no exceptions. An agent that pushes to GitHub without writing a Tribunal receipt has violated doctrine. An agent that writes a Tribunal receipt for a push that did not happen has violated doctrine. The two actions confirm each other — one without the other signals an incomplete or phantom operation.

**The enforcement sequence is fixed:**

```
STEP 1  Execute git push to correct branch (D04 Section 2.3)
STEP 2  Confirm push success (non-zero exit code = halt, write ERR packet, do not write receipt)
STEP 3  Write TRIBUNAL_GITHUB_PUSH_[YYYYMMDD]_[AGENT]_[LABEL].json to Operational Inbox
         _Tribunal_Inbox\ immediately after confirmed push
STEP 4  Apply identical change set to the local doctrine copy in v6.9\01_Doctrine\
         if the push contained doctrine modifications
STEP 5  Confirm local and remote doctrine files match exactly
         Any drift between local and GitHub = write TRIBUNAL_DOCTRINE_DRIFT_[...].json
         to Hub Inbox and halt further pushes until resolved
```

**Receipt must include at minimum:**
- Every commit hash pushed in this operation
- Every file changed, added, or deleted
- The branch and remote URL
- Doctrine refs governing the changes
- Open items or exclusions relevant to the push

**Change application rule:** if a push modifies any file in `v6.9\01_Doctrine\`, the identical modification must already be present in the local copy before the push is staged. GitHub is never ahead of local doctrine. Local doctrine is never ahead of GitHub. They move together or not at all.

**Pull concurrency:** the same rule applies in reverse. When a pull is executed and remote doctrine files differ from local, the local copies are updated to match before any session work begins. A pull that is not followed by local application is a compliance gap.

### 2.9 Poller Daemon Sync (Operational Inbox → GitHub)

The tribunal poller daemon syncs the Operational Inbox to `DCSE-Tribunal-Relay` on the following schedule:

- **Push trigger:** any new or modified root-level `TRIBUNAL_*.json` file in `_Tribunal_Inbox\`
- **Pull interval:** every 120 seconds
- **Branch:** `main` only (the relay repo has no feature branches — it is a state mirror, not a development repo)
- **Conflict rule:** local state wins; remote overwritten version is archived to `_Tribunal_Inbox\_Daily\[date]\conflicts\`

---

## Related Doctrine

- [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) - Error-catch and STOPGATE packets route to Hub Inbox (Section 5.3)
- [D05_Baseline_Promotion.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D05_Baseline_Promotion.md) - Release branch creation triggered by baseline promotion
- [D06_File_System.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D06_File_System.md) - 14-directory layout governs Hub Inbox (05_Tribunal_Inbox); Operational Inbox is outside Hub
- [D14_DART_PS_Protected.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D14_DART_PS_Protected.md) - PS litigation files are permanently excluded from all Git operations
- [D15_Database_Administration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D15_Database_Administration.md) - Credential safety rules enforced at Git staging gate (Section 2.6)

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
