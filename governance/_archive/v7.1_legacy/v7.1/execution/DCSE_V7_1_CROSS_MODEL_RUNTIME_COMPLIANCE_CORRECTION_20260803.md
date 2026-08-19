# DCSE V7.1 Cross-Model Runtime Compliance Correction

Date: 2026-08-03
Authority: DCS
Primary doctrine: D21 Doctrine Runtime Engine
Supporting doctrines: D03, D04, D05, D22
Disposition: SYSTEMIC GAP CONFIRMED

## Executive determination

V7.1 was present as a governance label, branch name, and policy reference, but runtime compliance was not consistently instantiated or proven for ChatGPT, Codex, Claude Code, Qwen Coder, Gemini, local models, or supporting agents.

No runtime may be treated as V7.1-compliant solely because:

1. a prompt mentions V7.1;
2. a task row contains a doctrine list;
3. work occurs on a V7.1-named branch;
4. an agent states that governance was loaded;
5. another agent approves the narrative.

V7.1 compliance requires a machine-verifiable admission receipt created before substantive execution.

## Accountability finding

DCS, acting in the co-founder, Chief Architect, and strategist function, did not consistently emit a D21 Doctrine Consideration Log or prove the loaded authority hashes before directing and evaluating BOW-001 through BOW-004. This is an orchestration design failure, not merely a worker-model error.

Worker runtimes also produced or evaluated work without a uniform admission contract. Responsibility is therefore distributed:

| Layer | Failure |
|---|---|
| Strategic orchestration | V7.1 authority was assumed from context instead of proven at runtime |
| Task control | task labels and doctrine arrays were accepted without doctrine-load receipts |
| Poller | claim eligibility did not require a V7.1 admission receipt |
| Worker models | narrative compliance claims were not bound to source hashes |
| Review | reviewers assessed evidence without first proving their own independent V7.1 admission |
| Promotion | GitHub and Supabase reconciliation did not prove doctrine execution |

## Evidence classification

### Verified

- The authoritative doctrine set is D01 through D22.
- D21 and D22 were omitted from portions of the prior runtime path.
- Existing agent registry records do not contain a verified V7.1 admission receipt or doctrine-source hash set for the principal models.
- Earlier BOW policy records used incomplete doctrine routes.
- Qwen Coder is restricted to bounded sandbox work and cannot supply host-operation proof.

### Likely

- Claude Code and other models followed portions of V7.1 because their tasks referenced its concepts.
- Some prior outputs remain technically useful even though governance execution was not proven.
- The same label-without-runtime defect may affect work outside BOW-001 through BOW-004.

### Unknown

- Which prior sessions independently loaded every applicable doctrine before execution.
- Whether prompt wrappers used by every runtime contained identical canonical V7.1 content.
- Whether all model-generated review receipts were produced after an independent doctrine admission.

Unknown is not treated as PASS.

## Mandatory V7.1 runtime admission gate

Before any model claims, executes, reviews, promotes, or closes a governed task, it must produce:

1. runtime identity and capability class;
2. task key, lane, product target, and execution role;
3. V7.1 manifest path, commit, and content hash;
4. D21 and D22 source paths and hashes;
5. all considered doctrines with activate, conditional, or exclude decisions;
6. D13 and D14 lane-firewall decision;
7. required inputs and verified access;
8. authorized actions and prohibited actions;
9. Stop-Gates, Pass-Gates, retry limits, fallback route, and rollback rule;
10. output schema, evidence locations, and reconciliation targets;
11. admission disposition of ADMIT, ADMIT_WITH_LIMITS, or DENY;
12. timestamp and durable receipt reference.

A task cannot move from planned to running without ADMIT or ADMIT_WITH_LIMITS. A reviewer must create a separate admission receipt. Model identity is not a substitute for independence, and model unavailability is not itself a Stop-Gate.

## Cross-model enforcement

| Runtime | Permitted role after admission | Additional control |
|---|---|---|
| ChatGPT | strategy, orchestration, synthesis | must emit D21 DCL and cannot self-certify technical execution |
| Codex | implementation, repository and independent review | execution and review require separate role receipts |
| Claude Code | host and repository execution | host claims require logs, heartbeat, outputs and source reconciliation |
| Qwen Coder | bounded sandbox implementation and tests | no poller, host, GitHub, or Supabase claim without actual tool evidence |
| Gemini | research and synthesis | source provenance and no operational-completion claims without tools |
| Local models | bounded extraction or challenge | no autonomous promotion; provenance and output capture mandatory |
| Database, GitHub and Tribunal agents | specialized operations | each mutation requires task linkage and reconciliation receipt |

## Prior-work correction rule

Previous artifacts remain immutable historical evidence. Each is classified:

- V7.1 VERIFIED: admission receipt and complete doctrine evidence exist.
- TECHNICALLY USABLE, GOVERNANCE UNVERIFIED: output may seed a rerun but cannot satisfy the V7.1 gate.
- SUPERSEDED: corrected output exists.
- INVALID: claim conflicts with authoritative evidence.

BOW-001 through BOW-004 are classified TECHNICALLY USABLE, GOVERNANCE UNVERIFIED until their strict-runtime reruns complete.

## Poller admission algorithm

1. Read task and dependency state.
2. Select a capability-eligible runtime.
3. Require a fresh V7.1 admission receipt.
4. Reject duplicate active assignment for the same runtime or task.
5. Claim atomically.
6. Execute within admitted scope.
7. Require nonempty outputs and evidence.
8. Record review admission and validation.
9. Apply D05 Pass-Gate.
10. Reconcile GitHub, Supabase, heartbeat, and successor release.

If admission fails, the poller records the exact failed condition and selects an eligible fallback. It does not invent progress or wait for a named model when another admitted runtime can perform the task.

## Corrective actions

1. Apply the admission requirement to all Baseline Set B tasks.
2. Add V7.1 admission status fields to every active agent registry entry.
3. Treat missing admission as not admitted, not implicitly compliant.
4. Audit active V7.1 tasks for incomplete doctrine paths.
5. Rerun BOW-001 through BOW-004 using the strict runtime contract.
6. Require separate executor and reviewer admission receipts.
7. Block promotion when admission, evidence, or reconciliation receipts are absent.
8. Preserve this discovery as a D21 runtime incident and lesson learned.

## Controlling lesson

Governance is not active because it is named. Governance is active only when the runtime proves authority, applicability, execution constraints, evidence, gate decisions, and reconciliation.
