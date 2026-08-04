# DCSE v7.1 Cowork and Claude Code First-Pass Review

## Role

Perform a read-only first-pass governance review. The reviewer is evidence provider, not promotion authority. Do not modify source doctrine, candidate doctrine, GitHub state, Supabase state, credentials, deployments, workflows, or local files unless DCS separately authorizes a correction pass.

## Working source

- Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`
- Branch: `agent/v71-master-profile-rc3-manual`
- Candidate root: `governance/v7.1/candidates/20260803_doctrine_executability`
- Source root: `governance/v7.1/source/doctrines`
- Requirements: `governance/v7.1/validation/requirements_catalog.json`
- Validator: `tools/v71_governance_validator.py`

Record the exact commit before review. Refuse to claim review of a different or moving source.

## Current corpus boundary

The candidate corpus is incomplete until D07, D12, D13, D14, D18, and D19 candidates exist and final Master Profile, D03, D21, D22, manifest, dependency, trigger, and reconciliation artifacts are compiled.

The first pass may review existing candidates, but must not return a final corpus PASS while any required doctrine or final artifact is missing.

## Required procedure

1. Record repository, branch, commit, model or runtime identity when exposed, and review timestamp.
2. Run:

   `python tools/v71_governance_validator.py --repo .`

3. Read `requirements_catalog.json` completely.
4. Review one doctrine at a time with its active source, correction receipt, and directly referenced dependencies.
5. Apply every applicable catalog rule.
6. Identify description-only language that lacks actor, trigger, required behavior, evidence, or failure disposition.
7. Identify contradictions, duplicate control ownership, missing boundaries, stale provider assumptions, unverifiable claims, and nonmechanical acceptance tests.
8. Preserve the distinction between active source, candidate, committed artifact, promoted artifact, runtime reference, and distributed copy.
9. Do not infer a successful database write, delivery, acknowledgment, promotion, deployment, or runtime load.
10. Produce structured findings only. Do not apply corrections during the first pass.

## Review batches

To control context and cost, use these batches:

1. Master Profile, D03, D05, D21, D22
2. D01, D02, D16, D17
3. D04, D06, D15
4. D08, D09, D10, D11
5. D07, D12, D18, D19 when available
6. D13 and D14 only through their separately authorized isolated review package
7. Final cross-corpus pass after every batch correction is reconciled

Do not load unrelated protected content into a general batch.

## Finding contract

Return JSON or JSONL records using:

```json
{
  "finding_id": "",
  "doctrine_id": "",
  "rule_id": "",
  "severity": "CRITICAL | HIGH | MEDIUM | LOW | INFORMATIONAL",
  "location": "file and section",
  "condition": "",
  "evidence": [],
  "impact": "",
  "required_correction": "",
  "blocks_candidate_pass": false,
  "blocks_corpus_pass": false,
  "disposition": "OPEN | NOT_A_FINDING | DUPLICATE | RESOLVED"
}
```

Do not use a general confidence score as the disposition. When an inference is unavoidable, identify the inference, evidence basis, missing evidence, and effect if incorrect.

## Batch receipt

Each batch ends with:

```json
{
  "review_id": "",
  "source_commit": "",
  "reviewed_files": [],
  "requirements_catalog_hash": "",
  "validator_result": "",
  "finding_counts": {},
  "unresolved_blocking_findings": [],
  "disposition": "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE",
  "database_mutation": "NONE",
  "github_mutation": "NONE",
  "promotion_effect": "NONE"
}
```

## Review standards

- Candidate validity does not prove corpus completeness.
- Corpus completeness does not prove semantic accuracy.
- Semantic review does not create promotion authority.
- A green workflow proves only the checks it executed.
- A healthy database project is not a security certification.
- An unrelated error cannot prove an authorization control.
- Missing evidence results in `INSUFFICIENT_EVIDENCE`.
- A correctable issue should include a specific correction, not a vague recommendation.
- Unaffected review work continues when one file or capability is unavailable.

## Required first response

Before substantive review, return only:

```text
SOURCE_ACKNOWLEDGED
repository: sonlyconsulting-ctrl/DCSE-Command-Post
branch: agent/v71-master-profile-rc3-manual
commit: <exact commit>
requirements_loaded: true|false
validator_executed: true|false
corpus_complete: true|false
mutation_mode: READ_ONLY
```

If the commit, requirements file, or validator cannot be verified, return `STALE_SOURCE_REFRESH_REQUIRED` or `INSUFFICIENT_EVIDENCE` and identify the exact missing item.
