# DCSE Doctrine D04: Command Post Communications v7.1 RC3 Candidate

**Document ID:** DCSE-D04-v7.1-RC3-CANDIDATE  
**Version:** v7.1 RC3  
**Status:** CANDIDATE PENDING DCS REVIEW AND PROMOTION  
**Classification:** DCSE INTERNAL  
**Lane:** ALL, subject to PS and PPR isolation  
**Authority holder:** DCS  
**Prepared date:** 2026-08-03  
**Source doctrine:** `governance/v7.1/source/doctrines/D04_Command_Post_Communications.md`  
**Source SHA-256:** `513dff0c525e7ad8bbdd59ed64c8d9c352944d3d89f8a12882cef327a562ffde`  
**Parent candidate:** `governance/v7.1/candidates/20260803_doctrine_executability/DCSE_Master_Profile_v7.1_RC3_CANDIDATE.md`  
**Orchestration dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D03_AI_Orchestration_v7.1_RC3_CANDIDATE.md`  
**Orchestration dependency SHA-256:** `88e80cf310ea55b36571d565218863f60171de228c13d9cead81e69b0a60beb0`  
**Distribution dependency:** `governance/v7.1/candidates/20260803_doctrine_executability/D22_Source_Authority_Runtime_Distribution_v7.1_RC3_CANDIDATE.md`  
**Distribution dependency SHA-256:** `0f27e111e429e53c94ee9a7f73d925089a854fb88e2739a23416e2afd86a830a`  
**Candidate branch:** `agent/v71-master-profile-rc3-manual`  
**Promotion effect:** NONE until DCS approves the exact candidate or exact diff and D05 and D22 processing is complete.  

## 1. Purpose

D04 governs communication between DCS, models, agents, scripts, pollers, GitHub, Supabase, local runtimes, offline systems, deployment systems, and human operators.

D04 defines message identity, routing, delivery state, acknowledgment, retries, GitHub communication receipts, poller behavior, conflict handling, and truthful closeout. It does not create task authority or promotion authority.

## 2. Communication principles

1. A channel is not authority.
2. A write is not delivery.
3. Delivery is not acknowledgment.
4. Acknowledgment is not task claim.
5. Task claim is not execution.
6. Heartbeat is not completion.
7. Chat narrative is not system evidence.
8. Every material message has one identity, one intended audience, and an attributable sender.
9. Retries must be idempotent.
10. Protected content never crosses an unauthorized lane or adapter.

## 3. Communication channels

Approved channel classes include:

| Channel | Purpose |
|---|---|
| DCS conversation | Direction, clarification, decisions, and attributable human approval. |
| GitHub | Versioned canonical artifacts, branches, pull requests, reviews, issues, and workflow evidence. |
| DCSE-DDNA Supabase | Constitutional runtime references, governance tasks, receipts, acknowledgments, and execution state through approved adapters. |
| SC Command Post Supabase | Operational application, worker, product, and task state through approved adapters. |
| Local or offline queue | Bounded host execution and protected or disconnected workflows. |
| Poller or scheduler | Transport, claim, liveness, and retry of eligible tasks. |
| Email or notification | Human notice and escalation; not an execution queue unless expressly adapted. |
| Deployment platform | Build, preview, deployment, and operational status. |

Physical table names, folders, filenames, schedules, repositories, or endpoints are adapter configuration, not permanent doctrine.

## 4. Message envelope

```yaml
message_envelope:
  schema_version: "1.0"
  message_id: ""
  correlation_id: ""
  causation_id: ""
  conversation_id: ""
  turn_id: ""
  task_id: ""
  assignment_id: ""
  sender_id: ""
  sender_runtime: ""
  audience: []
  target_channel: ""
  entity: ""
  lane: ""
  classification: ""
  message_type: ""
  priority: "ROUTINE | HIGH | RESERVED"
  authority_ref: ""
  canonical_source_refs: []
  content_hash: ""
  payload_ref: ""
  idempotency_key: ""
  acknowledgment_required: false
  expires_at: ""
  created_at: ""
