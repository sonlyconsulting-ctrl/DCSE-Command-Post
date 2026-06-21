# DCSE Doctrine D06: File System and Device Governance

**Document ID:** DCSE-D06  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T19:27:00-04:00
**Last Version/Release Date/Time:** 2026-06-21T15:22:10-04:00  
**Status:** DCSE Authorized version Pending Approval  
**Classification:** INTERNAL  
**Lane:** DCSE and PS Command Center  
**Canonical file:** D06_File_System.md  
**Doctrine Description:** The File System and Device Governance Doctrine (D06) establishes the definitive system for regulating the construction, intake, segregation, and retention of all DCSE entity assets, product configurations, and operational resources. Acting as the spatial foundation of the Hub-and-Spoke architecture, D06 defines the boundaries between cloud-synchronized collaborative workspaces and protected offline litigation environments. The system functions through three primary mechanisms: a rigid 14-directory layout, automated file routing rules based on content classification, and role-based device access controls. At its core, D06 segregates data into 14 distinct directories under the v6.9 Hub. This layout structures everything from master authority profiles and core doctrine files to active project workspaces, command packets, and baselines. By strictly partitioning these folders, the system prevents cross-contamination of metadata, avoids file duplication, and guarantees that every asset transitions predictably through its verified lifecycle. To manage external files, D06 mandates automated ingestion scripts that sweep staging locations, classifying incoming files and routing them according to their content type. Most critically, any files referencing active Pro Se litigation are immediately quarantined and routed to the offline Spoke (DS Litigation), completely firewalled from the cloud-synced Hub. Furthermore, the doctrine classifies legacy directories and root folders under strict preservation profiles. A key compliance mandate is the preservation of historical resume files under the PTGC All Things subfolders, which serve as essential evidentiary material for active litigation and are excluded from bulk automated cleanup pipelines. Hardware governance is enforced via a Device Governance Matrix, which maps individual nodes (such as SonlyBiz, HPCompu2, and primary Mobile Command laptops) to distinct operating roles, allowed commands, and restricted actions. No sensitive data or Git authority actions may occur on non-secure staging nodes. Finally, all cleanup actions must proceed through the seven-stage File Governance Pipeline, guaranteeing that no automated script can delete or rearrange assets without human Level 0 approval. This comprehensive system ensures data integrity, compliance, and strict operational security across the entire enterprise.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. The 14-Directory Layout (Hub)

All active, controlled files under the `C:\DS All Things\DCSE_Command_Center\v6.9` Hub must reside within one of the following directories:

1. `00_Authority`: Contains the Master Profile and Constitution.
2. `01_Doctrine`: Contains files D01 through D14.
3. `02_Registry`: Contains access maps, doctrine indexes, and metadata registries.
4. `03_Communications`: Contains protocols for inbox schemas.
5. `04_Command_Packets`: Contains target task run instructions.
6. `05_Tribunal_Inbox`: Contains the active JSON communication bus.
7. `06_Baselines`: Contains snapshots and checksum receipts.
8. `07_Projects`: Contains active application workspaces and staging directories.
9. `08_Templates`: Contains document layouts and formatting schemas.
10. `09_Tools`: Contains daemons, polling scripts, and cleanup tools.
11. `10_Archive`: Contains older versions and backups.
12. `11_Receipts`: Contains compliance audits and verification logs.
13. `12_Diffs`: Contains line-by-line version differences.
14. `13_Open_Items`: Contains active checklists, gap lists, and raw staging folders.
### 1.1 Candidate Mirror Scope

The local Hub remains the working authority and audit source. The GitHub `v69` branch is the candidate-published mirror used for review, model access, and cross-agent source distribution. When DCS approves a full local-to-GitHub mirror, the mirror scope extends beyond the 14 active control directories to include approved support, review, archive, receipt, and auxiliary source folders that are present under the local `v6.9` root.

Auxiliary folders, including `video_image_written`, are classified as SUPPORT or REVIEW unless promoted by a later D05 baseline decision. Their presence in `v69` supports reconciliation and source availability. It does not convert them into ACTIVE doctrine and does not authorize promotion to `main`.

The mirror scope remains bounded by D04 Section 2.6. Files containing live credentials, quarantine flags, or PS litigation material remain excluded from GitHub unless DCS separately assigns a safe destination and records that decision. All exclusions must be listed in the Tribunal push receipt.

---

## 2. Segmented Search & Routing Rules

- **Downloads Sweep**: Automated routing scripts monitors the user's local downloads folder.
- **PS Litigation Segregation**: All files containing litigation keywords ("seals", "823cv489", "dart") are routed strictly to the offline Spoke (`DS Litigation`). Under no circumstances may they enter the Hub.
- **Ambiguous Files**: If a file's lane or classification is unclear, it must be moved to `13_Open_Items/` for manual review.

