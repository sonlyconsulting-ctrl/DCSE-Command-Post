# ESCD Mainline Convergence Record v7.2

**Task ID:** DCSE-ESCD-GITHUB-CLOSE-001  
**Lane:** DCSE / ESCD  
**Status:** MAINLINE CONVERGENCE CANDIDATE  
**Authority:** DCS Level 0  
**Date:** 2026-09-10

## Purpose

Create a clean ESCD integration path directly from current `main` without importing the unrelated historical ancestry of `feature/aegis-executive-kernel`, `feature/escd-runtime-repair-001`, or `feature/escd-minimal-mvp-006`.

## Source Reuse

The current ESCD MVP implementation bytes were reused from `feature/escd-minimal-mvp-006` under D20 Reuse Before Redesign. The clean branch carries the current MVP application subtree and only the required top-level API, persistence candidate, Vercel routing, and review workflow.

Included:
- `apps/escd/**`
- `api/mvp.py`
- `supabase/candidates/20260910_escd_mvp_items.sql`
- `vercel.json`
- `.github/workflows/escd-mvp-review.yml`

Excluded intentionally:
- unrelated Aegis history
- unrelated historical Tribunal files
- obsolete branch-only work orders not required by the MVP runtime
- broader Executive/PA/workflow migration chain not required by this MVP convergence
- Preview-resume marker used only to probe Vercel rate limits

## Persistence Boundary

`20260910_escd_mvp_items.sql` is explicitly marked `CANDIDATE ONLY` and is therefore stored under `supabase/candidates/`, not `supabase/migrations/`. This prevents a GitHub merge from being represented or used as authorization to apply candidate DDL to production through an automated Supabase integration. Production database changes remain a separately authorized action.

## Provider Gate

The ESCD provider/Vault implementation remains subject to hosted Preview validation. Current GitHub deployment statuses report Vercel deployment rate limiting, so no provider-gate PASS is claimed.

## Security

No API keys or secret values are included in this convergence record. Provider secrets remain server-side and are not exposed in the browser surface.

## Validation Gate

Promotion to `main` requires both:
- `ESCD Mainline Review Gate`: PASS
- `V7.2 governance validation`: PASS

Vercel deployment and provider-key hosted validation remain separately observable runtime gates and do not become GitHub source-convergence failures.

## Promotion Boundary

This branch is intended to replace the stacked ESCD PR path after its GitHub review gates pass. Production deployment, provider credential entry, and production database migration are not authorized by this record.
