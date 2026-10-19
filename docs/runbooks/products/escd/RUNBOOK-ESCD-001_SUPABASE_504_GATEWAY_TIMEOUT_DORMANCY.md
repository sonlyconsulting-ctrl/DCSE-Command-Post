# RUNBOOK-ESCD-001: Supabase 504 Gateway Timeout & Free-Tier Dormancy Recovery

**Classification:** OPERATIONAL RUNBOOK · CRITICAL  
**Governing Standard:** DCSE Master Profile v7.3 // DCSE D17 Supabase Doctrine  
**Historical Incident Record:** `_Tribunal_Inbox/TRIBUNAL_SESSION_REPORT_20261019_AG_ESCD_GATEWAY_TIMEOUT_RESOLVED.md`  
**Primary Surface:** `sc-escd.vercel.app`, Supabase `nevgdyfpxdaloacuutal` (`SC-Command-Post`)  
**Conformity Target:** 98%+ Operator Success Rate  

---

## 1. Problem Statement & Error Signature

When navigating to `https://sc-escd.vercel.app/escd`, attempting to **"Sign in with Google"** or submitting operator email credentials fails with an immediate or delayed gateway timeout.

### Observable Symptoms:
1. **Google OAuth Button:**  
   Navigates to `https://nevgdyfpxdaloacuutal.supabase.co/auth/v1/authorize?provider=google&redirect_to=...` and renders:
   ```json
   HTTP/1.1 504 Gateway Timeout
   {"message":"Gateway Timeout"}
   ```
2. **Email / Password Sign-in:**  
   Displays error message `sign_in_failed` or `Invalid email or password` after hanging for 10–15 seconds.
3. **Underlying Cause:**  
   The backend Supabase project (`nevgdyfpxdaloacuutal`) is on the **Free Plan** and was automatically paused after 7 days without database queries. The database compute instance is stopped while Cloudflare reverse proxies remain in DNS.

---

## 2. Instant Diagnostic Command (CLI)

Execute this PowerShell command to check the health status of all four backend microservices:

```powershell
$token = (cmdkey /list | Select-String "Supabase CLI:supabase") # Requires logged-in Supabase CLI
# Alternatively, read PAT from Windows Credential Manager or Vault
$headers = @{ "Authorization" = "Bearer $env:SUPABASE_ACCESS_TOKEN" }
Invoke-RestMethod -Uri "https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/health?services=auth&services=db&services=rest&services=storage" -Headers $headers | Format-Table -AutoSize
```

### Expected Output:
- **DORMANT / TIMEOUT STATE:**
  ```text
  name    healthy status    error
  ----    ------- ------    -----
  auth    False   UNHEALTHY Service health check failed
  db      False   UNHEALTHY Service health check failed
  rest    False   UNHEALTHY Service health check failed
  storage False   UNHEALTHY Service health check failed
  ```
- **HEALTHY STATE:** All 4 services show `healthy = True` and `status = ACTIVE_HEALTHY`.

---

## 3. Remediation & Recovery Procedure

### Automated Fix via Supabase Management API (CLI):
Execute the project restore and restart commands:

```powershell
# 1. Trigger project container restore
$headers = @{ "Authorization" = "Bearer $env:SUPABASE_ACCESS_TOKEN"; "Content-Type" = "application/json" }
Invoke-RestMethod -Uri "https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/restore" -Method Post -Headers $headers

# 2. Trigger service restart
Invoke-RestMethod -Uri "https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/restart" -Method Post -Headers $headers
```

### Manual Fallback via Web Console:
1. Open the [Supabase Dashboard](https://supabase.com/dashboard/project/nevgdyfpxdaloacuutal).
2. If paused, a banner will display: **"Project is paused due to inactivity"**.
3. Click the green **"Restore project"** button and wait 60–90 seconds for container re-provisioning.

---

## 4. Verification Gate

Execute a live probe against the Google OAuth authorization redirect endpoint:

```powershell
curl.exe -i "https://nevgdyfpxdaloacuutal.supabase.co/auth/v1/authorize?provider=google&redirect_to=https%3A%2F%2Fsc-escd.vercel.app%2Fescd"
```

### Success Signature:
```http
HTTP/1.1 302 Found
Location: https://accounts.google.com/o/oauth2/v2/auth?...
```
*(Confirms immediate 302 redirect directly into Google OAuth; zero gateway timeout).*

---

## 5. Permanent Prevention Strategy
1. **Automated Heartbeat Cron:** Configure a weekly GitHub Actions workflow or local Windows scheduled task to send a single query (`GET /rest/v1/`) to reset the 7-day inactivity counter.
2. **Supabase Pro Upgrade:** Upgrade `SC-Command-Post` to the Pro tier ($25/mo) to permanently disable compute auto-pausing.
