# TRIBUNAL ACTIVITY RECORD - DCSE CP / Asset Portal / PM Command Post / P3-P5

**Date:** 2026-06-30  
**Prepared by:** Codex  
**Authority:** DCS/DCSE  
**Required Tribunal Folder:** `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`  
**Status:** Filed to Tribunal Inbox  
**Secret Values Included:** No  

## 1. Purpose

This Tribunal activity record captures the relevant operational activity from the DCSE Command Post / Asset Portal / PM Command Post workstream, including corrected architecture, deployment phases, key failures, remediation steps, governance doctrine changes, asset insertions, automation setup, and folder-path correction for Tribunal activity.

This record is intended as a Tribunal Inbox activity artifact, not as a database mutation or production deployment artifact.

## 2. Folder Rule Correction

DCS/DCSE clarified that all Tribunal activity must be saved only to:

`C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`

Prior local workspace folders, Command Post audit folders, OneDrive folders, and other repo-local folders are not valid Tribunal activity destinations unless DCS/DCSE explicitly changes the rule.

## 3. Workspace / Source-of-Truth Corrections

### Canonical Command Post project root

`C:\DS All Things\DCSE_CP_Project`

### Canonical deployed app root

`C:\DS All Things\DCSE_CP_Project\DCSE_ASSET_PORTAL_APP\apps\web`

### Correct production URLs

| Purpose | URL |
|---|---|
| Permanent app domain | `https://cp.sonlyconsulting.com` |
| DCSE Asset Portal | `https://cp.sonlyconsulting.com/cp` |
| PM Command Post | `https://cp.sonlyconsulting.com/pm` |
| DDNA ingest API | `https://cp.sonlyconsulting.com/api/ddna-ingest` |
| Wix Asset Portal destination | `https://www.sonlyconsulting.com/dcse-cp` |
| Wix PM Tasks destination | `https://www.sonlyconsulting.com/dcse-tasks` |

## 4. Module Semantics Confirmed

| Route | Correct Meaning | Incorrect Meaning Avoided |
|---|---|---|
| `/cp` | DCSE Asset Portal / asset registry module | Main Command Post |
| `/pm` | PM Command Post / Project Manager control module | Asset Portal |
| `/pm/staging-review` | Planned PM submodule for staged-record review | Promotion engine |

## 5. P3 Summary - DDNA Backend Mediation

P3 objective: migrate DDNA extraction from local-only JSON output toward mediated Supabase persistence.

### Confirmed architecture

Python extractor using standard library only:

`dcse_ddna_extraction_v01.py -> Next.js /api/ddna-ingest -> Supabase public.dcse_plan_inbox`

### P3 controls

- No `supabase-py` dependency.
- No direct Python-to-Supabase write path.
- Service key remains server runtime only.
- Local JSON fallback remains available.
- PS firewall blocks Critical/PS payloads.
- API tests validated 405/400/403/200 behavior.

### P3 result

- P3 code path validated.
- Production mediated API later verified.
- Wrap-up and extraction plan inserted as governed asset after DCS/DCSE approval.

## 6. P4 Summary - Permanent Vercel Deployment

### Project

Vercel project: `dcse-asset-portal`

### Initial deployment issue

The deployed root page initially showed the old Bracket King template. This was not the correct app experience.

### Corrective actions

- Removed old Bracket King root page.
- Root `/` now resolves to `/cp`.
- Removed stale `@bracket-king` dependencies/config references.
- Rebuilt and redeployed corrected app.
- Verified no Bracket King content at production domain.

### P4 credential incident

A Supabase service-role value was exposed in an AG command transcript. It was treated as compromised.

### Credential remediation

- New named Supabase secret key created.
- Vercel `SUPABASE_SERVICE_ROLE_KEY` rotated to new value.
- Production redeployed.
- Old keys deleted.
- Production POST retested successfully with HTTP 200.
- Secret values are not included in this record.

## 7. P5 Summary - Domain and Wix Access

### Domain

`cp.sonlyconsulting.com` is mapped to the corrected Vercel deployment.

### Verified routes

- `/` resolves to `/cp` with DCSE content.
- `/cp` returns 200.
- `/pm` returns 200.
- `GET /api/ddna-ingest` returns 405.
- malformed POST returns 400.
- PS/Critical POST returns 403.
- valid mediated POST returns 200.

### DNS clarification

No separate DNS record is required for `/pm`. DNS maps the `cp` hostname; Next.js handles `/cp`, `/pm`, and `/api/*` routes.

### Wix pages

