# DCSE Doctrine D06: File System and Device Governance v7.1 RC3 Candidate

**Document ID:** DCSE-D06-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D06_File_System.md`  
**Source SHA-256:** `ce8c57dbba4334447bb88f49c070da85083dd9067b7bd9cf7a9b2e759ab02b64`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Parent candidate SHA-256:** `d490536cfeddc1b6670f9a604ff1c8350c2a1aabae9bd5481bd1539fba7fdef5`  
**Runtime dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D21_Doctrine_Runtime_Engine_v7.1_RC3_CANDIDATE.md`  
**Runtime dependency SHA-256:** `5c2eccad502538a2defae73662c75dbabf10a3d8dd6c94219e1033f829cea995`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D06 governs the location, identity, classification, access, movement, retention, backup, recovery, synchronization, and deletion of files and device-resident artifacts used by DCSE.

D06 defines storage controls. It does not make a location authoritative merely because a file exists there. D05 governs promotion, D15 governs database state, D21 governs runtime execution, and D22 governs canonical identity and distribution.

## 2. Governing principles

1. Authority and location are separate attributes.
2. Every governed artifact has a canonical identity, even when several verified representations exist.
3. Storage topology is registry-driven and must not depend on a fixed operating system, drive letter, directory count, device name, or sync provider.
4. PS, PPR, credentials, personal data, family data, and other protected material receive explicit isolation controls.
5. Visibility never implies permission.
6. Classification precedes movement, synchronization, publication, or destructive action.
7. Reversible correction is preferred to deletion.
8. Missing paths isolate affected operations rather than stopping unrelated safe work.
9. Hash equivalence supports identity and duplicate review but never authorizes silent deletion.
10. File-system evidence must distinguish observation, action, verification, and authority.

## 3. Storage root registry

Every active storage root must be represented by an approved registry entry or verified configuration adapter.

```yaml
storage_root:
  root_id: ""
  display_name: ""
  root_type: "WORKSPACE | CANONICAL_REPOSITORY | AUDIT_COPY | INTAKE | QUARANTINE | ARCHIVE | BACKUP | OFFLINE_PROTECTED | DEPLOYMENT_CACHE"
  provider: ""
  platform: ""
  locator_ref: ""
  resolved_path_or_uri: ""
  entity: ""
  lane: ""
  classification_ceiling: ""
  sync_mode: "NONE | READ_ONLY | BIDIRECTIONAL | BACKUP_ONLY"
  allowed_operations: []
  prohibited_operations: []
  credential_ref: ""
  encryption_required: false
  retention_policy_ref: ""
  backup_policy_ref: ""
  authority_ref: ""
  verified_at: ""
  status: "ACTIVE | DEGRADED | QUARANTINED | RETIRED"
```

`locator_ref` may resolve to a Windows path, POSIX path, repository path, object-store URI, Supabase Storage location, or another approved adapter. A doctrine update is not required merely because a device name, drive letter, or provider changes.

## 4. Logical storage classes

The following logical classes replace the rigid v6.9 fourteen-directory requirement:

| Class | Purpose | Minimum control |
| --- | --- | --- |
| Authority | Promoted governance references | Exact canonical identity and restricted write |
| Candidate | Proposed artifacts and diffs | Non-promoting label and source lineage |
| Workspace | Active editable work | Scoped write access and recoverable history |
| Intake | Newly received content | Classification before onward movement |
| Quarantine | Ambiguous or suspected protected content | No general indexing, sync, or publication |
| Evidence | Receipts, logs, hashes, and validation results | Append-oriented integrity and retention |
| Archive | Superseded or inactive artifacts | Read-mostly retention and restoration path |
| Backup | Recovery copies | Encryption, retention, and restoration verification |
| Offline protected | PS, PPR, or other approved isolated material | No unapproved cloud, repository, model, or cross-lane exposure |
| Published | Public or deployed representations | Exact release linkage and public-safe classification |

A physical root may support more than one class only when the boundaries are mechanically distinguishable and access controls remain enforceable.

## 5. Artifact identity contract

```yaml
file_artifact:
  artifact_id: ""
  canonical_name: ""
  content_sha256: ""
  size_bytes: 0
  media_type: ""
  entity: ""
  lane: ""
  classification: ""
  privacy_tags: []
  source_ref: ""
  canonical_ref: ""
  representation_type: "SOURCE | COPY | EXPORT | BUILD | BACKUP | RECEIPT"
  lifecycle_state: ""
  retention_policy_ref: ""
  legal_hold_ref: ""
  created_at: ""
  observed_at: ""
```

