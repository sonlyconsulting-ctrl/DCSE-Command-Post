# TSL Phase 2c — Real-Time Sports Engine Architecture

**Governance:** DCSE v7. Branch `tsl/phase2c-realtime-sports-v7`, based on `origin/v69` @ `3ebc85f`.
**Date:** 2026-08-01
**Input:** `TSL_SPORTS_AVAILABILITY_MATRIX_20260801.md` (live-verified provider findings, WNBA added)
**Scope:** Architecture for TEAM/FIELD/CARD, then the MLB TEAM vertical slice, implemented on this branch.

## 0. Correction to my own earlier assumption

I previously assumed `tsl_events` was TEAM-only and that FIELD/CARD would need new tables. **That
assumption was wrong** — I checked before designing anything, per your instruction, and found the
schema already supports all three models. This section documents what's actually there before
proposing anything new.

## 1. What already exists (verified by reading the live schema, not memory)

**`tsl_events`** is already a proper supertype table, not TEAM-only:
- `event_format` — `CHECK (event_format IN ('HEAD_TO_HEAD','FIELD','CARD'))`
- `event_shape_valid` constraint — HEAD_TO_HEAD requires `home_abbr`/`away_abbr`; FIELD/CARD require `event_name` instead. The schema itself already refuses to let FIELD/CARD data get forced into home/away columns.
- `parent_event_id` (self-FK, `ON DELETE CASCADE`) — a card night is a parent event; each bout is a child event. Same table, same shape, just nested.
- `status` — 9-state enum (`scheduled, pre_event, live, halftime_or_break, final, review, archived, cancelled, postponed`), `external_source` (`ESPN/MANUAL/SEED`), `last_sync_at`, `metadata jsonb`, `is_pickable`, `contest_id` (nullable FK to `tsl_contests`).

**`tsl_event_competitors`** — the FIELD/CARD participant table: `event_id` FK, `competitor_key` (what a pick matches against), `display_name`, `seed_or_odds`, `finish_position` (golf leaderboard position), `is_winner`.

**`tsl_picks`** is already format-agnostic: `game_id` (FK to `tsl_events.game_id`), `picked_team` (plain text — a team abbr for HEAD_TO_HEAD, or a `competitor_key` for FIELD/CARD). No schema change needed for picks to work across all three models.

**`settle_event_picks(game_id, dry_run)`** already branches on `event_format`: HEAD_TO_HEAD reads `winner_abbr` off the event; anything else reads `is_winner` off `tsl_event_competitors`. **Settlement for all three models is already built and correct.**

**`enforce_pick_lock()`** already enforces `is_pickable`, `status IN ('scheduled','pre_event')`, and `now() < lock_time` — format-agnostic, no changes needed.

**`tsl_homepage_feed()`** already selects `event_format, event_name` generically alongside the HEAD_TO_HEAD columns and returns whatever's in `tsl_events` — it will surface FIELD/CARD events automatically once they exist, no RPC change needed.

**Conclusion:** the backend data model for TEAM/FIELD/CARD is essentially done. **The actual gap is that nothing has ever written a FIELD or CARD row, and nothing has ever kept `tsl_events` current for any sport.** Phase 2c is an ingestion problem, not a schema problem.

## 2. A live bug this surfaces, not just a gap

`tsl_platform_settings.strict_pick_lock = {enabled: false, description: "When true, picks against game_ids absent from tsl_events are rejected. Enable after feed ingestion backfills the event registry."}` — **this was already anticipated and deliberately left off**, waiting for exactly this work.

But `/picks` (`src/app/picks/page.tsx`) fetches games **client-side, directly from ESPN** (`lib/mlb-feed.ts`, `nba-feed.ts`, `ufl-feed.ts`, `nhl-feed.ts`) and writes picks straight to `tsl_picks` using ESPN's raw `event.id` as `game_id` — bypassing `tsl_events` entirely for display. With `strict_pick_lock` off, `enforce_pick_lock` lets these through even when nothing in `tsl_events` matches.

**Result, confirmed live:** `select count(*) from tsl_picks p where not exists (select 1 from tsl_events e where e.game_id = p.game_id)` → **123 real member picks**, spanning April, May, and as recently as **2026-07-31 (yesterday)** — meaning this is actively happening, not just historical. None of these can ever be graded by `settle_event_picks()` as it stands; the affected members never got their Smoove Coins.

This means Phase 2c isn't just "build a feed" — it needs a **backfill pass** to recover those 123 picks where the underlying ESPN games can still be looked up (MLB/NBA/NHL/UFL final scores are retained indefinitely by ESPN), before `strict_pick_lock` gets flipped on.

