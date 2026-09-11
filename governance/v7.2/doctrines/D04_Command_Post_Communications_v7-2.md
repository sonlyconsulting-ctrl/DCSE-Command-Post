# DCSE Doctrine D04: Command Post Communications v7.2 Alignment

**Document ID:** DCSE-D04  
**Version:** v7.2  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Canonical v7.2 File:** D04_Command_Post_Communications_v7-2.md  

## Scope

This v7.2 alignment preserves non-conflicting D04 communications, packet, receipt, and Tribunal operating requirements while superseding stale repository/branch/model-routing language that conflicts with the operative DCSE Master Profile v7.2 or D22 v7.2.

## Controlling Cross-System Rule

D04 governs communications and Tribunal transport. It does **not** independently determine canonical persistence destination when D22 applies.

- GitHub is the versioned artifact/source surface.
- Supabase/DDNA is structured state, registry, authority-reference, and relationship infrastructure.
- Tribunal is governance-significant communication and evidence.
- Storage is used for large/binary governed assets when Git is unsuitable.
- Vault/approved secret stores hold secret values.

Communications packets shall preserve source identity, lane, authority, task/decision identifiers, and content/hash references where applicable.

## Stale Routing Supersession

Any older D04 language that pins all models to a historical branch, historical repository map, or historical version family is superseded when it conflicts with current verified v7.2 authority and D22 routing. Models and agents shall resolve current authority rather than assume a legacy branch.

## Tribunal Boundary

Tribunal evidence does not replace the canonical doctrine/source artifact and does not independently create promotion authority. Governance-significant GitHub/Supabase synchronization shall produce or reference Tribunal evidence when required by D22/D05.

## Promotion Record

This D04 v7.2 alignment is **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 effective 2026-09-10**.