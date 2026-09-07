# DCSE v7.2 Completion Evidence Collector and Closure Integrity Directive

**Directive ID:** DCS-DIR-20260906-002  
**Status:** ACTIVE DCS EXPRESS DIRECTIVE  
**Authority:** DCS Level 0  
**Effective Date:** 2026-09-06  
**Classification:** CONFIDENTIAL / INTERNAL  
**Lane:** DCSE / ALL GOVERNED LANES  
**Parent Authority:** DCSE Master Profile v7.2 R5, OPERATIVE

## 1. Purpose

This directive closes a runtime-governance gap exposed during Task `DCSE-GOV-20260906-004`: execution completed across GitHub and DCSE-DDNA, but stale status text remained in dependent artifacts and the human reviewer was not immediately presented with a compact, direct evidence set.

Substantive DCSE work must therefore close with both:

1. **Closure Integrity Validation**, using forward chaining, backward chaining, inductive/deductive review, contradiction scanning, and affected-artifact reconciliation; and
2. a **Completion Evidence Collector (CEC)** that presents the human reviewer with immediate, orderly evidence of what was produced, changed, validated, and left unresolved.

## 2. Closure Integrity Validation

Before a substantive task may be reported COMPLETE, the executor SHALL:

1. start from the original request and declared exit criteria;
2. forward-chain through every executed action and produced artifact;
3. backward-chain from the claimed final state to the evidence required to prove that state;
4. identify every dependent artifact, registry, index, manifest, runtime record, deployment, receipt, or status label that should have changed because of the task;
5. compare those dependent states for contradictions or drift;
6. reconcile stale status, path, version, checksum, authority, deployment, or runtime references within authorized scope;
7. distinguish what was directly verified from what remains inferred or pending;
8. stop a COMPLETE claim when a material dependent state remains contradictory, inaccessible, unverified, or unreconciled.

A task is not complete merely because the primary artifact was created or the principal write succeeded.

## 3. Completion Evidence Collector (CEC)

At closeout of every substantive task, the executing model/agent SHALL assemble a human-review evidence packet in the user-facing response. For governed artifact work, the same evidence packet or an evidence-zone reference SHALL also be preserved in Tribunal or the designated evidence system.

The CEC SHALL collect only task-relevant evidence and SHALL present it in a compact, reviewable order.

### 3.1 Required Evidence Packet Fields

- Task ID
- final task state: COMPLETE, COMPLETE WITH FINDINGS, PARTIAL, or BLOCKED
- original requested outcome
- deliverable/artifact name
- current authoritative path or destination
- direct human-review link when one exists
- commit, deployment, version, or runtime identifier as applicable
- material SHA-256/checksum when governed identity requires it
- runtime/database/registry evidence when the task changed runtime state
- preview or production URL when deployment/rendering was part of the task
- validation performed and result
- downstream/dependent-artifact reconciliation result
- unresolved finding or remaining gate
- required human decision, if any

### 3.2 Evidence Quality Rules

The executor SHALL:

- prefer direct links to the exact artifact, commit, deployment, record, or review surface;
- avoid forcing DCS to reconstruct evidence from narrative descriptions;
- separate local-download links from canonical-system links;
- never fabricate a link, commit, hash, deployment, registry write, or validation result;
- identify evidence that could not be surfaced or independently verified;
- exclude credential values, tokens, private keys, connection strings, MFA/recovery data, and other secrets;
- avoid exposing protected PS material in an unauthorized destination;
- keep the packet concise enough for rapid human review while complete enough to verify the closeout claim.

## 4. Cross-System Tasks

When a task spans multiple systems, the CEC SHALL collect evidence by system. Example classes include:

- GitHub: exact file path, commit link, file/blob identity, diff or comparison when material;
- Supabase/database: project/system name, schema/table/record identity, safe query result or receipt, never secret credentials;
- Tribunal: evidence record path/link and status;
- Vercel/Netlify/Wix: project/deployment/preview/production evidence as applicable;
- local artifacts: downloadable file link plus canonical destination when promoted;
- RAG/DDNA: corpus/registry identity, ingestion/retrieval/evaluation result as applicable.

## 5. D21 Integration

This directive supplements the D21 task runtime and DCL closeout requirements.

For every substantive task:

- Preflight Validation remains required before execution;
- the D21 Doctrine Consideration Log remains required through closeout;
- `completion_evidence_packet` becomes a required closeout element;
- `closure_integrity_validation` becomes a required validation result;
- task identity and parent/child lineage remain preserved across handoffs.

If the executing surface cannot perform or surface the required evidence collection, it SHALL report the task as PARTIAL or UNSYNCHRONIZED for the affected claim rather than silently declaring completion.

## 6. Human Review Standard

The evidence packet is designed so DCS can rapidly answer:

1. What was supposed to happen?
2. What actually changed?
3. Where is each output?
4. Can the output be opened immediately?
5. What commit/version/hash/runtime record proves it?
6. What validation was performed?
7. Were dependent artifacts reconciled?
8. What remains pending or requires human review?

The human reviewer should not need to search multiple prior messages to locate basic proof of completion.

## 7. Status and Authority

This directive is effective immediately by express DCS Level 0 instruction. It supplements D21/D22 and does not replace the operative v7.2 R5 controller. Historical source doctrine labels remain provenance under the operative v7.2 authority model.

Formal doctrine incorporation may occur in a later controlled controller revision. Until then, this registered express directive is the controlling v7.2 rule for completion evidence collection and closure integrity.

**Structure Precedes Scale.**