## 3. Three event models — adapter design

One adapter family per shape, keyed off `tsl_sports.category`/`default_format` (already correctly set per sport in the matrix):

**`TeamAdapter`** (MLB, NFL, NCAAF, NBA, NCAAB, NHL, UFL, WNBA) — ESPN `scoreboard.events[]` → one `tsl_events` row per event, `event_format='HEAD_TO_HEAD'`, `game_id = event.id` (matches what `/picks` already writes — critical for the 123-pick backfill and for future picks to land on rows that exist). Maps `competitions[0].competitors` (home/away by `homeAway`) to `home_abbr`/`away_abbr`/`home_score`/`away_score`; maps ESPN `status.type.state`/`name` to the internal 9-state enum (mapping table below); sets `winner_abbr` when `status='final'` from whichever competitor has the higher score (or ESPN's explicit winner flag if present).

**`FieldAdapter`** (PGA, LPGA) — one `tsl_events` row per tournament (`event_format='FIELD'`, `event_name` = tournament name, `parent_event_id` null), plus one `tsl_event_competitors` row per player with `competitor_key` = ESPN athlete id, `finish_position` from the leaderboard, `is_winner` set once final. Pick semantics for FIELD need a product decision before UI work: outright winner vs. top-5/top-10 — the schema supports any of these via `competitor_key` + a pick-type distinction, but that distinction doesn't exist yet in `tsl_picks` (currently just team-vs-team). Flagging as a design gap, not silently picking one.

**`CardAdapter`** (UFC, eventually Boxing) — the fight night itself is a parent `tsl_events` row (`event_format='CARD'`), each bout is a **child** `tsl_events` row (`parent_event_id` = the card's `event_id`, its own `event_format='CARD'`, `event_name` = "Fighter A vs Fighter B"), with `tsl_event_competitors` holding the two fighters and the bout's own `lock_time`/`status`/`winner`. This lets members pick per-bout (what actually makes sense) while the card groups them for display. Boxing uses the identical shape via `feed_source='MANUAL'` — an admin creates the parent card event and its bout children by hand instead of an adapter populating them.

## 4. Status mapping (ESPN → internal)

| ESPN `status.type.state` / `name` | Internal `tsl_events.status` |
|---|---|
| `pre` / `STATUS_SCHEDULED` | `scheduled` |
| `pre` within ~30 min of start (configurable) | `pre_event` |
| `in` / `STATUS_IN_PROGRESS` | `live` |
| `in` + halftime/intermission detail | `halftime_or_break` |
| `post` / `STATUS_FINAL` | `final` |
| `STATUS_POSTPONED` | `postponed` |
| `STATUS_CANCELED` | `cancelled` |

Anything ESPN returns that doesn't map cleanly falls back to `review` (never silently dropped) and logs `sync_error` so it surfaces in the admin/freshness UI instead of vanishing.

## 5. Refresh rules

No cron exists today — `vercel.json` has zero `crons`, and `archive-events` is the only cron *route* in the codebase (rolls old rows off, fetches nothing). Proposed tiers, one consolidated endpoint (`/api/cron/sync-sports?sport=X`) rather than N separate crons:

| Tier | Condition | Frequency |
|---|---|---|
| Live | Any `tsl_events` row for the sport currently `status='live'` | every 1–2 min |
| Today | Sport has a `scheduled`/`pre_event` row starting within 24h | every 15 min |
| Horizon | No games today, but sport is in-season | every 6h (catch newly scheduled games) |
| Dormant | Sport confirmed off-season/preseason (per the matrix) | once daily, cheap check only |

MLB starts in the **Live/Today** tier immediately given 11 verified games in the 48h window.

## 6. Settlement, coins, leaderboard

No changes needed — `settle_event_picks`/`settle_all_pending_events`/`grant_tsl_reward` already work across all three `event_format`s per §1. The MLB slice's job is only to keep `tsl_events` accurate enough for these to have something correct to grade.

## 7. UI projections

- **Main homepage board** — already consumes `tsl_homepage_feed()`'s `live`/`upcoming`/`recent_final` arrays; once `tsl_events` has real MLB rows, "Today's Board" populates with zero frontend change.
- **`/picks` page** — needs to stop fetching ESPN directly and instead read from `tsl_events` (via `tsl_homepage_feed()` or a dedicated picks RPC), so what a member sees and picks against is the same registry that locks and settles it. This is the fix for the orphaned-pick bug, not just a nice-to-have.
- **Lounge mini-updates** — same feed, smaller/denser card treatment, per your ask; reuses the same RPC output.
- **Freshness/delay/provider-error states** — add `last_sync_at` (already a column) and a new `sync_error text` column to `tsl_events`; UI shows "Live · updated Xs ago" (pattern already exists on the homepage) and escalates to a visible "delayed" badge past a threshold (2 min for `live` status) or a "provider issue, showing last known state" badge when `sync_error IS NOT NULL` — never silently stale.

## 8. Migration plan (MLB slice only — FIELD/CARD tables already exist, untouched)

1. `ALTER TABLE tsl_events ADD COLUMN sync_error text` — additive, nullable, zero risk to existing rows.
2. No other schema changes. `game_id` unique constraint, `event_format` check, and all settlement RPCs are reused as-is.
3. Add `crons` array to `vercel.json` for `/api/cron/sync-sports`.
4. One-time backfill pass for the 123 orphaned picks (MLB-relevant ones first): re-fetch each orphaned `game_id` from ESPN, insert the resulting `tsl_events` row as `status='final'` with the correct `winner_abbr`, then run `settle_event_picks(game_id, dry_run=true)` to verify before committing for real.
5. Only after the backfill is verified and the sync cron has run cleanly for a full day: flip `strict_pick_lock.enabled` to `true`. Not done as part of this pass — a deliberate, later step, not bundled into initial deploy.

## 9. Rollback plan

Every step above is additive or reversible independently:
- `sync_error` column: `ALTER TABLE tsl_events DROP COLUMN sync_error` — no data loss, nothing else references it yet.
- Cron: remove the `crons` entry from `vercel.json` and redeploy — stops all syncing immediately, existing data untouched.
- Backfilled events: tagged `external_source='ESPN'` with a `metadata.backfill=true` marker, so they're identifiable and removable as a batch if something's wrong, without touching organically-synced rows.
- `strict_pick_lock`: a single settings-row flip, reversible in one UPDATE — not touched until backfill is verified, so there's no "in-flight" risk to roll back.

## 10. Test matrix

| Test | Expected result |
|---|---|
| Re-run sync for the same game twice | No duplicate `tsl_events` row (upsert on `game_id`) |
| Sync a game that's now `postponed` | Status updates, `lock_time` untouched unless ESPN provides a new time, no false settlement |
| Sync a game that just went `final` | `winner_abbr` set correctly from both possible ESPN score orderings (home > away and away > home) |
| Pick submitted before `lock_time` | Succeeds, matches `enforce_pick_lock` |
| Pick submitted after `lock_time` | Rejected with `PICK_REJECTED_PAST_LOCK`, unchanged from current behavior |
| `settle_event_picks` on a synced-then-final MLB game | WIN/LOSS/PUSH graded correctly, coins granted once, idempotent on re-run |
| Backfill of an orphaned pick | `tsl_events` row created, pick settles correctly, coins granted retroactively |
| ESPN endpoint returns malformed/unexpected JSON | Adapter logs `sync_error`, does not crash the cron run, does not corrupt existing rows |
| Cross-DST display | Times shown correctly for ET/CT/MT/PT `timezone_pref` around a DST boundary |
| `strict_pick_lock=false` (current default) vs. `true` (post-backfill) | Confirms the flag's documented behavior before flipping it |

## 11. Provider-risk controls

- Defensive parsing: never assume a field exists; a missing/renamed field logs `sync_error` and skips that event, not the whole sync run.
- The NCAAB 404-then-success finding from the matrix is the concrete proof this is needed, not hypothetical.
- Rate/backoff: single consolidated cron endpoint (not N parallel ones) to stay well under any informal ESPN rate limits.
- No auth dependency: ESPN's site API needs no key, so there's no credential-expiry failure mode — but also no SLA, so alerting on `sync_error` accumulation matters more than it would for an official API.

## 12. Immediate build priority (this pass)

MLB TEAM vertical slice, on `tsl/phase2c-realtime-sports-v7`:
1. `sync_error` column migration
2. `TeamAdapter` for MLB specifically (generalizes trivially to the other 7 TEAM sports later — same ESPN response shape)
3. `/api/cron/sync-sports` route, MLB wired in
4. `vercel.json` cron entry
5. Freshness/delay/error UI on the homepage board
6. `/picks` page fixed to read from `tsl_events` instead of fetching ESPN directly (closes the orphan-pick bug for future picks)
7. Backfill script for MLB-relevant orphaned picks (dry-run first)
8. Live verification, then GitHub/Supabase status update

PGA/LPGA (FIELD) and UFC (CARD) adapters are designed above but **not implemented this pass** — explicitly sequenced after MLB per your priority order. Boxing/Special manual-entry UI likewise designed (reuses the CARD shape) but not built this pass.
