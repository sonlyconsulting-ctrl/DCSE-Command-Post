# DCSE Core Infrastructure Baseline 1.0 Plan

Date: 2026-08-14
Status: AUTHORIZED PLAN / EXECUTION REQUIRED
Lane: DCSE SYSTEM
Authority: DCS
Purpose: Establish and seal a known-good core infrastructure baseline before further infrastructure expansion. Autonomous poller/orchestration work is excluded from the core baseline and is deferred for later build/buy/hybrid/defer evaluation.

## DCS Direction

DCS approves the Core Infrastructure Baseline 1.0 plan and directs pursuit of the baseline before resuming poller work. The poller is classified as an optional automation layer and shall not determine whether core DCSE infrastructure is healthy or whether website/product builds can proceed.

## Baseline Architecture

Core authority and operational chain:

GitHub canonical source
-> Supabase operational state where required
-> Application/build artifact
-> Vercel production deployment where applicable

Tribunal is the evidence and reconciliation record proving that the surviving source, database, deployment, and governance states agree.

The poller, universal dispatch controller, runtime workers, autonomous claims, heartbeats, result convergence, and automatic recovery are OUT OF SCOPE for Core Infrastructure Baseline 1.0.

## Baseline Target

Core Infrastructure Baseline 1.0 reaches PASS when 100 percent of production-critical baseline controls are reconciled and there are zero UNKNOWN or VERSION-DIVERGENT conditions on the surviving production path.

Required control outcomes:

1. One canonical GitHub repository is identified.
2. One exact baseline GitHub commit SHA is pinned.
3. Relevant Supabase production project IDs are pinned.
4. GitHub migration history and Supabase production migration history are reconciled.
5. Remote-only migrations are captured or formally dispositioned without blindly rerunning production DDL.
6. Duplicate or version-divergent migrations are reconciled.
7. Every relevant Vercel project has verified source ownership.
8. Every relevant Vercel project has a verified Root Directory and production branch where applicable.
9. Production domains are verified.
10. The currently serving production deployment and source SHA are pinned.
11. Obsolete or orphaned Vercel mappings are removed, retired, or formally dispositioned.
12. Open infrastructure PRs are dispositioned as CANONICAL, MERGE-INTO-CANONICAL, SUPERSEDED, REFERENCE-ONLY, or CLOSE.
13. Tribunal evidence is reconciled to the surviving GitHub, Supabase, and Vercel states.
14. A known rollback point is recorded.
15. Critical unknowns equal zero.

## Work Package 1: GitHub to Supabase Migration Reconciliation

Create an authoritative migration ledger with at least:

Migration version | Production | GitHub | Same change | Canonical file | Disposition

Allowed dispositions:

MATCH
REMOTE-ONLY
REPO-ONLY
VERSION-DIVERGENT
SUPERSEDED

Production DDL SHALL NOT be rerun merely to make migration history appear aligned. Already-applied production state shall be captured/reconciled into canonical source history through a controlled procedure.

Estimated focused effort: 60 to 120 minutes.

## Work Package 2: Vercel Production Mapping

For every relevant DCSE production/review application, establish:

Vercel project | GitHub repository | Root Directory | Production branch | Production domain | Current deployment | Source SHA | Disposition

Confirm project/source ownership and remove ambiguity created by shared-repository deployment triggers or historical mappings.

Estimated focused effort: 45 to 90 minutes.

## Work Package 3: GitHub Lifecycle Cleanup

Review overlapping infrastructure-generation PRs and branches. Assign one disposition to each:

CANONICAL
MERGE-INTO-CANONICAL
SUPERSEDED
REFERENCE-ONLY
CLOSE

The objective is to prevent future agents or operators from selecting superseded infrastructure implementations merely because those implementations remain open or appear valid.

Estimated focused effort: 30 to 60 minutes.

## Work Package 4: Tribunal Reconciliation and Baseline Seal

Create a final human-readable and machine-readable baseline receipt that pins at minimum:

- controlling governance identity and hash
- canonical GitHub repository and baseline SHA
- relevant Supabase project IDs and migration head/ledger state
- relevant Vercel project IDs
- production domains
- serving deployment IDs and source SHAs
- known rollback point
- open non-critical exceptions, if any
- acceptance disposition

Recommended artifacts:

DCSE_INFRASTRUCTURE_BASELINE_20260814.md
DCSE_INFRASTRUCTURE_BASELINE_20260814.json

Historical Tribunal evidence remains preserved. The sealed baseline receipt becomes the current-state pointer.

Estimated focused effort: 30 to 60 minutes.

## Expected Total Effort

Best case: approximately 3 focused hours.
Expected: approximately 4 to 5 focused hours.
Conservative: approximately 6 focused hours if migration reconciliation reveals additional historical divergence.

This is a reconciliation and closeout effort, not an infrastructure rebuild.

## Website and Product Build Dependency

Core baseline components are supporting infrastructure, but not every build requires every component operationally.

- GitHub is required for DCSE code-owned source control and reproducible builds.
- Vercel is required only for products/sites deployed through Vercel. Wix-only pages are not operationally dependent on Vercel.
- Supabase is required only when a build uses Supabase-backed data, authentication, storage, APIs, functions, RAG, telemetry, or other backend services.
- Tribunal is not required to render a webpage or execute an application, but remains the DCSE governance/evidence layer used to prove source, deployment, disposition, and closeout state and to prevent recurrent drift.

Therefore Core Infrastructure Baseline 1.0 shall be pursued before significant additional product/infrastructure scale, while individual low-risk website/product work may continue only where the required underlying surfaces are already verified and the work does not disturb baseline reconciliation.

## v7.2 Governance Status

Current controlling authority is DCSE Master Profile v7.2 R5 under the DCS operative designation dated 2026-08-08. The designation identifies `DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md` with SHA-256 `2d6afe04be2f65f8d56d6b4b26c81e254e04171e3c94a40023b56b9236de36ae` as the controlling artifact and supersedes R4 for authority purposes.

The operative designation expressly separates governance authority from deployment synchronization. All governed work SHALL apply v7.2 R5 now. No runtime or control surface may claim SYNCHRONIZED unless direct evidence proves exact reconciliation to the designated controller identity.

Accordingly:

- v7.2 R5 authority: OPERATIVE
- v7.2 R5 governance application to DCSE work: REQUIRED
- exact synchronization across every runtime/control surface: EVIDENCE-DEPENDENT and not presumed
- poller completion: NOT REQUIRED for Core Infrastructure Baseline 1.0

## Stop Conditions

Do not reopen poller development during Core Infrastructure Baseline 1.0 unless needed only to preserve evidence or prevent damage.

Do not perform destructive production changes solely for ledger alignment.

Do not declare a surface synchronized or baseline PASS without direct evidence.

Do not allow a poller/runtime defect to invalidate otherwise verified GitHub, Supabase, Vercel, or Tribunal core state.

## Exit Condition

Core Infrastructure Baseline 1.0 is sealed when the production-critical GitHub, Supabase, Vercel, and Tribunal states reconcile, critical unknowns are zero, rollback is known, and the baseline receipt is posted.

After seal, evaluate autonomous orchestration separately under BUILD / BUY / HYBRID / DEFER.

Structure Precedes Scale.
