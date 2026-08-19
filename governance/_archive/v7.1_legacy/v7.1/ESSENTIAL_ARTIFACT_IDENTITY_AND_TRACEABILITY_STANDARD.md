# DCSE V7.1 Essential Artifact Identity and Traceability Standard

Status: IMMEDIATE CONTROLLED USE
Authority: DCS
Scope: DCSE, SC, SS, TSL, approved product and website work
Confidentiality: INTERNAL

## 1. Purpose

Prevent essential code, scripts, embedded HTML, Wix payloads, SQL, prompts, workflows, reports, and generated assets from becoming unidentifiable, unsearchable, or detached from their governing task.

This standard applies only to essential artifacts, not every temporary note or disposable output.

## 2. Essential Artifact Test

An artifact is essential when one or more conditions apply:

1. It is deployed, published, embedded, scheduled, or executed.
2. It changes product behavior, data, governance, security, or operations.
3. It is required to reproduce, repair, audit, or migrate a system.
4. It contains a reusable DCSE method, component, prompt, workflow, or model profile.
5. It supports a public claim, production-readiness finding, or promotion decision.
6. It would create material rework if lost.

## 3. Required Identity Block

Every essential text-based artifact must contain an identity block in the native comment syntax where technically possible.

Required fields:

- Artifact ID
- Title
- Canonical filename
- Product or system
- Lane
- Version
- Status
- Repository
- Canonical path
- Related issue, PR, or task
- Supabase registry key
- Created date
- Last modified date
- Owner
- Purpose
- Dependencies
- Secrets classification
- Supersedes or superseded-by reference

## 4. Canonical Artifact ID

Format:

`DCSE-{LANE}-{TYPE}-{YYYYMMDD}-{SLUG}-{NNN}`

Examples:

- `DCSE-SC-PY-20260802-GMAIL-INTELLIGENCE-001`
- `DCSE-SC-WIXHTML-20260802-SERVICE-ASSESSMENT-001`
- `DCSE-TSL-SQL-20260802-SPORTS-AVAILABILITY-001`
- `DCSE-DCSE-GOV-20260802-AGENT-ONBOARDING-001`

Type codes may include:

- GOV
- ADR
- PLAN
- PY
- JS
- TS
- SQL
- HTML
- WIXHTML
- YAML
- JSON
- PROMPT
- REPORT
- DATA
- MEDIA

## 5. Python Header Template

```python
# DCSE_ARTIFACT_ID: DCSE-SC-PY-20260802-GMAIL-INTELLIGENCE-001
# TITLE: DCSE Gmail Intelligence Report Runner
# CANONICAL_FILENAME: dcse_gmail_report.py
# PRODUCT_SYSTEM: SC Command Post
# LANE: SC
# VERSION: 0.1.0-candidate
# STATUS: CANDIDATE
# REPOSITORY: sonlyconsulting-ctrl/DCSE-Command-Post
# CANONICAL_PATH: tools/gmail/dcse_gmail_report.py
# RELATED_PR_ISSUE_TASK: PR-29 | TASK-V7_1_GMAIL_INTELLIGENCE_INTAKE
# SUPABASE_REGISTRY_KEY: DCSE_SC_GMAIL_INTELLIGENCE_RUNNER
# CREATED_DATE: 2026-08-02
# LAST_MODIFIED_DATE: 2026-08-02
# OWNER: DCS
# PURPOSE: Generate governed Gmail operational intelligence reports.
# DEPENDENCIES: Gmail OAuth, approved Supabase connector when enabled
# SECRETS_CLASSIFICATION: NO SECRETS IN SOURCE
# SUPERSEDES: NONE
```

## 6. HTML and Wix Embedded Header Template

Place immediately after `<!doctype html>` or as the first safe comment in the pasted payload:

```html
<!--
DCSE_ARTIFACT_ID: DCSE-SC-WIXHTML-20260802-SERVICE-ASSESSMENT-001
TITLE: SC Service Assessment Widget
CANONICAL_FILENAME: sc-service-assessment-widget.html
PRODUCT_SYSTEM: SC Website
LANE: SC
VERSION: 0.1.0-candidate
STATUS: CANDIDATE
REPOSITORY: sonlyconsulting-ctrl/DCSE-Command-Post
CANONICAL_PATH: apps/sc-website/wix-embeds/sc-service-assessment-widget.html
RELATED_PR_ISSUE_TASK: ISSUE-### | TASK-###
SUPABASE_REGISTRY_KEY: SC_SERVICE_ASSESSMENT_WIDGET
CREATED_DATE: 2026-08-02
LAST_MODIFIED_DATE: 2026-08-02
OWNER: DCS
PURPOSE: Interactive governed service-readiness assessment.
DEPENDENCIES: Approved APIs only
SECRETS_CLASSIFICATION: NO SECRETS IN CLIENT CODE
SUPERSEDES: NONE
-->
```

If a platform strips comments, store the same identity in an adjacent visible repository manifest and include a compact runtime constant such as `data-dcse-artifact-id`.

## 7. File Naming

Canonical filename must be descriptive and stable.

Preferred format:

`{product}_{capability}_{artifact-type}_v{major}_{minor}.{ext}`

Avoid:

- `final.py`
- `new.html`
- `code2.js`
- `latest.sql`
- pasted snippets without filenames

## 8. Registry Requirements

Every essential artifact must be registered with:

- artifact ID
- canonical path
- Git commit SHA
- checksum when material
- current status
- product and lane
- source task
- deployment or embed location
- dependencies
- supersession history
- last verification date

GitHub stores the canonical source and history. Supabase stores searchable registry metadata, operational state, and cross-system relationships.

## 9. Intake Rule for Pasted Code

When DCS supplies code without filename or provenance, the receiving agent must:

1. classify whether it is essential;
2. assign a candidate artifact ID;
3. propose or determine a canonical filename and path;
4. insert the appropriate identity header;
5. preserve the original code body;
6. register the candidate before deployment or embedding;
7. obtain required review for security, data, or production impact.

Do not deploy anonymous essential code.

## 10. Search and Recovery

Agents must be able to locate essential artifacts by any of:

- artifact ID
- filename
- product
- capability
- issue, PR, or task
- Supabase registry key
- deployment location
- Git commit SHA

## 11. Completion Gate

An essential artifact is not complete unless:

1. identity block exists;
2. canonical filename and path exist;
3. Git history exists;
4. registry record exists;
5. deployment or embed location is recorded when applicable;
6. no secrets are embedded;
7. supersession state is clear;
8. validation evidence is linked.

## 12. Immediate Application

Apply this standard immediately to:

- `dcse_gmail_report.py`
- Wix and HTML embedded applications
- Supabase migrations and SQL repair scripts
- GitHub Actions workflows
- model and agent bootstrap manifests
- production and audit reports
- reusable prompts and agent profiles
- TSL data and product scripts
