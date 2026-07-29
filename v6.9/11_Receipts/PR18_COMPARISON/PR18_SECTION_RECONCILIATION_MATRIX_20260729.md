# PR #18 Doctrine Section Reconciliation Matrix

Date: 2026-07-29
Mode: local doctrine reconciliation; GitHub read-only
Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`
Branch: `feature/d03-d06-d20-reconciliation`
Draft PR: `#18`
PR head: `1ea507a47a189fefe066bc983a4c0e47f0c351de`
Gate: **HOLD ON MERGE**

## Executive determination

PR #18 is safely contained as a draft but is not ready to merge. D03, D04, D05, and D06 are substantive rewrites, not line-preserving reconciliations. The GitHub-created D20 does not duplicate the established D20's subject matter; it collides with the established D20 identifier and filename slot.

The established local D20 is the comparison source and must remain intact. The GitHub source-authority doctrine should not be merged into product-assembly D20. If retained, it should be renumbered to the currently unallocated D22 and remain a candidate until separately reviewed and promoted.

No copy wave, source mutation, GitHub write, Supabase mutation, promotion, or merge was performed.

## Evidence set

### Local governing comparison sources

The operational and immutable-root copies of D03-D06 are exact SHA-256 matches.

| Doctrine | Local operational path | Local SHA-256 | Verbatim local status |
|---|---|---|---|
| D03 | `doctrine\v6.9\01_Doctrine\D03_AI_Orchestration.md` | `083DB9EEB16B86565E7544C6D4F9314A37DAFCA921C3572472A8C928184BCA3D` | DCSE Authorized version Pending Approval |
| D04 | `doctrine\v6.9\01_Doctrine\D04_Command_Post_Communications.md` | `850CB096B1EDE8A1539AFC201F0922A58C9F086AE0F4282091CBFF139B892394` | DCSE Authorized version Pending Approval |
| D05 | `doctrine\v6.9\01_Doctrine\D05_Baseline_Promotion.md` | `C4912B2BB261D3CA3F1F27AE3289389D9852E65E2B141157E157D00EBEC4BAD0` | DCSE Authorized version Pending Approval |
| D06 | `doctrine\v6.9\01_Doctrine\D06_File_System.md` | `74C03A8212BD89F2EE200F7713876E8E5ABE03125D9F282D4967C93913DCCAB0` | DCSE Authorized version Pending Approval |
| D20 | `doctrine\v6.9\01_Doctrine\D20_Product_Assembly_Methodology.md` | `902EC78EA0184E8C1576BE5503EC216B5013C431F9B38DFD198795D3BDCE9B56` | DCSE Authorized Pending DCS Approval |

### GitHub PR #18 candidate sources

| Doctrine | GitHub path | GitHub SHA-256 | GitHub status |
|---|---|---|---|
| D03 | `v6.9/01_Doctrine/D03_AI_Orchestration.md` | `D9AD3B0EE24770F1B973804D9231B6975233D6B8D84FFEC093B818E40CFCF292` | CANDIDATE FOR PROMOTION |
| D04 | `v6.9/01_Doctrine/D04_Command_Post_Communications.md` | `D0CEB08C432A62896DE7A9221DB74E3F1CEAECF9B6D095B16CBD8CBEBB5AA685` | CANDIDATE FOR PROMOTION |
| D05 | `v6.9/01_Doctrine/D05_Baseline_Promotion.md` | `F2A56C2DBC971EF956051D33FE5A48F461DC75D50128B7DD6CAFDB561E5D35DC` | CANDIDATE FOR PROMOTION |
| D06 | `v6.9/01_Doctrine/D06_File_System.md` | `9CFD53A4602E271DCD018EEC00AE47FD31731E2D5B8099A297B5AF9FB6E63963` | CANDIDATE FOR PROMOTION |
| D20 candidate | `v6.9/01_Doctrine/D20_Source_Authority_Runtime_Distribution.md` | `9510321AFC179E90D7B36B7A3DF879B5439BADC678B8C7177EEDCC83E0651BB7` | CANDIDATE FOR PROMOTION |

GitHub hashes were computed from the full UTF-8 file content fetched from the PR head, not from truncated patches.

## D20 status resolution

The prior statement `D20 remains ACTIVE, pending DCS approval` is not a valid controlled status.

