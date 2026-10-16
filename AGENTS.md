# AGENTS.md - Tri-Model Operations & Boundaries

## 1. Context Repository & Single Source of Truth
- Master Governance: `governance/Master-Profile-v7.3.md` (OPERATIVE, superseding v7.2 by DCS Executive Directive)
- Operative Principles & Context: `C:\DS All Things\DCSE_Command_Center\v7.3`
- Strategic Roadmap: Active execution operates under v7.3 to deliver priority initiatives (The Critical Thinker's Journey / CTJ at minimum) before formally advancing to v7.4.
- Do not invent database migrations or edit Supabase RLS policies.

## 2. Division of Labor
- Claude Code: System Architect & Schema Lead. Writes structural specs, JSON definitions, and integration tests.
- OpenAI Codex: Implementation Engineer. Writes component code and data transforms.
- Antigravity / Gemini (`agy`): Sovereign Auditor & Gatekeeper. Performs git diff reviews, verifies brand tone, and signs off on pull requests.

## 3. Branching Rules
- Direct push to `main` is prohibited.
- Work only in branches named `feat/<ticket-id>-<slug>`.

## 4. Mandatory Deliverable Rule: Live Browser Previews (DCS Directive)
- Whenever completing visual, UI, or component-related tasks, all models and subagents MUST generate and refresh a standalone, zero-localhost live browser preview file (e.g. `sc_homepage_preview.html`).
- Code diffs or text descriptions alone are insufficient for human acceptance gates; a direct, launchable browser preview artifact is required.

## 5. Distributed Multi-Node Orchestration
- Primary Node (`LAPTOP-74UF76GB`): Sovereign Controller & Interactive Preview Hub.
- Remote Node (`DESKTOP-PG1JATE`): Dedicated Compute & AI Orchestration Track (Playwright E2E suites, headless browser testing, and automated builds).
- Both nodes synchronize through GitHub branches, shared network paths (`\\DESKTOP-PG1JATE\Downloads`), and the ESCD Canonical Convergence Registry (`apps/escd/runtime/escd_canonical_convergence_registry.json`).

