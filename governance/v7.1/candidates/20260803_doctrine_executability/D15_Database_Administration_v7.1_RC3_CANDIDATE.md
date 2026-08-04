# DCSE Doctrine D15: Database Administration v7.1 RC3 Candidate

**Document ID:** DCSE-D15-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to system, product, PS, PPR, and privacy isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D15_Database_Administration.md`  
**Source SHA-256:** `6262bb12238503ff95d3fbea01dd16b9daf8df191b4bc17f0164880d536a6c46`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Orchestration dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D03_AI_Orchestration_v7.1_RC3_CANDIDATE.md`  
**Orchestration dependency SHA-256:** `88e80cf310ea55b36571d565218863f60171de228c13d9cead81e69b0a60beb0`  
**File-system dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D06_File_System_Device_Governance_v7.1_RC3_CANDIDATE.md`  
**File-system dependency SHA-256:** `8b100e242f8439d403cfb6b88ca923c79f327b7d2a082f6fac9be42075defd36`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D15 governs the design, access, authorization, migration, integrity, operation, monitoring, backup, recovery, privacy, audit, and retirement of DCSE data systems.

It applies to hosted PostgreSQL and Supabase projects, local databases, object storage, database functions and RPCs, views, Auth integration, Realtime, Queues, Cron, Edge Functions, database branches, and approved offline protected stores.

D15 is the controlling database doctrine. A Supabase-specific doctrine such as D17 may add implementation detail but may not weaken D15. DDNA doctrine governs semantic extraction and learning, not database authority or security.

## 2. Governing principles

1. Security is part of object creation, not a later repair phase.
2. Authentication, authorization, grants, RLS, function execution rights, and application checks are distinct controls.
3. A successful query, migration, deployment, heartbeat, or advisor run proves only its measured scope.
4. Negative authorization tests are required alongside positive tests.
5. Database state, repository migrations, generated types, application assumptions, and receipts must reconcile.
6. Service-role or other bypass credentials never substitute for caller identity or object-level integrity controls.
7. Privileged functions are exceptional, narrowly callable, schema-qualified, and auditable.
8. Every mutation is attributable, bounded, retry-safe where required, and recoverable.
9. Protected and personal data are minimized, isolated, and processed only for an authorized purpose.
10. Correctable defects are repaired within approved scope; affected unsafe actions are isolated while safe work continues.

## 3. System and environment registry

Every data system must resolve through an approved registry or verified adapter.

```yaml
data_system:
  system_id: ""
  display_name: ""
  provider: ""
  engine: ""
  project_or_cluster_ref: ""
  environment: "LOCAL | DEVELOPMENT | TEST | PREVIEW | STAGING | PRODUCTION | OFFLINE_PROTECTED"
  entity: ""
  lane: ""
  classification_ceiling: ""
  constitutional_role: "NONE | REFERENCE | GOVERNANCE_REGISTRY"
  operational_role: ""
  exposed_schemas: []
  private_schemas: []
  data_api_enabled: "UNKNOWN"
  auth_provider: ""
  storage_enabled: false
  realtime_enabled: false
  queues_enabled: false
  cron_enabled: false
  edge_functions_enabled: false
  credential_refs: []
  migration_root_ref: ""
  backup_policy_ref: ""
  owner: ""
  authority_ref: ""
  verified_at: ""
  status: "ACTIVE | DEGRADED | QUARANTINED | RETIRED"
```

DCSE-DDNA, SC Command Post, product databases, preview branches, and protected offline stores are separate systems. A row in one system does not establish delivery, completion, authority, or state in another.

## 4. Schema adapter contract

No database-backed runtime routing activates until an approved physical schema adapter exists.

```yaml
schema_adapter:
  adapter_id: ""
  system_id: ""
  schema_version: ""
  migration_baseline: ""
  objects: []
  logical_to_physical_fields: {}
  primary_keys: {}
  foreign_keys: {}
  lifecycle_constraints: {}
  authorization_model_ref: ""
  rpc_signatures: {}
  generated_type_ref: ""
  content_hash: ""
  verified_at: ""
  status: "APPROVED | DEGRADED | RETIRED"
