"""Idea entity rules.

An Idea is a proposal that has not been decided. The whole risk with this
entity is that a proposal quietly acquires the standing of a decision, so most
of these rules are about keeping that from happening by accident.
"""
from __future__ import annotations

from model import MODERATE, Operation
from predicates import one_of, present, required, when
from registry import rule

IDEA_STATES = ("candidate", "under_review", "adopted", "declined", "superseded")
ORIGIN = "DCSE-GOV-20260913 / entity engineering"


@rule("IDEA-01", "An idea has a stable identity", ["idea"], origin=ORIGIN)
def _(op: Operation) -> str:
    return present(op, "idea_id")


@rule("IDEA-02", "An idea states itself", ["idea"], origin=ORIGIN,
      statement="A title is not a proposal. The idea has to say what it is.")
def _(op: Operation) -> str:
    return present(op, "statement")


@rule("IDEA-03", "An idea records where it came from", ["idea"], origin=ORIGIN,
      statement=("Origin is what lets an idea be re-examined when the evidence "
                 "behind it turns out to be wrong."))
def _(op: Operation) -> str:
    return present(op, "origin_ref")


@rule("IDEA-04", "An undecided idea is not presented as decided", ["idea"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("Only an adopted idea may be referenced as a decision. Anything "
                 "else carries its state with it wherever it is quoted."))
def _(op: Operation) -> str:
    return one_of(op, "state", IDEA_STATES)


@rule("IDEA-05", "Adoption requires a recorded decision", ["idea"],
      actions=["adopt", "promote"], consequence=MODERATE, origin=ORIGIN,
      statement=("An idea becomes a decision through a recorded decision, never "
                 "through repetition or through nobody objecting."))
def _(op: Operation) -> str:
    return when(op.get("state") == "adopted" or op.action in ("adopt", "promote"),
                required(op, "decision_ref"))
