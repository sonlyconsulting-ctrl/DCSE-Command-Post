# DCSE V7.1 Authoritative Governance Supersession Directive

**Authority:** Direct DCS approval  
**Effective:** August 3, 2026  
**Status:** `AUTHORITATIVE_UNTIL_FURTHER_NOTICE`

## Directive

DCSE V7.1 is the sole current and authoritative governance version for DCSE operations until DCS expressly adopts a later version.

V7.1 supersedes v6.8, v6.9, v7.0, and every earlier DCSE governance version for present interpretation, orchestration, task execution, AI conversation control, evidence, review, promotion, deployment, and closeout.

Earlier versions remain available only as historical evidence, lineage, and lessons learned. They have no controlling effect where they conflict with V7.1.

## Precedence

1. A later direct DCS instruction controls within its express scope.
2. DCSE V7.1 governs all current DCSE operations.
3. Earlier governance may be consulted only for historical context or provisions expressly retained by V7.1.
4. Conflicting legacy prompts, custom instructions, startup text, cached profiles, agent memories, scripts, documentation, database rows, and branch labels must be treated as stale and corrected.

## Required agent behavior

Every AI model, agent, worker, poller, reviewer, and orchestrator must:

- load and acknowledge V7.1 before operational work;
- report the canonical governance version and commit in its startup receipt;
- reject prior-version instructions that conflict with V7.1;
- preserve lane isolation and reserved Stop-Gates;
- use capability-based routing and fallback reassignment;
- record every governed conversation, task, event, artifact, review, and promotion;
- reconcile GitHub and Supabase at closeout.

## Migration requirement

Legacy materials must not be deleted merely because they are superseded. They must be labeled `HISTORICAL_SUPERSEDED`, excluded from active routing, and linked to this directive. Active bootstrap sources must be updated to reference V7.1.

## Acceptance gate

Supersession is fully operational when:

- the directive is committed to the canonical V7.1 governance branch;
- Supabase records the decision and current authority;
- the unified conversation and task ledger identifies V7.1 as controlling authority;
- startup acknowledgments report V7.1;
- scans find no active execution source declaring an earlier version authoritative.
