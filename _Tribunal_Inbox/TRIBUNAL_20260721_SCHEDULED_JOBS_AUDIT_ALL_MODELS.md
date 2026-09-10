# TRIBUNAL_20260721_SCHEDULED_JOBS_AUDIT_ALL_MODELS

```json
{
  "TRIBUNAL_MESSAGE_ID": "TRIB-20260721-SCHEDULED-JOBS-AUDIT-ALL-MODELS",
  "TIMESTAMP": "2026-07-21T00:00:00-04:00",
  "LANE": "DCSE // Orchestration / File Governance",
  "ORIGINATOR": "Claude CP (Cowork)",
  "STATUS": "ACTION_REQUIRED_CODEX_QWEN_CHATGPT_GEMINI_AG",
  "CLASSIFICATION": "DCSE Internal - cross-model scheduled jobs inventory request",
  "SESSION_SUMMARY": {
    "objective": "Every active model/agent reports all scheduled/automated jobs it runs or is aware of across DCSE: active vs inactive, schedule, purpose, last run, and for Supabase items specifically whether DBA-authority (schema/migration/key rotation/seeding) or non-DBA (read/report/sync).",
    "local_mode": "Local filesystem and Supabase read-only checks only. Non-destructive. No jobs created, modified, enabled, or disabled by the originator.",
    "session_accomplishments": [
      {
        "id": "ACK-001",
        "category": "audit",
        "title": "Claude CP scheduled-jobs findings (verified)",
        "detail": "One active Supabase pg_cron job (settle_all_picks, hourly, project nevgdyfpxdaloacuutal, non-DBA). Two Cowork scheduled skills found disabled (tsl-weekly-ledger-integrity last ran 2026-06-15, tsl-kpi-health-monitor last ran 2026-06-18). DCSE-DDNA Supabase project (uutpzaiqymyufljdgdaa) confirmed fully paused/INACTIVE, so no jobs can run there. A vercel.json with two cron routes found in SC_TSL candidate source (20_RECONCILED_PRODUCT_LIBRARY/02_APP_SOURCE_CANDIDATES) but not confirmed deployed on any live Vercel project. No GitHub Actions scheduled workflows found in local repo checkouts."
      },
      {
        "id": "ACK-002",
        "category": "coordination",
        "title": "pm_model_handoffs rows inserted",
        "detail": "5 rows inserted into public.pm_model_handoffs (project nevgdyfpxdaloacuutal), one per target model (Codex, Qwen, ChatGPT, Gemini, AG), handoff_type=audit_request, status=pending, each referencing this Tribunal packet and the companion .md file (TRIBUNAL_INSTRUCTION_20260721_SCHEDULED_JOBS_AUDIT_ALL_MODELS.md) in this same inbox."
      }
    ],
    "mandatory_reporting": {
      "files_read": [
        "C:\\DS All Things\\DCSE_Command_Center\\DCSE_CP_Project (partial, node_modules/.next/.git excluded)",
        "Supabase project nevgdyfpxdaloacuutal (public schema, cron.job)",
        "Supabase project uutpzaiqymyufljdgdaa (project status only, connection timed out on cron.job -- project paused)"
      ],
      "files_created": [
        "C:\\DS All Things\\DCSE_Command_Center\\_Tribunal_Inbox\\TRIBUNAL_INSTRUCTION_20260721_SCHEDULED_JOBS_AUDIT_ALL_MODELS.md",
        "C:\\DS All Things\\DCSE_Command_Center\\_Tribunal_Inbox\\TRIBUNAL_20260721_SCHEDULED_JOBS_AUDIT_ALL_MODELS.json",
        "C:\\DS All Things\\DCSE_Command_Center\\DCSE_CP_Project\\Command Post\\docs\\FS_Admin\\SCHEDULED_JOBS_AUDIT_TASK_PACKET_20260721.md"
      ],
      "files_edited": [],
      "files_skipped": [],
      "restrictions_followed": [
        "Local filesystem and Supabase read-only inspection only",
        "Non-destructive by default -- no jobs created, altered, enabled, or disabled",
        "No GitHub write performed -- local dcse-command-post clone has pre-existing uncommitted changes not made this session, flagged separately rather than committed over"
      ],
      "pending_dcs_response_items": [
        "Confirm whether dcse-command-post repo's uncommitted state (staged rename + unstaged v6.9 deletions, 7 commits behind origin/v69) is safe to touch"
      ],
      "next_recommended_action": "Codex, Qwen, ChatGPT, Gemini, and AG each read their pm_model_handoffs row (to_model = own name, status = pending) and this packet, then respond in the companion .md file and mark their handoff row completed.",
      "json_updated_and_validated": true
    }
  },
  "INSTRUCTIONS_TO_AGENTS": [
    "Treat this JSON as an active cross-model data request, not ratification of any architecture change.",
    "Report format: name/id, system, schedule, active/inactive, last run, DBA vs non-DBA for Supabase items, and explicitly flag anything stale/duplicate/superseded.",
    "Append your findings to TRIBUNAL_INSTRUCTION_20260721_SCHEDULED_JOBS_AUDIT_ALL_MODELS.md under your own model section.",
    "Update your own pm_model_handoffs row to status='completed', completed_at=now() once done."
  ],
  "RESPONSE_SLOTS": {
    "Codex": "PENDING",
    "Qwen": "PENDING",
    "ChatGPT": "PENDING",
    "Gemini": "PENDING",
    "AG": "PENDING",
    "DCS": "PENDING_REVIEW"
  },
  "NEXT_REQUESTED_ACTION": "Each named model reports its scheduled jobs; DCS reconciles once all sections are filled in.",
  "REVIEW_GATES": [
    "No job may be created, disabled, or modified as a side effect of this audit -- report only."
  ]
}
```
