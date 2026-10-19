---
name: dcse-platform-runbooks
description: >-
  Operational troubleshooting runbooks and 98% conformity execution protocols for
  Supabase 504 dormancy, Poller mutex locks, Vercel quota exhaustion, environment scopes,
  and commerce access validation across DCSE products (ESCD, CTJ, SC, SS, TSL).
---

# DCSE Operational Runbooks & 98% Conformity Skill (v7.3-OPERATIVE)

This skill equips any DCSE AI agent (`antigravity`, `claude_code`, `codex`, `chatgpt`, `gemini`, `dolphin_mistral`) or human operator with deterministic, verified troubleshooting procedures for known platform incidents across Supabase, Vercel, Task Scheduler, and GitHub.

---

## 1. When to Activate This Skill

Activate and follow this skill immediately whenever encountering:
1. **HTTP 504 Gateway Timeout** on Supabase auth or data endpoints (`*.supabase.co/auth/v1/...`).
2. **Poller lock contention** or `SKIP ... mutex` lines in agent worker logs (`worker_*.log`).
3. **Vercel deployment failure** with error `api-deployments-free-per-day` or deployment storms.
4. **Missing environment variables** in Vercel production scope (`auth_configuration_missing`).
5. **Commerce claim token or identity defects** (`ACCESS-01`).

---

## 2. Core Operational Catalog

All runbooks reside under [`docs/runbooks/products/`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/) and follow the **98% User Conformity Standard** (Zero-Ambiguity, exact copy-paste syntax, expected vs. defective dual output signatures, and automated verification gates):

| Runbook ID | Title | Diagnostic Trigger | Runbook Link |
| :--- | :--- | :--- | :--- |
| **RUNBOOK-POL-001** | Poller Mutex Lock Contention & Orphan Worker Recovery | `worker_antigravity.log` has >5 consecutive `SKIP ... mutex` lines | [RUNBOOK-POL-001.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/poller/RUNBOOK-POL-001_POLLER_LOCK_WEDGING_AND_RECOVERY.md) |
| **RUNBOOK-ESCD-001** | Supabase 504 Gateway Timeout & Free-Tier Dormancy | Browser or curl returns 504 Gateway Timeout on `/auth/v1/authorize` | [RUNBOOK-ESCD-001.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/escd/RUNBOOK-ESCD-001_SUPABASE_504_GATEWAY_TIMEOUT_DORMANCY.md) |
| **RUNBOOK-VERCEL-001** | Vercel Deployment Storm & Quota Exhaustion | Vercel CLI returns `api-deployments-free-per-day` (>100 deploys/day) | [RUNBOOK-VERCEL-001.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/vercel/RUNBOOK-VERCEL-001_DEPLOYMENT_STORM_AND_QUOTA_EXHAUSTION.md) |
| **RUNBOOK-ESCD-002** | Vercel Production Scope Missing Auth Environment Variables | Serverless function throws `auth_configuration_missing` | [RUNBOOK-ESCD-002.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/escd/RUNBOOK-ESCD-002_VERCEL_PRODUCTION_AUTH_ENV_MISSING.md) |
| **RUNBOOK-CTJ-001** | Claim Token Consumption & Identity Hijack Prevention (`ACCESS-01`) | Negative regression gate asserts wrong-buyer claim denial | [RUNBOOK-CTJ-001.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/ctj/RUNBOOK-CTJ-001_CLAIM_TOKEN_IDENTITY_HIJACK_ACCESS01.md) |

---

## 3. The 98%+ Conformity Standard: 5 Zero-Ambiguity Rules

Every agent authoring or executing a runbook must strictly adhere to:
1. **Exact Copy-Paste Syntax:** Never ask the operator to manually construct paths or interpolate variables. Provide fully qualified, self-contained command strings.
2. **Dual Output Signatures:** Show the exact terminal output for a **FAILING** system and the exact terminal output for a **REPAIRED** system.
3. **Automated Preflight:** Verify prerequisites (CLI tools, environment tokens, network access) in Step 1.
4. **Independent Verification Gate:** Never mark a remediation task complete without executing a verifiable automated probe (HTTP 200/302, database query, or test suite).
5. **Immediate Fallback / Rollback:** Document a safe rollback command for every state-mutating action.

---

## 4. Master Registry Anchor

This skill is indexed and maintained under:
* **Tribunal Master Index:** [`_Tribunal_Inbox/TRIBUNAL_RUNBOOK_INDEX.md`](file:///C:/DS%20All%20Things/DCSE_Command_Center/_Tribunal_Inbox/TRIBUNAL_RUNBOOK_INDEX.md)
* **Control Plane Repository:** `sonlyconsulting-ctrl/DCSE-Command-Post`
