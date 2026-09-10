# ESCD Mainline Convergence Record v7.2

**Task ID:** DCSE-ESCD-GITHUB-CLOSE-001  
**Lane:** DCSE / ESCD  
**Status:** MAINLINE CONVERGENCE CANDIDATE  
**Authority:** DCS Level 0  
**Date:** 2026-09-10

## Purpose

Create a clean ESCD integration path directly from current `main` without importing the unrelated historical ancestry of `feature/aegis-executive-kernel`, `feature/escd-runtime-repair-001`, or `feature/escd-minimal-mvp-006`.

## Source Reuse

The current ESCD implementation bytes were reused from `feature/escd-minimal-mvp-006` under D20 Reuse Before Redesign. The clean branch copies the current ESCD application subtree and only the required top-level API, migration, Vercel routing, and review workflow.

Included:
- `apps/escd/**`
- `api/escd.py`
- `api/mvp.py`
- `supabase/migrations/20260910_escd_mvp_items.sql`
- `vercel.json`
- `.github/workflows/escd-mvp-review.yml`

Excluded intentionally:
- unrelated Aegis history
- unrelated historical Tribunal files
- obsolete branch-only work orders not required at runtime
- Preview-resume marker used only to probe the Vercel rate limit

## Provider Gate

The ESCD provider/Vault implementation remains subject to hosted Preview validation. Vercel returned `Deployment rate limited - retry in 24 hours` on 2026-09-10, so no provider-gate PASS is claimed.

## Security

No API keys or secret values are included in this convergence record. Supabase provider secret RPC execution was verified as restricted to `postgres` and `service_role` before this convergence work.

## Promotion Boundary

This branch is intended to replace the stacked ESCD PR path only after its GitHub review gate passes. Production deployment and provider credential entry are not authorized by this record.
