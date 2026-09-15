# Antigravity brief: import and reconcile the delegation layer

    Supersedes: the recovery brief of the same date.
    Reason:     its central premise was false. Detail in section 0.
    Scope:      import, reconcile, branch, push, open a PR. No execution of
                queued work.

---

## 0. What changed from the recovery brief, and why

The earlier brief instructed a search of three local directories for delegation
files, on the understanding that Claude Desktop's work existed in an unpushed
local worktree.

**It does not, and it never did.** Claude ran in an isolated cloud container
with no folder connected from the laptop and no GitKraken authentication. It has
never had write access to that disk. The phrase "I could not push" was read as
"the work is local but unpushed"; the work is neither. It exists as a zip file
delivered into the chat.

Following the recovery brief produces one guaranteed outcome: three directories
inspected, no delegation files found in any of them, stop condition "Claude's
reported delegation files cannot be located" triggered, run ends. It fails
safely, which is to the credit of its stop conditions, and it fails.

**So this is an import, not a recovery.** No forensics. The source is a file
DCS provides.

Everything else in the recovery brief stands and most of it is carried forward
verbatim below, including two findings that improve on what Claude built.

## 1. Source of truth for the import

DCS provides `dcse-orchestrator.zip`. That archive is the whole delegation
layer. There is no second copy and nothing to reconstruct.

Before anything else, record the archive's SHA-256. Every later claim about
what was imported refers back to it.

Do not search `~/Projects/DCSE-App-MVP`, `~/sc-cp-deploy` or
`~/DCSE_WSL_WORKTREES/codex-wsl-runtime` for delegation files. Those were
reported as candidate locations of the canonical clone, not of the work. You
still need one of them, or a fresh clone, as the working tree.

## 2. Canonical repository

    sonlyconsulting-ctrl/DCSE-Command-Post
    main at handoff: 4ccc95d0604b7904655d270bf6bf86ff897debd0

Verify remote `main` before branching and use the SHA you verified, not the one
quoted here. The quoted value is a handoff reference and may already be stale.

## 3. Authentication

GitKraken authentication is not an architectural dependency. If the GitKraken
CLI is already authenticated it may be used. Otherwise use any authorized
GitHub write path available to you. Do not stop solely because
`gk auth login` has not been run.

Never print or expose credentials, tokens or secrets.

## 4. The baseline, which the earlier brief got subtly wrong

`baseline.json` is a benchmark scorecard of **this package's own rule engine**.
It can only be generated where this package's code exists, so it cannot come
from an unmodified canonical `main` that does not contain the package.

The correct meaning of unmodified here is **the package exactly as delivered,
before any reconciliation edits.**

    unzip to a scratch directory
    cd into it
    python -m dcse bench --save baseline.json
    record the file hash

A baseline generated after your edits proves nothing, which is the point the
earlier brief was reaching for.

The archive already contains a `baseline.json` generated in the container. Treat
it as a cross check rather than as authority: regenerate, and report if the two
disagree, because a disagreement means the environments differ in a way worth
knowing about.

## 5. Rule id collision, the risk nobody has named

This package registers generic ids: `TASK-01` through `TASK-08`, `IDEA-01`,
`ASSET-01`, `DDNA-01`, `KN-01`, and capability ids `ESCD`, `VOICE`, `SB`, `GH`,
`DEP`, `FILE`, numbered from 01.

The operative Rules Engineering baseline reportedly carries 148 rules including
entity sets for the same five entities. Collision is close to certain.

The registry raises `DuplicateRuleId` rather than overwriting, so a collision
fails loudly at import and nothing is silently replaced. That is the protection
working. When it fires:

- Do not rename the operative rule.
- Namespace the imported one instead, and report every id you changed.
- Do not resolve a collision by dropping either rule.

## 6. Preserve before changing

Capture an inventory before mutating anything: current branch, HEAD, upstream,
`git status --short`, untracked files, and local commits not present upstream,
for whichever working tree you select.

If a candidate tree holds uncommitted work of any kind, preserve it and report
it. Do not reset or clean to make room.

## 7. Reconciliation, and what the packets now say

The packets in the archive already carry a reconciliation state, because the
earlier brief's finding was correct and has been implemented. Computed risk says
whether work is safe. It cannot say whether work is still wanted, and a DCS hold
is the second kind of reason.

    T-001  HOLD_DCS          deployment architecture paused
    T-002  READY             write the five missing rule tests
    T-003  HOLD_DCS          same hold, presumes an undecided orchestrator placement
    T-004  STALE_RECONCILE   written before the Rules Engineering promotion