Identity is based on authoritative lineage and content hash, not filename alone. Generated exports may have distinct content hashes while remaining linked to one logical artifact.

## 6. Classification and protected-data boundary

Before content is opened, transmitted, indexed, synchronized, or placed in a general workspace, the runtime evaluates available metadata, source, lane, classification, and exposure indicators.

Keyword matching is a screening signal only. A generic term must not automatically route a file into a protected lane or expose the file to determine whether it belongs there. Suspected protected material is placed in a bounded quarantine and reviewed using the minimum necessary metadata or an approved protected-lane process.

### 6.1 Protected invariants

- PS and PPR material must remain inside their separately authorized storage and processing boundary.
- Secret values, recovery codes, MFA data, private keys, service-role credentials, private connection strings, and unrestricted private URLs must not enter GitHub, ordinary database content, model prompts, shared receipts, or public artifacts.
- Family, minor, health, financial, identity-masked, or other sensitive content follows its approved classification and disclosure policy.
- A mixed-content artifact must be partitioned or handled at the highest applicable classification.
- Possible exposure triggers containment of the affected artifact and destination. Unrelated safe work continues.

## 7. Intake and routing lifecycle

```text
RECEIVED
  -> IDENTIFIED
  -> CLASSIFIED
  -> SCANNED
  -> QUARANTINED_OR_ADMITTED
  -> CANONICAL_DESTINATION_RESOLVED
  -> COPIED_OR_MOVED
  -> HASH_VERIFIED
  -> REGISTERED
  -> RECEIPTED
```

Required routing controls:

1. preserve original source metadata before mutation;
2. determine lane and classification without unnecessary content exposure;
3. scan for secrets, malware, protected markers, and unsupported types as applicable;
4. resolve the destination from the storage registry;
5. use collision-safe naming and atomic operations where supported;
6. verify content hash after transfer;
7. record failure, rollback, or quarantine state;
8. never equate a mailbox insert, sync indicator, or copied file with confirmed delivery.

## 8. Device capability registry

Device rules belong in a mutable capability registry rather than permanent doctrine rows.

```yaml
device_profile:
  device_id: ""
  owner_or_custodian: ""
  platform: ""
  security_posture: ""
  encryption_status: "UNKNOWN"
  supported_operations: []
  prohibited_operations: []
  lane_authorizations: []
  classification_ceiling: ""
  local_model_capacity: ""
  backup_role: "NONE"
  credential_capability: "NONE"
  connectivity_mode: "CONNECTED | INTERMITTENT | OFFLINE"
  last_verified_at: ""
  status: "ACTIVE | DEGRADED | QUARANTINED | RETIRED"
```

Obsolete operating systems, unencrypted devices, shared devices, and unsupported hardware must not receive secrets or protected data unless a documented compensating control and direct DCS authority exist.

## 9. Access and least privilege

- Access is granted by identity, operation, lane, classification, root, and time where supported.
- Read, create, update, move, archive, delete, synchronize, and publish are separate permissions.
- Agents receive only the workspace and operation required for the assigned task.
- A mounted drive, cloned repository, shared link, browser session, or visible file does not create authority.
- Access changes are attributable, revocable, and periodically reviewed.
- Credential material is referenced through a secure location identifier and never copied into a receipt.

## 10. File operation contracts

### 10.1 Create and update

Create and update operations require a resolved destination, collision behavior, expected classification, and verification method. Controlled text and code changes use version history where available.

### 10.2 Copy and move

A copy preserves the source. A move is complete only when destination integrity is verified and source disposition is recorded. Cross-device and cross-provider moves are implemented as verified copy followed by separately authorized source disposition.

### 10.3 Archive

Archive operations preserve canonical identity, source lineage, retention, restoration method, and supersession status. Archive is not deletion.

### 10.4 Delete

Deletion classes are:

| Class | Rule |
| --- | --- |
| Reversible workspace cleanup | May proceed under a bounded DCS-approved standing procedure with exact target, exclusion list, backup or trash path, and receipt. |
| Duplicate disposition | Requires authority analysis in addition to hash match; preserve one verified authoritative representation. |
| Retention expiry | Requires policy match, legal-hold check, and recorded disposition. |
| Irreversible, protected, authoritative, or broad deletion | Direct DCS decision required. |

