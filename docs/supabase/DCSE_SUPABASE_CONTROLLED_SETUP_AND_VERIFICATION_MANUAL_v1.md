# DCSE Supabase Controlled Setup and Verification Manual v1

**Status:** OPERATIVE — DCS Level Zero approved 2026-09-15
**Controlling entity:** DCSE Database Security Control (DSC)
**Task source:** DCSE-SUPABASE-REVIEW-VERIFY-20260915-002
**Applies to:** new Supabase projects, schemas, tables, views, functions, RLS, agents, local workers, and RAG stores.

## 1. Preflight

Record Task ID, lane/entity, environment, project reference, owner, consumer, data/privacy class, object classification, Data API need, Realtime/Storage/RAG involvement, rollback, and approval boundary. Verify GitHub main, both applicable Supabase projects, and one safe read. Never record a secret.

## 2. Project setup

1. Record whether the Data API is enabled.
2. Record exposed and extra-search-path schemas.
3. Prefer a dedicated API schema. Keep internal worker, provider, secret, audit, governance, and protected-lane storage outside the API surface.
4. Revoke client-facing default privileges unless a reviewed exception requires them.
5. Define server secret placement and rotation ownership.
6. Enable leaked-password protection only after reviewing active signup/reset/support flows.
7. Record backup, retention, deletion, replication, webhook, Storage, and Realtime boundaries.

## 3. Object setup

Every migration declares one classification: INTERNAL_SERVER_ONLY, USER_OWNED, TENANT_SCOPED, PUBLIC_READ, PRIVILEGED_RPC, or PLATFORM_MANAGED.

In one migration:

- create or alter the object;
- set explicit ownership;
- enable RLS for application tables;
- revoke PUBLIC/anon/authenticated by default;
- create only required policies and grants;
- use security-invoker views;
- index measured ownership, tenant, membership, foreign-key, and policy filters;
- harden exceptional definers;
- include verification queries and rollback notes.

An internal table may deliberately have RLS with no policy when all client grants are absent.

## 4. Required review and verification

Before promotion:

1. Verify one intended consumer round trip.
2. Verify anon and unrelated-authenticated denial.
3. Review every new/changed SECURITY DEFINER.
4. Verify Data API exposed schemas and effective privileges.
5. Run static anti-drift validation, local/branch tests where available, and Supabase advisors.
6. Compare repository migrations with live migration history.
7. For RAG, verify ingestion authority, provenance, lane/privacy boundary, retrieval authorization, embedding provider/model, retention/deletion, and vector/index design.

## 5. Evidence packet

Return Verified/Likely/Unknown for:

- project and environment;
- exposed schemas;
- table RLS and policies;
- schema/table/sequence/function grants;
- function owner, security mode, search path, and identity binding;
- Realtime, Storage, webhooks, RAG/vector disclosure paths;
- intended and denied role tests;
- consumer round trip;
- advisor before/after;
- repository/live parity;
- rollback readiness.

## 6. Stop gates

Stop and escalate on unknown consumer credentials, service keys in model/browser context, caller-supplied identity used as proof, anonymous privileged mutation, unclassified objects, missing RLS on a granted table, client-facing default privileges, exposed non-invoker views, protected-lane crossover, unreviewed destructive DDL, or repository/live drift.

## 7. Exit

Setup is complete only when the intended consumer succeeds, denied roles fail, advisors introduce no unaccepted security finding, GitHub matches live history, and the evidence packet and Handoff ID are recorded.


## Level Zero approval record

DCS Level Zero approved this control as part of Topics 1–6 in the Supabase governance and hardening package on 2026-09-15. Ollama runtime verification, the first anti-drift workflow run, and post-merge deployment observation remain mandatory evidence gates and were not waived.
