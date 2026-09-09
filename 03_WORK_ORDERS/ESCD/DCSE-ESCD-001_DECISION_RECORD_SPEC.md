# ESCD DECISION RECORD SPEC

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD must distinguish a recommendation from a decision and a decision from an executed result.

## Required fields

- `decision_id`
- `title`
- `context`
- `decision_question`
- `decision_owner`
- `authority_class`
- `status`: open/recommended/decided/executing/implemented/superseded/closed
- `evidence_refs`
- `verified_facts`
- `likely_items`
- `unknowns`
- `assumptions`
- `alternatives`
- `tradeoffs`
- `risk_summary`
- `recommendation`
- `adversarial_review`
- `decision`
- `decision_rationale`
- `decided_at`
- `implementation_refs`
- `verification_refs`
- `follow_up`
- `supersedes/superseded_by`

## Rules

1. ESCD may recommend within delegated scope but may not fabricate a DCS decision.
2. A recommendation does not authorize consequential execution.
3. Material decisions require preserved alternatives and evidence.
4. Unknowns that materially affect the decision must be surfaced.
5. A decision record must be immutable as history; amendments create linked revisions.
6. Executed state requires evidence of actual execution.
7. Superseded decisions remain discoverable.
8. Decision records may be brief for routine low-risk matters and deeper for material matters.