Recursive deletion against an unresolved variable, wildcard, workspace root, home directory, drive root, or storage root is prohibited.

## 11. Duplicate and conflict handling

Duplicates are classified as exact content duplicates, equivalent representations, divergent versions, or naming collisions.

The resolver must:

1. compare hashes and relevant metadata;
2. identify canonical authority;
3. preserve divergent content;
4. quarantine unresolved conflicts;
5. update references before disposition;
6. record the chosen action and rollback path.

## 12. Synchronization and reconciliation

GitHub, Supabase references, local workspaces, cloud drives, archives, and deployments may each hold representations. D22 defines their authority relationship.

Synchronization must verify:

- source and destination identities;
- expected direction;
- excluded lanes and classifications;
- conflict behavior;
- content hash or equivalent integrity proof;
- completion on both ends;
- drift and last-known-good state.

`DRIFT` blocks reliance on the mismatched representation, not all unrelated operations.

## 13. Backup and recovery

```yaml
backup_record:
  backup_id: ""
  source_ref: ""
  scope: ""
  created_at: ""
  content_hash_or_manifest: ""
  encrypted: false
  destination_ref: ""
  retention_until: ""
  legal_hold_ref: ""
  restore_procedure_ref: ""
  restore_tested_at: ""
  restore_result: "UNKNOWN"
```

A backup claim is incomplete until the required restoration method has been tested. Database backups follow D15. Storage objects and external attachments must be included explicitly because a database backup may not contain them.

## 14. Retention, legal hold, and privacy

- Retention is assigned by artifact class and controlling obligation.
- Legal hold overrides ordinary deletion and rotation.
- Personal and protected data are minimized, access-limited, and deleted or anonymized when authorized and no longer required.
- Evidence and audit retention must not become an excuse to retain exposed secrets.
- Redaction creates a new representation; it does not alter the protected source silently.

## 15. GitHub and public eligibility

Before any file enters GitHub or another broadly replicated system, verify:

- repository visibility and audience;
- lane and classification eligibility;
- secret scan;
- protected-data scan;
- licensing and third-party rights;
- generated artifact policy;
- required source and receipt links.

Public release remains governed by D05 and applicable product or publication doctrine.

## 16. Local and offline operation

A runtime may operate from a verified local or offline package when network services are unavailable. The package must contain a manifest, canonical source references, hashes, applicable doctrine, and a reconciliation plan.

Offline work does not silently become authoritative. It is reconciled under D22 when connectivity returns.

## 17. Monitoring and maintenance

Maintenance cadence is risk-driven and configuration-backed rather than fixed in doctrine. Monitors may cover:

- unclassified intake age;
- quarantine age;
- unexpected protected-data placement;
- secret exposure;
- hash drift;
- failed sync;
- backup age and failed restore tests;
- storage capacity;
- stale device posture;
- broken canonical references;
- retention and legal-hold conflicts.

Alert delivery must be verified. Creating a row or sending a request is not proof that a human or runtime received it.

## 18. Failure and recovery behavior

| Condition | Required behavior |
| --- | --- |
| Required root unavailable | Try another approved representation; isolate dependent writes; continue safe inspection and recovery. |
| Classification uncertain | Quarantine affected artifact; do not expose content broadly. |
| Possible secret or protected exposure | Contain destination and artifact, preserve non-secret evidence, rotate or remediate through the security process. |
| Hash mismatch | Mark drift, preserve both copies, stop reliance on the mismatch. |
| Transfer interrupted | Verify destination state before retry; use idempotent resume or rollback. |
| Device posture stale | Limit the device to operations supported by the last verified posture. |
| D06 unavailable | Do not invent storage or protected-data rules; continue only work not dependent on D06. |

A Stop-Gate is reserved for affected irreversible, protected, authority-changing, production, public, or otherwise reserved action when no safe path exists.

## 19. File-operation receipt

```yaml
file_operation_receipt:
  receipt_id: ""
  task_ref: ""
  operation: ""
  source_ref: ""
  destination_ref: ""
  artifact_ids: []
  lane: ""
  classification: ""
  pre_hashes: []
  post_hashes: []
  authority_ref: ""
  standing_procedure_ref: ""
  rollback_ref: ""
  result: "PASS | PASS_WITH_FINDINGS | FAIL | PARTIAL"
  findings: []
  verified_at: ""
```

