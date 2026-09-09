# ESCD DDNA CANDIDATE INGESTION CONTRACT

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

ESCD may surface potentially reusable knowledge, preferences, patterns, rules, templates, and observations to DDNA as candidates. ESCD does not promote them to authority.

## Candidate package

- `candidate_id`
- `candidate_type`: fact/preference/pattern/rule/template/procedure/relationship/context/other
- `statement_or_payload`
- `source_refs`
- `provenance_chain`
- `observed_at`
- `scope`
- `confidence/status`: verified/likely/unknown/assumption
- `conflict_refs`
- `duplication_refs`
- `sensitivity/lane`
- `proposed_consumers`
- `retention recommendation`
- `submitted_by`
- `submission_reason`

## Rules

1. DDNA candidate presence is not authority.
2. ESCD must preserve source provenance and material contradictions.
3. Candidate extraction from communications must respect source permissions and confidentiality.
4. Do not include secrets, credentials, private keys, recovery codes, or hidden auth material.
5. Protected/sensitive lane material cannot be widened into general DDNA without explicit authorization.
6. Duplicate/conflicting candidates should link rather than overwrite each other.
7. Preferences inferred from repeated behavior remain inferred until explicitly confirmed or promoted under governed DDNA rules.
8. ESCD consumes only the DDNA authority/status returned by the governed DDNA process.
9. Dedicated DDNA consumer cutover remains a separate runtime release stream and is not authorized by this contract.
