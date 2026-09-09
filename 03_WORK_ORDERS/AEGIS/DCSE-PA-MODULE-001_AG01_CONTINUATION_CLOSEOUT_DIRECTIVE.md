# AEGIS ANTIGRAVITY AG01 CONTINUATION AND CLOSEOUT DIRECTIVE

**Task ID:** DCSE-PA-MODULE-001-AG01  
**Parent:** DCSE-PA-MODULE-001  
**Lane:** DCSE / Command Post  
**Worker:** Antigravity  
**Branch:** `feature/aegis-antigravity-slice001`  
**Status:** CONTINUE CURRENT WORK ONLY  
**Purpose:** Finish the already-started Aegis Slice 001 implementation safely, create a clean evidence-backed checkpoint, and hand it to Codex for independent reconciliation into the current ESCD architecture.

## 1. Current reported state to verify

DCS reports the local active branch is `feature/aegis-antigravity-slice001` and that the implementation files are created but not yet committed or pushed. AG reports Pass 1 currently has seven failing tests and four evidence documents remain to be produced.

Treat this as REPORTED, not VERIFIED, until local preflight confirms it.

Before mutation run:

```text
git rev-parse --show-toplevel
git branch --show-current
git status --short
git stash list
git worktree list
git log -5 --oneline --decorate
```

Required result: active branch is exactly `feature/aegis-antigravity-slice001` and all changed/untracked files relevant to this task can be identified as AG01-owned work.

If another worker is active on the same worktree, ownership is unclear, or the branch differs, STOP with `BLOCKED_STATE_RECONCILIATION`.

Do not switch branches for this task.

## 2. Scope freeze

This directive is a CLOSEOUT directive, not a new feature assignment.

AG SHALL NOT:

- rename Aegis to ESCD;
- integrate the newer ESCD rule/policy package from another branch;
- add new product features;
- expand DCS Employment logic;
- remove or redesign existing mission surfaces;
- create another branch;
- cherry-pick, rebase, merge, or force-switch;
- stash/reset/clean to simplify the workspace;
- modify poller/dispatcher work under AG02;
- modify governance;
- apply database migrations to live Supabase;
- deploy or merge to main.

The goal is to preserve and finish the current implementation checkpoint so Codex can independently classify it as REUSE / REPAIR / REFACTOR / SUPERSEDE / DEFER against current ESCD contracts.

## 3. Seven reported failures are hypotheses, not conclusions

AG MUST NOT assume a failing test is a test bug merely because the implementation appears correct.

For each failing test, first classify:

- `TEST_DEFECT`
- `IMPLEMENTATION_DEFECT`
- `BOTH`
- `REQUIREMENT_AMBIGUITY`

Then record evidence.

### F1. Scoring reproducibility, object equality

If the implementation returns structurally equal deterministic results and the test incorrectly uses reference equality (`strictEqual`) instead of structural equality, repair the test to `deepStrictEqual` or equivalent.

Do not change implementation merely to satisfy an invalid identity-comparison test.

### F2-F5. Desktop viewport, Android/mobile viewport, keyboard navigation, branding colors

Do not assume these are test-extraction defects until the rendered/embedded HTML/CSS actually satisfies each requirement.

Verify independently:

- viewport meta exists and is correct;
- responsive/mobile media behavior exists;
- keyboard/focus semantics or focus-visible behavior exists at the required baseline;
- DCS branding tokens required by the controlling packet are present in the implementation surface;
- the test harness can deterministically extract the HTML/CSS being asserted.

If implementation satisfies the requirement but the test cannot access the rendered string/module correctly, repair the test harness.

If implementation is missing the requirement, repair implementation and retain/strengthen the test.

### F6. Stale job handling

Treat this as potentially an IMPLEMENTATION DEFECT until proven otherwise.

Verify the controlling stale-job rule and exact boundary semantics. Test at least:

- just below stale threshold;
- exactly at threshold;
- just above threshold;
- no timestamp;
- future timestamp if malformed data permits it;
- deterministic behavior for the same evaluation time.

Do not alter the assertion merely to match current code. Repair whichever side contradicts the governing requirement.

### F7. Duplicate scoring reproducibility case

Apply the same evidence-first classification as F1.

## 4. Continuous repair loop

Execute without asking DCS again unless a material Stop-Gate occurs:

