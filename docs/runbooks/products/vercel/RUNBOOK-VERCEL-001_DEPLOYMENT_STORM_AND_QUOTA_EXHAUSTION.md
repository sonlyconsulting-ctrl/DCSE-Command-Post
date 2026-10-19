# RUNBOOK-VERCEL-001: Deployment Storm & Quota Exhaustion (`api-deployments-free-per-day`)

**Classification:** OPERATIONAL RUNBOOK · HIGH PRIORITY  
**Governing Standard:** DCSE Master Profile v7.3 // Vercel Deployment Ownership Standard  
**Historical Incident Record:** `docs/operations/VERCEL_DEPLOYMENT_STORM_CONTAINMENT_20260908.md`  
**Primary Surface:** Vercel Team `sonlyconsulting-ctrl's projects`, Monorepo Git pushes  
**Conformity Target:** 98%+ Operator Success Rate  

---

## 1. Problem Statement & Error Signature

Rapid-fire CI/CD preview builds triggered across monorepo projects (`sc-command-post`, `sc-escd`, `sc-agent-os`, `mental-ingenuity-qa`) by unrelated git commits deplete Vercel's daily build allowance, blocking all critical production updates.

### Observable Symptoms:
1. **Vercel CLI / Git Push Failure:**
   ```json
   {
     "status": "error",
     "reason": "deploy_failed",
     "message": "Resource is limited - try again in 24 hours (more than 100, code: \"api-deployments-free-per-day\")."
   }
   ```
2. **Production App Remains Stale:**  
   Code merged to `main` fails to deploy to live production domains (`sc-escd.vercel.app`, `os.sonlyconsulting.com`), leaving older builds active.
3. **Ghost Deployments:**  
   Unused or testing projects (e.g. `mental-ingenuity-qa`) continuously build on every commit made to unrelated workspaces.

---

## 2. Instant Diagnostic Command (CLI)

Run this command using Vercel CLI to inspect recent deployment counts and project states:

```powershell
vercel ls --scope sonlyconsulting-ctrls-projects
```

### Expected Output:
- **HEALTHY:** Deployments show `READY` status, recent builds occur only for explicitly targeted projects.
- **EXHAUSTED:** CLI returns `api-deployments-free-per-day` error code or shows consecutive `CANCELED` rows across secondary projects.

---

## 3. Remediation & Recovery Procedure

### Step 1: Implement `ignoreCommand` Build Suppression (Code Gate)
Add or verify the project ignore filter in the root `vercel.json` to silence orphan projects without deleting code:

```json
{
  "ignoreCommand": "[ \"$VERCEL_PROJECT_ID\" = \"prj_3t9SKxOUuW0peitSq97OHWDWCQy9\" ]"
}
```
*Note: Vercel convention treats exit code `0` as ignore (skip build) and `1` as proceed.*

### Step 2: Disconnect Orphan Git Links in Vercel Console (Web GUI)
1. Open [Vercel Dashboard](https://vercel.com/sonlyconsulting-ctrls-projects).
2. Go to secondary / inactive projects (e.g., `mental-ingenuity-qa`, `ctj-commercial-experience-preview`).
3. Navigate to **Settings > Git**.
4. Click **Disconnect** under Connected Git Repository.

### Step 3: Quota Recovery Protocol
- **DO NOT** attempt repeated manual redeployments while the 24-hour rate limit counter is active.
- Wait for the rolling 24-hour window to clear, or target the critical application exclusively using manual root scoping:
  ```powershell
  cd apps\escd
  vercel --prod --yes
  ```

---

## 4. Verification Gate

Verify that a commit pushed to `main` does NOT trigger builds on secondary projects:

```powershell
vercel inspect https://sc-escd.vercel.app
```

### Success Signature:
```text
● Production Deployment: Ready
● Target Domain: sc-escd.vercel.app
● Build Trigger: Targeted commit only
```

---

## 5. Permanent Prevention Strategy
1. **Strict Monorepo Root Mapping:** Every project in Vercel must have a configured **Root Directory** setting (e.g. `apps/escd`), never defaulting to the monorepo root.
2. **Mandatory Live Browser Previews:** (DCS Directive) Every visual or UI task requires an offline, zero-localhost HTML preview artifact before production deployment is authorized.
