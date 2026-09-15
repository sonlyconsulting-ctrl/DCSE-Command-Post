# DCSE Ollama Worker Supabase Acceptance Runbook v1

**Status:** CANDIDATE
**Architecture:** Supplements `02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md`
**Security boundary:** `v7_worker` is INTERNAL_SERVER_ONLY and service-role accessible. The model never receives the credential.

## 1. Purpose

Prove that the local Ollama worker remains operational after Supabase privilege hardening while anonymous and unrelated authenticated access remains denied.

## 2. Preconditions

- Approved Task ID, non-critical test task, lane, and rollback/cleanup plan.
- Worker identity is approved for the test lane/task type.
- Supabase URL and service credential are loaded from the approved broker/DPAPI or server secret store.
- No secret is printed, copied to prompts, stored in evidence, or exposed to the browser.
- `anon` and `authenticated` have no USAGE/EXECUTE/table privileges on internal `v7_worker`.
- Stop-gate and dead-letter behavior are known.

## 3. Controlled acceptance cycle

1. Record worker ID, device, model version, branch, lane, and UTC start time.
2. Enqueue or select one non-critical test task through the authorized control path.
3. Claim it using the worker's server-side service channel.
4. Verify exactly one active claim, correct task/lane/type, lease and visibility timeout.
5. Send heartbeat and verify liveness/current-task fields.
6. Produce a harmless deterministic result.
7. Submit and acknowledge the result or exercise the approved release/close path.
8. Verify claim closure, durable result, queue state, and no unintended retry/dead letter.
9. Run negative checks showing anonymous and unrelated-authenticated roles cannot use the internal schema or worker RPCs.
10. Remove only disposable test data under the approved cleanup method.

## 4. Required evidence

- Task and Handoff IDs
- Worker/agent ID and credential class, never secret value
- Queue message, claim, heartbeat, and submission identifiers
- Start/end timestamps and elapsed time
- Expected versus actual state transitions
- Negative-role denial evidence
- Logs with secrets and sensitive payloads redacted
- Advisor/privilege snapshot
- Failure diagnosis and next gate

## 5. Failure prescription

- `42501` for the service worker: confirm it is using the service credential and correct project; do not reopen client grants.
- Anonymous request succeeds: stop worker promotion and restore least-privilege containment immediately through an approved migration.
- Claim succeeds but heartbeat/result fails: inspect project binding, RPC signature, lease, and service grant; do not bypass RLS with a new definer.
- Duplicate claims: examine transaction locking, visibility timeout, and worker concurrency.
- Lost result/reopen failure: verify durable result/claim records and resume identifiers before retry.
- Secret appears in logs or prompts: stop, rotate credential, sanitize evidence, and open an incident.
- Lane/privacy mismatch: stop, quarantine task/result, and escalate to DCS.

## 6. Pass criteria

PASS requires a complete claim-to-close cycle, durable evidence, zero duplicate claim, correct lane enforcement, preserved service access, and verified client denial. Repository configuration alone is not runtime proof.
