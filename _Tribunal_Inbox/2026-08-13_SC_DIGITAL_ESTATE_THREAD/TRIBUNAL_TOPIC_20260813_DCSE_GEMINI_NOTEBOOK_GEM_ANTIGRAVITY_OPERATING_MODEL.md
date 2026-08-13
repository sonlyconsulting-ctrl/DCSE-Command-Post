# Tribunal Topic Record: Gemini, NotebookLM, Gem, and Antigravity Operating Model

**Record date:** 2026-08-13  
**Lane:** DCSE / SC  
**Status:** WORKFLOW OPERATING MODEL  
**Implementation authority:** NONE

## Finding

Gemini should be used more, but not as a competing primary controller.

Its highest-value role in this program is a specialized worker that receives bounded context and an explicit output contract.

NotebookLM, Gemini Gems, and Antigravity should have separate functions.

## NotebookLM role

**NotebookLM = project knowledge/evidence container.**

Recommended use:

- one notebook per materially distinct project/lane;
- load only approved project sources;
- use notebook instructions to establish the project boundary;
- keep PS-confidential material out of SC/SS notebooks;
- use NotebookLM for grounded synthesis, source comparison, evidence recovery, and project-specific Q&A.

NotebookLM should not be treated as the operational task database or canonical source-control system.

Canonical source remains in the governed repository/data systems as defined by the architecture.

## Gem role

**Gem = persistent repeatable specialized worker behavior.**

Recommended Gem:

`DCSE Workflow Engineer`

The Gem should transform approved objectives into actionable work packages.

Core output contract:

`Objective -> Current State -> Required End State -> Dependencies -> Work Packages -> Tool/Owner -> Acceptance Evidence -> Risks -> Stop-Gates -> Next Executable Action`

Mandatory rule:

**Do not return recommendations without converting them into executable work packages.**

This directly addresses the observed weakness where Gemini can return useful concepts without enough operational detail.

## Gemini general role

Preferred assignments:

- workflow engineering;
- research synthesis;
- visual archaeology;
- design comparison;
- bulk inventory;
- channel adaptation;
- second-pass planning;
- adversarial review;
- QA.

Avoid assigning final architecture authority, final governance promotion, unsupported production claims, cross-lane source merging, or unbounded "design the whole company" tasks.

## Antigravity role

Antigravity remains a strong candidate for:

- DBA/data engineering;
- schema review;
- data migration preparation;
- query/performance review;
- browser/technical inspection;
- bounded engineering work;
- independent technical validation where separation of duties is preserved.

Do not represent Antigravity as automatically admitted to the DCSE neutral dispatcher until runtime admission/heartbeat evidence is current.

## Knowledge/work separation

### NotebookLM
Project facts and approved evidence.

### Gem
Worker behavior and output structure.

### Antigravity
Execution surface for bounded technical work.

### Tribunal
Work/evidence communication bank.

### Supabase
Operational/control/data state.

### GitHub
Versioned source and implementation evidence.

### Primary controller
Architecture, reconciliation, routing, and decision support.

## Source-loading order for a Gemini project

1. short project boundary/instructions;
2. current architecture interview/decision packet;
3. approved governing voice/brand sources required for the task;
4. relevant current estate inventory;
5. exact asset(s) under review;
6. acceptance criteria;
7. previous worker output only when necessary.

Do not upload the entire DCSE corpus by default. Use the smallest sufficient source packet.

## Copy/paste companion files

- `SKILL_NOTEBOOKLM_DCSE_PROJECT_KNOWLEDGE_CONTAINER.md`
- `SKILL_GEMINI_GEM_DCSE_WORKFLOW_ENGINEER.md`
- `SKILL_ANTIGRAVITY_DCSE_DBA_EXECUTION.md`

These are written so DCS can paste instructions directly into the relevant surfaces with minimal editing.