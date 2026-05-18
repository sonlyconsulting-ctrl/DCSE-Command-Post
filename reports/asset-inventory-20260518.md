# DCSE Asset Inventory Report
**Scan Date:** 2026-05-18T21:44:16Z  
**Root Path:** `.`  
**Total Files Scanned:** 13  
**Scan ID:** `b07ba2fc-c9b2-445a-9a36-a10f4f41f173`  
**Governed by:** DBA Stop-Gate Active — DCS approval required before any promotion

---

## ⚠ CREDENTIAL EXPOSURE — Immediate Review Required

The following files contain credential strings outside `.env` files:

- `supabase/migrations/0005_cron_ddna_extractor.sql`
- `scripts/dcse_asset_inventory.py`
- `scripts/dcse_ddna_extraction_v01.py`
- `docs/audit/DCSE_End_of_Day_DDNA_Sweep_20260516.md`
- `docs/audit/extraction-rules.md`
- `docs/audit/schema-audit-2026-05-18.md`

**Action:** Rotate all referenced credentials before any external push.

---

## 1. Executive Summary

### Files by Lane

| Lane | Count |
|---|---|
| DCSE | 13 |

### Files by Lifecycle Stage

| Stage | Count |
|---|---|
| Captured | 13 |

### Files by Output Type

| Type | Count |
|---|---|
| SQL Script | 5 |
| Doctrine / Doc | 5 |
| Python Script | 2 |
| Manifest / Data | 1 |

### Risk and Gate Flags

| Flag | Count |
|---|---|
| Credential Exposure Risk | 6 |
| Rls Unverified | 2 |
| Codebase Gate Active | 5 |

---

## 2. Known EOD Asset Cross-Reference

Files matched against EOD manifest: **0** of 13

| External ID | Known Title | File | Lane | Stage |
|---|---|---|---|---|

---

## 3. Pending DCS Review

**0** files carry `pending_approval` status from the EOD manifest.

| File | Lane | Output Type | Known Title |
|---|---|---|---|

---

## 4. Folder-by-Folder Inventory

### `docs/audit`

Files: 6

| Filename | Type | Lane | Stage | DDNA Layers | Flags |
|---|---|---|---|---|---|
| `DCSEDDNAExtractionRoutinev1-20260515.md` | Doctrine / Doc | DCSE | Captured | Sentiment | Logic | Design | Product | Technical | — |
| `DCSE_End_of_Day_DDNA_Sweep_20260516.md` | Doctrine / Doc | DCSE | Captured | Sentiment | Logic | Design | Technical | creds! |
| `dcse_eod_daily_asset_ddna_20260517.json` | Manifest / Data | DCSE | Captured | Sentiment | Logic | Design | Product | Technical | — |
| `dcse_eod_daily_asset_ddna_20260517.md` | Doctrine / Doc | DCSE | Captured | Sentiment | Logic | Design | Product | Technical | — |
| `extraction-rules.md` | Doctrine / Doc | DCSE | Captured | Sentiment | Logic | Design | Product | Technical | creds! |
| `schema-audit-2026-05-18.md` | Doctrine / Doc | DCSE | Captured | Logic | Design | Technical | creds! |

### `scripts`

Files: 2

| Filename | Type | Lane | Stage | DDNA Layers | Flags |
|---|---|---|---|---|---|
| `dcse_asset_inventory.py` | Python Script | DCSE | Captured | Sentiment | Logic | Design | Product | Technical | creds! |
| `dcse_ddna_extraction_v01.py` | Python Script | DCSE | Captured | Logic | Technical | creds! |

### `supabase/migrations`

Files: 5

| Filename | Type | Lane | Stage | DDNA Layers | Flags |
|---|---|---|---|---|---|
| `0001_baseline_comment.sql` | SQL Script | DCSE | Captured | Logic | Design | Technical | rls?, gate active |
| `0002_rls_dcse_ddna_signals.sql` | SQL Script | DCSE | Captured | Logic | Design | Technical | gate active |
| `0003_rls_model_activity_log.sql` | SQL Script | DCSE | Captured | Logic | Design | Technical | gate active |
| `0004_missing_tables.sql` | SQL Script | DCSE | Captured | Logic | Design | Technical | gate active |
| `0005_cron_ddna_extractor.sql` | SQL Script | DCSE | Captured | Logic | Design | Technical | rls?, creds!, gate active |

---

## 5. Open Items for DCS

Generated from active flags. Resolve before any promotion or push.

- [ ] Rotate credentials for 6 flagged file(s)
- [ ] Verify or add RLS for 2 SQL file(s)
- [ ] Resolve codebase gate (v0.2 Supabase migration blocked — see sweep 2026-05-16) for 5 file(s)

---

*End of DCSE Asset Inventory Report*
