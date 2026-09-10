# ESCD TEST PASS 1

**Task ID:** DCSE-ESCD-001-WORKFLOW-004  
**Pass:** Functional / integration candidate validation  
**Status:** PASS

## Verified evidence

GitHub Actions run `34428703272` executed the ESCD review gate on workflow/UI code head `403bc9ecc1c01a44acf5e373a60f6b68b7b4926f` before evidence-only closeout commits.

Results:

- ESCD Python and candidate API entrypoint compile: PASS
- ESCD Python policy/runtime/workflow/UI-contract suite: **181 passed plus 10 subtests**
- isolated PostgreSQL 17 bootstrap: PASS
- full current ESCD candidate migration chain: PASS
- existing runtime SQL behavior checks: PASS
- Executive/PA SQL behavior checks: PASS
- structured source-link SQL behavior checks: PASS
- workflow orchestration/authority SQL behavior checks: PASS

## Workflow functional coverage

Pass 1 covers:

- all ten planned workflow template types
- deterministic template fingerprints
- exact version and instance binding
- controlled inheritance and non-weakening parent controls
- workflow instance creation and dedupe
- governed-job execution binding
- workflow and step transition contracts
- dependencies and deterministic next-step selection
- action-scoped approval behavior
- A4 prohibited step behavior
- evidence-gated step/workflow completion
- retry/failure state
- append-oriented workflow history
- caller-JWT/RLS repository and API surface
- main ESCD workflow list/detail/instantiate UI contract
- dedicated workflow lifecycle operator UI contract
- specific ESCD UI/API routing before generic fallback
- responsive, keyboard-focus, reduced-motion and loading/empty/error UI states

## Important validation boundary

This functional pass proves the candidate repository implementation and isolated persistence behavior. It does not prove a deployed authenticated browser journey, live authorized database migration, provider-side connector execution or mobile/device delivery. Those remain final release-validation evidence requirements.

No production system was modified during this validation.
