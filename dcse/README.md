# DCSE rule orchestrator

    python -m dcse test         the suite
    python -m dcse bench        the scenario benchmark
    python -m dcse demo         the ESCD production gate, run through the rules
    python -m dcse inventory    what is registered and in what state

Standard library only. Python 3.9 or newer.

    60 rules, 127 cases, 0 failures.
    5 scenarios, 21 steps, score 1.00.

## The two designs, resolved

Two architectures were live and neither superseded the other. They are not
alternatives. One describes which rules apply to an operation, the other
describes which rules are allowed to exist. They sit at different layers and
this package runs both.

    entity x capability     resolves which rules apply     from the second surface
    lifecycle gate          filters which of those bind    from the register
    orchestrator            evaluates, disposes, executes  neither had this

They conflicted in exactly one place, two verdict vocabularies, and that was
decided rather than merged.

**A rule evaluates.** PASS, FAIL or UNKNOWN. The distinction between the last
two is not a judgment call: missing knowledge is UNKNOWN, evidence that a
triggered rule explicitly required and did not receive is FAIL. A Task marked
COMPLETE with nothing behind it is a failed claim, not a gap.

**An operation is disposed of.** EXECUTE, EXECUTE_AS_CANDIDATE, ESCALATE or
REFUSE, computed from the results plus reversibility and consequence. REGENERATE
is not an operation verdict at all. It is a lifecycle action on a rule and it
belongs in the register.

Collapsing those two vocabularies is how "the rule passed" becomes "the
deployment is fine", which is the specific error this whole program exists to
stop.

## The shadow gate

Only PROVISIONAL and ACTIVE rules can change an outcome. CANDIDATE rules
evaluate, record their firing, and block nothing.

That one property is what lets the rule base grow safely. A new rule joins in
shadow, accumulates firings against real work, and earns its way to binding
through the register's promotion transitions. Nothing has to be correct on the
day it is written, and nothing untested can ever stop work.

It also means an inventory number is not a capability claim. Sixty registered
rules with every one in candidate is a system that refuses nothing, and the
inventory says so plainly rather than implying otherwise.

## Why sixty and not a hundred and forty eight

The suite enforces two things before it runs a single case:

    every registered rule has at least one case
    every registered rule has at least one case that expects a refusal

The second is the one that matters. A rule shown only to allow correct input is
unproven. If a rule cannot be made to fail on purpose, either it does nothing
or nobody understands it, and both should stop a build.

Twelve tests against a hundred and forty eight rules tells you about the suite,
not about the rules. Sixty rules that can each be shown to refuse is a smaller
number and a larger claim.

## The demo

`python -m dcse demo` runs the deployment that has been blocking production,
using the facts from the gate report. The canonical commit is on main, the
configuration validator passed, and the platform then failed looking for a build
artifact the project was never going to emit.

    disposition REFUSE
    reason      1 rule failed: DEP-02
    DEP-02      FAIL   A gate is not a build

The refusal happens before the platform is ever called and it names the rule
rather than a platform error code. Nothing in the pipeline had asked the one
question that would have caught it: a gate passed, but did anything get built.

The second half of the demo runs the same release with the validator moved out
of the build command slot. It escalates rather than executing, with no rule
failing, because promotion to production is irreversible and that is the one
place a gate belongs.

## What the disposition rules are

In order, and every branch is a comparison rather than a judgment.

1. A binding FAIL refuses. A rule that triggered and was not satisfied is the
   system saying no, and no amount of reversibility makes that an execute.
2. A binding UNKNOWN escalates. Missing knowledge is not misconduct. Somebody
   has to supply it or decide to proceed without it.
3. Irreversible, or high consequence, escalates.
4. Residual, or moderate consequence, writes to the candidate layer.
5. Everything else executes.

A rule scoped to particular actions sets the operation's risk profile, because
it is describing what those actions cost. A rule that applies to every action is
stating an invariant, and its consequence describes the severity of violating it
rather than the risk of the work. Letting invariants set the profile makes
escalation the default for anything serious even when it complies, which is the
opposite of gate minimization.

That distinction was found by a test, not by design.

## Adapters

Every capability defaults to an adapter that performs nothing and says so. A
system whose default is a convincing no-op reports work it did not do, and that
had already happened four times before anyone noticed.

## Files

    model.py          Operation, Rule, Plan, Outcome, and the disposition function
    predicates.py     the shared predicate library, one condition written once
    registry.py       registration, duplicate id protection, the lifecycle gate
    orchestrator.py   resolve, evaluate, dispose, execute, record, emit evidence
    adapters.py       capability doors, honest by default
    rules/            five entity sets, six capability sets
    tests.py          the suite and its two coverage assertions

## The benchmark

A unit case proves one rule behaves. A scenario proves the system handles a
whole realistic operation, which is a different claim and catches the class of
defect that only appears when rules interact.

    BENCH-01  the assistant is asked to help build out its own rules
    BENCH-02  the ESCD production gate, as it actually stands
    BENCH-03  a file arrives and becomes work
    BENCH-04  the assistant is asked to send something in your name
    BENCH-05  the assistant is asked to do something it already advised against

BENCH-01 is the recursive one and the load bearing step is the fifth: the
assistant proposes a rule, which is cheap and reversible and is not gated, and
then tries to adopt it, which is refused. No model may put its own proposal into
force. If that step ever passes by executing, the governance model is
decorative.

Every scenario declares what it expects before it runs, and the runner refuses a
scenario with no expectations rather than scoring it zero. Expectations written
after seeing output describe behaviour; they do not test it.

### Scaling without regressing

    python -m dcse bench --save baseline.json
    python -m dcse bench --against baseline.json

The second form reports what moved, regressions first. That is the question that
matters as rules are added, because the failure mode of incremental work is a
change that fixes one case and quietly breaks another nobody re-ran.

The detector has been shown to detect. Weakening VOICE-03 to accept any message
class, the kind of change that reads as a simplification, produces:

    baseline score 1.00, now 0.95
    regressed  BENCH-04::confirming an appointment is not agreeing to terms

### What the benchmark found

The first run failed one scenario, and the rules were wrong rather than the
expectation. Taking a file into storage was escalating to a human every time.

The cause was a confusion worth naming: a rule's consequence and reversibility
describe the action when the rule PASSES, not the severity of violating it.
Violation severity is already handled, because a FAIL refuses regardless. So
those two fields answer one question only, which is whether a compliant action
still needs a person. A correct send does, because it is still unsendable. A
correct intake does not, because it is reversible and harmless.

Setting a guard to high consequence because violating it would be bad makes
every compliant operation escalate, which turns gate minimization inside out.
Eleven rules were recalibrated.

## Status

CANDIDATE. Every rule is in candidate lifecycle, which means this refuses
nothing until someone promotes it deliberately. It has no canonical repository,
no commit and no runtime reference, so by the authority order it is not
operative and should not be described as such.

Six capabilities are covered, not eighteen. The missing twelve are not written
rather than written and unproven, which is the same discipline the rule count
reflects.
