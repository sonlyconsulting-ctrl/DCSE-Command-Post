> **v7.2 platform normalization:** This is the platform-scoped canonical placement of the already Level 0-approved Supabase Schema, RLS, Privacy, and Agent Access Doctrine. D15 remains the controlling numbered database-administration doctrine. D22 remains controlling for persistence/source reconciliation. The prior root-level file remains a compatibility reference until all routes are reconciled.

# DCSE Supabase Schema, RLS, Privacy, and Agent Access Doctrine v1

**Status:** OPERATIVE — DCS Level Zero approved 2026-09-15  
**Controlling entity:** DCSE Database Security Control (DSC)  
**Authority:** DCS / CTO; administered by the designated database owner  
**Applies to:** developers, agents, migrations, SQL Editor changes, Edge Functions, server runtimes, Vercel/Netlify functions, local workers, REST, GraphQL, Realtime, Storage, and direct Postgres connections.

## 1. Purpose and precedence

DSC prevents accidental exposure, policy drift, cross-lane access, secret leakage, and unreviewed privileged execution. It supplements existing v7.2 governance and the Universal Agent Onboarding standard. Where requirements conflict, the stricter privacy/security control applies and the conflict enters Tribunal review. It does not authorize access by itself.

## 2. Mandatory object classification

Every table, view, function, sequence, bucket, and schema must declare one class in its migration header:

| Class | Intended access | Required boundary |
|---|---|---|
| `INTERNAL_SERVER_ONLY` | service/backend only | non-exposed schema; no client grants; RLS defense in depth |
| `USER_OWNED` | authenticated principal's rows | RLS with `auth.uid()` ownership; explicit grants |
| `TENANT_SCOPED` | organization/lane rows | RLS with immutable tenant membership; indexed tenant key |
| `PUBLIC_READ` | deliberate anonymous read | select-only grant and narrow select policy; no public writes |
| `PRIVILEGED_RPC` | controlled operation | narrow API wrapper; explicit EXECUTE; identity/authorization in function |
| `PLATFORM_MANAGED` | Supabase-owned schema/object | do not alter unless official procedure requires it |

Unclassified objects fail review. `RLS enabled, no policy` is acceptable only for documented `INTERNAL_SERVER_ONLY` objects with no client grants.

## 3. Schema architecture

- `public` and any configured Data API schema are treated as exposed.
- Internal orchestration, worker queues, provider configuration, secrets, audit, and governance storage remain in non-exposed schemas.
- API schemas contain only intentional tables/views/RPC wrappers.
- Views exposed to clients use `security_invoker = true` on PostgreSQL 15+ or are inaccessible to client roles.
- Data API settings are recorded in the environment inventory and compared during release review.

## 4. Atomic migration rule

The same migration must contain: classification header, object creation/change, owner, RLS decision, policies, grants/revokes, required indexes, comments, verification query, and rollback notes. Dashboard/SQL Editor hotfixes require immediate capture as a repository migration and evidence receipt.

Defaults:

1. Revoke object access from `PUBLIC`, `anon`, and `authenticated`.
2. Enable RLS on every application table; force RLS when owner bypass is not required and has been tested.
3. Grant only the verbs required by the classified consumer.
4. Do not grant client-facing default privileges. Any exception requires DCS approval, schema scope, named owner, expiry, and regression tests.
5. Do not create permissive policies merely to clear an advisor finding.

## 5. RLS construction rules

- Use `(select auth.uid())`, `(select auth.jwt())`, or another stable request expression when the result is invariant within the statement.
- Never use `raw_user_meta_data`/`user_metadata` for authorization. Approved authorization claims reside in app metadata or canonical membership tables.
- `TO authenticated` proves only the database role; it is not row authorization. Add ownership, membership, lane, privacy, and lifecycle predicates.
- UPDATE requires both SELECT access and matching `USING` plus `WITH CHECK` predicates.
- Index ownership, tenant, membership, foreign-key, and policy-filter columns based on measured query plans.
- Keep policies simple and testable. A complex helper may be used only after invoker-first design is rejected with evidence.
- Explicit application filters improve planning and reduce accidental broad reads, but never replace RLS.

## 6. Function and RPC rules

- Prefer `SECURITY INVOKER`.
- `SECURITY DEFINER` is an exception, never a permission-error shortcut.
- A definer must use a trusted fixed search path (prefer `pg_catalog` or empty with fully-qualified objects), have an explicit owner, validate identity and authorization, and immediately revoke EXECUTE from `PUBLIC`, `anon`, and `authenticated` before any narrow re-grant.
- Caller-supplied `user_id`, `agent_id`, tenant, lane, or role is input, not identity proof. Bind identity to verified JWT claims or use a trusted server-side service channel.
- Trigger/event-trigger functions are not API endpoints and must not retain client EXECUTE.
- RLS does not constrain a definer running as a bypass role; the function body is the security boundary.

