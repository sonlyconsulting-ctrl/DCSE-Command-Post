# GoTime PM Backbone — Leakage Scan Spec

**Status:** Draft, produced by Claude (Code) as Validator/Red Team under the 2026-07-02 redirect order. Governs the mandatory scan step for `POST /api/work-orders/from-tribunal` and `POST /api/work-orders/from-markdown` before any intake reaches a work order.

## Why this exists

Two real incidents today made this non-optional rather than nice-to-have: (1) PS case facts (case number, discovery deadline, defendant names) were pasted directly into an Employment/SC-scoped chat thread and had to be caught manually; (2) actual litigation filings were found sitting inside a public product release-candidates folder (`SC_CTJ/.../02_FINAL_RELEASE_CANDIDATES/`). Both were caught by a human/AI noticing, not by a system control. An automated intake pipeline removes that human noticing step unless the scan is built in.

## State flow (mandatory, per redirect order Phase D)

```
RAW_INTAKE → LEAKAGE_SCAN_PENDING → FLAGGED_PS_HOLD | CLEARED_FOR_WORK_ORDER_DRAFT → DCS_REVIEW → WORK_ORDER_READY
```

No path exists from `RAW_INTAKE` directly to `WORK_ORDER_READY`. Every record passes through the scan. `CLEARED_FOR_WORK_ORDER_DRAFT` still requires `DCS_REVIEW` before promotion — the scanner reduces DCS's review burden (only flagged items need deep review), it doesn't remove DCS from the loop.

## Scan terms (minimum set, from the redirect order — extend, don't shrink, without DCS sign-off)

Case-identifying: `8:23CV489`, `Seals v. DHHS`, `DHHS`, `Nebraska`, `Ballentine`

Procedural/legal vocabulary: `docket`, `motion`, `summary judgment`, `bench trial`, `exhibit`, `witness`, `deposition`, `Rule 52`, `Title VII`, `§1981`, `§1983`, `Darden`

Structural: known PS folder names (`DCSE_PS_CP_Project`, `DS Litigation`, `Pro Se Docs`, `PS_WIN_WIN_WIN`, any path containing `PS_` prefix), court names (District of Nebraska, Hruska Federal Courthouse), judge names (Rossiter, DeLuca), attorney/party/witness names from a protected local list (not hardcoded in this spec — maintained separately, see "Protected name list" below)

## Match logic

- **Case-insensitive substring match** on all terms above against the full raw intake text (both the Tribunal JSON payload and pasted markdown).
- **Any single match is sufficient to hold.** Do not require multiple matches or a confidence threshold — this control is intentionally biased toward over-flagging (false positives are cheap: a human reviews and clears; false negatives are expensive: PS content silently becomes a public-visible work order).
- **§1981/§1983 matching:** match both the section-symbol form and the spelled-out form (`Section 1981`, `42 U.S.C. 1981`) since intake text won't always use the § glyph.
- **Protected name list:** attorney names (Justin J. Hall, Tyrone E. Fahie, Byndon Law, Olowolafe Law Firm), witness names (Lori Snyder, Dannette Smith, and any name appearing in `PS_EXHIBIT_WITNESS_INDEX_STATUS.md` once that file exists), and the defendant names already known from today's tribunal records (Converse, Christensen, Schafers). This list lives in a config table or protected file the scanner reads at runtime, not inline in application code, so it can be updated without a redeploy. It is itself `DcseLane = PS` classified — the scanner needs read access to it, but it must not be exposed via any public or non-PS-scoped API.

## On match (`FLAGGED_PS_HOLD`)

1. Do not create a work order.
2. Set intake record status to `FLAGGED_PS_HOLD`.
3. Store the raw intake text in the quarantine/staging table only — never copy it into a `WorkOrder` or `Task` row, even in a "pending" state.
4. Dashboard displays a redacted summary only: source, timestamp, matched-term count (not the matched terms themselves, not surrounding context — showing which term matched can itself leak information to a non-PS-authorized viewer).
5. Require explicit DCS PS-lane review before any further action on that intake record.
6. Create a Tribunal receipt entry for the hold (id, timestamp, source, match count, reviewer assigned — not match content).

## On no match (`CLEARED_FOR_WORK_ORDER_DRAFT`)

Still routes to `DCS_REVIEW` before `WORK_ORDER_READY` — a clean scan is necessary, not sufficient, for promotion. This catches paraphrased or indirect references the term list doesn't cover.

## Test cases (minimum required before this scanner ships)

| # | Input | Expected result |
|---|---|---|
| 1 | Raw text containing "8:23CV489" | `FLAGGED_PS_HOLD` |
| 2 | Raw text containing "the DHHS case" | `FLAGGED_PS_HOLD` |
| 3 | Raw text mentioning "summary judgment" in a non-case context (e.g. a generic legal-industry article pasted by mistake) | `FLAGGED_PS_HOLD` — false positive is acceptable and expected; a human clears it |
| 4 | Raw text about the CTJ product roadmap, no PS terms | `CLEARED_FOR_WORK_ORDER_DRAFT` |
| 5 | Raw text with a protected witness name but no other PS term | `FLAGGED_PS_HOLD` |
| 6 | Tribunal JSON with `"LANE": "DCSE // PS"` in its own metadata field, regardless of body text match | `FLAGGED_PS_HOLD` — lane field itself is a match condition, not just body text |
| 7 | Empty/near-empty intake (e.g. a title-only stub) | `CLEARED_FOR_WORK_ORDER_DRAFT`, but flag for DCS review as "insufficient content to classify" rather than silently clearing |
| 8 | Raw text containing §1981 in numeric-only form "1981" without section context | Should NOT match on the bare number alone (too many false positives — "1981" could be a year). Match only "§1981", "Section 1981", "42 U.S.C. 1981", or "42 U.S.C. §1981" |

## False-positive handling

False positives are the expected cost of this design, not a bug to eliminate. Handling:
- `FLAGGED_PS_HOLD` records include a DCS override action: "confirmed non-PS, promote to work order draft" — logged with who/when, creates its own receipt entry.
- Track false-positive rate over time (flagged-then-cleared vs. flagged-then-confirmed-PS) in the Deliverables/Blocked Items register. If false-positive rate is high enough to create real review burden, that's a term-list tuning conversation with DCS — not a reason to loosen the match logic unilaterally.

## Explicitly out of scope for this spec

- This scanner does not scan file attachments/binaries (docx/pdf) referenced by `sourcePath` — only the raw text/JSON payload submitted to the intake endpoints. Binary-content scanning is a separate, larger effort (would need the same text-extraction approach used elsewhere this session for docx/pdf review) and should not block this phase.
- This scanner is not a substitute for the Phase 1 full PS-contamination sweep of SC_CTJ/SC_TSL/SC_Gov-OS/SC_FLAGSHIP — that's a one-time folder audit, this is an ongoing intake control. Both are needed.
