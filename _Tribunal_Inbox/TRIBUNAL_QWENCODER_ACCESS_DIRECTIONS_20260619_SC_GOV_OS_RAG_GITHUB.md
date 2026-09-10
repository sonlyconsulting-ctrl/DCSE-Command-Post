# QwenCoder Access Directions: SC Gov-OS RAG GitHub Relay

Status: ACTIVE_DIRECTIONS_FOR_QWENCODER_REVIEW
Lane: SC/Gov_OS
Boundary: GitHub relay access and Tribunal reporting only. No live database work, no RAG seeding, no public packaging.

## Access Now

Repository:

`https://github.com/sonlyconsulting-ctrl/DCSE-Tribunal-Relay`

Branch:

`main`

Latest known commits to review:

- `7bc2f2b8fb79b6d14541d0c267fff500c61a5de2`: post-success Tribunal GitHub push proof
- `5a134721c3dbc3eb0daea9000a731981d7e656cf`: SC Gov-OS Tribunal coordination records

QwenCoder should clone the repository or pull latest `main`. If already cloned, run `git pull origin main` and record the commit hash reviewed.

## Required Starting Files

- `TRIBUNAL_20260619_SC_GOV_OS_RAG_CTO_REVIEW_MANAGER.json`
- `TRIBUNAL_GITHUB_PUSH_REPORT_20260619_SC_GOV_OS_RAG_COORDINATION.json`
- `TRIBUNAL_INSTRUCTION_20260619_SC_GOV_OS_AG_QWEN_GITHUB_SCHEMA_CLOSEOUT.json`
- `DCS_SC_GOV_OS_RAG_CLEANUP_AND_ROUTING_INSTRUCTIONS_20260619.md`
- `TRIBUNAL_RESPONSE_20260619_CTO1_CODEX_SC_GOV_OS_RAG_REVIEW.json`
- `TRIBUNAL_RESPONSE_20260619_CLAUDE_CP_RAG_CTO_REVIEW.json`
- `TRIBUNAL_ACTIVITY_LOG_CHECK_20260619_CLAUDE_COWORK_CODE_CORRECTIONS.json`

## Current QwenCoder Task

Task ID:

`QWENCODER_SC_GOV_OS_RAG_TECHNICAL_REVIEW_20260619`

Expected output files:

- `TRIBUNAL_RESPONSE_20260619_QWEN_CODER_SC_GOV_OS_RAG_TECHNICAL_REVIEW.json`
- `TRIBUNAL_RESPONSE_20260619_QWEN_CODER_SC_GOV_OS_RAG_TECHNICAL_REVIEW.md`

Decision options:

- `APPROVE_CANDIDATE_FOR_NEXT_TEST`
- `REVISE_BEFORE_TEST`
- `REJECT`
- `STOP_GATE`

## Required Review Focus

- schema consistency
- rule determinism
- fail routing
- edge cases
- QwenCoder GitHub relay viability
- SQL draft boundaries
- JSON schema quality
- testability
- PS firewall protection
- special conditions for Codex and AG

## Mandatory Special Conditions Relay

Every QwenCoder response must include:

`special_conditions_for_codex_and_ag`

This field must report:

- access limitations
- runtime limitations
- files unavailable
- GitHub permission limitations
- validation tools missing
- SQL validation not performed
- any suspected secret exposure
- any PS firewall concern
- any language hygiene concern
- any ambiguity requiring DCS decision
- any AG action required before QwenCoder can complete

If any special condition affects compliance, stop active work and report the condition in Tribunal before continuing.

## QwenCoder Rules

- Do not overwrite, delete, rename, or normalize existing Tribunal source responses.
- Do not treat raw reviewer output as approved knowledge or RAG seed.
- Do not request or expose credentials, service role keys, tokens, API keys, database URLs, or live connection strings.
- Do not include PS restricted content or litigation evidence in the SC/Gov_OS GitHub relay.
- Do not claim SQL validates unless parser, database, or reliable dry-run validation was actually performed and logged.
- Use ASCII-safe punctuation in new output. No em dashes. Use `->` only if an arrow is necessary.
- Create new response files only, or return response content to AG for commit if direct GitHub write is unavailable.

## Going Forward

1. Codex or AG publishes a Tribunal task packet to GitHub.
2. QwenCoder pulls latest `main` and records commit reviewed.
3. QwenCoder creates response JSON and MD, or returns them to AG for commit if direct write is unavailable.
4. QwenCoder includes `special_conditions_for_codex_and_ag` in every response.
5. AG or Codex commits the response to the Tribunal relay with proof.
6. Codex compiles the Tribunal state and reports final body-of-work status.

Tribunal remains the end-of-body-of-work record.
