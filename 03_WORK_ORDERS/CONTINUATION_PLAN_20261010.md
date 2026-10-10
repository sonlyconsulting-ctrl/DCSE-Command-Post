# DCSE Continuation Plan — 2026-10-10

**Purpose:** Finite-step handoff so any new model session can resume without losing context.
**Lane:** DCSE / SC / SS
**Authority:** DCS directive from session `session_01Lu4ytWTTq8t6vGEqXfY26A`

---

## Repositories in Scope

| Repo | Local path | Default branch | Notes |
|------|-----------|---------------|-------|
| `sonlyconsulting-ctrl/SC-CTJ` | `/home/user/sc-ctj` | `main` | CTJ SPA (React + Vite, hash-routing) |
| `sonlyconsulting-ctrl/ctj-focus-and-flow` | `/home/user/ctj-focus-and-flow` | `main` | Focus & Flow app (React + Tailwind, Vite) |
| `sonlyconsulting-ctrl/ctj-mental-ingenuity` | `/home/user/ctj-mental-ingenuity` | `main` | Mental Ingenuity app (React + Vite) |
| `sonlyconsulting-ctrl/DCSE-Command-Post` | `/home/user/DCSE-Command-Post` | `main` | Governance, DCSE dashboard |

---

## COMPLETED — Do Not Repeat

### SC-CTJ Entitlement Gate (E3) — DONE (branch `review/ctj-preproduction-20261001`, PR #4)
- `EntitledApp` component: server-side verify via `ctj-delivery` edge function before rendering workspace.
- `#/app` route now redirects to `#/unified` without a valid session token.
- `#/app` "Continue" button removed from public nav; replaced with "Get Unified" routing to `#/unified`.

### Test Harness — DONE (50 tests pass; committed `dc56069`)
- `tests/e2e/helpers/entitlement.mjs` — mock helper
- `tests/e2e/entitlement-gate.spec.mjs` — 9 gate tests
- `tests/e2e/product-suite.spec.mjs` — 36 parameterized product tests
- `tests/e2e/ctj-smoke.spec.mjs` — 5 smoke tests (all fixed)
- `tests/e2e/preproduction.spec.mjs` — pre-production regression tests (all fixed)

Run tests with:
```bash
cd /home/user/sc-ctj
CTJ_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome npx playwright test
```

---

## PENDING WORK — Prioritized

### P1 — Operator Actions (Blocked on DCS / Netlify)

**O1: Stripe Payment Link return URLs**
All 5 Stripe Payment Links must be updated (via Stripe dashboard — NOT via script, existing links must not be duplicated):
```
Return URL: https://sonlyconsulting.com/ctj/?session_id={CHECKOUT_SESSION_ID}#/delivery
```
Do NOT recreate products/prices/links. Edit existing links only.

**O2: Unified price discrepancy**
Stripe live shows $125, controlled baseline says $119. DCS must resolve before public release.

**O3: Netlify redeploy for Parts 1-3 blank screen**
Branch `review/ctj-preproduction-20261001` has the fix. Netlify must redeploy this branch to the preview URL.
The fix: `PartProductPage` was passing a hardcoded tour ID that no longer exists in the `MediaTour` component. Fix committed in sc-ctj.

---

### P2 — Focus & Flow Modernization (`sonlyconsulting-ctrl/ctj-focus-and-flow`)

**Current state:** Single-page React app with Tailwind. Colors: `sc-navy #0A0F24`, `sc-gold #C8A444`, `sc-ivory #F6F2E9`. Header/footer present but minimal. No nav buttons between views.

**Requested changes (DCS directive):**
1. Brand color consistency — audit all color usage against `sc-navy / sc-gold / sc-ivory / sc-ink / sc-muted` palette.
2. Header redesign — match SC brand header style (logo left, title center or inline, minimal controls right).
3. Footer redesign — match SC brand footer ("Powered by Sonly Consulting" attribution, consistent with CTJ app).
4. Navigational buttons — add back/forward or step-indicator navigation between views (Welcome → Warmup → Journal → Export → Completion).
5. Visual appeal — improve spacing, typography weight, and section contrast.
6. Playwright automated tests — add `tests/e2e/` spec covering: renders without crash, nav flows, brand colors present.

**Work branch:** Create `claude/focus-flow-modernization` off main.
**Deploy target:** `https://sonlyconsulting.com/focus-flow/` (Netlify or Vercel — check existing deployment config).

---

### P3 — Mental Ingenuity "How to Play" Tab (`sonlyconsulting-ctrl/ctj-mental-ingenuity`)

**Current state:** React + Vite SPA. Has unique game-like UI with good brand uniformity (per DCS review). Existing footer matches SC style (confirmed via screenshot review).

**Requested changes (DCS directive):**
1. Add a "How to Play" tab — treat the exercise as a game/thinking game; tab should explain the rules, scoring logic, and journey metaphor.
2. Market entry strategy consideration: the "game" framing is a market entry strategy — lean into it; document the decision in a `MENTAL_INGENUITY_HOW_TO_PLAY_SPEC.md` before implementing.
3. Playwright automated tests — add `tests/e2e/` spec covering: renders without crash, "how to play" tab visible and accessible, no console errors.

