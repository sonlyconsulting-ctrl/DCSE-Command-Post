# Tribunal Task Record — SC Netlify Deploy Package Elements

**Artifact Type:** Tribunal Task Record
**Task ID:** TRIB-SC-NETLIFY-DEPLOY-001
**Status:** READY FOR DEPLOY
**Generated:** 2026-08-19
**Authority:** DCSE Master Profile v7.2 R5 — Compiled Governance Controller
**Associated Records:** `TRIBUNAL_TASK_SC_WEBSITE_CONTENT_ELEMENTS.md`

---

## Mission: SC Website — Netlify Deploy Package

Package the production-ready Sonly Consulting website (homepage + product/tool pages) into a single static folder for manual drag-and-drop deploy to Netlify under `sonlyconsulting.com`.

**Assigned To:** Claude (Chat/Design)
**Built From:** `Sonly Consulting Homepage.dc.html`, `CTJ Product Line.dc.html`, `Get Your Think On.dc.html`, `ctj-strategic-clarity-assessment.html`, `gyto-clarity-compass.html`

---

## Deploy Package Contents (`deploy/`)

| File | Role | Notes |
|---|---|---|
| `index.html` | Homepage / site root | Hero → audience cards → three pillars → Ecosystem tabs → ways to work → Studio (Assessment + CTJ) → Mental Ingenuity → Smoove Spots → SC Method → final CTA (contact form) → footer |
| `CTJ Product Line.dc.html` | Product/pricing page | Parts 1–3 @ $35 ea, Full Series $85/$105, Unified Edition $125; links back via `index.html` |
| `Get Your Think On.dc.html` | GYTO brand page | Thought Cycle™ 6 stages, hero video, CTA to quiz |
| `gyto-clarity-compass.html` | Live quiz tool | Linked from GYTO page and homepage |
| `ctj-strategic-clarity-assessment.html` | Live CTJ assessment | Linked from homepage Studio section and CTJ page |
| `support.js` | DC runtime | Required by all `.dc.html` files — do not edit |
| `uploads/` | Media + document assets | Images, video, Privacy Policy PDF, Terms DOCX |

---

## Internal Link Corrections Applied

- All "back to homepage" links across product/tool pages repointed from `Sonly Consulting Homepage.dc.html` → `index.html` (Netlify serves `index.html` as site root).
- Smoove Spots CTA → `https://smoove-spots.vercel.app`
- Mental Ingenuity CTA → `https://mental-ingenuity-qa.vercel.app/`
- Inquiries form → Netlify Forms (`data-netlify="true"`, name="inquiries"), activates once live on Netlify.

---

## Status

**READY FOR DEPLOY** — Package assembled and downloaded by DCS as a zip. Awaiting manual Netlify deploy (Add new site → Deploy manually → drag folder) and DNS repoint of `sonlyconsulting.com` (domain transfer from Wix pending).

## Next Step

DCS to deploy `deploy/` folder to Netlify, confirm live `*.netlify.app` URL, then repoint domain DNS once the Wix-to-registrar transfer completes.