```

The envelope contains references instead of secret values, unrestricted URLs, or private reasoning.

## 5. Message types

| Type | Meaning |
|---|---|
| `DIRECTIVE` | DCS or valid authority communicates an instruction. |
| `TASK_ASSIGNMENT` | Bounded task offered to an eligible runtime. |
| `TASK_CLAIM` | Runtime accepts accountable ownership. |
| `HEARTBEAT` | Runtime or worker reports liveness and current assignment reference. |
| `STATUS_UPDATE` | Current verified execution state. |
| `EVIDENCE_SUBMISSION` | Retrievable outputs and test evidence. |
| `VALIDATION_RECEIPT` | Attributable review result. |
| `PROMOTION_RECEIPT` | D05 lifecycle authority result. |
| `RECONCILIATION_RECEIPT` | D22 source and distribution result. |
| `ANNOUNCEMENT` | Informational communication with no task ownership. |
| `ERROR` | Verified failure and affected scope. |
| `RETRY` | Authorized repeat of an idempotent operation. |
| `ESCALATION` | Reserved decision or unresolved high-risk condition. |
| `REVOCATION` | Access, assignment, message, or distribution withdrawal. |

An announcement cannot be treated as a task assignment unless a governed adapter explicitly converts it and records the resulting assignment identity.

## 6. Communication state machine

```text
CREATED
  -> QUEUED
  -> DISPATCHED
  -> DELIVERED
  -> ACKNOWLEDGED
  -> CONSUMED
```

Exceptional states are `RETRY_PENDING`, `DELIVERY_FAILED`, `EXPIRED`, `REVOKED`, `DUPLICATE`, and `DEAD_LETTERED`.

Each state requires direct evidence:

| State | Evidence |
|---|---|
| `CREATED` | Durable message identity and content. |
| `QUEUED` | Accepted by the configured queue or transport. |
| `DISPATCHED` | Attributable delivery attempt. |
| `DELIVERED` | Target endpoint accepted the message. |
| `ACKNOWLEDGED` | Intended target or listener confirmed receipt. |
| `CONSUMED` | Target reports governed processing of the exact message. |

## 7. Task communication lifecycle

Task state is separate from message state:

```text
ASSIGNED
  -> CLAIMED
  -> STARTED
  -> HEARTBEAT_ACTIVE
  -> OUTPUT_SUBMITTED
  -> VALIDATED
  -> PROMOTED_IF_APPLICABLE
  -> RECONCILED
  -> CLOSED
```

A communication adapter must not advance task state beyond the evidence received. A poller claim may create `CLAIMED`; it cannot create `OUTPUT_SUBMITTED` or `VALIDATED` without additional evidence.

## 8. Channel adapter contract

Every adapter defines:

- channel and environment identity;
- verified physical schema, path, API, or protocol;
- authentication method;
- permitted message types;
- lane and classification limits;
- idempotency behavior;
- delivery and acknowledgment evidence;
- retry and dead-letter behavior;
- payload size and retention limits;
- monitoring and health behavior;
- revocation and cleanup;
- adapter version and authority reference.

If an adapter cannot be verified, affected writes are disabled. Other approved channels may continue.

## 9. GitHub communication

### 9.1 Repository and branch resolution

The current manifest, task declaration, and D22 canonical identity determine repository, base branch, working branch, and permitted actions. D04 does not maintain a permanent model-to-branch table.

Before a GitHub write:

1. resolve repository and branch;
2. verify access and working-tree or remote state;
3. identify exact intended files;
4. preserve unrelated user changes;
5. scan intended content for secrets and protected material;
6. verify branch protection and authority boundary;
7. use the smallest safe commit set;
8. verify the remote result;
9. issue or queue the communication receipt.

### 9.2 Commit behavior

- Stage or submit only intended files.
- Do not treat a dirty worktree as disposable.
- Do not force-push, discard, overwrite, or reset another contributor's work without explicit authority.
- Use a feature or candidate branch unless the applicable standing rule permits another target.
- A merge does not independently create D05 promotion.
- Batch related files when safe to reduce workflow and notification noise.

### 9.3 GitHub receipt

```yaml
github_operation_receipt:
  schema_version: "1.0"
  operation_id: ""
  repository: ""
  branch: ""
  base_ref: ""
  operation: "CREATE | UPDATE | DELETE | COMMIT | PUSH | PR | REVIEW | MERGE"
  commit_shas: []
  file_refs: []
  content_hashes: []
  pull_request_ref: ""
  workflow_results: []
  remote_verification: "NOT_RUN"
  exclusions: []
  findings: []
  accountable_identity: ""
  completed_at: ""
