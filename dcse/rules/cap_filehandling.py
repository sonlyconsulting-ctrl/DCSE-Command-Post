"""File handling capability rules.

The intake lifecycle, which is where evidence enters the estate. Everything
downstream inherits whatever discipline is or is not applied here, which is why
these rules are stricter than they look.

The layering they enforce: the source file is immutable evidence, anything read
out of it is derived and regenerable, and only a recorded decision is
operational truth. Nothing promotes itself from one layer to the next.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, MODERATE, Operation, PASS, FAIL
from predicates import (all_pass, falsy, hash_ok, present, required, resolves,
                        truthy, when)
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / file lifecycle"


@rule("FILE-01", "Intake is one transaction or it is nothing", ["filehandling"],
      actions=["take", "upload", "ingest"], stage=EVIDENCE, origin=ORIGIN,
      statement=("Hash, write, read back, compare, and only then record. Any "
                 "failure records nothing at all, so a row pointing at an "
                 "absent object cannot come into existence."))
def _(op: Operation) -> str:
    if op.action not in ("take", "upload", "ingest"):
        return PASS
    return all_pass(hash_ok(op, "content_hash"),
                    required(op, "readback_hash"),
                    PASS if op.get("readback_hash") == op.get("content_hash") else FAIL)


@rule("FILE-02", "One destination, pre-provisioned, and it resolves",
      ["filehandling"], actions=["take", "upload", "ingest"], stage=EVIDENCE, origin=ORIGIN,
      statement=("Not a chain of destinations selected by failure. A fallback "
                 "chain is an undefined destination wearing a definition, and "
                 "afterwards nobody can say which link holds the file."))
def _(op: Operation) -> str:
    if op.action not in ("take", "upload", "ingest"):
        return PASS
    return all_pass(falsy(op, "runtime_provisioned"),
                    falsy(op, "fallback_used"),
                    resolves(op, "storage_ref", "object_present"))


@rule("FILE-03", "A reread supersedes, it does not overwrite", ["filehandling"],
      actions=["read", "reread", "extract"], origin=ORIGIN,
      statement=("A better extractor later must never destroy what an earlier "
                 "one saw, because the earlier reading is how a wrong "
                 "improvement gets noticed."))
def _(op: Operation) -> str:
    return when(op.action in ("read", "reread", "extract"),
                falsy(op, "overwrites_prior_reading"))


@rule("FILE-04", "Facts and frames are separate objects", ["filehandling"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("A fact records what the evidence establishes. A frame records "
                 "an interpretation of it against an objective. Protection is "
                 "absent is a fact; calling it a gap is a frame."))
def _(op: Operation) -> str:
    if op.has("frames") and not op.has("facts"):
        return FAIL
    return when(op.has("frames"), required(op, "frame_derived_from"))


@rule("FILE-05", "A desired state traces to an objective", ["filehandling"],
      consequence=MODERATE, origin=ORIGIN,
      statement=("A to-be with no trace to a stated objective, requirement, "
                 "doctrine reference or explicit direction is a proposal and is "
                 "labelled one. Untraced, it is wishful thinking with a "
                 "confident format."))
def _(op: Operation) -> str:
    return when(op.has("to_be"), required(op, "objective_ref"))
