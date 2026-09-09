# DCSE DDNA Consumer Cutover Runtime Baseline

Task ID: `DCSE-DDNA-CONSUMER-CUTOVER-20260909-001`
Status: IN PROGRESS

## SC Agent OS baseline

Vercel project: `sc-agent-os`
Project ID: `prj_z6GCdh8IzcPnQ4PwgFmZ8V5YhNKM`
Team ID: `team_g4aI8rT2IsL2OCR3pYA65141`

Observed on 2026-09-09:
- Recent Git-linked deployments are repeatedly marked `CANCELED`.
- The deployment triggered by merge commit `b53b590bfc3bd3d8fbaef946e7ebb7bbad32aeef` is `CANCELED`.
- Error-only build-log inspection for that deployment returned no error/stderr/exit events.
- Therefore deployment-cancellation cause is UNKNOWN at this stage.

## Control implication

DDNA cutover testing must establish application/runtime health independently from DDNA read equivalence. A canceled deployment must not be treated as evidence that the DDNA implementation failed unless causal evidence supports that conclusion.

## Required baseline tests before production release

- Identify most recent known-good reachable SC Agent OS deployment or current production alias behavior.
- Exercise the existing legacy DDNA read path before switching.
- Exercise the dedicated DDNA read path in preview/test-safe execution.
- Compare functional response and failure behavior.
- Verify rollback mode returns to legacy behavior.

No production cutover is authorized by this baseline artifact.
