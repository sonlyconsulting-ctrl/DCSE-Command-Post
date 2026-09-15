# DCSE Rule-Stage Lifecycle Specification

## The Core Distinction: Precondition vs Postcondition

A rules engine must distinguish between rules that gate an attempt and rules that verify the result.

```
       [ PRECONDITION ]
      Does the actor have authority?
      Is the target scope approved?
      Is the proposed operation reversible?
              |
              v (Pass)
        [ EXECUTION ]
      Perform reversible edit / local action
              |
              v
      [ POSTCONDITION ]
      Does the git diff contain secrets (GH-05)?
      Did the schema migration preserve rollback?
              |
              v
          [ AUDIT ]
      Were acceptance criteria met?
      Did benchmark score regress?
```

### Problem Solved
If a postcondition rule (e.g. `GH-05: No credential shapes in a diff`) is evaluated during the planning phase before any diff exists, it returns `UNKNOWN`. If `UNKNOWN` escalates a reversible action to a human before any execution has occurred, the assistant is paralyzed and cannot make simple reversible branch edits.

### Solution
- `stage="plan"`: Evaluates preconditions. Excludes postcondition diff/runtime verification rules.
- `stage="evidence"`: Evaluates postconditions. Preserves `UNKNOWN` if evidence cannot be established after execution.
- `stage="audit"`: Evaluates acceptance benchmarks and regression baselines.