- `https://www.sonlyconsulting.com/dcse-cp` maps user access to Asset Portal.
- `https://www.sonlyconsulting.com/dcse-tasks` maps user access to PM Command Post.

## 8. Staging Review Module Asset

DCS/DCSE approved creation of the PM-owned Staging Review Module asset.

### Asset

`DCSE-PM-STAGING-REVIEW-MODULE-20260523`

### Purpose

A PM Command Post submodule that reads staged records from `public.dcse_plan_inbox`, displays what was inserted, and captures DCS commentary and review decisions in a separate `public.dcse_plan_reviews` table.

### Doctrine

- Staging is not approval.
- Original staged payload remains intact.
- DCS commentary is written separately.
- Module does not promote records directly.
- DCS retains final approval authority.

### Artifact handling status

Current artifact handling is partial. Lean registry payloads with file references are supported. High-volume artifact support needs a dedicated artifact table/storage/linking layer before heavy use.

## 9. Wrap-Up / Extraction Asset

DCS/DCSE approved insertion of the DCSE Asset Wrap-Up and Extraction Plan.

### Asset

`DCSE-ASSET-WRAPUP-EXTRACTION-PLAN-20260523`

### Insert method

Production mediated API `/api/ddna-ingest`

### Insert result

HTTP 200 verified. Full Markdown was retained by file reference rather than stuffed into a large payload after an oversized payload attempt timed out.

## 10. DDNA vs Knowledge Base Lanes

### DDNA extraction

Purpose: convert source material into signals, candidate assets, process records, and operational learnings.

### Knowledge Base acquisition

Purpose: preserve approved rules, standards, doctrine, context, and model-readable references.

### Rule

Overlap is allowed only as candidate material until DCS/DCSE approves promotion or database insertion.

## 11. New/Updated Governance Rules and Lessons Learned

| Area | Lesson / Rule |
|---|---|
| Known-working path | Always identify and preserve the actual working module before redesign or schema work. |
| Scope drift | Draft apps and production apps must not be conflated. |
| Cloudflare | Quick tunnels are temporary previews only; never Wix/production targets. |
| Vercel | Use governed project names, not generic `web`. |
| Supabase | GRANT, Data API exposure, and RLS must be verified separately. |
| Secrets | Never echo or paste secret values in commands/transcripts. Exposure triggers rotation. |
| Root route | Production root must identify/redirect to the intended DCSE module. |
| Artifacts | Use lean registry records plus artifact references; avoid large Markdown payloads in registry rows. |
| Agent roles | Codex drives architecture/code/spec/verification; AG handles credential/account execution; DCS approves authority changes. |
| Tribunal activity | All Tribunal activity must be filed only in the Tribunal Inbox folder. |

## 12. Automation and Model Awareness

A daily frontier-model awareness automation was created:

`daily-frontier-model-awareness`

Purpose: monitor actionable changes in OpenAI/Codex, Claude, Gemini, Vercel, Supabase, Wix, plugins, MCP, deprecations, and governance impacts.

Noted items across heartbeats included:

- Avoid tying workflows to retiring models.
- Use budgeted Vercel AI Gateway keys for recurring automations.
- Add Vercel AI/account action attribution to traces.
- Verify Supabase Postgres/Data API/GRANT/RLS posture.
- Treat Supabase ChatGPT app as inspection-only until SQL execution policy is approved.
- Treat Gemini/Computer Use as UI testing candidate, not credential executor.
- Keep Claude in review/spec/risk lane unless explicitly connected as executor.

## 13. Pending Build List / Governance Items

DCS/DCSE added the following pending governance items:

| Item | Classification |
|---|---|
| Default-deny technical baseline / Article 13 | CRITICAL |
| No-log-deletion adapter clause | CRITICAL |
| Instruction-layer limitation disclosure | OTHER |
| Per-agent network reach specification | RESEARCH NEEDED |
| Prompt-injection vector via Tribunal Inbox | RESEARCH NEEDED |

These are pending review and approval, not ratified doctrine.

## 14. Required Follow-Up

1. Use `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox` for Tribunal activity only.
2. If this record needs database insertion, request separate DCS/DCSE approval.
3. Do not place Tribunal activity in Command Post audit folders or local workspace folders.
4. Continue P6 hardening/monitoring work as a separate governed track.
5. Define artifact-volume architecture before heavy multi-artifact module use.

## 15. Safety Notes

- No secret values are included.
- No PS/TI restricted details are included.
- This record summarizes operational activity and governance corrections.
- This record does not authorize schema changes, promotions, deletions, or database mutations.
