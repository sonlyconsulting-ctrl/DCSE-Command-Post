"""GitHub capability rules.

Source control, governed by the transaction envelope. The envelope is not
permission, it is the receipt that makes a change attributable and therefore
reversible. You cannot undo what you cannot attribute.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, MODERATE, Operation, PASS, FAIL
from predicates import falsy, no_credentials, present, required, when
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / ATGS transaction envelope"
NAMESPACES = ("feature/", "fix/", "release/", "chore/", "evidence/")


@rule("GH-01", "Every change carries a transaction envelope", ["github"],
      actions=["push", "commit", "pr_open"], consequence=MODERATE, origin=ORIGIN,
      statement=("Agent, class, task, directive, lane and the hash of the "
                 "rulebook the agent actually read. The last field is what "
                 "turns allegiance from a promise into a comparison."))
def _(op: Operation) -> str:
    return when(op.action in ("push", "commit", "pr_open"),
                required(op, "agent_id", "agent_class", "directive", "policy_hash"))


@rule("GH-02", "Branches use the approved namespace", ["github"],
      actions=["push", "pr_open", "create_branch"], origin=ORIGIN,
      statement="An agent does not get to invent a branch namespace.")
def _(op: Operation) -> str:
    if not op.has("branch"):
        return PASS
    return PASS if str(op.get("branch")).startswith(NAMESPACES) else FAIL


@rule("GH-03", "A superseded branch is not merged as a set", ["github"],
      actions=["pr_open", "merge"], consequence=HIGH, origin=ORIGIN,
      statement=("Material on a superseded branch may be ported commit by "
                 "commit under review. It is never merged wholesale, because "
                 "that reintroduces everything nobody looked at."))
def _(op: Operation) -> str:
    return when(op.action in ("pr_open", "merge"), falsy(op, "branch_superseded"))


@rule("GH-04", "Changed paths fall inside the declared scope", ["github"],
      actions=["push", "commit", "pr_open"], consequence=MODERATE, origin=ORIGIN,
      statement=("A single out of scope file fails the whole transaction. Scope "
                 "that stretches to fit the change is not scope."))
def _(op: Operation) -> str:
    if not (op.has("changed_paths") and op.has("declared_scope")):
        return PASS if not op.has("changed_paths") else FAIL
    scope = tuple(op.get("declared_scope"))
    bad = [p for p in op.get("changed_paths") if not str(p).startswith(scope)]
    return PASS if not bad else FAIL


@rule("GH-05", "No credential shapes in a diff", ["github"],
      consequence=HIGH, stage=EVIDENCE, origin=ORIGIN,
      statement=("Caught at the push rather than at review, because a secret "
                 "that reached the remote is compromised whatever happens next."))
def _(op: Operation) -> str:
    return no_credentials(op, "diff", "added_lines")
