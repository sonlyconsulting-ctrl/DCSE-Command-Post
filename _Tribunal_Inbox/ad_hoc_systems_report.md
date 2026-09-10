# DCSE-CP RESPONSE PACKET — Ad-Hoc Systems Diagnostics Report
**Document ID:** DCSE-CP/DIAGNOSTICS/20260624-005
**Target:** `https://cp.sonlyconsulting.com/pm`

## 1. System Identification (Vercel / Next.js)
You were correct. The system powering `cp.sonlyconsulting.com/pm` is a **Next.js** application deployed to Vercel. 
- **Source Code Location:** I located the exact repository on your machine at:
  `C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\DCSE_ASSET_PORTAL_APP\apps\web`

## 2. Root Cause Analysis: Why it's not showing results
I performed a deep inspection of the Next.js frontend code (`src/app/pm/page.tsx`) and the Supabase backend configuration. There are two overlapping issues causing the blank results:

### A. The Supabase RLS (Row-Level Security) Block
When the `/pm` page loads, it asks the Supabase database for records from the `dcse_plan_inbox` table (specifically where `record_type = 'priority_module'`). 
However, Supabase is enforcing strict security. I checked your database administration scripts (e.g., `apply_public_policies.ts`), and while they grant read access to tables like `pm_projects` and `pm_tasks`, **they completely missed the `dcse_plan_inbox` table**. 
Because there is no policy allowing the frontend to read that specific table, Supabase silently rejects the request and returns `0` results to the screen.

### B. Missing Seed Data
I found a script in the repository named `seed_pms.ts`. This script was specifically designed to inject the initial Priority Modules (like CTJ, TSL, and the DCS Employment Module) into the `dcse_plan_inbox` table. Because of the database lockdown (and potentially not running the script post-deployment), the table itself might actually be empty in your production database.

## 3. The Fix Implementation Plan
To bring `cp.sonlyconsulting.com/pm` back online and displaying results, we need to execute the following fixes:

1. **Database Policy Update:** 
   I will write a Prisma/SQL migration script to apply a `DCS Public Select` policy to the `dcse_plan_inbox` table, instructing Supabase to allow the frontend to read the Priority Modules.
2. **Execute Seed Script:** 
   I will run the `seed_pms.ts` script locally using your `NEXT_PUBLIC_SUPABASE_URL` and keys to populate the database with the core modules.
3. **Verify Frontend:** 
   Once the database allows the read and has data, the live Vercel site at `cp.sonlyconsulting.com/pm` will instantly populate without needing to redeploy the Next.js code.

> [!IMPORTANT]
> **Approval Required**
> Do you approve this fix plan? If so, I will generate the policy script and push the fix to your database immediately.
