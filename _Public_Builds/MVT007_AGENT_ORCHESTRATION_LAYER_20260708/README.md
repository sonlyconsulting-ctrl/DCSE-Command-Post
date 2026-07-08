# DCSE MVT-007 Agent Orchestration Layer

Status: public-safe proof-of-layer  
Date: 2026-07-08  
Primary lane: DCSE  
Operating layer: Supabase Command Post schema, agent registry, task registry, handoff records, GitHub/Tribunal coordination

## Purpose

MVT-007 creates the missing orchestration layer for participating agents and models. The purpose is to let DCS assign work to one agent, many agents, a role group, or a review board, while preserving shared state, authority boundaries, task history, and handoff records.

This is the layer that turns isolated agent activity into controlled Command Post orchestration.

## What was created

The following Supabase Command Post structures were created:

```text
dcse_cp.agent_registry
dcse_cp.agent_tasks
dcse_cp.agent_task_assignments
dcse_cp.agent_task_events
dcse_cp.agent_orchestration_dashboard
```

The following migrations were applied:

```text
mvt007_agent_orchestration_layer
mvt007_seed_agents_initial_task
mvt007_seed_assignments_events
```

## What this enables

```text
one-to-one assignment
one-to-many assignment
many-to-one synthesis
sequential handoff
parallel review
review-board routing
DCS final authority
GitHub and Tribunal coordination
Supabase operating memory
```

## Agent participation model

Agents coordinate through governed shared state, not informal hidden backchannels.

```text
DCS creates or authorizes a task.
The task is classified.
One or more agents are assigned.
The assigned agent acts.
The result is recorded.
The next handoff is determined.
Control returns to DCS, another agent, a review board, or all participating agents by role.
```

## Initial registered participants

```text
ChatGPT
Claude Code
Codex
AG Builder
Review Board
Tribunal Agent
Supabase Database Agent
GitHub Agent
DCS Authority
```

## Authority rule

```text
No agent owns DCSE.
No agent owns final authority.
Agents own assigned actions.
DCS owns authorization.
The Command Post owns traceability.
```

## Relationship to MVT-004 through MVT-006

MVT-004 through MVT-006 proved the data-to-build path:

```text
approved SC source
classification
embedding
pgvector rows
scoped retrieval
HTML build artifact
GitHub public-safe preservation
```

MVT-007 adds the coordination path:

```text
task
assignment
agent role
handoff
event
receipt
dashboard visibility
```

Together, these prove the early Command Post loop:

```text
Data can move.
Agents can act.
GitHub can preserve.
Supabase can remember.
Tribunal can record.
DCS can decide.
```

## Public-safe statement

Use this wording:

```text
DCSE has demonstrated the first version of a governed agent orchestration layer where participating models and agents can be registered, assigned tasks, record outcomes, and hand work off through shared Supabase and GitHub state.
```

Do not use this wording:

```text
All agents now communicate freely and autonomously without DCS control.
```

## Guardrails

```text
No PS leakage.
No uncontrolled public retrieval.
No broad member retrieval.
No hidden agent authority.
No release authority without DCS.
No merge authority unless DCS grants it for that context.
```
