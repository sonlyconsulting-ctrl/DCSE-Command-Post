> **v7.2 alignment note (2026-09-11):** The reserved stop-gate substance below is retained as a current v7.2 control. Historical BOW sequencing language remains source lineage only where still present and does not expand current scope.

# DCS Level 0 Reserved Stop-Gates and Conditional Advancement v7.2

Status: ACTIVE
Authorized by: Donald Seals, DCS Level 0
Scope: v7.2 governed execution and promotion controls

DCS Level 0 authorizes immediate readiness testing, baselining, bounded execution, correction, retesting, independent review, controlled validation, conditional promotion, and sequential release of the v7.2 governed work.

## Automatic advancement

A body of work is conditionally approved to advance and promote when:

1. all required acceptance criteria pass;
2. the independent reviewer returns APPROVE;
3. GitHub and Supabase evidence reconcile;
4. no unresolved critical or high-risk finding remains;
5. no reserved stop gate is triggered;
6. rollback or recovery is documented;
7. canonical artifacts and commit SHAs are read back from GitHub.

Minor and moderate defects return automatically to the executor for correction, retest, and rereview.

## Sequential release

- BOW-001 promotion releases BOW-002.
- BOW-002 promotion releases BOW-003.
- BOW-003 promotion completes the Foundational Trilogy.

## Reserved DCS stops

This authorization does not waive DCS review for:

- production or public release;
- destructive operations outside an approved procedure;
- security exceptions or credential exposure;
- lane conflicts;
- material architecture replacement;
- material new spending;
- constitutional governance changes;
- unresolved critical or high-risk findings;
- reviewer disposition REJECT or INSUFFICIENT_EVIDENCE;
- unreconciled GitHub and Supabase evidence.

## Authority limitation

Models and agents may execute, review, verify, and recommend. Final authority originates from DCS Level 0 through this conditional authorization. No model may expand the scope of this authorization.