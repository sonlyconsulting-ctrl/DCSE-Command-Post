# Coder GitHub Authentication Recovery and Push Protocol

Status: ACTIVE CONTROLLED USE
Governance: V7.1
Applies to: Qwen Coder, Coder, Codex, Claude Code, and other approved implementation runtimes

## Purpose

Restore GitHub write access without exposing credentials in chat or creating a parallel authentication method.

## Canonical target

Repository: sonlyconsulting-ctrl/DCSE-Command-Post
Branch: governance/v7.1-owned-product-harness

## Required startup checks

1. Confirm local repository path.
2. Confirm `.git` exists.
3. Run `git remote -v` and verify origin resolves to the canonical repository.
4. Run `git branch --show-current` and verify the canonical branch.
5. Run `git status` and preserve all unrelated changes.
6. Run `git fetch origin`.

## Approved authentication recovery order

1. Existing Windows Git Credential Manager credentials.
2. GitHub MCP or GitKraken OAuth.
3. GitHub CLI browser authentication using `gh auth login`.
4. Existing SSH key already registered to the approved GitHub account.
5. DCSE Control Plane or approved connector.

## Prohibited methods

- Do not request or accept a PAT in chat.
- Do not print tokens, cookies, OAuth codes, SSH private keys, or credential-manager contents.
- Do not place credentials in repository files, shell history, logs, task packets, or Supabase.
- Do not create a new GitHub account or repository.
- Do not rewrite the existing local commits unless required by a proven conflict.

## Push procedure

After authentication succeeds:

```powershell
git remote -v
git branch --show-current
git status
git fetch origin
git log --oneline --decorate -10
git push origin governance/v7.1-owned-product-harness
```

Then verify:

```powershell
git ls-remote origin governance/v7.1-owned-product-harness
git rev-parse HEAD
```

The returned remote head and local HEAD must match.

## Failure handling

If authentication cannot be completed in the current runtime:

1. Stop only the push step.
2. Return the exact local repository path.
3. Return the full 40-character SHA for every unpushed commit.
4. Return `git status`, current branch, and `git remote -v` output with secrets redacted.
5. Do not declare the Foundational Trilogy globally blocked.
6. Continue non-destructive baselining and evidence collection where authorized.

## Supabase update after push

After GitHub confirms the remote commit:

- record the full remote commit SHA;
- record the canonical branch;
- record the GitHub path for each artifact;
- mark the local-only blocker resolved;
- do not register a short SHA as canonical;
- reconcile the task and governance registry records.

## Completion evidence

Return:

- authentication method used;
- repository path;
- canonical branch;
- remote URL;
- local HEAD;
- remote HEAD;
- pushed commit list;
- GitHub verification result;
- Supabase reconciliation result;
- unresolved blockers.
