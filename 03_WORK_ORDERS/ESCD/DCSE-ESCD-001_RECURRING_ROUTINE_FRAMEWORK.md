# ESCD RECURRING ROUTINE FRAMEWORK

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Purpose

Define repeatable assistant work that can recur without turning ESCD into uncontrolled background automation.

## Routine record

Each routine stores stable ID, mission, purpose, trigger/schedule, autonomy class, source inputs, action template, approval requirement, expected evidence, failure policy, escalation class, last run, next run, and owner.

## Routine types

- executive briefing
- inbox/pin triage
- employment follow-up review
- deadline/watch review
- project/status reconciliation
- evidence/receipt completeness check
- connector health check
- knowledge/DDNA candidate harvest
- recurring personal/executive reminder

## Trigger model

Routines may be time-based, event-based, or condition-based. Trigger firing only creates an eligible execution event; it does not bypass authorization or stop-gates.

## Execution contract

`TRIGGER -> ELIGIBILITY -> SOURCE READ -> DEDUPE -> AUTONOMY CHECK -> EXECUTE/PROPOSE -> VERIFY -> EVIDENCE -> NEXT RUN`

## Idempotency

Each run has a stable run ID and dedupe key. Replays must not create duplicate sends, calendar events, tasks, approvals, or evidence records.

## Missed runs

On recovery, ESCD evaluates whether a missed run is still useful. It must not blindly replay every missed occurrence. Material deadlines may escalate; obsolete routine occurrences close as skipped with reason.

## Pause/cancel

DCS can pause or disable a routine without deleting history. Routine changes preserve prior configuration version and effective timestamp.

## Acceptance

Test normal run, duplicate trigger, missed run, paused routine, changed schedule, failed connector, approval-required action, restart recovery, and bounded retry.