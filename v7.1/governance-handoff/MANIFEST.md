# V7.1 Poller and Foundational Trilogy Handoff Package

Status: PARTIAL, VERIFIED SOURCE PACKAGE

This package contains the poller source and runtime evidence available in the current ChatGPT conversation. It does not contain the four unpublished commits that exist only in the Qwen Coder `/workspace` repository.

## Included canonical-candidate source

- tribunal/v7/job_tribunal_poller_v7.py
- tribunal/v7/tribunal_v7_state_machine.py
- tribunal/v7/tribunal_v7_codex_adapter.py
- tribunal/v7/tribunal_v7_fable_adapter.py
- tribunal/v7/README.md

## Included runtime evidence

- claude_code_poller.ps1
- poller_log.txt
- poller_state.json
- start_tribunal_poller_20260604.cmd
- TRIBUNAL_20260721_POLLER_V7_PREFLIGHT_RESPONSE.snapshot.json

## Missing unpublished Coder commit payloads

These commits were reported by Coder but their file contents are not mounted in this session:

- 91b9be1acb343f2fd95e42c88db9be33f94cce07, V7.1 Foundational Trilogy Implementation Plan
- 7cd6f196ae7c7d8640f9e973621a07367cb776d4, DCS Level 0 Conditional Authorization
- 7671d829d47fedfb683960ecb53613882a5747a6, DCS Correction Notice
- 4408e5bfc9e73c0cb69ea531950d318c3448a6dc, Push requirements and post-push actions

The authentic patch range must be exported from Coder's `/workspace` using:

    git format-patch 88fdc9e..4408e5bfc9e73c0cb69ea531950d318c3448a6dc -o v7_1_trilogy_handoff

Do not reconstruct or invent these commits from summaries.
