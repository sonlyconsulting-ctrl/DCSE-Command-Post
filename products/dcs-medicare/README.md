# DCS Medicare Decision Center · Standalone Product

Task: DCS-MEDICARE-APP-20261019-01
Entity/lane: DCS Private Personal Research (PPR)
Product ID: dcs_medicare
Version: 1.1
Status: PROTECTED_HOSTED / SOURCE-REPO-HANDOFF-PENDING
Source HTML SHA-256: a79ae5bdcc9b493b3950922524b43fc1578e26a6e6cda9dcf54fe8bf14f4c26e

## Independent runtime
Vercel project: dcs-medicare-decision-center
Project ID: prj_iy77wadMTTjcwx2aiDCyowPZlqos
Protected URL: https://dcs-medicare-decision-center.vercel.app
Deployment ID: dpl_2TKzTfsCR4DYeeMXY3iHJcBH7SP2
Protection: Vercel Authentication enabled for all deployment types.
The current hosted file is a static, session-only browser application. There is no backend, user record storage, live Medicare API integration, or individual user login feature.

## Source chain and release limitation
Source of this deployment: conversation artifact DCS_Medicare_Decision_Center_Preview.html (self-contained HTML), also bundled in DCS_Medicare_Decision_Center_Benefits_v1_1_Package.zip.
The GitHub connector blocked uploading the full HTML source to this repository. The exact file bytes are therefore NOT versioned in GitHub. Do not claim this manifest is a source commit or a complete rollback repository.
A dedicated private GitHub repository with this source and test harness is a mandatory follow-up prior to long-term maintenance; the available GitHub connector does not expose repository creation.

## Separation and access
ESCD is a launcher. The Medicare application is not an ESCD runtime module, does not access ESCD databases or credentials, and must not be framed or proxied through a public route.
The ESCD catalog stores only product metadata and protected app URL.
Personal Medicare numbers, benefit letters, medical data, passwords and API credentials must not enter product metadata, public URLs, or Git source.

## Verification
15/15 deterministic calculation tests passed 2026-10-21 in isolated release-audit execution.
15/15 Chromium browser tests passed 2026-10-21 against the source HTML (including 375px mobile).
Vercel project/deployment readiness and SSO all readback verified.
Authenticated live end-to-end browser click-through was NOT performed in this session; external read is blocked by protection and direct browser navigation tooling is unavailable.
Official Medicare plan details and 2027 data remain source-verification gates before recommending a plan.

## Next gates
- DCS opens protected URL and confirms functional experience.
- Create distinct private repository with source, tests and rollback tag; wire into the Vercel project.
- Implement app-local authentication/persistence only if storing personal data for broader 65+ audiences.
- Validate accessibility targets, user isolation, benefits sourcing, currency and real service eligibility.

## DCS review status and private repository requirement (2026-10-21)

DCS confirmed the protected standalone application's production availability and ESCD product placement. Product disposition is `PENDING_REVIEW`; do not interpret production deployment as final product approval.

GitHub repository inventory checked 2026-10-21: no standalone Medicare source repository was present among the 22 repositories returned for `sonlyconsulting-ctrl`. This existing `DCSE-Command-Post` repository is **PUBLIC** and contains only catalog metadata and this deployment/source manifest, not the Medicare app source or beneficiary records. Do **not** change the visibility of the entire Command Post repository merely to protect the Medicare product.

Required separate repository: `sonlyconsulting-ctrl/DCS-Medicare-Decision-Center`, visibility **PRIVATE**, then attach its contents to the existing Vercel project without changing Vercel Authentication for all deployment types. Repo creation / visibility management is not available through this session's GitHub actions; [issue #199](https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post/issues/199) tracks completion. Do not mark this control satisfied without a live GitHub visibility readback.

Private-source handoff generated for DCS in the conversation: `DCS_Medicare_Private_GitHub_Repo_Ready.zip`. It contains only the reviewed static app source, documentation, tests and a GitHub workflow; original compiled HTML SHA-256 remains `a79ae5bdcc9b493b3950922524b43fc1578e26a6e6cda9dcf54fe8bf14f4c26e`. The attached source package is **not** committed to the public Command Post repository.
