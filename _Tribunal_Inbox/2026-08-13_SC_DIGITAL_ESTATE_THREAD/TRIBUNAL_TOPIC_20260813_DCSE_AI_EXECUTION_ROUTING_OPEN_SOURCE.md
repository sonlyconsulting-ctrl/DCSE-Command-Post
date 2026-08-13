# Tribunal Topic Record: DCSE AI Execution Routing, Usage Preservation, and Open Source

**Record date:** 2026-08-13  
**Lane:** DCSE / SC  
**Status:** OPERATING-MODEL DISCUSSION RECORD  
**Implementation authority:** NONE

## Finding

The AI/tool estate should operate as a portfolio of specialized execution surfaces under DCS authority and a primary architecture/controller function.

The goal is not model competition.

The goal is:

**right task -> least expensive sufficient authorized surface -> evidence -> reconciliation**

## Current role model

### DCS
Objectives, priorities, business judgment, approval, release/promotion decisions.

### ChatGPT / GPT-5.6 Sol
Architecture, governance, orchestration, reconciliation, adverse findings, decision packets, high-value review, ambiguity resolution.

Do not spend premium reasoning capacity on bulk work that a cheaper authorized worker can perform adequately.

### Gemini
Best candidate roles: workflow analysis, visual/design review, research synthesis, second-pass planning, content adaptation, bulk classification, and adversarial QA.

Gemini should not duplicate the primary-controller role. Force actionable output through an execution contract.

### Qwen
Candidate roles: independent coding/review, lower-cost engineering, structured validation, and CLI/headless work where admitted and verified.

### Antigravity
Candidate roles: DBA/data engineering, schema/migration work, database review, browser/technical inspection, bounded technical execution, and independent technical validation where separation of duties is preserved.

Current runtime admission must be verified before representing Antigravity as an automated poller worker.

### Codex
Repository engineering, refactor, testing, debugging, migrations, deployment remediation, and release engineering.

### Local Ollama
Verified bounded capability from supplied Tribunal records:

- `smollm2:1.7b`;
- local-only Ollama;
- 11 of 11 D08 extraction chunks completed;
- exact schema validation;
- 15,898 total local model tokens;
- $0 local model/API charge;
- no cloud fallback.

The current Windows machine has approximately 8 GB RAM and requires careful memory gating.

Best local uses: extraction, classification, normalization, structured tagging, bounded batch transformations, and some first-pass review.

Do not assume the current hardware can replace frontier reasoning, strong visual design, or complex software generation.

## Usage-management principle

Preserve high-value controller capacity, offload labor-heavy tasks, use CLI/local execution selectively, and preserve evidence so expensive work is not repeated.

## Generic worker output contract

`Objective -> Known State -> Required End State -> Dependencies -> Work Packages -> Tool/Owner -> Acceptance Evidence -> Risks -> Stop-Gates -> Next Executable Action`

Mandatory rule:

**Do not return recommendations without converting them into executable work packages.**

Each recommendation must identify action, execution surface, dependency, evidence required for completion, and next handoff.

## Worker portability objective

Create a reusable Agent Work Package Contract so Gemini, Qwen, Codex, Antigravity, local models, and future workers receive the same bounded task envelope.

Candidate fields: task_id, lane, confidentiality, objective, authorized/prohibited sources, current state, required end state, inputs, outputs, tool restrictions, cost ceiling, acceptance criteria, Stop-Gates, evidence schema, and handoff target.

## Consequence

This reduces dependency on any one model vendor and makes model-quality differences manageable because tasks are routed by capability rather than expecting one model to perform every role.