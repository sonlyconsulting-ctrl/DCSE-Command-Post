# DCSE Vercel Promotion and Rollback Checklist v1

**Status:** OPERATIVE - package control  
**Package:** DCSE v7.2 Vercel Governance Package  
**Task ID:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02  
**Authority:** DCS Level 0 or verified delegated authority for the exact action.

## A. Promotion preflight

- [ ] Task ID, lane/entity, product, project/team, environment, and destination recorded.
- [ ] Exact repository, branch, source SHA, and root directory recorded.
- [ ] Candidate Vercel deployment ID/URL recorded.
- [ ] Deployment is the same artifact that was validated.
- [ ] Required GitHub checks passed for the exact head SHA.
- [ ] Preview protection remained intact or an authorized access method was used.
- [ ] Required routes/APIs passed.
- [ ] Applicable desktop/mobile/customer-flow checks passed.
- [ ] Authentication/authorization passed where applicable.
- [ ] Server-side data/provider path passed where applicable.
- [ ] Browser console and runtime logs show no unresolved critical/high finding.
- [ ] Development/Preview/Production variable-name matrix reviewed.
- [ ] No secret value appears in source, logs, screenshots, prompts, or evidence.
- [ ] Domain/alias target and canonical-host behavior verified.
- [ ] Data/database migration state identified and compatible.
- [ ] Cost/rate-limit state permits one controlled promotion and observation cycle.
- [ ] Rollback target is identified and known compatible.
- [ ] Unresolved findings are listed with owner/disposition.
- [ ] DCS Level 0 approval or exact delegated authority is evidenced.

## B. Promotion execution evidence

- [ ] Exact deployment promoted without an unvalidated rebuild where supported.
- [ ] Production traffic assignment recorded.
- [ ] Primary domain resolves to intended deployment.
- [ ] Critical route/API smoke test passed after promotion.
- [ ] Customer/operator critical path passed after promotion.
- [ ] Runtime logs observed after promotion.
- [ ] GitHub, Vercel, data state, and Tribunal evidence reconciled.
- [ ] Final state assigned: PROMOTED, OBSERVED, RECONCILED, COMPLETE, PARTIAL, or BLOCKED.

## C. Rollback decision gate

Trigger rollback review when any of the following is true:

- production critical path fails;
- authentication/authorization regression is observed;
- material data/provider incompatibility appears;
- domain points to wrong deployment;
- security exposure or unsafe runtime behavior is detected;
- error rate or availability impact exceeds the approved tolerance;
- required evidence proves the promoted artifact is not the validated artifact.

Before rollback:

- [ ] Incident/task ID and reason recorded.
- [ ] Current and target deployment IDs recorded.
- [ ] Target deployment is known-good for intended domains.
- [ ] Database/external side effects assessed.
- [ ] Rollback authority confirmed.
- [ ] Customer/user impact and communication need assessed.

## D. Rollback execution and verification

- [ ] Traffic reassigned to authorized target deployment.
- [ ] Domain/alias assignment verified.
- [ ] Critical routes/APIs retested.
- [ ] Authentication and data/provider path retested where applicable.
- [ ] Runtime logs inspected.
- [ ] Database/external side effects reconciled or explicitly left open.
- [ ] GitHub/Vercel/Tribunal records updated.
- [ ] Final state is COMPLETE only if cross-system state reconciles; otherwise PARTIAL or BLOCKED.

## E. Package promotion boundary

This checklist governs Vercel promotion/rollback. It does not authorize Supabase remediation. The separate 2026-09-15 Supabase broader database audit HOLD remains controlling for its database scope until its own gates are closed.

## Level Zero approval record

Approved as part of the single DCSE v7.2 Vercel Governance Package promotion on 2026-09-15. No production deployment was performed by the package promotion.