### Evidence

1. The prior D20 hash `4A04DF0558E37663CDBAD826ED4FB220A9C415BCBAADD3B31F9534AAE32A82FB` appears in the 2026-07-26 D08 RC3 baseline receipt with role `COMPATIBILITY_MIRROR`, not as a D20 promotion receipt.
2. The operational registry reconciliation preserved D20 as `PENDING`.
3. The 2026-07-28 Tribunal record states `MULTI_MODEL_REVIEW_IN_PROGRESS`, consensus `INCOMPLETE`, with 4 of 12 receipts submitted and DCS Level 0 ratification still required.
4. The original Claude D20 PROMOTE recommendation referenced the superseded `4A04...CCE6` hash.
5. The corrected `902E...9B56` evidence packet requires a refreshed Claude receipt, Qwen review, and final DCS Level 0 decision.
6. No Git history entry or completed local ratification receipt proves that either D20 hash reached `ACTIVE_RATIFIED`.

### Controlled conclusion

| Question | Determination |
|---|---|
| Last promoted D20 version | **None proven.** No completed DCS Level 0 ratification record was found. |
| Prior `4A04...CCE6` version | Pre-correction candidate/compatibility mirror; promotion review incomplete; not proven promoted. |
| Current `902E...9B56` version | **CANDIDATE PENDING PROMOTION.** It is the complete local comparison source and current working candidate. |
| Does a prior promoted D20 remain controlling? | **No prior promoted D20 is proven.** D05, D06, D11, and D07 remain the governing source doctrines for the product lifecycle pending D20 ratification. |
| Earlier `ACTIVE` inventory label | Superseded for promotion-status purposes by this evidence-bound correction. It described operational presence, not ratified authority. |

## Line-by-line comparison summary

Counts use a whitespace-preserving line LCS after trimming only line-end whitespace. Blank matching lines are included in the LCS total; the nonblank column shows substantive verbatim preservation.

| Doctrine | Local lines | GitHub lines | LCS lines | Verbatim nonblank lines | Local-only lines | GitHub-only lines | Result |
|---|---:|---:|---:|---:|---:|---:|---|
| D03 | 322 | 92 | 30 | 4 | 292 | 62 | Wholesale rewrite |
| D04 | 272 | 115 | 37 | 3 | 235 | 78 | Wholesale rewrite |
| D05 | 50 | 130 | 14 | 1 | 36 | 116 | Replacement plus conflicting promotion model |
| D06 | 239 | 123 | 38 | 3 | 201 | 85 | Wholesale rewrite |
| D20 | 360 | 171 | 47 | 1 | 313 | 124 | Different doctrine occupying the same identifier |

## Section-by-section reconciliation

### D03 - AI Orchestration

| Local section | GitHub section | Relationship | Required disposition |
|---|---|---|---|
| 1 Model Delegation Matrix | 2 Current Model Governance Matrix | Partial subject overlap; assignments and system roster differ. | Preserve local matrix; review modern model rows as candidate additions, not replacements. |
| 2 Minimum Effective Context | 4 Minimum Effective Context | Partial overlap. GitHub adds explicit PS separation and materiality threshold. | Preserve local controls; add only non-conflicting PS/materiality wording. |
| 3 Operational Mode Switching | No direct equivalent | Local-only execution routing. | Retain. |
| 4 Prompt Wrappers and Metadata Headers | 3 Required Task Header | Partial overlap; field sets differ materially. | Retain local wrappers and add reviewed authority/access/secret fields. |
| 5 Instruction Attachment and Folder Routing | No direct equivalent | Local-only attachment and restricted-source controls. | Retain. |
| 5.3 Missing File Protocol | 9 Stop-Gates | Conflict: local mandates halt, JSON error packet, and STOPGATE; GitHub narrows missing-source stops by materiality. | Preserve local hard protocol until a separately approved amendment defines safe exceptions. |
| 6 Universal Session Open Protocol and subsections | 7 Session Open Protocol | Partial overlap; GitHub is much shorter and omits constitution load, source routing table, doctrine path, and MEC declarations. | Retain complete local protocol; add only non-conflicting branch/scan/exit-state items. |
| 7 Forward Thinking Enforcement | No direct equivalent | Local-only DDNA behavioral layer. | Retain. |
| 8 AI Model Update Monitoring | No direct equivalent | Local-only capability monitoring and doctrine update pathway. | Retain. |
| No direct equivalent | 5 Execution Authority | GitHub-only separation of discussion, direction, execution, verification, and promotion. | Candidate additive section. |
| No direct equivalent | 6 Database and Credential Work | GitHub-only explicit credential boundary. | Candidate additive section, subject to D15/D21 consistency. |
| No direct equivalent | 8 Voice and Dictation Control | GitHub-only instruction-interface safeguard. | Candidate additive section. |

