# MILESTONE: ESCD-MVP-0.7.2 Golden Baseline & Database Recovery Runbook

**Milestone ID:** `DCSE-ESCD-MILESTONE-20260920-GOLDEN-BASELINE`  
**Recorded:** 2026-09-20 07:07 UTC by Antigravity at DCS direction ("Its working whoop whoop. record steps and save and memory for if a next time... This is a good working version to revert to going forward")  
**Lane:** DCSE / ESCD  
**Status:** PRODUCTION VERIFIED & GOVERNED BASELINE LOCKED  
**Golden Commit:** `1b9a101`  
**Golden Git Tags:** `baseline/escd-mvp-0.7.2-golden-working-20260920`, `v0.7.2-escd-golden`  
**Production Deployment:** `dpl_DDjdD7jiK2jhzh74U4viF1U39w4g`  
**Production URL:** [https://sc-escd.vercel.app](https://sc-escd.vercel.app)  

---

## 1. What the Milestone Covers

- **Verification of Live Production:**
  - Google OAuth login works cleanly end-to-end with token persistence and zero redirect looping.
  - Multi-model provider selection catalog is enabled (OpenAI ChatGPT, Anthropic Claude, Alibaba Qwen, and Google Gemini).
  - Built-in circuit breaker (`_SUPABASE_RPC_FAIL_UNTIL`) protects against backend database stalls.
  - Fail-fast timeouts (3s/4s/5s) guarantee requests respond under Vercel edge runtime limits ($<3.5$s maximum degraded time vs 72s previously).
  - Clean error surfacing with structured HTTP 503 instead of 500 internal errors.
- **Operational Memory & Runbook Established:**
  - Complete recovery procedures documented in `apps/escd/docs/ESCD_DATABASE_IO_EXHAUSTION_AND_RECOVERY_RUNBOOK.md`.
  - Co-registered in canonical convergence registry as `CANON-162` (`KNOWLEDGE`).
- **Cryptographic & Git Reversion Anchor:**
  - Annotated tags pushed to GitHub `origin`.
  - Fast single-command rollback instructions for both Git and Vercel CLI.

---

## 2. Evidence & Verification

- **Live Production URL:** `https://sc-escd.vercel.app` confirmed fully operational by DCS operator.
- **Automated Test Suite:** 71 passed, 0 failed (`apps/escd/tests`).
- **Git Push Verification:**
  - Push of `baseline/escd-mvp-0.7.2-golden-working-20260920` and `v0.7.2-escd-golden` completed to `origin`.
  - Pre-push regression gate passed 11/11 tests.
- **Supabase Metrics Post-Reboot:**
  - Disk I/O exhaustion cleared after instance restart.
  - Diagnostic queries prepared for ongoing cron maintenance (`cron.job_run_details`).

---

## 3. Revert Reference

- **Git Checkout:**
  ```bash
  git checkout baseline/escd-mvp-0.7.2-golden-working-20260920
  ```
- **Vercel Rollback:**
  ```bash
  npx vercel alias set dpl_DDjdD7jiK2jhzh74U4viF1U39w4g sc-escd.vercel.app
  ```

---

## 4. Open Operational Notes
- Monitor Supabase database metrics on `nevgdyfpxdaloacuutal`. If Disk I/O bursts continue under heavy traffic, execute the `TRUNCATE TABLE cron.job_run_details;` maintenance script or scale compute to Micro (1 GB RAM).
