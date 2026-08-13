# Tribunal Topic Record: DCSE GitHub, Supabase, and Tribunal Control Model

**Record date:** 2026-08-13  
**Lane:** DCSE / SC  
**Status:** ARCHITECTURE DISCUSSION RECORD  
**Implementation authority:** NONE

## Finding

The SC web modernization must use the existing DCSE control plane rather than create a parallel website-project control system.

Three systems have distinct roles.

## GitHub

Proposed role:

- versioned source of truth for code;
- architecture specifications;
- migrations;
- reusable prompts/skills;
- tests;
- release artifacts;
- hashes and receipts where appropriate.

Accessible repository: `sonlyconsulting-ctrl/DCSE-Command-Post`.

## Supabase

Proposed role:

- operational control-plane state;
- task/assignment/event data;
- runtime/agent state;
- artifact references;
- conversations;
- decisions;
- project/workstream/task records;
- application databases where Supabase is selected as data owner.

Current SC Command Post structures already include agent registry, agent tasks, assignments, task events, convergences, artifact references, conversations/turns, strategic decisions, runtime surfaces, PM projects, workstreams, tasks, artifacts, decisions, handoffs, closeouts, and plan-inbox/review records.

## Tribunal

Proposed role: **persistent human-readable work, communication, and evidence bank.**

Tribunal should preserve task packets, handoffs, conversation/topic records, build instructions, receipts, review findings, closeout records, operator decisions, and recovery context.

It should not become a competing authority source that contradicts canonical repository/control-plane state.

## Crosswalk principle

Every material work item should receive one stable external/task identity.

Target chain:

`Project -> Workstream -> Task -> Assignment -> Event -> Artifact -> Review -> Decision -> Closeout`

The identity should be carried through Tribunal filename/payload, Supabase records, GitHub metadata, PR/commit references, deployment evidence, test evidence, and closeout.

## Why this matters

Current DCSE history contains overlapping task/project record generations. The objective is not immediate deletion. The objective is to define lifecycle ownership and stop generating orphaned or duplicate task records.

## Recommended ownership boundary

### Tribunal
Human-readable coordination and evidence.

### Supabase
Machine-operational state and queryable relationships.

### GitHub
Versioned implementation/source/artifact history.

### Deployment platforms
Runtime/deployment evidence, not project-management authority.

## Web modernization umbrella project

Candidate: **SC Digital Estate & Hybrid Web Architecture**

Candidate workstreams:

1. Wix Estate Audit & Design Archaeology
2. SC Information Architecture & Design Contract
3. Hybrid Rendering Architecture
4. Wix Business Capability Rationalization
5. Data Ownership Architecture
6. Chat/F&A Upgrade
7. Blog/Publishing Workflow
8. Offer Architecture
9. GitHub + Wix CLI + Velo Engineering
10. External Platform/Deployment Estate
11. QA, Promotion & Release

## Evidence expectations

For material implementation: stable task ID, branch/commit, PR where appropriate, build/test evidence, deployment evidence, Supabase reconciliation, Tribunal receipt, visual/mobile/accessibility QA where applicable, rollback, cost impact, and human acceptance.

## No unsupported completion

Do not claim completion merely because a command ran, a file exists, a deployment is `READY`, a Supabase row was inserted, or a Tribunal record was created. Completion requires evidence matching task acceptance criteria.