# SC / CTJ Canonicalization Receipt

**Task ID:** SC-CTJ-CANONICALIZATION-20260925-01  
**Lane / entity:** Sonly Consulting / The Critical Thinker's Journey  
**Authority:** DCS Level 0 approval received September 25, 2026  
**Status:** COMPLETE - canonical source promotion, repository rename, branch preservation, and GitHub reference verification complete  
**Handoff ID:** SC-CTJ-FAMILY-INTEGRATION-20260925-01

## Authorized decisions

1. Promote SCA PR #2 as the canonical implementation baseline.
2. Rename `CTJ-MVP-11252025` to `SC-CTJ`.
3. Establish `review/ctj-family-integration-20260925` from the promoted canonical baseline.
4. Preserve PR #1 as the Unified source line and reconcile it through the integration branch.
5. Do not deploy, cut over URLs, or activate production commerce through this decision.

## Preflight validation

- Repository admin, maintain, push, pull, and triage permissions: VERIFIED through the GitHub connector.
- PR #2 head: `1126363ff51eb8634d8887f30b128a4d956f32b9`.
- PR #2 mergeability before promotion: VERIFIED true.
- CTJ SCA CI workflow run `34711013061`: completed successfully.
- PR #2 moved from draft to ready for review before merge.
- DCS Level 0 promotion note recorded on PR #2 as comment `5837110035`.

## Completed actions and evidence

### Canonical SCA promotion

- PR #2 merged successfully.
- Merge commit: `7a70b28a54f83df9281f837d288f6a8c8fa691db`.
- Canonical scope includes the 31-question deterministic SCA, 10 / 10 / 11 independent dimensions, fixed scoring and tie handling, interludes, profile, pattern analysis, Immediate Blueprint, and Part 1/2/3 routing.
- AI remains excluded from official scoring.

### Family integration branch

- Created `review/ctj-family-integration-20260925`.
- Branch base: canonical SCA merge commit `7a70b28a54f83df9281f837d288f6a8c8fa691db`.
- No deployment was triggered or authorized.

### Repository rename

- Renamed `sonlyconsulting-ctrl/CTJ-MVP-11252025` to `sonlyconsulting-ctrl/SC-CTJ`.
- Stable repository ID remained `1104050729`.
- Default branch remained `main`.
- The former repository path resolves to `SC-CTJ`, verifying GitHub redirection.
- PR #1, merged PR #2, and all three review branches resolve under the new repository name.

### Unified PR preservation and conflict control

- PR #1 remains open and draft.
- After the SCA merge, GitHub reports PR #1 as not mergeable against updated `main`.
- A control note was added to PR #1 as comment `5837189837`.
- PR #1 must not be merged as-is. Its approved capstone changes are to be reconciled into the family integration branch while preserving the canonical SCA baseline.

## Reference audit

GitHub code search found the former name in historical Command Post audit and checkpoint records. Those records accurately describe the repository name at their original timestamps and are preserved rather than rewritten. The canonicalization receipt now supplies the current-name crosswalk.

No active source file or GitHub workflow reference requiring an immediate rename correction was identified in the returned search results. Netlify project linkage, local Git remotes, and non-GitHub automation remain separate runtime checks because they are not visible through the GitHub repository connector.

## Next-gate exit criteria

- Reconcile approved Unified changes from PR #1 into `review/ctj-family-integration-20260925` while preserving the canonical SCA baseline.
- Run the combined SCA, Unified, responsive, accessibility, and persistence validation suite.
- Verify Netlify repository linkage and any local Git remotes against `sonlyconsulting-ctrl/SC-CTJ` before a review deployment.
- Prepare the governed Claude Design package after the integrated branch passes.

## Release boundary

This receipt authorizes and records canonical source promotion only. It does not authorize public deployment, production URL changes, Stripe activation, entitlement changes, or release completion.
