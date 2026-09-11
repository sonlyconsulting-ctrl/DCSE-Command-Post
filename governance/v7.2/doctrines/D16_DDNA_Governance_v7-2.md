# DCSE Doctrine D16: DDNA Governance

**Document ID:** DCSE-D16  
**Version:** v7.2  
**Last Modified:** 2026-09-10T15:22:00-04:00  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Classification:** INTERNAL  
**Lane:** DCSE / ALL  
**Canonical File:** D16_DDNA_Governance_v7-2.md  
**Parent Controller:** DCSE Master Profile v7.2  

## 1. Purpose

DDNA is the governed system for extracting, classifying, storing, relating, retrieving, validating, and promoting reusable signals from DCS/DCSE sessions, artifacts, builds, decisions, products, and technical work. D16 governs DDNA signal production and lifecycle. D22 governs canonical-source and persistence routing. D03 governs model/agent behavior.

This v7.2 revision preserves the five-layer DDNA model and clarifies how DDNA operates across GitHub, DCSE-DDNA Supabase, Tribunal, local working copies, storage, and runtime retrieval.

## 2. Five-Layer DDNA Model

Every qualifying DDNA extraction evaluates five distinct signal classes:

1. **Sentiment:** voice, tone, posture, corrections, confidence, friction, learning preferences, public-safe translation.
2. **Logic:** workflows, routing rules, triggers, decision architecture, gates, model assignments, QA patterns, rationale.
3. **Design:** visual systems, structural patterns, layout, typography, hierarchy, interaction and reusable design conventions.
4. **Product:** reusable product candidates, asset families, template opportunities, cross-lane reuse, productization gaps.
5. **Technical:** automation candidates, schemas, integrations, data/registry implications, file handling, APIs, infrastructure, testing, deployment and security patterns.

Signals shall be evidence-derived. DDNA shall distinguish directly observed material from inference and shall not promote a signal merely because a model generated it.

## 3. Source, Knowledge, Authority, and Retrieval Are Separate

DDNA shall maintain four separations:

### 3.1 Source Artifact
The original or governed source artifact remains in its proper canonical artifact location under D22, commonly GitHub for versioned text/code or approved object storage for large/binary material.

### 3.2 Structured DDNA Knowledge
Extracted signals, entities, relationships, provenance, classification, confidence, lifecycle, runtime status, and source references reside in the DCSE-DDNA Supabase governed data model.

### 3.3 Authority
DDNA extraction does not create enterprise authority. A DDNA record may describe or reference authority only when linked to an authorized DCS decision and the applicable canonical artifact/version/hash.

### 3.4 Retrieval Aid
Embeddings, vectors, chunks, summaries, model memory, indexes, and search results are retrieval aids. They shall preserve provenance and shall not substitute for the authoritative source.

## 4. Canonical Persistence Routing

D16 adopts D22 as controlling persistence doctrine.

| DDNA Object | Canonical Surface | Required Relationship |
|---|---|---|
| Versioned DDNA doctrine/tool/schema/template | GitHub | Supabase artifact/authority registry reference |
| Structured extracted DDNA signals | DCSE-DDNA Supabase | source artifact + provenance linkage |
| DDNA authority/controller designation | GitHub decision/designation artifact + DDNA authority registry | exact source/reference/hash where available |
| Governance-significant extraction/promotion/reconciliation evidence | Tribunal | link to source + affected registry/artifact |
| Large/binary DDNA source | Approved object storage | Supabase metadata/hash/source relationship |
| Secret value | Vault/approved secret store only | no value copied into DDNA content |

Local folders may stage, cache, execute, or audit DDNA work, but local existence alone does not make a source canonical or promoted.

## 5. Extraction Lifecycle

A qualifying DDNA run shall perform the equivalent of:

`LOAD SOURCE -> CLASSIFY SOURCE -> RESOLVE LANE/RESTRICTIONS -> EXTRACT FIVE LAYERS -> PROPOSE SIGNALS/ASSETS -> ASSIGN CONFIDENCE/LIFECYCLE -> LINK PROVENANCE -> WRITE STRUCTURED DDNA -> REGISTER SOURCE/RELATIONSHIPS -> ISSUE MATERIAL RECEIPT WHEN REQUIRED`

If source authority, lane, provenance, or restrictions cannot be resolved, the affected item shall remain candidate/unknown/blocked rather than being silently promoted.

## 6. Reuse Before Redesign Integration

D16 is an enterprise discovery surface for D20 Reuse Before Redesign.

DDNA shall support discovery of prior:

- architectures;
- schemas;
- integrations;
- workflows;
- prompts and templates;
- model/agent patterns;
- deployment patterns;
- storage/Vault patterns;
- testing and rollback procedures;
- product/design patterns;
- known defects and remediation evidence.

DDNA records shall identify whether an observed capability is merely proposed, implemented, tested, validated, promoted, deployed, or retired. Planned work shall not be represented as proven capability.

## 7. Promotion and Feedback

DDNA candidates may feed improvements into D03, D04, D05, D06, D08, D09, D11, D15, D20, D21, D22, products, registries, and reusable architecture libraries. Such feedback is a proposal until the governing authority promotes the change.

When DCS Level 0 explicitly approves exact DDNA/governance content for immediate promotion, administrative GitHub/Supabase/Tribunal synchronization shall not be treated as a second approval gate.

## 8. Cross-System Integrity

For authority-bearing or reusable DDNA artifacts, maintain the strongest available linkage among:

- DDNA/authority identifier;
- canonical artifact filename/path;
- GitHub repository and commit SHA where applicable;
- content SHA-256 where applicable;
- Supabase registry record;
- lifecycle/promotion state;
- issuing authority;
- effective date;
- Tribunal decision/reconciliation receipt where material;
- supersession lineage.

Mismatch among those surfaces shall be classified as DRIFT and reconciled under D22.

## 9. Existing DDNA Data

Legacy DDNA tables or records remain historical/operational evidence until explicitly migrated, superseded, archived, or retired. This v7.2 doctrine does not authorize destructive migration merely because a newer schema exists.

Current v7.2 DDNA constitutional runtime records shall use the current governed schemas and preserve lineage to legacy data where relevant.

## 10. Security and Publication

Do not place passwords, tokens, API/service-role keys, private keys, connection strings, recovery codes, MFA material, or other secret values in DDNA records, doctrine, Tribunal receipts, prompts, model memory, GitHub artifacts, or public outputs.

Internal DDNA knowledge may not be published merely because it is retrievable. Public use remains subject to lane, evidence, confidentiality, source, brand, and publication controls.

## 11. Related Doctrine

- D03 AI Orchestration
- D04 Command Post Communications
- D05 Baseline Promotion
- D06 File System
- D08 Voice and Tone
- D09 Brand Identity
- D15 Database Administration
- D20 Product Assembly Methodology v7.2
- D21 Doctrine Runtime Engine
- D22 Source Authority and Runtime Distribution v7.2

## 12. Promotion Record

This D16 v7.2 governance alignment is **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 effective 2026-09-10**. It supersedes conflicting DDNA persistence-routing language in older D16 copies while preserving the five-layer DDNA model and non-conflicting extraction/lifecycle requirements.