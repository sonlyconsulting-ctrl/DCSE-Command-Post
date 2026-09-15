"""DCSE object model.

Four things and the relationships between them.

    Operation   what someone is trying to do. An entity, the capabilities the
                work touches, an action, and the facts known about it.

    Rule        one predicate over an Operation, returning PASS, FAIL or
                UNKNOWN, with a reversibility and consequence that feed the
                disposition.

    Plan        the compiled set of applicable rules plus their results.

    Outcome     the disposition and the evidence record.

The verdict split is deliberate and is the one place two designs conflicted.
A RULE evaluates. An OPERATION is disposed of. They are not the same vocabulary
and collapsing them is how "the rule passed" turns into "the deployment is
fine", which is the error this whole program exists to stop.
"""
from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from typing import Any, Callable, Dict, List, Optional, Sequence, Set

# -- rule evaluation -------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"
UNKNOWN = "UNKNOWN"
NOT_TRIGGERED = "NOT_TRIGGERED"

# -- operation disposition -------------------------------------------------

EXECUTE = "EXECUTE"
EXECUTE_AS_CANDIDATE = "EXECUTE_AS_CANDIDATE"
ESCALATE = "ESCALATE"
REFUSE = "REFUSE"

# -- reversibility and consequence, as in the register ---------------------

REVERSIBLE = "reversible"
RESIDUAL = "reversible_with_residue"
IRREVERSIBLE = "irreversible"

LOW, MODERATE, HIGH = "low", "moderate", "high"

# -- lifecycle, mirrored from the register so the gate can be applied ------

CANDIDATE = "candidate"
PROVISIONAL = "provisional"
ACTIVE = "active"
DEPRECATED = "deprecated"
RETIRED = "retired"

BINDING = (PROVISIONAL, ACTIVE)     # these can change an outcome
SHADOW = (CANDIDATE,)               # these evaluate and record, nothing more
INERT = (DEPRECATED, RETIRED)       # these do not run

# -- when a rule can be evaluated ------------------------------------------
# Some rules gate the attempt and others verify the result, and they cannot
# both be checked at the same moment. A diff scan needs a diff. A runtime probe
# needs a deployment. Asking those questions before the work is done produces
# UNKNOWN, and an UNKNOWN escalates, which is how every delegable task ends up
# requiring a human for a question nobody could have answered yet.

PLAN = "plan"          # checkable before acting. A precondition.
EVIDENCE = "evidence"  # checkable only after. A postcondition.
BOTH = "both"          # the default: meaningful at either moment.

# -- entities and capabilities ---------------------------------------------

ENTITIES = ("task", "idea", "asset", "ddna", "knowledge")
CAPABILITIES = ("escd", "voice", "supabase", "github", "deployment", "filehandling")


def now() -> float:
    return time.time()


def new_id(prefix: str) -> str:
    return prefix + "_" + uuid.uuid4().hex[:12]


def sig(payload: Any) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode("utf-8")
    ).hexdigest()[:16]


@dataclass
class Operation:
    """One thing someone is trying to do.

    `facts` is deliberately a flat dict and deliberately allowed to be
    incomplete. A missing fact is the normal case, not an error, and the
    difference between a missing fact and a withheld one is what separates
    UNKNOWN from FAIL.
    """
    entity: str
    action: str
    capabilities: Sequence[str] = field(default_factory=tuple)
    facts: Dict[str, Any] = field(default_factory=dict)
    actor: str = "unknown"
    lane: str = "DCSE"
    directive: str = ""
    id: str = field(default_factory=lambda: new_id("op"))
    at: float = field(default_factory=now)

    def has(self, key: str) -> bool:
        """Present and not empty. None, "" and [] all count as absent."""
        v = self.facts.get(key, None)
        return not (v is None or v == "" or v == [] or v == {})

    def get(self, key: str, default: Any = None) -> Any:
        return self.facts.get(key, default)

    def signature(self) -> str:
        """Groups repeats of the same case, so five reruns cannot look like
        five confirmations when the register counts them."""
        return sig({"entity": self.entity, "action": self.action,
                    "capabilities": sorted(self.capabilities),
                    "facts": sorted(self.facts.keys())})


