# DCSE Rules Engineering — OPERATIVE v0.2

Status: **OPERATIVE**

Canonical repository: `sonlyconsulting-ctrl/DCSE-Command-Post`  
Canonical path: `rules_engine/`  
Promotion authority: explicit DCS authorization on 2026-09-13.

This directory is the active DCSE Rules Engineering baseline for immediate execution and testing.

## Locked architecture

L0 Master / Authority  
L1 Doctrine  
L2 Skills  
L3 Rule Runtime  
L4 Evidence / Audit / Learning

S1 = Rule Discovery & Decomposition  
S2 = Rule Engineering & Operationalization

## Current baseline

- 5 entity rule sets: Task, Idea, Asset, DDNA, Knowledge
- 18 capability rule sets through Media
- Meta-rule lifecycle
- 148 atomic rules
- 5 entity composites
- deterministic runtime and registry
- operative-status regression checks
- 15/15 promotion tests passing

## Use

From repository root:

```bash
python rules_engine/bootstrap.py --test
```

The bootstrap expands the exact promoted archive into `rules_engine/runtime/` and runs the packaged test suite.

OPERATIVE does not mean immutable. L4 evidence may route a rule back through S1/S2 for regeneration, supersession, merge, split, or retirement. Candidate objects produced by operative rules retain their own lifecycle state until separately promoted.
