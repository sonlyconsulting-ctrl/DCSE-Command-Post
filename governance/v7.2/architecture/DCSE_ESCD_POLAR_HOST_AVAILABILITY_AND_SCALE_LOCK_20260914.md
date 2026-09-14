# DCSE ESCD + Polar Host Availability and Scale Lock

Document ID: DCSE-ESCD-POLAR-HOST-LOCK-20260914
Date: 2026-09-14
Status: LOCKED BY DCS / OPERATIVE-PATCH BASELINE
Lane: DCSE / Command Post / ESCD Runtime
Authority: DCS Level 0

## 1. Purpose

Lock the operating model by which ESCD remains available from any authorized client while governed execution occurs only on eligible machine-hosted Polar runtime capacity.

Polar is the DCS operational name for the machine-resident neutral poller/dispatch/wake execution fabric. It does not create a second governance controller, second durable queue, or second authority layer. Canonical governance remains the DCSE Universal Dispatch Controller / provider-neutral orchestration model.

## 2. Core Architecture

DCS / authorized user -> escd.sonlyconsulting.com -> Supabase durable control plane -> eligible Polar host -> Universal Dispatch Controller / local worker -> approved provider/model -> result + evidence + receipt -> Supabase -> ESCD.

Client location and execution-host location are independent. A phone does not require direct network access to the Windows workstation. The phone uses the permanent ESCD surface and Supabase exchange. If an eligible Polar host is online and heartbeating, the request can be claimed and executed. If no eligible host is online, the request remains durable and waits.

## 3. Host Dependency Rule

A host is execution-eligible only when registered identity, security-approved operating system, protected credentials, required runtime/tooling, fresh heartbeat, lane/capability eligibility, and applicable Stop-Gates are all satisfied.

No UI, provider, or stale database status may imply execution capacity when the required host is unavailable.

## 4. Host Tiers

### Tier 1 — DCS Windows 11 Primary

Host key: DCS-WIN11-PRIMARY
Known host label: LAPTOP-74UF76GB
Mode: ON_DEMAND
Routing priority: 100
Current role: primary DCS/DCSE Polar host.

Expected behavior: used while the Windows 11 workstation is powered on; scheduled poller/health monitor supplies liveness; local Ollama/ESCD worker starts only when needed; browser/mobile clients communicate through ESCD/Supabase rather than localhost; queued requests survive browser closure or client change.

### Tier 2 — Legacy Desktop Secondary Candidate

Host key: DCS-WIN8-SECONDARY-CANDIDATE
Mode target: BEST_EFFORT_24X7
Current security state: HOLD_SECURITY.

This machine is not authorized for production secrets or autonomous DCSE execution while it remains on an unsupported legacy Windows operating system. Before enablement it must receive a supported/hardened OS, protected credentials, canonical host identity, heartbeat certification, worker acceptance testing, security review, and DCS approval.

### Tier 3 — Enterprise 24/7 Polar Server

Host key: DCSE-POLAR-SERVER-01
Mode target: ENTERPRISE_24X7
Current state: PLANNED
Routing priority target: 200.

Enterprise target characteristics: supported server OS, continuous uptime target, automatic restart, independent monitoring, protected secrets, private/zero-trust access, durable logs, capacity monitoring, patching discipline, backup/recovery, explicit RPO/RTO, and provider-neutral bounded workers.

## 5. Mobile and Remote Access

Authorized remote/mobile flow is phone/tablet/laptop -> HTTPS permanent ESCD domain -> Supabase durable request -> eligible Polar host -> worker -> durable result -> ESCD.

Direct public exposure of Windows RDP, local Ollama port 11434, service-role credentials, or local worker APIs is prohibited. Remote desktop administration, if later required, must use an approved private/zero-trust path and is separate from ESCD execution transport.

## 6. Availability Semantics

ONLINE = eligible host with fresh heartbeat. OFFLINE = registered host without fresh heartbeat. PLANNED = not yet provisioned. HOLD_SECURITY = security qualification required. DISABLED = administratively disabled.

When a valid ESCD operation exists but no eligible host is online, the operation remains REQUESTED and the user-facing effective status is WAITING_HOST. WAITING_HOST is derived presentation state and does not require a new operation-turn enum value.

Host absence is not provider failure and must not be represented as completed, failed, or refused.

## 7. Routing Rule

Identify required capabilities; filter to enabled and execution-eligible hosts; require fresh heartbeat and compatible worker; order by routing priority; atomically claim; heartbeat during long work; persist result/evidence; return control to Orchestrator. If no host qualifies, wait durably.

## 8. Windows 11 On-Demand Behavior

The existing scheduled Polar/poller cycle is the host supervision cadence. It may publish heartbeat, inspect durable ESCD REQUESTED turns, ensure the local execution worker is running, start local Ollama only when needed, and start the ESCD Ollama worker in bounded/on-demand mode. This does not create a second queue or controller.

## 9. Phone Use Case

If Windows 11 is online, a phone-submitted request persists, the scheduled Polar cycle sees it, the worker is started/confirmed, the turn is claimed, and the result returns through Supabase. If Windows 11 is powered on but the worker is stopped, the next supervision cycle starts the worker. If Windows 11 is asleep/off, the request waits durably until an eligible host returns. Wake-on-LAN is a future capability requiring separate security design.

## 10. Credential Boundary

Server-side Supabase credentials never appear in browser/mobile code, chat, command transcripts, receipts, logs, or Git. Any plaintext-exposed credential is treated as compromised until rotated and the old credential is proven invalid.

## 11. Implementation State

Production migration polar_runtime_host_registry_v1 establishes dcse_cp.runtime_host_registry, dcse_cp.runtime_host_status, the Windows 11 primary registration, legacy-desktop HOLD_SECURITY candidate, enterprise-server PLANNED target, and DCS-WINDOWS-OLLAMA-01 host metadata.

A reusable host supervisor helper is provided for integration into the existing single scheduled poller cycle. It is not a standalone second poller.

## 12. Acceptance Criteria

Phase 1 is accepted only after: Windows 11 reports ONLINE; a non-Windows client can submit an ESCD turn; the existing scheduled Polar cycle detects pending work; the local worker starts or is confirmed alive; the worker claims and completes a real turn; evidence persists; History/Resume works from another client; offline requests remain REQUESTED/WAITING_HOST and execute after host return without resubmission; legacy desktop cannot execute while HOLD_SECURITY; planned server cannot execute while PLANNED; no credential is exposed; the permanent SC ESCD URL remains unchanged throughout host changes.

## 13. Scale Decision

Current posture: Windows 11 = approved on-demand primary. Legacy desktop = hardware candidate only under security hold. Enterprise server = preferred long-term 24/7 target.

LOCKED BY DCS — 2026-09-14