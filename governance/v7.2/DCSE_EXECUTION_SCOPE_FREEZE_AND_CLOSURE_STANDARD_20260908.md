# DCSE Execution Scope Freeze and Closure Standard

**Document ID:** DCSE-GOV-SCOPE-FREEZE-001  
**Effective Date:** 2026-09-08  
**Authority:** DCS Level 0  
**Status:** OPERATIVE  
**Applies To:** Command Post issues, workstreams, certification tasks, remediation tasks, promotion tasks, and Completion Evidence Collector closeout.

## Purpose
Prevent execution loops in which a parent issue continually absorbs new findings, remediation, validation, or follow-on work and therefore never converges to closure.

## Rule 1: Acceptance Contract Freeze
Once execution begins, the parent task's acceptance criteria are frozen. New findings do not silently become new acceptance criteria.

A new requirement may enter the parent acceptance contract only through an explicit DCS Level 0 scope-change decision that records:
- the new criterion;
- why it invalidates or materially changes the original objective;
- impact on time, risk, cost, evidence, and rollback;
- whether previously completed evidence remains valid.

Absent that decision, new findings must be classified and routed separately.

## Rule 2: Finding Classification
Every new finding discovered during execution must be classified as exactly one of:
1. **IN-SCOPE DEFECT**: prevents an original acceptance criterion from passing.
2. **DEPENDENCY BLOCKER**: external prerequisite that prevents execution but does not expand the objective.
3. **FOLLOW-ON HARDENING**: improvement that is useful but not required to satisfy the original acceptance contract.
4. **NEW WORKSTREAM**: separate objective requiring its own Task ID or issue.
5. **OBSERVATION ONLY**: evidence retained without implementation obligation.

Only IN-SCOPE DEFECTS may remain inside the parent execution loop.

## Rule 3: Retry Budget
A failed certification or execution path receives a bounded retry budget defined before retry.

Default unless a task-specific rule overrides it:
- maximum two materially distinct attempts for the same failure mode;
- no identical no-op retry;
- after the retry budget is exhausted, classify the failure as BLOCKED, isolate it, and choose an alternate architecture or route.

A retry is materially distinct only when the cause, implementation, input, dependency, or validation method changes in a way that could reasonably alter the result.

## Rule 4: No Moving Finish Line
Completed criteria remain completed unless new evidence directly invalidates the evidence that satisfied them.

A later unrelated failure does not reopen a completed criterion.

## Rule 5: Parent Issue Closure
A consolidation or parent issue is not a permanent execution bucket.

It closes when:
- each original criterion is COMPLETE, BLOCKED with an owned child issue, or SUPERSEDED by an explicit DCS-approved architecture decision;
- completed evidence is preserved;
- residual work has independent Task IDs/issues and exit criteria;
- the final CEC identifies completed items, transferred residuals, unresolved material risks, and rollback/checkpoint references.

Closing a parent issue does not claim transferred residual work is complete.

## Rule 6: Evidence Preservation
Failed attempts, receipts, result submissions, and deterministic validation failures are evidence and must not be deleted merely to make a retry appear clean.

Use release, supersession, disposition, or corrective receipts. Destructive evidence cleanup requires explicit governed retention authority.

## Rule 7: Least Privilege Does Not Yield to Certification Pressure
A certification failure must not be solved by broadening permissions beyond the task's actual requirement merely to obtain a PASS.

Examples of prohibited shortcuts without explicit DCS authority:
- global command wildcards;
- administrator escalation wildcards;
- unrestricted secret access;
- PS access for non-PS tasks;
- publication/deployment authority added solely to satisfy a test.

## Rule 8: Tool and Access Boundaries
If required evidence exists only on a host or system not reachable by the controlling runtime, the task must be marked PARTIAL or BLOCKED at that boundary. The controller must not repeatedly ask DCS to act as a message bus when an executable packet, worker, broker, connector, or future automation can carry the work instead.

## Rule 9: Independent Validation
Where governance explicitly requires independent validation, the controlling author/reviewer cannot self-ratify the artifact. The validation must be attributable to a separate authorized validator. Preparation, evidence packaging, and routing may be automated, but validator independence must remain observable.

## Rule 10: Closeout Test
Before declaring a parent task complete, answer:
1. Did the acceptance contract change without explicit authority?
2. Did a completed criterion get reopened without invalidating evidence?
3. Was the same failure retried beyond budget?
4. Were unrelated findings allowed to block the parent?
5. Was evidence deleted instead of dispositioned?
6. Was permission broadened merely to force PASS?
7. Are residuals independently owned and bounded?

Any YES to 1-6 blocks closeout until corrected. A NO on 7 blocks parent closure until routing is complete.

**Principle:** Structure Precedes Scale. Scope Precedes Retry. Evidence Precedes Closure.
