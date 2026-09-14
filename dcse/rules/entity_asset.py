"""Asset entity rules.

An Asset is a stored object with an identity derived from its content. These
rules are the ones with the most production evidence behind them, because the
attachment defect that started this whole task lives here: a metadata row that
pointed at nothing, and nothing in the system refused it.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, IRREVERSIBLE, MODERATE, Operation, PASS, FAIL, UNKNOWN
from predicates import (all_pass, falsy, hash_ok, present, required, resolves,
                        truthy, when)
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / ESCD attachment defect"


@rule("ASSET-01", "An asset has a stable identity", ["asset"], origin=ORIGIN)
def _(op: Operation) -> str:
    return present(op, "asset_id")


@rule("ASSET-02", "An asset carries a content hash", ["asset"], origin=ORIGIN,
      statement=("Identity is the hash of the bytes. A filename is a label and "
                 "two files with one name are still two assets."))
def _(op: Operation) -> str:
    return hash_ok(op, "content_hash")


@rule("ASSET-03", "The destination resolves", ["asset"], actions=["store", "write", "create"], stage=EVIDENCE, origin=ORIGIN,
      statement=("A named destination is not enough. Something has to be found "
                 "there. Substitute resolves for defined wherever it appears."))
def _(op: Operation) -> str:
    return resolves(op, "storage_ref", "object_present")


@rule("ASSET-04", "A write is verified by reading it back", ["asset"],
      actions=["store", "write", "create"], stage=EVIDENCE, origin=ORIGIN,
      statement=("Hash, write, read back from the address, compare. Only then is "
                 "metadata written. Any failure records nothing at all."))
def _(op: Operation) -> str:
    return when(op.action in ("store", "write", "create"),
                all_pass(required(op, "readback_hash"),
                         PASS if op.get("readback_hash") == op.get("content_hash")
                         else FAIL))


@rule("ASSET-05", "The source is never rewritten in place", ["asset"],
      actions=["update", "edit", "write"], origin=ORIGIN,
      statement=("Derived versions supersede. The original bytes are the one "
                 "thing in the system with no recoverable prior state."))
def _(op: Operation) -> str:
    return falsy(op, "mutates_source")


@rule("ASSET-06", "A generated asset carries its lineage", ["asset"], origin=ORIGIN,
      statement=("Anything produced from other assets names them, or the chain "
                 "from evidence to output is broken at that link."))
def _(op: Operation) -> str:
    return when(bool(op.get("generated")), required(op, "derived_from"))


@rule("ASSET-07", "Deletion removes the object and the row together", ["asset"],
      actions=["delete", "remove"], consequence=HIGH, reversibility=IRREVERSIBLE,
      stage=EVIDENCE, origin=ORIGIN,
      statement=("A half deletion leaves either an orphaned object or a row "
                 "pointing at nothing, and the second one is the defect that "
                 "started this."))
def _(op: Operation) -> str:
    return when(op.action in ("delete", "remove"),
                all_pass(truthy(op, "object_removed"), truthy(op, "metadata_removed")))
