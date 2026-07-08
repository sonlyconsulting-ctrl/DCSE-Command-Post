# TRIBUNAL SC GEMINI HANDOFF CORRECTION

Date: 2026-07-08
Prepared By: ChatGPT
Lane: SC / TI
Status: Workflow correction

## Correction

The prior handoff method was wrong because it gave Gemini the YouTube URL directly in chat-facing instructions. The intended test is GitHub-first discovery. Gemini should locate the active task from the public GitHub record and complete the review from repository-accessible materials.

## Correct Standard

Gemini should search the public repository record for the active website intake task. The repository is public, but newly created files may not appear in GitHub code search immediately. For immediate discovery, a public GitHub issue or task-queue record should be used.

## Active Repository

sonlyconsulting-ctrl/DCSE-Command-Post

## Gemini Discovery Requirement

Gemini should find the active SC website YouTube intake record from GitHub, not from a chat-provided video URL.

## Guardrail

SC / TI only. No PS crossover.
