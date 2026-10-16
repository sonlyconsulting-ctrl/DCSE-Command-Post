# DCSE Vercel Agent and Platform Doctrine v1

**Document ID:** DCSE-V72-VERCEL-DOCTRINE-v1  
**Status:** OPERATIVE - DCS Level 0 approved 2026-09-15  
**Lane / Entity:** SC / DCSE Command Post  
**Classification:** INTERNAL  
**Canonical package:** DCSE v7.2 Vercel Governance Package  
**Authority:** DCS Level 0 under operative DCSE v7.2  
**Task ID:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02  
**Supersession rule:** This doctrine supplements, and does not replace, D03, D04, D05, D15, D21, D22, the platform execution profile, or the cross-system reconciliation contract.

## 1. Purpose

This doctrine establishes the authoritative DCSE control model for Vercel projects, deployments, domains, runtime configuration, Functions, observability, agent operations, promotion, rollback, and evidence. Vercel is a bounded delivery and compute platform. It is not constitutional authority, the canonical doctrine repository, or the durable source of orchestration truth.

## 2. Governing principles

1. Structure precedes scale.
2. Source identity precedes deployment claims.
3. A Vercel project is a bounded delivery surface with one declared product purpose, source root, environment model, domain set, and owner.
4. Build success, deployment readiness, production assignment, DCS promotion, and task completion are distinct states.
5. Production, public release, billing changes, security exceptions, domain changes, secret changes, destructive actions, and material architecture changes remain reserved gates unless a narrower approved procedure expressly delegates them.
6. Platform capability never creates permission.
7. Exact source SHA and deployment identity must be connected in promotion evidence.
8. Runtime proof must include the human or customer journey when that journey is part of the requested outcome.
9. Secrets remain in approved secret stores and must not enter source, prompts, screenshots, logs, Tribunal payloads, or browser-exposed variables.
10. A Vercel action may not silently expand into GitHub, Supabase, DNS, billing, or production mutation.

## 3. Vercel object model

| Vercel object | DCSE control meaning |
| --- | --- |
| Team | Administrative, access, and billing boundary |
| Project | Bounded delivery surface |
| Git link | Source integration relationship, not authority |
| Root directory | Monorepo ownership boundary |
| Deployment | Immutable build/runtime candidate |
| Preview | Candidate runtime for validation |
| Production assignment | Traffic routing state, not DCS authority |
| Domain / alias | Public or internal entry point |
| Environment variable | Runtime configuration and secret boundary |
| Function | Bounded compute unit |
| Logs / metrics | Runtime evidence with platform retention limits |
| Promote / rollback | Traffic reassignment controls requiring governed evidence |

## 4. Required project identity record

Every governed Vercel project SHALL record:

- Vercel team and project ID;
- human-readable project name;
- owning DCSE lane/entity and product purpose;
- source repository and production branch;
- root directory and framework/build/output configuration;
- included and ignored paths;
- Development, Preview, and Production variable-name inventory;
- public versus server-only variable classification;
- domains and aliases;
- expected runtime and Function behavior;
- owner and recovery contact;
- cost/rate-limit expectation;
- lifecycle state: active, review, hold, superseded, or archival candidate;
- rollback target or recovery procedure.

A project without this identity record is not eligible for production promotion.

## 5. Monorepo control

Where multiple Vercel projects observe one repository, each project SHALL have an explicit root and trigger policy. Documentation-only or unrelated product changes should not create unnecessary builds. A deployment storm, ambiguous root, duplicate product deployment, or unclear Git provenance is a governance finding and may trigger HOLD until source-to-project identity is proven.

## 6. Environment and secret control

1. Development, Preview, and Production are separate configuration contexts.
2. Missing Preview variables must be reported as configuration state, not masked by copying Production secrets.
3. Browser-visible prefixes such as `NEXT_PUBLIC_*` are public by design.
4. Service-role, provider, database, deployment, signing, and privileged tokens remain server-side.
5. Evidence records variable names, environment, presence/absence, owner, and verification time, never secret values.
6. Suspected secret exposure triggers rotation through the authorized secret owner and blocks release until reconciled.

## 7. Preview and validation

A preview candidate SHALL be tied to the exact project, root, branch, and source SHA. Validation SHALL be proportionate to the product but normally covers:

- build result;
- protected access;
- route/API smoke tests;
- desktop and mobile rendering;
- authentication and authorization where applicable;
- server-side data/provider access;
- browser console and runtime errors;
- required environment-variable presence;
- no unauthorized production mutation;
- customer or operator critical path.

A platform status such as READY is not sufficient evidence of functional readiness.

## 8. Functions and bounded compute

Vercel Functions may host bounded APIs, webhooks, server-side model calls, controlled orchestration entry points, file/metadata processing, payment callbacks, and response streaming. Long-lived leases, durable workflow state, local workstation inference, or authoritative governance state belong in the appropriate durable system. A cloud Function SHALL NOT assume it can reach a DCS workstation through `localhost`.

