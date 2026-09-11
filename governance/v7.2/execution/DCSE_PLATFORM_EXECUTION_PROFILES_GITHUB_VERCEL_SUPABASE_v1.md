# DCSE Platform Execution Profiles: GitHub, Vercel, Supabase v1

**Document ID:** DCSE-PEP-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-11  
**Parent:** DCSE Governed Execution and Interaction Standard v1  
**Status:** APPROVED FOR CANONICAL v7.2 INTEGRATION

## 1. Purpose

Apply one execution envelope to three materially different systems without flattening their security, rollback, or validation requirements.

---

# 2. GitHub Execution Profile

**Default Effort:** MEDIUM for governed writes.  
**Typical Risk:** LOW to HIGH depending on repository, workflow, or authority effect.

Lifecycle:

`VERIFY REPO/BRANCH -> CHECK BASELINE -> BRANCH -> CHANGE -> VALIDATE -> PR -> CI -> REVIEW/RECONCILE -> MERGE -> READBACK -> RECEIPT`

Required controls:

1. verify repository and authority branch;
2. capture starting commit;
3. use a task-scoped branch for material governance/code work unless an approved direct-write path applies;
4. preserve lineage and avoid destructive history rewrite;
5. validate changed artifacts before merge;
6. use expected-head guards where supported;
7. read back merge commit and final file state;
8. capture CI result;
9. reconcile dependent manifests/registries;
10. preserve rollback reference.

Governance changes SHALL distinguish:
- file existence;
- canonical persistence;
- lifecycle state;
- promotion authority.

A commit alone does not create constitutional authority.

---

# 3. Vercel Execution Profile

**Default Effort:** MEDIUM.  
**Typical Risk:** MEDIUM, HIGH for production/domain/environment changes.

Lifecycle:

`VERIFY PROJECT -> VERIFY SOURCE -> CLASSIFY ENVIRONMENT -> BUILD -> PREVIEW -> VALIDATE -> PROMOTE -> PRODUCTION HEALTH CHECK -> RECEIPT`

Required controls:

- identify project, source repository/commit, framework/runtime, and target environment;
- distinguish Preview from Production;
- identify environment-variable requirements without exposing secret values;
- verify build result and deployment ID;
- inspect preview before production promotion for material changes;
- verify production URL/domain only after promotion;
- capture runtime/health evidence after promotion;
- preserve previous deployment or rollback target;
- distinguish deployment success from application correctness.

Reserved or elevated gates include:

- production promotion when not already delegated;
- domain/DNS changes;
- environment-secret changes;
- destructive project deletion;
- material spending/capacity changes;
- security exceptions.

A Vercel deployment may be operational evidence. It is not governance authority.

---

# 4. Supabase Execution Profile

**Default Effort:** HIGH for governed writes involving schema, RLS, auth, secrets, migrations, production data, or privileged functions.

Lifecycle:

`VERIFY PROJECT -> IDENTIFY DATA CLASS -> INSPECT CURRENT STATE -> BACKUP/CHECKPOINT -> PLAN -> VALIDATE SQL/MIGRATION -> EXECUTE -> RLS/AUTH/SECURITY TEST -> DATA VERIFY -> ROLLBACK VERIFY -> REGISTRY/RECEIPT`

Before privileged work capture:

- project ID/name;
- schema/object;
- environment;
- actor/access mechanism;
- data classification;
- secret/PS exposure;
- action type;
- approval/delegation;
- expected rows/objects affected;
- rollback/checkpoint;
- evidence destination.

## 4.1 Secret Rules

Never expose or store:

- passwords;
- service-role keys;
- API tokens;
- private keys;
- connection strings;
- recovery codes;
- MFA secrets.

Use secured runtime/plugin/MCP access. Credential custody never creates authority.

## 4.2 Schema and Migration Rules

For schema or migration work:

1. inspect current schema;
2. determine dependencies;
3. define forward migration;
4. define rollback/recovery;
5. evaluate RLS/auth/access effect;
6. execute only within verified authority;
7. validate expected schema;
8. run access/security tests;
9. confirm application/runtime compatibility where applicable;
10. record migration/version/evidence.

## 4.3 Data Mutation Rules

For material UPDATE/INSERT/DELETE:

- define target predicate;
- estimate/verify affected scope;
- use transaction where appropriate;
- avoid broad destructive predicates without explicit authority;
- verify post-write state;
- preserve audit/receipt.

Destructive operations outside approved procedure remain a reserved stop gate.

## 4.4 RLS/Auth Rules

RLS, authentication, role grants, service-role behavior, and access policy are security architecture.

They require:
- explicit access model;
- least privilege;
- positive and negative tests;
- anon/authenticated/service-role distinctions where relevant;
- no reliance on client-side secrecy;
- post-change security validation.

## 4.5 Runtime State

Supabase may be canonical for structured runtime/registry state under D22. A database row does not independently create constitutional authority.

---

# 5. Common Readback Rule

Every material write to GitHub, Vercel, or Supabase SHALL be followed by readback or equivalent verified evidence.

`WRITE WITHOUT READBACK = PARTIAL`

## 6. Common Rollback Rule

If rollback is applicable, record the rollback target before the change.

If rollback is impossible or materially lossy, classify reversibility accordingly and elevate risk/approval before execution.

## 7. Cross-System Work

When one task touches more than one of these systems, the Cross-System Reconciliation and Completion Evidence Contract applies.

**Structure Precedes Scale.**
