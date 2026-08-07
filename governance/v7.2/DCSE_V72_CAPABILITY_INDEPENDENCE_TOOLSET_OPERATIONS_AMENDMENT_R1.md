# DCSE v7.2 CAPABILITY INDEPENDENCE & TOOLSET OPERATIONS AMENDMENT R1

**Artifact Class:** Governance Architecture Amendment / Operating Model  
**Controller Family:** DCSE Master Profile v7.2  
**Status:** CANDIDATE INPUT FOR R4  
**Authority:** DCS  
**Architecture Principle:** Structure Precedes Scale  
**Target Independence Date:** 2026-10-03  
**Program:** DCSE AI Capability Portability & Open-Source Independence  
**Project Code:** `DCSE_AI_PORTABILITY_20261003`

---

# 1. PURPOSE

This amendment adds a missing operating layer to DCSE v7.2:

> Paid AI subscriptions, proprietary models, open-source models, runtime agents, plugins, connectors, browsers, research systems, coding agents, media tools, and local runtimes SHALL be governed as interchangeable capability surfaces under the DCSE controller.

No vendor, model family, subscription, desktop application, coding agent, notebook product, or cloud agent SHALL become a constitutional dependency merely because it is powerful or currently paid for.

The objective is practical, not theoretical:

> By 2026-10-03, DCSE SHALL be able to continue defined core DCSE / SC / SS operations if OpenAI and Claude paid plans are not renewed.

Google AI Pro remains available longer under the current user-reported renewal window, but SHALL also be treated as acceleration capacity rather than foundational authority.

---

# 2. CURRENT USER-REPORTED SUBSCRIPTION WINDOWS

| Provider | Plan / Surface | User-Reported Window | Governance Treatment |
|---|---|---|---|
| OpenAI | ChatGPT Pro / GPT / Work / Codex / Desktop | "through September 3, 2024" | **DATE ANOMALY.** Current date is 2026-08-07. Do not silently correct. Requires DCS confirmation. |
| Anthropic | Claude Pro | through 2026-08-11 | Active, near-term extraction and renewal decision priority |
| Google | Google AI Pro | through November 2026 | Active, month known, exact day unknown |

Renewals SHALL be re-evaluated from evidence rather than automatically presumed necessary.

---

# 3. V7.2 SUBSCRIPTION-INDEPENDENCE RULE

## MP-CAP-01 Paid Plans Are Accelerators

Paid subscriptions MAY improve model quality, agentic depth, tool access, coding speed, research quality, media generation, context capacity, convenience, and concurrency.

They SHALL NOT own DCSE governance, canonical project state, reusable prompts or process rules, evidence, source assets, project/task history, tool-selection logic, DDNA knowledge, acceptance criteria, model evaluations, maintenance schedules, or promotion authority.

## MP-CAP-02 Independence Target

The initial independence target is `2026-10-03`.

By that date, DCSE SHALL test continuity of a defined core workflow set without relying on OpenAI or Claude paid-plan-only capabilities.

Passing does not require open-source models to equal frontier models on every task. Passing requires that DCSE can accept work, classify it, retrieve relevant knowledge, create governed context, dispatch a compatible worker, use tools, produce structured outputs, write or modify governed artifacts, run tests where applicable, capture evidence, validate, reconcile state, and continue essential operations.

---

# 4. CAPABILITY REGISTRY MODEL

v7.2 SHALL maintain a capability registry independent of `agent_registry`.

`agent_registry` answers: **Who is the logical worker and what may it do?**

`runtime_surface_registry` answers: **Where and how does the worker execute?**

`tool_capability_registry` answers: **What functional capability exists, which provider/tool supplies it, what subscription controls it, and what replacement path exists?**

Each capability SHALL record at least:

```text
capability_key
provider
product family
tool name
capability class
access mode
subscription dependency
mission relevance
operational role
tool surface
vendor-lock risk
portability requirement
OSS replacement target
replacement status
target independence date
verification source
verification date
```

---

# 5. CURRENT TOOL FAMILY STRATEGY

## 5.1 OpenAI

Mission-relevant capability classes include Chat/reasoning, Work/long multi-step knowledge work, Codex/software work, Projects/persistent scoped context, Deep Research, Scheduled Tasks, Plugins/Apps, desktop browser operation, and voice where useful.

DCSE SHALL use these capabilities while access exists, but every repeated high-value process SHALL be captured into DCSE-owned workflow/toolset records.

