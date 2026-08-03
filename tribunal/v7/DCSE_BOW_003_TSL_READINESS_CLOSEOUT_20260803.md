# BOW-003 TSL Production Readiness Closeout and Remediation Plan

**Task:** `V7_1_BOW_003_TSL_AUDIT_INVENTORY`  
**Recorded state:** Completed  
**Audit disposition:** `APPROVE_WITH_FINDINGS`  
**Production readiness:** `NON_PASS`

## Verified result

The recovered audit covers architecture, code quality, database policies, authentication, security, deployment, sports-data integrity, user experience, and commercial readiness.

- Branch: `bow3/tsl-production-readiness-audit`
- Head: `2f758b303d2383f3654b77559aa31ff024008a52`
- PR #36 merge: `98c52c2aadb3f3948b4c1a62d1d31f8c2a09ad20`
- Audit: `tribunal/v7/BOW-003_TSL_PRODUCTION_READINESS_AUDIT_20260803.md`
- Audit SHA-256: `b2b6c64754e20019ee2ee6af1ae3760dab2bf88406e3046749af89b64f7c3b18`
- Receipt SHA-256: `26af21774230fb1ec58796294b0b1b3f331ca050a4dbc2dcded8973341fabc6d`
- Review: `BOW-003-TSL-AUDIT-20260803-CODEX`, confidence `0.98`

At audit time, the system contained 70 auth users, 70 profiles, one global user, 31 teams, 110 events, 336 picks, and three contests. Stored events had unique external IDs and no missing start times, but sport coverage was limited to MLB, NBA, NHL, and UFL.

## Production blockers

1. `public.tsl_community_picks` exposes a security-definer view.
2. Exposed `SECURITY DEFINER` functions require privilege and search-path remediation.
3. Canonical application source is not reconciled into governed GitHub.
4. `profiles` and `global_users` create parallel identity models.
5. Parallel favorites models create divergent state.
6. Sports feed coverage and freshness are not established across active sports.
7. Deployment, observability, recovery, privacy, and commercial controls are incomplete.

## Build and remediation plan

1. Inventory every view and function reachable by `anon` and `authenticated`.
2. Convert views to security-invoker behavior or revoke inappropriate access.
3. Move necessary privileged functions to a non-exposed schema, constrain `search_path`, validate authorization, and revoke default public execution.
4. Import and designate the canonical application repository and branch.
5. Select one identity model and migrate dependent references.
6. Select one favorites model and migrate dependent references.
7. Implement feed freshness, coverage, error, and recovery monitoring by sport.
8. Establish deployment, rollback, privacy, support, and commercial baselines.

## Test plan

- RLS matrix for anonymous, authenticated owner, authenticated non-owner, administrator, and service roles.
- Negative invocation tests for every privileged function.
- Identity and favorites migration tests with no orphaned references.
- Sports provider contract, uniqueness, freshness, timezone, reschedule, cancellation, and recovery tests.
- End-to-end authentication, picks, contests, favorites, leaderboard, and account lifecycle tests.
- Build, deployment, rollback, monitoring, and incident-response tests.
- Supabase security and performance advisor review after database corrections.

## Approval and promotion gate

TSL is promotable only after all security blockers close, canonical source is governed, duplicate domain models are reconciled, active-sport coverage is defined and tested, release and rollback evidence is retrievable, and independent review returns an approving disposition against the exact promoted commit.

## Lessons learned

- Audit completion must not be reported as product readiness.
- Clean stored rows do not prove complete provider coverage.
- Privileged database objects require explicit authorization tests.
- Empty poller output must trigger recovery, not administrative completion.

## Current gate

**TSL audit complete. Production release blocked pending security, source, data-model, sports-feed, and release-control remediation.**