---

## 3. Root Folder Classification Hierarchy

To preserve historical context and avoid accidental deletion, the root folders of `C:\DS All Things` are classified under distinct governance rules. **Classification must occur before cleanup.**

### 3.1 Folder Governance Matrix
- **`DCSE_DOWNLOAD FILES`**:
  - *Classification*: Controlled Intake / Legacy Download Repository.
  - *Status*: Review Required. Excluded from bulk moves or deletion. Hashes must be audited to verify authoritative vs duplicate status.
- **`PTGC All Things`**:
  - *Classification*: Legacy Persona Archive.
  - *Status*: Permanent Retention. Offline migration to Machine 2 (`UBC_AV_HPCompu2`) is required for long-term cold backup. SonlyBiz is explicitly excluded from this backup path.
  - *Critical Preservation*: The subfolder `PTGC All Things\DS All Things 2024\DS Projects 24\AION 2024\DS Oldest Resumes` contains December 2023 and March 2024 resumes which are critical evidence of job search efforts for the active PS litigation. These must be preserved.
- **`SC Oct 2023 Projects`**:
  - *Classification*: Historical SC Project Reference.
  - *Status*: Long-Term Offline Retention. Excluded from active cleanup or modification.

---

## 4. Device Governance Matrix

DCSE assets are distributed across designated nodes, each governed by role-based operational permissions:

| Device Label | Operating System | Active Role | Allowed Actions | Restricted Actions / Exclusions |
| :--- | :--- | :--- | :--- | :--- |
| **SonlyBiz** | Windows 8.1 (64-bit) | Casual Utility & Staging Node (`DCS-UTILITY-STAGING-NONCONFIDENTIAL`) | - Web lookups<br>- Casual ChatGPT browser runs<br>- Non-sensitive temporary staging. | - **NO** PS legal or sensitive files.<br>- **NO** Supabase production credentials/API keys.<br>- **NO** Git authority commits. |
| **UBC_AV_HPCompu2** | Windows 7 Home Premium | Backup Utility Node (`DCS-BACKUP-UTILITY-WIN7`) | - Long-term cold backups<br>- Running Python file-inventory and checksum scripts. | - **NO** primary/authoritative files.<br>- **NO** active court drafting.<br>- **NO** Git push permissions. |
| **LAPTOP-74UF76GB** | Windows 10 | Primary Mobile Command Node (`DCS-MOBILE-COMMAND-LAPTOP`) | - VS Code editing<br>- Git/GitHub commits<br>- Supabase hydration<br>- Active PS legal drafting. | - Avoid heavy local LLM pipelines (quantized 1B-3B models only).<br>- Avoid Docker tasks until storage space is recovered. |

---

## 5. File Governance Pipeline

No automated script may delete or modify file arrangements unless the target path has completed the following pipeline:

```text
[Periodic Root Scan] -> [Path Classification] -> [Authority Determination] -> [Duplicate Analysis] -> [Cleanup Proposal] -> [Human Level 0 Approval] -> [Execution & Log Commit]
```

---

## 6. Intent

D06 exists to solve a specific operational problem: when a multi-lane enterprise runs across multiple machines, cloud sync tools, AI orchestration sessions, and legal workstreams simultaneously, file location ambiguity becomes a compliance risk — not just an inconvenience. A misrouted litigation file that enters a cloud-synced workspace is a disclosure event. A backup that lands on SonlyBiz instead of HPCompu2 violates the device governance matrix. An AI agent that writes to the wrong directory can corrupt a baseline or contaminate an evidentiary chain.

The intent of D06 is therefore threefold:

1. **Spatial certainty**: Every file in the ecosystem has exactly one canonical home. The 14-directory layout eliminates ambiguity by assigning a lane to every file type. There is no "miscellaneous" folder at the root level.
2. **Segregation enforcement**: The Hub (`v6.9`) and the offline Spoke (`DS Litigation`) are physically and operationally separated. D06 is the boundary rule set that prevents cross-contamination. No automation may override this boundary.
3. **Lifecycle traceability**: From intake through archive through cold storage, every file must pass through classifiable states. D06 defines those states so that audits, legal discovery requests, and compliance checks can be answered with precision.

This doctrine is the spatial foundation that all other doctrine files write into. D03 sends STOPGATE packets to `05_Tribunal_Inbox`. D05 writes baselines to `06_Baselines`. D13 routes evidentiary receipts to `11_Receipts`. D15 routes database backups to `10_Archive`. None of those operations are valid unless D06 is stable.

---

## 7. Setup

