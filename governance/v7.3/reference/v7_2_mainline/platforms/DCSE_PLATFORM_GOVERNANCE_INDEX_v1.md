# DCSE v7.2 Platform Governance Index v1

**Status:** OPERATIVE upon Level 0 package promotion  
**Authority:** DCS Level 0  
**Parent:** DCSE Master Profile v7.2 R5  
**Purpose:** Route platform-specific governance without inventing new numbered doctrines.

## 1. Architecture

Platform doctrines are **separate subordinate governance modules**, not D23/D24/D25 and not replacements for D01-D22.

| Platform | Platform doctrine | Controlling numbered doctrine(s) |
|---|---|---|
| GitHub | `platforms/github/DCSE_GITHUB_AGENT_PLATFORM_DOCTRINE_v1.md` | D22 source authority/persistence, D05 promotion, D04 evidence/communications, D21 runtime routing |
| Vercel | `platforms/vercel/DCSE_VERCEL_AGENT_PLATFORM_DOCTRINE_v1.md` | D20 product assembly, D21 runtime, D22 source/reconciliation, D05 promotion |
| Supabase | `platforms/supabase/DCSE_SUPABASE_AGENT_PLATFORM_DOCTRINE_v1.md` | D15 database administration, D22 persistence/reconciliation, D21 runtime, D05 promotion |

Shared execution remains in `execution/DCSE_PLATFORM_EXECUTION_PROFILES_GITHUB_VERCEL_SUPABASE_v1.md`.

## 2. Masterclass separation

Masterclass/annotated-source files are instructional source material. They remain separate from platform doctrine and never create authority by themselves.

- Vercel annotated source: `docs/vercel/DCSE_Vercel_Masterclass_Annotated_Source_20260915.md`
- Supabase source/audit materials remain separate from the platform doctrine and controlled manual.
- GitHub masterclass source, when canonically ingested, SHALL live under `docs/github/` and remain distinct from the GitHub platform doctrine.

## 3. Precedence

`MASTER PROFILE -> D01-D22 -> PLATFORM DOCTRINE -> OPERATIONS MANUAL / CONTROL MATRIX -> MASTERCLASS SOURCE -> PROJECT/TASK`

A platform doctrine specializes platform behavior. It may not supersede the Master Profile or its controlling numbered doctrines absent an explicit Level 0 amendment.

**Structure Precedes Scale.**
