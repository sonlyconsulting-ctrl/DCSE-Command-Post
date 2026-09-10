# Tribunal Router Phase 2 Receipt v1.0

Status: Candidate built, awaiting DCS review after live placement and validation.

Scope:

- Reconstruct `TRIBUNAL_ROUTER_RULE_BASE_v1.0.json` from DCS Phase 1 seed because the stated live file was not present at preflight.
- Build `tribunal_router_engine.py` with autonomous routing capability and DCS gate controls.
- Preserve root-level `_Tribunal_Inbox` handling.

Autonomous posture:

- Default mode is `autonomous_with_dcs_gate`.
- `--apply` writes `ROUTER_DECISION` annotations into routed Tribunal JSON files.
- Low-confidence, unknown, emerging, or safety-gated directives route to DCS.
- Outcome decisions append to `TRIBUNAL_ROUTER_OUTCOME_LOG.jsonl`.

Safety controls:

- Minimum autonomous confidence: `0.84`.
- Catch-all unknown route: `DCS`.
- PPR secret or identifier risk routes to DCS.
- PS/PPR overlap routes to DCS.
- Emerging SC strategy rule routes to DCS review by default.

Phase reduction:

- No separate dry-run phase is required before capability exists.
- The engine is built for controlled autonomous routing now.
- DCS approval remains the gate for broader unattended operation.
