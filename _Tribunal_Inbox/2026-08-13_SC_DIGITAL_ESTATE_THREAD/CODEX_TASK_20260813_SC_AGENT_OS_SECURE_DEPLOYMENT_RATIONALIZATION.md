# Codex Task: SC Agent OS Secure Deployment Rationalization

**Date:** 2026-08-13
**Lane:** DCSE / SC infrastructure
**Status:** AUTHORIZED FOR IMPLEMENTATION / NO PRODUCTION PROMOTION
**Incident:** TRIB-INC-20260813-GITHUB-VERCEL-001

## Objective

Convert the current SC Agent OS deployment into one explicit, secure application boundary that can be deployed from a dedicated repository path without losing the existing authentication/security wrapper.

## Verified current state

1. `os.sonlyconsulting.com` is currently served by the Vercel project `sc-agent-os` and the known production deployment remains protected by the DCSE Secure Access screen.
2. The repository root contains the secure gateway in `api/index.js`. It imports `apps/sc-agent-os/api/index.js` and adds Supabase authentication, secure cookies, operator validation, password recovery, CSP/security headers, and server-managed provider credentials.
3. `apps/sc-agent-os/api/index.js` is the underlying Mission Control application.
4. A controlled preview built with Vercel Root Directory `apps/sc-agent-os` returned SC Agent OS directly without the secure gateway. Therefore `apps/sc-agent-os` is not yet a safe standalone production root.
5. The current direct application implementation contains legacy browser-side API-key entry/storage behavior. Production currently depends on the root secure wrapper to suppress/replace that behavior. Do not regress this protection.
6. `sc-command-post` is frozen and currently has no verified unique custom production domain. Treat it as a retirement/merge candidate, not as a second active production application unless evidence proves an independent lifecycle.
7. `consumer-shell`, `dcse-asset-portal`, and `mental-ingenuity-qa` have been disconnected from `DCSE-Command-Post` Git automation. Mental Ingenuity production was restored and verified before disconnection.
8. `sc-agent-os` and `sc-command-post` are temporarily frozen in Vercel with Ignored Build Step = Don't build anything.

## Required target state

Preferred target unless code evidence requires a safer alternative:

`apps/sc-agent-os` becomes the canonical deployable root for both secure access and Mission Control.

Within that root:

- authentication remains mandatory before Mission Control renders;
- Supabase auth/session handling remains server-side where currently implemented;
- secure cookie behavior remains intact;
- CSP, no-store, referrer, and content-type security headers remain intact;
- provider API credentials remain server-managed;
- no raw provider API keys are stored in browser localStorage, exposed in client HTML, logged, or committed;
- password-recovery behavior remains functional;
- `os.sonlyconsulting.com` remains the intended production domain;
- underlying Mission Control functionality remains behaviorally equivalent except where a security defect requires correction;
- PS firewall/lane isolation must not weaken.

A compatibility shim at repository root is acceptable temporarily if needed for rollback, but production source ownership must become explicit and bounded.

## Engineering requirements

1. Inspect complete current implementations before editing:
   - `api/index.js`
   - `api/chat.js`
   - `vercel.json`
   - `apps/sc-agent-os/api/index.js`
   - `apps/sc-agent-os/vercel.json`
   - `apps/sc-agent-os/package.json`
2. Refactor with the smallest safe delta. Prefer extraction/composition over rewriting business/UI behavior.
3. Add automated tests or executable validation for at least:
   - unauthenticated `/` returns secure access, not Mission Control;
   - authenticated path delegates to Mission Control;
   - password recovery route remains available;
   - provider cloud chat path does not require or expose client-supplied raw API credentials;
   - security headers are present on auth surfaces;
   - direct Mission Control cannot be reached by bypassing the wrapper through a public route;
   - PS-sensitive behavior is not introduced into SC/public surfaces.
4. Run static scan for raw secret patterns and browser storage key names.
5. Preserve rollback to the current verified production deployment until the new preview passes independent review.
6. Do not promote production and do not unfreeze `sc-command-post`.
7. Do not change Supabase schema/data in this task.
8. Do not change Mental Ingenuity, consumer-shell, or dcse-asset-portal.

## Vercel acceptance sequence

After local/repository tests pass:

1. Produce a branch/PR release candidate.
2. Coordinate a preview deployment of only `sc-agent-os` from the intended dedicated root.
3. Verify by content, not READY status alone:
   - preview root shows DCSE Secure Access while unauthenticated;
   - authenticated path reaches SC Agent OS Mission Control;
   - no provider key input/localStorage regression;
   - no unrelated Vercel projects deploy;
   - `sc-command-post` remains frozen.
4. Return evidence and stop before production promotion.

## sc-command-post disposition analysis

Determine whether `sc-command-post` has any current unique function, domain, environment binding, or lifecycle that is not already part of SC Agent OS secure access. Return one recommendation:

- `RETIRE VERCEL PROJECT`
- `RETAIN AS DISTINCT SECURE GATEWAY`
- `MERGE INTO SC AGENT OS`

Preferred default is `MERGE INTO SC AGENT OS` unless contrary evidence exists.

## Required evidence

Return a concise receipt containing:

- branch and commit SHA;
- changed files;
- before/after architecture;
- test commands and results;
- secret scan result;
- preview deployment ID/URL if created;
- unauthenticated content verification;
- authenticated verification result or explicit blocker;
- Vercel project activity showing unrelated projects remained silent/contained;
- recommended `sc-command-post` disposition;
- rollback target;
- unresolved risks;
- final disposition: `READY_FOR_INDEPENDENT_REVIEW`, `BLOCKED`, or `NOT_READY`.

## Stop conditions

Stop and report rather than improvise if:

- authentication behavior cannot be preserved;
- a service-role or other privileged Supabase credential would need to enter browser code;
- provider credentials would need to be exposed client-side;
- production promotion is required to validate the change;
- source ownership is ambiguous after inspection;
- tests indicate direct unauthenticated Mission Control exposure.

## Governance

Evidence outranks narrative. No completion claim without executable evidence. Self-authored changes require independent review before production promotion. Production remains frozen until DCS authorizes release after review.
