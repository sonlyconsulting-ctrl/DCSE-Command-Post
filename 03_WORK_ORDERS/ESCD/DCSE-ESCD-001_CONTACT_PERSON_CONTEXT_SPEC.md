# ESCD CONTACT / PERSON CONTEXT SPEC

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD needs useful person context without turning informal model inference into authoritative contact data.

## Source separation

- Contact system remains source of truth for saved contact fields.
- Email/calendar/message systems remain source evidence for communications and interactions.
- ESCD may maintain derived relationship context only with provenance and confidence/status.

## Context object

- `person_context_id`
- `contact_ref`
- `display_name`
- `organization/role` when source-supported
- `relationship_context`
- `active_commitments`
- `waiting_on_them`
- `they_are_waiting_on_dcs`
- `recent_interaction_refs`
- `next_follow_up_at`
- `communication_preferences` when observed or explicitly set
- `important_dates` when source-supported
- `notes`
- `provenance_refs`
- `confidence/status`
- `last_reconciled_at`

## Rules

1. Do not overwrite Google Contacts or another source-of-truth system from inference.
2. Separate verified contact facts from assistant-derived context.
3. Do not infer sensitive traits.
4. A stale relationship summary must not override newer source evidence.
5. Deduplicate identities using verified identifiers where available.
6. External communication still follows approval policy.
7. Person context should support follow-up and briefing, not create unsolicited surveillance behavior.