## 5.2 Anthropic

Mission-relevant capability classes include Claude chat, Claude Code, Cowork, Projects/RAG, Research, Artifacts, code execution/file creation, Plugins, and Remote MCP connectors.

Claude Pro's near-term renewal date makes extraction of repeatable Claude operating knowledge a priority.

## 5.3 Google AI Pro

Mission-relevant capability classes include Gemini Pro, Gemini Deep Research, Gemini Notebook, Google AI Studio, Jules, Google Flow, Gemini in Workspace applications, Chrome/Auto Browse where available, and Antigravity only where stable and governed.

Google AI Pro SHALL be exploited aggressively for DCSE-relevant work, but Google SHALL remain one provider inside the fabric rather than becoming the fabric.

## 5.4 Open-Source / Local

Initial open-source/local replacement targets include Qwen Windows CLI/Qwen Code, Ollama-compatible local models, Hermes local, Dolphin Mistral challenger, future tool-capable Qwen/Llama/Mistral models, local embeddings/RAG, open browser automation, and vendor-neutral MCP/A2A/function-call adapters.

---

# 6. TOOLSET RULE

Every new material workflow SHALL have a toolset assignment or an explicit `TOOLSET_EXCEPTION`.

A toolset defines workflow class, applicable lanes, lifecycle phases, preferred capabilities, challenger capabilities, open-source fallback capabilities, selection policy, DDNA requirement, independent-validation requirement, export-capture requirement, maintenance profile, and independence target.

Initial governed toolsets:

```text
TS_IDEA_TO_OPERATIVE
TS_CODE_BUILD_TRIAD
TS_RESEARCH_DDNA
TS_PRODUCT_BUILD
TS_CONTENT_CAMPAIGN
TS_KNOWLEDGE_DOCUMENT
TS_MAINTENANCE_SELF_CHECK
TS_PORTABILITY_EXIT
```

---

# 7. IDEA-TO-OPERATIVE WORKFLOW

```text
IDEA
  ↓
INTAKE
  ↓
DISCOVER / INVENTORY
  ↓
RESEARCH
  ↓
ARCHITECT / SPEC
  ↓
TOOLSET SELECTION
  ↓
BUILD
  ↓
TEST
  ↓
INDEPENDENT REVIEW
  ↓
PROMOTION / RELEASE DECISION
  ↓
OPERATE
  ↓
OBSERVE
  ↓
MAINTAIN
  ↓
EXTRACT LESSONS / DDNA
  ↓
IMPROVE
```

The Command Post SHALL create planning records in the Project Manager and executable units in `dcse_cp.agent_tasks`. The Project Manager SHALL NOT manually create duplicate assignment rows. `route_task_assignment` remains the execution-assignment authority.

---

# 8. COMMAND POST DASHBOARD INTAKE

DCS / SC / SS project or build intake SHOULD capture:

```text
Entity / business domain
Runtime lane
Objective
Problem or opportunity
Desired deliverable
Workflow class
Sensitivity / confidentiality
Source materials
Deadline / target date
Definition of done
Risk level
External publication / deployment intent
```

The planner SHALL derive:

```text
recommended toolset
required phases
preferred provider/tool capabilities
challenger/reviewer family
OSS fallback
context packet
acceptance criteria
required evidence
maintenance profile
DDNA extraction requirement
```

Overrides SHALL be recorded.

---

# 9. TOOL-SELECTION PRINCIPLE

Tool selection SHALL be capability-based, not brand-first.

The controller chooses among implementations based on authority, lane, sensitivity, tool availability, entitlement, runtime health, cost, quality history, speed, context requirements, tool access, vendor-lock risk, open-source parity objective, and independent-validation needs.

---

# 10. MULTI-MODEL BEHAVIOR

For material work, model families MAY be assigned distinct roles:

```text
Primary: perform the task
Challenger: seek missed assumptions, over-normalization, failure cases or alternatives
Validator: independently verify evidence, tests, grounding or acceptance criteria
Extractor: convert output/process into reusable DCSE knowledge
Convergence: reconcile findings into a governed result
```

A workflow SHALL NOT require all providers merely for ceremony.

---

# 11. PAID-PLAN EXTRACTION RULE

Every material use of a paid-plan capability SHOULD produce a reusable knowledge-capture decision.

Capture when applicable:

