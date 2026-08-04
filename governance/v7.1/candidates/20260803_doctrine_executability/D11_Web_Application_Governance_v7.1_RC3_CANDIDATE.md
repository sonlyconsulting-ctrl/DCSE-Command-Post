# DCSE Doctrine D11: Web and Application Governance v7.1 RC3 Candidate

**Document ID:** DCSE-D11-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to entity, product, environment, and data classification  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D11_HTML_Wix_App.md`  
**Source SHA-256:** `148841178e07447028605b8630373f96ab6bd82e7840679e114de43481b8c240`  
**Product dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D20_Product_Assembly_Methodology_v7.1_RC3_CANDIDATE.md`  
**Product dependency SHA-256:** `2773cb8009e086f96df69cba5b00104ddd1efc4f34045e61eedca7ed9854f7a3`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until exact DCS promotion and D22 reconciliation.  

## 1. Purpose

D11 governs websites, web applications, mobile web experiences, dashboards, portals, embedded modules, progressive applications, provider-hosted pages, and related frontend and backend integration.

The doctrine is platform-neutral. Wix, Vercel, static HTML, React, Next.js, hosted builders, local applications, and future platforms use adapters to the same product, security, accessibility, evidence, deployment, and operational contracts.

## 2. Governing principles

1. User goals and acceptance criteria precede framework choice.
2. Authentication, authorization, database grants, RLS, and application checks are distinct.
3. Secrets and privileged credentials remain server-side or in approved secret stores.
4. Accessibility is tested through structure, keyboard, screen-reader, contrast, motion, error, and recovery behavior.
5. Responsive behavior follows content and supported devices rather than fixed universal breakpoints.
6. Failure, empty, loading, offline, expired-session, and recovery states are designed explicitly.
7. Provider-specific integration belongs in an adapter.
8. Preview success does not prove production readiness.
9. Synthetic or de-identified data is used for testing unless protected data is expressly required and authorized.
10. Deployment, monitoring, rollback, support, and retirement are part of the application.

## 3. Application declaration

```yaml
application_profile:
  application_id: ""
  product_id: ""
  entity: ""
  audience: ""
  intended_use: ""
  application_class: "SITE | WEB_APP | DASHBOARD | PORTAL | EMBED | PWA | HYBRID"
  environments: []
  routes: []
  user_roles: []
  data_system_refs: []
  auth_profile_ref: ""
  integration_refs: []
  brand_profile_ref: ""
  accessibility_baseline_ref: ""
  supported_devices_and_browsers: []
  deployment_profile_ref: ""
  monitoring_profile_ref: ""
  support_owner: ""
  retirement_plan_ref: ""
```

## 4. Architecture and provider adapters

Core application requirements must not assume Wix, one JavaScript framework, one hosting provider, one database client, or one directory layout.

```yaml
platform_adapter:
  adapter_id: ""
  provider: ""
  version: ""
  supported_features: []
  unsupported_features: []
  authentication_behavior: ""
  secret_handling: ""
  embed_behavior: ""
  deployment_behavior: ""
  preview_behavior: ""
  rollback_behavior: ""
  observability_behavior: ""
  exit_or_migration_path: ""
```

Provider limitations must be visible in architecture and acceptance plans.

## 5. State and interaction model

Every material interface defines applicable states:

- initial;
- loading;
- partial;
- empty;
- ready;
- editing;
- validating;
- submitting;
- success;
- warning;
- error;
- offline or disconnected;
- session expired;
- unauthorized;
- forbidden;
- conflict;
- recovery;
- archived or retired.

State changes are observable, accessible, and accurate. A silent write failure, endless spinner, ambiguous empty screen, or success message before persistence verification fails acceptance.

## 6. Authentication and authorization

- Authentication establishes identity; authorization decides permitted operations.
- Client UI restrictions do not replace server or database enforcement.
- Session creation, refresh, expiry, logout, recovery, verification, and multi-factor states are tested where applicable.
- Redirect targets and return URLs are allowlisted.
- Protected routes verify current identity and permissions server-side where the architecture requires it.
- Privileged actions require explicit server-side checks and audited execution.
- D15 controls database grants, RLS, functions, RPCs, Storage, and service-role use.
- Anonymous and authenticated roles receive only the minimum required access.
- User-controlled metadata is not used as an authorization source.

## 7. Data and privacy

