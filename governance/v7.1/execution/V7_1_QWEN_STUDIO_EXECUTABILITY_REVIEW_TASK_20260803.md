# V7.1 Qwen Studio Doctrine Executability Review Task

Date: 2026-08-03
Task key: V7_1_QWEN_STUDIO_DOCTRINE_EXECUTABILITY_REVIEW
Lane: SYSTEM
Primary doctrine: D21
Supporting doctrines: D03, D04, D05, D06, D22
Execution mode: MP-Full

## Objective

Review every document in the V7.1 Canonical Governance Package Manifest and determine whether its requirements are executable runtime instructions or merely descriptions, aspirations, outlines, examples, or task lists.

## Qwen capability boundary

Qwen Studio is admitted for document analysis and structured output only.

Qwen must not claim:

- GitHub commits or branch changes;
- Supabase queries, writes, heartbeats, or task claims;
- Windows-host execution;
- poller activity;
- tests not actually performed through available tools.

The review is valid only when its output is attached to this task and independently reconciled by Codex.

## Required review method

For every Master Profile, doctrine, registry, manifest, authorization, gate, addendum, runtime contract, and correction document:

1. Read the complete document.
2. Record filename, internal version, status, source path, and Git blob SHA.
3. Identify every normative statement using MUST, SHALL, REQUIRED, PROHIBITED, STOP, PASS, PROMOTE, ROLLBACK, RETRY, or equivalent language.
4. Classify each normative statement:
   - EXECUTABLE;
   - PARTIALLY_EXECUTABLE;
   - DESCRIPTIVE_ONLY;
   - CONFLICTING;
   - OBSOLETE;
   - NOT_APPLICABLE.
5. For executable rules, identify:
   - trigger;
   - required inputs;
   - actor or runtime;
   - ordered action;
   - output;
   - evidence;
   - Pass-Gate;
   - Stop-Gate;
   - retry or fallback;
   - rollback or recovery;
   - durable receipt.
6. Identify unresolved pronouns, ambiguous actors, undefined terms, missing paths, stale versions, local-only links, circular authority, and impossible actions.
7. Convert every DESCRIPTIVE_ONLY or PARTIALLY_EXECUTABLE requirement into a proposed executable rule.
8. Identify cross-document conflicts and apply the V7.1 source-authority hierarchy without silently choosing one.
9. Confirm the D13 and D14 PS firewall and prohibit PS content leakage into the review outputs.
10. Report missing documents, including the referenced Master Profile RC2.

## Required output files

1. QWEN_V7_1_DOCUMENT_INVENTORY.csv
2. QWEN_V7_1_EXECUTABILITY_MATRIX.csv
3. QWEN_V7_1_CONFLICT_AND_GAP_REGISTER.md
4. QWEN_V7_1_PROPOSED_EXECUTABLE_RULES.md
5. QWEN_V7_1_MASTER_PROFILE_RECONCILIATION.md
6. QWEN_V7_1_RUNTIME_TEST_SPEC.md
7. QWEN_V7_1_REVIEW_RECEIPT.json

## Matrix minimum columns

- document_id
- filename
- internal_version
- lifecycle_status
- source_path
- git_blob_sha
- rule_id
- rule_text_summary
- classification
- trigger
- inputs
- actor
- ordered_actions
- outputs
- evidence
- pass_gate
- stop_gate
- retry_fallback
- rollback_recovery
- receipt
- conflict_refs
- proposed_correction
- confidence

## Runtime test specification

Qwen must propose tests demonstrating that:

- a missing doctrine prevents admission;
- a stale hash prevents promotion;
- model unavailability invokes fallback;
- empty output references prevent completion;
- narrative claims cannot satisfy evidence;
- executor and reviewer admissions remain separate;
- PS doctrine content is not loaded in a TSL task;
- resource thresholds change routing without creating unnecessary stoppage;
- GitHub and Supabase mismatch produces a reconciliation failure;
- a valid Pass-Gate releases the eligible successor automatically.

## Pass conditions

The Qwen task passes only when:

- every package document appears in the inventory;
- every doctrine D01 through D22 has at least one matrix row;
- every normative rule is classified;
- every gap has a proposed executable correction;
- all seven output files are nonempty;
- the receipt contains file hashes and row counts;
- Qwen identifies its tool and access limits;
- Codex independently validates sample coverage, source hashes, conflict findings, and output-schema compliance.

## Failure conditions

The task fails or returns INSUFFICIENT_EVIDENCE when:

- any doctrine is skipped;
- the review relies only on titles, summaries, or the package manifest;
- outputs contain fabricated tool activity;
- files are empty or unavailable;
- source hashes are missing;
- findings are not traceable to documents;
- descriptive recommendations are presented as implemented rules.

## Resource controls

- default effort: MEDIUM;
- mechanical inventory and CSV formatting: LOW;
- authority conflicts, gate conflicts, PS firewall, and final synthesis: HIGH;
- bounded batches: D01-D06, D07-D12, D13-D17, D18-D22, authority and V7.1 controls;
- emit a checkpoint receipt after every batch;
- model or session unavailability triggers resumption from the last verified checkpoint.

## Independent validation

Codex reviews Qwen's outputs only after Qwen submits all required files. Codex may return APPROVE, APPROVE_WITH_CORRECTIONS, REJECT, or INSUFFICIENT_EVIDENCE. Qwen's self-assessment cannot promote doctrine changes.