Function controls include input validation, authentication, authorization, bounded timeouts, idempotent retries, honest failure states, trace/evidence IDs, concurrency/cost awareness, and server-only secrets.

## 9. Domains, routing, middleware, and caching

Domain changes require exact domain, owning product, target project/deployment, DNS state, canonical redirect behavior, certificate state, legacy aliases, and rollback. Routing, middleware, headers, redirects, and cache behavior must have explicit responsibility. Cache state SHALL be considered during source/runtime reconciliation.

A product's approved architecture controls platform choice. Vercel shall not become the default host for a product whose approved architecture places the public surface elsewhere.

## 10. Agent authority model

An agent may, within verified access and task scope:

- inspect projects, deployments, logs, configuration presence, and domains;
- correlate Git SHA and Vercel deployment identity;
- run approved protected-preview tests;
- diagnose build/runtime failures;
- prepare evidence packets, rollback recommendations, and decision cards.

An inspection task does not authorize redeployment, production promotion, domain mutation, billing changes, protection removal, secret rotation, or cross-system mutation.

Every substantive Vercel assignment SHALL carry Task ID, project/team identity, environment, source repository/branch/SHA, authorized and prohibited actions, expected routes, variable-name requirements, test matrix, rate/cost boundary, rollback, and evidence destination.

## 11. Deployment state machine

`BUILT -> PREVIEW_READY -> VALIDATED -> APPROVED -> PROMOTED -> OBSERVED -> RECONCILED -> COMPLETE`

No state may be skipped by implication. Merge does not equal promotion. Promotion does not equal completion. Rollback of application traffic does not reverse database migrations or external side effects.

## 12. Promotion gate

Before Vercel production promotion, the evidence packet SHALL establish:

1. exact Git commit SHA;
2. exact Vercel project and deployment identity;
3. successful applicable checks;
4. preview/runtime acceptance evidence;
5. environment and secret review;
6. data/provider dependency status;
7. domain mapping;
8. customer/operator critical-path result;
9. cost/rate-limit state;
10. rollback target and data-compatibility note;
11. DCS Level 0 approval or verified delegated authority;
12. post-promotion observation and cross-system reconciliation plan.

## 13. Rollback

Rollback requires target deployment, scope, reason, expected user impact, data compatibility, and verification steps. After rollback, verify the intended domain assignment, critical route behavior, logs, external dependencies, and Git/Vercel/Supabase evidence state. If an associated database or external mutation is not reversed, the system remains PARTIAL until reconciled.

## 14. Cost and capacity

Plan limits are architecture inputs. Retry storms and irrelevant builds SHALL be stopped rather than amplified. A plan upgrade may address capacity but does not resolve duplicate projects, ambiguous ownership, bad roots, uncontrolled triggers, or weak provenance. Spending changes require their applicable authority gate.

## 15. Security baseline

Required controls include least privilege, MFA where available, protected previews as appropriate, server-only secrets, API authentication/authorization, safe headers/CORS, webhook signature validation, abuse/rate controls, dependency/runtime maintenance, auditability, and incident recovery. OIDC may reduce long-lived external credentials but does not waive platform-specific CI authentication requirements.

## 16. Failure handling

For build failure: verify project, SHA, root, first material error, runtime/lockfile, required variable presence, and framework/output configuration before changing code.

For runtime failure: verify domain-to-deployment mapping, reproduce a traceable request, inspect logs, identify the first failed dependency, decide rollback versus forward fix within authority, and retest the human journey.

For quota/rate-limit failure: stop automated retries, preserve evidence, identify unnecessary triggers, and resume only through one controlled validation path.

## 17. Cross-system reconciliation

GitHub proves reviewed source and repository checks. Vercel proves deployment identity and runtime evidence. Supabase or other state systems prove data-side effects. Tribunal preserves material decisions and receipts. Completion requires these claims to agree or unresolved drift to be disclosed.

The 2026-09-15 Supabase broader audit HOLD remains independent. Promotion of this Vercel governance package does not authorize or declare complete any Supabase remediation, migration, worker-access change, or production database action.

## 18. Definition of done

Vercel-governed work is COMPLETE only when the requested outcome is achieved, source and deployment identities reconcile, required tests pass, security/lane checks pass, human/customer acceptance is evidenced where applicable, rollback exists, post-change observation is recorded, and unresolved findings are either closed or explicitly accepted by the proper authority.

## 19. Package relationship

This doctrine is one of five coordinated artifacts in the DCSE v7.2 Vercel Governance Package:

1. this authoritative Agent/Platform Doctrine;
2. controlled Human-and-Agent Operations Manual;
3. annotated Masterclass Source;
4. machine-readable Control Matrix;
5. Promotion/Rollback Checklist.

The five artifacts receive one package-level Level 0 promotion. Source and training material remain non-authoritative except where a control is explicitly adopted into this doctrine or another promoted v7.2 authority.

## Level Zero approval record

DCS Level 0 directed completion and promotion of the coordinated Vercel governance package on 2026-09-15 through Task `DCSE-V72-PLATFORM-GOVERNANCE-20260915-02`. No deployment or production change is authorized by this approval.
