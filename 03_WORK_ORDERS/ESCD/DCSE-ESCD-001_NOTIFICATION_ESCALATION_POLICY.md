# ESCD NOTIFICATION AND ESCALATION POLICY

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Principle

Notifications exist to surface consequential change, not to manufacture urgency. ESCD should reduce attention load, not create an alert stream that competes with the work itself.

## Classes

- **N0 Informational:** routine completion/history, normally in-app only.
- **N1 Attention:** upcoming commitment, useful update, low urgency.
- **N2 Action Required:** approval, response, deadline, blocked high-value task.
- **N3 Urgent:** near-term material deadline, failed critical workflow, major opportunity risk.
- **N4 Hard Stop:** security, authority, secret exposure, destructive-action gate, material production/release issue.

## Channel order

Target architecture: Android push primary, in-app always available, email secondary, other channels only when explicitly enabled. A channel is not considered operational until device/runtime evidence confirms delivery.

## Escalation

- N0 does not escalate.
- N1 may roll into next executive briefing.
- N2 escalates only if unacknowledged and the action window is materially shrinking.
- N3 may re-notify on a bounded cadence tied to deadline/risk.
- N4 remains visible until acknowledged/resolved and must identify the exact stop condition.

No alert may retry indefinitely.

## Quiet behavior

Routine overnight automation should aggregate into the next briefing unless a genuine N3/N4 condition occurs. Duplicate alerts with the same state/evidence are suppressed.

## Notification record

Each notification stores stable ID, class, source event, target item/job/approval, reason, created time, channel, delivery attempts, acknowledgement, escalation state, and closure reason.

## Approval notifications

Approval alerts must include the exact proposed action, consequence, destination, urgency, evidence, and approve/reject/defer choices. Never use ambiguous 'approve this' language.

## Employment notifications

Interview requests, recruiter/client deadlines, expiring submissions, and time-sensitive income opportunities may qualify as N2/N3 when evidence supports urgency.

## Acceptance

Test deduplication, quiet aggregation, failed delivery, acknowledgement, escalation, deadline change, repeated unchanged condition, N4 persistence, and no false device-delivery claim.