### 7.1 Hub Directory Initialization

The following PowerShell block initializes the full 14-directory Hub layout under a given version root. It is idempotent — running it on an existing structure will not overwrite existing files.

```powershell
$hub = "C:\DS All Things\DCSE_Command_Center\v6.9"
$dirs = @(
  "00_Authority", "01_Doctrine", "02_Registry", "03_Communications",
  "04_Command_Packets", "05_Tribunal_Inbox", "06_Baselines", "07_Projects",
  "08_Templates", "09_Tools", "10_Archive", "11_Receipts", "12_Diffs", "13_Open_Items"
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Force -Path "$hub\$d" | Out-Null }
Write-Host "Hub initialized at $hub"
```

### 7.2 Spoke Segregation Setup

The PS litigation Spoke must be confirmed as offline (not synced to OneDrive, Google Drive, or any cloud agent) before any routing automation is activated. Verify:

```powershell
# Confirm DS Litigation path is NOT under a known sync root
$spoke = "C:\DS Litigation"
$syncRoots = @("$env:USERPROFILE\OneDrive", "$env:USERPROFILE\Google Drive")
foreach ($root in $syncRoots) {
  if ($spoke.StartsWith($root)) { Write-Warning "SPOKE IS UNDER SYNC ROOT — STOP" }
}
Write-Host "Spoke segregation check passed."
```

### 7.3 Device Role Assignment

Before any node is used for DCSE operations, its role label must be confirmed in this document's Device Governance Matrix (Section 4). If a new device is added to the ecosystem, a row must be added to Section 4 before that device touches any DCSE assets. Role assignment is a human-level action and may not be automated.

### 7.4 SC Lane Structures

