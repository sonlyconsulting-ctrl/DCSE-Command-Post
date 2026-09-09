# ESCD COMMAND GRAMMAR SPEC

**Task ID:** DCSE-ESCD-001
**Status:** CANDIDATE IMPLEMENTATION CONTRACT

## Purpose

Natural language should be converted into an explicit operation contract before consequential execution.

## Canonical command form

`<operation> <target> [context] [constraints] [destination] [timing] [authority] [evidence]`

## Operation classes

- CAPTURE
- TRIAGE
- PLAN
- MAKE
- FIX
- DO
- DECIDE
- APPROVE
- COMMUNICATE
- RESEARCH
- ROUTINE
- MONITOR
- REVIEW
- RELEASE
- ARCHIVE

## Parsed command object

- `command_id`
- `raw_request`
- `operation`
- `target`
- `context`
- `constraints`
- `destination`
- `timing`
- `authority_class`
- `source_refs`
- `required_connectors`
- `expected_outputs`
- `evidence_required`
- `rollback/recovery`
- `ambiguities`
- `status`

## Rules

1. Low-risk ambiguity may be resolved from verified context and recorded.
2. Material ambiguity involving authority, recipient, destination, money, destructive action, privacy, or release requires clarification or approval.
3. "Make" means create a new governed artifact/product/component from an explicit baseline or defined requirements.
4. "Fix" means diagnose and correct an existing target while preserving known-good baseline and regression coverage.
5. "Continue" means advance through already-authorized non-material steps, not expand scope silently.
6. "Send", "publish", "deploy", "buy", "delete", "merge", and equivalent consequential verbs trigger authorization evaluation before execution.
7. A parsed command is not evidence that execution occurred.
8. ESCD should show the interpreted action when consequential execution is proposed.
