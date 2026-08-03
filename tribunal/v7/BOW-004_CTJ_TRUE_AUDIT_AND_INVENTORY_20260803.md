# BOW-004 Critical Thinker's Journey True Audit and Inventory

**Task:** `V7_1_BOW_004_CTJ_TRUE_AUDIT_INVENTORY`  
**Purpose:** Correct the BOW-002 scope substitution and complete the CTJ-specific audit  
**Disposition:** `APPROVE_WITH_FINDINGS` for audit completion  
**Product readiness:** `NON_PASS`  
**Lane:** SS  

## Executive determination

The CTJ audit is complete. CTJ exists across six GitHub repositories, with two materially different product generations:

1. Static single-file HTML editions for the full journey and Parts 1 through 3.
2. A newer React/Vite MVP that combines three modules, local journal storage, accessibility settings, voice input, heuristic guidance, PDF/text export, privacy content, and session reset.

The product has meaningful content and a viable offline-first prototype. It is not production-ready. The current generation lacks a canonical repository decision, automated tests, a lockfile, lint/type-check scripts, governed deployment configuration, durable account-based storage, entitlement and commerce controls, recovery/sync behavior, observability, and verified security/accessibility acceptance. A build receipt was not available from GitHub, and no claim of a passing build is made.

## Evidence boundary

### Verified

- Repository metadata, branches, commit history, changed-file inventories, and current source files were read through authenticated GitHub access.
- SC-Command-Post Supabase asset registry contains no CTJ-labelled rows.
- SC-Command-Post Supabase contains no CTJ-labelled application tables.
- BOW-004 completion-contract enforcement was applied and negatively tested.

### Not verified

- Local Windows CTJ copies outside GitHub.
- Any deployment not referenced by repository evidence.
- Current browser execution, npm installation, production build, accessibility automation, or malware/dependency scan.
- Storefront, payment processor, email delivery, analytics, or customer records.

## 1. Canonical inventory

### Repository inventory

| Repository | Visibility | Branch | Latest verified commit | Material content | Classification |
|---|---|---|---|---|---|
| `SS-CTJ-Full` | Public | `main` | `b620db24d64fef66e6229e24ef71efc51508c208` | Single `index.html` full edition | RETAIN as legacy reference |
| `SS-CTJ-Part1` | Public | `main` | `bed93cd31700b7ed3fe8e1c11bff2125c5507378` | Single `index.html`, Part 1, clarity and confidence | RETAIN as source content |
| `SS-CTJ-Part2` | Public | `main` | `d4aef702511bd0f14535c6b968c1b5284505c45b` | Single `index.html`, Part 2 | RETAIN as source content |
| `SS-CTJ-Part-3` | Public | `main` | `fb02d83998560aee4e6ddbc9c925ff5d391e2169` | README-only repository | ARCHIVE after reconciliation |
| `SS-CTJ-Part3` | Public | `main` | `dee5736f51d298be040ab998c46a14f0d719843f` | Single `index.html`, Part 3 | RETAIN as source content |
| `CTJ-MVP-11252025` | Private | `main` | `a43fbcd4575108ecb6057f226403ad580ec1a6ac` | React 19, TypeScript, Vite application | REFACTOR into canonical product |

All six repositories expose only a `main` branch through the connected GitHub surface.

### Current MVP source inventory

Verified source includes:

- `App.tsx`
- `index.tsx`
- `constants.ts`
- `types.ts`
- `context/AppContext.tsx`
- `components/AIAssist.tsx`
- `components/CompletionView.tsx`
- `components/ExportView.tsx`
- `components/JournalView.tsx`
- `components/Layout.tsx`
- `components/PrivacyPolicyView.tsx`
- `components/UserGuideView.tsx`
- `components/WarmupView.tsx`
- `components/WelcomeView.tsx`
- `package.json`
- `vite.config.ts`
- `tsconfig.json`
- `metadata.json`
- `README.md`

Current package dependencies are React 19.2, React DOM 19.2, Lucide React, canvas-confetti, and jsPDF. Development dependencies include TypeScript 5.8, Vite 6.2, and the Vite React plugin.

