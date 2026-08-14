# DCSE R5 Operative Cutover and Context Compiler Walkthrough

**Status:** OPERATIVE AUTHORITY, PARTIAL DEPLOYMENT  
**Authority:** DCS  
**Effective:** 2026-08-14T19:11:56-04:00  
**Classification:** INTERNAL, NON-PS  

## 1. Authority Correction

R5 is designated `OPERATIVE` by registered directive `DCS-DIR-20260814-R5-OPERATIVE-001`.

The candidate language embedded in the reviewed R5 source is preserved as historical evidence. It no longer controls the authority-state decision. Deployment remains independently `PARTIAL` until required surfaces acknowledge the exact R5 artifact, canonical commit, runtime manifest, and lane mapping.

## 2. Why v7.1 Kept Appearing

The canonical GitHub v7.2 branch contained R4 candidate files and no R5 canonical artifact, directive registry, R5 lane mapping, or R5 runtime manifest. The R5 document available outside the canonical repository still contained its pre-approval candidate gate. The result was a repeated fallback to its own stale §42 language.

## 3. Step 3, Resolve Controller and Authority

For every substantive task, the compiler shall log these decisions in order:

1. Read the task declaration.
2. Identify the exact controller revision and SHA-256.
3. Load the express DCS directive registry.
4. Resolve any active directive affecting the task.
5. Apply the MP precedence order.
6. Record superseded or drifting statements.
7. Resolve the lane and security class.
8. Stop if authority, lane, or protected boundaries remain unresolved.

Required log phases:

```text
TASK_DECLARATION
AUTHORITY_RESOLUTION
LANE_RESOLUTION
CONFLICT_DISPOSITION
EXECUTION_DECISION
```

For an SS website task, `AUTHORITY_RESOLUTION` must show both operative directives and the R5 hash. `LANE_RESOLUTION` must resolve `SS`, `NON_PS`, and exclude protected D13/D14 bodies.

## 4. Step 4, Build the Context Packet

The compiler shall:

1. Load `context_profiles/ss_website.v7.2.json`.
2. Select every direct source listed in `direct_rule_sources`.
3. Evaluate each conditional source against actual task scope.
4. Compute transitive dependency closure.
5. Log each dependency and inclusion basis.
6. Apply firewall exclusions.
7. Apply conflict dispositions, including the orange-brown drift control.
8. Verify that every expected rule is present.
9. Build and hash the packet manifest.
10. Run runtime preflight.
11. Authorize execution only after preflight passes.

The SS dependency set is no longer described as likely. The direct set is fixed by the registered profile. D12, D15, and D18 are conditional and must be included when their declared trigger is true.

## 5. Log Locations

```text
logs/context_compiler/YYYY-MM-DD/{task_id}.jsonl
receipts/context_packets/{context_packet_id}.manifest.json
```

Each JSONL record carries the task, packet, R5 identity, phase, decision, reason, evidence references, source or rule, inclusion basis, and evidence status.

## 6. Inspection Commands

Full ordered event view:

```powershell
.\scripts\Inspect-DCSEContextCompiler.ps1 -LogPath .\logs\context_compiler\2026-08-14\SS-WEB-001.jsonl
```

Summary and missing-phase detection:

```powershell
.\scripts\Inspect-DCSEContextCompiler.ps1 -LogPath .\logs\context_compiler\2026-08-14\SS-WEB-001.jsonl -Summary
```

Watch a running compilation:

```powershell
.\scripts\Inspect-DCSEContextCompiler.ps1 -LogPath .\logs\context_compiler\2026-08-14\SS-WEB-001.jsonl -Follow
```

Inspect authority only:

```powershell
.\scripts\Inspect-DCSEContextCompiler.ps1 -LogPath .\logs\context_compiler\2026-08-14\SS-WEB-001.jsonl -Phase AUTHORITY_RESOLUTION
```

## 7. Immediate Change Integration Rule

An immediate DCS change enters operation as follows:

```text
DCS directive
-> directive registry entry
-> affected-rule and conflict mapping
-> operative patch or controller incorporation
-> context profile update
-> compiler preflight test
-> canonical GitHub commit
-> runtime registry synchronization
-> local and model distribution
-> Tribunal receipt
```

No new approval cycle is required for a change DCS has expressly approved. The implementation record must still preserve hashes, scope, rollback, runtime acknowledgments, and any remaining deployment gap.

## 8. Current Integration Disposition

The following are immediate operative controls:

- R5 is the controlling DCSE Master Profile.
- R5 authority and runtime deployment are independent states.
- The MP §8.1 precedence order is controlling.
- SS website context selection is deterministic.
- Legacy orange-brown SS palette language is `DRIFT`.
- SS personality, voice, tone, and lane separation are mandatory acceptance criteria.
- Compiler decisions are auditable through JSONL events and packet manifests.

Required surface acknowledgments remain deployment work and do not reverse the operative authority decision.
