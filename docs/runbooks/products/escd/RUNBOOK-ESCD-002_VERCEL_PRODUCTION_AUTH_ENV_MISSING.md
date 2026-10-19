# RUNBOOK-ESCD-002: Vercel Production Scope Missing Supabase Auth Environment Variables

**Classification:** OPERATIONAL RUNBOOK · HIGH PRIORITY  
**Governing Standard:** DCSE Master Profile v7.3 // DCSE D17 Supabase Doctrine  
**Historical Incident Record:** `_Tribunal_Inbox/TRIBUNAL_SESSION_REPORT_20260913_AG_ESCD_AUTH_CONFIG_RESTORED.json`  
**Primary Surface:** Vercel project `sc-escd` (`prj_TfGqYXFwkLfaZth644kXLn48CMVR`), Supabase Auth  
**Conformity Target:** 98%+ Operator Success Rate  

---

## 1. Problem Statement & Error Signature

When deploying `sc-escd` or `sc-command-post` to Vercel, the application builds successfully, but any authentication request immediately fails with a 500 error or exception.

### Observable Symptoms:
1. **Serverless Function Log / Exception:**
   ```text
   AuthError: auth_configuration_missing
   ```
2. **Frontend Symptom:**  
   Clicking Sign-in returns a blank or red banner stating `auth_configuration_missing` or `Unable to load auth configuration`.
3. **Underlying Cause:**  
   The required Supabase credentials (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`) were populated exclusively in the Vercel **Preview** or **Development** environment scope, but were absent from the **Production** scope.

---

## 2. Instant Diagnostic Command (CLI)

Run this command inside the project directory to check variable presence in the production scope:

```powershell
vercel env ls production --scope sonlyconsulting-ctrls-projects
```

### Expected Output:
- **DEFECTIVE:** `SUPABASE_URL` or `NEXT_PUBLIC_SUPABASE_URL` is missing from the list under the `Production` column.
- **HEALTHY:** All 5 variables are displayed with `type: Secret` or `Encrypted` under environment `Production`:
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_ROLE_KEY`
  - `NEXT_PUBLIC_SUPABASE_URL`
  - `NEXT_PUBLIC_SUPABASE_ANON_KEY`

---

## 3. Remediation & Recovery Procedure

### Automated Fix via Vercel CLI:
Populate the missing variables into the production scope:

```powershell
# In PowerShell / Bash:
$supaUrl = "https://nevgdyfpxdaloacuutal.supabase.co"
$supaAnon = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." # Replace with active anon key

# Add to production environment
vercel env add SUPABASE_URL production --value "$supaUrl"
vercel env add NEXT_PUBLIC_SUPABASE_URL production --value "$supaUrl"
vercel env add SUPABASE_ANON_KEY production --value "$supaAnon"
vercel env add NEXT_PUBLIC_SUPABASE_ANON_KEY production --value "$supaAnon"
```

### Redeploy Production Instance:
Environment variable additions in Vercel do **not** take effect until a new deployment is built:

```powershell
vercel --prod --yes
```

---

## 4. Verification Gate

Execute a live probe against the dynamic auth-config API endpoint:

```powershell
curl.exe -i "https://sc-escd.vercel.app/api/mvp/auth-config"
```

### Success Signature:
```json
HTTP/1.1 200 OK
Content-Type: application/json

{"supabase_url":"https://nevgdyfpxdaloacuutal.supabase.co"}
```

---

## 5. Permanent Prevention Strategy
1. **Unified Environment Scope Enforcement:** When provisioning variables in Vercel, always select all three environments (`Production, Preview, Development`) unless a feature flag intentionally isolates staging.
2. **Preflight Build Assertion:** The Python handler `_supabase_config()` in `apps/escd/api/mvp.py` asserts variable presence on invocation and returns deterministic errors rather than unhandled crashes.
