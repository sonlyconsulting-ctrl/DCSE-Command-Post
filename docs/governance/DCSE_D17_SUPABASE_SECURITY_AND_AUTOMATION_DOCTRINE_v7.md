# DCSE D17 Supabase Security and Automation Doctrine v7

Status: DCSE AUTHORIZED OPERATIONAL DOCTRINE
Effective: 2026-07-29
Authority: DCS Enterprise v7 Governance
Applies to: SC-Command-Post, DCSE-DDNA, all future DCSE Supabase projects, schemas, tables, views, functions, storage objects, queues, cron jobs, and worker communications

## 1. Purpose

This doctrine makes security part of implementation, not a repair step. No Supabase object is complete until its access model, RLS posture, grants, function execution rights, negative tests, advisor results, rollback, and receipt are complete.

Structure precedes scale. A working object that fails the security gate is incomplete and cannot be promoted.

## 2. DBA operating authority

AG is not the primary DBA. Database duties are distributed across Code and Codex under CTO governance. Either may prepare, review, execute, and verify bounded database work when operating within an approved task and migration scope.

No model receives unrestricted mutation, promotion, or deployment authority. Production mutations must be migration-controlled, attributable, reversible, and verified.

## 3. Proper implementation pattern

Every database change must follow this order:

1. Define the object owner, callers, lane, data classification, and mutation class.
2. Define the access matrix before writing DDL.
3. Create the object and its primary key, constraints, indexes, and comments.
4. Enable RLS in the same migration for every table in an exposed schema.
5. Revoke default and unnecessary privileges from PUBLIC, anon, and authenticated.
6. Add only the minimum grants and policies required by the access matrix.
7. Restrict every privileged function with a fixed search_path and explicit EXECUTE grants.
8. Run positive and negative authorization tests.
9. Run Supabase security and performance advisors.
10. Verify rollback, idempotency, migration ordering, and schema drift.
11. Produce a receipt containing migration hash, test results, advisor delta, and promotion result.
12. Promote automatically when all mandatory gates pass and no Stop-Gate condition exists.

Post-build security patching is prohibited as the normal workflow. A remediation migration is permitted only for inherited debt, emergency correction, or a defect that escaped an enforced gate.

## 4. Table security standard

Every new table in public or another exposed schema must, in the same migration:

- Enable RLS.
- Revoke all from PUBLIC, anon, and authenticated unless access is explicitly required.
- Declare whether the table is user-facing, worker-facing, backend-only, append-only, or audit-only.
- Use ownership, membership, lane, or protected app_metadata authorization where row access is required.
- Never rely on TO authenticated alone as authorization.
- Never use user_metadata for authorization.
- Include both USING and WITH CHECK for UPDATE policies.
- Avoid USING true or WITH CHECK true for mutation policies unless an approved, documented public-ingest exception exists.
- Use deny-by-default when no direct user access is required.

Backend-only workflow tables may have RLS enabled with no anon or authenticated policies. Service-role access alone is acceptable when documented and tested.

## 5. Function and RPC security standard

Every SECURITY DEFINER function must:

- Exist only when RLS bypass is necessary and justified.
- Set a fixed search_path limited to pg_catalog and approved schemas.
- Revoke EXECUTE from PUBLIC immediately after creation.
- Revoke EXECUTE from anon and authenticated unless the function is intentionally exposed.
- Receive an explicit grant only to the approved caller role.
- Validate caller identity, assignment, lane, object scope, and mutation class inside the function.
- Enforce idempotency and replay protection for mutations.
- Bound text, JSON, file, and batch sizes.
- Emit an audit event for success and rejection.
- Never return secrets, credential hashes, or privileged error detail.

Worker identity may not rely solely on a client-supplied agent_id or session setting. A worker credential must be bound to an approved identity and checked by the server-side function.

## 6. Candidate, evaluation, promotion, and deployment

CANDIDATE is an intake state, not an approval stop.

The lifecycle is:

- CANDIDATE: registered, immutable source metadata and hash captured, deployment prohibited.
- EVALUATING: deterministic and model-based checks executing.
- QUALIFIED: all mandatory checks passed.
- PROMOTED: automatically promoted when the promotion contract passes and no Stop-Gate exists.
- DEPLOYABLE: deployment-specific checks passed.
- DEPLOYED: release completed and verified.

