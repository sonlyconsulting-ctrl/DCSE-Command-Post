# DCSE-DDNA Physical Legacy Transfer Receipt

**Parent Task ID:** DCSE-RCHE-20260909-EMP-HARVEST-001
**Subtask:** DCSE-DDNA-PHYSICAL-TRANSFER-20260909-001
**Status:** COMPLETE
**Started:** 2026-09-09T14:54:37.695Z
**Completed:** 2026-09-09T14:55:25.785Z

## Scope

This receipt records the exact physical preservation transfer requested in GitHub Issue #65 for PR #64. The source project was `nevgdyfpxdaloacuutal` / `dcse_cp`; the destination project was `uutpzaiqymyufljdgdaa` / `dcse_ddna_legacy`.

No source rows were deleted or mutated. No consumer cutover was performed. No rule, source, or runtime record is promoted to governing authority by this transfer.

## Transfer Counts

| Table | Source rows | Destination rows | Per-row equivalence | Aggregate fingerprint | Source aggregate SHA-256 |
| --- | ---: | ---: | --- | --- | --- |
| ddna_source_queue | 129 | 129 | PASS | PASS | f57a4c08fc2221576602cb44353d383c2dfac65885d81dcd036d520fe91ee2e2 |
| ddna_ollama_jobs | 40 | 40 | PASS | PASS | e49d5c97248c128cc885a41634f113b9b72c19b26009f0467f59ba3e3dfe5c43 |

## Provenance

Per-row provenance links were recorded in `dcse_ddna.provenance_links` with source project, source schema/table, source key, copy event, destination project, destination schema/table, destination key, and row fingerprint metadata.

Provenance link count for this copy event: 169

## Safety Checks

- PS lock scan: PASS_NONE_DETECTED
- Secret pattern scan: PASS_NONE_DETECTED
- Source post-transfer fingerprint check: PASS
- Consumer cutover: NOT PERFORMED
- Source mutation: NOT PERFORMED
- PR merge: NOT PERFORMED

## Advisor Review

Destination security advisor result count at warning level or above: 1
Destination performance advisor result count at warning level or above: 1

Advisor findings are recorded in the validation JSON. Inherited findings outside the transfer scope were not remediated in this task.

## Final Status

COMPLETE

Structure Precedes Scale.