**Work branch:** Create `claude/mental-ingenuity-how-to-play` off main.
**Deploy target:** `https://sonlyconsulting.com/mental-ingenuity/`

---

### P4 — Author/About Content Rewrite

**Repo:** SC-CTJ (`/home/user/sc-ctj/src/App.jsx` — look for Author/About/Intro sections).
**Issue:** Current content does not align with SC v7.3 brand voice. Too many generic AI-generated phrases. The About section and Author/Intro section do not harmonize.
**Direction:** v7.3 SC voice = precise, clinical, structure-forward. No em dashes. No filler. Capability claims must trace to verified facts. Third-person solo-brand posture.
**Action needed:** Read current content, draft replacement copy aligned to v7.3, present to DCS before committing.

---

### P5 — CTJ Thinking Exercise Reframe

**Concept (DCS notes):** CTJ's current framing skews toward "journey" or "journal." DCS wants to reframe as a "thinking exercise" — compare/contrast vs. journey/journal metaphor. The takeaway on first glance should be structured thinking, not narrative tracking.
**Scope:** Copy/content changes across product pages in SC-CTJ. No architecture change required.
**Action needed:** Draft revised framing and taglines; present to DCS before committing.

---

### P6 — GitHub Repository Reorganization

**Proposed structure (DCS direction):**
```
SC.com (parent)
  └── CTJ suite
        ├── SC-CTJ (main app)
        ├── ctj-focus-and-flow
        └── ctj-mental-ingenuity
SS.com (sibling to SC.com)
DCSE-Command-Post (cross-entity governance)
```

**Legacy repos to review (all public, superseded):**
- `SS-CTJ-Part1`, `SS-CTJ-Part2`, `SS-CTJ-Part3`, `SS-CTJ-Full`, `SS-CTJ-Part-3`
- **STOP-GATE:** Verify no live deployments point to these before archiving. Check Netlify/Vercel config.

**SC.com and SS.com website repos:** Do not exist yet. Creating them is a separate tracked task.

**DCSE-Command-Post visibility:** Currently public. DCS must decide: keep public or make private.

**Action needed:** Confirm no live traffic to legacy repos → archive them → create SC.com repo → create SS.com repo → move products under correct parent (Netlify/Vercel project transfer or re-link).

---

### P7 — Governance Records

**Market Intelligence Lab:**
- First run: Monday 2026-10-12 9AM ET
- Requires 3 consecutive runs for consistency
- Intelligence Study Model → recurring Market Intelligence Lab (not standalone TSL report)
- Record in DCSE Tribunal/task system after each run

**SC.com / SS.com priority:** SC.com is Priority 1, SS.com is Priority 2. CTJ held at DCS discretion.

**DDNA signal expansion:** Expanded to 5 signal types (details in TSL PR #6).

---

## Key Technical Facts for Next Session

### SC-CTJ app constants (in `/home/user/sc-ctj/src/App.jsx`)
```js
CTJ_DELIVERY_ENDPOINT = "https://nevgdyfpxdaloacuutal.supabase.co/functions/v1/ctj-delivery"
CTJ_WORKSPACE_KEY = "ctj_workspace_session"
```

### Entitlement logic
```js
// isEntitledTo(orderCode, requestedCode)
// CTJ-COLLECTION grants access to everything
// Parts do NOT grant workspace (#/app) access
// Only CTJ-UNIFIED and CTJ-COLLECTION grant #/app
```

### URL format for delivery page
```
/?session_id={CHECKOUT_SESSION_ID}#/delivery
// NOT: /#/delivery?session_id=...
// app reads window.location.search, not hash params
```

### Focus & Flow color tokens
```js
'sc-navy': '#0A0F24'
'sc-gold': '#C8A444'
'sc-ivory': '#F6F2E9'
'sc-ink': '#0E1422'
'sc-muted': '#6E7480'
```

### Chromium path (cloud container)
```
/opt/pw-browsers/chromium-1194/chrome-linux/chrome
// Set: CTJ_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
```

### Supabase project
```
Project ID: nevgdyfpxdaloacuutal
Schema: dcse_cp (24 tables)
```

---

## Security Constraints (Always Active)

- NEVER recreate Stripe products/prices/links (5 already exist).
- SUPABASE_SERVICE_ROLE_KEY and provider API keys must never appear in HTML, console.log, responses, or error messages.
- No secrets committed to any repository.
- No PS content in any dispatch or build.
- No direct-to-main push without DCS authorization.
- No force push to main.
- Do not infer payment from redirect alone; entitlement verification stays server-side.
- Do not expose purchase records or Stripe session IDs in GitHub.

---

## How to Resume

1. Add repos to session: `add_repo` for each of the 4 repos above.
2. Clone each one sequentially (proxy caps at 2 concurrent HTTP ops).
3. Start with P2 (Focus & Flow) or P3 (Mental Ingenuity) — both are unblocked code work.
4. For P1 (Operator actions) — report to DCS, do not execute without authorization.
5. For P6 (GitHub reorg) — do NOT archive legacy repos until live deployment check is complete.

---

_Last updated: 2026-10-10 by Claude Code session `session_01Lu4ytWTTq8t6vGEqXfY26A`_
