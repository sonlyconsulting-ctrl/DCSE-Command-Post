# F-01 Lane Registry — DCS Input Evidence
## V7.2 R2 Review Finding, Persisting to R4

**Prepared by:** claude_code (CCR session, 2026-08-08)  
**For:** DCS decision on operative lane set (Tier 1 blocker)  
**Source:** Live query against `dcse_cp.agent_tasks` and `dcse_cp.runtime_surface_registry`

---

## Live Operational Lane Data (queried 2026-08-08T01:51 UTC)

| Lane | Task count | Status in R2 registry | Status in R4 registry |
|------|-----------|----------------------|----------------------|
| SYSTEM | 54 | **ABSENT** | Unknown — R4 not reviewed |
| DCSE | 20 | Present | Assumed present |
| TSL | 11 | Demoted (no routing rule) | Unknown |
| SS | 11 | Present | Assumed present |
| SC | 3 | Present | Assumed present |
| TRIBUNAL | 2 | **ABSENT** | Unknown |
| DDNA | 1 | **ABSENT** | Unknown |
| RAG | 0 tasks | **ABSENT** | Unknown |
| PS | 0 tasks in table | Present (protected) | Assumed present |

**Lanes in R2 registry with no live tasks:** DCS (role identity, not dispatch lane), TI (no grounding found), INFRA/TECH (maps to SYSTEM?)

---

## DCS Decision Required

For each of the following, DCS must designate the operative treatment:

1. **SYSTEM** — 54 active tasks. Enterprise lane or internal routing label?  
   If enterprise lane: add to registry, assign type, define compiler treatment.  
   If internal label: define routing rule (which enterprise lane absorbs SYSTEM tasks?).

2. **TRIBUNAL** — 2 active tasks. Enterprise lane or governed product domain?

3. **DDNA** — 1 active task. Enterprise lane or governed subdomain of DCSE?

4. **RAG** — 0 tasks but used as a routing label. Keep, route-through, or retire?

5. **TSL** — 11 active tasks. R2 demoted it. What enterprise lane absorbs TSL tasks in the compiler?

6. **DCS** — In R2 registry as a lane. Is DCS a dispatch lane or authority identity only?  
   If authority identity only: remove from lane registry, reclassify.

7. **TI** — In R2 registry. What is the v7.1 source grounding for TI as an enterprise lane?

8. **INFRA/TECH** — In R2 registry. Does this map to SYSTEM? If so, consolidate.

---

## Runtime Surfaces Requiring Activation Gate Designation (MP72-030)

Queried from `dcse_cp.runtime_surface_registry` (2026-08-08):

| Surface | Family | Can claim | Polling mode | Enabled |
|---------|--------|-----------|-------------|---------|
| claude_code_windows_cli | claude | YES | scheduled | YES |
| cli_windows_poller | claude | YES | scheduled | YES |
| codex_windows_cli | openai | YES | scheduled | YES |
| qwen_windows_cli | qwen | YES | scheduled | YES |
| chat_browser | claude | no | interactive | YES |
| controller_windows | dcse | no | controller | YES |
| desktop_app | claude | no | interactive | YES |
| remote_cloud_ccr | claude | no | interactive | YES |
| unspecified | legacy | no | legacy | YES |
| worker_v7 | dcse | no | legacy | YES |

**DCS must designate** which surfaces are "mandatory" for MP72-030 activation gate purposes.  
Suggested split: claiming surfaces (top 4) = mandatory activation; non-claiming surfaces = activation optional or read-only acknowledgment.

---

## Files Changed in This Correction Pass

| File | Change |
|------|--------|
| `CLAUDE.md` | Updated DDNA authority section to reflect actual DB state (D01-D22 promoted, R4 operative, D17=DART) |
| `governance/v7.1/instructions/CLAUDE_REVIEW_INSTRUCTIONS.md` | Added OC-1 through OC-4 operational cross-reference requirement |
| `docs/governance/DCSE_D17_SUPABASE_SECURITY_AND_AUTOMATION_DOCTRINE_v7.md` | Added naming conflict notice; flagged as incorrectly labeled D17 |
| This file | Created as DCS input for Tier 1 lane decision |
