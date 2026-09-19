# DCSE DDNA Knowledge Loop and Change Routing Amendment v1
**Task ID:** DCSE-CTJ-DDNA-V72-20260919-03
**Lane:** SC / Command Post; enterprise reuse only after classification and authorized routing
**Classification:** INTERNAL
**Status:** CANDIDATE / FAST-TRACK VALIDATION AND EXACT-CONTENT DCS PROMOTION
**Date:** 2026-09-19
**Parent:** Operative v7.2 Master Profile R5; D16 DDNA Governance
**Related controls:** D05, D16, D20, D21, D22; Issue #122; CTJ certification issues #127, #139, #142, #143
**Source:** DCS direction dated 2026-09-19, the cited conversation and prior DDNA exercise, plus preexisting canonical v7.2 doctrines.
**Scope exclusion:** Poller/communications implementation (issue #134), new production database schema, deployment, payment changes, public release, and any PS-origin content.

## 1. Purpose and preservation
Extend the existing operative D16 five-layer DDNA method with an explicit, repeatable **information/data -> provenance-preserved observation -> interpreted knowledge -> governed change -> tested outcome -> further knowledge** loop. Knowledge is both a derived output and an eligible input to future authorized inquiry; its repetition or retrieval does not confer authority. Preserve source assertions, model interpretations, decisions, outcomes, and authority as different record types. Do not silently replace D16 or the compiled R5 bytes. This document becomes an operative v7.2 amendment only after exact-content DCS promotion and D22 reconciliation.

## 2. Five layers and cross-cutting facets
Continue to evaluate Sentiment, Logic, Design, Product, and Technical as the five interpretation layers under D16. Tag, **without inventing a sixth authoritative layer**, each material finding with relevant cross-cutting facets: (a) source/author/provenance; (b) classification and lane; (c) authority/decision and lifecycle; (d) risk, contradiction, uncertainty and alternative; (e) task/relationship/dependency; (f) opportunity/reuse; (g) knowledge/change/learning outcome. Absence of a facet must remain UNKNOWN or NOT_APPLICABLE, not be fabricated.

## 3. Knowledge cycle
1. **INGEST:** identify source artifact, originating task/conversation, author/participant, original statement or observed runtime event, time, and permitted lane.
2. **PRESERVE:** distinguish raw data, source claim, user directive, evidence, model inference, independent opinion, tested result and previously promoted authority. Store or reference each in its proper D22 home. Do not paraphrase away material contradictions.
3. **EXTRACT:** evaluate D16's five layers, produce separately identifiable findings with provenance, classification, confidence and uncertainty, and distinguish WHAT HAPPENED from WHAT IT MAY MEAN.
4. **CHALLENGE:** deduplicate, compare existing enterprise records, identify counterexamples, outcomes and competing explanations. Model agreement alone is not factual verification. A prior DDNA output re-entering the loop remains derived knowledge, not a new primary source.
5. **ROUTE:** determine whether the result calls for (i) no action/retention, (ii) a candidate knowledge record, (iii) an executable task or defect correction, (iv) an amendment to an EXISTING canonical artifact/section, or (v) an explicitly justified new artifact when no existing owner fits. Resolve the target author or accountable document owner and the correct destination BEFORE generating another standalone specification.
6. **VALIDATE:** verify source authenticity, owner/authority, source-to-rule semantics AND observable control outcome. For a MUST/SHALL rule, test whether the system actually prevents the disallowed state; finding the sentence in a document does not satisfy control validation. Preserve functional independence or separate-actor requirements under D05.
7. **PROMOTE/APPLY:** fast-track routing, preparation, independent review and administrative synchronization. Exact-content authority for doctrine or other governing changes remains with DCS Level 0 or an express scoped delegation under D05. A DCS directive to fast-track the WORK is not approval of unreviewed normative text. Apply only authorized content; preserve prior promoted identities and rollback.
8. **FEEDBACK:** record actual tests, downstream impact, release/defect outcome, and new contradictions as a new provenance-linked input. Explicitly mark the next cycle's source as derived/observational rather than authoritative by recursion.

## 4. Material knowledge/change routing record
Every proposed normative or reusable material change SHALL carry:
- candidate_id, task_id, source_artifact_ref, originating conversation/record and exact quote/observation reference;
- statement_author or originating participant, capturing agent and responsible destination owner (distinct roles);
- lane, entity, classification, sharing restrictions and PS/secret screening result;
- evidence type, D16 signal layer(s), optional cross-cutting facets, finding, inference/uncertainty, contradictions and candidate change;
- selected existing canonical destination repository/path/section plus verification time, or a documented WHY_NEW reason;
- affected systems, products, consumers, dependencies and backward-compatibility risk;
- validation criteria including a negative/counterexample test, independent reviewer/function, evidence/receipt path and rollback;
- candidate, validated, approved, operative, distributed and deployed states represented SEPARATELY, with exact version/hash and DCS authority reference only when actually established.
Never silently convert an attributed statement, model output, claimed delivery, commit, message ID or registry row into verified runtime behavior or approval.

## 5. Model exploration and execution separation
During early DDNA learning runs, invite multiple *available and authorized* model perspectives without assigning permanent model personalities or specialties. Preserve individual reasoning outputs and disagreements before synthesis. Compare four optional consultation modes: direct single participant; independent parallel interpretations; scoped specialist division; adversarial validation. Mode selection shall later use observed performance, access, cost, confidentiality and reliability evidence, not model-name stereotypes. No multi-model exchange is a prerequisite for CTJ product completion or this DDNA amendment. The existing communications integration remains deferred.

## 6. CTJ certification and reporting
Use the active CTJ family completion task, Issue #127, and existing candidate product sources as the first bounded learning case without rebuilding validated product cores. For each material CTJ decision/correction/test, create a provenance-linked DDNA candidate and route only necessary improvements to the existing CTJ semantic object/product documentation, D16/D20 or the appropriate operative document. Protect public-product copy from internal-only terminology, model conjecture, protected-lane source material and unapproved commerce claims. A candidate product build, passing CI, unmerged PR, public URL or working ZIP does not prove package, price, entitlement, payment, post-checkout delivery or public-release approval.
Each material status report SHALL distinguish newly observed activity, verified commit/PR/runtime evidence, completed and uncompleted product gates, DDNA candidates, DCS decisions required, and next executable action; preserve report time and source freshness. Do not describe GitHub discovery alone as product or DDNA completion.

## 7. Deterministic acceptance checks for this amendment
A. Input is a model claim without primary evidence -> retained as CLAIM/UNKNOWN, not VERIFIED.
B. Input is a repeated knowledge summary -> deduplicated with lineage; repetition never creates authority.
C. Input is a DCS correction -> original behavior, correction and desired behavior retained; candidate routed to the correct existing rule and negative behavior test.
D. Input contains PS-origin or secret material -> stop affected cross-lane propagation; no public/RAG/general-DDNA spill.
E. Proposed amendment has an existing canonical owner -> target that owner/section; no unexplained parallel document.
F. A written SHALL is present but prohibited behavior is still possible -> validation FAIL, no completion or promotion.
G. CTJ product PR passes CI while paid delivery untested -> product-core PASS remains distinct from commercial release UNKNOWN/GATED.
H. Communications transport is unavailable -> permitted local/source DDNA and CTJ completion work continues; no false delivered/ACK claim.
I. Candidate approval not linked to exact identity -> no ACTIVE_RATIFIED or production cutover claim.
J. Approved artifact exists but registry/runtime mirror differs -> DRIFT/UNSYNCHRONIZED until D22 receipt and cross-verification.

## 8. Promotion and receipt contract
D05 gates: freeze this exact candidate; inspect D16/D20/D21/D22 conflicts; independently reperform checks A-J on frozen source; record source/version/hash, finding dispositions, lane/secret scan, rollback and attributable validation receipt; obtain DCS Level 0's exact-content approval or exact scoped standing promotion authority; merge through required GitHub controls; reconcile D16/index/manifest references where applicable, DCSE-DDNA authority/artifact registry and Tribunal receipt under D22; verify actual distribution to intended consumers. Until these conditions are met, this amendment remains CANDIDATE and the already-promoted D16 is controlling. Immediate exploratory DDNA capture within existing D16 authority may proceed without awaiting new transport or full RAG cutover.

**Rollback:** preserve existing D16 v7.2 and current promoted runtime identities; if this candidate is rejected or fails tests, close without merging and leave their operative state unchanged. If later promoted, rollback requires DCS-authorized supersession/reversal with lineage and cross-system verification.