Proposed canonical D03: local hash `083D...BCA3D` remains the governing comparison source. PR D03 must be reconstructed as an additive candidate based on that full local file.

### D04 - Command Post Communications

| Local section | GitHub section | Relationship | Required disposition |
|---|---|---|---|
| 1 Dual Inbox Architecture; 1.1-1.3 | 2 Communication Layers; 3 Packet Schema | Partial overlap. GitHub adds Supabase runtime target and hash fields but omits operational detail. | Preserve local inbox paths, daemon distinction, and schema; add reviewed Supabase/hash fields. |
| 2.0 Model-to-Source Routing Table | 5 Model Source Routing | Partial overlap; GitHub removes the detailed per-model access table. | Retain detailed local routing table. |
| 2.10 v69 Candidate Mirror Rule | 4 Repository Map and D20 source model | Material conflict: local says the local Hub is working authority and `v69` is candidate mirror after approval; GitHub makes GitHub the canonical artifact layer. | Do not replace local hierarchy until a separately ratified source-authority doctrine resolves it. |
| 2.2 Branch Strategy | No direct equivalent | Local-only branch controls. | Retain. |
| 2.3 Push Protocol; 2.4 Pull Protocol | 6 GitHub Write Protocol | Partial overlap; GitHub compresses and changes the process. | Retain local detailed controls; review blob-SHA and post-write runtime-reference items as additions. |
| 2.5 Conflict Resolution | 7 Conflict Resolution | Partial overlap. | Reconcile additively; preserve no-silent-overwrite rule. |
| 2.6 What Never Goes Into Git | 9 No-Git Exclusions | Partial overlap. | Preserve the more restrictive union without importing PS content. |
| 2.8 Git-Tribunal Concurrency Rule | 8 GitHub and Tribunal Concurrency | Direct conflict: local requires a single atomic operation with no exceptions; GitHub allows receipt immediately after commit. | Local hard rule controls pending explicit amendment. |
| 2.9 Poller Daemon Sync | No direct equivalent | Local-only operational schedule and sync behavior. | Retain. |

Proposed canonical D04: local hash `850C...2394` remains the governing comparison source. PR D04 must preserve all detailed operational controls.

### D05 - Baseline and Promotion

| Local section | GitHub section | Relationship | Required disposition |
|---|---|---|---|
| 1 Baseline System | 2 Baseline Standard | GitHub expands scope and metadata. | Preserve local baseline identity and 06_Baselines rule; review expanded fields as additions. |
| 2 Promotion Protocol | 3-7 Promotion States and Rules | Material conflict: local says only DCS Level 0 may ratify promotion; GitHub authorizes automatic promotion in some workflows. | Local Level 0 rule controls. Remove automatic promotion from this candidate unless separately ratified as a constitutional amendment. |
| 2 Modified-after-promotion rule | 7 Modification After Promotion | Substantive match: both revert material changes to candidate and retain prior promoted authority. | Preserve; GitHub wording is a useful clarification. |
| Error-Catch Protocol | No direct equivalent | Local-only halt/log/STOPGATE behavior. | Retain. |
| No direct equivalent | 6 Promotion Receipt | GitHub-only expanded receipt schema. | Candidate additive section, with `promotion_type=automatic` removed pending authority decision. |
| No direct equivalent | 8 Drift Control; 9 Rollback | GitHub-only useful controls. | Candidate additive sections after source hierarchy is resolved. |

Proposed canonical D05: local hash `C491...BAD0` controls the comparison. The PR version is not mergeable because its automatic-promotion rule contradicts the current Level 0 gateway.

### D06 - File System and Device Governance

