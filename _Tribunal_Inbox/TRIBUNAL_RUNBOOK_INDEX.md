# TRIBUNAL OPERATIONAL RUNBOOK INDEX & 98% CONFORMITY PLAYBOOK

**Catalog ID:** `TRIB-RUNBOOK-INDEX-v7.3`  
**Governing Standard:** DCSE Master Profile v7.3 // DCS Level 0 Directives  
**Facility:** `_Tribunal_Inbox` (Primary Incident & Governance Anchor)  
**Standardized Catalog Path:** `docs/runbooks/products/`  
**Conformity Standard:** **98%+ Operator Success Rate** (Zero-Ambiguity Execution)  

---

## 1. Executive Index of Incident Runbooks

| Runbook ID | Title & Domain | Symptoms / Error Signatures | Primary Surface | Severity | Associated Tribunal Receipts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [`RUNBOOK-POL-001`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/poller/RUNBOOK-POL-001_POLLER_LOCK_WEDGING_AND_RECOVERY.md) | **Poller Mutex Lock Contention & Orphan Worker Recovery** | `SKIP ... task lock held by mutex`, Control Plane stagnation, ghost heartbeats | Windows Task Scheduler, PowerShell, `dcse_cp` | **HIGH** | `DCSE-CP-POLLER-RUNTIME-RECOVERY-20260917-H01` |
| [`RUNBOOK-ESCD-001`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/escd/RUNBOOK-ESCD-001_SUPABASE_504_GATEWAY_TIMEOUT_DORMANCY.md) | **Supabase 504 Gateway Timeout (Free-Tier Dormancy)** | Google OAuth & Email login timeout on `sc-escd`, Cloudflare 504 | Supabase Management API, `SC-Command-Post` | **CRITICAL** | `TRIB-20261019-ESCD-GATEWAY-TIMEOUT-RESOLVED` |
| [`RUNBOOK-VERCEL-001`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/vercel/RUNBOOK-VERCEL-001_DEPLOYMENT_STORM_AND_QUOTA_EXHAUSTION.md) | **Vercel Deployment Storm & Daily Quota Depletion** | `api-deployments-free-per-day` (>100 deploys/day), secondary projects building on all git commits | Vercel CLI, root `vercel.json` | **HIGH** | `DCSE-VERCEL-CONTAIN-20260908-001`, `DCSE-INCIDENT-20260919-01` |
| [`RUNBOOK-ESCD-002`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/escd/RUNBOOK-ESCD-002_VERCEL_PRODUCTION_AUTH_ENV_MISSING.md) | **Vercel Production Scope Missing Auth Environment Variables** | `auth_configuration_missing` 500 error on sign-in; keys present in Preview but omitted in Production | Vercel Environment Scopes, `apps/escd/api/mvp.py` | **HIGH** | `TRIB-20260913-ESCD-AUTH-CONFIG-RESTORED` |
| [`RUNBOOK-CTJ-001`](file:///C:/DS%20All%20Things/DCSE_Command_Center/docs/runbooks/products/ctj/RUNBOOK-CTJ-001_CLAIM_TOKEN_IDENTITY_HIJACK_ACCESS01.md) | **Claim Token Consumption & Identity Hijack Prevention (`ACCESS-01`)** | Wrong authenticated user consuming unburned claim token; order binding without identity verification | `commerce/access.mjs`, PostgreSQL `dcse_cp.ctj_claim` | **CRITICAL** | `DCSE-RELEASE-20261017-01`, `AG-RECEIPT-09-PR19-BE70C54-VERIFICATION-20261018` |

---

## 2. Lead Engineer Coaching: The "When to Use CLI" Decision Matrix

Every technical action carries a cognitive, operational, and audit cost. To maintain engineering rigor and prevent platform drift, follow this definitive matrix:

| Use the CLI / API when... | Use the Web GUI / Dashboard when... |
| :--- | :--- |
| **1. Repeatability & Determinism:** The task must yield the exact same outcome regardless of who runs it (e.g. running tests, restarting containers, pulling variables). | **1. Initial Visual Setup:** Configuring third-party OAuth consent screens (e.g., Google Cloud Console logo, terms, and brand verification). |
| **2. Diagnostic Precision:** You need raw HTTP response codes, latency timings, exact error JSON bodies, or stack traces without UI truncation. | **2. Spatial / Visual Review:** Reviewing end-user typography, animation transitions, or component layouts in a browser. |
| **3. Credential & Secret Isolation:** Passing bearer tokens or service keys via environment variables or secret vaults without exposing them in browser history or screen shares. | **3. High-Friction One-Time Setup:** Initial payment method entry or multi-factor recovery seed generation. |
| **4. State Verification & Audit Gates:** Proving that an assertion passes (e.g. `psql` transaction rollback, Playwright headless smoke, SHA256 checksums). | **4. Broad Organizational Exploration:** Browsing monthly billing graphs or reviewing audit log trends across months. |

---

## 3. The 98%+ Conformity Standard for Runbook Authoring

Runbooks typically fail in practice because they leave room for human operator interpretation. To guarantee **98%+ execution conformity** across human operators, subagents, and automated workers, every runbook must adhere to the **5 Zero-Ambiguity Rules**:

1. **Exact Copy-Paste Command Blocks:**  
   Never say *"Navigate to your project directory and run the test."*  
   Always provide the exact, fully qualified command:  
   `powershell.exe -ExecutionPolicy Bypass -File "C:\DS All Things\DCSE_Command_Center\scripts\test.ps1"`
2. **Explicit "Expected vs. Defective" Output Signatures:**  
   Always display both the exact terminal output of a **FAILING** system and the exact terminal output of a **REPAIRED** system so the operator never has to guess if the step worked.
3. **Preflight Step 1:**  
   Every procedure must begin with an instantaneous preflight command that checks prerequisites (e.g., verifying `supabase`, `vercel`, or `python` versions and authentication tokens).
4. **Mandatory Automated Verification Gate:**  
   A runbook is never marked complete until an independent verification probe (e.g., curling an endpoint, asserting HTTP 200/302, or checking an RLS constraint) passes.
5. **Deterministic Rollback / Fallback Instructions:**  
   Every mutating step must document an immediate, safe rollback path if unexpected output occurs.
