"""Supabase capability rules.

Database work, governed by what actually went wrong rather than by what could
theoretically go wrong. The service role key bypasses row level security
entirely, which is why an agent never holds it: handing it over removes every
boundary the rest of the estate depends on.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, IRREVERSIBLE, MODERATE, Operation, RESIDUAL
from predicates import (all_pass, falsy, no_credentials, required, truthy, when)
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / database governance"
WRITES = ("insert", "update", "upsert", "write")
DESTRUCTIVE = ("drop", "truncate", "delete_all", "destructive_alter")


@rule("SB-01", "A write is verified by reading it back", ["supabase"],
      actions=list(WRITES), stage=EVIDENCE, origin=ORIGIN,
      statement=("The same transaction shape as storage. A write that was not "
                 "read back is a write that was reported, not confirmed."))
def _(op: Operation) -> str:
    return when(op.action in WRITES, truthy(op, "readback_verified"))


@rule("SB-02", "No credential shapes in a payload", ["supabase"],
      consequence=HIGH, reversibility=IRREVERSIBLE, origin=ORIGIN,
      statement=("A credential written into a row is disclosed to everyone who "
                 "can read that row, now and retroactively."))
def _(op: Operation) -> str:
    return no_credentials(op, "payload", "query", "values")


@rule("SB-03", "Schema change goes through a migration", ["supabase"],
      actions=["alter", "create_table", "add_column", "migrate"],
      reversibility=RESIDUAL, consequence=MODERATE, origin=ORIGIN,
      statement=("Ad hoc DDL against a live project leaves no reviewable record "
                 "and no path back."))
def _(op: Operation) -> str:
    return when(op.action in ("alter", "create_table", "add_column", "migrate"),
                required(op, "migration_ref"))


@rule("SB-04", "Destructive work ships with its reversal", ["supabase"],
      actions=list(DESTRUCTIVE), reversibility=IRREVERSIBLE, consequence=HIGH,
      origin=ORIGIN,
      statement=("Destruction is the class with no before to return to, so the "
                 "before has to be manufactured in advance or the action does "
                 "not run."))
def _(op: Operation) -> str:
    return when(op.action in DESTRUCTIVE,
                all_pass(required(op, "reversal_script"), truthy(op, "backup_verified")))


@rule("SB-05", "An agent does not hold the service role", ["supabase"],
      consequence=HIGH, origin=ORIGIN,
      statement=("The service role bypasses row level security entirely. An "
                 "agent using it is an agent with no boundaries at all."))
def _(op: Operation) -> str:
    return falsy(op, "uses_service_role")
