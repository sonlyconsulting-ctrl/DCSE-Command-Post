"""Command line entry.

    python -m dcse inventory              what is registered and in what state
    python -m dcse demo                   the live ESCD production gate, run
    python -m dcse test                   the suite
    python -m dcse run --entity task --action promote --cap deployment \
                       --fact build_command_is_validator=true
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import PROVISIONAL, Operation  # noqa: E402
from orchestrator import Orchestrator  # noqa: E402
from registry import REGISTRY, load_rules  # noqa: E402


def parse_fact(raw: str):
    key, _, value = raw.partition("=")
    low = value.strip().lower()
    if low in ("true", "false"):
        return key.strip(), low == "true"
    if low in ("none", "null", ""):
        return key.strip(), None
    if "," in value:
        return key.strip(), [v.strip() for v in value.split(",") if v.strip()]
    try:
        return key.strip(), float(value) if "." in value else int(value)
    except ValueError:
        return key.strip(), value.strip()


def cmd_inventory(_args) -> int:
    load_rules()
    inv = REGISTRY.inventory()
    print("\n  %d rules registered\n" % inv["total"]["rules"])
    print("  lifecycle  " + json.dumps(inv["by_lifecycle"]))
    print("  scope      " + json.dumps(inv["by_scope"]))
    print()
    for r in REGISTRY.all():
        print("  %-12s %-11s %-14s %-26s %s"
              % (r.id, r.lifecycle, r.reversibility[:12], "/".join(r.applies_to)[:26],
                 r.name))
    print()
    return 0


def cmd_demo(_args) -> int:
    """The deployment that has been failing all day, run through the rules.

    Every fact below is from the production gate report: the canonical SHA is on
    main, the ESCD configuration validator passed, and the platform then failed
    looking for a build artifact that this project was never going to emit,
    because the validator was occupying the build command slot.

    The point of the demo is not that the rules agree with the diagnosis. It is
    that the refusal happens before the platform is ever called, and it names
    the rule rather than a platform error code.
    """
    load_rules()
    REGISTRY.bind_all(PROVISIONAL)
    o = Orchestrator()

    print("\n" + "=" * 72)
    print("  ESCD production gate, as it actually stands")
    print("=" * 72)
    blocked = Operation(
        entity="task", action="promote", capabilities=("deployment", "github"),
        actor="release-agent", lane="DCSE", directive="ESCD-GOV-20260913-001",
        facts={
            "task_id": "ESCD-PROD-GATE", "objective": "certify phase 1 production",
            "acceptance_criteria": ["health probe", "runtime audit"], "owner": "DCS",
            "state": "blocked", "blocker_ref": "STATIC_BUILD_NO_OUT_DIR",
            "commit_sha": "db8ed1fbfbe140121b06fbc3f49498616ed936c7",
            "is_ancestor_of_main": True,
            "preflight_passed": True, "preflight_allows_fallback": False,
            "build_command_is_validator": True,
            "build_output_path": ".next", "build_artifact_present": False,
            "author": "release-agent", "promoter": "dcs",
            "agent_id": "release-agent", "agent_class": "A3",
            "directive": "ESCD-GOV-20260913-001", "policy_hash": "0" * 64,
            "branch": "release/escd-phase1-completion-20260913",
            "branch_superseded": False,
        })
    print(o.explain(o.run(blocked, execute=False)))

    print("\n" + "=" * 72)
    print("  the same release once the validator is out of the build slot")
    print("=" * 72)
    fixed = Operation(
        entity="task", action="promote", capabilities=("deployment", "github"),
        actor="release-agent", lane="DCSE", directive="ESCD-GOV-20260913-001",
        facts=dict(blocked.facts, **{
            "state": "open",
            "build_command_is_validator": False,
            "build_output_path": "public/",
            "build_artifact_present": True,
        }))
    print(o.explain(o.run(fixed, execute=False)))
    print()
    return 0


def cmd_run(args) -> int:
    load_rules()
    if args.bind:
        REGISTRY.bind_all(PROVISIONAL)
    facts = dict(parse_fact(f) for f in (args.fact or []))
    op = Operation(entity=args.entity, action=args.action,
                   capabilities=tuple(args.cap or []), facts=facts,
                   actor=args.actor, lane=args.lane, directive=args.directive)
    o = Orchestrator()
    outcome = o.run(op, execute=not args.no_execute)
    print("\n" + o.explain(outcome) + "\n")
    if args.evidence:
        with open(args.evidence, "w", encoding="utf-8") as fh:
            json.dump(outcome.evidence(), fh, indent=2, default=str)
        print("  evidence written to %s\n" % args.evidence)
    return 0 if outcome.disposition != "REFUSE" else 1


def cmd_tasks(args) -> int:
    """What another model reads when told to check the repository."""
    import delegation
    load_rules()
    REGISTRY.bind_all(PROVISIONAL)
    o = Orchestrator()
    packets = delegation.load_all()
    if not packets:
        print("\n  no task packets in tasks/\n")
        return 0

    invalid = []
    for p in packets:
        try:
            p.validate()
        except delegation.InvalidPacket as exc:
            invalid.append(str(exc))

    if args.id:
        for p in packets:
            if p.id == args.id:
                d = p.disposition(o)
                print("\n" + json.dumps(p.to_dict(), indent=2, sort_keys=True))
                print("\n  rules say: %s  (%s)" % (d["disposition"], d["reason"]))
                print("  approval:  %s\n"
                      % ("DCS decides" if d["needs_approval"] == "True"
                         else "the executor decides"))
                return 0
        print("\n  no packet with id %s\n" % args.id)
        return 1

    print(delegation.report(packets, o))
    if invalid:
        print("  INVALID PACKETS")
        for msg in invalid:
            print("    %s" % msg)
        print()
        return 1
    print("  python -m dcse tasks --id T-001   to read one in full")
    print("  tasks/README.md                   is the instruction for the executor\n")
    return 0


def cmd_bench(args) -> int:
    import bench
    return bench.run(args.save, args.against, not args.quiet)


def cmd_test(_args) -> int:
    import tests
    return tests.run()


def main() -> int:
    ap = argparse.ArgumentParser(prog="dcse", description="DCSE rule orchestrator.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("inventory").set_defaults(fn=cmd_inventory)
    sub.add_parser("demo").set_defaults(fn=cmd_demo)
    sub.add_parser("test").set_defaults(fn=cmd_test)

    tk = sub.add_parser("tasks")
    tk.add_argument("--id", help="print one packet in full")
    tk.set_defaults(fn=cmd_tasks)

    b = sub.add_parser("bench")
    b.add_argument("--save", help="record this run as the baseline")
    b.add_argument("--against", help="report what moved since a baseline")
    b.add_argument("--quiet", action="store_true")
    b.set_defaults(fn=cmd_bench)

    r = sub.add_parser("run")
    r.add_argument("--entity", required=True)
    r.add_argument("--action", default="inspect")
    r.add_argument("--cap", action="append")
    r.add_argument("--fact", action="append")
    r.add_argument("--actor", default="cli")
    r.add_argument("--lane", default="DCSE")
    r.add_argument("--directive", default="")
    r.add_argument("--bind", action="store_true",
                   help="treat candidate rules as binding for this run")
    r.add_argument("--no-execute", action="store_true")
    r.add_argument("--evidence", help="write the evidence record to this path")
    r.set_defaults(fn=cmd_run)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