## 7. Agent communication patterns

| Scenario | Required pattern |
|---|---|
| Interactive agent acting for a user | forward validated user JWT; RLS applies; never use service key in browser/model context |
| Background/local worker | server-side service credential or dedicated non-bypass database role; secret outside prompts/logs; explicit lane/task validation |
| Cross-tenant administrative task | controlled backend command with approval receipt, audit event, bounded parameters, and service identity |
| Public experience | publishable key, minimal grants, public-read policy only where approved |

Service-role credentials bypass RLS. They stay server-side in managed secrets/DPAPI/vault, never in `NEXT_PUBLIC_*`, source, prompts, evidence payloads, or browser code. Rotate on suspected exposure.

## 8. Privacy and lane controls

- Apply data minimization and classify fields as public, internal, confidential, secret, or protected.
- Protected lane data cannot cross schemas, logs, embeddings, exports, or model contexts without specific authority.
- Audit records store identifiers and outcomes, not secrets or unnecessary payloads.
- Realtime publication, Storage policies, database webhooks, replicas, backups, and vector/RAG ingestion are reviewed as independent disclosure paths.
- Retention, deletion, export, and legal-hold requirements are defined before production ingestion.

## 9. Controlled lifecycle

1. **Intent:** Task ID, owner, consumer, classification, privacy, expected volume, and rollback.
2. **Design:** threat model, schema/API boundary, role matrix, query/index plan, alternatives.
3. **Migration:** atomic DDL with least privilege and deterministic names.
4. **Static gate:** changed-migration anti-drift validator.
5. **Isolated proof:** local/branch migration, pgTAP role tests, advisor run, application/worker round trip.
6. **PR review:** database/security reviewer; no self-approval for privileged changes.
7. **Promotion:** explicit environment authority, backup/rollback confirmation, migration apply.
8. **Closeout:** live privilege queries, negative access proof, advisors, logs, evidence and handoff IDs.

## 10. Required role matrix

Test `anon`, unrelated authenticated principal, correct principal, service role/dedicated worker role, and owner. Assert both allow and deny outcomes for SELECT/INSERT/UPDATE/DELETE/EXECUTE. A success-only test is incomplete. Mutation tests use rollback or disposable data.

## 11. Automated stop gates

CI blocks new/changed migrations containing: client-facing default grants; broad client grants; exposed tables without RLS; client-executable definers without an approved marker and controls; mutable definer search paths; unsafe metadata authorization; deprecated `auth.role()`; exposed non-invoker views; or missing classification headers. Dynamic tests and Supabase advisors remain required because static scanning cannot prove effective privileges.

## 12. Exceptions

An exception records rule, object, reason, alternatives, risk owner, compensating controls, expiry, and removal task. Exceptions cannot expose service keys, protected material, or anonymous privileged mutation.

## 13. Definition of done

- Repository migration matches live history.
- Intended consumers work; unauthorized roles fail.
- No new unaccepted security advisor warnings.
- Effective privileges, RLS/policies, function configuration, Data API schemas, and secret placement are evidenced.
- Rollback is documented and tested where practicable.
- Handoff identifies remaining performance or product gates separately from security closure.

## References

- https://supabase.com/docs/guides/api/securing-your-api
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/database/postgres/roles
- https://supabase.com/docs/guides/security/product-security


## 14. Mandatory review/verify controls

The following are required evidence gates, not optional cleanup:

1. A local/background worker change requires one controlled service-role claim, heartbeat, result, and release/close cycle plus anonymous and unrelated-authenticated denial proof.
2. Every client-executable SECURITY DEFINER must be classified and reviewed before promotion.
3. Authentication hardening settings require user-flow impact review before activation.
4. Each release records the authoritative Data API enabled state, exposed schemas, extra search path, intended consumers, and effective grants.
5. Database doctrine changes remain CANDIDATE until reconciled with operative governance and expressly designated.
6. A production database change is incomplete until the repository migration and live history match.
7. A RAG implementation begins with a verified schema/vector/provider/provenance/privacy/retrieval/retention baseline before ingestion.

Review-only authority never implies permission to remediate, merge, deploy, promote, rotate credentials, modify configuration, or ingest production data.


## Level Zero approval record

DCS Level Zero approved this control as part of Topics 1–6 in the Supabase governance and hardening package on 2026-09-15. Ollama runtime verification, the first anti-drift workflow run, and post-merge deployment observation remain mandatory evidence gates and were not waived.
