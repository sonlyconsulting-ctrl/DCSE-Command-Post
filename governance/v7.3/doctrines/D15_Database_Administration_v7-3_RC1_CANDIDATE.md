> **v7.3 RC1 DEVELOPMENT CARRY-FORWARD (2026-09-19).** Candidate only. This file reproduces the v7.2 source body from pinned GitHub main commit `0c7850e71f21e1c9442dfcbd0a7299ba38b41230` (source Git blob `f3bbc8630801b9a67165867db5e739228cbd63be`). Embedded version, authority labels and historic links in the body below are source provenance and DO NOT designate this v7.3 file operative or promoted. Current operative v7.2 R5/D05/D21/D22 remain controlling until exact v7.3 review, DCS approval, promotion and reconciliation. Do not silently import open PR #156/#158/#159/#160 into this file. Original v7.2 bytes remain intact at `governance/v7.2/doctrines/D15_Database_Administration_v7-2.md`.

---

# DCSE Doctrine D15: Database Administration v7.2 Alignment

**Document ID:** DCSE-D15  
**Version:** v7.2  
**Status:** ACTIVE / OPERATIVE  
**Promotion Status:** PROMOTED  
**Approved / Authorized By:** DCS Level 0  
**Effective Date:** 2026-09-10  
**Canonical v7.2 File:** D15_Database_Administration_v7-2.md  

## Scope

This v7.2 alignment preserves non-conflicting D15 database administration, migration, backup, RLS, access-control, integrity, and operational safety rules while superseding blanket language that treats Tribunal or runtime transactions as automatically committed to Git.

## Database Role Separation

- **DCSE-DDNA Supabase** is the constitutional runtime governance/authority/relationship registry and structured DDNA data surface.
- **SC Command Post Supabase** is operational/application state and may reference DCSE-DDNA authority.
- A Supabase row does not independently create doctrine authority.
- GitHub remains canonical for versioned doctrine/source artifacts where D22 assigns GitHub as canonical.
- Tribunal stores governance-significant decision/execution/validation evidence, not every routine database transaction.

## Git Relationship

Database schemas, migration source, reusable SQL, controlled database configuration templates, and other Git-eligible artifacts should be versioned in GitHub when authorized. Runtime rows and ordinary transactions remain database state and are not automatically mirrored to Git.

Where a database change affects governance or a promoted artifact, preserve the applicable GitHub source/version, Supabase state/reference, and Tribunal evidence relationship under D22.

## Secrets

Connection strings, service-role keys, passwords, private keys, tokens, recovery material, and equivalent secrets shall not be committed to GitHub, ordinary Supabase tables, Tribunal evidence, prompts, or doctrine. Use approved secret-management surfaces.

## Cross-Database Integrity

Cross-database references shall identify the source project/schema/object and authority relationship. Copies of authority data in operational databases are governed references, not replacement constitutional authority.

## Promotion Record

This D15 v7.2 alignment is **APPROVED, PROMOTED, ACTIVE, and AUTHORIZED immediately by DCS Level 0 effective 2026-09-10**.