### Content inventory

The React MVP presents three modules:

- Module 1, Foundation: Scout Mindset, Map versus Territory, First Principles, Inversion, Circle of Competence, and checkpoint.
- Module 2, Exploration: Divergent Thinking, Five Whys, Systems Thinking, Steelmanning, Second-Order Thinking, and checkpoint.
- Module 3, Meaning: Values Audit, Eulogy Test, Energy Audit, Essentialism, Blueprint, and final reflection.

The current MVP contains 18 prompt/checkpoint records and three bias-quiz questions. The static Part 1 artifact alone contains a much richer long-form journal structure. Content parity between the legacy HTML editions and the React MVP is not established.

## 2. Dependency graph

1. `index.html` and `index.tsx` bootstrap React.
2. `App.tsx` routes between welcome, warmup, journal, export, completion, guide, and privacy views.
3. `AppContext.tsx` owns view state, accessibility settings, prompt position, journal entries, and local persistence.
4. `constants.ts` owns modules, prompts, quiz content, heuristics, copy, version, and storage keys.
5. `JournalView.tsx` depends on browser speech recognition, prompt content, local journal state, and `AIAssist`.
6. `AIAssist.tsx` performs local string-based heuristic analysis. It does not use a model API in the verified current file.
7. `ExportView.tsx` depends on jsPDF and browser Blob/download APIs.
8. `CompletionView.tsx` resets local session data and uses canvas-confetti.
9. Vite provides the build and development server.
10. Google Fonts and Tailwind CDN references in HTML create external runtime dependencies.
11. No verified backend, authentication, Supabase client, commerce provider, analytics provider, or remote content service exists in the current MVP.

## 3. Gap register

| Gap | Severity | Verified basis |
|---|---|---|
| No single canonical CTJ repository | High | Six repositories contain overlapping full/part/MVP representations |
| CTJ absent from enterprise asset registry | High | No CTJ-labelled `dcse_asset_registry` rows |
| No CTJ database/application registry | High | No CTJ-labelled live tables |
| No automated test suite | High | No test script or verified test files |
| No lint or explicit type-check script | Medium | Package scripts expose only dev, build, preview |
| No verified lockfile | High | Changed-file inventory and root source reads show none |
| No CI workflow or deployment configuration verified | High | No evidence from inspected repository history |
| README and runtime design disagree about Gemini | High | README requires a Gemini key; verified AIAssist is local heuristics |
| Vite injects Gemini key into client definitions | Critical if used | `vite.config.ts` defines client-accessible API-key constants |
| LocalStorage-only journal | High | No account sync, backup, multi-device continuity, or server recovery |
| Settings hydration toggles rather than sets values | Medium | Saved-state restoration dispatches toggle actions |
| Text scale is not persisted in reducer | Medium | `SET_TEXT_SCALE` changes memory only |
| Speech-recognition support is browser-specific | Medium | WebKit/SpeechRecognition dependency |
| Content parity is unverified | High | Legacy HTML is materially richer than 18-prompt MVP |
| External CDN/font dependencies lack offline/failure controls | Medium | HTML references external Tailwind/Google Fonts |
| No commercial lifecycle | High | No entitlements, billing, fulfillment, cancellation, or support evidence |
| No production privacy/data-retention verification | High | Local journal data and exports need explicit privacy behavior |

## 4. Technical-debt register

| Debt | Category | Required correction |
|---|---|---|
| Repository fragmentation | Architecture | Select one canonical repo and archive/supersede duplicates |
| Content duplication and drift | Product/content | Build a versioned content manifest and parity matrix |
| API-key configuration in client build | Security | Remove client secret injection; use server mediation if AI is added |
| Placeholder AI terminology | Product integrity | Label current feature heuristic guidance, not model AI |
| Toggle-based settings restoration | State correctness | Add a set-settings hydration action and schema validation |
| Incomplete settings persistence | State correctness | Persist and migrate text scale |
| LocalStorage schema without versioning | Data | Add explicit storage schema version, migration, export, and recovery |
| Missing tests and CI | Quality | Add unit, component, accessibility, build, and E2E workflows |
| Unpinned dependency resolution | Supply chain | Commit a lockfile and automate dependency review |
| CDN runtime dependency | Deployment | Bundle production CSS/fonts or document resilient fallback |
| No observability | Operations | Add privacy-safe error and release monitoring |
| No product registry entries | Governance | Register canonical code, content, build, deployment, and doctrine assets |

