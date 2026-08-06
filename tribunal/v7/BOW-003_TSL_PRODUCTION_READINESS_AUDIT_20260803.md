# BOW-003 TSL Production Readiness Audit and Inventory

**Task:** `V7_1_BOW_003_TSL_AUDIT_INVENTORY`  
**Evidence timestamp:** 2026-08-03  
**Product lane:** SS / Tedo's Sports Lounge  
**Disposition:** `APPROVE_WITH_FINDINGS` for audit completion; `NOT_READY` for production release  

## Executive determination

BOW-003's audit deliverable is complete. TSL has a substantial working database foundation, live sports-event data, authenticated profiles, picks, contests, trust documents, favorites controls, and registered application assets. It is not production-ready.

The production gate remains closed because the live Supabase security advisor reports a security-definer view and exposed `SECURITY DEFINER` functions, deployment evidence identifies a missing server credential for a retired favorites route, the canonical application source is registered only as a Windows-host tree rather than reconciled GitHub source, and several commercial and operational acceptance surfaces lack evidence.

This report is an evidence inventory and build plan. It does not authorize public release, destructive database work, credential exposure, or a replacement architecture.

## Evidence boundaries

### Verified live

- Supabase project `nevgdyfpxdaloacuutal` is `ACTIVE_HEALTHY`.
- TSL tables, policies, routines, row counts, asset-registry records, and advisor findings were queried directly.
- GitHub PR #29 remains an open draft against `main`.
- GitHub PR #30 and PR #31 were merged into `governance/v7.1-owned-product-harness`.
- BOW-003's prior Claude assignment ended `blocked` with a 20-minute timeout and no output references.

### Registry-supported, not source-reperformed

- Application-file descriptions and hashes in `dcse_asset_registry`.
- Windows paths under `C:\\DS All Things\\dcse-sc-sportsociety\\scss-build\\consumer-shell`.
- Vercel dependency descriptions recorded for application assets.

### Unknown or not independently accessible

- Complete current Windows application source tree.
- Current Vercel environment-variable configuration and latest production deployment logs.
- Browser-based end-to-end results for signup, login, profile, favorites, picks, leaderboard, media administration, checkout, billing, cancellation, and mobile accessibility.
- Current sports-provider contract, quotas, retry behavior, and service-level commitments.

## Canonical inventory

### Database surface

| Asset | Live rows | RLS | Policies | Classification |
|---|---:|---:|---:|---|
| `profiles` | 70 | Yes | 8 | RETAIN, consolidate policies |
| `global_users` | 1 | Yes | 2 | REFACTOR, architectural decision required |
| `Team` | 31 | Yes | 1 | RETAIN |
| `FavoriteTeam` | 0 | Yes | 6 | RETAIN, simplify and test |
| `tsl_events` | 110 | Yes | 1 | RETAIN |
| `tsl_picks` | 336 | Yes | 3 | RETAIN |
| `tsl_contests` | 3 | Yes | 2 | REFACTOR authorization policy |
| `tsl_sports` | 13 | Yes | 1 | RETAIN |
| `tsl_event_competitors` | 0 | Yes | 1 | WRAP pending non-team event validation |
| `tsl_lounge_media` | 0 | Yes | 2 | REFACTOR duplicate read policy |
| `tsl_member_favorites` | 0 | Yes | 4 | REFACTOR against parallel `FavoriteTeam` model |
| `tsl_audit_log` | 4 | Yes | 1 | RETAIN |
| `tsl_platform_settings` | 11 | Yes | 1 | RETAIN, modernize policy syntax |
| `tsl_tester_registry` | 0 | Yes | 2 | RETAIN, restrict broad authenticated read if needed |
| `tsl_trust_documents` | 3 | Yes | 2 | RETAIN, consolidate read policies |
| `tsl_trust_acknowledgments` | 0 | Yes | 3 | RETAIN, remove duplicate policy and index |

### Registered application and migration assets

The registry contains nine TSL application-code rows, one TSL audit row, and five visible TSL database-migration rows in the audited selection. All application-code entries remain `PENDING` promotion. One route, `api/favorites/route.ts`, is `Retired`. Two registry entries refer to the same `profile/page.tsx` file for separate features. Database assets are not hash verified.

Key registered dependencies include AuthContext, signup, profile, admin media, lounge media management, Team and FavoriteTeam access, profile auto-provisioning, audit logging, and `tsl_events.sync_error`.

## Nine-category readiness assessment

