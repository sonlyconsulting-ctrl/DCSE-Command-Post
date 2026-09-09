# ESCD Codex Handoff After Runtime Repair 001

**Task:** DCSE-ESCD-001-RUNTIME-001  
**Review branch:** `feature/escd-runtime-repair-001`  
**Target review base:** `feature/aegis-executive-kernel`  
**Historical AG01 evidence:** `e287fd7ed41d555e9e5c9b0e00ed25fa9788f744`  
**Status:** READY FOR CODEX REVIEW

## Codex Mission

Perform independent senior engineering and security review. Do not restart product discovery or rebuild the completed policy tranche unless a concrete contradiction is found.

Review in this order:

1. authentication and operator authorization boundary;
2. RLS user-JWT repository path and absence of service-role application dependency;
3. job transition, approval, evidence and exit-criteria hard gates;
4. candidate SQL migration and trigger behavior;
5. Next Best Action adapter against the existing 54-rule / 19-rule-set policy layer;
6. briefing acknowledgement semantics;
7. safe rendering and CORS behavior;
8. runtime/adversarial tests and missing edge cases;
9. AG01-to-ESCD reconciliation dispositions.

## Hard Requirements

Codex should reject the candidate if any of these are true:

- an unauthenticated or unauthorized caller can reach privileged state;
- application code requires a service-role key for normal ESCD requests;
- `waiting_approval -> completed` is possible;
- required approval can be self-asserted by client payload;
- completion can occur without evidence and exit criteria;
- persisted content can reach unsafe HTML injection;
- briefing read advances acknowledgement without explicit ack;
- Next Best Action bypasses the tested ESCD policy contract;
- new tables weaken the current `dcse_cp.is_dcs_owner()` boundary;
- Employment logic is reintroduced into ESCD core.

## Validation Requested From Codex

- run existing ESCD pure policy tests;
- run `apps/escd/tests/test_runtime_security.py`;
- review SQL syntax and transition trigger semantics;
- if an approved safe database target exists, apply the candidate migration there and execute anon / unauthorized-authenticated / DCS-owner RLS matrix tests;
- review Vercel/Python runtime import/deployment assumptions before any deployment;
- return exact defects and repairs, not narrative approval.

## Do Not Perform Without DCS Release Authority

- merge to main;
- production Supabase migration;
- production deployment;
- Google OAuth configuration changes;
- credential/auth-provider changes;
- Android push production enablement.

## Expected Terminal Result

`CODEX_REVIEW_PASS`, `CODEX_REVIEW_FINDINGS`, or `BLOCKED`.

If findings exist, repair on the review branch or a controller-authorized successor branch and rerun the complete test surface before recommending release.
