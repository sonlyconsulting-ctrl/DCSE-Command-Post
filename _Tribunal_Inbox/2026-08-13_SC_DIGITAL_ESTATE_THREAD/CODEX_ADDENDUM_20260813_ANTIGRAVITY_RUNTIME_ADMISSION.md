# Codex Addendum: Antigravity Runtime Admission

**Date:** 2026-08-13
**Lane:** DCSE / SYSTEM
**Status:** AUTHORIZED FOLLOW-ON IMPLEMENTATION / NO RLS REMEDIATION

## Objective

Extend the current universal dispatcher so Antigravity becomes a first-class claimable runtime and can automatically claim the already queued task `AG-SUPABASE-RLS-REVIEW-20260813`.

## Verified precondition

- Agent key `antigravity` exists in `dcse_cp.agent_registry`.
- Current status is `standby`.
- Runtime admission metadata is `REQUIRED_NOT_YET_ADMITTED`.
- No Antigravity runtime surface currently exists in `dcse_cp.runtime_surface_registry`.
- No Antigravity heartbeat currently exists.
- Queued workload `AG-SUPABASE-RLS-REVIEW-20260813` is assigned to Antigravity and must remain read-only.

## Required engineering work

1. Inspect the current neutral Windows universal dispatcher, runtime surface registry, claim logic, heartbeat logic, and repo migrations/config before editing.
2. Add the minimum governed runtime surface and dispatcher support needed to invoke Antigravity non-interactively.
3. Establish a stable runtime identity and verifiable heartbeat.
4. Preserve the distinction between logical agent identity and execution surface.
5. Preserve lane isolation. Antigravity must not gain PS access.
6. Preserve credential containment. Do not expose tokens or secrets in logs, task payloads, GitHub, or Tribunal.
7. Do not perform the Supabase RLS remediation in this task.
8. Do not broaden Antigravity authority beyond its registered allowed actions.
9. Use the real queued task `AG-SUPABASE-RLS-REVIEW-20260813` as the first admission workload after the runtime is proven.
10. If Antigravity cannot be invoked headlessly or reliably from the Windows dispatcher, stop and return the exact blocker rather than simulating success.

## Acceptance criteria

- `runtime_surface_registry` contains an explicit Antigravity execution surface with correct family, polling mode, enabled state, and claimability.
- Host/runtime emits a valid heartbeat for that surface.
- Dispatcher can route an Antigravity-assigned task without user copy/paste.
- `AG-SUPABASE-RLS-REVIEW-20260813` is claimed by Antigravity only after admission passes.
- The RLS review executes read-only and returns evidence/receipt.
- No production RLS/DDL change is made by Antigravity.
- No PS access, credential exposure, autonomous publish/deploy/delete, or production DB write is introduced.
- Rollback is documented.
- GitHub, Supabase, runtime state, and Tribunal evidence reconcile.

## Stop gate

Do not mark Antigravity admitted based on registry insertion alone. Admission requires a real host heartbeat plus a successful governed task claim and receipt.
