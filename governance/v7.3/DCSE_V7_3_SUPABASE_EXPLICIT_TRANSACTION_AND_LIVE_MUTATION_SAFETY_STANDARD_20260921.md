# DCSE V7.3 Supabase Explicit Transaction and Live-Mutation Safety Standard

**Task ID:** DCSE-V73-SUPABASE-SAFETY-RECONCILIATION-20260921-01  
**Status:** OPERATIVE upon Level 0 promotion and canonical merge  
**Authority:** DCS Level 0  
**Lane:** DCSE / ALL SUPABASE PROJECTS  
**Classification:** INTERNAL  
**Effective date:** 2026-09-21

## 1. Controlling boundary

Supabase inspection, source SQL, candidate migration, committed migration, applied migration, runtime data mutation, and verified synchronization are separate states.

No generic instruction authorizes a live database mutation. Source approval, GitHub merge, CI success, a migration file, configured credentials, a successful connection, or a dashboard display is not proof that the intended live state exists.

## 2. Project identity firewall

Before any Supabase query or mutation, record and verify:

- project name and immutable project reference;
- environment;
- schema;
- object/table/function;
- lane/entity and data classification;
- credential class and secret source;
- read-only or mutating intent;
- expected result and rollback.

DCSE-DDNA governance and SC Command Post operations are distinct projects. An environment-variable fallback, familiar schema name, copied record, or available credential SHALL NOT select the target project.

If project identity is missing, conflicting, or inferred: `SUPABASE_TARGET_UNRESOLVED`; stop before querying privileged state or writing.

## 3. Safe inspection

Read-only inspection is permitted only within task authority and shall:

- use the least-privileged available credential;
- identify the target project explicitly;
- avoid exporting secrets or protected data;
- bound result size;
- record whether evidence came from repository source, database metadata, or live row readback.

Configuration presence is reported as `CONFIGURED_UNVERIFIED`, never synchronized.

## 4. Candidate and migration lifecycle

```text
SOURCE PLAN
-> supabase/candidates (NON-DEPLOYING)
-> security/static review
-> isolated local/branch proof
-> explicit transaction authorization
-> supabase/migrations
-> authorized live apply
-> live schema/RLS/data readback
-> repository/live-history comparison
-> receipt
```

Candidate SQL SHALL remain outside `supabase/migrations/`. Moving a file into `supabase/migrations/` is a deployment-capable action because Git integration may apply it. It requires the authorization packet in §5 even when no agent directly calls Supabase.

A migration filename or GitHub merge is never proof of application.

## 5. Mandatory Supabase transaction authorization packet

Any changed file under `supabase/migrations/`, live SQL, migration application, RLS/policy change, privileged RPC change, auth change, storage-policy change, secret rotation, or production data mutation requires:

```text
SUPABASE TRANSACTION AUTHORIZED
Task ID:
Project name:
Project reference:
Environment:
Schema/object:
Lane/data classification:
Operation class:
Exact migration path or SQL hash:
Forward effect:
RLS/grant/auth effect:
Data effect:
Destructive effect: none | exact authorized effect
Backup/checkpoint:
Verification queries:
Rollback:
Git-integration apply authorized: true | false
Live mutation authorized: true | false
Authorization: DCS Level 0 or exact delegated authority
Single use: true
```

Missing, ambiguous, inherited, or inferred fields produce `SUPABASE_MUTATION_NOT_AUTHORIZED`.

## 6. RLS and authorization stop gates

The following are prohibited without an explicit exception and security proof:

- exposed application tables without RLS;
- `TO authenticated` without an ownership/tenant authorization predicate;
- UPDATE without both `USING` and `WITH CHECK`;
- deprecated `auth.role()`;
- authorization based on `user_metadata` or `raw_user_meta_data`;
- non-`security_invoker` exposed views;
- using `SECURITY DEFINER` to bypass a permission failure;
- public client execution of privileged definers;
- mutable/untrusted definer `search_path`;
- service-role or secret keys in browser code, `NEXT_PUBLIC_*`, prompts, source, Tribunal, logs, or ordinary content;
- broad `GRANT ALL` or client-facing default privileges;
- anonymous privileged mutation.

## 7. Execution discipline

- Use explicit project targeting; never rely on ambiguous environment fallback.
- Iterate in an isolated/local environment before producing the final migration.
- Run security advisors and role-based tests before production.
- Confirm Data API exposure separately from RLS.
- Use transactions where supported and verify affected-row counts.
- Stop on unexpected row counts, schema identity, policy state, or project reference.
- Do not retry the same failed mutation repeatedly.
- Never place rollback SQL inside an auto-applied migrations directory.
- Never modify production merely to make a test pass.

## 8. Required live readback

After an authorized mutation, verify independently:

- project reference and environment;
- migration history;
- object definition;
- effective grants;
- RLS enabled/forced state;
- policy definitions;
- function owner, security mode, search path, and EXECUTE grants;
- Data API exposure where applicable;
- bounded application/user-role round trip;
- expected row counts/data result;
- rollback readiness.

`WRITE WITHOUT READBACK = PARTIAL`.

## 9. Claim language

Allowed states:

- `CANDIDATE_SOURCE_ONLY`
- `MIGRATION_AUTHORIZED_NOT_APPLIED`
- `APPLY_ATTEMPTED_UNVERIFIED`
- `LIVE_APPLIED_VERIFIED`
- `CONFIGURED_UNVERIFIED`
- `DRIFT`
- `ROLLED_BACK_VERIFIED`

No agent may say migrated, fixed, synchronized, secured, or live without the exact project, migration/transaction identity, and successful readback.

## 10. CI enforcement

Changed SQL in `supabase/migrations/` must have a single-use authorization packet that:

- is state `AUTHORIZED`;
- names the exact migration path;
- names project and project reference;
- names environment;
- explicitly sets Git-integration apply authorization;
- explicitly sets live-mutation authorization.

Candidate SQL outside migrations remains non-deploying and does not satisfy live-change requests.

Structure Precedes Scale.
