# For the model executing these tasks

You have been told to check this repository and run the latest task from Claude
desktop. This file is what that means.

## What to do

    python -m dcse tasks

That prints every task, its status, whether it is runnable, and whether it needs
DCS approval. The arrow marks the next runnable one. A task with unmet
`depends_on` is not runnable no matter how urgent it looks.

Open `tasks/<id>.json`. Read all of it before touching anything, particularly
`scope`, `forbidden` and `acceptance`.

## The five fields that matter

**scope** is the only place you may write. Paths outside it are out of bounds
even when the change would obviously be an improvement. If the task cannot be
done inside its scope, stop and report that, because a scope that stretches to
fit the work is not a scope.

**steps** are ordered. They are not suggestions and they are not a summary of an
approach you may substitute.

**acceptance** is a list of commands and what their output must show. Run every
one. Paste the actual output into your report rather than describing it. A
summary of a test result is not a test result.

**forbidden** is not advisory. Each line is there because doing that thing has
already gone wrong once.

**needs_approval** is computed from the rules, not asserted by whoever wrote the
task. When it says yours, stop at the point of the irreversible act and report.
Do not perform it and then ask.

## What you may decide alone

Anything the rules dispose of as EXECUTE or EXECUTE_AS_CANDIDATE. That is most
of the work: reading, editing inside scope, writing tests, running the suite,
committing to a branch.

## What you may not

Anything disposed as ESCALATE or REFUSE. In practice that is a short list and it
is short on purpose: deploying or promoting to production, sending anything in
the principal's name, destructive database work, making storage public, and
putting any proposal of your own into force. Propose freely. Adopt nothing.

Check before you act:

    python -m dcse run --entity <entity> --action <action> --cap <capability> --bind

If it returns ESCALATE or REFUSE, that is your answer and the reason names the
rule.

## Before you report

    python -m dcse test
    python -m dcse bench --against baseline.json

The first proves the rules still behave. The second proves you did not fix one
thing while breaking another, which is the failure mode of incremental work and
the reason the baseline exists. Any line reading `regressed` means stop and
report rather than continue.

If `baseline.json` is absent, generate it with `--save baseline.json` on an
unmodified checkout first, and say in your report that you did, because a
baseline taken after your change proves nothing.

## Your report

Return what the task's `report` field asks for, and these four regardless:

1. The branch and commit sha.
2. Every acceptance command's real output, pasted.
3. Anything you could not do inside scope.
4. Anything you were about to do and stopped because the rules escalated it.

The fourth is the most useful line in the report and it is usually the one left
out. A run with nothing in it either did nothing consequential or did something
consequential without noticing.

## If a rule blocks you and you think it is wrong

Say so. Do not weaken the rule to get past it. A rule that is wrong is a real
finding and it gets recorded, examined, and changed deliberately. A rule quietly
softened to make a build go green is how a rule base stops meaning anything, and
recovering from that is much harder than reading a complaint.
