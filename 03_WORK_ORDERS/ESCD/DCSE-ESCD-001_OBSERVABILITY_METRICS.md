# ESCD OBSERVABILITY AND OPERATING METRICS

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Purpose

ESCD should be measurable as an executive operating system. Metrics support diagnosis and improvement; they do not replace evidence or encourage activity for its own sake.

## Health metrics

- active NOW count
- APPROVAL count and oldest age
- WAITING/WATCH count by trigger type
- overdue actionable commitments
- jobs by lifecycle state
- failed jobs and retry exhaustion
- connector health/freshness
- notification delivery/acknowledgement failures
- briefing generation freshness
- evidence-link completeness

## Flow metrics

- capture-to-triage latency
- triage-to-action latency
- approval wait time
- cycle time from active to verified completion
- blocked/waiting time
- duplicate suppression count
- reopen rate
- failed/uncertain external side-effect count

## Value metrics

Where supported by evidence:

- DCS Employment opportunities progressed
- submissions completed with receipt
- interviews/follow-ups generated from real opportunities
- high-value commitments completed on time
- recurring manual steps reduced through verified workflows

Do not invent financial ROI or attribute revenue to ESCD without a defensible causal record.

## Quality metrics

- NBA agreement/override rate
- briefing correction rate
- false-positive urgency/escalation rate
- duplicate-task creation rate
- unsupported-claim detection count
- approval bypass attempts blocked
- stale/contradictory source incidents surfaced

## Audit events

Material actions emit structured events for state transition, actor/executor, source, authorization class, result, evidence ref, and error/rollback where relevant. Logs must avoid secrets and unnecessary sensitive payloads.

## Dashboard principle

Show exception and decision signal first. Healthy routine automation should not dominate the executive UI.

## Acceptance

Metrics implementation must be derived from persisted operational events, reproducible from source records where practical, and resilient to restart. A metric with unknown/partial coverage must be labeled accordingly.