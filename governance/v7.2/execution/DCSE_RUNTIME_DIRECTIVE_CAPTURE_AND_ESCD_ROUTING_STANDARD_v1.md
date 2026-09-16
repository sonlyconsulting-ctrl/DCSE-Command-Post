# DCSE Runtime Directive Capture and ESCD Routing Standard v1

**Document ID:** DCSE-RDC-ESCD-001  
**Version:** 1.0  
**Authority:** DCS Level 0 instruction dated 2026-09-16  
**Status:** ACTIVE BY DCS LEVEL 0 EXPRESS DIRECTIVE  
**Lane:** DCSE  
**Parent controls:** Master Profile v7.2 R5, D03, D04, D05, D21, D22, Conversation Intake and Closeout Contract

## 1. Purpose

Prevent authoritative operating corrections, defaults, and recurring execution expectations from remaining trapped in conversation history.

When DCS states a prospective operating requirement using language such as **should**, **must**, **default**, **always**, **whenever**, **from now on**, **make this the rule**, or equivalent directive language, the Orchestrator SHALL resolve whether that requirement is already represented in v7.2 and persist it appropriately.

This standard does not make every casual suggestion doctrine. It governs DCS operating directions intended to control future DCSE behavior.

## 2. Directive Capture Resolution

For each qualifying DCS direction:

1. classify lane, entity, scope, sensitivity, authority and intended operational effect;
2. search current v7.2 doctrine, directives, execution standards, methodologies, Rule Foundry and project overlays for an existing control;
3. classify the result as:
   - `EXISTING_NO_CHANGE`
   - `EXISTING_AMEND`
   - `NEW_V72_CONTROL`
   - `PROJECT_ONLY`
   - `DECISION_REQUIRED`
4. update/amend the existing controlling artifact when appropriate;
5. otherwise create the smallest correct v7.2 control surface;
6. record lineage in `dcs_express_directives.v7.2.json` when the direction is Level 0 and enterprise-operational;
7. add navigation/manifest references when the new control must be discoverable during normal v7.2 startup;
8. create/update executable rule representation when deterministic enforcement is appropriate;
9. record evidence and runtime/ESCD synchronization.

A model shall not respond only with "we should add this later" when the current task has enough authority and access to persist the control.

## 3. ESCD / Dashboard Intake Resolution

When DCS presents an item "for ESCD", "for the dashboard", or equivalent:

1. classify item type, lane, entity, authority, sensitivity and lifecycle;
2. search the predetermined destination registry/registries;
3. determine **existing vs new before response**;
4. if existing, update or link the existing object rather than duplicate it;
5. if new, create it in the predetermined destination;
6. return the action state and durable identifier.

Allowed action states:

- `EXISTING_UPDATED`
- `EXISTING_LINKED`
- `NEW_CREATED`
- `BLOCKED`

### Predetermined destinations

| Object | Primary destination |
|---|---|
| user-facing task/idea/knowledge/asset | `public.items` |
| substantive governed project task | `public.pm_tasks` |
| artifact/evidence pointer | `public.pm_artifacts` and optionally `public.items` |
| material decision | `public.pm_decisions` |
| risk | `public.pm_risks` |
| blocker | `public.pm_blockers` |
| DDNA learning/source state | DCSE-DDNA + vector-memory tables |
| canonical governance/code | GitHub v7.2 / governed project repository |

The Orchestrator may create linked records in more than one destination when each serves a distinct required function. Duplication of the same logical object without linkage is prohibited.

## 4. Existing-vs-New Matching

Resolve in this order:

1. exact Task ID / task code;
2. exact source/artifact key;
3. exact external evidence identity such as GitHub issue/commit;
4. normalized title + project/lane/entity;
5. semantic similarity.

A semantic near-match with uncertain identity SHALL be linked and marked for review rather than silently merged.

## 5. "Should" Interpretation Boundary

A qualifying DCS "should" is prospective governance when it clearly describes how DCSE, its agents, workflows, systems, artifacts, or future executions are expected to operate.

Examples:
- "ESCD should automatically determine new or existing."
- "Media assets should be collected into a domain-first codebase."
- "Every correction like this should become part of v7.2."

A "should" is not automatically enterprise governance when it is:
- brainstorming about a public product;
- an unresolved design preference;
- a hypothetical;
- an external recommendation being discussed;
- a project-specific choice that does not generalize.

When ambiguous and the distinction materially changes authority or enterprise behavior, ask DCS. Otherwise route to the narrowest justified scope.

## 6. UI/Runtime Evidence Contract

For persisted ESCD/dashboard objects, preserve when applicable:

- Task ID / object ID;
- NEW vs EXISTING resolution;
- lane and entity;
- object type;
- current state;
- priority;
- canonical/evidence links;
- related GitHub issue/commit;
- parent/child relationships;
- synchronization state;
- unresolved gate;
- next action.

The UI should expose these without requiring DCS to infer system state from prose.

## 7. DDNA Learning

Runtime corrections and their before/after outcomes are high-value DDNA sources.

DDNA may derive patterns and rule candidates but may not self-promote them. Level 0 directives retain their authority through the exact directive/canonical artifacts, not through embeddings or recurrence.

## 8. Stop Gates

Stop and escalate for:
- PS/protected spill into non-PS surfaces;
- secret/credential exposure;
- destructive or public/production action not authorized;
- conflict between current Level 0 directions;
- required constitutional/Master Profile change not expressly authorized.

## 9. Closeout

A qualifying directive-capture task is not complete until:
- existing/new status is resolved;
- v7.2 or project control is persisted;
- relevant ESCD/runtime object is reconciled;
- evidence links are returned;
- any deterministic rule status is disclosed accurately.

**Structure Precedes Scale.**