- Collect only data required for declared product purpose.
- Explain consent, retention, export, correction, and deletion where applicable.
- Prevent protected or confidential data from entering logs, analytics, URLs, client storage, source maps, prompts, or public repositories.
- Avoid long-lived sensitive data in browser storage.
- Use server-side provider integrations for private API keys.
- Test cross-user, cross-role, cross-product, and cross-lane denial.
- Use environment-specific data and credentials.
- Analytics and session replay require privacy review, masking, retention, and opt-out behavior where applicable.

## 8. Application security

Applicable controls include:

- output encoding and safe rendering;
- input validation on trust boundaries;
- cross-site scripting prevention;
- request forgery protection where architecture requires it;
- content security policy;
- secure cookies and transport;
- dependency and supply-chain review;
- rate limiting and abuse controls;
- file type, size, malware, and storage validation;
- origin validation for cross-window messages;
- schema validation for messages and APIs;
- redirect and URL validation;
- error redaction;
- secret and credential scanning;
- least-privilege backend identities.

Security headers and policies are verified in the deployed environment, not only present in source configuration.

## 9. Embedded modules and cross-window communication

Embeds require an adapter-specific threat model. Controls include:

- minimum sandbox capabilities;
- explicit allowed origins;
- message type and schema allowlist;
- sender and receiver validation;
- replay or duplicate handling;
- size and resize constraints;
- focus and keyboard behavior;
- accessible title and fallback;
- privacy and tracking boundary;
- failure and timeout behavior.

`allow-same-origin` combined with scripts is not declared universally safe. The required sandbox tokens depend on origin, content ownership, and capability.

## 10. Semantic structure and accessibility

Applicable acceptance includes:

- correct language and page title;
- semantic landmarks and heading order;
- keyboard access and logical focus order;
- visible focus;
- accessible names, roles, descriptions, and states;
- labels and instructions for forms;
- actionable validation and error recovery;
- sufficient contrast and non-color cues;
- zoom, reflow, text spacing, and orientation support;
- reduced motion and animation controls;
- captions, transcripts, and media alternatives;
- meaningful link and button text;
- skip navigation where applicable;
- status announcements without disruptive focus changes;
- timeout and session-expiry warning where applicable.

The approved accessibility baseline and exceptions are versioned. Automated scans supplement, but do not replace, keyboard, screen-reader, zoom, motion, and real-user testing required by the acceptance plan.

## 11. Responsive and resilient layout

Layouts use intrinsic sizing, flexible grids, content-driven constraints, container or media queries where appropriate, and tested overflow behavior.

Support is declared by device, viewport, browser, input method, zoom, orientation, and network condition. Fixed pixels are permitted where semantically appropriate, but main layouts must not depend on one fixed viewport.

## 12. Design system and brand integration

Applications consume versioned D09 semantic tokens and D08 voice profiles. Code must not duplicate an obsolete palette or hardcode one entity's identity across unrelated products.

Components define default, hover, active, focus, disabled, loading, success, warning, error, empty, and selected states as applicable.

Internal candidate or governance labels are removed from public builds while remaining available in governed build evidence.

## 13. Performance and reliability

Acceptance plans define applicable budgets for:

- initial and route load;
- interaction responsiveness;
- layout stability;
- image, font, media, and script weight;
- cache and offline behavior;
- API latency and timeout;
- concurrency and retry;
- degraded dependency behavior;
- resource use on supported devices.

Performance is measured in representative environments. A high-end development machine is not the only test fixture.

## 14. Forms, files, and user content

- Validate on client for usability and server for trust.
- Preserve user input across correctable errors when safe.
- Prevent duplicate submission through idempotency or explicit handling.
- Show progress and final persistence state accurately.
- Validate upload type, content, size, authorization, destination, and retention.
- Sanitize or safely render user content.
- Provide correction, deletion, and recovery behavior where required.

## 15. Testing matrix

Required classes are selected by application risk:

- unit and component;
- integration and contract;
- end-to-end user journey;
- authorization matrix;
- accessibility;
- responsive and browser compatibility;
- security and dependency;
- performance and resilience;
- visual regression;
- rollback and recovery;
- analytics and privacy;
- deployment smoke and monitoring.

Tests must exercise real control paths. Mocked success alone cannot prove production integration.

## 16. Deployment and operations

