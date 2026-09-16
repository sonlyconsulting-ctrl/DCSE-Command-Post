"""The orchestrator.

Receive an operation, resolve the rules that apply to it, evaluate them,
compute a disposition, execute if permitted, and emit evidence that a later
reader can check without trusting this account of it.

This is the layer both designs were reaching for and neither had. One of them
described which rules apply to an operation. The other described which rules
are allowed to exist. Neither of them ran anything. This does, and it is where
the two compose: the entity by capability decomposition resolves the set, the
lifecycle gate filters it, and the register records what happened so the set
can improve.

Nothing here is a judgment call. Every branch is a comparison.
"""
from __future__ import annotations

import json
import sys
from typing import Any, Callable, Dict, List, Optional, Sequence

from adapters import AdapterSet, DEFAULT_ADAPTERS
from closure import RULE_ID as CLOSURE_RULE_ID, RULESET as CLOSURE_RULESET, SOURCE_REFS as CLOSURE_SOURCE_REFS, VERSION as CLOSURE_VERSION, validate_closeout
from model import (ACTIVE, BINDING, BOTH, CANDIDATE, ESCALATE, EXECUTE,
                   EXECUTE_AS_CANDIDATE, FAIL, HIGH, IRREVERSIBLE, LOW,
                   MODERATE, NOT_TRIGGERED, Operation, Outcome, PASS, Plan,
                   REFUSE, RESIDUAL, REVERSIBLE, Rule, RuleResult, SHADOW,
                   UNKNOWN, disposition_for)
from predicates import missing_of
from registry import REGISTRY, Registry, load_rules

REVERSIBILITY_RANK = {REVERSIBLE: 0, RESIDUAL: 1, IRREVERSIBLE: 2}
CONSEQUENCE_RANK = {LOW: 0, MODERATE: 1, HIGH: 2}


