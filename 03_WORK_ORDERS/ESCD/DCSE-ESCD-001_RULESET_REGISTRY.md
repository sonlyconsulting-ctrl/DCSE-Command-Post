# ESCD RULE-SET REGISTRY

**Task ID:** DCSE-ESCD-001  
**Lane:** DCSE / Command Post  
**Status:** IMPLEMENTED AND LOCALLY TESTED  
**Scope:** ESCD assistant core only. DCS Employment remains separate under DCS-EMPLOYMENT-BUILD-001.

## Execution principle

For implementation-ready ESCD behavior, the required path is continuous:

`SPECIFICATION -> RULE -> RULE SET -> EXECUTABLE LOGIC -> TEST -> REPAIR -> RETEST`

A specification is not treated as complete for implementation merely because prose exists. Deterministic behavior is externalized into stable rule IDs and executable policy logic where practical. Rules that govern external systems still require runtime integration evidence before external write capability is considered implemented.

## Registry summary

The current assistant-core policy package contains **54 executable/reference rules grouped into 19 rule sets**.

1. `RS-GOVERNANCE` - authority boundary, provenance, stable identity, material unknown handling.
2. `RS-AUTONOMY` - A0 through A4 classification, approval, prohibition, secrets.
3. `RS-TASK-STATE` - NOW/APPROVAL/WAITING/WATCH/BACKLOG routing and deduplication.
4. `RS-NBA` - deterministic next-best-action scoring and tie breaking.
5. `RS-STATE` - item, job, and approval lifecycle transition validation.
6. `RS-SOURCE-ROUTING` - source precedence, contradiction preservation, connector execution class.
7. `RS-BRIEFING` - persisted-state briefing and non-fabrication behavior.
8. `RS-CALENDAR` - overlap and transition-buffer conflict detection plus authorization boundary.
9. `RS-COMMUNICATIONS` - deterministic message triage and external-send gate.
10. `RS-PERSON-CONTEXT` - provenance and sensitive-inference prohibition.
11. `RS-WORKFLOW` - template types, step contracts, inheritance, secret prohibition.
12. `RS-MAKE-FIX-RELEASE` - distinct MAKE, FIX, and RELEASE preconditions and gates.
13. `RS-RECOVERY` - bounded retry, hard stops, uncertain external side-effect reconciliation.
14. `RS-NOTIFICATIONS` - meaningful-change notification, suppression, escalation, hard-stop persistence.
15. `RS-ROUTINES` - pause/cancel, idempotency, missed-run behavior.
16. `RS-DECISIONS-EVIDENCE` - decision completeness and evidence-backed completion.
17. `RS-DDNA-CANDIDATE` - candidate-only knowledge contribution, provenance, secret/self-promotion prohibition.
18. `RS-COMMAND` - command normalization and mandatory authority evaluation.
19. `RS-MOBILE` - pending-until-server-ack and evidence-backed completion behavior.

## Executable implementation

Primary files:

- `apps/escd/policy/models.py`
- `apps/escd/policy/engine.py`
- `apps/escd/policy/extensions.py`
- `apps/escd/policy/catalog.py`
- `apps/escd/policy/complete_catalog.py`

Test files:

- `apps/escd/tests/test_policy.py`
- `apps/escd/tests/test_policy_extensions.py`

## Rule-source relationship

The executable rule sets derive from the ESCD requirements registry, autonomy contract, assistant operating rules, workflow process, next-best-action specification, state/data model, connector/source routing matrix, executive briefing specification, calendar policy, email/message triage rules, workflow template schema, failure/recovery model, notification policy, recurring routine framework, decision record specification, contact/person context specification, command grammar, mobile model, and DDNA candidate contract.

The prose specifications remain design/source contracts. The rule registry is the stable executable decision layer. Neither supersedes current operative DCSE governance.

## Boundaries

- DCS Employment domain logic is not included in this rule-set count.
- Supabase persistence, RLS, queues, live connector writes, Android push, and DDNA production ingestion are not claimed implemented by these pure policy tests.
- No secret, service-role key, credential, production deployment, destructive operation, or external send is authorized by this registry.
- DDNA output is candidate-only until governed validation/promotion.

## Completion condition for this tranche

This specification-to-rules-to-executable-logic tranche is complete when the full policy test suite passes with zero failures and the rule catalog validates unique IDs, expected rule-set count, deterministic NBA weights, and major safety gates. Runtime/persistence integration is a subsequent controlled tranche.
