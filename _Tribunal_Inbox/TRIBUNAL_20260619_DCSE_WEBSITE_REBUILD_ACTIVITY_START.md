# Tribunal Activity Start: DCSE Website Rebuild

Task ID: TRIB-20260619-DCSE-WEBSITE-REBUILD-ACTIVITY-START
Entity: SC / DCSE
Mode: SC-Blueprint / DCSE-Report
Action Mode: ACKNOWLEDGE_ONLY
Status: New activity started, awaiting DCS selection
Promotion Status: Not promoted. Not approved for build.

## Architecture Acknowledged

The controlled packet defines a hybrid GovOS web application for the Sonly Consulting website rebuild, DCS premium proof layer, GovOS member portal, Wix CMS content layer, Wix Velo orchestration layer, and Supabase operational data layer.

Control rule: Doctrine governs. GovOS routes. Velo mediates. Wix presents. Supabase stores operational truth. Wix CMS stores public and premium content. DCS promotes.

## Boundaries

- No scaffold files created.
- No Velo utility files created.
- No schemas created.
- No Supabase proposal docs created.
- No Wix CMS proposal docs created.
- No live Wix action performed.
- No live Supabase connection performed.
- No migration performed.
- No credentials requested or exposed.
- No RAG vectorization or seeding performed.
- No GitHub action performed.
- No PS content movement performed.

## Utility Layers Identified

- auth-utils.js
- plan-utils.js
- entitlement-utils.js
- content-gate-utils.js
- cms-adapter.js
- supabase-client.server.js
- supabase-repository.js
- dashboard-read-model.js
- intake-utils.js
- govos-router.js
- audit-log-utils.js
- media-manifest-utils.js
- embed-registry-utils.js
- performance-budget-utils.js
- release-gate-utils.js
- firewall-utils.js
- api-client-utils.js
- error-utils.js
- member-dashboard.web.js
- govos-intake.web.js
- content-access.web.js
- http-functions.js

## Risk Flags

- Secrets and service role keys must remain backend-only and never enter frontend code.
- Supabase cannot become marketing CMS and Wix CMS cannot become operational truth.
- Dashboard payloads must be compact and backend mediated.
- Heavy media and embedded HTML require registry and performance budget controls.
- PS firewall remains active across SC, SS, DCS, TI, member, premium, public website, and RAG flows.
- Candidate records must not be vectorized or treated as approved knowledge.

## DCS Selection Requested

Option 1: ACKNOWLEDGE ONLY
Option 2: CREATE DOCUMENTATION STUBS ONLY
Option 3: CREATE UTILITY LAYER STUBS ONLY
Option 4: CREATE SCHEMAS ONLY
Option 5: CREATE SUPABASE PROPOSAL DOCS ONLY
Option 6: CREATE WIX CMS PROPOSAL DOCS ONLY
Option 7: CREATE TEST CHECKLISTS ONLY
Option 8: CREATE FULL LOCAL SCAFFOLD
Option 9: REVISE PLAN BEFORE ANY CREATION

Recommended next selection: Option 2 if DCS wants a low-risk documentation start, or Option 9 if DCS wants revisions before any creation.

## Pending DCS Items

- Select the next action option.
- Confirm the approved local root if any creation is selected.
- Confirm whether AG, QwenCoder, Claude-Code, or Claude-CoWork should review this packet before scaffold creation.
- Confirm whether this website rebuild activity stays separate from SC-Gov-OS RAG CTO review records except for shared governance references.
