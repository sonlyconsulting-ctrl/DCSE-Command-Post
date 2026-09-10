# DCS SC/Gov-OS RAG Cleanup and Routing Instructions
**ID**: DCS-SC-GOVOS-RAG-CLEANUP-20260619  
**Classification**: SC Confidential // Silver Lane  
**Posture**: Candidate Only / Controlled Routing Gate  
**Authority**: DCS Level 0 Review Required Before Action  

This document defines the controlled cleanup and routing instructions for the SC/Gov-OS RAG candidate package prior to active CTO review distribution.

---

## 1. Controlled Cleanup Instructions

### Language Hygiene Normalization
*   **Violations Detected**: Review files contain non-compliant characters (e.g. em dashes, right-arrow symbols):
    *   `TRIBUNAL_RESPONSE_20260619_CLAUDE_CP_RAG_CTO_REVIEW.json`: 20 em dashes, 10 right-arrow symbols.
    *   `TRIBUNAL_RESPONSE_20260619_CLAUDE_CP_CTO_INBOX_REVIEW.json`: 12 em dashes.
    *   `TRIBUNAL_RESPONSE_20260619_CLAUDE_CP_CTO_INBOX_REVIEW.md`: 18 em dashes.
*   **Hygiene Rule**: All active review files must use standard ASCII/UTF-8 clean formatting.
*   **Action**: Cleanse raw formatting. However, the original CTO responses must be preserved as source evidence. Normalized copies or summaries may be created only after explicit DCS approval.

### Filename Mismatch Correction
*   **Issue**: `TRIBUNAL_RESPONSE_20260619_CLAUDE_CP_RAG_CTO_REVIEW.json` identifies the reviewer as `Claude-Code` but the manager JSON points to a non-existent `TRIBUNAL_RESPONSE_20260619_CLAUDE_CODE_RAG_CTO_REVIEW.json`.
*   **Action**: Resolve the mismatch by copy/alias record linking, not by deletion of original files. Preserve the original source files intact.

### SQL Validation Posture
*   **Action**: Keep the SQL validation status in all specs and build logs strictly labeled as:  
    `SQL draft prepared for later validation`

---

## 2. Git Push Instructions for Codex (Separate DCS Gate)

Git push actions represent a separate DCS authorization gate. Codex must not execute git operations until the following are satisfied:
*   **Pre-push Review**: Review `git status` output to exclude untracked, temp, or unrelated files.
*   **Commit Scope**: Only authorized candidate specifications and schemas under `SC_Gov-OS` may be committed.
*   **Forbidden Content**: Strictly block the staging or pushing of secrets, active Supabase connection keys, active RAG seed records, or PS restricted litigation content.
*   **Target Details**:
    *   *Repository*: `DCSE-Tribunal-Relay`
    *   *Remote*: `origin`
    *   *Branch*: `main` (or designated candidate branch `dcse-tribunal-authorization-process-713e2` only if authorized).

---

## 3. Reviewer Roster Reconciliation

*   **Claude-Code**: Current review exists under `CLAUDE_CP_RAG_CTO_REVIEW.json` (pending filename mismatch aliasing).
*   **Claude-CoWork**: Current file `CLAUDE_CP_CTO_INBOX_REVIEW.json` is registered as an inbox identity correction (due to being marked `BLOCKED AWAITING AG ADDENDUM` during the inbox pre-check). It does not count as a full post-addendum RAG CTO review unless DCS explicitly waives or accepts it.
*   **Qwen Coder**: Missing current RAG CTO review. Must be routed to complete its slot. Do not tell AG that all CTO inputs are complete.

---

## 4. RAG Manager Activity Comments

*   **Current State Comment**: Append comment to the manager activity log:  
    `2 current RAG reviews received + 1 Cowork identity correction + Qwen Coder missing`
*   **Hygiene Comment**: Log the active language hygiene violations.
*   **Completeness Guard**: Ensure the system does not flag the collection phase as complete until Qwen Coder's review is obtained or DCS waives it.
