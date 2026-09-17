"""Knowledge entity rules.

Knowledge is material the estate relies on being true. The failure mode is not
losing it, it is quietly holding two versions and not knowing which one is in
force, so most of these rules are about authority and supersession.

KN-04 is the amendment the other surface made to my design and they were right.
Desk drops what it cannot classify, which suits a personal tool where the source
is one click away. Enterprise evidence is retained as UNCLASSIFIED, because an
unread line may matter later and its absence is unrecoverable.
"""
from __future__ import annotations

from model import MODERATE, Operation, FAIL, PASS
from predicates import falsy, one_of, present, required, when
from registry import rule

AUTHORITY_LEVELS = ("stated", "derived", "observed", "assumed", "unclassified")
ORIGIN = "DCSE-GOV-20260913 / knowledge provenance"


@rule("KN-01", "A record has a stable identity", ["knowledge"], origin=ORIGIN)
def _(op: Operation) -> str:
    return present(op, "knowledge_id")


@rule("KN-02", "A record names its source", ["knowledge"], origin=ORIGIN,
      statement=("Knowledge with no source cannot be re-examined and cannot be "
                 "retired when its source is withdrawn."))
def _(op: Operation) -> str:
    return present(op, "source_ref")


@rule("KN-03", "A record carries an authority level", ["knowledge"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("Stated, derived, observed and assumed are different kinds of "
                 "true and must not be stored as one kind."))
def _(op: Operation) -> str:
    return one_of(op, "authority", AUTHORITY_LEVELS)


@rule("KN-04", "Unclassifiable material is retained, never invented or dropped",
      ["knowledge"], origin=ORIGIN + " / amendment from the second surface",
      statement=("Material that cannot be classified with confidence is kept "
                 "with its source and marked unclassified. It is never assigned "
                 "a class to populate a field."))
def _(op: Operation) -> str:
    if op.get("authority") == "unclassified" and not op.has("source_ref"):
        return FAIL
    return falsy(op, "value_inferred")


@rule("KN-05", "A revision supersedes rather than overwrites", ["knowledge"],
      actions=["update", "revise"], consequence=MODERATE, origin=ORIGIN,
      statement=("A new version marks the old one superseded and keeps it. The "
                 "previous reading is how a wrong correction gets caught."))
def _(op: Operation) -> str:
    return when(op.action in ("update", "revise"), required(op, "supersedes"))
