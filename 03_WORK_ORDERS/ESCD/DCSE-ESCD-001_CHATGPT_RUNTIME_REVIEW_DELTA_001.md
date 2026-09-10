# ESCD Runtime Review Delta 001

**Task ID:** DCSE-ESCD-001  
**Review target:** PR #72 / `feature/escd-runtime-repair-001`  
**Status:** PARTIAL, NON-RELEASE  

## Purpose

Record the additional independent runtime review performed after the initial AG01 reconciliation. This delta preserves the existing implementation and repairs only confirmed integrity defects. It does not authorize production deployment, production DDL, merge, credential changes, or unrelated migration cleanup.

## Confirmed repairs

1. Briefing acknowledgement cursor now rejects malformed, timezone-naive, future, and regressive acknowledgement timestamps at the API boundary.
2. Candidate database transition validation no longer accepts any historical approved record. It evaluates the latest approval deterministically by `requested_at DESC, id DESC`.
3. Job status transitions now emit append-oriented `status_transition` events through a database trigger so lifecycle history is retained independently of chat state.
4. Candidate database acknowledgement guard rejects principal mismatch, future acknowledgement, and regressive cursor movement.
5. Runtime reads now use deterministic tie-break ordering for jobs, evidence, approvals, events, and briefing acknowledgements.
6. Completion transition no longer trusts a request-body `exit_criteria_met` assertion. The runtime consumes persisted job verification state and therefore fails closed until a governed verification path records exit-criteria satisfaction.

## Preserved controls

- User JWT and DCS operator authorization remain the normal runtime boundary.
- No service-role credential was introduced into normal ESCD runtime code.
- Existing RLS approach remains intact.
- No production database mutation was performed.
- No main merge was performed.
- No Employment workflow was added to ESCD core.
- No DDNA production consumer cutover was bundled into this work.

## Remaining release dispositions

The following must be resolved or explicitly dispositioned before PR #72 can leave draft/review status:

1. Exact approval action/payload binding remains incomplete. The autonomy contract requires material approval to bind to the specific action/payload/version. Current candidate schema/runtime does not yet prove that binding end to end.
2. Persisted exit-criteria verification now fails closed, but the governed verification write path is not yet implemented in this runtime slice.
3. Approval-decision append history should be proven behaviorally, not inferred from mutable current-row state.
4. Full post-repair functional and adversarial test passes have not yet been executed against the new review delta.
5. Supabase Git Preview remains blocked by an unrelated historical migration-chain error involving missing schema `family_vow_go`.
6. Vercel preview/status checks are currently blocked by the account daily deployment quota. These external failures are not evidence that ESCD runtime code is correct or incorrect.

## Release posture

PR #72 remains draft and must not be merged or deployed to production until the acceptance matrix hard gates pass with fresh evidence.

Structure Precedes Scale.
