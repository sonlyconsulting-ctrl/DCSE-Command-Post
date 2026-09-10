# GoTime PM Backbone — Schema Reconciliation Report

**Status:** Complete. Produced by Claude (Code) as Validator/Red Team under the 2026-07-02 redirect order, Phase A.

## Headline finding — read this before anything else

A PM backbone functionally identical to what AG's plan proposes to build **already exists, live, in the production Supabase database**, applied via raw SQL migrations (`002_lock_governed_core_batch.sql`, `003_add_service_role_policies.ts`). It was never pulled into `schema.prisma`, so it's invisible to anyone reading the Prisma schema file — which is almost certainly why AG proposed rebuilding it.

Live tables not yet represented in Prisma (or only partially, see `pm_artifacts` below): `pm_projects`, `pm_workstreams`, `pm_tasks`, `pm_closeouts`, `pm_decisions`, `pm_blockers`, `pm_risks`, `pm_model_handoffs`, `pm_activity_log`, `cp_lanes`, `cp_entities`.

**This changes the build order.** The primary work now is a `prisma db pull`/reverse-engineering pass to bring these into Prisma with proper typed fields, plus building the handful of genuinely-new pieces — not an 8-model, 5-enum greenfield build.

## Model-by-model verdict

| Proposed Model | Existing Coverage | Verdict | What's Actually Needed |
|---|---|---|---|
| **Project** | `pm_projects` — near-identical field set (project_code, entity_code, primary_lane, classification, status, priority, purpose/scope, dates) | **REUSE** | Pull into Prisma with typed fields (not a JSON blob) |
| **WorkOrder** | `pm_workstreams` — status/priority/objective/exit_criteria | **REUSE** | Pull into Prisma; rename mapping only |
| **Task** | `pm_tasks` — task_code, status, priority, assigned_to, model_role, due_date, stop_gate_flag, validation flags | **REUSE** | Pull into Prisma with full typed fields |
| **Milestone** | *(nothing)* — no dedicated milestone entity exists anywhere | **GENUINELY NEW** | New `pm_milestones` table, following the exact column/FK/RLS conventions of the sibling `pm_*` tables |
| **Deliverable** | `pm_artifacts` (build-output tracking) partially covers it; doesn't have acceptance/sign-off semantics | **EXTEND** `pm_artifacts` | Add `deliverable_flag`, `acceptance_status`, `accepted_at`, `accepted_by` |
| **AgentAssignment** | `pm_model_handoffs` — from_model/to_model, handoff_type, status, validation_required | **REUSE** | Pull into Prisma; rename mapping only |
| **Blocker** | `pm_blockers` — exact match, including unblock_condition | **REUSE** | Pull into Prisma; rename mapping only |
| **TribunalReceipt** | No live table, but a well-established file-based convention (`tribunal_receipts/*.json`) plus `AuditLog` as the closest DB analog | **GENUINELY NEW**, model as an `AuditLog` specialization | New table or `AuditLog` entries with `actionName = 'TRIBUNAL_RECEIPT'` carrying the existing JSON receipt shape as the JSONB payload |

## Enum-by-enum verdict

| Proposed Enum | Existing Coverage | Verdict |
|---|---|---|
| **DcseLane** | `cp_lanes` — live lookup table with seeded values (PS, SC, SC_PRODUCT_ARCHITECTURE, TI, SS, TRAINING, PA_PERSONAL_ADMIN, ARCHIVE, OTHER_REVIEW, MIXED_REVIEW, SECRET_RISK, FEDERATED_COMMAND_INDEX) | **REUSE — do not create a competing enum.** A lookup table also carries metadata (`restricted boolean`, `description`) a bare enum can't. Converting to an enum would require repointing FKs across 10+ tables for no real benefit. |
| **DcseClassification** | `DcseConfidentiality` (LOW/MEDIUM/HIGH/RESTRICTED) already exists as a typed enum on `RegistryRecord`; `pm_projects.classification` is free text defaulting to `'CONFIDENTIAL'` | **REUSE `DcseConfidentiality`.** If GoTime needs a `CONFIDENTIAL` value, add it to that enum rather than create a 5th overlapping one. |
| **DcseWorkStatus** | No typed enum exists, but a documented text vocabulary is already live in `pm_tasks.status`: `not_started, ready, in_progress, blocked, validation, revision_required, done, closed, cancelled` | **GENUINELY NEW, but codify the existing vocabulary exactly** — don't invent new values, or existing rows need remapping |
| **DcseAgentRole** | No typed enum; documented role vocabulary already in use in `pm_tasks.model_role` / `pm_model_handoffs.from_model`/`to_model`: DCS governance, ChatGPT DCS architect, Codex builder, Anti-Gravity executor, Opus 4.7 validator, Gemini challenge, Claude drafting/review | **GENUINELY NEW, codify from existing list.** Converting the existing free-text columns to this enum requires a value-mapping/backfill on tables that already have production rows — not a pure additive change. |
| **DcseGateType** | Only untyped booleans exist today (`pm_tasks.stop_gate_flag`, `validation_required`, `opus_validation_required`) | **GENUINELY NEW.** Real opportunity to collapse three booleans into one typed field or a normalized gate-join table instead of adding a fourth boolean later. |

## Summary

- **6 of 8 proposed models** map almost 1:1 onto tables already live in production.
- **2 of 5 proposed enums** (`DcseLane`, `DcseClassification`) should reuse existing structures outright.
- **1 model extends** an existing table (`Deliverable` → `pm_artifacts`).
- **Genuinely new work**: `Milestone` table, `TribunalReceipt` (as an `AuditLog` specialization), and 3 enums (`DcseWorkStatus`, `DcseAgentRole`, `DcseGateType`) — all should codify vocabulary that's already in documented/informal use, not invent fresh taxonomies.

## Schema-wide note relevant to any new work

Across the entire existing schema, there are **zero** Prisma `@relation` declarations — every FK-like reference is a bare UUID column, joined manually at the query level. Any new or pulled-in GoTime tables should decide deliberately whether to introduce real `@relation` pairs (better DX, `include`/nested writes) or match the existing flat-FK convention (consistency with everything else). Recommend real relations for new work — the flat-FK pattern looks more like schema drift than a deliberate choice.