`reproduce -> classify -> minimum repair -> run affected test -> run full suite -> inspect regressions -> repair -> rerun full suite`

Required target for AG01 closeout:

- zero unexplained test failures;
- no P0/P1 defects left undispositioned;
- no acceptance criterion weakened to manufacture a pass;
- no test deleted solely because it fails;
- no implementation change outside Slice 001 scope.

If any test cannot be made valid without changing architecture or current product scope, classify `PARTIAL` and document the exact conflict for Codex.

## 5. Additional mandatory closeout checks

Before evidence generation, verify:

### Security

- service-role or privileged credentials are not in client/browser code;
- no secrets are committed;
- RLS migration is additive and deny-by-default as intended;
- no user-editable metadata is used as the sole authorization boundary;
- rollback SQL is explicit and non-destructive to unrelated schemas;
- migration was NOT applied to production in this task.

### Seed/test data

If `001_aegis_schema.sql` contains seed data, prove it is explicitly labeled and safe for development/test use. It must not fabricate authoritative DCS operational state or silently become production data.

### API/SPA

Verify the listed routes actually map to implemented handlers and that route-not-found, unauthorized, malformed input, and internal error paths fail safely.

### Evidence/completion

A UI transition, HTTP 200, model statement, or queued operation is not completion evidence. Keep the existing evidence/receipt distinction.

## 6. Required evidence documents

Complete exactly these AG01 documents:

- `apps/aegis/docs/ANTIGRAVITY_IMPLEMENTATION_REPORT.md`
- `apps/aegis/docs/ANTIGRAVITY_TEST_EVIDENCE.md`
- `apps/aegis/docs/ANTIGRAVITY_SECURITY_REVIEW.md`
- `apps/aegis/docs/ANTIGRAVITY_HANDOFF.md`

The handoff MUST include:

- exact branch;
- final commit SHA after commit;
- complete changed-file list;
- test command(s) and exact pass/fail counts;
- the seven original failures and their final classification;
- implementation defects repaired;
- test defects repaired;
- remaining P0/P1/P2/P3 defects;
- migrations present and whether applied;
- secrets/security scan result;
- VERIFIED / LIKELY / UNKNOWN;
- Google OAuth remaining external configuration as PARTIAL if still unverified;
- rollback procedure;
- explicit statement: no merge, no production deployment, no live DB migration.

## 7. Commit discipline

After all allowed repairs and evidence are complete:

1. run `git status --short`;
2. explicitly stage only AG01-owned files;
3. inspect `git diff --cached`;
4. ensure no unrelated Tribunal, DDNA, Codex, nested-repository, secret, or local-environment file is staged;
5. commit one coherent AG01 checkpoint;
6. report the SHA;
7. do not merge or deploy.

Do not stage the entire repository with an indiscriminate command if unrelated untracked content exists.

## 8. Relationship to current ESCD work

This branch is now a historical implementation input to ESCD, not current product authority.

Current ESCD specifications, rule sets, policy code, DCS Employment separation, and poller work exist on other controlled branches. AG01 SHALL NOT reconcile those differences itself during closeout.

Codex/senior review will compare the committed AG01 checkpoint against the current ESCD contracts and decide which elements are retained or changed.

This prevents losing valid implementation while avoiding uncontrolled cross-branch convergence by Antigravity.

## 9. Poller AG02 dependency

`DCSE-ESCD-001-AG02` poller/dispatcher work is DEFERRED on this shared worktree until AG01 reaches a clean committed handoff or a controller provides a separate approved worktree.

Do not switch from AG01 into `feature/escd-poller-ag02` as part of this assignment.

## 10. Stop-Gates

Stop only for:

- branch/worktree ownership conflict;
- missing controlling requirement needed to decide a failing test;
- unresolved P0 security/data-integrity defect;
- required architecture change;
- credential/auth/permission requirement;
- live production change requirement;
- destructive operation;
- protected-lane conflict;
- inability to produce a clean isolated AG01 commit.

Minor implementation/test repairs inside the existing Slice 001 contract should be completed without another DCS interruption.

## 11. Terminal states

Return only one:

- `READY_FOR_CODEX_REVIEW`
- `PARTIAL`
- `BLOCKED`

Do not use `COMPLETE`, `PRODUCTION_READY`, or `RELEASED`.
