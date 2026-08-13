# Tribunal Progress Record: Vercel Remediation Confirmed

**Date:** 2026-08-13  
**Incident:** `TRIB-INC-20260813-GITHUB-VERCEL-001`  
**Lane:** DCSE / SC infrastructure  
**Status:** MANUAL REMAPPING COMPLETE / ACCEPTANCE TEST PENDING

## Confirmed completed actions

DCS completed the required Vercel UI remediation steps:

- `consumer-shell` disconnected from `DCSE-Command-Post` Git integration.
- `dcse-asset-portal` disconnected from `DCSE-Command-Post` Git integration.
- `mental-ingenuity-qa` restored to the known-good Mental Ingenuity deployment and disconnected from `DCSE-Command-Post` Git integration.
- `mental-ingenuity-qa.vercel.app` independently verified to return the Mental Ingenuity application after promotion.
- `sc-agent-os` Root Directory set to `apps/sc-agent-os`.
- `sc-agent-os` root-aware skip behavior enabled for changes outside the root directory/dependencies.
- `sc-agent-os` remains temporarily frozen with `Don't build anything` pending acceptance testing.
- `sc-command-post` remains frozen pending domain/application ownership reconciliation.

## Repository remediation branch

Branch:

`fix/github-vercel-trigger-containment-20260813`

Current material branch delta relative to main:

- remove obsolete `.github/workflows/one-shot-fix-ollama-completion.yml`;
- add incident record;
- add Vercel project/source ownership reconciliation record;
- add candidate deployment ownership/trigger boundary standard.

The transitional repository-wide Vercel ignore script was removed after the three orphan mappings were disconnected and `sc-agent-os` was correctly root-scoped.

## Remaining acceptance work

1. Open and review remediation PR.
2. Verify GitHub Actions no longer produces the obsolete one-shot Ollama failure.
3. With `sc-agent-os` still frozen, merge/perform a documentation-only source change and verify:
   - disconnected projects remain silent;
   - `sc-agent-os` does not actively build;
   - `sc-command-post` remains contained;
   - Supabase ignores the change when `supabase/` is unchanged.
4. After Test 1 passes, remove the temporary freeze only from `sc-agent-os` and perform one bounded `apps/sc-agent-os` change to prove targeted deployment behavior.
5. Reconcile `sc-command-post` domain/application ownership before re-enabling its Git deployment.
6. Complete Tribunal/Supabase/GitHub closeout only after evidence passes.

## Stop-Gate

Do not unfreeze `sc-command-post`.

Do not reconnect the three disconnected Vercel projects to `DCSE-Command-Post` without a verified corresponding source root and ownership record.

Do not remove the `sc-agent-os` temporary freeze until the documentation-only acceptance test is complete.
