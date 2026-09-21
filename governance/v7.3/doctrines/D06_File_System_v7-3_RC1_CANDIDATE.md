> **v7.3 RC1 DEVELOPMENT CARRY-FORWARD (2026-09-19).** Candidate only. This file reproduces the v7.2 source body from pinned GitHub main commit `0c7850e71f21e1c9442dfcbd0a7299ba38b41230` (source Git blob `301f935958b64c0357c61fd58623aa1975d893ce`). Embedded version, authority labels and historic links in the body below are source provenance and DO NOT designate this v7.3 file operative or promoted. Current operative v7.2 R5/D05/D21/D22 remain controlling until exact v7.3 review, DCS approval, promotion and reconciliation. Do not silently import open PR #156/#158/#159/#160 into this file. Original v7.2 bytes remain intact at `governance/v7.2/doctrines/D06_File_System_v7-2.md`.

---

# DCSE Doctrine D06: File System v7.2 Alignment

**Document ID:** DCSE-D06  
**Version:** v7.2  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Canonical v7.2 File:** D06_File_System_v7-2.md  

## Scope

This v7.2 alignment preserves non-conflicting D06 file classification, naming, staging, duplicate detection, protected-placement, archive, and local working-copy controls while making D22 v7.2 controlling for canonical platform selection and cross-system persistence.

## File Intake Rule

Incoming files shall be classified before controlled placement. Ambiguous items remain staged/open rather than being silently assigned authority.

A file's physical presence in a local folder does not establish its canonical enterprise home.

## Canonical Platform Selection

After classification:

- Git-eligible versioned doctrine, code, schemas, reusable workflows, controlled templates, manifests, and governed text artifacts use GitHub as canonical artifact storage.
- Structured operational/governance state, registry entries, relationships, lifecycle state, and DDNA structured signals use the appropriate Supabase schema/project.
- Large or binary governed assets use approved object storage when Git is unsuitable.
- Governance-significant decisions, validations, exceptions, promotions, and reconciliation events use Tribunal evidence.
- Secret values use Vault or another approved secret-management surface only.

D22 v7.2 is controlling when destination rules conflict.

## Duplicate and Reuse Rule

Before creating a new canonical file, perform duplicate/reuse evaluation using identity, content hash where available, source/provenance, and D20 Reuse Before Redesign. Duplicate files shall not be silently deleted or multiplied across active canonical locations.

## Synchronization

Where an artifact is canonical in GitHub or object storage, Supabase should register its identity, status, relationships, and integrity metadata rather than become a competing copy of authority. Tribunal records material lifecycle evidence rather than serving as a substitute file repository.

## Promotion Record

This D06 v7.2 alignment is **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 effective 2026-09-10**.