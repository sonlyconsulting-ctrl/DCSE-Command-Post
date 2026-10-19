# TRIBUNAL SESSION REPORT: ESCD AUTH GATEWAY TIMEOUT RESOLUTION

**Message ID:** `TRIB-20261019-ESCD-GATEWAY-TIMEOUT-RESOLVED`  
**Timestamp:** `2026-10-19T16:33:00.000Z`  
**Task ID:** `DCSE-ESCD-GATEWAY-TIMEOUT-20261019-001`  
**Lane:** `DCSE // ESCD // TRIBUNAL`  
**Originator / Role:** Antigravity (`agy`) — Sovereign Auditor & Gatekeeper  
**Status:** `COMPLETE`  

---

## 1. Incident Research & Root Cause Analysis

When attempting operator authentication on `https://sc-escd.vercel.app/escd`, both **Google OAuth** and **Email/Password** logins resulted in `504 Gateway Timeout` (`{"message":"Gateway Timeout"}`).

### Empirical Diagnostic Findings:
1. **Google OAuth Link:**  
   `https://nevgdyfpxdaloacuutal.supabase.co/auth/v1/authorize?provider=google&redirect_to=https%3A%2F%2Fsc-escd.vercel.app%2Fescd`  
   Direct requests to this URL timed out after 5–10 seconds with Cloudflare `HTTP/1.1 504 Gateway Timeout`.
2. **Email / Password Flow:**  
   `POST https://sc-escd.vercel.app/api/mvp/login` calls `url + "/auth/v1/token?grant_type=password"` on Supabase. Because the backend GoTrue / PostgreSQL instance was unreachable, the Python HTTP client encountered connection timeouts and returned `sign_in_failed`.
3. **Supabase Service Health Audit:**  
   Querying the Supabase Management API (`GET https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/health`) revealed that all four platform services were down:
   ```json
   [
     {"name": "auth", "healthy": false, "status": "UNHEALTHY"},
     {"name": "db", "healthy": false, "status": "UNHEALTHY"},
     {"name": "rest", "healthy": false, "status": "UNHEALTHY"},
     {"name": "storage", "healthy": false, "status": "UNHEALTHY"}
   ]
   ```
   Under the Free Plan in organization `hwnilrdznitvqrwvdffz`, the underlying compute/database instance had become paused/dormant, leaving Cloudflare/Kong reverse proxies unable to reach the upstream services.

---

## 2. Remediation Executed

1. Triggered an immediate lifecycle restore and container restart via the Supabase Management API:
   - `POST https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/restart`
   - `POST https://api.supabase.com/v1/projects/nevgdyfpxdaloacuutal/restore`
2. Monitored service provisioning until all components achieved healthy state.

---

## 3. Verification & Live Operational Confirmation

1. **Supabase Platform Health:**  
   All four services are now confirmed active and healthy:
   - `auth`: `ACTIVE_HEALTHY` (GoTrue `v2.197.0`)
   - `db`: `ACTIVE_HEALTHY`
   - `rest`: `ACTIVE_HEALTHY` (PostgREST schema `public,graphql_public,dcse_cp,v7_worker,v7_bootstrap`)
   - `storage`: `ACTIVE_HEALTHY`
2. **Google OAuth Endpoint:**  
   `curl.exe -i "https://nevgdyfpxdaloacuutal.supabase.co/auth/v1/authorize?provider=google&redirect_to=https%3A%2F%2Fsc-escd.vercel.app%2Fescd"`  
   **Result:** `HTTP/1.1 302 Found` with redirect `Location: https://accounts.google.com/o/oauth2/v2/auth?...` (Zero timeout; immediate Google redirect).
3. **Email / Password Endpoint:**  
   `POST https://sc-escd.vercel.app/api/mvp/login` now connects and evaluates against Supabase GoTrue in <1s.
4. **Web Frontend:**  
   [`https://sc-escd.vercel.app/escd`](https://sc-escd.vercel.app/escd) loads cleanly (`HTTP 200`) and dispatches authentication requests without gateway timeouts.