```yaml
deployment_receipt:
  receipt_id: ""
  application_ref: ""
  environment: ""
  source_commit: ""
  build_ref: ""
  configuration_ref: ""
  migration_refs: []
  deployment_ref: ""
  smoke_results: []
  accessibility_results: []
  security_results: []
  monitoring_results: []
  rollback_result: ""
  known_findings: []
  authority_ref: ""
  disposition: "PASS | PASS_WITH_CORRECTIONS | FAIL | INSUFFICIENT_EVIDENCE"
```

Preview, staging, and production are distinct. Promotion and deployment require applicable D05 authority. D22 reconciles source, build, deployment, and runtime identities.

## 17. Failure and recovery

| Condition | Required behavior |
| --- | --- |
| Backend unavailable | Preserve safe input, show accurate state, retry or provide recovery. |
| Session expires | Protect unsaved work where safe and provide accessible reauthentication. |
| Write result uncertain | Reconcile before retry or success claim. |
| Dependency degrades | Use declared fallback or isolate affected feature. |
| Deployment fails | Preserve last verified release and execute rollback or forward recovery. |
| D11 unavailable | Isolate application-dependent release and continue safe source work. |

## 18. Runtime interfaces

```text
resolve_application_profile(product, environment) -> ApplicationProfile
resolve_platform_adapter(profile, provider) -> PlatformAdapter
compile_application_acceptance(profile, doctrines) -> TestMatrix
validate_application(build, matrix) -> ApplicationValidation
deploy_application(build, environment, authority) -> DeploymentReceipt
reconcile_application(source, build, deployment) -> ReconciliationReceipt
```

## 19. Mechanical acceptance tests

| Test | Scenario | Required result |
| --- | --- | --- |
| D11-001 | Hosting provider changes | Core requirements remain valid through a new adapter. |
| D11-002 | Browser contains private provider key | Security gate fails. |
| D11-003 | UI hides button but backend permits action | Authorization test fails. |
| D11-004 | Cross-user read is attempted | Server and data controls deny it. |
| D11-005 | Write fails but success banner appears | State test fails. |
| D11-006 | Empty result is valid | Accessible empty state appears. |
| D11-007 | Loading never terminates | Timeout and recovery test fails. |
| D11-008 | Session expires during form entry | Safe recovery behavior is tested. |
| D11-009 | Embed accepts any origin | Security test fails. |
| D11-010 | Embed sandbox has unnecessary capability | Least-capability test fails. |
| D11-011 | Keyboard cannot reach control | Accessibility test fails. |
| D11-012 | Automated scan passes but screen-reader path fails | Accessibility disposition fails. |
| D11-013 | Layout works only at fixed width | Responsive test fails. |
| D11-014 | Animation ignores reduced motion | Accessibility test fails. |
| D11-015 | Public build exposes candidate label | Release test fails. |
| D11-016 | Duplicate form submission occurs | Idempotency or duplicate handling is required. |
| D11-017 | File extension is safe but content is not | Upload is rejected or quarantined. |
| D11-018 | Preview passes without production configuration check | Production readiness remains unproven. |
| D11-019 | Deployment succeeds but monitoring is absent | Operational readiness remains incomplete. |
| D11-020 | Rollback is declared but untested | Deployment PASS is unavailable. |
| D11-021 | Analytics captures sensitive fields | Privacy test fails. |
| D11-022 | Dependency fails | Declared fallback or affected-feature isolation occurs. |
| D11-023 | D11 is unavailable | Application-dependent release is isolated. |
| D11-024 | Complete matrix passes | Receipt may return PASS without promotion. |

## 20. Source correction record

| Source condition | RC3 correction |
| --- | --- |
| HTML and Wix treated as doctrine core | Platform-neutral application contract and adapters. |
| Fixed sandbox tokens | Threat-model and least-capability embed controls. |
| Fixed breakpoints and fonts | Declared support matrix and D09 tokens. |
| RLS described as complete browser security | Distinct auth, authorization, grants, RLS, and app controls. |
| Limited accessibility guidance | Full interaction, content, recovery, media, and assistive testing. |
| No deployment lifecycle | Environment, monitoring, rollback, support, and retirement controls. |
| Blanket halt | Application-dependent affected-action isolation. |

## 21. Candidate status

This candidate does not replace active D11 or authorize build, data access, deployment, public release, or promotion until exact DCS promotion and D22 reconciliation.
