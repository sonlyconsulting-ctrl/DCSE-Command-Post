# DCSE Bulk Media and Creative Codebase Capture Standard v1

**Document ID:** DCSE-MEDIA-CAPTURE-001  
**Version:** 1.0  
**Status:** ACTIVE IMPLEMENTATION STANDARD  
**Scope:** governed bulk media discovery, manifesting and creative-codebase staging  
**Parent controls:** D06, D16, D18, D19, D20, D22, Shared Media Asset Standard

## 1. Purpose

Replace ad-hoc one-file-at-a-time media collection with a repeatable bulk process that preserves provenance and does not confuse discovery with authority or release rights.

## 2. Reference implementation

- `scripts/dcse_media_codebase_bulk_capture.py`
- `governance/v7.2/media/DCSE_BULK_MEDIA_CAPTURE_CONFIG_TEMPLATE.json`

## 3. Required sequence

`APPROVED ROOTS -> INVENTORY -> SHA-256 -> DOMAIN/ROLE CLASSIFICATION -> DEDUPE -> CODE-CONSUMPTION CHECK -> MANIFEST -> OPTIONAL SAFE STAGE -> VERIFY`

Default execution is inventory only.

## 4. Domain-first working structure

When staging a creative codebase, use:

`assets/<domain>/<role>/`

Domains may include SC, SS, CTJ, TSL, X5O, B4L, personas and shared assets. Roles may include brand, hero, persona, background, images, video, audio, docs and training media.

This working structure does not replace canonical object storage or source repositories.

## 5. Mandatory metadata

For each located asset record where available:
- source root/path;
- filename;
- SHA-256;
- bytes;
- MIME/type;
- domain;
- role;
- duplicate relationship;
- code-consumption references;
- staged path/state;
- canonical status;
- rights status;
- release status.

Unknown canonical/rights/release states remain UNVERIFIED.

## 6. Safe staging

- source files are never deleted or mutated;
- dry-run/inventory is the default;
- no staged overwrite with different content;
- filename collision uses a hash suffix;
- large media is manifest-only by default;
- large masters should normally remain in governed media/object storage with working derivatives supplied to creative codebases.

## 7. Consumption state

Creative handoff reporting should distinguish:

`DISCOVERED -> PREPARED -> RECEIVED_BY_WORKER -> REFERENCED_IN_OUTPUT`

A file discovered on disk does not prove it reached or was used by a creative worker.

## 8. Privacy / security

Do not stage:
- secrets/credentials;
- PS-protected content onto non-PS routes;
- unapproved private/personally identifying media;
- files whose rights/release state prohibits the target use.

## 9. Evidence

A bulk run should return:
- JSON manifest;
- CSV manifest;
- source roots;
- asset count;
- unique hash count;
- duplicate groups;
- consumed-asset count;
- staging states;
- errors;
- exact tool/config version.

**Structure Precedes Scale.**