All SC product lanes (SC_CTJ, SC_Gov-OS, SC_TSL) live under `C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\` and are governed by this doctrine for routing, intake, and archival. Their internal folder structures (00_GOVERNANCE through 20_RECONCILED_*) are D06-compliant child layouts and must not be collapsed or renamed without updating this document.

---

## 8. Regulations

The following rules carry the force of doctrine. Any AI agent, script, or human operator executing within the DCSE ecosystem is bound by them.

### 8.1 Immutable Boundaries
- **REG-D06-01**: No file classified as PS litigation material may reside in any Hub directory at any time for any reason. Violations trigger an immediate STOPGATE.
- **REG-D06-02**: No file may be deleted from any controlled path without completing all seven stages of the File Governance Pipeline (Section 5). Scripts that attempt direct deletion without a logged Level 0 approval are non-compliant.
- **REG-D06-03**: The `PTGC All Things` root and its subfolders — particularly `DS Oldest Resumes` — are designated Permanent Retention. No cleanup script, migration tool, or AI agent may touch these paths without explicit written instruction from the operator.

### 8.2 Intake and Routing
- **REG-D06-04**: All incoming files must pass through a classification check before being placed in any controlled directory. Files that cannot be classified are routed to `13_Open_Items` pending human review.
- **REG-D06-05**: Litigation keywords ("seals", "823cv489", "dart", "pro se") trigger mandatory Spoke routing. This list is additive — new keywords may be appended but never removed without a formal doctrine update.
- **REG-D06-06**: Duplicate files detected by SHA-256 comparison must be flagged and held in `13_Open_Items`. Automated deduplication (silent deletion of detected duplicates) is prohibited.

### 8.3 Device Compliance
- **REG-D06-07**: SonlyBiz (Windows 8.1) is permanently excluded from receiving PS legal files, Supabase production credentials, and Git authority commits. This restriction survives any role reassignment.
- **REG-D06-08**: UBC_AV_HPCompu2 (Windows 7) may only receive cold backup archives. It must never hold authoritative (primary) files or participate in active Git operations.
- **REG-D06-09**: Database backup exports from D15 tools must be routed to `10_Archive` on the Primary Mobile Command Node, then mirrored cold to HPCompu2. SonlyBiz is excluded from this backup path.

### 8.4 Cross-Doctrine Compliance
- **REG-D06-10**: Any doctrine file that writes to a Hub directory (D03, D04, D05, D13, D15) must reference the target directory by its canonical label (e.g., `05_Tribunal_Inbox`, not a relative path or alias). This ensures D06 audits can parse cross-doctrine references unambiguously.
- **REG-D06-11**: The 14-directory layout is frozen for v6.9. New directories may only be added as part of a formal version increment (e.g., v6.10 or v7.0), not by individual script or agent action.

---

## 9. Suggested Maintenance

Maintenance on the file system should be performed on a cadence that matches operational tempo. The following schedule is the baseline recommendation:

### 9.1 Weekly
- **Inbox Sweep**: Run the D15 `db_verify_inbox.py` tool against `05_Tribunal_Inbox` to flag malformed JSON packets, orphaned receipts, and stale STOPGATE files older than 7 days.
- **Open Items Review**: Manually review `13_Open_Items` for any files pending classification. Any file sitting in `13_Open_Items` longer than 7 days without action should be escalated for operator decision.
- **Downloads Staging Check**: Confirm that the downloads sweep script has not accumulated unrouted files in the local downloads folder. Route or quarantine as appropriate.

### 9.2 Monthly
- **Hash Audit**: Run `db_audit_evidentiary.py` (D15) against `06_Baselines` and `11_Receipts` to verify that no files have been silently modified since their last checksum commit.
- **Device Compliance Spot-Check**: Verify that no DCSE-controlled files have appeared on SonlyBiz or HPCompu2 outside their permitted roles. Check via a targeted file search on both machines.
- **Archive Rotation**: Review `10_Archive` for items older than 90 days. Files that meet cold storage criteria should be queued for migration to HPCompu2. Log the migration in `11_Receipts`.
- **`12_Diffs` Pruning**: Diffs older than 60 days that have been superseded by a promoted baseline may be compressed and moved to `10_Archive`. Never delete a diff without confirming its baseline promotion is logged.

### 9.3 Per Version Release
- **Full Pipeline Audit**: Before promoting any new Hub version (e.g., v6.9 → v6.10), run the complete seven-stage File Governance Pipeline against all 14 directories. Generate an audit receipt in `11_Receipts`.
- **Device Matrix Review**: Confirm that all device role entries in Section 4 reflect current operational reality. Decommission any node no longer in service.
- **Doctrine Cross-Reference Check**: Verify that all sibling doctrine files referencing Hub directory paths use the canonical labels defined in Section 1. Update any that have drifted.

---

## 10. Ongoing Upgrade

D06 is a living governance document and must evolve with the ecosystem. The following principles govern how upgrades are managed:

### 10.1 Version Increment Protocol
- Minor layout changes (new subdirectory under an existing numbered folder, new device row in Section 4) are handled as **patch updates** — increment the `Last Doc Modified Date/Time` field and log the change in `12_Diffs`.
- Structural changes (new top-level numbered directory, modification to the File Governance Pipeline, changes to segregation boundary rules) are **minor version increments** — they require a new `v6.x` Hub and a full baseline promotion per D05.
- Changes to the litigation segregation keyword list (REG-D06-05) require a **doctrine update receipt** written to `11_Receipts` before the keyword takes operational effect.

### 10.2 D15 Integration Maintenance
As the database layer (D15) matures, D06 must be updated to reflect new backup destinations, new schema export paths, and any new tool placements in `09_Tools`. D15 changes that affect file routing are considered D06 changes and must be reflected here within the same version cycle.

### 10.3 SC Lane Expansion
When new SC product lanes are onboarded (beyond SC_CTJ, SC_Gov-OS, SC_TSL), the following must occur before the lane is operational:
1. The new lane folder must be created under `DCSE_CP_Project\` with a D06-compliant internal layout.
2. An entry must be added to Section 7.4 of this document naming the lane and its governance classification.
3. The lane must be registered in the Doctrine Index (`02_Registry/DCSE_Doctrine_Index_v6.9.md`).

### 10.4 AI Agent Scope Expansion
As new AI agents are granted write access to Hub directories, each agent must be explicitly listed under D03_AI_Orchestration.md with its permitted write paths. D06 must then be updated to reflect the agent's permitted directories in a cross-reference note under the relevant section. No agent has blanket write access to the Hub by default.

### 10.5 Deprecation Handling
When a Hub directory is deprecated (e.g., a directory consolidated into another in a future version), the following steps apply:
1. All contents must be classified and routed to their new canonical homes per the File Governance Pipeline.
2. The deprecated directory must be renamed with a `_DEPRECATED_` prefix and held in `10_Archive` for a minimum of one version cycle before deletion.
3. All sibling doctrine files referencing the deprecated path must be updated before the deprecation is finalized.

---

## Related Doctrine

- [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) - STOPGATE files written to 05_Tribunal_Inbox; agent write-path permissions
- [D04_Command_Post_Communications.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D04_Command_Post_Communications.md) - Communications bus operates within this file system layout
- [D05_Baseline_Promotion.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D05_Baseline_Promotion.md) - Baselines stored in 06_Baselines directory
- [D13_DART_Core.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D13_DART_Core.md) - Evidentiary receipts and SHA-256 audit logs routed to 11_Receipts
- [D15_Database_Administration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D15_Database_Administration.md) - DB backup exports routed to 10_Archive per REG-D06-09

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
