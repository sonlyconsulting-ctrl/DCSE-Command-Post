# EVALUATION — SC-WEBSITE-DOSSIER-BUILD-PROMPT v1.0

**Evaluated:** `SC-WEBSITE-DOSSIER-BUILD-PROMPT.md` (v1.0, 2026-08-10)
**Against:** `SC-AI-RFP-SIM-001` Sections A/B/C, `CP_OPEN_ITEMS_SC_AI_RFP_SIM.md`, project standing rules
**Result:** NOT READY for distribution as written. 12 defects (5 critical).
**Remedy:** `SC-WEBSITE-DOSSIER-BUILD-PROMPT-v1.1.md` — issued, supersedes v1.0.
**Date:** 2026-08-09

---

## 1. What v1.0 is

The sanitized, outbound twin of the SC-AI-RFP-SIM-001 build plan. Internal lane codes, the
protected-surface name, the related-brand name, and doctrine section refs were replaced with
neutral terms. **That sanitization is correct and is preserved in v1.1** — the document is written
for models outside the governance core.

The problem is that the sanitization pass also removed controls that were not sensitive and were
load-bearing.

## 2. Completeness — defects found

| # | Severity | Defect | v1.1 remedy |
| :-- | :-- | :--- | :--- |
| 1 | CRITICAL | "Protected content" never defined; the mandated automated scan has no target. An undefined scan reports PASS by default. | §0.2 — controlled term list, referenced by hash; a scan without a resolvable list version is a failed scan |
| 2 | CRITICAL | DCS Level 0 release gate absent. Phase 8 leadership read "Technical authority (go-live execution)" — an agent could self-approve publication. Section A makes this DCS-only and mandatory. | Phase 8 release authority restored, explicitly non-delegable |
| 3 | CRITICAL | All roles were placeholders ("Primary (strategy authority)"). Undistributable — poller output would produce duplicate or absent ownership. | §0.1 roster with per-phase Primary / Fallback / mandatory co-signer |
| 4 | CRITICAL | No pre-Phase-7 backup or before-state capture of the existing live site. Production changes with no proven revert path. | Phase 7 pre-work: verified backup **plus an executed restore test** before any modification |
| 5 | CRITICAL | Completion signaling was "exit gate met → proceed," bypassing `needs_review` and DCS acceptance. Contradicts the standing rule that an agent receipt is not completion. | §0.5 — `needs_review` mandatory; no path from `running` to `completed` |
| 6 | HIGH | No platform feasibility screen before the Phase 4 direction is selected. A direction chosen on aesthetics can be unbuildable on-platform, surfacing at Phase 7 when change is most expensive. | Phase 4 feasibility screen; NOT BUILDABLE directions are ineligible |
| 7 | HIGH | No protected-content scan at Phase 6. Verification jumped 5 → 7, skipping asset metadata — the likeliest leak surface in that phase. | Phase 6 scan covering filenames, alt-text, captions, lineage, EXIF/XMP, and text rendered inside images/video |
| 8 | HIGH | No artifact destinations, filenames, or task identity. "All approvals logged" named no log. Poller distribution needs rows with lane and status. | §0.4 destinations and naming; append-only decision log; gate-receipt schema |
| 9 | MEDIUM | Contradictory gate metrics: Phase 2 body "100% pass" vs. summary table "0% false positives"; Phase 3 80% vs. Section A's 100%. | Single stated metric per gate; contradictions resolved and the resolution noted inline |
| 10 | MEDIUM | The 80% three-click threshold defined no test population or task set — unmeasurable. | Phase 3 method: 10 fixed tasks, ≥5 human testers, ≥80% overall **and** ≥60% per task |
| 11 | MEDIUM | "100% WCAG AA" is not an achievable automated assertion; "Lighthouse 90+" unscoped (category, device, throttling, run count). | Split into automated-zero-violations + named manual checks; Lighthouse scoped to Performance, mobile, Slow 4G, median of 5 |
| 12 | MEDIUM | Toolchain access prerequisites dropped; Phase 5 could open without verified tool access. | §0.3 verification with per-tool PASS/FAIL; Phase 5 blocked on any FAIL |

Additional: v1.0 carried no prohibition on placeholder statistics, which the standing evidence rule
requires. Added as §0.6.

## 3. Effect assessment

As written, v1.0 distributed to a model team would have produced structurally confident phase
reports with (a) no enforceable safety property, since the central prohibition was undefined,
(b) no named accountability, and (c) a self-certifying path to publication. The predicted failure
mode is procedural drift and late-stage rework, not poor output quality — which matches the
failure pattern already recorded for this program.

## 4. Blocking dependencies (unchanged by this evaluation)

Open items 1-4 in `CP_OPEN_ITEMS_SC_AI_RFP_SIM.md` remain unmet. v1.1 is distributable, but
Phase 1 does not open until DCS Level 0 grants entry approval and the §0.2 term-list owner is
assigned.

## 5. Recommended next actions

1. DCS-L0 reviews v1.1 and confirms or amends the §0.1 roster mapping.
2. CTO is assigned the §0.2 protected-terms list with a delivery date. **This is the long pole** —
   Phase 2 cannot open without it.
3. DBA begins §0.3 toolchain verification in parallel with Phase 1 (no dependency).
4. Create `tribunal/SC-WEBSITE/` destinations per §0.4.
5. Distribute v1.1 via poller. Retain v1.0 as the superseded record; do not distribute it.