| Category | Status | Evidence and required result |
|---|---|---|
| Architecture | NON-PASS | Parallel identity models exist: 70 `profiles` rows versus 1 `global_users` row. Parallel favorites models also exist: `FavoriteTeam` and `tsl_member_favorites`. Adopt one canonical identity and favorites model, migrate references, and retire the duplicate path. |
| Code quality | INSUFFICIENT_EVIDENCE | Registry hashes exist for application assets, but the current source tree is not present in the connected repository. Import, lint, type-check, unit, integration, and build receipts are required from the canonical source commit. |
| Database policies | NON-PASS | RLS is enabled on the audited tables, but policies use `auth.role()` and `{public}` broadly. Duplicate permissive policies exist. Advisor findings require correction and role-matrix testing. |
| Authentication | PARTIAL | `auth.users` and `profiles` reconcile at 70 each. Signup auto-provisioning is recorded. No end-to-end evidence covers signup confirmation, login, refresh, password reset, email change, logout, session revocation, or admin authorization. |
| Security | STOP-GATE | `tsl_community_picks` is reported as a security-definer view. Anonymous or authenticated execution remains available on several `SECURITY DEFINER` functions. Production release is prohibited pending least-privilege remediation and retest. |
| Deployment configuration | NON-PASS | The app source is not reconciled to the governance repository. A retired favorites route records a missing Vercel service credential. Current production configuration, health route, rollback deployment, and environment-variable inventory are not evidenced. |
| Sports data integrity | PARTIAL PASS | 110 events have unique external identifiers, start times, and no recorded sync errors. 109 are final and 1 scheduled. Only MLB, NBA, NHL, and UFL currently have stored events. Nine active sports have zero stored events. Provider freshness and expected-season coverage remain unproven. |
| UX and accessibility | INSUFFICIENT_EVIDENCE | Registry describes theme, profile, favorites, and admin-media corrections. No current browser matrix, responsive test, WCAG keyboard/focus test, empty-state test, or failure-state evidence was available. |
| Commercial readiness | NON-PASS | No verified checkout, subscription lifecycle, entitlement enforcement, refund/cancellation handling, terms/privacy acceptance flow, support process, analytics, conversion funnel, or production monitoring package was produced. |

## Live sports-data findings

- 110 events total.
- 109 final and 1 scheduled.
- 110 distinct external source/ID combinations.
- Zero missing external IDs.
- Zero missing start times.
- Zero missing competitors for team-format events.
- Zero non-null `sync_error` values.
- 336 picks across 20 users and 126 game identifiers.
- Four picks have no recorded result.
- Stored event coverage: MLB 80, NBA 22, NHL 5, UFL 3.
- Active but zero-event sports: NFL, NCAAF, WNBA, PGA, LPGA, UFC, BOXING, and SPECIAL. NCAAB is inactive and has zero events.

The zero-error column is useful but does not prove a healthy current feed. Most stored events are historical, and the latest stored event is August 1, 2026. Provider polling freshness must be measured against the current sports-availability matrix.

## Security findings

### Critical production blockers

1. Convert `public.tsl_community_picks` to a security-invoker view or restrict it from exposed roles.
2. Review and revoke unintended `anon` execution for `handle_new_auth_user`, `log_favorite_team_change`, `tsl_homepage_feed`, `tsl_leaderboard`, and `tsl_platform_stats`.
3. Review authenticated execution and internal authorization for `admin_get_user_picks`, `admin_upsert_lounge_media`, and `grant_tsl_reward`.
4. Replace deprecated `auth.role()` policy predicates with explicit `TO` roles and ownership or authorization conditions.
5. Validate that administrative authority is stored in protected app metadata or a governed membership table, not user-editable metadata.

Reference: https://supabase.com/docs/guides/database/database-linter

### High-priority correctness risks

- `FavoriteTeam_dcs_admin` checks `auth.jwt() ->> 'role'`, which requires verification against actual protected claim placement.
- `tsl_contests` management is tied to a hard-coded email address.
- `tsl_lounge_media`, `tsl_trust_documents`, and `tsl_trust_acknowledgments` have overlapping read policies.
- `tsl_trust_acknowledgments` has duplicate indexes.
- The public schema contains privileged functions whose `EXECUTE` grants require explicit review.

## Architecture decision record

### Decision

Retain the existing Supabase-backed TSL architecture. Do not replace it. Reconcile the duplicate identity and favorites models, move the canonical application source into governed GitHub history, and harden exposed database APIs before production release.

### Rationale

The live system already contains working profiles, events, picks, contests, sports configuration, trust records, audit records, and RLS. Replacing that foundation would increase migration risk without addressing the immediate security, evidence, and deployment gaps.

### Consequences

- Existing data and migrations remain authoritative.
- Security remediation is additive and migration-controlled.
- Local Windows-only source ceases to be the sole application authority.
- Product release remains gated until automated role-matrix and end-to-end tests pass.

## Dependency map