```

Repository-based read-only routing may operate first when canonical source identity is verified. Missing or stale adapters prohibit affected writes and final status claims, not unrelated safe inspection or candidate work.

## 5. Data classification and privacy

Every table, column group, object bucket, message payload, and exported dataset receives an owner, purpose, lane, classification, retention rule, and authorized audience.

Minimum rules:

- PS and PPR data remain within their separately authorized boundary.
- Family, minor, health, financial, account-recovery, precise-location, identity-masked, and other sensitive data use explicit access restrictions.
- Public, internal, family, protected, and classified states are not interchangeable.
- Production personal data is not copied into development or model prompts unless explicitly authorized and minimized.
- Logs, audit events, dead letters, receipts, and error messages must not reproduce secrets or excessive personal data.
- Data collection and retention are limited to an approved purpose.
- Deletion, anonymization, correction, export, and consent obligations are implemented where applicable.

## 6. Access modes and credential boundaries

Approved access modes include:

| Mode | Expected use | Required control |
| --- | --- | --- |
| Publishable client key plus JWT | Browser or mobile Data API | Least-privilege grants and tested RLS |
| Trusted server client | Server-side application operations | Secret storage, scoped route authorization, audit |
| Direct PostgreSQL connection | Migrations, trusted workers, DBA tools | Secret manager, TLS, connection pooling as applicable |
| Edge Function | Server-side bounded API or integration | JWT or explicit custom authentication and scoped secrets |
| MCP or management interface | Governed inspection and administration | Project scope, least privilege, attribution, no secret disclosure |
| Local or offline adapter | Protected or disconnected operation | Local encryption, access control, manifest, reconciliation plan |

Rules:

- Secret and service-role keys never enter browser code, localStorage, request bodies from an ordinary browser, logs, prompts, doctrine, receipts, or repositories.
- Public or publishable keys are identifiers, not authorization. RLS and grants remain mandatory.
- Modern revocable publishable and secret keys are preferred when supported; legacy keys are tracked for rotation.
- A worker must not receive service-role credentials merely to avoid designing authenticated worker identity.
- Credential rotation, revocation, ownership, environment, use, and last verification are tracked without storing the value in ordinary tables.

## 7. Authentication and authorization

Authentication establishes the principal. Authorization establishes permitted resources and operations.

- Client-supplied identity fields, agent IDs, role names, session settings, headers, or request payloads are not trusted identity unless cryptographically or server-side bound.
- Authorization decisions must not use user-editable metadata.
- Supabase `raw_user_meta_data` and `user_metadata` are prohibited for authorization.
- Approved app metadata, membership tables, server-side allowlists, or verified claims may support authorization, subject to freshness and revocation controls.
- JWT-based authorization accounts for token staleness. Sensitive operations may require fresh session validation.
- Deleting or disabling an identity does not by itself prove all issued sessions are invalidated.
- Anonymous sign-in identities must be distinguishable from permanent users when the product permits anonymous sign-in.

## 8. Grants and Data API exposure

Grants determine whether a role can reach an object. RLS determines which rows are available after access is granted.

Every migration that creates or changes a Data API object must explicitly declare:

- whether its schema is exposed;
- required privileges for `anon`, `authenticated`, server, and custom roles;
- default privilege posture;
- whether Data API access is needed at all;
- matching RLS or equivalent controls;
- function `EXECUTE` roles;
- sequence and schema `USAGE` privileges.

New tables and functions must not rely on provider defaults. DCSE migrations remain valid as Supabase transitions new and existing projects toward explicit Data API grants.

## 9. Row Level Security standard

### 9.1 Table requirements

Every table in an exposed schema has RLS enabled in the same migration unless an approved equivalent control and non-exposure proof exist. Private schemas use RLS as defense in depth where appropriate.

Every RLS-enabled table is classified as one of:

- intentionally inaccessible to direct client roles, with no client policies;
- public read with a documented data-minimization justification;
- owner-scoped;
- membership or tenant-scoped;
- role-scoped;
- worker-scoped;
- server-only;
- append-only audit;
- protected or isolated.

RLS enabled with no policy is acceptable only when deny-all is intentional, direct roles lack unnecessary grants, and the state is documented. It is not evidence that required access works.

### 9.2 Policy requirements

- `TO authenticated` alone is authentication, not row authorization.
- Ownership and membership predicates use a verified principal.
- UPDATE policies include both `USING` and `WITH CHECK` when row ownership or tenant binding must remain invariant.
- UPDATE tests include the required SELECT policy because PostgreSQL must first see the row.
- Permissive policies are evaluated as logical OR. Multiple policies must be reviewed for accidental broadening.
- Restrictive policies are used when a condition must always apply and are tested with the complete policy set.
- `auth.role()` is not used as the authorization predicate; role targets use the `TO` clause and row predicates.
- Public `USING (true)` is permitted only for data deliberately classified public and minimized for that audience.
- Service-role `USING (true)` does not mitigate abuse by a holder of the bypass key; constraints, triggers, validated functions, and credential containment remain necessary.

### 9.3 Role matrix

Every affected object has tests for relevant combinations of:

- unauthenticated and anonymous;
- authenticated wrong user;
- authenticated correct user;
- wrong tenant, product, lane, or membership;
- suspended, retired, or disabled identity;
- admin and ordinary member;
- server or service path;
- replay, duplicate, expired lease, and cross-owner mutation;
- protected-lane denial;
- expected positive path.

A denial caused by a NOT NULL error, missing relation, ambiguous column, unrelated exception, or broken function is a failed authorization test, not a pass.

## 10. Views

- Exposed views use invoker security where supported so caller permissions and RLS apply.
- A definer view requires an explicit documented exception, restricted grants, and data-minimization proof.
- Views are tested for cross-user, cross-tenant, and inference leakage.
- Materialized views and cached exports receive their own access and refresh controls.

## 11. Functions, triggers, and RPCs

### 11.1 Default rule

Use `SECURITY INVOKER` unless privilege elevation is necessary and justified.

### 11.2 SECURITY DEFINER requirements

Every definer function must:

1. live in a private or intentionally exposed schema appropriate to its API role;
2. use an empty or tightly fixed `search_path` and fully schema-qualified object names;
3. revoke `EXECUTE` from `PUBLIC` immediately;
4. revoke `EXECUTE` from `anon` and `authenticated` unless intentionally exposed;
5. grant only the exact caller roles required;
6. validate verified caller identity and authorization inside the function;
7. validate lane, tenant, object, state, and mutation scope;
8. enforce input sizes, enum values, and safe error detail;
9. enforce idempotency and replay protection where mutations may retry;
10. emit attributable audit evidence without secrets;
11. pass positive and negative RPC tests;
12. appear in advisor and grant-diff review.

Adding `SECURITY DEFINER` to fix a permission error is prohibited unless the entire contract above is satisfied.

### 11.3 Trigger functions

Trigger-only functions are not ordinary RPC endpoints. Revoke direct execution from API roles and verify that the trigger continues to function.

### 11.4 Worker functions

Worker claim, heartbeat, renewal, result, release, and recovery functions must enforce:

- server-bound worker identity;
- approved status;
- lane and task-type authorization;
- immutable claim ownership;
- active and unexpired lease;
- foreign-key relationship between result and claim;
- one authoritative result per idempotency key;
- bounded concurrency;
- complete recovery of all eligible expired claims;
- dead-letter and retry limits;
- safe result acknowledgement.

## 12. Schema design and integrity

Every persistent object defines applicable:

- primary key;
- foreign keys and delete behavior;
- uniqueness and idempotency keys;
- lifecycle and enum constraints;
- nullability;
- timestamps and ownership fields;
- concurrency controls;
- audit behavior;
- comments for sensitive or non-obvious invariants;
- indexes derived from actual query and policy paths.

Application code must not be the only enforcement point for identity, ownership, state, or idempotency invariants that the database can enforce safely.

## 13. Migration lifecycle

```text
DISCOVER
  -> BASELINE
  -> DESIGN ACCESS MATRIX
  -> CREATE MIGRATION
  -> STATIC VALIDATION
  -> APPLY TO ISOLATED ENVIRONMENT
  -> POSITIVE AND NEGATIVE TESTS
  -> ADVISORS
  -> APPLICATION SMOKE TEST
  -> ROLLBACK OR FORWARD-RECOVERY TEST
  -> DRIFT CHECK
  -> REVIEW
  -> AUTHORIZED APPLY
  -> POST-APPLY VERIFY
  -> RECEIPT
