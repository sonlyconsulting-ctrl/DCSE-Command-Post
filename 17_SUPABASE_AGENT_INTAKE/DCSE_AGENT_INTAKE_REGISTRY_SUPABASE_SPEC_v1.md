# DCSE Agent Intake Registry Supabase Spec v1

Date: 2026-07-08
Lane: SC / TI infrastructure
Status: Draft architecture specification
Purpose: Provide an agent-accessible intake surface for Gemini, Claude Chat, Claude Code, Cowork, and other review agents when GitHub browser access is unreliable.

## 1. Problem

GitHub remains the repository of record, but chat-based agents may fail to read GitHub tree pages or raw file URLs because of tool restrictions, robots controls, search-index delay, or credential boundaries.

The NateBJones website media intake test proved that public GitHub visibility alone does not guarantee agent-readable access in normal chat environments.

## 2. Design Decision

Supabase will serve as the agent-accessible intake registry. GitHub remains the durable repository of record. Supabase provides a controlled public-read layer for non-confidential SC / TI intake records.

## 3. Operating Model

1. Intake record is created in GitHub.
2. Intake record is mirrored into Supabase.
3. Gemini or Claude reads the Supabase public view or endpoint.
4. Agent produces a review.
5. Review is stored in Supabase as pending.
6. Approved review is committed back to GitHub.

## 4. Lane Firewall

SC / TI records may be exposed through public-read views when approved for external-agent review.

PS records must not be exposed through the public-read layer. PS material requires private storage, authenticated access, and separate review controls.

## 5. Core Tables

### agent_intake_items

Stores source intake records.

Recommended fields:

- id uuid primary key
- lane text not null
- title text not null
- source_type text not null
- source_url text
- source_id text
- github_path text
- github_commit text
- summary text
- status text not null default 'queued'
- review_required boolean not null default true
- promotion_gate text not null default 'review_required_before_public_use'
- public_read boolean not null default false
- created_by text
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

### agent_reviews

Stores agent review outputs.

Recommended fields:

- id uuid primary key
- intake_id uuid references agent_intake_items(id)
- agent_name text not null
- review_status text not null default 'draft'
- title_verification text
- source_metadata jsonb
- transcript_need text
- website_strategy_relevance text
- accessibility_ux_lessons text
- risks text
- recommendation text
- full_review text
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

### agent_task_queue

Stores agent-readable task instructions.

Recommended fields:

- id uuid primary key
- task_name text not null
- target_intake_id uuid references agent_intake_items(id)
- assigned_agent text
- instructions text not null
- status text not null default 'queued'
- due_status text
- public_read boolean not null default false
- created_at timestamptz not null default now()
- updated_at timestamptz not null default now()

## 6. Public Read View

Create a view named public_agent_intake_view that exposes only records where public_read is true and lane is not PS.

The view should include only fields needed by external agents. It should not expose service metadata, private notes, or secrets.

## 7. Security Controls

- Enable RLS on all base tables.
- Allow public select only through a safe view or narrow policy.
- Allow inserts and updates only through authenticated service-role workflows or admin UI.
- Never store secrets, tokens, private credentials, or PS work product in public-read fields.
- Keep source URLs public-only for SC / TI records.

## 8. Agent Query Pattern

Agents should receive a Supabase public endpoint or view URL and a task id. The agent should not need GitHub browsing to locate the active intake item.

Example instruction:

Read task id `TASK-20260708-NATEBJONES` from the public agent intake registry. Complete the review using the intake record and return the structured review output.

## 9. Promotion Gate

Supabase is an intake and review surface, not final authority. GitHub remains the repository of record. Public website copy, campaign copy, doctrine updates, or product changes require a separate promotion decision.

## 10. Immediate Build Sequence

1. Create SQL migration for the three tables and public view.
2. Add RLS policies.
3. Insert one test record for the NateBJones website media intake.
4. Test Gemini and Claude Chat against the public Supabase endpoint.
5. Confirm that agent review can be returned without pasting the video link into chat.
6. Commit approved reviews back to GitHub.

## 11. Success Criteria

- Agent can discover active intake without GitHub browsing.
- Agent can read source metadata from Supabase.
- Agent does not ask for the source link when the registry record exists.
- PS material is excluded from public view.
- GitHub remains the final archive of approved records.
