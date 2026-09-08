# DCSE AGY Supabase Discovery Certification Packet v1

**Task ID:** DCSE-ORCH-20260908-006  
**Parent:** DCSE-ORCH-20260908-005 / GitHub Issue #56  
**Lane:** DCSE / Command Post  
**Task type:** Runtime admission certification  
**Action:** Prove AGY provider execution through the governed control-plane lifecycle using a read-only Supabase discovery workload  
**Status:** READY FOR EXECUTION / NOT YET CERTIFIED

## Preflight Validation

**Authority/source:** Current GitHub governance, Issue #56, provider-neutral inter-agent contract candidate, Antigravity runtime admission addendum.  
**Execution surface:** `agy.exe` 1.1.12, subject to live probe.  
**Systems/access:** Command Post worker/claim surface, local AGY CLI, authorized read-only Supabase access.  
**Secret exposure:** PROHIBITED.  
**PS exposure:** NO. PS lane access must remain denied.  
**Approval need:** No approval for read-only certification within existing authorization. Any write/remediation, credential change, governance promotion, public release, or PS access requires escalation.  
**Rollback:** terminate claim/process, release or fail claim according to state machine, remove only certification-generated temporary artifacts if policy permits, preserve receipt/evidence. No production data rollback should be required because writes are prohibited.

## Source executable asset

`enterprise_discovery.ts`

- path: `C:\DS All Things\DCSE_Command_Center\DCSE_CP_Project\dcse-command-post\scripts\enterprise_discovery.ts`
- SHA256: `F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`
- size: `12667`
- LastWriteTime: `2026-09-08 00:55:58` local operator time
- disposition: candidate reusable discovery/automation asset

## Required lifecycle evidence

1. TASK: certification TaskEnvelope accepted by deterministic admission gate.
2. CLAIM: AG/Antigravity logical agent claims through an authorized runtime surface. Record claim ID and lease.
3. HEARTBEAT: real host/runtime heartbeat observed for the claiming surface.
4. EXECUTE: dispatcher invokes `agy.exe` noninteractively without user copy/paste.
5. ARTIFACT: discovery produces sanitized JSON manifest and Markdown narrative.
6. RECEIPT: hashes and normalized ResultEnvelope recorded.
7. VALIDATE: deterministic checks prove read-only behavior, artifact completeness, schema conformance, allowed-root compliance and secret/PS protections.
8. CONTINUE/CLOSE: controller closes only if all required checks pass. Otherwise retry, escalate, Stop-Gate or fail according to policy.

## Discovery constraints

- SELECT/read-only behavior only.
- No migrations, DDL, DML, remediation, deletion or policy changes.
- Do not return individual `auth.users` records.
- Do not return storage object contents.
- Do not expose secrets, tokens, connection strings, browser/CDP endpoints, private keys, environment secret values or authentication material.
- Permission denied must be recorded as an access boundary, not translated into asset absence.
- RLS absence is a candidate finding requiring context, not automatically a compliance defect.
- Edge Functions or management-plane assets that cannot be observed through authorized access must be marked UNKNOWN.

## Deterministic acceptance checks

- source script hash equals `F7F8D758346BE3171EE851D48A052B3AAC9718DFBA172498936616EF74B21844`
- runtime probe reports AGY executable and version
- claim ID exists
- heartbeat timestamp falls within the governed execution window
- runtime surface matches authorized Antigravity surface
- process invocation is noninteractive
- process timeout is bounded
- output parses as required structured result
- required JSON and Markdown artifacts exist
- every durable artifact has SHA256 and size
- artifact paths remain inside allowed roots
- no prohibited database write is evidenced
- no PS lane/resource access is evidenced
- no secret patterns/values are included in persisted outputs
- receipt references the task, claim, result and artifact hashes

## Asset registration candidate

After successful certification, register the discovery script as a reusable enterprise automation/discovery asset with at minimum:

- canonical asset ID
- name and purpose
- lane/entity
- source path
- SHA256
- version/status
- inputs/outputs
- dependencies
- allowed execution surfaces
- read-only safety classification
- owner/authority
- validation evidence
- last certified timestamp
- related workflow/certification Task ID

The exact live registry write must use the current registry schema. Do not invent columns or bypass required fields.

## Exit criteria

PASS only when a real Command Post assignment reaches AGY without manual relay, AGY executes the bounded discovery, artifacts are created and hashed, deterministic validation passes, a receipt is persisted, and control-plane/runtime evidence reconciles. A registry insertion or successful manual CLI invocation alone is insufficient.