```

Migration requirements:

- sortable provider-compatible version names;
- correct dependency order;
- immutable committed migration after promotion;
- no manual production hotfix left uncaptured;
- explicit grants, RLS, policies, comments, and rollback or forward-recovery strategy;
- safe replay behavior or documented one-time behavior;
- transaction use when supported and appropriate;
- no generated IDs hardcoded into later data operations without stable lookup;
- generated types and adapters refreshed after schema change;
- local and remote migration histories reconciled.

A provider check marked green does not prove the complete schema applied, that dependent schemas exist, or that the application path was exercised.

## 14. Change authority and production safety

D05 controls authority for database promotion and production mutation.

Routine bounded changes may proceed under an exact DCS-approved standing rule when the change, environment, tests, rollback, risk ceiling, and receipt destination all match. Direct DCS decision remains required for uncovered destructive operations, protected-lane changes, security exceptions, material privacy changes, credential expansion, production data deletion, or scope expansion.

No agent creates authority by editing doctrine, inserting a review row, changing task status, or passing its own test.

## 15. Supabase product controls

### 15.1 Auth

- Redirect URLs, account recovery, email change, MFA, anonymous sign-in, session duration, and password protections are environment-specific and tested.
- Leaked-password protection and other available safeguards are reviewed for production systems.
- Auth hooks and custom claims are versioned, tested, and minimally privileged.

### 15.2 Storage

- Buckets have explicit public or private classification.
- Storage policies cover select, insert, update, delete, and upsert behavior as needed.
- Upsert tests verify the combined INSERT, SELECT, and UPDATE requirements.
- Signed URLs have bounded duration and audience.
- Database backups do not prove Storage objects are backed up.

### 15.3 Realtime

- Publication membership is explicit.
- Sensitive tables are not replicated to unauthorized clients.
- RLS and channel authorization are tested for Realtime separately from Data API checks.

### 15.4 Queues and Cron

- Jobs are idempotent or deduplicated.
- Claims use leases and bounded retries.
- Overlap and single-instance behavior are explicit.
- Failures route to durable dead-letter or recovery evidence.
- Schedules, enablement, and actual execution are separate states.

### 15.5 Edge Functions

- JWT verification remains enabled unless custom authentication is explicit and tested.
- A public or no-JWT endpoint must deny unsafe requests by construction.
- Secrets remain server-side.
- Decommissioned vulnerable endpoints use a deterministic deny-all tombstone or verified removal while dependencies are reconciled.

### 15.6 Extensions

- Extensions use approved schemas rather than `public` when supported.
- Extension installation and update behavior follows current provider rules.
- Migration scripts do not depend on unsupported version pinning.

## 16. Backup, recovery, and continuity

```yaml
database_backup_record:
  backup_id: ""
  system_id: ""
  environment: ""
  scope: "SCHEMA | DATA | PITR | LOGICAL | STORAGE_OBJECTS | COMPLETE_SERVICE"
  created_at: ""
  encrypted: false
  retention_until: ""
  destination_ref: ""
  manifest_or_hash_ref: ""
  restore_target: ""
  restore_tested_at: ""
  restore_result: "UNKNOWN"
  rpo_result: ""
  rto_result: ""
