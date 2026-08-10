# V7.1 First-Assignment Readiness and Fail-Fast Gate

Status: ACTIVE CONTROLLED USE
Authority: DCS Level 0 conditional authorization
Applies to: every framework, model, agent, worker, product lane, repository task, and scheduled runtime

## Purpose

Prevent a framework from discovering missing access, missing paths, missing dependencies, missing authority, or missing rollback only after it receives meaningful work.

No framework receives its first production-relevant assignment until it completes a bounded readiness assignment.

## Required Readiness Assignment

The first assignment for every new or materially changed framework is a non-destructive preflight with no production writes.

The framework must prove all applicable checks below.

### Identity and governance

- Load `/DCSE_MANIFEST.yaml`.
- Identify governance version and operating status.
- Identify assigned lane, role, capability class, and authority ceiling.
- Identify reserved DCS stop gates.
- Produce startup acknowledgment.

### GitHub

- Resolve `sonlyconsulting-ctrl/DCSE-Command-Post`.
- Verify authenticated access.
- Verify the expected branch and current remote HEAD.
- Read one canonical governance file.
- List or query applicable PRs and issues when repository-management access is required.
- Prove write capability with a reversible test only when the assigned role requires writes.
- Never request a PAT in chat.

### Supabase

- Verify access to `DCSE-DDNA` and `SC-Command-Post` through MCP/OAuth, approved connector, or Control Plane.
- Read one approved record from each applicable project.
- Verify the task, evidence, and governance registries needed by the assignment.
- Never request or expose a service-role key.

### Local runtime

- Confirm whether the runtime is local, mounted, or sandbox-only.
- Confirm access to every required local path.
- Verify executable discovery for required tools.
- Verify scheduler or service identity when applicable.
- Record OS, working directory, repository path, and credential method without exposing secrets.

### Dependencies

- Verify imported modules, scripts, configuration files, schemas, migrations, CLIs, and external services.
- Verify version compatibility.
- Verify rate-limit and quota assumptions where applicable.
- Verify required environment variables by name only, never by value.

### Safety and recovery

- Confirm no production mutation is required for preflight.
- Confirm rollback or restoration path.
- Confirm idempotency or duplicate protection.
- Confirm evidence destination and expected outputs.
- Confirm timeout, retry, and stop behavior.

## Gate Outcomes

Only these outcomes are permitted:

- `READY`: all mandatory checks passed.
- `READY_WITH_LIMITATIONS`: work may begin only within listed limitations.
- `NOT_READY_FIXABLE`: framework automatically receives a bounded remediation task.
- `STOP_DCS_REQUIRED`: reserved authority, security, lane, destructive, or production stop gate triggered.

`NOT_READY_FIXABLE` does not return to DCS. The orchestrator assigns remediation, retest, and rereview automatically.

## Fail-Fast Rule

A framework must stop before substantive work when any required precondition is missing. It must report the failed check precisely and may not generalize the failure beyond the tested surface.

Examples:

Permitted: `GitHub push authentication is unavailable in this runtime; read access and local implementation remain available.`

Prohibited: `The Foundational Trilogy is blocked.`

Permitted: `The local C: drive is not mounted in this sandbox.`

Prohibited: `The poller source does not exist.`

## Automatic Remediation Classes

The orchestrator may automatically assign fixes for:

- OAuth or credential-manager setup
- repository remote configuration
- branch checkout or fetch
- canonical path discovery
- missing non-secret environment configuration
- missing dependency installation
- obsolete allowlists
- scheduler command correction
- test fixture creation
- evidence-link reconciliation

DCS approval is not required for these bounded remediations unless they cross a reserved stop gate.

## Reserved DCS Stops

- production deployment or production-data mutation
- destructive database or repository action outside an approved procedure
- security exception or credential exposure
- lane-boundary change
- constitutional governance change
- material architecture replacement
- material spending or paid-service commitment
- public claim or release

## Readiness Receipt

Every framework must return a machine-readable receipt containing:

- framework identity and version
- runtime identity
- governance and lane
- GitHub access status
- Supabase access status
- local path status
- dependency status
- authority ceiling
- limitations
- failed checks
- remediation task references
- evidence references
- outcome
- timestamp

## First Meaningful Assignment Release

A framework receives meaningful work only after outcome `READY` or `READY_WITH_LIMITATIONS` is recorded in Supabase and linked to the task.

The readiness receipt expires when any of these materially change:

- runtime or device
- authentication method
- repository or branch
- Supabase project or schema
- framework version
- required dependency set
- authority or lane

## Foundational Trilogy Application

BOW-001 requires readiness receipts for Qwen Coder and Claude Code before poller implementation or review.

BOW-002 requires a fresh CTJ audit readiness receipt proving access to all approved CTJ repositories, databases, local paths, and evidence stores.

BOW-003 requires a fresh TSL audit readiness receipt proving access to all approved TSL repositories, Supabase projects, deployment systems, branches, and production-readiness evidence.

No body of work advances on an assumed prior login or stale access statement.