## 20. Runtime interfaces

```text
resolve_storage_root(root_id, context) -> StorageResolution
classify_artifact(source_ref, metadata, context) -> ClassificationResult
plan_file_operation(operation, sources, destination, context) -> FileOperationPlan
execute_file_operation(plan) -> FileOperationReceipt
verify_transfer(receipt) -> VerificationResult
detect_storage_drift(scope) -> DriftReport
plan_recovery(source_ref, backup_ref) -> RecoveryPlan
```

Implementations may use PowerShell, Python, shell, platform APIs, repository APIs, or storage SDKs. Doctrine does not embed destructive executable scripts.

## 21. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D06-001 | Windows path changes | Registry resolves the new path without doctrine edit. |
| D06-002 | POSIX runner loads package | Storage adapter resolves valid roots. |
| D06-003 | File contains generic protected keyword | Screening does not auto-route solely on the word. |
| D06-004 | Confirmed PS artifact enters intake | Artifact is quarantined and kept out of general sync and indexing. |
| D06-005 | Mixed protected and general content | Highest applicable classification or verified partition is used. |
| D06-006 | Exact duplicate found | No silent deletion occurs. |
| D06-007 | Cross-provider move fails midway | Source remains and destination is verified before retry. |
| D06-008 | Broad delete uses unresolved variable | Operation is rejected. |
| D06-009 | Approved reversible cleanup | Exact targets move to recoverable destination and receipt is written. |
| D06-010 | Legal hold exists | Retention expiry does not delete the artifact. |
| D06-011 | Backup created | Backup remains incomplete until required restore verification. |
| D06-012 | Database backup excludes Storage objects | Missing object-storage scope is reported. |
| D06-013 | GitHub copy hash differs from canonical | Drift is recorded and mismatched copy is not relied upon. |
| D06-014 | Mailbox row inserted | Delivery remains unconfirmed until recipient-side evidence exists. |
| D06-015 | Device is unencrypted or unsupported | Secret and protected operations are denied absent explicit exception. |
| D06-016 | D06 source missing | Only D06-dependent actions are isolated. |
| D06-017 | Secret scan detects value | Value is not repeated in output; containment process starts. |
| D06-018 | Offline package used | Manifest and hashes verify before execution. |
| D06-019 | Connectivity returns | Offline work reconciles under D22 before authority reliance. |
| D06-020 | Same filename, different content | Both versions are preserved pending authority resolution. |

## 22. Cross-doctrine boundaries

- D03 selects and coordinates capable runtimes.
- D04 governs communication and delivery evidence.
- D05 governs promotion, rollback, and supersession.
- D13 and D14 govern protected DART and PS content within their authorized boundary.
- D15 governs database, Storage, and data-service state.
- D16 governs DDNA extraction without weakening file classification.
- D20 governs product assembly outputs.
- D21 executes this doctrine through runtime contracts.
- D22 governs canonical source identity and reconciliation.

## 23. Source correction record

| Source condition | RC3 correction | Reason |
| --- | --- | --- |
| Fixed fourteen-directory v6.9 Hub | Registry-driven logical storage classes | Supports current and future platforms without weakening controls. |
| Local Hub described as working authority | Separates location from canonical authority | Prevents silent supersession and drift. |
| Keyword-only litigation routing | Uses risk screening plus bounded classification | Prevents false routing and unnecessary exposure. |
| Named devices and operating systems in doctrine | Uses mutable device capability profiles | Keeps security current without constitutional edits. |
| Every deletion needs an individual human gate | Allows bounded reversible cleanup under standing DCS authority | Preserves nonstoppage while reserving irreversible and protected decisions. |
| Embedded PowerShell and fixed schedules | Defines interfaces, contracts, and risk-driven monitors | Makes requirements testable and implementation-neutral. |
| Global halt when D06 is missing | Isolates affected actions | Preserves safe work and recovery. |
| Visibility and access were conflated | Requires explicit operation-level grants | Implements least privilege. |

## 24. Candidate status

This candidate is correction evidence only. It does not replace the active D06 until DCS promotes the exact artifact or exact diff and D22 records the authoritative representation.
