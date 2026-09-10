# ESCD Runtime Review Delta 001

**Task ID:** DCSE-ESCD-001  
**Review target:** PR #72 / `feature/escd-runtime-repair-001`  
**Status:** PARTIAL, NON-RELEASE  

## Purpose

Record the additional independent runtime review performed after the initial AG01 reconciliation. This delta preserves the existing implementation and repairs only confirmed integrity defects. It does not authorize production deployment, production DDL, merge, credential changes, or unrelated migration cleanup.

## Confirmed repairs

1. Briefing acknowledgement cursor rejects malformed, timezone-naive, future, and regressive acknowledgement timestamps at the API boundary.
2. Candidate database transition validation no longer accepts any historical approved record. Approval lookup is deterministic and bound to the exact transition action key.
3. Approval records now carry an explicit `action_key`, optional `payload_fingerprint`, expiration, and conditions fields for material action binding.
4. Expired approvals cannot authorize a transition and cannot be newly approved through the runtime decision path.
5. Job status transitions emit append-oriented `status_transition` events through a database trigger.
6. Approval status transitions emit append-oriented `approval_transition` events with action key and payload fingerprint provenance.
7. RLS write checks bind creator/requester/actor/decision identity fields to the authenticated principal instead of allowing caller-supplied provenance identities.
8. Candidate database acknowledgement guard rejects principal mismatch, future acknowledgement, and regressive cursor movement.
9. Runtime reads use deterministic tie-break ordering for jobs, evidence, approvals, events, and briefing acknowledgements.
10. Completion transition no longer trusts a request-body `exit_criteria_met` assertion. The runtime consumes persisted job verification state and fails closed until a governed verification path records exit-criteria satisfaction.

## Preserved controls

- User JWT and DCS operator authorization remain the normal runtime boundary.
- No service-role credential was introduced into normal ESCD runtime code.
- Existing RLS architecture remains intact and was tightened for provenance identity.
- No production database mutation was performed.
- No main merge was performed.
- No Employment workflow was added to ESCD core.
- No DDNA production consumer cutover was bundled into this work.

## Remaining release dispositions

The following must be resolved or explicitly dispositioned before PR #72 can leave draft/review status:

1. Persisted exit-criteria verification now fails closed, but the governed verification write path is not yet implemented in this runtime slice.
2. Full post-repair functional and adversarial test passes have not yet been executed against the current review head.
3. Supabase Git Preview remains blocked by an unrelated historical migration-chain error involving missing schema `family_vow_go`.
4. Vercel preview/status checks are currently blocked by the account daily deployment quota. These external failures are not evidence that ESCD runtime code is correct or incorrect.
5. No GitHub Actions workflow currently runs for this branch, so there is no independent repository CI evidence for the current head.

## Release posture

PR #72 remains draft and must not be merged or deployed to production until the acceptance matrix hard gates pass with fresh evidence.

Structure Precedes Scale.