A packet in any blocking state returns ESCALATE regardless of how reversible its
work is, and the queue refuses to mark it runnable. The vocabulary is
`READY`, `HOLD_DCS`, `STALE_RECONCILE`, `SUPERSEDED`, `BLOCKED`, and a blocking
state with no note is rejected as invalid, because a hold nobody can read is
indistinguishable from a hold nobody meant.

`status: done` is rejected outright in a packet. Done is established by
execution evidence, not by a field being set. That is TASK-06 applied to the
delegation layer itself.

**Execute none of T-001 through T-004 in this operation.** Only T-002 is even
eligible and it is still out of scope here.

## 8. Rule staging: report what the code does, not more

The implemented distinction has two values, `plan` and `evidence`, plus `both`
as the default. A rule marked `evidence` is skipped when a task packet is
evaluated, because a diff scan needs a diff and a runtime probe needs a
deployment, and asking those questions beforehand yields UNKNOWN, which
escalates, which was making every delegable task require a human for a question
nobody could have answered yet.

The earlier brief proposed four phases: precondition, execution, postcondition,
audit. That is a better model and it may well be where this ends up. **It is not
what the code does.** The brief's own instruction applies: do not generalize
beyond what the implementation and tests support. Import two stages, report the
four phase proposal as a recommendation, and let DCS decide whether to widen it.

Seven rules are marked `evidence`: `GH-05`, `DEP-05`, `ASSET-03`, `ASSET-04`,
`ASSET-07`, `FILE-01`, `FILE-02`, `SB-01`, `VOICE-05`.

## 9. Branch and placement

Do not write to `main`.

    git fetch origin
    git rev-parse origin/main          # verify, then branch from this
    git switch -c antigravity/delegation-layer-import-20260914 <verified sha>

Placement: the package is self contained and runs as `python -m dcse`. Keep its
internal layout intact rather than redistributing files to match an expected
shape. If its layout differs materially from what the repository expects,
preserve it and report the difference rather than reorganising it.

Push the branch. Open a PR to `main`. Do not merge.

## 10. Validation, with the expected result for each

Run each and report the actual output, pasted, not summarised.

| # | Check | Expected |
|---|-------|----------|
| 1 | archive sha-256 recorded | a value, matched against what DCS sent |
| 2 | `git remote -v` on the selected tree | `sonlyconsulting-ctrl/DCSE-Command-Post` |
| 3 | `git rev-parse origin/main` | a sha, quoted in the report |
| 4 | `python -m dcse test` | 60 rules, 127 cases, 0 failures |
| 5 | `python -m dcse bench` | 5 scenarios, 21 steps, score 1.00 |
| 6 | `python -m dcse bench --against baseline.json` | nothing moved |
| 7 | `python -m dcse tasks` | 4 packets, only T-002 marked runnable |
| 8 | `python -m dcse inventory` | 60 rules, all lifecycle candidate |
| 9 | `python -m dcse demo` | REFUSE, DEP-02, before any platform call |
| 10 | rule id collisions against the operative set | listed, namespaced, none dropped |
| 11 | operative rules downgraded to candidate | none, and say so explicitly |
| 12 | PR opened, not merged | number and URL |

Item 8 matters and is easy to misread as a failure. Every rule ships in
candidate, which means the imported package refuses nothing until someone
promotes it deliberately. That is the shadow gate and it is correct.

Item 6 fails if you generate the baseline after editing. Generate it first.

## 11. Stop and report rather than improvise

- No candidate tree maps to the canonical repository and a fresh clone is not
  possible.
- The archive is missing, truncated, or its hash does not match.
- Local changes in the selected tree would be lost by proceeding.
- No authorized GitHub write path exists at all.
- A rule id collision cannot be resolved by namespacing the imported rule.
- Reconciliation would require changing L0 authority or doctrine rather than
  importing a framework.

## 12. Report

    archive sha-256
    working tree selected, and why
    remote url
    original branch and HEAD, with any preserved local work
    canonical main sha verified at branch time
    branch name and commit sha
    PR number and url
    files imported, and any id namespaced
    every validation row above with its actual output
    baseline location and hash, and whether it matched the shipped one
    disposition of T-001 through T-004 as found, unchanged
    anything you were about to do and stopped because a rule or a hold refused it

The last line is the one most often left out and the most useful. A run with
nothing in it either did nothing consequential or did something consequential
without noticing.