| Local section | GitHub section | Relationship | Required disposition |
|---|---|---|---|
| 1 Hub Layout; 1.1 Candidate Mirror Scope | 2 Controlled Storage Layers; 3 Source Placement; 4 Hub Structure | Material overlap and conflict. GitHub changes the authority model from local working Hub/candidate mirror to GitHub canonical artifact plus local audit mirror. | Preserve local hierarchy until source-authority doctrine is separately ratified. |
| 2 Segmented Search and Routing | 5 Intake and Classification | Partial overlap. | Preserve both through additive reconciliation. |
| 3 Root Folder Classification | No direct equivalent | Local-only root governance matrix. | Retain. |
| 4 Device Governance Matrix | 8 Device and Executor Controls | Partial overlap; GitHub omits actual node roles. | Retain matrix; add explicit revocable-access fields. |
| 5 File Governance Pipeline | 9 Cleanup and Deletion Pipeline | Strong conceptual overlap. | Preserve local pipeline and add backup/recovery checks. |
| 6 Intent | 1 Purpose | Partial overlap. | Retain local operational rationale. |
| 7 Setup and SC Lane Structures | No direct equivalent | Local-only implementation and lane placement. | Retain. |
| 8 Regulations | 5-10 | Partial overlap; GitHub reorganizes and omits several detailed rules. | Preserve local regulations; add non-conflicting secret/PS rules. |
| 9 Suggested Maintenance | No direct equivalent | Local-only cadence. | Retain. |
| 10 Ongoing Upgrade | No direct equivalent | Local-only version, D15, lane, agent-scope, and deprecation controls. | Retain. |
| No direct equivalent | 6 PS Isolation; 7 Secrets and Credentials | GitHub-only explicit firewall wording. | Candidate additive sections. |
| No direct equivalent | 10 Duplicate and Drift; 11 Backup and Recovery | GitHub-only explicit drift and recoverability wording. | Candidate additive sections after D20/D22 identity is resolved. |

Proposed canonical D06: local hash `74C0...CAB0` remains the governing comparison source. PR D06 must be rebuilt as an additive candidate, not accepted as a replacement.

### D20 identity collision

| Established local D20 | GitHub-created D20 | Finding |
|---|---|---|
| Product Assembly Methodology | Source Authority and Runtime Distribution | Different domains and different lifecycle purpose. |
| Six phases: Intake, Build, Test, Package, Promote, Deploy | Authority hierarchy, GitHub/Supabase source model, runtime doctrine records, model distribution, drift | No functional duplication. |
| Live Preview Mandate; testing depth; cybersecurity quick reference; trigger mechanism; tier access | Canonical artifact identity; constitutional runtime registry; operational Supabase separation; retrieval verification | Both contain promotion/hash language only at a generic cross-reference level. |
| 360 lines | 171 lines | Only 1 substantive nonblank line is preserved verbatim. |

Determination:

- The GitHub-created D20 must **not** replace or merge into established D20.
- Established local D20 keeps identifier D20 and filename `D20_Product_Assembly_Methodology.md`.
- Preserve every unique established D20 provision: six-phase pipeline, phase quality gates, Live Preview Mandate, cybersecurity checklist, product-type testing depth, triggers, sub-pipeline integration, tier access, and error-catch protocol.
- The GitHub source-authority text may remain a separate candidate only after renumbering. D22 is presently unallocated in the non-protected doctrine library, so the recommended candidate identity is `D22_Source_Authority_Runtime_Distribution.md` / `DCSE-D22`.
- Before any D22 promotion, deconflict it with D04 source routing, D05 promotion, D06 placement, D15 database authority, D21 runtime/retrieval controls, and the Access Tiers registry.

## Material conflicts

**Conflict count: 10**

