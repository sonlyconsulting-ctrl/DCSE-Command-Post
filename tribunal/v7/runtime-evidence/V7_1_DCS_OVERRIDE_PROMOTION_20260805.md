# v7.1 DCS-Override Promotion — Receipt

**Date:** 2026-08-05
**Executor:** Claude Code (Sonnet 5)
**Trigger:** DCS (sonlyconsulting@gmail.com), explicit chat instruction: *"ok...can you make everything promoted and available sounds like the last question/step...if so please do so."*
**Authority form:** `DIRECT_DCS` per D05 Sec. 2 ("Promotion is based solely on DCS authority... DCS approves the exact object")

## What this is, precisely

This is the second promotion wave. The first wave (see `V7_1_DOCTRINE_REGISTRY_PROMOTION_20260805.md`) promoted 11 doctrines (Master Profile, D03, D04, D05, D06, D15, D16, D17, D20, D21, D22) that independently passed the 2026-08-03 executability audit. It left 10 doctrines (D01, D02, D07, D08, D09, D10, D11, D12, D18, D19) registered honestly as `PARTIAL_NOT_EXECUTABLE` — real content, explicit gap, not promoted — because that audit found each one structurally incomplete.

DCS then explicitly directed promoting all of them. Per D05 Sec. 2, DCS approval of the exact object is a complete, sufficient form of promotion authority — it does not require the object to have separately passed an automated gate. This receipt records that override being exercised, and preserves exactly what it does and does not change.

## What changed

All 10 remaining rows in `dcse_cp.governance_directives` moved from `status=candidate, promotion_status=PARTIAL_NOT_EXECUTABLE` to `status=promoted, promotion_status=PROMOTED_WITH_KNOWN_GAPS` — a status deliberately distinct from the clean `PROMOTED` used by the first 11, so the record does not claim these are the same thing.

### Group A — real RC3-corrected candidates exist (`authority_level=DCS_OVERRIDE_KNOWN_GAPS`)

| ID | Title | SHA-256 | Known gap (2026-08-03 audit, not resolved by this promotion) |
|---|---|---|---|
| D01 | Forward Thinking | `b1eb4f764ec80722ee5040837561994bba42403284de0ae2de4269074e13033d` | no receipt, gate schema, or rollback |
| D02 | Forward and Backward Chaining | `a9d1acb4dd2bdc89d3bcb6ac27c7f77b514fab00a822317887fd281fa52d6885` | no durable evidence contract or promotion gate |
| D08 | Voice and Tone | `9605f1a5abc45ee104a2a460e708d488f27e57952b7542bdb1e8637e2dac4c64` | lacks objective pass criteria and evidence schema |
| D09 | Brand Identity | `2f3985b79bcc3f389d07d737f91d3fb36dd8f420c7f36cf78028c3f1ffa595ed` | lacks runtime receipt and rollback |
| D10 | Persona Assets | `cc6ad446c2b2000ec5bc57f91b2206ef25ce87d501e297c781abb798c0e3c8bd` | lacks explicit lifecycle and gate receipt |
| D11 | HTML, Wix, and App Governance | `78a3e088125205641bf523c8254f6764d26056bfbae1e6a2090f42ef7b8a5a9c` | lacks promotion receipt and rollback contract |

Each SHA-256 was independently recomputed from the fetched RC3 candidate file and matched against `V71_GOVERNANCE_VALIDATION_REPORT.json` before write — same standard as wave one.

### Group B — no RC3-corrected candidate exists at all (`authority_level=DCS_OVERRIDE_UNCORRECTED_SOURCE`)

| ID | Title | SHA-256 | Known gap |
|---|---|---|---|
| D07 | Campaign Governance | `fd65f3983eada0d02e905b3974aac7d235f0915c8e8825046e531a9315b53ce6` | lacks explicit inputs, outputs, receipts and rollback |
| D12 | Video and Media | `488039e82a0431c47592ca03ee16ad3f52d11caa450ef6aa0948cb329c5ac142` | lacks explicit Stop-Gate and durable receipt |
| D18 | Media Production Pipeline | `49b6007405a569829528db1d8e876a72be22c4ac720853f3048ede3ec9316c30` | lacks complete rollback and durable receipt details |
| D19 | Visual Creation Pipeline | `75f41e2fe811ef960fcc12f1d76dd05c889a20c9223ed6726d6d825fbffd337b` | lacks complete rollback and durable receipt details |

These four were confirmed absent from the 2026-08-03 executability audit's *processed* set — meaning no RC3-corrected candidate has ever existed for them in this repository, only the older v6.9-labeled uncorrected source. `body` for these rows is the actual uncorrected source text, explicitly labeled as such, not a fabricated corrected version.

## What did not change

- **The structural gaps are real and are not fixed.** Nothing about this promotion added a receipt schema, gate criteria, or rollback contract to any of these 10 doctrines. The gap text from the 2026-08-03 audit is preserved verbatim in each row's `body`.
- **D13/D14 remain untouched.** PS-protected, no row exists for either, same as wave one.
- **The engine's distinction is mechanical, not cosmetic.** `tribunal/v7/dcse_d21_runtime_engine.py` was updated so `DoctrineRecord.is_promoted()` treats both `PROMOTED` and `PROMOTED_WITH_KNOWN_GAPS` as available (selectable), while a new `needs_wrapper()` method independently flags every DCS-override row for D21 Sec. 8's executability wrapper — regardless of promotion status. Verified live: routing all 21 doctrines through `Router.route()` against this exact data selects all 21 and flags the same 10 as `wrappers_required`. Promotion and structural completeness are tracked as two different facts, on purpose.

## Verification

- 23/23 tests pass (`pytest tribunal/v7/test_d21_runtime_engine.py -v`), including two new tests (`test_d21_017`, `test_d21_017b`) added specifically to prove the override-promoted-but-still-needs-wrapper behavior.
- Live-proof: `tribunal/v7/runtime-evidence/dcl/DCL-LIVE-PROOF-002.dcl.json`, generated by running the adapter and router against the actual live `governance_directives` rows fetched this session. `selected: 21/21`, `wrappers_required: [D01, D02, D07, D08, D09, D10, D11, D12, D18, D19]`.

## Result

`dcse_cp.governance_directives`: 21/21 rows `status=promoted` — 11 `PROMOTED`, 10 `PROMOTED_WITH_KNOWN_GAPS`. "Everything promoted and available" is now literally true of the registry. Which 10 carry known structural gaps, and what those gaps are, remains visible in the same row rather than being cleared to make the summary look cleaner.

## Rollback

Same mechanism as wave one: every write was `ON CONFLICT (id) DO UPDATE`, preserving `created_at`. Reverting any of these 10 rows to `PARTIAL_NOT_EXECUTABLE` is a further `UPDATE` restoring the prior status/promotion_status/authority_level values recorded in `V7_1_DOCTRINE_REGISTRY_PROMOTION_20260805.md`.
