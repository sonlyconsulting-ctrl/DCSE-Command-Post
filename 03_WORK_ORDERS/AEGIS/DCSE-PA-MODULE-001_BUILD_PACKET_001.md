# AEGIS BUILD PACKET 001

**Task ID:** DCSE-PA-MODULE-001  
**Lane:** DCSE / Command Post  
**Execution model:** Codex + GPT-6 Astra  
**Branch:** `feature/aegis-executive-kernel`  
**Objective:** Bring the first usable Aegis Executive Kernel online as a governed vertical slice.

## Mission

Build, test, and document the first usable version of Aegis. Do not stop at architecture narration. Inspect current state, reuse proven Command Post assets, implement one complete vertical slice, run two validation passes, repair defects, and leave an evidence-backed closeout.

Aegis is DCS's personal Executive Operating System. It must feel standalone while using the Command Post as its governance/control plane. It is advisory by default, proactive within delegated authority, and never a voting executive decision-maker.

## Gate 0: Local Astra readiness

Before code changes on the DCS workstation:

```powershell
codex --version
npm install -g @openai/codex@latest
codex --version
```

Requirement: Codex CLI `>=0.153.0` and GPT-6 Astra selectable/active for the build session.

If install method differs from npm, discover the supported upgrade command from the installed channel. Record old version, new version, command used, and outcome. Do not expose credentials.

## Gate 1: Baseline inspection

Read `AGENTS.md` first.

Inspect before changing:

1. `DCSE_MANIFEST.yaml`
2. `governance/v7.2/`
3. `apps/sc-agent-os/`
4. existing migrations and schema assumptions
5. current Command Post runtime/deployment wiring
6. current Supabase project schema, RLS, auth settings, queues/cron availability, and advisors
7. current GitHub issue/PR state that can materially affect the build

The existing SC Agent OS is a reuse candidate, not a disposable predecessor. Preserve functional capability and refactor only where the Aegis slice requires it.

Produce a short baseline note with VERIFIED / LIKELY / UNKNOWN findings. Do not block on minor unknowns that can be safely isolated. Hard-stop only for missing authority, credentials/access, destructive-action approval, unresolved security exposure, or conflicting current governance.

## Vertical Slice 001

Implement the minimum end-to-end path below.

### 1. Aegis application surface

Create or extend the repository so Aegis has a dedicated operating surface under the same control plane. Prefer a clean `apps/aegis/` boundary unless repository inspection shows a better existing pattern.

Default landing experience:

- Aegis identity/header
- greeting mode by default
- DCS Enterprise mission card
- DCS Employment mission card
- executive briefing panel
- next-best-action panel
- active/recent jobs
- approvals requiring DCS
- completed-since-last-session summary
- Command Post access button/deep link
- optional hybrid layout when practical without delaying the vertical slice

Responsive design is required for desktop and Android-class mobile widths.

### 2. DCS branding

Use the existing DCS Enterprise palette and visual language:

- DCSE Blue `#0A192F`
- Gold `#D4AF37`

Use calm executive hierarchy, restrained motion, accessible contrast, strong information density, and clear status semantics. If Aegis-specific tokens are needed, create candidate tokens derived from the DCS palette and label them candidate/internal. Do not silently redefine enterprise branding.

### 3. Authentication

Implement Google authentication through the existing Supabase project where compatible.

Target identity model:

- one DCS principal
- Sonly Consulting Google identity as primary
- DSEADO01 Google identity as backup
- both identities must resolve to the same Aegis principal when the current auth architecture safely supports linked identities

If live OAuth configuration requires dashboard/user intervention, implement all code/config scaffolding and stop only at the specific external approval/configuration step. Record exact remaining action.

### 4. Persisted state

Create/reuse the smallest safe schema needed for:

- principals
- missions
- executive_sessions
- jobs
- job_events
- approvals
- evidence/receipts
- next_actions
- notifications or notification intents if required for this slice

Do not duplicate existing Command Post tables when a stable existing table or view can be safely reused.

State must survive browser reload and be reconstructable independently of model chat history.

### 5. Durable job lifecycle

Implement at least:

`queued -> running -> waiting_approval -> completed | failed | cancelled -> archived`

Every job requires:

- stable ID
- mission
- title/purpose
- priority
- executor/tool target
- state
- created/updated/completed timestamps
- provenance/source
- approval requirement indicator
- evidence references
- error/failure detail when applicable

Use Supabase Queue-backed dispatch if available and compatible with current project state. If not available/configured, implement a repository-local abstraction that can be swapped to Supabase Queues without redesigning the job state model. Do not fake queue completion.

### 6. Executive briefing

On Aegis launch and on demand, derive a briefing from persisted state answering:

