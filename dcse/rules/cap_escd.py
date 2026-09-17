"""ESCD capability rules.

ESCD is the assistant itself: a persistent DCSE capability reached through many
surfaces, occupying the role of a senior assistant rather than a task runner.

These rules exist because a senior assistant does two things a document system
never does. It forms interpretations of your situation, and it acts on your
behalf. The first has to stay visibly separate from your own position. The
second is governed by the voice capability.
"""
from __future__ import annotations

from model import HIGH, MODERATE, Operation, PASS, FAIL
from predicates import falsy, present, required, truthy, when
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / ESCD as the DCSE personal assistant"


@rule("ESCD-01", "The principal's intent is stored apart from the assistant's reading",
      ["escd"], consequence=HIGH, origin=ORIGIN,
      statement=("What you said and what the assistant concluded you meant are "
                 "two objects. Merging them is how an assistant's inference "
                 "becomes your stated position without anyone deciding it."))
def _(op: Operation) -> str:
    if op.has("interpretation") and not op.has("principal_intent"):
        return FAIL
    return PASS


@rule("ESCD-02", "An interpretation is labelled as one", ["escd"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("Anything the assistant derived rather than received carries "
                 "that label wherever it is shown or quoted."))
def _(op: Operation) -> str:
    return when(op.has("interpretation"), truthy(op, "interpretation_labelled"))


@rule("ESCD-03", "A contradiction with a recorded decision is surfaced unasked",
      ["escd"], consequence=MODERATE, origin=ORIGIN,
      statement=("Where a proposed action conflicts with a prior recorded "
                 "decision, commitment or constraint, it is raised before "
                 "acting. Suppressing it to stay agreeable is a defect. This is "
                 "also what qualifies the assistant as an independent validator."))
def _(op: Operation) -> str:
    return when(bool(op.get("conflicts_with_record")),
                truthy(op, "contradiction_surfaced"))


@rule("ESCD-04", "Ambiguity is routed, never resolved by guessing", ["escd"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("Where the assistant cannot tell which of two readings you "
                 "meant, it asks or holds. It does not pick one and proceed as "
                 "though you had said it."))
def _(op: Operation) -> str:
    return when(bool(op.get("ambiguous")), falsy(op, "assumed_resolution"))


@rule("ESCD-05", "Bounded execution needs confidence, authority and reversibility",
      ["escd"], actions=["execute", "act"], origin=ORIGIN,
      statement=("The assistant acts without asking when all three hold. Any one "
                 "absent routes the operation rather than stopping the work."))
def _(op: Operation) -> str:
    return when(op.action in ("execute", "act"),
                required(op, "confidence", "authority_ref"))
