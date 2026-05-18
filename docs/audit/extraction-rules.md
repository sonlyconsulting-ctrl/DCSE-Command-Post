# DCSE Asset Inventory — Extraction Rules
**Version:** v1  
**Date:** 2026-05-18  
**Source authority:** DCSE-DDNA-EXTRACT-ROUTINE-001 v1 + EOD-DDNA-ASSET-CAPTURE-20260517-001  
**Governed by:** DBA Stop-Gate (active)

---

## 1. Scope

These rules govern the automated file-system inventory scan of the DCSE working directory tree. The scanner walks every subfolder, classifies every file, cross-references against the known EOD asset manifest, and outputs a structured report and CSV for DCS review.

The scan is **read-only**. No files are moved, renamed, or written to the source directory.

---

## 2. Input

| Parameter | Value |
|---|---|
| Root path | `C:\DS All Things\dcse-sc-sportsociety` (or CLI argument) |
| Known asset manifest | EOD JSON: `dcse_eod_daily_asset_ddna_20260517.json` |
| Ignored patterns | `.git`, `__pycache__`, `node_modules`, `*.tmp`, `*.log` |

---

## 3. Lane Assignment Rules

Lane is inferred from folder path and filename prefix. First match wins.

| Pattern (case-insensitive) | Lane |
|---|---|
| `\ps\`, `\ps_`, filename starts with `ps_` | PS (isolated — DCS authorization required before any extraction) |
| `\sc\`, `\sc_`, `sc_home`, `sc_about`, `sonly` | SC |
| `\ss\`, `\ss_`, `sportsociety` | SS |
| `\emp\`, `\employment\`, `dcs_resume`, `dcs_hero` | EMP |
| `\dcse\`, `\eod\`, `dcse_`, `eod_`, `ddna` | DCSE |
| matches multiple lanes above | CROSS |
| no match | DCSE (default) |

---

## 4. Lifecycle Stage Rules

| Condition | Stage |
|---|---|
| File in known EOD manifest AND status = `COMMITTED_AND_VERIFIED` | Promoted |
| File in known EOD manifest AND status = `pending_approval` | Staged |
| File path contains `staging`, `inbox`, `plan_inbox` | Staged |
| File path contains `reviews`, `confirmed`, `pm_artifacts`, `canonical` | Confirmed or Promoted |
| File path contains `archive` | Archive |
| Otherwise | Captured |

---

## 5. Output Type Rules

| Extension(s) | Output Type |
|---|---|
| `.html`, `.htm` | HTML Module |
| `.sql` | SQL Script |
| `.py` | Python Script |
| `.md` | Doctrine / Doc |
| `.json` | Manifest / Data |
| `.docx`, `.doc` | Word Document |
| `.csv` | Data / Report |
| `.pdf` | PDF |
| `.txt` | Text |
| `.png`, `.jpg`, `.svg`, `.ico` | Image / Design Asset |
| `.tsx`, `.ts`, `.js` | Frontend Code |
| other | Binary / Unknown |

---

## 6. DDNA Layer Signal Rules

Each file receives a list of DDNA layer flags based on keyword matching in filename and (optionally) first 200 lines of content.

### Layer 1 — Sentiment
Keywords: `sweep`, `posture`, `morale`, `voice`, `tone`, `friction`, `readiness`

### Layer 2 — Logic
Keywords: `workflow`, `routing`, `gate`, `trigger`, `lifecycle`, `stage`, `doctrine`, `rule`, `decision`, `audit`

### Layer 3 — Design
Keywords: `html`, `css`, `color`, `typography`, `layout`, `playfair`, `amber`, `obsidian`, `tab`, `nav`, `icon`, `badge`  
Extensions: `.html`, `.svg`, `.css`

### Layer 4 — Product
Keywords: `candidate`, `template`, `home`, `about`, `resume`, `hero`, `glossary`, `services`, `guide`, `prototype`

### Layer 5 — Technical
Keywords: `rls`, `policy`, `migration`, `service_role`, `anon_key`, `supabase`, `pg`, `insert`, `alter`, `create`, `cron`, `ddna`, `extract`, `registry`  
Extensions: `.sql`, `.py`

---

## 7. Risk and Gate Flags

These flags are appended per file and must be resolved before DCS promotes any flagged asset.

| Flag | Trigger Condition |
|---|---|
| `ps_risk_flag` | File in a `ps_` lane folder, or filename contains `ps_risk` |
| `dba_stop_gate_required` | `.sql` file not located under a `migrations/` folder |
| `rls_unverified` | `.sql` file that does NOT contain the string `enable row level security` |
| `credential_exposure_risk` | Any file containing `service_role_key`, `anon_key`, or `SUPABASE_URL` as a literal string (outside `.env*` files) |
| `codebase_gate_active` | File relates to Supabase migrations and the sweep gate is active (per 2026-05-16 sweep) |
| `pending_dcs_review` | File matched in EOD manifest with status `pending_approval` |

---

## 8. Known EOD Asset Cross-Reference

The scanner loads `dcse_eod_daily_asset_ddna_20260517.json` at startup and builds a lookup table of all 27 known external IDs and their titles. For each scanned file, it attempts to match the filename (minus extension, lowercased, hyphens/underscores normalized) against this lookup. A match populates `known_external_id` and `known_asset_title`.

---

## 9. Output Fields (Asset Record Schema)

Every file in the inventory produces one record with these fields:

| Field | Source |
|---|---|
| `scan_id` | Auto-generated UUID per scan run |
| `scan_date` | Run timestamp |
| `file_path` | Absolute path |
| `folder` | Immediate parent folder name |
| `subfolder_depth` | Integer depth from root |
| `filename` | File name with extension |
| `extension` | Lowercased extension |
| `file_size_bytes` | OS stat |
| `last_modified` | OS stat (ISO 8601) |
| `output_type` | Rule §5 |
| `lane` | Rule §3 |
| `lifecycle_stage` | Rule §4 |
| `ddna_layers` | Rule §6 (pipe-separated list) |
| `known_external_id` | Rule §8 |
| `known_asset_title` | Rule §8 |
| `ps_risk_flag` | Rule §7 |
| `dba_stop_gate_required` | Rule §7 |
| `rls_unverified` | Rule §7 |
| `credential_exposure_risk` | Rule §7 |
| `codebase_gate_active` | Rule §7 |
| `pending_dcs_review` | Rule §7 |
| `notes` | Free text (populated when multiple flags active) |

---

## 10. Enforcement

- Scan is read-only. No source files are modified.
- PS-lane files are listed but content scanning is skipped. Lane, path, and metadata only.
- Any file raising `credential_exposure_risk` is listed in a dedicated **Credential Exposure** section at the top of the report.
- Summary totals by lane, lifecycle stage, and output type are generated at report footer.
- Report and CSV are written to `reports/` in the Command Post repo. They are not written back to the source working directory.
