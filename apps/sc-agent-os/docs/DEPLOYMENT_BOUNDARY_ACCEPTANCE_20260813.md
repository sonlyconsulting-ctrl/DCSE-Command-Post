# SC Agent OS Deployment Boundary Acceptance Record

**Date:** 2026-08-13
**Purpose:** Harmless app-root change used to verify Vercel root-directory and affected-project deployment behavior for `sc-agent-os`.

Expected result:

- `sc-agent-os` receives a deployment because this file is under `apps/sc-agent-os`.
- `sc-command-post` remains ignored/frozen.
- `consumer-shell`, `dcse-asset-portal`, and `mental-ingenuity-qa` receive no deployment because their stale Git mappings were removed.
- Supabase preview branching remains idle because `supabase/` is unchanged.
- No obsolete Ollama one-shot GitHub Actions workflow runs.

This file is operational evidence only and does not change application behavior.
