# ESCD MOBILE INTERACTION MODEL

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

Mobile ESCD should optimize fast executive interaction, not reproduce the entire desktop interface at smaller scale.

## Primary mobile actions

- capture
- view NOW
- approve/reject
- defer/snooze
- mark done
- open source/evidence
- reply-draft review
- watch/unwatch
- open meeting prep
- launch/retry bounded workflow

## Core mobile surfaces

1. **Today**: briefing, NOW, approvals, calendar conflicts, watch alerts.
2. **Capture**: text-first quick capture, optional voice later.
3. **Inbox**: triage queue.
4. **Approvals**: concise consequence, evidence, action buttons.
5. **Tasks**: active/waiting/watch/backlog filters.
6. **Evidence**: source and receipt drill-down.

## Interaction rules

1. Consequential swipe/quick actions require confirmation or an undo window appropriate to consequence.
2. Approval cards must show exactly what action will occur, target/destination, and material effect.
3. Push notification text must not expose sensitive details unnecessarily.
4. Offline/poor-connectivity action must show pending state until server acknowledgement.
5. A tap is not success evidence; server-side state/evidence confirms execution.
6. Mobile layouts prioritize actionability over dense analytics.
7. Accessibility targets include readable scaling, focus/semantic labels, adequate target size, and non-color-only status signals.
8. Device-level push remains unverified until real device testing.
