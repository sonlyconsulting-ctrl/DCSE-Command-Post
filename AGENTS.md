# DCSE Codex Operating Instructions

## Authority and scope

Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`
Task: `DCSE-PA-MODULE-001`
Current build lane: DCSE / Command Post
Feature branch: `feature/aegis-executive-kernel`

Aegis is the DCS personal Executive Operating System. It is a single-principal internal operating surface that must feel standalone while remaining connected to the Command Post control plane.

Do not treat historical files as authority merely because they exist. Before material implementation, inspect current `governance/v7.2`, the current repository manifest, current Command Post code, migrations, and current runtime configuration. Preserve contradictions as findings rather than silently reconciling them.

## Execution posture

1. Inspect before changing.
2. Reuse verified Command Post and SC Agent OS capabilities before creating duplicates.
3. Build in vertical slices that end in executable tests and evidence.
4. No placeholder integrations may be reported as working.
5. No production deployment, destructive database action, credential change, or irreversible external action without explicit DCS approval.
6. Never place secrets, tokens, service-role keys, private keys, connection strings, MFA data, or recovery data in source, prompts, logs, issues, documentation, or browser code.
7. Use server-side mediation for privileged operations.
8. All user/state tables in exposed Supabase schemas require RLS and tested authorization policies.
9. Treat model output as advisory unless authority has been explicitly delegated by policy.
10. Evidence outranks narrative. A build is incomplete until its claims are tested.

## Model and Codex gate

Astra-capable execution requires Codex CLI `0.153.0` or newer. The first local step is:

```powershell
codex --version
npm install -g @openai/codex@latest
codex --version
```

If the package manager or installed channel differs, discover the supported upgrade command rather than guessing. Do not continue with Astra-specific implementation until the resulting Codex version is `>=0.153.0` and the active model is confirmed.

## Existing baseline to inspect first

At minimum inspect:

- `DCSE_MANIFEST.yaml`
- `governance/v7.2/`
- `apps/sc-agent-os/`
- `apps/sc-agent-os/docs/IMPLEMENTATION_STATUS.md`
- `apps/sc-agent-os/docs/PRIVACY_CONTROLS.md`
- `apps/sc-agent-os/docs/GOVERNANCE_GATES.md`
- `apps/sc-agent-os/migrations/`
- current Supabase schema and advisors
- current Vercel/Netlify routing relevant to Command Post

Existing Agent OS capabilities include task/portfolio CRUD, Tribunal dispatch, runtime health, phase gates, DCS decision queue, receipts/evidence, personas/assets, Supabase-backed governance surfaces, and prior security remediation. Reuse or refactor them. Do not rebuild those capabilities merely under an Aegis label.

## Aegis MVP contract

Initial mission domains:

- DCS Enterprise
- DCS Employment

Initial must-have capabilities:

- Google sign-in for the DCS principal
- primary Sonly Consulting Google identity and DSEADO01 backup identity mapped to the same principal when technically supported
- persisted executive session state independent of chat history
- durable job lifecycle
- next-best-action calculation
- opening executive briefing from actual persisted state
- approval queue
- evidence/receipt history
- bounded initiative
- Command Post deep-link / hybrid operating view
- Android-first notification architecture, with in-app and email secondary paths

The opening briefing must answer from state, not invented narrative:

1. What changed?
2. What completed?
3. What requires DCS approval?
4. What is the highest-value next action?
5. What blockers exist?

## State model

Keep at least these concerns separate:

- conversation state
- executive state
- mission state
- job state
- approval state
- evidence state
- notification state

Do not use the LLM transcript as the source of truth for job, authorization, completion, or evidence state.

## Job lifecycle

Minimum states:

`queued -> running -> waiting_approval -> completed | failed | cancelled -> archived`

Every job must have a stable identifier, mission, priority, executor, current state, timestamps, provenance, and evidence references. Long-running work must be resumable/idempotent where practical.

## Governance and rules

Business rules are governed data, not prompt prose alone. Keep doctrine, executable business rules, policy evaluation, and model instructions distinct.

For consequential actions, evaluate authorization deterministically before dispatch. Approval does not replace governance. Governance determines whether an approval request is valid.

## Supabase rules

- Verify current Supabase docs/changelog before implementing features.
- RLS on every table in exposed schemas.
- Never use user-editable metadata for authorization.
- Never expose `service_role` or secret keys to clients.
- Prefer ownership predicates in RLS policies.
- UPDATE policies require both `USING` and `WITH CHECK` where ownership can change.
- Treat views and `SECURITY DEFINER` functions as security-sensitive.
- Run advisors after schema/security changes.
- Verify each schema change with test queries and adversarial authorization tests.
- Use queues for durable asynchronous job dispatch when available and appropriate; use cron only as a trigger/scheduler, not as the primary orchestration engine.

## DCS branding

Use existing DCS Enterprise branding when present. Current repository doctrine identifies the DCSE visual palette as:

- DCSE Blue `#0A192F`
- Gold `#D4AF37`

Aegis should feel executive, precise, premium, calm, and operational. Do not expose internal doctrine text in the public/client surface. Avoid neon/default-browser aesthetics. Build responsive mobile/desktop layouts and target accessible contrast and keyboard operation.

If a required Aegis-specific visual token is not defined, create it as a clearly labeled Aegis candidate token derived from the DCS palette rather than silently declaring a new enterprise brand standard.

## Validation

Two distinct test passes are mandatory.

Pass 1: functional/integration
- persistence
- state transitions
- Google auth behavior
- RLS and unauthorized access
- Supabase integration
- job dispatch/retry/failure handling
- approvals
- evidence creation
- connector failure behavior

Pass 2: end-to-end/adversarial/regression
- desktop and mobile
- accessibility target checks
- session restore across reload/device simulation where testable
- permission escalation attempts
- destructive-action gating
- stale/duplicate job behavior
- regression after corrections

Calculate release confidence from objective evidence. Target `>=95/100` with no critical security/governance gate failure. A numeric score never overrides a failed hard gate.

## Closeout

For every vertical slice record:

- what changed
- files/migrations changed
- tests executed and results
- evidence references
- limitations
- rollback path
- next recommended slice

Do not claim COMPLETE without executable evidence.