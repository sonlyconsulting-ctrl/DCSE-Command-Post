# DCSE Master-First Navigation, Media Routing, and DDNA Reconciliation Receipt

**Task:** DCSE-V72-PLATFORM-GOVERNANCE-20260915-02  
**Child scope:** Master-first participant navigation, project bootstrap, media persistence routing, and Vercel DDNA closeout  
**Authority:** DCS Level 0  
**Date:** 2026-09-15  
**Lane:** DCSE / SC

## Decisions

1. Master Profile v7.2 is the mandatory first authoritative read for every DCSC participant.
2. `DCSE_MANIFEST.yaml` is a machine locator/index and does not precede the Master Profile as authority.
3. After the Master Profile, participants load operative designation/sync, participant navigation, doctrine index, onboarding/access, D22, D21, D03 when applicable, stop-gates/platform controls, then the designated product repository.
4. Each product repository should expose a `DCSE_PROJECT_MANIFEST.yaml` or equivalent before task execution.
5. Task execution loads the exact Task ID/work order, source files, and asset manifest after governance/project bootstrap.
6. GitHub is the canonical media-control/index surface, not the default warehouse for all large binaries.
7. Large/high-resolution/frequently changing media should use governed object storage; GitHub retains manifests, hashes, provenance, rights, release state, and storage references.
8. "Accessible by all" means all authorized participants permitted by task/lane, not anonymous public access.
9. A general DCSE workflow-media bucket is not created in this task because its RLS/consumer/access contract must be explicitly designed and tested before activation.

## Vercel package DDNA reconciliation

Verified write/readback in DCSE-DDNA:
- artifact key: `DCSE-V72-VERCEL-GOVERNANCE-PACKAGE-20260915`
- authority key: `DCSE-V72-VERCEL-GOVERNANCE-PACKAGE-20260915-OPERATIVE`
- promotion key: `PROMO_DCSE_V72_VERCEL_GOV_PACKAGE_20260915`
- Git merge: `d63d24ee86b3872625b5c088d0d74feec814a2a7`
- designation SHA-256: `739950df92943e7bce9ed9f2bb6ceef14c49e175e84544e908e31c4e91a16941`
- runtime sync: `ddna_surface_recorded`
- authority state: `OPERATIVE`

No schema, RLS, worker, storage, secret, or broader Supabase remediation change was performed.

## Remaining media implementation gate

Before creating the shared workflow-media object-storage surface:
- define project/lane folder taxonomy;
- define authorized human/agent consumers;
- define private/public classification;
- define RLS policies and negative tests;
- define signed-URL or server-mediated retrieval;
- define upload/update/delete roles;
- define retention/versioning/archive policy;
- define hash/manifest reconciliation;
- define cost/file-size limits;
- validate one end-to-end media workflow.

**State:** Governance architecture resolved. Media storage implementation remains a separate controlled implementation task.