@dataclass
class Rule:
    """One predicate, plus how much the action it guards actually costs.

    `consequence` and `reversibility` describe THE ACTION WHEN THE RULE PASSES,
    not the severity of violating the rule. That distinction is not obvious and
    getting it wrong is expensive.

    Violation severity is already handled: a FAIL refuses, always, whatever the
    consequence says. So these two fields answer one question only, which is
    whether a compliant action still needs a person. Sending in someone's name
    does, because a correct send is still unsendable. Taking a file into content
    addressed storage does not, because a correct intake is reversible and
    harmless.

    Setting a guard's consequence to HIGH because violating it would be bad
    makes every compliant operation escalate, which turns the gate minimization
    principle inside out. Found by the benchmark, not by review.
    """
    id: str
    name: str
    applies_to: Sequence[str]          # entity names, capability names, or "*"
    actions: Sequence[str]             # action names, or "*"
    check: Callable[["Operation"], str]
    statement: str = ""
    reversibility: str = REVERSIBLE
    consequence: str = LOW
    lifecycle: str = CANDIDATE
    requires: Sequence[str] = field(default_factory=tuple)
    origin: str = ""
    blocking: bool = True              # a False rule reports but never refuses
    stage: str = BOTH                  # plan, evidence, or both

    def in_stage(self, stage: str) -> bool:
        return self.stage == BOTH or stage == BOTH or self.stage == stage

    def triggered_by(self, op: "Operation") -> bool:
        scope = set(self.applies_to)
        if "*" not in scope:
            touched = {op.entity} | set(op.capabilities)
            if not (scope & touched):
                return False
        if "*" not in set(self.actions) and op.action not in set(self.actions):
            return False
        return True


@dataclass
class RuleResult:
    rule_id: str
    verdict: str
    detail: str = ""
    binding: bool = True               # False when the rule ran in shadow
    missing: Sequence[str] = field(default_factory=tuple)
    ruleset: str = ""
    version: str = "0.2.1"
    status: str = "OPERATIVE"
    source_ref: str = ""
    severity: str = "NORMAL"
    disposition: str = ""
    evidence_refs: Sequence[str] = field(default_factory=tuple)


@dataclass
class Plan:
    operation: Operation
    results: List[RuleResult] = field(default_factory=list)
    reversibility: str = REVERSIBLE
    consequence: str = LOW

    def binding(self) -> List[RuleResult]:
        return [r for r in self.results if r.binding]

    def failures(self) -> List[RuleResult]:
        return [r for r in self.binding() if r.verdict == FAIL]

    def unknowns(self) -> List[RuleResult]:
        return [r for r in self.binding() if r.verdict == UNKNOWN]

    def shadow(self) -> List[RuleResult]:
        return [r for r in self.results if not r.binding]


@dataclass
class Outcome:
    operation_id: str
    disposition: str
    reason: str
    plan: Plan
    executed: bool = False
    execution: Dict[str, Any] = field(default_factory=dict)
    evidence_id: str = field(default_factory=lambda: new_id("ev"))
    at: float = field(default_factory=now)

    def evidence(self) -> Dict[str, Any]:
        """What actually happened, in a form a later reader can check without
        trusting this narrative."""
        return {
            "evidence_id": self.evidence_id,
            "at": self.at,
            "operation": {
                "id": self.operation_id,
                "entity": self.plan.operation.entity,
                "action": self.plan.operation.action,
                "capabilities": list(self.plan.operation.capabilities),
                "actor": self.plan.operation.actor,
                "lane": self.plan.operation.lane,
                "directive": self.plan.operation.directive,
                "signature": self.plan.operation.signature(),
                "facts_present": sorted(self.plan.operation.facts.keys()),
            },
            "disposition": self.disposition,
            "reason": self.reason,
            "executed": self.executed,
            "execution": self.execution,
            "rules": [asdict(r) for r in self.plan.results],
            "counts": {
                "evaluated": len(self.plan.results),
                "binding": len(self.plan.binding()),
                "shadow": len(self.plan.shadow()),
                "fail": len(self.plan.failures()),
                "unknown": len(self.plan.unknowns()),
            },
        }


def disposition_for(plan: Plan) -> tuple:
    """Deterministic. Returns (disposition, reason).

    Order matters and is argued for:

      A binding FAIL refuses. A rule that triggered and was not satisfied is
      the system saying no, and no amount of reversibility makes that an
      execute.

      A binding UNKNOWN escalates rather than refusing. Missing knowledge is
      not misconduct. Somebody has to supply it or decide to proceed without.

      Then reversibility and consequence decide the rest, which is the gate
      minimization principle as arithmetic.
    """
    fails = plan.failures()
    if fails:
        return REFUSE, "%d rule%s failed: %s" % (
            len(fails), "" if len(fails) == 1 else "s",
            ", ".join(r.rule_id for r in fails[:5]))
    unknowns = plan.unknowns()
    if unknowns:
        missing: Set[str] = set()
        for r in unknowns:
            missing.update(r.missing)
        if missing:
            return ESCALATE, "missing: %s" % ", ".join(sorted(missing)[:6])
        # A rule can be unresolved without naming a field, so name the rule.
        # "unstated facts" tells the reader nothing they can act on.
        return ESCALATE, "unresolved: %s" % ", ".join(
            r.rule_id for r in unknowns[:6])
    if plan.reversibility == IRREVERSIBLE:
        return ESCALATE, "irreversible action requires a decision"
    if plan.consequence == HIGH:
        return ESCALATE, "high consequence requires a decision"
    if plan.reversibility == RESIDUAL or plan.consequence == MODERATE:
        return EXECUTE_AS_CANDIDATE, "reversible with residue, writes to the candidate layer"
    return EXECUTE, "reversible and low consequence"