```text
task objective
prompt or instruction pattern
context preparation
tool sequence
input/output format
intermediate artifacts
tests / evals
failure modes
recovery steps
model-specific observable techniques
provider-specific dependency
vendor-neutral rule
open-source replacement note
source/evidence references
```

Do NOT export credentials, secrets, inaccessible proprietary model internals, hidden chain-of-thought, private provider data, or PS material outside PS authorization.

---

# 12. EXTRACTION CONVEYOR

```text
Asset / Idea / Workflow / Completed Task
          ↓
Asset Registry / Source Reference
          ↓
DDNA Source Queue
          ↓
Source Resolution + Hash Verification
          ↓
Extraction Run
          ↓
Candidate Characteristics
          ↓
Multi-Model Comparison
          ↓
Shared Findings / Divergence / Lost Signals
          ↓
Convergence
          ↓
DCS Review when required
          ↓
RAG Eligibility
          ↓
Reusable Context / Toolset / Doctrine / Training Asset
```

DDNA SHALL distinguish source fact, model observation, shared finding, model-specific finding, unsupported assumption, generic-AI contamination, lost signal, unconventional observation, candidate rule, and approved rule. PS remains fail-closed.

---

# 13. CURRENT DDNA INVENTORY ACTION

Batch `V72_ASSET_INVENTORY_SEED_20260807` contains 56 non-PS registered assets queued for DDNA:

```text
Priority 1: 25 governance / doctrine / Master Profile / methodology / project-instruction sources
Priority 2: 5 product / campaign / implementation / tool sources
Priority 3: 21 code / migration / registry / webpage sources
Priority 4: 5 operational / receipt / status sources
```

The two PS assets in the current asset registry were excluded. Source content SHALL be resolved from authoritative storage before extraction.

---

# 14. MAINTENANCE CONTROL PLANE

Defined controls:

```text
MC_VENDOR_FEATURE_DIFF_WEEKLY
MC_SUBSCRIPTION_RENEWAL_WATCH
MC_OPEN_SOURCE_PARITY_WEEKLY
MC_MODEL_SELF_CHECK_WEEKLY
MC_POLLER_HEALTH_HOST
MC_DDNA_QUEUE_DAILY
MC_ASSET_INVENTORY_WEEKLY
MC_WORKFLOW_TOOLSET_GAP_DAILY
MC_EXPORT_CAPTURE_PER_TASK
```

Vendor feature checks SHALL use current official sources. Model self-checks SHOULD prove version, runtime surface, heartbeat, claim mode, admission, actions, tool access, sample task, structured output, and receipt path. Poller health SHALL check scheduler, logs, worker launch, fresh heartbeat, claim smoke, receipt submission, and orphan recovery.

Maintenance tasks are first-class governed work.

---

# 15. OPEN-SOURCE PARITY MODEL

Open-source parity is workflow-level, not identical model intelligence.

Scoring dimensions MAY include task completion, instruction adherence, tool calling, structured-output validity, artifact quality, coding/test performance, citation/source handling, latency, host resource cost, recovery behavior, receipt completeness, and security-boundary compliance.

Paid primary and OSS fallback SHOULD run stable equivalent fixtures where practical. Results feed DDNA model comparisons, capability selection, toolset policy, and renewal decisions.

---

# 16. OCTOBER 3 INDEPENDENCE GATE

Before 2026-10-03, DCSE SHALL run a controlled paid-plan outage simulation using core fixtures including research, governance analysis, document generation, repository code change, tests, code review, database analysis, browser research/action, asset classification, DDNA extraction, structured receipt, project/task planning, maintenance self-check, RAG retrieval, and SC/SS content workflow.

The gate SHALL report `PASS`, `PASS_WITH_GAPS`, or `FAIL`.

Renewal decisions SHALL use actual usage, unique value, parity gaps, cost, operational risk, vendor lock, migration cost, and strategic value.

---

# 17. CURRENT CONTROL-PLANE IMPLEMENTATION

The following v7.2 capability layer exists in Supabase:

```text
dcse_cp.vendor_subscription_registry
dcse_cp.tool_capability_registry
dcse_cp.workflow_toolset_registry
dcse_cp.maintenance_control_registry
dcse_cp.task_toolset_bindings
dcse_cp.subscription_independence_status
dcse_cp.toolset_binding_gaps
```

Initial capability inventory:

```text
OpenAI:       9
Anthropic:    9
Google:       9
Open source:  3
Total:       30
```