```

GitHub and receipt writes cannot be perfectly atomic across independent systems. The truthful states are `GITHUB_CONFIRMED_RECEIPT_PENDING`, `RECEIPT_CONFIRMED_GITHUB_PENDING`, `RECONCILED`, or `FAILED`. D22 completes reconciliation. No phantom atomicity may be claimed.

## 10. Git conflict handling

When local and remote work conflict:

1. preserve both states;
2. identify authorship, commits, paths, and intended authority;
3. stop only overlapping writes;
4. continue unaffected files and tasks;
5. resolve mechanically safe conflicts when authority and intent are clear;
6. route ambiguous user-versus-agent, doctrine-authority, protected-lane, or destructive conflicts;
7. test the merged result;
8. record the resolution.

Neither local nor remote state automatically wins merely because of location. Force resolution without evidence is prohibited.

## 11. Pollers and schedulers

Pollers and schedulers are communication and execution transports.

Required controls include:

- configurable eligibility rules rather than obsolete hardcoded allowlists;
- one active instance when concurrent execution is unsafe;
- lease, claim, and expiration behavior;
- idempotency and duplicate suppression;
- bounded retries and dead-letter state;
- liveness heartbeat;
- current assignment identity;
- output and error references;
- capability-based fallback;
- credential-source verification without exposure;
- health-monitor evidence;
- clean shutdown and restart recovery.

A healthy scheduled task proves scheduler and liveness state only. Productive completion requires output and validation evidence.

## 12. Supabase communication

Supabase communication uses verified D22 adapters. The logical operation records:

- project and environment;
- adapter version;
- object and message identity;
- operation type;
- idempotency key;
- returned record identity;
- affected row count when available;
- delivery and acknowledgment state;
- RLS or authorization result;
- reconciliation state.

A successful insert is not evidence that another runtime received, consumed, or acted on the message.

## 13. Local and offline communication

Local or offline queues may support host execution, recovery, protected operation, or disconnected work. Their exact paths are configuration.

An offline adapter must define:

- controlled root;
- permitted lanes and classifications;
- schema and filename behavior;
- single-writer or locking rules;
- watcher or polling behavior;
- archive and retention;
- acknowledgment evidence;
- synchronization and reconciliation procedure.

PS material may use a protected offline adapter. It must not be mirrored into general GitHub, Supabase, email, or model retrieval.

## 14. Retry, timeout, and dead-letter behavior

- Retries preserve the same idempotency key for the same logical message.
- Retry policy is bounded and adapter-specific.
- A timeout is recorded as unknown delivery unless the channel proves failure.
- Exhausted retries enter `DEAD_LETTERED` or equivalent failure state.
- A later successful retry records its relationship to prior attempts.
- Retry must not create duplicate tasks, promotions, deployments, or notifications.

## 15. Notifications and noise control

Notifications are routed by severity and actionable audience.

- Applicable validation failures notify the responsible owner.
- Repeated failures from one root cause are grouped where possible.
- Documentation-only commits should not trigger unrelated deployment or model-repair notifications.
- Successful routine events may be summarized rather than emailed individually.
- Reserved security, credential, protected-lane, destructive, and production incidents remain immediate.

Email volume is an operational signal, not authority. Notification cleanup must not hide unresolved critical events.

## 16. Security and protected content

- Secret values are excluded from messages and receipts.
- Payload access is least-privilege and lane-scoped.
- PS and PPR content uses authorized protected channels only.
- Public notifications contain no internal paths, project identifiers, private findings, or unrestricted links unless expressly safe.
- Message signatures or tokens are adapter concerns and are never placed in model-visible doctrine payloads.
- Untrusted inbound payloads are validated before processing.

## 17. Status reporting

Every status report separates:

- verified;
- likely;
- unknown;
- failed or blocked;
- next executable action;
- authority required, if any.

Claims must cite retrievable evidence. Phrases such as sent, delivered, completed, promoted, synchronized, and healthy are used only when the corresponding state is directly proven.

## 18. Communication reconciliation

D22 reconciliation compares:

- message identity and content hash;
- sender and target;
- channel and adapter version;
- queue, delivery, acknowledgment, and consumption evidence;
- linked task and execution states;
- GitHub and Supabase references;
- retries, duplicates, expiration, and revocation;
- unresolved findings.

## 19. Degraded behavior

| Condition | Response |
|---|---|
| Primary channel unavailable | Use approved fallback and record pending reconciliation. |
| Acknowledgment unavailable | Report delivery only to the proven state. |
| Poller unavailable | Use manual authenticated execution or another eligible worker. |
| Supabase unavailable | Continue GitHub and approved offline evidence; queue runtime reconciliation. |
| GitHub unavailable | Continue safe local or database evidence only when canonical identity remains verified. |
| D04 unavailable | Avoid unverified communication claims; use D03 and D22 fallback contracts. |
| Protected-lane leak | Contain affected payload and invoke reserved controls. |

## 20. Implementation contract

A reusable D04 module must expose equivalent functions:

```python
build_message(payload, context) -> MessageEnvelope
validate_message(envelope, adapter) -> ValidationResult
queue_message(envelope, adapter) -> QueueResult
dispatch_message(message_ref, adapter) -> DeliveryResult
record_acknowledgment(message_ref, evidence) -> AcknowledgmentResult
claim_assignment(message_ref, runtime, lease) -> ClaimResult
classify_git_operation(request, manifest) -> GitOperation
build_github_receipt(operation, result) -> GitHubOperationReceipt
classify_conflict(local, remote, authority_context) -> ConflictResult
poll_once(poller_context) -> PollerCycleResult
reconcile_communication(context) -> ReconciliationReceipt
```

Identical verified inputs and adapter versions must produce deterministic message, state, and routing classifications.

## 21. Mechanical acceptance tests

| Test | Scenario | Expected result |
|---|---|---|
| D04-001 | Announcement row inserted | Creation or queue state recorded; delivery not inferred. |
| D04-002 | Target acknowledges exact message | State advances to `ACKNOWLEDGED`. |
| D04-003 | Poller claims task | Task is `CLAIMED`; output is not inferred. |
| D04-004 | Fresh heartbeat exists | Liveness proven; completion remains separate. |
| D04-005 | Retry repeats logical message | Same idempotency key prevents duplicate task. |
| D04-006 | Preferred poller runtime unavailable | Capable fallback or manual authenticated execution selected. |
| D04-007 | Obsolete allowlist blocks approved tasks | Allowlist identified as configuration drift and corrected within scope. |
| D04-008 | Two pollers overlap unsafely | Single-instance or lease control prevents duplicate execution. |
| D04-009 | GitHub write succeeds but receipt adapter fails | `GITHUB_CONFIRMED_RECEIPT_PENDING`; no false reconciliation. |
| D04-010 | Receipt exists for failed GitHub write | Receipt corrected; GitHub result remains failed. |
| D04-011 | Remote and local files conflict | Both preserved; only overlapping write isolates. |
| D04-012 | Documentation commit triggers unrelated workflows | D22 workflow drift recorded; applicable validation assessed separately. |
| D04-013 | Supabase insert succeeds | Insert proven; delivery and consumption remain unproven. |
| D04-014 | Supabase adapter schema is unverified | Writes disabled; approved fallback continues. |
| D04-015 | PS payload targets general channel | Payload blocked and contained. |
| D04-016 | Notification failures share one root cause | Events grouped without hiding severity. |
| D04-017 | Timeout occurs after dispatch | Delivery remains unknown unless channel proves result. |
| D04-018 | Model claims message was sent from chat only | Claim rejected without channel evidence. |
| D04-019 | Git repository has unrelated user changes | Intended files isolated; unrelated changes preserved. |
| D04-020 | D04 unavailable | D03 and D22 fallback used; unverified communication claims prohibited. |

## 22. Source-to-candidate change record

| Source condition | Candidate correction | Reason |
|---|---|---|
| Two hardcoded Windows inboxes define communication | Uses channel and adapter contracts | Supports local, cloud, and offline execution without path assumptions. |
| Packet schema uses ambiguous authority and limited states | Adds complete message identity, authority reference, and state model | Makes delivery mechanically provable. |
| Permanent model-to-source table points to v69 | Uses manifest, task, D21, and D22 source resolution | Removes stale named-model routing. |
| Repository and branch map is hardcoded | Resolves targets from current authority and manifest | Prevents obsolete Git routing. |
| Local state always wins some conflicts | Preserves both and resolves by evidence and authority | Prevents destructive overwrite. |
| Git push and receipt declared perfectly atomic | Uses explicit partial and reconciliation states | Independent systems cannot guarantee atomicity. |
| Poller schedule and branch are constitutional constants | Moves cadence and endpoints to adapter configuration | Supports change without doctrine rewrite. |
| Mailbox, delivery, task, heartbeat, and completion states blur | Separates communication and task lifecycles | Prevents false reporting. |
| Notifications lack noise controls | Adds grouping, path eligibility, and actionable routing | Addresses email flooding without hiding incidents. |
| Missing D04 globally halts | Adds D03 and D22 fallback with affected-action isolation | Preserves safe non-stoppage. |
| No executable acceptance suite | Adds D04-001 through D04-020 | Enables repeatable validation. |

## 23. Candidate disposition

**Disposition:** `D04_EXECUTABLE_COMMUNICATIONS_CANDIDATE_PENDING_VALIDATION_AND_PROMOTION`

**Operational use before promotion:** Review and implementation specimen only.

**Next required state:** Validate with D03, D06, D15, D21, D22, GitHub, Supabase, poller, and offline adapters; run D04-001 through D04-020; obtain exact DCS decision.