class Orchestrator:
    def __init__(self, registry: Optional[Registry] = None,
                 adapters: Optional[AdapterSet] = None,
                 recorder: Optional[Callable[[str, Operation, RuleResult], None]] = None):
        self.registry = registry or load_rules()
        self.adapters = adapters or DEFAULT_ADAPTERS
        self.recorder = recorder

    # -- the flow ------------------------------------------------------

    def resolve(self, op: Operation, stage: str = BOTH) -> List[Rule]:
        return self.registry.applicable(op, stage)

    def evaluate(self, op: Operation, rules: Sequence[Rule]) -> Plan:
        plan = Plan(operation=op)
        worst_rev, worst_con = REVERSIBLE, LOW

        for r in rules:
            binding = r.lifecycle in BINDING and r.blocking
            try:
                verdict = r.check(op)
            except Exception as exc:  # noqa: BLE001
                # A rule that raises is a broken rule, not a failed operation.
                # It reports and is never allowed to refuse, because a crash is
                # not a finding about the work.
                plan.results.append(RuleResult(
                    rule_id=r.id, verdict=UNKNOWN, binding=False,
                    detail="rule raised %s: %s" % (type(exc).__name__, exc)))
                continue

            if verdict == PASS and not r.triggered_by(op):
                continue

            missing = missing_of(op, *r.requires) if r.requires else ()
            if verdict == UNKNOWN and not missing:
                missing = tuple(k for k in r.requires if not op.has(k))

            plan.results.append(RuleResult(
                rule_id=r.id, verdict=verdict, binding=binding,
                detail=r.name, missing=missing,
                ruleset=getattr(r, "ruleset", getattr(r, "category", r.id.split("-")[0])),
                status=getattr(r, "lifecycle", "OPERATIVE"),
                source_ref=getattr(r, "origin", ""),
                severity=getattr(r, "consequence", "NORMAL"),
                evidence_refs=tuple(op.facts.get("evidence_refs") or ([op.facts["completion_evidence"]] if op.facts.get("completion_evidence") else ()))
            ))

            if self.recorder is not None:
                self.recorder(r.id, op, plan.results[-1])

            # Which rules set the operation's risk profile, and why it is not
            # all of them. A rule scoped to particular actions is describing
            # what those actions cost: VOICE-01 fires on send and says sending
            # is irreversible. A rule that applies to every action is stating
            # an invariant, and its consequence describes the severity of
            # violating it, not the risk of the work.
            #
            # Letting invariants set the profile makes ESCALATE the default for
            # anything that touches a serious rule even when it satisfies it,
            # which is the opposite of gate minimization. Found by a test.
            if binding and "*" not in set(r.actions):
                if REVERSIBILITY_RANK[r.reversibility] > REVERSIBILITY_RANK[worst_rev]:
                    worst_rev = r.reversibility
                if CONSEQUENCE_RANK[r.consequence] > CONSEQUENCE_RANK[worst_con]:
                    worst_con = r.consequence

        # An operation may declare its own floor. A caller who knows the work
        # is irreversible says so, and no rule can talk it back down.
        declared_rev = op.get("reversibility")
        declared_con = op.get("consequence")
        if declared_rev in REVERSIBILITY_RANK and \
                REVERSIBILITY_RANK[declared_rev] > REVERSIBILITY_RANK[worst_rev]:
            worst_rev = declared_rev
        if declared_con in CONSEQUENCE_RANK and \
                CONSEQUENCE_RANK[declared_con] > CONSEQUENCE_RANK[worst_con]:
            worst_con = declared_con

        # Closure integrity is an operative controller invariant sourced from
        # existing DCS authority. It is injected here rather than left to worker
        # narrative so a terminal/review-ready state cannot be self-declared.
        closure = validate_closeout(op)
        if closure.applicable:
            closure_result = RuleResult(
                rule_id=CLOSURE_RULE_ID,
                verdict=PASS if closure.passed else FAIL,
                binding=True,
                detail=closure.detail,
                missing=tuple(closure.missing),
                ruleset=CLOSURE_RULESET,
                version=CLOSURE_VERSION,
                status="OPERATIVE_DIRECTIVE",
                source_ref="; ".join(CLOSURE_SOURCE_REFS),
                severity="HIGH" if not closure.passed else "NORMAL",
                disposition="" if closure.passed else "HOLD_REMEDIATE",
                evidence_refs=tuple(closure.evidence_refs),
            )
            plan.results.append(closure_result)
            if self.recorder is not None:
                self.recorder(CLOSURE_RULE_ID, op, closure_result)

        plan.reversibility = worst_rev
        plan.consequence = worst_con
        return plan

    def run(self, op: Operation, execute: bool = True,
            stage: str = BOTH) -> Outcome:
        """stage="plan" answers whether the work may be attempted. The default
        answers both that and whether it was done correctly, which is what you
        want when the facts are already in hand."""
        rules = self.resolve(op, stage)
        plan = self.evaluate(op, rules)
        disposition, reason = disposition_for(plan)

        outcome = Outcome(operation_id=op.id, disposition=disposition,
                          reason=reason, plan=plan)

        closure_failure = next(
            (r for r in plan.results
             if r.rule_id == CLOSURE_RULE_ID and r.binding and r.verdict == FAIL),
            None,
        )
        if closure_failure is not None:
            # Refusing the state transition is not the same as declaring the
            # underlying implementation failed. Preserve technical completion,
            # expose the evidence gap, and make remediation machine-actionable.
            outcome.reason = closure_failure.detail
            outcome.execution = {
                "performed": False,
                "state": "TECHNICALLY_COMPLETE",
                "review_state": "HUMAN_REVIEW_EVIDENCE_PENDING",
                "requested_transition": op.get("target_state", op.action),
                "remediation_required": list(closure_failure.missing),
                "authority_refs": list(CLOSURE_SOURCE_REFS),
            }

        if execute and disposition in (EXECUTE, EXECUTE_AS_CANDIDATE):
            adapter = self.adapters.for_operation(op)
            result = adapter.perform(op)
            outcome.executed = bool(result.get("performed"))
            outcome.execution = result
            if disposition == EXECUTE_AS_CANDIDATE:
                outcome.execution["layer"] = "candidate"
        return outcome

    # -- reporting -----------------------------------------------------

    def explain(self, outcome: Outcome) -> str:
        p = outcome.plan
        lines = [
            "operation   %s  %s on %s" % (outcome.operation_id, p.operation.action,
                                          p.operation.entity),
            "capabilities %s" % (", ".join(p.operation.capabilities) or "none"),
            "risk        %s / %s consequence" % (p.reversibility, p.consequence),
            "disposition %s" % outcome.disposition,
            "reason      %s" % outcome.reason,
            "",
            "  %-12s %-9s %-7s %s" % ("RULE", "VERDICT", "MODE", "NAME"),
        ]
        for r in p.results:
            if r.verdict == PASS and r.binding:
                continue
            lines.append("  %-12s %-9s %-7s %s%s" % (
                r.rule_id, r.verdict, "bind" if r.binding else "shadow", r.detail,
                ("  missing: " + ", ".join(r.missing)) if r.missing else ""))
        counts = outcome.evidence()["counts"]
        lines.append("")
        lines.append("  %d evaluated, %d binding, %d shadow, %d fail, %d unknown"
                     % (counts["evaluated"], counts["binding"], counts["shadow"],
                        counts["fail"], counts["unknown"]))
        if outcome.execution:
            lines.append("  execution: %s" % json.dumps(outcome.execution))
        return "\n".join(lines)


def bridge_to_register(rulebase: Any) -> Callable[[str, Operation, RuleResult], None]:
    """Feed every firing into the rule register.

    This is what closes the loop. The orchestrator runs rules; the register
    decides which rules are allowed to run bindingly next time, based on what
    happened when they ran. Note the validated_by default: silence. A firing
    nobody checked confirms nothing, and the register will refuse to promote on
    it no matter how many times it happens.
    """
    def record(rule_id: str, op: Operation, result: RuleResult) -> None:
        if rulebase.rule(rule_id) is None:
            return
        rulebase.record_firing(
            rule_id, op.signature(),
            matched=result.verdict != NOT_TRIGGERED,
            selected=result.binding,
            outcome=result.verdict,
            validated_by="silence",
            exception=(result.verdict == FAIL and not result.binding),
            detail=result.detail)
    return record