## 5. Remediation backlog

### P0, before any public production release

1. Select `CTJ-MVP-11252025` or a new governed successor as the canonical repository.
2. Remove Gemini/API-key injection from the browser build.
3. Reconcile all Part 1, Part 2, Part 3, and Full content into a versioned content manifest.
4. Add a lockfile, secret scan, dependency audit, lint, type-check, unit tests, production build, and accessibility test.
5. Define privacy, retention, export, deletion, backup, and recovery behavior for journal entries.
6. Register canonical CTJ assets in `dcse_asset_registry`.

### P1, product integrity

7. Correct settings hydration and persist text scale.
8. Add storage schema versioning and migration tests.
9. Add browser fallback for speech recognition.
10. Verify PDF and text export for long entries, Unicode, page breaks, and mobile browsers.
11. Add content-completeness and duplicate-prompt tests.
12. Add responsive, keyboard, focus, reduced-motion, contrast, and screen-reader acceptance.

### P2, commercial readiness

13. Define free, part, full-series, bundle, and future audio entitlements.
14. Add purchase, fulfillment, cancellation, refund, and customer-support flows.
15. Add privacy-safe analytics and conversion events.
16. Add release versioning, deployment rollback, monitoring, and incident procedures.
17. Archive or clearly mark superseded repositories after canonical import and hash reconciliation.

## 6. Confidence report

| Surface | Confidence | Basis |
|---|---:|---|
| Repository identity and branch inventory | 0.99 | Authenticated GitHub metadata |
| Commit and changed-file inventory | 0.98 | Authenticated commit reads |
| Current MVP architecture | 0.95 | Direct source reads of key application files |
| Static-edition content identity | 0.92 | Commit diffs and current single-file structure |
| Buildability | 0.45 | Source appears structurally buildable, but install/build was not executed |
| Runtime UX | 0.40 | Source inspection only, no browser execution |
| Deployment readiness | 0.20 | No verified deployment or CI evidence |
| Commercial readiness | 0.10 | No verified commercial implementation |
| Overall audit confidence | 0.94 | High confidence in inventory and gaps; explicit limits preserved |

## 7. Lessons learned

1. Product names must resolve to repositories before an audit begins.
2. An enterprise registry scan cannot substitute for a product audit.
3. Required deliverables must be machine-enforced at status transition.
4. Evidence references must be nonempty and semantically mapped to every required deliverable.
5. A successful assignment result must precede task completion.
6. Repository fragmentation is itself an audit finding and must not be hidden by selecting only the newest repo.
7. README claims must reconcile with current source behavior.
8. Client-build secret injection must be treated as a production Stop-Gate even when the feature is not currently called.
9. Static content richness and application convenience require a formal parity process.

## Deliverable matrix

| Required deliverable | Result | Evidence location |
|---|---|---|
| Canonical inventory | PASS | Section 1 |
| Dependency graph | PASS | Section 2 |
| Gap register | PASS | Section 3 |
| Technical-debt register | PASS | Section 4 |
| Remediation backlog | PASS | Section 5 |
| Confidence report | PASS | Section 6 |
| Lessons learned | PASS | Section 7 |

## Acceptance

BOW-004 CTJ audit: **COMPLETE WITH FINDINGS**.

CTJ production readiness: **NON-PASS**.

The audit completion does not authorize production release. The P0 backlog is mandatory before release review.

## Rollback

- The audit itself changes no CTJ source or production data.
- The completion-contract migration may be rolled back by dropping `trg_enforce_task_completion_contract` and `dcse_cp.enforce_task_completion_contract()`.
- Rollback is not recommended because the control prevents the exact false-completion defect that affected BOW-002 and BOW-003.
