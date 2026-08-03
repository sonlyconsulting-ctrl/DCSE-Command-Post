# V7.1 BOW-003R Runtime Admission and Baseline Freeze

Date: 2026-08-03
Task: V7_1_RERUN_BOW_003_STRICT_RUNTIME
Lane: TSL
Execution mode: MP-Full
Phase: RUNTIME_ADMISSION
Disposition: ADMIT_WITH_LIMITS

## Objective

Rerun the TSL production-readiness audit under a provable V7.1 execution model while preserving the prior BOW-003 record as immutable Baseline Set A.

## Authority receipt

| Authority | Source | Verified reference |
|---|---|---|
| V7.1 manifest | canonical governance branch | Git blob 7910abd7117c6325d655e8c1530d8d72edb8c256 |
| D21 Doctrine Runtime Engine | v7.0 runtime source | SHA-256 11951EEB25ED215F61D2AF7875C2A056A6EA1D9A82F6016CC35A95211CE92341; Git blob 81a4fd326536f2fa343e7b2e9cb7ce71a8fba20e |
| D22 Source Authority and Runtime Distribution | v7.0 runtime source | SHA-256 BE24661B9FC9C6A3E5E1D5EA9ADFA706C59AB9EF5DA925904A1BF814FD561885; Git blob 165e4b9c8f984ecd5ce07b8605b59283bd21db29 |
| V7.1 cross-model correction | canonical governance branch | commit c69b70e15867e31c2656f16db68c44c1b037c812 |
| V7.1 strict runtime contract | canonical governance branch | commit f216da3b99ba796f04aceadd5fe8e79ee3bde9de |

## Source-authority exception

D21 and D22 are not physically normalized onto the V7.1 canonical branch. The live registry points to the v7.0 branch. D21 internally identifies as v6.9 active-ratified. D22 internally identifies as v7.0 candidate pending promotion.

DCS's V7.1 supersession directive is the controlling authority for this proving run. The mismatch is recorded as a D22 distribution defect.

This exception permits read-only audit and evidence reconciliation. It does not permit production promotion, deployment, destructive action, or database mutation.

## Doctrine Consideration Log

| Doctrine | Decision | Runtime purpose |
|---|---|---|
| D01 | ACTIVATE | forward risks and downstream consequences |
| D02 | ACTIVATE | forward and backward evidence chaining |
| D03 | ACTIVATE | orchestration, readiness and fail-fast |
| D04 | ACTIVATE | communications, delivery and receipts |
| D05 | ACTIVATE | immutable baseline and promotion controls |
| D06 | ACTIVATE | repository paths, evidence and integrity |
| D07 | ACTIVATE | TSL campaign and product governance |
| D08 | ACTIVATE | voice and UX consistency |
| D09 | ACTIVATE | TSL brand identity |
| D10 | ACTIVATE | personas and member-facing assets |
| D11 | ACTIVATE | application and interface governance |
| D12 | CONDITIONAL | video or media assets encountered in scope |
| D13 | EXCLUDE | PS-only doctrine; TSL lane firewall |
| D14 | EXCLUDE | PS-only doctrine; TSL lane firewall |
| D15 | ACTIVATE | Supabase, RLS, auth and database evidence |
| D16 | ACTIVATE | DDNA and source reconciliation |
| D17 | ACTIVATE | adversarial readiness audit |
| D18 | CONDITIONAL | media pipeline only when media is audited |
| D19 | CONDITIONAL | visual pipeline only when visuals are audited |
| D20 | ACTIVATE | product intake, build, test, package, promote and deploy gates |
| D21 | ACTIVATE | runtime router and DCL |
| D22 | ACTIVATE | source authority and reconciliation |

## Role admission

| Runtime | Role | Admission |
|---|---|---|
| ChatGPT/DCS | orchestration and phase control | ADMIT_WITH_LIMITS for task initiation and reconciliation |
| Claude Code | primary repository and host evidence executor | PENDING SEPARATE RECEIPT |
| Codex | independent technical reviewer | RESERVED; separate reviewer receipt required |
| Qwen Coder | bounded sandbox verification | NOT ASSIGNED at admission; ADMIT_WITH_LIMITS required if used |

## Baseline Set A freeze

The following historical evidence is immutable:

- task V7_1_BOW_003_TSL_AUDIT_INVENTORY;
- PR 36;
- merge commit 98c52c2aadb3f3948b4c1a62d1d31f8c2a09ad20;
- evidence commit 2f758b303d2383f3654b77559aa31ff024008a52;
- prior audit SHA-256 b2b6c64754e20019ee2ee6af1ae3760dab2bf88406e3046749af89b64f7c3b18;
- prior receipt SHA-256 26af21774230fb1ec58796294b0b1b3f331ca050a4dbc2dcded8973341fabc6d;
- prior disposition APPROVE_WITH_FINDINGS;
- prior product readiness NON_PASS.

Baseline Set A is technically usable but governance unverified. It cannot satisfy the new V7.1 Pass-Gate.

## Admitted scope

Stage 1 is read-only:

1. architecture;
2. application code;
3. database and RLS;
4. authentication and authorization;
5. security;
6. deployment configuration;
7. sports-data integrity;
8. UX and accessibility;
9. commercial readiness.

No production deployment, schema migration, destructive action, public release, or remediation change is admitted during Stage 1.

## Required Stage 1 outputs

- executor admission receipt;
- canonical inventory;
- dependency map;
- prior-finding reconciliation;
- verified gap and risk register;
- RLS and authorization matrix;
- sports-data readiness matrix;
- test evidence package;
- prioritized remediation backlog;
- production-readiness disposition;
- GitHub and Supabase reconciliation receipt.

## Gate decision

BOW-003R remains in RUNTIME_ADMISSION until Claude Code submits its executor receipt. Upon receipt validation, the task advances automatically to RUNNING_READ_ONLY_AUDIT. Named-model unavailability triggers capability fallback, not suspension.
