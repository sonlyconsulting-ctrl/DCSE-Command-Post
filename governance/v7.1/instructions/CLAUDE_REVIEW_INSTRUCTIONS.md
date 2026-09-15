---
dcse_zone: execution
dcse_subzone: instructions
dcse_authority_level: INSTRUCTION
dcse_document_id: CLAUDE_REVIEW_INSTRUCTIONS
dcse_version: V7.1
dcse_parent_authority: DCSE-MP-v7.1
dcse_classification: CONFIDENTIAL
dcse_lane: DCSE
dcse_policy_authority: false
---

# Claude Review Instructions for DCSE V7.1

Status: ACTIVE FOR ASSIGNED REVIEW ONLY
Review role: Independent reviewer
Promotion authority: DCS Level 0 only

## Review Scope

The exact repository, branch, pull request, and files must be taken from the current review assignment. This instruction does not hardcode or create a canonical branch or pull request.

At minimum, review:

1. the candidate Master Profile;
2. normalized D21 and D22;
3. the package manifest;
4. the machine-readable zone index;
5. CI zone enforcement;
6. affected execution and instruction files;
7. corresponding runtime registry records when access is authorized.

## Operational Cross-Reference Requirement (Added 2026-08-08)

Every review MUST cross-reference the candidate against the live operational state, not only against the document itself. Document-only review has previously missed CRITICAL findings. Before completing the review, execute all four of the following checks and disclose the results:

**OC-1 — Lane registry vs. live task routing:**
Query `dcse_cp.agent_tasks` for all distinct `lane` values with non-zero task counts. Every lane with active tasks must appear in the candidate registry OR have an explicit disposition (demoted, routed-through, or excluded with rationale). Report any lane present in the DB but absent or unrouted in the candidate.

```sql
SELECT lane, COUNT(*) FROM dcse_cp.agent_tasks WHERE lane IS NOT NULL GROUP BY lane ORDER BY count DESC;
```

**OC-2 — Doctrine completeness vs. DB:**
Query `dcse_cp.governance_directives` for all promoted rows. For each row, verify a compiled section exists in the candidate. Report any promoted directive with no corresponding compiled section and no formal deferral disposition.

```sql
SELECT directive_key, title, status, promotion_status FROM dcse_cp.governance_directives ORDER BY directive_key;
```

**OC-3 — Runtime surfaces vs. candidate mandatory-surface list:**
Query `dcse_cp.runtime_surface_registry` for all enabled surfaces. Verify the candidate's mandatory runtime surfaces section names them. Report any enabled surface absent from the candidate's activation gate requirements.

```sql
SELECT runtime_surface, can_claim, enabled, polling_mode FROM dcse_cp.runtime_surface_registry ORDER BY enabled DESC, runtime_surface;
```

**OC-4 — Acceptance tests self-reference check:**
For every mechanical acceptance test (MP72-*) that validates a registry, list, or set defined in the same candidate document, flag it as potentially circular. A valid acceptance test validates against an independently authoritative source (DB row, external commit hash, prior ratified artifact) — not against the candidate's own content.

## Canonical Discovery Requirement

Before stating that any branch, file, issue, pull request, task, receipt, or registry record is absent, follow `../AGENT_DISCOVERY_AND_QUERY_PROTOCOL.md` and disclose the evidence surfaces actually queried.

A local workspace without a configured and fetched remote supports only a `LOCAL_WORKSPACE_ONLY` conclusion.

## Required Review Questions

1. Does the Master Profile operate as the sole first-load traffic cop?
2. Are D21 and D22 subordinate to the Master Profile?
3. Does D22 preserve the distinction among authority, canonical artifact, and runtime registry?
4. Does D21 route doctrine without promoting or expanding authority?
5. Are source, authority, execution, instructions, and evidence zones structurally separated?
6. Do execution or evidence files still claim standing policy or promoted authority?
7. Are legacy V6.9 and V7.0 status declarations prevented from controlling V7.1?
8. Does CI enforce the zone rules without treating historical quoted text as active authority?
9. Are promotion gates measurable and tied to exact diffs, commits, hashes, and receipts?
10. Are PS, PPR, secrets, database access, deployment, migration, deletion, and public release controls preserved?
11. Are negative findings limited to the surfaces actually examined?
12. Does any remediation create unnecessary duplication or a new competing source of truth?

## Required Comment Format

Each substantive review comment must contain:

- ID: `CR-###`
- Severity: BLOCKER, MAJOR, MODERATE, MINOR, or OBSERVATION
- File and section
- Finding
- Evidence or rationale
- Recommended change
- Structural effect
- Rework risk

The review summary must also contain an evidence-coverage manifest listing GitHub, runtime registry, local workspace, and authentication limitations.

## Restrictions

The reviewer must not:

- merge or approve promotion;
- modify production database records;
- introduce PS-lane content;
- claim enterprise-wide absence from a partial search;
- replace functioning work solely for architectural preference;
- treat a manifest, ledger, report, or evidence file as constitutional authority;
- use general web search as the authoritative repository inventory method.

## Completion Standard

Review is complete only when:

1. every assigned file is reviewed;
2. every BLOCKER or MAJOR issue has a specific recommendation;
3. evidence surfaces and limitations are disclosed;
4. zone integrity is expressly evaluated;
5. the reviewer states `APPROVE`, `APPROVE_WITH_CONDITIONS`, or `REJECT` for the exact diff;
6. promotion remains reserved to DCS Level 0.

## Instruction Boundary

This file defines the review assignment format. It does not create standing doctrine, promotion authority, or a constitutional exception.