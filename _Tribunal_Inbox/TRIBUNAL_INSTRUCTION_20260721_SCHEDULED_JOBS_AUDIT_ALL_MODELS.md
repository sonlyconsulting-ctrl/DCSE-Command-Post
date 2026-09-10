# Scheduled Jobs Audit — All Models Instruction

Status: ACTION_REQUIRED_CODEX_QWEN_CHATGPT_GEMINI_AG
Boundary: Claude CP (Cowork) performed a read-only Supabase/local-filesystem check only. No jobs were created, modified, enabled, or disabled by Claude CP. No GitHub operations performed by Claude CP.

## Why

DCS requested a cross-model inventory of every scheduled/automated job active across DCSE, including which touch Supabase under DBA authority versus which do not. Claude CP cannot query Codex, Qwen, ChatGPT, or Gemini directly — this file plus the corresponding `pm_model_handoffs` rows (from_model=Claude CP, handoff_type=audit_request, to_model=<you>, status=pending) are the routing mechanism.

## Operating Flow

1. Claude CP recorded its own verified findings below and logged one `pm_model_handoffs` row per model in Supabase project `nevgdyfpxdaloacuutal`.
2. Each named model reads its own row (`select * from public.pm_model_handoffs where to_model = '<your name>' and status = 'pending'`), performs the audit, and appends its findings to this file under its own section.
3. Each model updates its own `pm_model_handoffs` row: `status = 'completed'`, `completed_at = now()` once its section below is filled in.
4. Claude CP or DCS reconciles all sections once populated.

## Required Report Format (same for every model)

For every scheduled or automated job you run or are aware of:
- Name/id, system (Supabase pg_cron, Vercel cron, GitHub Actions, OS-level scheduler, internal agent loop, etc.)
- Schedule (cron expression or plain English)
- What it does
- Active or inactive/disabled
- Last run, if known
- Supabase items only: DBA-authority (schema mutation, migration, key rotation, seeding) or non-DBA (read/report/sync)
- Flag anything you believe is stale, duplicate, or superseded — do not stay silent on it

## Claude CP / Cowork — COMPLETED 2026-07-21

| Job | System | Schedule | Active | Last run | DBA / non-DBA |
|---|---|---|---|---|---|
| `settle_all_picks()` | Supabase pg_cron, project `nevgdyfpxdaloacuutal` | `0 * * * *` (hourly) | Active | not queried | non-DBA (data settlement) |
| `tsl-weekly-ledger-integrity` | Cowork scheduled skill, `DCSE_Command_Center\Scheduled\` | Manual only | Inactive/disabled | 2026-06-15 | non-DBA |
| `tsl-kpi-health-monitor` | Cowork scheduled skill, `DCSE_Command_Center\Scheduled\` | Manual only | Inactive/disabled | 2026-06-18 | non-DBA |
| pg_cron on DCSE-DDNA (`uutpzaiqymyufljdgdaa`) | Supabase | n/a | Cannot run — project itself is paused (status INACTIVE) | n/a | n/a |
| `/api/cron/sync-schedule` (*/15 min), `/api/cron/sync-live` (every min) | Vercel cron, found in `SC_TSL\20_RECONCILED_PRODUCT_LIBRARY\02_APP_SOURCE_CANDIDATES\vercel.json` | As listed | **Unconfirmed** — candidate source, not verified as deployed on any live Vercel project checked | n/a | n/a |
| GitHub Actions scheduled workflows | Local repo checkouts under DCSE_CP_Project | n/a | None found | n/a | n/a |

Full detail: `Command Post\docs\FS_Admin\SCHEDULED_JOBS_AUDIT_TASK_PACKET_20260721.md`

## Codex

Status: PENDING

## Qwen

Status: PENDING — standing audit/CCO mandate, please prioritize

## ChatGPT

Status: PENDING

## Gemini

Status: PENDING

## AG / Antigravity

Status: PENDING — most likely holder of DBA-authority scheduled items (migrations, key rotation, seeding jobs)

## Proof Required From Each Model

- Report appended under its own section above
- `pm_model_handoffs` row updated to `status = 'completed'`
- Any stale/duplicate/superseded job explicitly flagged, not silently omitted
