---
dcse_zone: execution
dcse_subzone: instructions
dcse_authority_level: INSTRUCTION
dcse_document_id: CODER_GITHUB_AUTHENTICATION_RECOVERY_AND_PUSH_PROTOCOL
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: SC
dcse_policy_authority: false
---

# Coder GitHub Authentication Recovery and Push Protocol

Status: ACTIVE CONTROLLED USE SUBJECT TO CONTROLLING GOVERNANCE
Governance route: Master Profile, D21, D22, and applicable GitHub authorization
Applies to: Qwen Coder, Coder, Codex, Claude Code, and other approved implementation runtimes

## Purpose

Restore GitHub write access without exposing credentials in chat or creating an unauthorized authentication method.

## Canonical Target

Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`

The destination branch must be taken from the current authorized task or D22 reconciliation record. This instruction does not independently establish a canonical branch.

## Required Startup Checks

1. Confirm local repository path.
2. Confirm `.git` exists.
3. Run `git remote -v` and verify origin resolves to the authorized repository.
4. Run `git branch --show-current` and verify the authorized work branch.
5. Run `git status` and preserve unrelated changes.
6. Run `git fetch origin`.

## Approved Authentication Recovery Order

1. Existing Windows Git Credential Manager credentials.
2. GitHub MCP or approved OAuth connector.
3. GitHub CLI browser authentication using `gh auth login`.
4. Existing SSH key already registered to the approved GitHub account.
5. DCSE Control Plane or approved connector.

## Prohibited Methods

- Do not request or accept a PAT in chat.
- Do not print tokens, cookies, OAuth codes, SSH private keys, or credential-manager contents.
- Do not place credentials in repository files, shell history, logs, task packets, or Supabase.
- Do not create a new GitHub account or repository.
- Do not rewrite existing commits unless required by a proven conflict and authorized task scope.

## Push Procedure

After authentication succeeds:

```powershell
git remote -v
git branch --show-current
git status
git fetch origin
git log --oneline --decorate -10
git push origin HEAD
```

Then verify:

```powershell
git ls-remote origin $(git branch --show-current)
git rev-parse HEAD
```

The returned remote head and local HEAD must match.

## Failure Handling

If authentication cannot be completed in the current runtime:

1. Stop only the push step.
2. Return the exact local repository path.
3. Return the full 40-character SHA for every unpushed commit.
4. Return `git status`, current branch, and `git remote -v` output with secrets redacted.
5. Continue non-destructive baselining and evidence collection where authorized.
6. Use the connector-mediated publication fallback when its trigger conditions are satisfied.

## Runtime Update After Push

After GitHub confirms the remote commit:

- record the full remote commit SHA;
- record the verified destination branch;
- record the GitHub path for each artifact;
- mark the local-only blocker resolved;
- do not register a short SHA as canonical;
- reconcile task and governance registry records through D22.

## Completion Evidence

Return:

- authentication method used;
- repository path;
- destination branch;
- remote URL;
- local HEAD;
- remote HEAD;
- pushed commit list;
- GitHub verification result;
- runtime reconciliation result;
- unresolved blockers.

## Instruction Boundary

This instruction provides a safe authentication recovery procedure. It does not grant repository access, authorize a push, choose a branch, promote content, or override D22 source controls.