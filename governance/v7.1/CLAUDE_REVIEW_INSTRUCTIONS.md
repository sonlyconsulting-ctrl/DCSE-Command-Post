# Claude Review Instructions for DCSE V7.1

Status: ACTIVE FOR THIS DRAFT PULL REQUEST
Review Role: Independent external reviewer
Promotion Authority: DCS only

## Review Scope

Review these files:

1. `governance/v7.1/DCSE_V7.1_OWNED_PRODUCT_HARNESS_BUILD_PLAN.md`
2. `governance/v7.1/RESEARCH_ANALYSIS_AND_SOURCE_REGISTER.md`
3. `governance/v7.1/CLAUDE_REVIEW_INSTRUCTIONS.md`
4. `governance/v7.1/AGENT_DISCOVERY_AND_QUERY_PROTOCOL.md`

Review the corresponding Supabase registry records in project `DCSE-DDNA` when access is available. Review operational execution state in `SC-Command-Post` when material.

## Canonical Discovery Requirement

Before stating that any V7.1 branch, file, issue, pull request, task, receipt, or registry record is absent, follow `AGENT_DISCOVERY_AND_QUERY_PROTOCOL.md`.

Canonical identifiers:

- Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`
- Branch: `governance/v7.1-owned-product-harness`
- Pull request: `#29`
- Governance path: `governance/v7.1/`
- Governance registry: `DCSE-DDNA` (`uutpzaiqymyufljdgdaa`)
- Operations registry: `SC-Command-Post` (`nevgdyfpxdaloacuutal`)

There is no requirement for a branch named exactly `v7.1`. Exact-name failure is not evidence that V7.1 is absent.

Every review must disclose which GitHub and Supabase surfaces were actually queried. A local workspace without a configured and fetched remote may support only a `LOCAL WORKSPACE ONLY` conclusion.

## Required Review Questions

1. Is V7.1 the correct version classification, or does any proposal materially require V8?
2. Does the plan preserve existing TSL, SC, SS, and platform work?
3. Is Version 1 sufficiently thin for time to market?
4. Which elements are overengineered?
5. Which controls are missing for security, privacy, data integrity, or lane isolation?
6. Is Planner/Builder/Verifier the correct minimum orchestration pattern?
7. Are the marketable product capabilities differentiated and credible?
8. Which items should be deferred until after the TSL audit pilot?
9. Are the promotion gates measurable?
10. What could create hidden recurring cost, lock-in, or maintenance burden?
11. Does the discovery protocol prevent false enterprise-wide negative findings?
12. Are GitHub, DCSE-DDNA, SC-Command-Post, and local workspace roles separated correctly?

## Required Comment Format

Each review comment must contain:

- ID: `CR-###`
- Severity: BLOCKER, MAJOR, MODERATE, MINOR, or OBSERVATION
- File and section
- Finding
- Evidence or rationale
- Recommended change
- Time-to-market effect
- Rework risk

Each review summary must also contain an evidence-coverage manifest showing:

- GitHub repository verified
- branches queried
- pull requests queried
- issues queried
- files queried
- DCSE-DDNA queried
- SC-Command-Post queried
- local workspace status
- authentication or access limitations

## Restrictions

Claude must not:

- merge or approve promotion
- modify production Supabase records
- introduce PS-lane content
- assume access to unreviewed product repositories
- claim TSL production readiness without direct evidence
- replace functioning work solely for architectural preference
- use general web search as the authoritative GitHub inventory method
- generalize a negative finding from one database, branch query, code index, or local checkout

## Response Protocol

ChatGPT/DCS will respond to every substantive review comment with one disposition:

- ACCEPT
- ACCEPT WITH MODIFICATION
- DEFER
- REJECT

The response must explain the decision and identify any resulting file or registry update.

## Completion Standard

Claude review is complete only when:

1. All four files are reviewed.
2. Every BLOCKER or MAJOR issue has a specific recommendation.
3. Time-to-market and rework risks are expressly addressed.
4. The reviewer states whether the proposal is suitable for CONTROLLED PILOT.
5. The evidence-coverage manifest is complete.
6. Negative findings are scoped to the evidence surfaces actually searched.