Initial active toolsets: `8`  
Initial maintenance controls: `9`

---

# 18. PROJECT MANAGER PROGRAM

Registered program:

```text
DCSE_AI_PORTABILITY_20261003
```

Workstreams:

```text
WS01 Subscription & Capability Inventory
WS02 Knowledge & Process Extraction
WS03 Open-Source Parity & Runtime Adapters
WS04 CP Dashboard Toolset Routing
WS05 Maintenance & Model Self-Check
WS06 Asset Inventory & DDNA Feed
WS07 October 3 Independence Gate
```

The program contains 16 initial PM tasks. The Project Manager remains the planning layer. Executable tasks flow into `dcse_cp.agent_tasks`.

---

# 19. FIRST TOOLSET-BOUND DISPATCH

First time-critical execution task:

```text
V7_2_CLAUDE_PORTABILITY_EXTRACTION_20260807
```

Initial state: `assigned -> claude_code`  
Bound toolset: `TS_PORTABILITY_EXIT`

Selected capabilities:

```text
cl_code
cl_cowork
cl_projects_rag
cl_research
cl_artifacts
cl_plugins
cl_remote_mcp
```

Required result: portable DCSE-owned Markdown process assets, GitHub commit/hash, Supabase receipt, vendor-neutral replacement mapping, no PS, no secrets, no hidden chain-of-thought export.

---

# 20. V7.2 ENFORCEMENT LOGIC

```text
MP-CAP-01  Paid subscriptions are acceleration capacity, not sovereign dependency.
MP-CAP-02  Every material workflow has a governed toolset or recorded exception.
MP-CAP-03  Toolsets define capabilities and fallback paths, not a single mandatory vendor.
MP-CAP-04  Paid-plan-only process knowledge creates portability debt until exported or explicitly waived.
MP-CAP-05  A material workflow may not become newly dependent on a single vendor-specific capability without a documented fallback decision.
MP-CAP-06  Provider/model/tool capability state must be evidence-based and periodically reverified.
MP-CAP-07  Model self-checks require external evidence for runtime/claim/tool assertions.
MP-CAP-08  Maintenance tasks are first-class governed work, not optional housekeeping.
MP-CAP-09  Completed material work is eligible for DDNA/process extraction.
MP-CAP-10  PS remains fail-closed across all proprietary and open-model capability surfaces.
MP-CAP-11  Subscription renewal is a DCS decision informed by portability evidence.
MP-CAP-12  By 2026-10-03, core continuity shall be tested without OpenAI or Claude paid-plan-only paths.
MP-CAP-13  New vendor features must be evaluated for use, replacement risk, and workflow integration.
MP-CAP-14  Existing tasks are not retroactively blocked solely because they lack a toolset binding. Migration is progressive.
MP-CAP-15  route_task_assignment remains the sole production assignment owner. Toolset planning must not duplicate executor assignments.
```

---

# 21. ARCHITECTURE

```text
                         DCS
                          |
                          v
              DCSE Master Profile v7.2
                          |
                          v
                Context / Policy Compiler
                          |
          +---------------+---------------+
          |                               |
          v                               v
   Project / Task Intake            Maintenance Intake
          |                               |
          v                               v
   Workflow Classification         Self-Check / Drift Class
          |                               |
          +---------------+---------------+
                          |
                          v
                   Toolset Selector
                          |
       +------------------+------------------+
       |                  |                  |
       v                  v                  v
  Paid / Frontier     Open / Local       Tools / Apps
  Model Surfaces      Model Surfaces     MCP / Browser /
                                          RAG / DB / Git
       |                  |                  |
       +------------------+------------------+
                          |
                          v
                 DCSE Agent Task Router
                          |
                          v
                     Execution
                          |
                          v
                 Evidence / Receipt
                          |
                          v
             Independent Validation
                          |
                          v
                  State Reconcile
                          |
                          v
                Export / DDNA Decision
                          |
                          v
          Capability & Workflow Improvement
```

---

# 22. CONTROLLING PRINCIPLE

DCSE SHALL take maximum practical advantage of paid frontier tools while they are available.

DCSE SHALL not confuse access with ownership.

The enterprise owns its governance, processes, artifacts, evaluations, source inventories, task state, evidence, DDNA, tool-selection logic, and operating model.

Vendors supply capability.  
Open-source supplies portability and leverage.  
The Control Plane supplies orchestration.  
DCS supplies authority.

**Structure Precedes Scale.**