1. D20 identifier collision: two unrelated doctrines claim `DCSE-D20`.
2. D20 lifecycle contradiction: the local audit said ACTIVE while all direct promotion evidence remains pending/incomplete.
3. D05 promotion authority: Level 0-only ratification versus candidate automatic promotion.
4. D06 source hierarchy: local Hub as working authority/candidate GitHub mirror versus GitHub as canonical artifact layer.
5. D04 Git/Tribunal timing: hard atomic/no-exception rule versus receipt at or immediately after commit.
6. D03 missing-doctrine behavior: unconditional local halt/log/STOPGATE versus GitHub materiality-based continuation.
7. D03 preservation failure: local prompt wrappers, attachment routing, DDNA mindset, and model-update protocol were omitted.
8. D04 preservation failure: detailed branch, pull/push, routing, poller, and concurrency controls were omitted or compressed.
9. D06 preservation failure: root/device matrices, setup, maintenance, upgrade, and deprecation controls were omitted.
10. Index regression: PR index removes registered D17-D21 lineage, assigns the wrong D20, and states D17-D19 are undefined despite the current local index defining D17-D21.

## Proposed canonical version by doctrine

| Doctrine | Proposed canonical comparison version | Promotion status |
|---|---|---|
| D03 | Local `D03_AI_Orchestration.md` hash `083D...BCA3D` | Existing local status retained; PR additions remain candidate-only. |
| D04 | Local `D04_Command_Post_Communications.md` hash `850C...2394` | Existing local status retained; PR additions remain candidate-only. |
| D05 | Local `D05_Baseline_Promotion.md` hash `C491...BAD0` | Level 0 promotion gate controls. |
| D06 | Local `D06_File_System.md` hash `74C0...CAB0` | Existing local status retained; PR additions remain candidate-only. |
| D20 | Local `D20_Product_Assembly_Methodology.md` hash `902E...9B56` | CANDIDATE PENDING PROMOTION; no prior promoted D20 proven. |
| D22 candidate | Renumbered GitHub source-authority text | CANDIDATE only; separate deconfliction and promotion required. |

## Exact PR #18 file disposition

| PR file | Required action | Reason |
|---|---|---|
| `v6.9/01_Doctrine/D03_AI_Orchestration.md` | **AMEND / REBUILD** on the complete local D03; retain all local sections and add only reviewed non-conflicting candidate sections. | Current PR file drops material local controls. |
| `v6.9/01_Doctrine/D04_Command_Post_Communications.md` | **AMEND / REBUILD** on the complete local D04; retain atomic receipt rule, branch strategy, routing table, and poller controls. | Current PR file compresses or conflicts with operational controls. |
| `v6.9/01_Doctrine/D05_Baseline_Promotion.md` | **REPLACE CURRENT PR CONTENT** with a local-based additive candidate; remove automatic promotion unless separately ratified. | Current candidate conflicts with Level 0-only promotion. |
| `v6.9/01_Doctrine/D06_File_System.md` | **AMEND / REBUILD** on the complete local D06; preserve hierarchy, device matrix, pipeline, setup, maintenance, and upgrade rules. | Current PR file reverses source role and omits controls. |
| `v6.9/01_Doctrine/D20_Source_Authority_Runtime_Distribution.md` | **RENUMBER** to proposed `D22_Source_Authority_Runtime_Distribution.md`; change document ID to `DCSE-D22`; retain as candidate only. | Different doctrine; D20 is already occupied. |
| `v6.9/02_Registry/DCSE_Doctrine_Index_v6.9.md` | **REPLACE / AMEND AFTER IDENTITY FIX**; restore D17-D21, keep D20 Product Assembly, add D22 only as candidate metadata after review. | Current index regresses lineage and points D20 to the wrong file. |
| `v6.9/11_Receipts/TRIBUNAL_D03_D06_D20_RECONCILIATION_20260729.md` | **SUPERSEDE / REPLACE** with a corrected receipt after all file hashes and section decisions are final. | Current receipt claims reconciliation without the local comparison and records the erroneous D20 identity. |

## Gate decision

PR #18 is **not safe to merge** in its current form.

After the corrections above, it may safely continue as a draft review package only if:

1. the rebuilt D03-D06 candidates preserve the complete local provisions;
2. automatic promotion is removed or separately ratified;
3. source hierarchy is explicitly resolved without silently reversing current local doctrine;
4. D20 Product Assembly remains D20;
5. source-authority text is renumbered and deconflicted as a separate candidate;
6. the index restores D17-D21 and does not present D22 as promoted;
7. a new receipt records full-file hashes and the section-level reconciliation;
8. DCS Level 0 makes the applicable promotion and merge decision.

Current authorized next state: **draft correction planning only; no write or promotion authorization issued.**