1. Auth users provision `profiles`.
2. Profiles and protected role data control member and administrative capabilities.
3. `tsl_sports` configures provider coverage.
4. Provider ingestion populates `tsl_events` and optional competitors.
5. Contests reference events.
6. Authenticated users create `tsl_picks` and favorites.
7. Settlement determines pick results and leaderboard projections.
8. Audit and trust tables support accountability and terms acknowledgment.
9. The consumer shell and admin routes depend on Supabase keys, RLS, RPC grants, and Vercel configuration.

## RETAIN, WRAP, REFACTOR, REPLACE

### RETAIN

- Supabase project and migration history
- `auth.users` plus `profiles` as the current populated identity path
- Events, sports, contests, picks, audit log, trust documents, and acknowledgments
- Existing RLS-first access model
- External provider identifiers and sync visibility

### WRAP

- Sports-provider ingestion with freshness, quota, retry, and idempotency telemetry
- Administrative operations with server-side authorization and audit receipts
- Deployment configuration with explicit environment validation and a health endpoint

### REFACTOR

- Security-definer view and function grants
- Deprecated and broad RLS policies
- `global_users` versus `profiles`
- `FavoriteTeam` versus `tsl_member_favorites`
- Duplicate registry entries, policies, and indexes
- Hard-coded email-based administrative authorization
- Canonical source and CI ownership

### REPLACE

- No major platform replacement is authorized.
- Replace only the obsolete or duplicate identity/favorites pathways after migration and rollback testing.

## Risk register

| Risk | Severity | Control |
|---|---|---|
| Exposed privileged database paths | Critical | Restrict grants, enforce internal authorization, rerun security advisor and adversarial role tests |
| Security-definer community view | Critical | Convert to security invoker or revoke exposed access |
| Windows-only canonical application source | High | Import exact source with hashes into governed Git branch and CI |
| Parallel identity models | High | Adopt profiles or documented successor; migrate all FKs atomically |
| Parallel favorites models | High | Select one schema/API and migrate callers |
| Feed freshness not evidenced | High | Scheduled ingestion monitor, last-success metric, provider reconciliation |
| Commercial lifecycle absent | High | Complete billing, entitlements, terms, refunds, support, and analytics tests |
| No browser acceptance matrix | Medium | Automated desktop/mobile and accessibility suite |
| Duplicate RLS policies and indexes | Medium | Consolidate through reviewed migrations |

## Tailored production build plan

### Gate 1: Canonical source and CI

- Import the exact Windows consumer-shell source into a governed repository branch.
- Preserve file hashes and identify the deploy commit.
- Run dependency install, lint, type-check, unit tests, production build, and secret scan.

### Gate 2: Database security

- Add migration-controlled fixes for the security-definer view, function grants, policy roles, and duplicate policies.
- Run Supabase security and performance advisors.
- Execute anon, authenticated owner, authenticated non-owner, administrator, and service-role tests.

### Gate 3: Identity and domain reconciliation

- Decide `profiles` versus `global_users`.
- Decide `FavoriteTeam` versus `tsl_member_favorites`.
- Reconcile foreign keys, code calls, policies, audit triggers, and rollback.

### Gate 4: Sports operations

- Prove provider ingestion for each active sport.
- Record last-success, rows received, duplicates rejected, errors, quota, and source timestamp.
- Reconcile the current sports-availability matrix against stored events.

### Gate 5: Product acceptance

- Test authentication, profiles, themes, favorites, contests, picks, settlement, leaderboard, trust acknowledgment, and admin media.
- Test empty, loading, stale, provider-error, unauthorized, and offline states.
- Complete keyboard, focus, contrast, mobile, and screen-reader checks.

### Gate 6: Commercial and deployment readiness

- Verify plan tiers, billing, entitlement enforcement, cancellation, refund handling, legal acceptance, support, analytics, and monitoring.
- Validate production environment variables without exposing values.
- Deploy a preview, run smoke tests, document rollback, then request production release approval.

## Acceptance result

BOW-003 audit output: **COMPLETE WITH FINDINGS**.  
TSL production readiness: **NON-PASS**.  
Recommended task disposition: **APPROVE_WITH_FINDINGS** for the audit artifact, with production release held behind the critical security and canonical-source gates.

## Rollback and lessons learned

- This audit made no schema or production-code changes.
- Rollback for the evidence publication is removal or reversion of the audit commit only.
- Task state must never become `completed` when the assignment result is `blocked`, `failed`, or `timeout`.
- Poller heartbeats must continue while child work runs.
- Output references must be nonempty and retrievable before completion.
- Canonical application source cannot remain solely on a Windows host while governance evidence is maintained in GitHub.
- Advisor output and role-matrix testing belong in the acceptance gate, not post-release remediation.