```

Rules:

- Backup commands use argument arrays or approved tooling, not `shell=True` command strings containing database URIs.
- Credentials are not exposed in command lines, logs, or filenames.
- Restore tests occur in an isolated target.
- Rollback scripts that intentionally reopen a vulnerability are audit artifacts, not normal operational rollback.
- Destructive rollback steps are explicit and disabled until separately authorized.
- Forward recovery is preferred when rollback would destroy valid newer data.

## 17. Audit, monitoring, and self-correction

Monitoring covers:

- security and performance advisors;
- RLS-disabled or RLS-no-policy objects;
- object grants and default privileges;
- definer functions and views;
- trigger functions callable as RPCs;
- exposed schemas and Data API settings;
- migration drift;
- schema and generated-type drift;
- failed auth, RPC, storage, realtime, and database logs;
- stale leases and orphaned work;
- duplicate results and idempotency violations;
- unexpected public reads;
- backup and restore age;
- extension placement and provider breaking changes;
- credential age and suspected exposure;
- privacy, retention, and consent exceptions.

### 17.1 Healing boundary

The system may automatically correct a known issue only when an approved remediation rule identifies the exact condition, environment, change, tests, rollback or forward-recovery method, and audit destination.

Automatic healing must:

1. capture the pre-state;
2. prove the defect with a deterministic check;
3. generate or select an immutable migration;
4. apply first in an isolated environment when available;
5. run targeted negative and positive tests;
6. verify no access broadening;
7. apply only within standing authority;
8. verify post-state and application health;
9. record the exact change and evidence;
10. revert or isolate only the affected change when verification fails.

Automatic healing must not guess a missing policy, add `SECURITY DEFINER`, broaden grants, disable RLS, expose a schema, or use service-role bypass simply to make an error disappear.

## 18. Accessibility and user safety

Database design must support accessible product behavior without weakening privacy:

- account recovery and verification states are explicit and do not strand users silently;
- user-facing errors distinguish permission, validation, unavailable service, and no-result states without leaking privileged detail;
- profile and preference schemas support accessibility settings where the product requires them;
- consent and trust acknowledgements are versioned and attributable;
- administrators can correct data through audited flows rather than direct untracked edits;
- deletion, correction, export, and recovery workflows remain usable by authorized users.

Accessibility acceptance belongs in application doctrine and tests, but D15 must preserve the data and authorization states those flows require.

## 19. Database change receipt

```yaml
database_change_receipt:
  receipt_id: ""
  task_ref: ""
  system_id: ""
  environment: ""
  migration_refs: []
  migration_hashes: []
  pre_schema_ref: ""
  post_schema_ref: ""
  access_matrix_ref: ""
  positive_tests: []
  negative_tests: []
  advisor_before: []
  advisor_after: []
  advisor_exceptions: []
  application_checks: []
  rollback_or_recovery_result: ""
  drift_result: ""
  privacy_result: ""
  secret_scan_result: ""
  authority_ref: ""
  result: "PASS | PASS_WITH_FINDINGS | FAIL | PARTIAL"
  findings: []
  verified_at: ""
