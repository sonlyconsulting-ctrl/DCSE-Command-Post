"""DDNA entity rules.

These rules govern the known behaviour of the entity and deliberately do not
invent an expansion for the acronym or semantics nobody stated. That restraint
came from the other surface and it is correct: a rule set that guesses what its
subject means encodes the guess as doctrine.

The governing design decision here is that capture is permissive and promotion
is gated. Whether something is worth noticing is a judgment and judgments are
not admissible as rules. Whether something becomes operational is a transition
and transitions are exactly what rules are for.
"""
from __future__ import annotations

from model import HIGH, MODERATE, Operation
from predicates import lane_clear, one_of, present, required, when
from registry import rule

DDNA_STATES = ("captured", "staged", "candidate", "promoted", "superseded", "retired")
ORIGIN = "DCSE-GOV-20260913 / gate the promotion, not the noticing"


@rule("DDNA-01", "A record has a stable identity", ["ddna"], origin=ORIGIN)
def _(op: Operation) -> str:
    return present(op, "record_id")


@rule("DDNA-02", "A record declares its lane", ["ddna"], consequence=MODERATE,
      origin=ORIGIN,
      statement="Lane is assigned at capture, not inferred later from content.")
def _(op: Operation) -> str:
    return present(op, "lane")


@rule("DDNA-03", "A record carries a sensitivity verdict", ["ddna"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("Sensitivity is decided once, at capture, and travels with the "
                 "record. Deciding it at use time means deciding it repeatedly "
                 "and differently."))
def _(op: Operation) -> str:
    return present(op, "sensitivity")


@rule("DDNA-04", "Capture is open, promotion is gated", ["ddna"],
      actions=["promote"], consequence=MODERATE, origin=ORIGIN,
      statement=("Anything may be captured. Only a recorded decision moves a "
                 "record to promoted, and nothing reaches operational state by "
                 "having been extracted."))
def _(op: Operation) -> str:
    return when(op.action == "promote" or op.get("state") == "promoted",
                required(op, "decision_ref"))


@rule("DDNA-05", "Protected lane material stays in its lane", ["ddna"],
      consequence=HIGH, origin=ORIGIN,
      statement=("The one condition that never softens to unknown. A cross lane "
                 "transaction touching a protected lane fails."))
def _(op: Operation) -> str:
    return lane_clear(op)
