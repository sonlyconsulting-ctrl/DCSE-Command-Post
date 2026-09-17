"""Task entity rules.

A Task is a unit of intended work. These rules govern what makes one valid and
what it must carry before it may claim a state.

The rule that matters most here is TASK-06, and it did not come from me. The
other engineering surface found it during construction: a Task marked COMPLETE
with no completion evidence originally resolved as UNKNOWN, and that is wrong.
Missing knowledge is UNKNOWN. Evidence a triggered rule explicitly required and
did not receive is FAIL. The distinction is the difference between a system
that admits what it does not know and one that accepts a claim because nobody
supplied the counter-evidence.
"""
from __future__ import annotations

from model import FAIL, HIGH, MODERATE, PASS, RESIDUAL, UNKNOWN, Operation
from predicates import all_pass, one_of, present, required, when
from registry import rule

LIFECYCLE_STATES = ("draft", "open", "blocked", "complete", "cancelled", "superseded")
ORIGIN = "DCSE-GOV-20260913 / entity engineering, both surfaces"


@rule("TASK-01", "A task has a stable identity", ["task"], origin=ORIGIN,
      statement="Every task carries an id that does not change across its life.")
def _(op: Operation) -> str:
    return present(op, "task_id")


@rule("TASK-02", "A task states its objective", ["task"], origin=ORIGIN,
      statement="A task with no objective cannot be judged complete by anyone.")
def _(op: Operation) -> str:
    return present(op, "objective")


@rule("TASK-03", "A task carries acceptance criteria", ["task"], origin=ORIGIN,
      statement=("Completion is a computed property of acceptance criteria, "
                 "never an assertion. No criteria means no computable done."))
def _(op: Operation) -> str:
    return present(op, "acceptance_criteria")


@rule("TASK-04", "A task names an owning authority", ["task"], origin=ORIGIN,
      statement="Unowned work has no one who can decide it is finished.")
def _(op: Operation) -> str:
    return present(op, "owner")


@rule("TASK-05", "Lifecycle state is from the closed set", ["task"], origin=ORIGIN,
      statement="An invented state is a state nothing knows how to handle.")
def _(op: Operation) -> str:
    return one_of(op, "state", LIFECYCLE_STATES)


@rule("TASK-06", "Complete requires completion evidence", ["task"],
      consequence=MODERATE, origin=ORIGIN + " / defect found in v0.2 construction",
      statement=("A task claiming COMPLETE must carry a reference to the evidence "
                 "of completion. Absent evidence is a failed claim, not a gap in "
                 "knowledge."))
def _(op: Operation) -> str:
    return when(op.get("state") == "complete",
                required(op, "completion_evidence"))


@rule("TASK-07", "Blocked requires a named blocker", ["task"], origin=ORIGIN,
      statement=("A task claiming BLOCKED must name what blocks it. A blocker "
                 "nobody can read is indistinguishable from avoidance."))
def _(op: Operation) -> str:
    return when(op.get("state") == "blocked", required(op, "blocker_ref"))


@rule("TASK-08", "A superseded task cannot also be complete", ["task"],
      origin=ORIGIN,
      statement=("Supersession and completion are different ends. Claiming both "
                 "makes the history unreadable."))
def _(op: Operation) -> str:
    if op.get("state") == "superseded" and op.get("completion_evidence"):
        return FAIL
    return when(op.get("state") == "superseded", required(op, "superseded_by"))
