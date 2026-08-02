# Claude Review Instructions for DCSE V7.1

Status: ACTIVE FOR THIS DRAFT PULL REQUEST
Review Role: Independent external reviewer
Promotion Authority: DCS only

## Review Scope

Review these files:

1. `governance/v7.1/DCSE_V7.1_OWNED_PRODUCT_HARNESS_BUILD_PLAN.md`
2. `governance/v7.1/RESEARCH_ANALYSIS_AND_SOURCE_REGISTER.md`
3. `governance/v7.1/CLAUDE_REVIEW_INSTRUCTIONS.md`

Review the corresponding Supabase registry records in project `DCSE-DDNA` when access is available.

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

## Restrictions

Claude must not:

- merge or approve promotion
- modify production Supabase records
- introduce PS-lane content
- assume access to unreviewed product repositories
- claim TSL production readiness without direct evidence
- replace functioning work solely for architectural preference

## Response Protocol

ChatGPT/DCS will respond to every substantive review comment with one disposition:

- ACCEPT
- ACCEPT WITH MODIFICATION
- DEFER
- REJECT

The response must explain the decision and identify any resulting file or registry update.

## Completion Standard

Claude review is complete only when:

1. All three files are reviewed.
2. Every BLOCKER or MAJOR issue has a specific recommendation.
3. Time-to-market and rework risks are expressly addressed.
4. The reviewer states whether the proposal is suitable for CONTROLLED PILOT.