DCS confirmation is not required for ordinary promotion when all approved acceptance criteria pass. The system shall promote and report.

Human confirmation is required only when a Stop-Gate condition exists, including:

- PS or confidential lane exposure.
- Destructive or irreversible mutation.
- Financial commitment.
- Public release with unresolved legal, privacy, brand, or factual risk.
- Security exception.
- Failed or indeterminate mandatory check.
- Material scope change.

A model cannot self-approve by changing its own status. Promotion must be performed by a separate deterministic promotion function or authorized controller using recorded evidence.

## 7. Automation Gate 1: Static Migration Gate

Before migration execution, automation must fail the change when any of the following is found:

- Exposed table created without RLS enabled in the same migration.
- Missing primary key without an approved exception.
- PUBLIC, anon, or authenticated grants without an access-matrix justification.
- SECURITY DEFINER without fixed search_path.
- SECURITY DEFINER retaining default PUBLIC EXECUTE.
- Policy based only on TO authenticated.
- UPDATE policy missing USING or WITH CHECK.
- Authorization using user_metadata.
- Mutation policy containing unconditional true without an approved ingest exception.
- View in an exposed schema without security_invoker or equivalent protection.
- Service-role or secret key referenced in browser code.
- Missing rollback or missing migration receipt metadata.

## 8. Automation Gate 2: Ephemeral Verification Gate

The migration must be applied to an isolated test database or Supabase branch and pass:

- Schema creation and rollback.
- Migration replay and idempotency checks.
- Anon denial tests.
- Ordinary authenticated denial or ownership tests.
- Wrong-user, wrong-worker, wrong-lane, and cross-product tests.
- Valid owner, valid worker, and service-path tests.
- RPC input validation and replay tests.
- Storage policy tests when storage is affected.
- Security advisor scan with no new unresolved warning.
- Performance advisor scan with no new critical regression.
- Application smoke tests for affected routes.

## 9. Automation Gate 3: Promotion and Drift Gate

Promotion automation must compare the candidate against the approved baseline and require:

- Exact migration hash and repository receipt match.
- No untracked production DDL.
- No RLS regression.
- No expanded grants or function execution rights outside the approved matrix.
- No new security advisor warning unless documented as an approved exception.
- Required negative tests passed.
- Rollback verified.
- Application health route passed.
- Audit receipt written successfully.

When all checks pass, the change is promoted automatically and a completion report is issued. The workflow must not stop merely to request routine approval.

## 10. Dashboard and provider-key rule

Browser applications must never request, store, or transmit secret provider keys as ordinary UI configuration.

- Anthropic, Google, OpenAI, Supabase service-role, and similar secrets belong in server-side environment variables or a protected secret manager.
- The browser may use publishable keys only.
- Provider requests must route through a server-side API, Edge Function, or approved local bridge.
- The UI must display provider availability based on a health endpoint, not ask the user to paste a secret key into the page.
- Local Ollama access must use a bounded local bridge or allowlisted origin configuration. Global wildcard CORS is prohibited for production use.

## 11. Baseline and exception control

A security baseline shall record:

- Exposed schemas.
- RLS state for every table.
- Policies and grants.
- SECURITY DEFINER functions and EXECUTE roles.
- Storage policies.
- Advisor warnings and accepted exceptions.
- Migration versions and hashes.

Any delta from that baseline must be explained by the migration receipt. Accepted exceptions require an owner, reason, expiration or review date, compensating control, and test evidence.

## 12. Current mandatory remediation

The following current conditions are subject to immediate remediation and verification:

- RLS disabled on public.dcse_participant_review_tasks.
- RLS disabled on public.dcse_repair_tasks.
- RLS disabled on public.dcse_promotion_state_log.
- Worker-facing SECURITY DEFINER functions callable by unintended roles.
- Dashboard browser prompts for Anthropic and Google secret API keys.
- Ollama browser connectivity dependent on unresolved CORS configuration.

## 13. Definition of done

A Supabase change is complete only when:

- Code exists in the repository.
- Migration applied successfully in the required environment.
- RLS, grants, and policies match the access matrix.
- Positive and negative tests pass.
- Advisors are reviewed.
- Rollback is verified.
- Application health is verified.
- Receipt is recorded.
- Promotion occurs automatically when no Stop-Gate exists.

Anything less is development remaining, not completion.
