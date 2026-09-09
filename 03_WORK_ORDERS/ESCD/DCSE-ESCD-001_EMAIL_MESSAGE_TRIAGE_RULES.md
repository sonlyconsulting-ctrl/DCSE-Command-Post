# ESCD EMAIL / MESSAGE TRIAGE RULES

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD should turn communications into actionable executive state while preserving the source message and avoiding autonomous external commitments.

## Triage classes

- `ACTION`: DCS must do something.
- `REPLY`: response is required or prudent.
- `WAITING`: DCS has acted and is awaiting another party.
- `DECISION`: material choice or approval is required.
- `SCHEDULE`: meeting/date/calendar action.
- `REFERENCE`: useful information, no current action.
- `WATCH`: condition/status/future response should be monitored.
- `ARCHIVE_CANDIDATE`: no active value after verification.

## Extraction contract

For each actionable communication, capture:

- source/message/thread reference
- sender/participants
- received_at
- concise subject/purpose
- requested action
- explicit deadline/date
- inferred deadline separately labeled if any
- commitment made by DCS, if source-supported
- commitment made by others, if source-supported
- required files/context
- urgency/importance
- suggested next action
- approval class
- follow-up trigger

## Drafting behavior

ESCD may automatically prepare drafts when context is sufficient and low-risk. Drafts must preserve factual uncertainty and must not invent commitments, rates, dates, qualifications, outcomes, or attachments.

## Sending rules

1. External send is approval-gated by default.
2. A future explicit delegation may permit narrowly scoped low-risk sends, but the scope must be recorded and revocable.
3. Replies that create obligations, spend money, release confidential information, accept terms, make public claims, or alter schedules require explicit approval.
4. Verify recipient identity before consequential send.
5. Preserve sent-message evidence after actual send.

## Anti-noise rules

- Do not create separate tasks for every message in a thread if they represent one commitment.
- Update the existing task/thread relationship where appropriate.
- Newsletters/automated notifications should not enter NOW unless they create a real obligation or material signal.
- Acknowledged unchanged messages do not re-escalate without new information.
