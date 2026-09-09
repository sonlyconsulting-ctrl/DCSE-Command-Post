# ESCD NEXT-BEST-ACTION SPECIFICATION

**Task ID:** DCSE-ESCD-001  
**Status:** IMPLEMENTATION CONTRACT

## Purpose

Define a deterministic, inspectable ranking engine for ESCD. Model reasoning may explain a ranking but must not silently replace the scoring policy.

## Eligibility gate

An item is rankable for NOW only when it is actionable. Items with unresolved external dependency, future trigger, missing required approval, or explicit hold route to WAITING, WATCH, or APPROVAL before scoring.

## Required factors

Each rankable item records normalized 0-100 factors and weighted contributions:

- mission priority
- task/job priority
- deadline urgency
- revenue relevance
- dependency unblock value
- commitment/customer/recruiter consequence
- aging/staleness
- effort/complexity estimate
- DCS explicit override
- risk of delay
- strategic leverage/reuse value

Blocked work receives no age-based promotion into NOW.

## Baseline scoring

Candidate default weights, adjustable only through a governed policy revision:

- mission priority: 15%
- explicit priority: 15%
- urgency: 20%
- revenue relevance: 10%
- dependency unblock value: 10%
- consequence/risk of delay: 10%
- aging: 5%
- effort efficiency: 5%
- strategic leverage: 5%
- DCS override: 5%

Weights must total 100%. Scores and factor inputs are stored with the ranking event.

## Determinism

For identical inputs and evaluation timestamp, the result must be reproducible. Tie-break order:

1. DCS override
2. hard deadline proximity
3. revenue relevance
4. unblock value
5. oldest stable item ID/order

No random tie breaking.

## DCS Employment bias

When two items are otherwise comparable, verified near-term income opportunities may outrank internal architecture work. Revenue relevance is never inferred from optimism; it must be supported by the opportunity/task record.

## Explanation contract

Every surfaced NBA must display:

- item/title
- score
- top positive factors
- penalties or missing information
- why it is actionable now
- what would change its priority
- any DCS override

## Override

DCS may pin, promote, demote, defer, or force-rank an item. Overrides must be explicit, timestamped, reversible, and visible. A model may recommend an override but cannot silently apply one.

## Recalculation triggers

Recompute when a material factor changes, including due date, approval state, dependency state, revenue relevance, status, explicit priority, DCS override, or new evidence. Do not continuously churn ranking solely because time passes by minutes.

## Acceptance

Tests must cover deterministic repeatability, blocked-item routing, overdue tasks, equal-score ties, DCS override, revenue weighting, stale-item handling, missing dates, waiting approvals, and identical input/output behavior.