```

Advisor findings classified INFO are still recorded and dispositioned. A receipt cannot claim zero findings when it filtered them out by schema or severity without saying so.

## 20. Failure behavior

| Condition | Required behavior |
| --- | --- |
| Schema adapter missing or stale | Disable affected writes and final claims; continue verified read-only source work. |
| Permission error `42501` | Identify whether the missing layer is grant, RLS, schema usage, or function execution; do not add bypass privileges reflexively. |
| Query returns zero rows unexpectedly | Check SELECT policy, UPDATE visibility, filters, and identity freshness before claiming success. |
| Authorization test fails for unrelated error | Mark test invalid and repair the fixture or function. |
| Advisor finds privileged callable function | Isolate endpoint if needed; inspect intended caller; revoke or redesign through migration. |
| Migration history diverges | Stop affected apply; reconcile version names, order, hashes, and remote history. |
| Manual production hotfix discovered | Capture exact state in a migration and verify other environments. |
| Worker or job overlaps | Enforce lease, lock, idempotency, and recovery; do not rely only on scheduler status. |
| Suspected credential exposure | Contain, rotate or revoke, inspect use, and record non-secret evidence. |
| D15 unavailable | Do not invent database authority or security; continue unrelated safe work. |

## 21. Runtime interfaces

```text
resolve_data_system(system_id, environment) -> DataSystemResolution
load_schema_adapter(system_id, version) -> SchemaAdapter
inspect_access_surface(system_id) -> AccessSurfaceReport
validate_migration(migration_ref, baseline_ref) -> MigrationValidation
run_authorization_matrix(system_id, object_refs, fixture_ref) -> AuthorizationReport
run_advisors(system_id) -> AdvisorReport
detect_database_drift(system_id, repository_ref) -> DriftReport
plan_database_recovery(system_id, incident_ref) -> RecoveryPlan
execute_approved_remediation(plan, authority_ref) -> DatabaseChangeReceipt
```

## 22. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D15-001 | Exposed table created | Same migration declares grants, enables RLS, and adds intended policies. |
| D15-002 | RLS table intentionally server-only | No client policies or grants; deny-all intent is documented and tested. |
| D15-003 | Authenticated user reads another user's row | Denied by ownership or membership predicate. |
| D15-004 | UPDATE attempts to change owner | `WITH CHECK` rejects reassignment. |
| D15-005 | UPDATE has no SELECT visibility | Test reports missing visibility rather than false success. |
| D15-006 | Anonymous sign-in is enabled | Permanent-user-only action checks the anonymous claim. |
| D15-007 | Policy uses user metadata or `auth.role()` | Static gate fails. |
| D15-008 | Multiple permissive policies overlap | Effective OR behavior is analyzed and tested. |
| D15-009 | Definer function retains PUBLIC execute | Static or advisor gate fails. |
| D15-010 | Trigger-only function is RPC-callable | Direct execution is revoked and trigger path retested. |
| D15-011 | Definer function has mutable search path | Migration gate fails. |
| D15-012 | Worker submits without real active claim | Foreign key and lease controls reject it. |
| D15-013 | Worker replays same result | Idempotency constraint rejects or returns prior result safely. |
| D15-014 | Worker claims another lane | Server-bound identity and lane rule deny it. |
| D15-015 | Claim expires beyond one recovery cycle | Recovery processes every eligible expired claim. |
| D15-016 | Migration filename is not provider-compatible | Static gate fails before preview deployment. |
| D15-017 | Production hotfix is absent from repository | Drift gate blocks promotion until captured. |
| D15-018 | Preview lacks dependent schema | End-to-end claim remains unverified despite green migration status. |
| D15-019 | Storage upsert is required | INSERT, SELECT, and UPDATE policies are tested. |
| D15-020 | Database backup exists but Storage objects do not | Complete-service recovery remains non-pass. |
| D15-021 | Security advisor reports ERROR or WARN | Finding is remediated or explicitly excepted with authority and expiry. |
| D15-022 | Advisor reports INFO no-policy table | Intentional deny-all or missing access is classified and tested. |
| D15-023 | Browser sends provider or service key | Security gate fails. |
| D15-024 | Edge Function disables JWT verification | Custom authentication or deterministic deny-all behavior must pass negative tests. |
| D15-025 | Auto-heal proposes broad grant | Healing is rejected as unsafe. |
| D15-026 | Data API default changes | Explicit grants preserve intended behavior. |
| D15-027 | View bypasses caller RLS | Invoker behavior or approved exception is required. |
| D15-028 | Backup command contains URI in shell string | Static gate fails. |
| D15-029 | Secret appears in error or receipt | Output is redacted and exposure response begins. |
| D15-030 | Required D15 source is unavailable | Only database-authority-dependent actions are isolated. |

## 23. Cross-doctrine boundaries

- D03 selects capable database runtimes and preserves accountable ownership.
- D04 governs communication and delivery evidence.
- D05 governs database promotion and production authority.
- D06 governs database export, backup, and local artifact storage.
- D11 governs browser and application integration.
- D13 and D14 govern protected evidentiary and PS data inside their authorized boundary.
- D16 governs DDNA semantics and must use D15-approved adapters and access.
- D17 may specialize Supabase security and automation but cannot supersede D15.
- D20 governs product assembly and acceptance.
- D21 executes D15 contracts.
- D22 reconciles repository, runtime registry, database, and deployment state.

## 24. Evidence-grounded source correction record

The requirements above incorporate verified DCSE history, including:

- RLS remediation after orchestration tables were first created without complete enforcement;
- a production security remediation that reduced 43 advisor findings but left residual debt;
- browser storage and request transmission of provider API keys;
- trigger and definer functions retaining unintended API execution rights;
- mutable `search_path` on privileged functions;
- a caller-asserted worker identity endpoint that minted tokens without an enrollment secret and later required a deny-all tombstone;
- worker results accepted without real claims, active leases, or duplicate suppression;
- cross-worker mutation enabled by service-role bypass;
- recovery logic that permanently orphaned older expired claims;
- authorization tests that falsely passed because unrelated errors caused the denial;
- production hotfixes absent from repository migrations;
- nonconforming migration version names and dependency order;
- preview branches missing dependent schemas while provider checks appeared green;
- live advisor debt on both DCSE-DDNA and SC Command Post as of 2026-08-03.

These findings are evidence for preventive controls. They are not embedded as permanent object names or a claim that the transient findings remain unchanged after the recorded date.

## 25. Candidate status

This candidate is correction evidence only. It does not change either Supabase project, apply a migration, broaden or revoke access, or replace the active D15 until DCS promotes the exact artifact or exact diff and D22 records the authoritative representation.
