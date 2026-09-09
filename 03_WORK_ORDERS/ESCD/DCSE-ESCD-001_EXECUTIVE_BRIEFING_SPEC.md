# ESCD EXECUTIVE BRIEFING SPECIFICATION

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Purpose

The ESCD briefing is a persisted-state executive reconciliation, not a conversational summary.

## Required opening briefing

Every session opening should answer, in order:

1. What changed since the last acknowledged session?
2. What completed and what evidence supports completion?
3. What requires DCS approval or decision?
4. What commitments are due or at risk?
5. What DCS Employment/revenue opportunities require action?
6. What blockers or waiting dependencies exist?
7. What is the highest-value next action and why?
8. What material watches/conditions should remain visible?

If there is no verified data for a section, state none/unknown rather than inventing narrative.

## Briefing layers

### Tier 1: Executive snapshot
One-screen summary with NOW, APPROVAL, WAITING/WATCH, completed-since-last-session, and NBA.

### Tier 2: Drill-down
Source-linked records, evidence, dates, score factors, dependencies, and decisions.

### Tier 3: Historical reconciliation
Prior briefing acknowledgement, changes since acknowledgement, and evidence trail.

## Change detection

Use stable timestamps/event IDs and the last acknowledged executive session marker. A page refresh must not reset the comparison window.

## Completion rules

A completion appears only when exit criteria/evidence support the state. Drafted, queued, attempted, or model-reported work is not automatically completed.

## Approval display

Each approval must show proposed action, consequence, destination, supporting evidence, rollback if applicable, expiration/urgency, and exact choice requested from DCS.

## Briefing tone

Precise, concise, evidence-led, prioritizing signal over activity volume. Do not congratulate the system for routine automation.

## User controls

DCS can acknowledge briefing, pin an item, change priority, defer, open evidence, approve/reject, or start the recommended action. Acknowledgement records a checkpoint; it does not alter task truth.

## Acceptance

Test empty state, first session, reload, changed state, no changes, completed item, failed item, pending approval, overdue employment item, blocked item, stale source, and contradictory-source condition.