1. What changed since the prior Aegis session?
2. What completed?
3. What requires DCS approval?
4. What is the highest-value next action?
5. What blockers exist?

No fabricated narrative. If there is no data, state that explicitly.

### 7. Next-best-action engine

For Slice 001, implement deterministic scoring before adding model interpretation.

At minimum score using:

- mission priority
- task/job priority
- deadline/urgency
- blocked/unblocked status
- approval dependency
- revenue relevance where known
- aging/staleness
- explicit DCS override

Return the highest-value actionable item plus a transparent reason summary. The model may later enrich the explanation, but the ranking must be reproducible from stored state.

### 8. Governance and approval boundaries

Aegis may autonomously:

- inspect/read approved data
- organize and prioritize
- generate summaries
- prepare drafts
- create internal candidate tasks/jobs
- run approved non-destructive checks/tests

Require DCS approval for at least:

- external sends/messages
- public publishing
- spending/purchases
- production deployment
- destructive database/source operations
- credential/authentication configuration changes
- deletion of authoritative evidence/source records
- irreversible external actions

The UI must visibly distinguish recommendation, proposed action, approved action, and completed action.

### 9. Supabase security

Before considering Slice 001 complete:

- enable RLS on every exposed user/state table
- use explicit owner/principal predicates
- never authorize from user-editable metadata
- keep service-role/secret credentials server-side
- test SELECT/INSERT/UPDATE/DELETE behavior for authorized and unauthorized contexts
- test anonymous rejection where required
- inspect views and privileged functions
- run Supabase advisors after changes
- document residual findings

No security finding may be waived merely to achieve the release score.

### 10. Notification architecture

Primary target: Android push notification.
Secondary: in-app notification and email.

For Slice 001, it is acceptable to implement notification intents/in-app delivery and the provider abstraction if full Android push provisioning requires a later external configuration step. Do not label Android push as working until an actual device receives a test notification.

## Reuse requirements

Before writing replacement code, inspect existing SC Agent OS capabilities for:

- task queue
- portfolio
- Tribunal dispatch
- DCS decision queue
- receipts/evidence
- phase gates
- runtime health
- Supabase schema
- persona/assets governance

Prefer shared services/modules or compatible API contracts over code duplication.

## Testing mandate

### Pass 1: Functional and integration

Test:

- app boot
- auth happy path and rejected path
- session persistence
- mission retrieval
- job creation/state transitions
- job failure handling
- approval transitions
- briefing derivation
- next-best-action reproducibility
- RLS access matrix
- evidence/receipt creation
- queue/worker behavior when implemented
- connector/network failure handling

### Repair cycle

Fix all P0/P1 defects and all security/governance defects. Re-run impacted tests before Pass 2.

### Pass 2: End-to-end, adversarial, regression

Test:

- desktop workflow
- Android/mobile viewport workflow
- keyboard navigation/accessibility basics
- reload/session restore
- duplicate submission/idempotency where relevant
- stale job handling
- unauthorized row access attempts
- approval bypass attempts
- destructive action without approval
- regression of previously passing flows

## Objective release score

Score only from evidence:

- requirements/architecture conformance: 10
- reproducible build/install: 10
- database/schema integrity: 10
- auth/RLS security: 15
- unit/component tests: 10
- integration tests: 15
- end-to-end workflows: 15
- failure/retry/recovery: 5
- regression: 5
- deployment/rollback evidence: 5

Target: `>=95/100` AND no failed hard gate.

A failed critical security, authority, governance, data-integrity, or rollback gate means FAIL regardless of numeric score.

## Deliverables

Commit on the feature branch:

1. working Slice 001 code
2. migrations/schema changes
3. automated tests
4. `apps/aegis/docs/BASELINE_INSPECTION.md`
5. `apps/aegis/docs/TEST_PASS_1.md`
6. `apps/aegis/docs/TEST_PASS_2.md`
7. `apps/aegis/docs/RELEASE_SCORE.md`
8. `apps/aegis/docs/ROLLBACK.md`
9. `apps/aegis/docs/LIMITATIONS_AND_NEXT_SLICE.md`

Open a draft PR to `main` only after local/integration evidence exists. Do not merge or deploy to production without DCS approval.

## Exit criteria

Slice 001 exits only when:

- Aegis launches
- persisted state works
- at least one real mission/job flow completes end-to-end
- the briefing reads actual persisted state
- next-best-action returns a reproducible result
- RLS adversarial tests pass
- two test passes are documented
- rollback is documented and feasible
- release score is calculated from evidence
- remaining external configuration steps are explicit

If blocked, return a precise BLOCKED/PARTIAL closeout with the smallest action DCS must take next. Do not replace missing execution evidence with prose.