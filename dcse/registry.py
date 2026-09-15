"""Rule registry and the lifecycle gate.

Two jobs.

    Registration     one id, one rule, no silent redefinition. A duplicate id
                     raises rather than overwriting, because a rule that
                     quietly replaced another is the worst kind of drift: the
                     old one still appears in the inventory.

    The gate         only PROVISIONAL and ACTIVE rules can change an outcome.
                     CANDIDATE rules evaluate, record and change nothing.
                     DEPRECATED and RETIRED rules do not run at all.

That gate is the whole reason a rule base can grow safely. A new rule joins in
shadow, accumulates firings against real operations, and earns its way to
binding through the register's promotion transitions. Nothing has to be right
on the day it is written, and nothing untested can block work.
"""
from __future__ import annotations

import importlib
import pkgutil
from typing import Callable, Dict, List, Optional, Sequence

from model import (ACTIVE, BINDING, BOTH, CANDIDATE, INERT, PROVISIONAL,
                   SHADOW, LOW, REVERSIBLE, Operation, Rule)


class DuplicateRuleId(ValueError):
    pass


class Registry:
    def __init__(self) -> None:
        self._rules: Dict[str, Rule] = {}
        self._order: List[str] = []

    # -- registration --------------------------------------------------

    def register(self, rule: Rule) -> Rule:
        if rule.id in self._rules:
            raise DuplicateRuleId(
                "rule id %r is already registered by %r. Ids are unique so an "
                "inventory cannot show two different rules under one name."
                % (rule.id, self._rules[rule.id].name))
        self._rules[rule.id] = rule
        self._order.append(rule.id)
        return rule

    def rule(self, rule_id: str) -> Optional[Rule]:
        return self._rules.get(rule_id)

    def all(self) -> List[Rule]:
        return [self._rules[i] for i in self._order]

    def ids(self) -> List[str]:
        return list(self._order)

    def __len__(self) -> int:
        return len(self._rules)

    # -- lifecycle -----------------------------------------------------

    def set_lifecycle(self, rule_id: str, lifecycle: str) -> None:
        r = self._rules[rule_id]
        r.lifecycle = lifecycle

    def bind_all(self, lifecycle: str = PROVISIONAL) -> int:
        """Used by the suite and by a deliberate operator action. Never called
        automatically, because a rule base that promotes itself is the loop
        confirming its own bias."""
        n = 0
        for r in self._rules.values():
            if r.lifecycle == CANDIDATE:
                r.lifecycle = lifecycle
                n += 1
        return n

    # -- resolution ----------------------------------------------------

    def applicable(self, op: Operation, stage: str = BOTH) -> List[Rule]:
        """Rules that trigger on this operation and are not inert.

        This is the entity by capability decomposition doing its work: a rule
        is written once against a capability and reached by whichever entity
        invokes it, rather than copied per entity.
        """
        return [r for r in self.all()
                if r.lifecycle not in INERT and r.triggered_by(op)
                and r.in_stage(stage)]

    def inventory(self) -> Dict[str, Dict[str, int]]:
        by_life: Dict[str, int] = {}
        by_scope: Dict[str, int] = {}
        for r in self.all():
            by_life[r.lifecycle] = by_life.get(r.lifecycle, 0) + 1
            for s in r.applies_to:
                by_scope[s] = by_scope.get(s, 0) + 1
        return {"by_lifecycle": by_life, "by_scope": by_scope,
                "total": {"rules": len(self._rules)}}


REGISTRY = Registry()


def rule(rule_id: str, name: str, applies_to: Sequence[str],
         actions: Sequence[str] = ("*",), statement: str = "",
         reversibility: str = REVERSIBLE, consequence: str = LOW,
         requires: Sequence[str] = (), origin: str = "",
         blocking: bool = True, lifecycle: str = CANDIDATE,
         stage: str = BOTH) -> Callable:
    """Decorator. The function body is the predicate and takes an Operation.

        @rule("TASK-06", "Complete requires completion evidence",
              applies_to=["task"], actions=["complete"])
        def _(op): ...
    """
    def wrap(fn: Callable[[Operation], str]) -> Callable[[Operation], str]:
        REGISTRY.register(Rule(
            id=rule_id, name=name, applies_to=tuple(applies_to),
            actions=tuple(actions), check=fn, statement=statement or fn.__doc__ or "",
            reversibility=reversibility, consequence=consequence,
            lifecycle=lifecycle, requires=tuple(requires), origin=origin,
            blocking=blocking, stage=stage))
        return fn
    return wrap


def load_rules(package: str = "rules") -> Registry:
    """Import every rule module once. Importing twice would raise on duplicate
    ids, which is the protection working rather than a bug."""
    if getattr(load_rules, "_loaded", False):
        return REGISTRY
    pkg = importlib.import_module(package)
    for mod in pkgutil.iter_modules(pkg.__path__):
        if mod.name.startswith("_"):
            continue
        importlib.import_module("%s.%s" % (package, mod.name))
    load_rules._loaded = True  # type: ignore[attr-defined]
    return REGISTRY
