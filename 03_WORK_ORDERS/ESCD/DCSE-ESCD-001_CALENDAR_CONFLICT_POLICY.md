# ESCD CALENDAR AND CONFLICT POLICY

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD should make the calendar operationally useful without silently changing commitments.

## Core behavior

ESCD may read authorized calendar state, reconcile it with tasks/routines, identify conflicts, prepare meetings, recommend schedule changes, and create proposed calendar actions. External calendar writes remain governed by the autonomy contract.

## Conflict classes

- `C1 overlap`: two events occupy overlapping time.
- `C2 travel/buffer`: insufficient transition time between events.
- `C3 task-deadline`: scheduled commitment conflicts with a high-priority due item.
- `C4 preparation`: required preparation has no feasible time before meeting/event.
- `C5 recurring collision`: recurring routines repeatedly collide with higher-value commitments.
- `C6 stale/tentative`: tentative or stale event may distort planning.

## Required conflict output

- affected events/tasks
- conflict class
- time window
- source refs
- impact
- options
- recommended resolution
- approval requirement

## Meeting preparation

For material meetings, ESCD may assemble:

- purpose
- participants/context
- prior decisions/commitments
- open questions
- files/evidence
- desired outcome
- follow-up items

## Rules

1. Do not delete, reschedule, invite, decline, or accept externally without authorization.
2. Treat calendar source data as source evidence, not model memory.
3. Prefer surfacing conflicts before manufacturing free time.
4. Preserve explicit DCS overrides.
5. Do not repeatedly alert on unchanged conflicts after acknowledgement unless the situation worsens or deadline approaches.
6. Distinguish hard events from flexible holds/routines when source-supported.
7. Meeting prep may be generated automatically when low-risk; external attendee actions remain approval-gated.
