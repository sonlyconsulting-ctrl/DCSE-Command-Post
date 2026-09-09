# ESCD ANTIGRAVITY STATE RECONCILIATION ADDENDUM

**Task ID:** DCSE-ESCD-001-AG02  
**Parent:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Applies to:** `DCSE-ESCD-001_ANTIGRAVITY_POLLER_CONTROL_PACKET_002.md`  
**Status:** CONTROLLING PRE-EXECUTION ADDENDUM

## Reason

The local DCSE repository has been handed back and forth between Antigravity and Codex during the Aegis/ESCD work. Therefore the current local branch, worktree, stash, and uncommitted ownership state MUST NOT be inferred from historical Antigravity evidence or from remote GitHub branch existence.

Remote GitHub currently contains the historical branches `feature/aegis-antigravity-slice001` and `feature/aegis-executive-kernel` plus the controller-created `feature/escd-poller-ag02`. Remote branch existence does not prove the local workspace is safe to switch.

## Superseding preflight rule

Before following any branch-switch instruction in Packet 002, Antigravity MUST perform STATE RECONCILIATION ONLY.

Run and report, without mutation:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git stash list
git worktree list
git log -5 --oneline --decorate
git reflog -10 --date=iso
```

Also inventory untracked files under the repository root and identify whether any changed/untracked file appears to belong to prior Aegis/ESCD, Codex, Antigravity, Tribunal, or DDNA work.

## No-switch-until-reconciled rule

Antigravity MUST NOT switch branches merely because the worktree appears superficially clean.

It may switch to `feature/escd-poller-ag02` only when ALL are true:

1. current branch and latest handoff state are identified;
2. `git status --short` is clean;
3. no untracked nested-repository or sub-worktree artifact would be displaced;
4. no unresolved prior Codex/Antigravity implementation ownership is present;
5. historical stash `pre-aegis-slice001-stash`, if present, is preserved untouched;
6. the target branch is not checked out in another worktree;
7. no active Codex process or other worker is operating on the same worktree;
8. the switch can be performed with ordinary `git switch`, without force, stash, reset, clean, checkout overwrite, or file movement.

If any condition is unknown, STOP with `BLOCKED_STATE_RECONCILIATION` and report the smallest concrete action needed.

## Worker handoff ownership classification

Before mutation, classify each visible changed/untracked work surface as exactly one of:

- `CODEX_OWNED_ACTIVE`
- `ANTIGRAVITY_OWNED_ACTIVE`
- `PRESERVED_SHARED_BASELINE`
- `HISTORICAL_STASH_OR_EVIDENCE`
- `UNRELATED_NESTED_REPOSITORY`
- `UNKNOWN_OWNER_STOP`

Antigravity may not alter, stash, move, commit, delete, or absorb anything classified `CODEX_OWNED_ACTIVE`, `HISTORICAL_STASH_OR_EVIDENCE`, `UNRELATED_NESTED_REPOSITORY`, or `UNKNOWN_OWNER_STOP`.

## Dedicated AG02 surface preference

If the current repository state is safe but branch switching would disturb another worker's workspace, prefer a separately controlled worktree for the already-created branch rather than taking over the shared worktree. Antigravity MAY NOT invent the worktree path or create one unless the controller provides the exact path or the current repository already defines an approved worker-worktree convention.

## Required reconciliation output

Return this block before executing Packet 002:

```text
STATE_RECONCILIATION
TASK_ID: DCSE-ESCD-001-AG02
REPO_ROOT:
CURRENT_BRANCH:
HEAD:
WORKTREE_STATUS:
OTHER_WORKTREES:
STASHES_PRESENT:
PRE_AEGIS_STASH_PRESENT: YES | NO
ACTIVE_CODEX_PROCESS_DETECTED: YES | NO | UNKNOWN
ACTIVE_AG_PROCESS_DETECTED: YES | NO | UNKNOWN
CHANGED_OR_UNTRACKED_SURFACES:
OWNERSHIP_CLASSIFICATION:
SAFE_TO_SWITCH_TO_AG02: YES | NO
WHY:
SMALLEST_UNBLOCK_ACTION:
```

Only `SAFE_TO_SWITCH_TO_AG02: YES` permits the normal Packet 002 execution sequence to continue.

## Authority

This addendum narrows execution. It does not authorize branch creation, forced switching, stash manipulation, production changes, Supabase mutation, RLS changes, deployment, merge, or any Codex-owned Aegis/ESCD modification.
