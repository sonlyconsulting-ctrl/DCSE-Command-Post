# DCSE Doctrine D04: Command Post Communications

**Document ID:** DCSE-D04  
**Version:** v7 reconciliation candidate  
**Last Modified:** 2026-07-29  
**Status:** CANDIDATE FOR PROMOTION  
**Classification:** CONFIDENTIAL  
**Lane:** DCSE / SC  
**Canonical file:** `D04_Command_Post_Communications.md`

## 1. Purpose

D04 governs operational packets, Tribunal records, GitHub communication, source routing, handoffs, receipts, and conflict reporting.

## 2. Communication Layers

### 2.1 Operational Tribunal Inbox

`C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`

Use for active task coordination, execution packets, model handoffs, and immediate operational receipts.

### 2.2 Hub Tribunal Inbox

`C:\DS All Things\DCSE_Command_Center\v6.9\05_Tribunal_Inbox`

Use for doctrine errors, Stop-Gates, governance notices, drift reports, promotion records, and compliance receipts.

### 2.3 Supabase Runtime Communication

Supabase may store governed task state, acknowledgements, execution queues, promotion logs, source references, and model-access records. Supabase records must identify the canonical GitHub artifact and matching integrity hash under D20.

## 3. Required Packet Schema

```json
{
  "packet_id": "TRIBUNAL-YYYYMMDD-AGENT-LABEL",
  "timestamp": "ISO-8601",
  "sender_id": "agent-or-system",
  "target": "OPERATIONAL_INBOX | HUB_INBOX | SUPABASE_RUNTIME",
  "priority": "HIGH | STANDARD | LOW",
  "status": "PENDING | ACTIVE | COMPLETE | BLOCKED",
  "lane": "PS | TI | SC | PA | MIXED",
  "authority": "DCS | DCSC | delegated-authority",
  "canonical_source": "repository/path@commit",
  "content_sha256": "hash-or-null",
  "payload": {}
}
```

## 4. Repository Map

The active enterprise repository is:

`sonlyconsulting-ctrl/DCSE-Command-Post`

Repository content is divided by governed paths and branches. A path or branch does not create authority by existence.

- `main`: stable production or promoted state as recorded by D05 and D20.
- `v69`: legacy and reconciliation branch for the v6.9 constitutional library.
- `feature/*`: bounded changes under review.
- `hotfix/*`: urgent bounded remediation.

No agent may assume authority from branch naming alone. The controlling promotion record and integrity hash govern.

## 5. Model Source Routing

| Model | Preferred Source Method | Write Method |
| --- | --- | --- |
| ChatGPT DCS | GitHub connector, uploaded canonical file, or scoped Supabase retrieval | Governed GitHub branch or approved connector action |
| Codex | Repository checkout and scoped task branch | Feature or hotfix branch, tests, commit, PR |
| Claude | GitHub or approved local source set | Governed branch or review packet |
| Gemini | GitHub raw source, approved upload, or scoped runtime retrieval | Review record or approved branch |
| Qwen | Local checkout or approved source package | Bounded local or branch execution |
| NotebookLM | Operator-uploaded promoted source package | No direct repository authority |

All models must verify version, status, lane, promotion state, and hash before treating a source as controlling.

## 6. GitHub Write Protocol

1. Confirm repository and branch.
2. Fetch current state.
3. Confirm the target file and current blob SHA.
4. Stage or update only the named files.
5. Run secret and PS scans.
6. Commit with lane, action, doctrine references, and authority.
7. Record changed files and commit SHA.
8. Create or update the Tribunal receipt.
9. Update Supabase runtime references only after the GitHub commit is known.
10. Verify hashes under D20.

Direct writes to `main` require explicit repository authority. Routine governed work belongs on a feature or hotfix branch unless a controlling workflow authorizes otherwise.

## 7. Conflict Resolution

- Operator versus agent: operator controls.
- Promoted source versus candidate: promoted source controls.
- GitHub artifact versus Supabase runtime row: compare promotion record and hash. A mismatch is `DRIFT` and blocks reliance.
- PS conflict: immediate PS isolation Stop-Gate.
- Secret conflict: stop, redact, rotate when required, and record the incident without reproducing the secret.

## 8. GitHub and Tribunal Concurrency

A GitHub change and its governance receipt are one governed operation. The receipt may be committed with the change set or written immediately after the commit. It must include repository, branch, commit SHA, files changed, exclusions, validation results, and open risks.

## 9. No-Git Exclusions

Never commit live credentials, service-role keys, passwords, private recovery data, MFA data, unrestricted private URLs, raw PS evidence, or files marked quarantine.

## 10. Related Doctrine

- D03: model orchestration and execution authority
- D05: baseline and promotion
- D06: file and storage placement
- D20: source authority and runtime distribution
