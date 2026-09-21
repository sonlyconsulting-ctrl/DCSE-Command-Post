# DCSE V7.3 Vercel Risk-Based Preview-to-Production Release Standard

**Task ID:** DCSE-V73-VERCEL-RISK-BASED-RELEASE-20260921-01  
**Status:** OPERATIVE upon Level 0 promotion and canonical merge  
**Authority:** DCS Level 0  
**Lane:** DCSE / VERCEL PROJECTS  
**Classification:** INTERNAL  
**Effective date:** 2026-09-21

## 1. Purpose

This standard selects preview, production, verification, and rollback requirements according to change risk. Preview is mandatory when a change can alter behavior, structure, presentation, platform operation, data, security, payment, authentication, routing, configuration, or an uncertain outcome. Preview may be waived only for a bounded R0 editorial change.

This standard does not itself authorize any deployment. Every preview and production action remains subject to the explicit deployment authorization packet.

## 2. Release classes

| Class | Scope | Preview rule | Production gate |
|---|---|---|---|
| R0 EDITORIAL | Typo, punctuation, approved wording, bounded metadata correction | OPTIONAL with documented waiver | Diff review, tests, production packet |
| R1 PRESENTATION | CSS, spacing, imagery, responsive layout, visible text with wrapping/accessibility risk | REQUIRED | Preview visual/accessibility acceptance and production packet |
| R2 FUNCTIONAL | JavaScript, APIs, forms, auth, providers, persistence, workflows | REQUIRED | Preview functional acceptance and production packet |
| R3 PLATFORM | Routes, Vercel configuration, dependencies, runtime/build settings, environment variables | REQUIRED | Preview/build evidence, rollback, production packet |
| R4 CRITICAL | Database migration, RLS, secrets, payments, identity, destructive or breaking change | REQUIRED with staged coordination | Level 0 production packet and cross-system evidence |

Uncertainty moves the change to the higher class.

## 3. R0 preview-waiver criteria

Preview may be waived only when every statement is true:

1. text or bounded metadata only;
2. no HTML/document structure change;
3. no link, button, navigation, form, script, style, configuration, dependency, route, or environment change;
4. no authentication, payment, pricing, legal disclosure, security statement, governance behavior, or regulated content effect;
5. no material text-length, wrapping, responsive, accessibility, or localization risk;
6. bounded diff reviewed;
7. required syntax and regression checks passed;
8. known rollback commit recorded;
9. waiver reason recorded in the production authorization packet.

Failure of any condition requires preview.

## 4. Mandatory preview triggers

Preview is required when a change could:

- alter runtime behavior;
- affect navigation, layout, responsiveness, accessibility, or visible product experience;
- touch HTML structure, CSS, JavaScript, APIs, routes, configuration, dependencies, build logic, or environment variables;
- affect authentication, data, providers, payments, permissions, RLS, security, or secrets;
- affect shared components, multiple pages, products, projects, entities, or domains;
- be difficult to reverse or verify immediately;
- produce an uncertain classification.

## 5. Preview cycle

`AUTHORIZED SOURCE CHANGE -> TEST/BUILD -> PREVIEW AUTHORIZATION PACKET -> IMMUTABLE PREVIEW -> ACCEPTANCE -> PRODUCTION AUTHORIZATION PACKET -> PROMOTE SAME ARTIFACT -> PRODUCTION READBACK -> OBSERVE -> CLOSEOUT`

Preview authorization never authorizes production. Preview success never automatically authorizes promotion.

The exact preview artifact shall normally be promoted to production. An independent rebuild requires new artifact identity and renewed verification.

## 6. R0 direct-production cycle

`AUTHORIZED SOURCE CHANGE -> BOUNDED DIFF -> TESTS -> R0 CLASSIFICATION -> RECORDED PREVIEW WAIVER -> PRODUCTION AUTHORIZATION PACKET -> PRODUCTION RELEASE -> TARGETED READBACK -> CLOSEOUT`

“Preview optional” never means “production automatic.”

## 7. Production authorization packet

Every production release requires:

```text
PRODUCTION DEPLOYMENT AUTHORIZED
Platform: Vercel
Account/team:
Project:
Environment: production
Release class: R0 | R1 | R2 | R3 | R4
Preview disposition: validated URL/deployment ID | R0 waiver with reason
Source repository:
Exact commit/artifact:
Deployment method: promote validated artifact | exact authorized alternative
Expected effects:
Database/schema effects: none | exact authorized transaction
Alias/domain effects: none | exact authorized change
Verification URL/endpoint:
Rollback deployment/commit:
Observation window:
Authorization: DCS Level 0 or exact delegated authority
```

Missing fields produce `PRODUCTION_DEPLOYMENT_NOT_AUTHORIZED`.

## 8. Required evidence

### Preview

- deployment ID and URL;
- target = preview;
- exact commit/artifact;
- READY state;
- required visual, accessibility, functional, and integration results;
- unresolved findings.

### Production

- production deployment ID and URL;
- exact promoted artifact;
- production alias/domain state;
- live endpoint readback;
- error/log observation;
- rollback target;
- closeout receipt.

## 9. Git integration posture

Automatic Vercel Git deployments remain disabled. Preview and production are deliberate manual transactions after classification and authorization. GitHub activity alone creates no deployment authority.

Structure Precedes Scale.
