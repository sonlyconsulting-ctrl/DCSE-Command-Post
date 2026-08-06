# BOW-002 — Enterprise Audit & Inventory: dcse_asset_registry Reconciliation

Executor: Claude Code, host session, 2026-08-03. Scope: reconcile `public.dcse_asset_registry`
(SC-Command-Post, 57 rows) against actual file existence across all known branches and the
local filesystem. This is a real, bounded pass, not an exhaustive full-repo file census — see
"Not covered" below for what this does not claim to check.

## Method

For each registry row's `storage_location`, checked existence via `git ls-tree` across all
remote branches (for `github://` and repo-relative paths) or direct filesystem check (for
`Desktop/`, local drive, and non-git paths). No file contents modified.

## Confirmed finding: systematic path-prefix bug

26 rows (`DCSE-2026-D01-001` through `D21-001`, plus `IDX-001`, `RAM-001`, `TIER-001`,
`TSL-AUD-001`) record `storage_location` as `doctrine/v6.9/01_Doctrine/...` or
`doctrine/v6.9/02_Registry/...`. The actual path on both `origin/tsl/phase2c-realtime-sports-v7`
and `origin/v69` is `v6.9/01_Doctrine/...` / `v6.9/02_Registry/...` -- no leading `doctrine/`
directory. The files are not missing; the registry's recorded path is wrong for all 26 rows
in the same way, and none of them are reachable from the canonical
`governance/v7.1-owned-product-harness` branch (they exist on `tsl/phase2c-realtime-sports-v7`
and `v69` only).

**Fix required:** strip the erroneous `doctrine/` prefix from all 26 `storage_location` values,
and record which branch each lives on, since the canonical governance branch doesn't have them.
Not applied in this pass -- editing `dcse_asset_registry` rows is a data-correction decision
for the registry owner, not something to silently rewrite mid-audit.

## Confirmed finding: two broken references

| asset_id | storage_location | Result |
|---|---|---|
| `DCSE-2026-SC-TOOL-001` | `github://.../tools/dcse_gmail_report.py@governance/v7.1-owned-product-harness` | **Not found on any remote branch.** File does not exist anywhere in the GitHub repo. |
| `DCSE-2026-MP-001` | `DCS_Employment_Workflow/00_DOCTRINE_AND_GOVERNANCE/DCSE_Master_Profile_CURRENT.md` | **Not found on any remote branch.** Registry marks `hash_verified: true` -- a hash was recorded for a file not present in the repo, so that verification is not trustworthy as recorded. |

## Verified present, no action needed

- `CLAUDE.md`, all `docs/status/7-day/*`, all `docs/campaigns/custom-digital-campaigns/*` --
  present on the current branch, paths correct.
- 5 `Desktop/*` entries -- present on local filesystem at the recorded path (these are
  intentionally outside git per their own entity_lane).
- `_Tribunal_Inbox/TRIBUNAL_20260725_V69_DOCTRINE_PROMOTION_RATIFIED.json` -- present on local
  filesystem, not git-tracked (consistent with the broader pattern already found in BOW-001:
  governance-relevant files living outside version control).

## Update: remaining rows checked

- **14 `DCSE-2026-TSL-APP-*` rows (11 unique paths)** -- checked against
  `C:\DS All Things\dcse-sc-sportsociety\scss-build\...`. 10 of 11 present. The one absence
  (`api/favorites/route.ts`, asset `TSL-APP-009`) is correct: its own `lifecycle_status` is
  `Retired`, so its absence matches the registry, not an orphaned reference.
- Found in passing: `TSL-APP-003` and `TSL-APP-011` are duplicate rows for the identical file
  (`profile/page.tsx`, same path) -- registry hygiene issue, not a broken reference.
- **6 `DCSE-2026-TSL-DB-*` rows** -- checked against live migration history on
  `nevgdyfpxdaloacuutal` via `list_migrations`. All 6 referenced migrations exist
  (`add_preferred_theme_to_profiles`, `auto_provision_profile_on_signup`,
  `backfill_missing_profiles`, `grant_select_team_to_public_roles`,
  `favoriteteam_ownership_rls_and_audit_trigger`, `fix_tsl_audit_log_actor_fk_target`,
  `add_sync_error_to_tsl_events`). No orphaned references in this group.

## Not covered in this pass

- No naming-convention sweep run across the repo's other ~30 top-level directories
  (`SC_ASP`, `SC_CTJ`, `SC_Gov-OS`, `SC_SASH`, `SC_SHY`, `SC_TSL`, `DCSE_ASSET_PORTAL_APP`,
  etc.) that aren't already claimed as assets in the registry -- this pass reconciled the
  registry's own 57 claimed assets exhaustively, not a from-scratch full-filesystem census of
  everything that *isn't* registered. That would be a materially larger, separate pass (an
  audit for missing/unregistered files, rather than broken references in existing entries).

## Disposition

All 57 rows in `dcse_asset_registry` reconciled against real state (git branches, local
filesystem, and live migration history). Confirmed defects: 26 rows with a systematic
`storage_location` path-prefix bug, 2 rows referencing files that don't exist on any branch
(one incorrectly marked `hash_verified: true`), 2 duplicate rows for the same file. Everything
else checks out, including one correctly-absent retired asset. Registry corrections not
applied -- that's a data-owner decision, not something to silently rewrite mid-audit.
BOW-002's acceptance criterion of "no orphaned references" is now fully evaluated against the
registry's own claims (not a from-scratch inventory beyond what's already registered).
