# Tribunal Record — Sonly Consulting Social Campaign

**Tribunal ID:** `TRIBUNAL_20260816_SC_SOCIAL_CAMPAIGN_STATUS`
**Task ID:** TRIB-SC-DIGITAL-CAMPAIGN-002
**Status:** IN PROGRESS — MULTIPLE TRACKS AWAITING CONFIRMATION
**Generated:** 2026-08-16
**Build Platform:** Claude (Design Component / HTML)

---

## 1. Scope

Sonly Consulting (SC) digital campaign presence: birthday race event promotion (Wix landing page + Facebook post) and DCSE Tribunal governance infrastructure (GitHub + Supabase).

## 2. Delivered Artifacts

| Artifact | Description |
|---|---|
| `Sonly Wix Landing.dc.html` | Live editable source (Design Component) |
| `Sonly Wix Landing - Wix Embed.html` | Bundled export for manual paste into Wix Custom Embed |
| `Sonly Facebook Post.dc.html` | Facebook post design (video + caption) |
| `assets/birthday-race-results.mp4` | July 30 Birthday Race event video, 19 sec |
| `DCSE-Tribunal-Relay` (GitHub) | Governance repo, synced through 2026-07-27 |

## 3. Build Summary

- **Wix landing page:** rotating SC logo header (new standard for all future SC webpages), 4-section layout, Contact CTA linking to `/inquiries` form (replaces prior email CTA), 2026 footer.
- **Wix embed constraint:** page (~620KB) exceeds Wix Custom Embed's 15,000-char API limit — cannot be auto-placed; bundled file must be pasted manually into the Wix editor.
- **Facebook post:** auto-publish blocked (requires OAuth, not yet implemented); Facebook API work halted per directive. Delivered as two manual uploads — video (`July 30 Birthday Race Results-989e9bcf.MP4`) + caption text — to user's Facebook account.
- **DCSE Tribunal scope:** limited to SC/SS/DCSE content. Pro Se (PS) litigation files found in repo are out of scope and flagged for removal.
- **Access boundaries:** GitHub write access unavailable to Claude — commits must be pushed locally by user. Supabase write access available via MCP.

## 4. Open Items

- Confirm: create new Supabase table `v7_build_status_report` (JSONB) for v7.0 compliance/lessons record, or use existing schema.
- PS-flagged file removal list staged — awaiting go-ahead on exact `.gitignore` update + removal commands.
- Manual paste of Wix embed into live Wix editor (not yet performed by user).
- Manual publish of Facebook post (video + caption uploaded to account, not yet posted live).

## 5. Status

**IN PROGRESS** — Wix and Facebook deliverables build-complete and staged for manual publish; DCSE Tribunal infrastructure work (Supabase schema, PS file cleanup) awaiting user confirmation before proceeding.
