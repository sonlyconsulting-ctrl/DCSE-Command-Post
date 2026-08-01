# TSL Phase 2b — Verified Requirements Matrix

**Date:** 2026-08-01
**Verified by:** Claude Sonnet 5
**Repo (TSL app):** `C:\DS All Things\dcse-sc-sportsociety\scss-build\consumer-shell` — local-only, no GitHub remote. Deploys via `vercel deploy` CLI.
**Baseline commits:** `c02a79c`, `f3eeb8d` — deployed as `dpl_A9Q91a3PiCwN7oSN6WTmuPXhQRRy`
**Supabase project:** `nevgdyfpxdaloacuutal` (SC-Command-Post)
**Tribunal record:** `TRIBUNAL_20260801_TSL_PHASE2B_VERIFICATION.json`
**Supabase status record:** `dcse_promotion_state_log`, batch `TSL-PHASE2B-VERIFICATION-20260801`

## Baseline carried forward (must be preserved through all Phase 2b work)

- 71/71 `auth.users` rows now have a `profiles` row (auto-provisioning trigger + backfill)
- Premium pricing corrected to $9.99/mo in `profile` and `membership` pages
- 4 assets registered in `dcse_asset_registry`: `DCSE-2026-TSL-APP-002/003/004`, `DCSE-2026-TSL-DB-001`
- QA test account created, tested, and cleanly deleted

## Build results

`npm run build` — clean, 32 static routes generated, TypeScript check passed, no errors (verified twice: after the profile-provisioning fix and after the pricing fix).

## H008 disposition

**COMPLETED** — shipped in PHASE 2 batch 1, commit `1bad366` (2026-07-31), not Phase 2b scope. Live-verified this session: header toggle cycles light → dark → auto and persists to `localStorage`. Absent from the Phase 2b inventory only because it was never assigned to Phase 2b — batch 1 was H004/H008/H001/H002/H003, Phase 2b is H005/H006/H007/H009/H010.

## Matrix

### H007 — Admin media upload UI
| | |
|---|---|
| State | Backend-ready, no frontend. `admin_upsert_lounge_media` RPC exists, validated (title required, https-only URLs, admin-allowlist-gated). Targets `tsl_lounge_media` (RLS on, 2 policies). Homepage "TSL Media Lounge" already renders from this table live. |
| DB deps | `tsl_lounge_media`, `admin_upsert_lounge_media` — both exist and are sound |
| Frontend deps | New admin route/form + list/edit view |
| External deps | None (video_url is a link, not a file upload) |
| Security | RPC already enforces admin allowlist + https-only server-side; UI must call the RPC, not the table |
| Acceptance criteria | Admin can create/edit/deactivate an entry; it appears live on homepage; non-admin RPC calls rejected |
| Test requirements | RPC succeeds as admin, rejected as non-admin/anon; homepage reflects new entry; build; live verification |
| **Stop-gate** | **None** |

### H009 — Favorite sports/teams selector
| | |
|---|---|
| State | Frontend (`FavoriteTeamsSelector.tsx`) and `/api/favorites` route are fully built (5-team limit, JWT auth, Zod, audit logging) but query **wrong table/column names** — code expects `teams`/`member_favorite_teams`/`audit_logs`; real tables are `"Team"` and `"FavoriteTeam"` (camelCase columns) and `tsl_audit_log`. 100% broken as shipped. Hosted on `/lounge`, not in real member nav, and that page has unrelated hardcoded mock data (fake wallet balance, fake live scores). |
| DB deps | `"Team"` (RLS, 1 policy), `"FavoriteTeam"` (RLS, 3 policies), `tsl_audit_log` (RLS) — all exist |
| Frontend deps | Fix table/column names; decide real navigation placement |
| External deps | None |
| Security | RLS already on; `/api/favorites` mediation pattern is sound, just misaddressed |
| Acceptance criteria | Member selects up to 5 real teams, persists correctly, page reachable from real nav, no mock data remains |
| Test requirements | Add/remove reflects in DB with correct types; 6th add rejected; unauthenticated rejected; build; live verification |
| **Stop-gate** | **None** |

### H010 — Account settings completion
| | |
|---|---|
| State | Core fields (display name, avatar, timezone, theme) fixed and live today. Email change + notification prefs still missing. |
| DB deps | None new for email change; notification prefs blocked on H006 |
| Frontend deps | Email-change form + confirmation flow; notification-prefs UI (blocked) |
| External deps | Email-change delivery needs the unresolved Supabase Site URL fix (flagged since 2026-07-30, never re-verified) |
| Security | Email change must require confirmation via new address, no silent takeover |
| Acceptance criteria | Member can request email change, confirms, updates only after confirmation |
| Test requirements | Round-trip through real inbox blocked pending Site URL fix; build + live verification of what's shippable now |
| **Stop-gate** | **Partial** — email confirmation delivery blocked on Site URL issue |

### H006 — Persistent notification inbox
| | |
|---|---|
| State | `NotificationQueue` table exists but minimal — no read state, no type/category, no action link, `userId` is text (not uuid, mismatched vs `auth.users.id`). Zero frontend code references it. |
| DB deps | Schema changes needed: read state, type, action link, userId type fix |
| Frontend deps | Full inbox UI — none exists |
| External deps | Unclear — `sent_at` column implies a dispatch mechanism may have been planned |
| Security | RLS enabled (3 policies) — scope needs confirming before building on top |
| Acceptance criteria | Not yet definable |
| Test requirements | Cannot be scoped until design decision made |
| **Stop-gate** | **Yes** — needs a design decision (event sources, read-state model, retention, delivery channel) before implementation |

### H005 — Wix membership upgrade flow
| | |
|---|---|
| State | Zero integration code anywhere in the app. "Upgrade Now" is fully inert; page states payments are simulated. `unified_identity_links` is fully built and ready but completely unused. |
| DB deps | `unified_identity_links` — exists, ready, unused |
| Frontend deps | Real entitlement check (read `participation_lane`); real Wix checkout handoff |
| External deps | Wix site API credentials/webhook secret; confirmation of entitlement source-of-truth direction — **not available in this session** |
| Security | Client must never set its own `participation_lane`; entitlement server/webhook-verified only; cancellations honored |
| Acceptance criteria | No simulated payments in production; TSL must not duplicate membership authority; real Wix checkout handoff; downgrade/cancellation flows correctly |
| Test requirements | Cannot verify end-to-end without live Wix webhook configuration |
| **Stop-gate** | **Yes** — external Wix configuration required |

## Confirmed execution order

H007 → H009 → H010 (partial) → H006 (blocked) → H005 (blocked)

## Phase boundary

Phase 2b ends after H005 passes build/database/security/live verification, or is formally stopped at its documented stop-gate. This does **not** authorize a final TSL completion declaration. Phase 2c (real-time sports engine) begins only after Phase 2b closes, followed by rewards/leaderboard certification, security certification, brand conversion, and production lock.
