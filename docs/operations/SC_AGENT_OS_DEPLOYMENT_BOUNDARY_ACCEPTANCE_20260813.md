# SC Agent OS Deployment Boundary Acceptance

**Date:** 2026-08-13
**Test branch:** `test/sc-agent-os-deployment-boundary-20260813`
**Application:** `sc-agent-os`
**Root Directory:** `apps/sc-agent-os`
**Status:** ACCEPTANCE IN PROGRESS

## Test 1: targeted application-root change

Commit `dc865516f04ca3c1e1c5a5955f8149fa8d692d8d` added only an operational evidence file under `apps/sc-agent-os/docs/`.

Observed result:

- `sc-agent-os` created deployment `dpl_G5xjcgxzR24Ywa7Dp5qbnNSoFaeC`.
- deployment reached `READY`.
- preview returned HTTP 200 and rendered `SC Agent OS v1.3 — Mission Control`.
- `consumer-shell` created no deployment.
- `dcse-asset-portal` created no deployment.
- `mental-ingenuity-qa` created no deployment.
- `sc-command-post` created only a canceled/ignored deployment because it remains deliberately frozen.

This proves the SC Agent OS application root can trigger its own Vercel project while the three disconnected projects remain silent.

## Test 2: documentation-only change outside application root

This file is the second acceptance change. It is intentionally located under `docs/operations/`, outside `apps/sc-agent-os`.

Expected result:

- `sc-agent-os` must not execute a build because neither its root directory nor a dependency changed.
- `sc-command-post` remains ignored/frozen.
- the three disconnected projects remain silent.
- Supabase remains path-filtered because `supabase/` is unchanged.
- obsolete one-shot Ollama GitHub workflow remains absent.

Final disposition will be recorded after platform evidence is collected.
