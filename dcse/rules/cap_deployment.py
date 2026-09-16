"""Deployment capability rules.

DEP-02 is the rule that has been blocking your production release all day,
written as a predicate. The validator was placed in the build command slot, so
it ran, printed GATE PASSED, exited zero, and emitted no build artifact. The
platform then looked for an output directory that this project was never going
to produce and stopped.

Nothing in the pipeline asked the one question that would have caught it before
the platform did: a gate passed, but did anything get built? An inspection is
not a construction, and a validator that returns zero has told you nothing about
whether an application exists.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, IRREVERSIBLE, MODERATE, Operation, PASS, FAIL
from predicates import (all_pass, different_identities, present, required,
                        truthy, when)
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / ESCD production gate"
PROMOTE = ("deploy", "promote", "release")


@rule("DEP-01", "The commit being promoted is on the canonical branch", ["deployment"],
      actions=list(PROMOTE), consequence=HIGH, origin=ORIGIN,
      statement=("Promotion takes a commit that is already an ancestor of main. "
                 "Promoting anything else makes the deployed state unlocatable "
                 "in the history."))
def _(op: Operation) -> str:
    return when(op.action in PROMOTE,
                all_pass(required(op, "commit_sha"), truthy(op, "is_ancestor_of_main")))


@rule("DEP-02", "A gate is not a build", ["deployment"], actions=list(PROMOTE),
      consequence=HIGH, origin=ORIGIN + " / STATIC_BUILD_NO_OUT_DIR",
      statement=("A passing validation step does not produce an application. "
                 "Promotion requires a build artifact at the path the project "
                 "actually emits, and a validator occupying the build command "
                 "slot produces none."))
def _(op: Operation) -> str:
    if op.action not in PROMOTE:
        return PASS
    if op.get("build_command_is_validator") is True:
        return FAIL
    return all_pass(required(op, "build_output_path"), truthy(op, "build_artifact_present"))


@rule("DEP-03", "Production configuration is verified before promotion", ["deployment"],
      actions=list(PROMOTE), consequence=HIGH, origin=ORIGIN,
      statement=("Presence, scope and reachability, with no fallback and no "
                 "continue anyway. A validator with a fallback validates "
                 "nothing. A missing production variable must never be "
                 "discoverable only from a login screen."))
def _(op: Operation) -> str:
    return when(op.action in PROMOTE,
                all_pass(truthy(op, "preflight_passed"),
                         PASS if op.get("preflight_allows_fallback") in (False, None)
                         else FAIL))


@rule("DEP-04", "The identity that wrote the change does not promote it",
      ["deployment"], actions=list(PROMOTE), reversibility=IRREVERSIBLE,
      consequence=HIGH, origin=ORIGIN,
      statement=("Separation of duties. Whoever authored it is the least able "
                 "to see what is wrong with it."))
def _(op: Operation) -> str:
    return when(op.action in PROMOTE, different_identities(op, "author", "promoter"))


@rule("DEP-05", "Deployment success is not runtime health", ["deployment"],
      actions=["verify", "certify"], consequence=HIGH, stage=EVIDENCE, origin=ORIGIN,
      statement=("READY means the platform finished. It does not mean the "
                 "application answers. Certification requires a probe against "
                 "the live surface and the deployment id it ran against."))
def _(op: Operation) -> str:
    return when(op.action in ("verify", "certify"),
                all_pass(required(op, "deployment_id"), truthy(op, "health_probe_passed")))
