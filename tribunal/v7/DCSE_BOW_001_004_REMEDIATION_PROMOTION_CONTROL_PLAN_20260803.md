# BOW-001 Through BOW-004 Remediation and Promotion Control Plan

## Objective

Convert the four completed audit records into executable build, test, fix, validate, approve, and promote work without named-model stoppages or false completion.

## Asset sequence

| Asset | Immediate workstream | Blocking relationship |
|---|---|---|
| BOW-001 | Poller host hardening and capability routing | Enables dependable unattended execution but does not block safe manual or connector-backed work |
| BOW-002 | Registry defect remediation | Can proceed concurrently |
| BOW-003 | TSL security and production remediation | Can proceed concurrently, subject to canonical source reconciliation |
| BOW-004 | CTJ canonicalization and production remediation | Can proceed concurrently |

## Operating lifecycle

1. **Plan:** Convert each finding into a task with evidence, severity, acceptance test, dependency, eligible capability, and rollback.
2. **Build:** Execute bounded corrections against a named branch and task assignment.
3. **Test:** Run required unit, integration, security, data, host, and rollback tests.
4. **Fix:** Create correction tasks from failed assertions and repeat the affected tests plus regression tests.
5. **Validate:** Reconcile output artifacts, hashes, assignment results, GitHub commits, and Supabase records.
6. **Approve:** Use an eligible independent reviewer that did not produce the evidence. Model identity is not mandatory when capability and independence are verifiable.
7. **Promote:** Merge the reviewed result into the governance branch and then promote to `main` only when the product or operational gate passes.

## Nonstoppage rules

- Unavailable providers trigger reassignment to another eligible capability.
- Independent workstreams continue unless a machine-readable dependency or Stop-Gate applies.
- Conversational approval is not required for bounded, reversible work already covered by the work order.
- Security exposure, destructive operations, production deployment, financial commitment, credential handling, and cross-lane leakage retain explicit Stop-Gates.
- A failed task records failure evidence and releases unrelated work. It does not become completed and does not halt the program.

## Required V7.1 output contract

Every task result must contain:

- original and completed scope;
- execution and production-readiness status;
- GitHub, Supabase, and artifact evidence;
- artifact hashes;
- blockers, corrections, debt, and unknowns;
- required, passed, and failed tests;
- rollback;
- lessons learned;
- generated next tasks.

Completion must fail when evidence is empty, deliverables are missing, assignment results are unsuccessful, scope is wrong, commits do not reconcile, or readiness is unsupported.

## Program promotion gate

The BOW-001 through BOW-004 program is promotable when:

- BOW-001 host hardening passes sustained operation and rollback tests;
- BOW-002 registry defects are closed and the full scan passes;
- BOW-003 TSL blockers close and production readiness changes from `NON_PASS`;
- BOW-004 CTJ blockers close and production readiness changes from `NON_PASS`;
- PR #29 is reconciled against the final governance head;
- all required Supabase receipts reference the exact promoted GitHub commits;
- independent validation confirms each asset and the consolidated promotion.

## Current state

**Planning authorized. Remediation workstreams should open concurrently. Production promotion remains gated by evidence and acceptance tests, not by routine conversational approvals.**
