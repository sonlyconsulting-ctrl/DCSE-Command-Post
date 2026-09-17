"""The benchmark runner.

Runs each scenario against the current rule base, compares what happened to
what the scenario said should happen, and writes a scorecard.

The scorecard is the point. A single run tells you whether the system is right
today. Two runs compared tell you whether a change improved it, and that second
question is the one that matters as the rule base grows, because the failure
mode of incremental work is a change that fixes one case and quietly breaks
another nobody re-ran.

    python -m dcse bench                    run and report
    python -m dcse bench --save base.json   record this run as the baseline
    python -m dcse bench --against base.json  report what moved since

Two refusals are built in and both are deliberate.

    A scenario with no expectations is refused rather than scored. Expectations
    written after seeing output describe behaviour, they do not test it.

    A benchmark run binds the rule base for the duration. Candidate rules
    refuse nothing by design, so benchmarking against them measures the shadow
    gate rather than the rules.
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import PASS, PROVISIONAL, UNKNOWN  # noqa: E402
from orchestrator import Orchestrator  # noqa: E402
from registry import REGISTRY, load_rules  # noqa: E402
from scenarios import SCENARIOS, Scenario, Step  # noqa: E402


class NoExpectations(ValueError):
    pass


def check_step(o: Orchestrator, step: Step) -> Dict[str, Any]:
    if not step.expect_disposition:
        raise NoExpectations(
            "step %r declares no expected disposition. A scenario that does not "
            "say what should happen cannot tell you whether it did." % step.label)

    outcome = o.run(step.operation, execute=True)
    got = {r.rule_id: r.verdict for r in outcome.plan.results}
    misses: List[str] = []

    if outcome.disposition != step.expect_disposition:
        misses.append("disposition expected %s, got %s (%s)"
                      % (step.expect_disposition, outcome.disposition, outcome.reason))

    for rule_id, want in step.expect_rules.items():
        actual = got.get(rule_id)
        if actual is None:
            misses.append("%s did not fire at all" % rule_id)
        elif actual != want:
            misses.append("%s expected %s, got %s" % (rule_id, want, actual))

    if step.must_not_execute and outcome.executed:
        misses.append("executed when the scenario forbids it")

    return {
        "label": step.label,
        "ok": not misses,
        "misses": misses,
        "disposition": outcome.disposition,
        "reason": outcome.reason,
        "note": step.note,
        "rules_fired": len(outcome.plan.results),
        "failures": [r.rule_id for r in outcome.plan.failures()],
    }


def run_scenario(o: Orchestrator, sc: Scenario) -> Dict[str, Any]:
    if not sc.steps:
        raise NoExpectations("scenario %s has no steps" % sc.id)
    steps = [check_step(o, s) for s in sc.steps]
    return {
        "id": sc.id, "title": sc.title, "tags": list(sc.tags),
        "ok": all(s["ok"] for s in steps),
        "steps": steps,
        "passed": sum(1 for s in steps if s["ok"]),
        "total": len(steps),
    }


def scorecard(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    steps_total = sum(r["total"] for r in results)
    steps_passed = sum(r["passed"] for r in results)
    return {
        "rules_registered": len(REGISTRY),
        "scenarios": len(results),
        "scenarios_passed": sum(1 for r in results if r["ok"]),
        "steps": steps_total,
        "steps_passed": steps_passed,
        "score": round(steps_passed / steps_total, 4) if steps_total else 0.0,
        "by_scenario": {r["id"]: "%d/%d" % (r["passed"], r["total"]) for r in results},
        "by_step": {"%s::%s" % (r["id"], s["label"]): s["ok"]
                    for r in results for s in r["steps"]},
    }


def compare(current: Dict[str, Any], baseline: Dict[str, Any]) -> Dict[str, List[str]]:
    """What moved. Regressions first, because a benchmark that leads with its
    improvements is a press release."""
    cur, base = current["by_step"], baseline.get("by_step", {})
    regressed = sorted(k for k in cur if base.get(k) is True and cur[k] is False)
    fixed = sorted(k for k in cur if base.get(k) is False and cur[k] is True)
    added = sorted(k for k in cur if k not in base)
    removed = sorted(k for k in base if k not in cur)
    return {"regressed": regressed, "fixed": fixed, "added": added, "removed": removed}


def run(save: Optional[str] = None, against: Optional[str] = None,
        verbose: bool = True) -> int:
    load_rules()
    bound = REGISTRY.bind_all(PROVISIONAL)
    o = Orchestrator()

    if verbose:
        print("\n" + "=" * 74)
        print("  DCSE benchmark")
        print("  %d rules bound for this run (candidate rules refuse nothing, so"
              % bound)
        print("  benchmarking against them would measure the shadow gate)")
        print("=" * 74)

    results = [run_scenario(o, sc) for sc in SCENARIOS]

    if verbose:
        for r, sc in zip(results, SCENARIOS):
            mark = "PASS" if r["ok"] else "FAIL"
            print("\n  %-4s %-9s %s" % (mark, r["id"], r["title"]))
            print("       %s" % sc.why.replace("\n", "\n       "))
            print()
            for s in r["steps"]:
                print("       %-4s %s" % ("ok" if s["ok"] else "MISS", s["label"]))
                print("            %s  %s" % (s["disposition"], s["reason"]))
                if s["note"]:
                    print("            note: %s" % s["note"])
                for m in s["misses"]:
                    print("            MISS: %s" % m)

    card = scorecard(results)
    if verbose:
        print("\n" + "=" * 74)
        print("  scenarios %d/%d    steps %d/%d    score %.2f    rules %d"
              % (card["scenarios_passed"], card["scenarios"], card["steps_passed"],
                 card["steps"], card["score"], card["rules_registered"]))
        print("=" * 74)

    if against:
        with open(against, "r", encoding="utf-8") as fh:
            baseline = json.load(fh)
        moved = compare(card, baseline)
        print("\n  against %s" % against)
        print("    baseline score %.2f, now %.2f"
              % (baseline.get("score", 0.0), card["score"]))
        for key in ("regressed", "fixed", "added", "removed"):
            for item in moved[key]:
                print("    %-10s %s" % (key, item))
        if not any(moved.values()):
            print("    nothing moved")
        if moved["regressed"]:
            print("\n  REGRESSION. A change improved something and broke something"
                  " else.\n")
            return 1

    if save:
        with open(save, "w", encoding="utf-8") as fh:
            json.dump(card, fh, indent=2, sort_keys=True)
        print("\n  baseline written to %s" % save)

    print()
    return 0 if card["scenarios_passed"] == card["scenarios"] else 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="bench")
    ap.add_argument("--save")
    ap.add_argument("--against")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    raise SystemExit(run(a.save, a.against, not a.quiet))
