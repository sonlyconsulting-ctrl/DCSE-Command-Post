# DCSE V7.3 Agent Authority Adoption and Correction Standard

**Task ID:** DCSE-V73-AGENT-ADOPTION-CORRECTION-20260921-01  
**Status:** OPERATIVE upon Level 0 promotion and canonical merge  
**Authority:** DCS Level 0  
**Lane:** DCSE / ALL AGENTS  
**Classification:** INTERNAL  
**Effective date:** 2026-09-21

## 1. Purpose

This standard prevents agents from misreporting the operative governance version, confusing repository head with promotion authority, claiming that an event was logged without a durable record, or treating one synchronized platform as proof for another.

## 2. Mandatory authority resolution

Before any substantive governed task or any answer about current doctrine, an agent SHALL resolve:

1. the V7.3 operative designation;
2. the V7.3 machine manifest;
3. the inherited V7.2 R5 substantive controller;
4. the current root `DCSE_MANIFEST.yaml`;
5. D21 task routing;
6. D22 canonical-source and persistence routing;
7. D05 promotion controls and applicable task doctrine.

The constitutional front door is the operative designation. `00_START_HERE.md` is navigation after authority resolution.

## 3. Commit identity taxonomy

The following identities SHALL NOT be collapsed:

- **Foundation merge:** `c256f2e2a55eb90301c3441944ac810e4bb14a78`
- **Operative promotion/activation merge:** `d24b4f64e7f464c22bbe8f2d5060c8521434a660`
- **Canonical route/validator reconciliation:** `fe804d6af1be3cdd32d7b58d21108ad4ad645057`
- **ESCD contextual runtime implementation merge:** `5ea85c85d311743e9d02d6d26aebccc9968ecca5`
- **Current repository head:** dynamic; it is not automatically the promotion identity.

Canonical identity remains repository + path + governing commit + content hash when available.

## 4. V7.2 continuity rule

V7.2 is superseded as the current governance name. It remains the inherited substantive controller, rollback baseline, compatibility source, and lineage. Correct citation of V7.2 for those roles is required and SHALL NOT be classified as drift.

Drift exists when a surface that has consumed the V7.3 designation presents V7.2 as the current operative governance name or when required identities disagree without disposition.

## 5. Evidence language

An agent SHALL NOT say `logged`, `recorded`, `saved`, `deployed`, `promoted`, `synchronized`, or equivalent unless it can provide the applicable durable identifier and successful readback.

When only the conversation contains the correction, the required phrase is:

> Acknowledged in this conversation; durable recording is not yet verified.

## 6. Deterministic correction route

`AUTHORIZED CORRECTION -> CANONICAL ARTIFACT -> CONTENT HASH -> REGISTRY UPDATE WHEN APPLICABLE -> TRIBUNAL EVIDENCE -> DISTRIBUTION -> CROSS-VERIFY`

Destination selection must follow D22. Agents may not invent a Tribunal inbox, Supabase table, execution ledger, or filename.

## 7. Cross-system claims

GitHub, Supabase/DDNA, Tribunal, Vercel, ESCD, local mirrors, and model prompts maintain separate synchronization states.

- Level 0 authority may be immediately operative for the exact decision.
- Canonical GitHub merge makes the artifact independently discoverable.
- Distribution is administrative synchronization, not a new decision gate.
- No surface is synchronized until that surface supplies direct readback.
- Build success is not deployment proof.
- Configuration is not request success.
- A migration artifact is not live-schema proof.

## 8. Agent corrective behavior

When an agent discovers or is shown a governance error, it SHALL:

1. acknowledge the exact error;
2. stop repeating the superseded claim;
3. query canonical authority;
4. distinguish verified fact from inference;
5. correct authorized artifacts and runtime contracts when instructed;
6. create durable evidence;
7. validate and promote through D05;
8. report any blocked downstream synchronization without converting it into success.

Structure Precedes Scale.
