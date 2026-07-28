# DCSE V7 Runtime Compiler Architecture

Status: Candidate for Convergence Review 001

## Purpose
The Runtime Compiler converts a governed objective into a bounded, traceable runtime packet. It resolves entity, lane, authority, doctrine, executable rules, skills, workflow, capabilities, worker eligibility, scope, tests, limits, Stop-Gates, and evidence requirements.

Workers execute. The Runtime Compiler decides what they execute with. The Command Post decides why and when execution occurs.

## Compiler sequence
1. Normalize objective.
2. Resolve entity and lane.
3. Resolve authority and firewall.
4. Resolve destination and risk.
5. Resolve doctrine through Minimum Effective Context.
6. Resolve executable rules.
7. Resolve skills.
8. Resolve workflow.
9. Resolve capabilities and eligible workers.
10. Resolve repository and data scope.
11. Attach ECI requirements and negative tests.
12. Attach cost, time, retry, rollback, and Stop-Gates.
13. Assemble packet.
14. Generate runtime hash.
15. Validate.
16. Register and dispatch.
17. Link execution receipt.
18. Capture drift and learning.

## Frequency
- Per task: every task receives a newly compiled packet.
- Event driven: recompile after material doctrine, rule, skill, workflow, routing, security, OTI, AGE, or DEE changes.
- Daily: integrity and stale-reference checks.
- Weekly: context, routing, token, and cost optimization.
- Monthly: architecture, retirement, promotion, and drift review.

## Doctrine selection
Workers do not independently determine governing doctrine. The Doctrine Resolver selects the minimum authoritative set using task type, entity, lane, authority, destination, risk, product type, content type, and required outputs.

## OTI and AGE
AGE is native to OTI. Operational changes may be tested and routed automatically. Architectural changes create bounded change packets. Constitutional, firewall, security, or promotion changes require Level 0.

## DEE
DEE covers technology, models, products, content, employment, freelance work, consulting, and human skill development.

## Content as product
Content tasks require audience, objective, ownership, source and claim controls, story architecture, illustration and media needs, voice, accessibility target, delivery, distribution, commercial readiness, and outcome measures.

## Result states
PASS, REPAIRABLE, DRIFT, STOP_GATE, BLOCKED.

## Promotion
Candidate, Reviewed, Validated, Approved, Promoted. No artifact becomes authority by existence or successful execution alone.
