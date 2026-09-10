# ESCD TEST PASS 2

**Task ID:** DCSE-ESCD-001-EXEC-PA-003  
**Pass:** Adversarial / regression for candidate tranche  
**Status:** PASS WITH DECLARED RELEASE-LEVEL LIMITATIONS

## Adversarial controls exercised

The exact-head review suite verifies or statically enforces:

- terminal items do not re-enter the executive queues or NBA
- blocked items cannot age/promote into NOW
- equal-score NBA ordering is deterministic
- duplicate intake retains provenance rather than deleting source identity
- structured source links are append-only and idempotent
- cross-principal candidate inserts are rejected by RLS policy checks
- invalid item transitions are rejected
- item transition history is append-oriented
- routine configuration cannot be silently mutated in place
- duplicate/paused routine evaluation is bounded
- sensitive contact inference is rejected
- communication drafting does not send externally
- calendar analysis does not mutate external commitments
- notification evaluation creates intent only and does not claim delivery
- security/permission failure blocks automatic retry
- command, file and mobile contracts do not claim execution
- existing approval, evidence and job-verification hard gates remain covered by the regression suite
- browser-rendered persisted content continues to use safe DOM text operations rather than `innerHTML`
- no normal runtime service-role credential dependency is introduced

## Regression result

The complete ESCD Python suite passed **157/157** and all isolated SQL behavior scripts passed in GitHub Actions run `34426600439`.

## Limits of this pass

This is adversarial validation of the candidate repository/runtime tranche, not a production E2E certification. Live Gmail/Calendar writes, Android push delivery, production Supabase application, production deployment, and device/browser release journeys remain deliberately outside this tranche and require their later authorized gates.
