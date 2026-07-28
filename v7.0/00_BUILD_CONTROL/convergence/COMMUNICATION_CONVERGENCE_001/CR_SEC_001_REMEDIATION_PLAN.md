# CR-SEC-001 Remediation and Rollback Plan

Date: 2026-07-28  
Target: Supabase staging project `liwdquzuigrlgfzgmpjp` only  
Production and v6.9: out of scope and unchanged

## Confirmed pre-remediation state

- `v7-worker-auth` deployment version 1 is `ACTIVE`, has `verify_jwt=false`, and has deployment bundle SHA-256 `0543b0f68f8de3276c0bd931aee4d22d150426907a619b63067ebc591e8b1c20`.
- The deployed source accepts a caller-asserted allowlisted `agent_id` and directly signs an HS256 token. It does not require an enrollment secret.
- `v7-worker-token` deployment version 2 is `ACTIVE`, has `verify_jwt=false`, and has deployment bundle SHA-256 `f4ceb9efe0125ee4c40cfb68d48bc00c44d37a1e61677b749007293d7379a6df`.
- `v7-worker-token` requires both `agent_id` and `enrollment_secret`, validates the bcrypt-backed enrollment through `public.v7_verify_worker_enrollment`, and then uses Supabase Auth to obtain the worker session.
- Repository runtime callers use `v7-worker-token`. No repository runtime caller uses `v7-worker-auth`.
- Repository mentions of `v7-worker-auth` are governance findings, exclusion assertions, and this rollback package.
- The available recent Edge Function log window showed `v7-worker-token` requests, including successful and safely rejected requests, and no observed `v7-worker-auth` invocation.
- Windows scheduled-task enumeration was unavailable under the sandbox identity and therefore remains an explicit verification item.

## Decommission action

Deploy `supabase/decommission/v7-worker-auth/index.ts` to the existing staging slug `v7-worker-auth` with `verify_jwt=false`. The replacement handler ignores all credentials and request content and returns HTTP 410 with `endpoint_decommissioned`. It contains no signing library, JWT secret reference, Supabase credential reference, or token-minting path.

This route-preserving tombstone is preferred to an immediate delete because it gives existing callers an explicit deterministic failure, supports direct negative validation, and is reversible. Deletion may follow only after the post-deployment log window confirms no valid dependency.

## Required post-deployment proof

1. List the staging functions and confirm `v7-worker-auth` has a new version, remains `verify_jwt=false`, and its deployment hash differs from version 1.
2. POST an allowlisted caller-asserted identity without credentials. Require HTTP 410 and confirm no `access_token`, `refresh_token`, or JWT-shaped value exists in the response.
3. POST without a body or authentication. Require HTTP 410.
4. Call `v7-worker-token` with missing and invalid enrollment secrets. Require safe 400/401 results.
5. Call `v7-worker-token` with the governed worker enrollment secret without logging that secret or returned token. Require HTTP 200 and record only status and non-secret claim metadata.
6. Confirm a fresh worker heartbeat and one SC-safe authentication/task-path check.
7. Re-run deterministic, CI, secret, RLS, RPC, drift, rollback, advisor, and endpoint-security checks without rerunning Gate 001.

## Rollback artifact and procedure

The exact vulnerable deployment source is preserved at `supabase/rollback/v7-worker-auth-v1/index.ts` for audit and emergency reconstruction. It is classified ARCHIVE and must not be redeployed without a new security review because redeployment would reopen CR-SEC-001.

Operational rollback for a false-positive dependency discovery is:

1. Keep the 410 tombstone deployed while the dependent caller is migrated to `v7-worker-token`.
2. If immediate service restoration is essential, deploy a temporary deny-by-default compatibility handler that authenticates against the canonical enrollment-secret verification RPC; do not redeploy archived v1.
3. Validate the compatibility handler with the same negative and positive endpoint suite.
4. Remove the compatibility handler after caller migration and restore the 410 tombstone or delete the obsolete slug.

No database schema, RLS policy, RPC grant, worker permission, production deployment, or v6.9 artifact is changed by this plan.

## Completion state

The user supplied a CR-SEC-001-only override for staging and GitHub closeout operations. The version 2 HTTP 410 tombstone was deployed at 2026-07-28T06:10:58Z with deployment SHA-256 `d1e5964f817a0144dbad289c0546e471c9b2b63ab7df445f086cde96f3477773`.

All required staging endpoint, canonical broker, SC-safe path, heartbeat, RLS/RPC, drift, permission, advisor, and transactional rollback checks passed without rerunning Gate 001. CR-SEC-001 is CLOSED; publication and canonical merge remain the next gate.
