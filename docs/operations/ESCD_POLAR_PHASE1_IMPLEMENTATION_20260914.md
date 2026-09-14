# ESCD + Polar Phase 1 Implementation Plan

Plan ID: DCSE-ESCD-POLAR-PH1-20260914
Status: ACTIVE IMPLEMENTATION / DCS APPROVED
Authority: DCS Level 0

## Goal

Make ESCD remotely usable while preserving host-dependent Polar execution and a clean scale path from on-demand Windows 11 to enterprise 24/7 service.

## Phase 1A — Permanent Access

Canonical production URL target: escd.sonlyconsulting.com
QA target: escd-qa.sonlyconsulting.com

The SC-owned domain is the human-facing contract. Vercel/Netlify deployment URLs are implementation evidence only.

## Phase 1B — Host Registry

Applied production migration: polar_runtime_host_registry_v1

Registered:
- DCS-WIN11-PRIMARY — VERIFIED / ON_DEMAND / eligible
- DCS-WIN8-SECONDARY-CANDIDATE — HOLD_SECURITY / disabled
- DCSE-POLAR-SERVER-01 — PLANNED / disabled

Runtime status is available from dcse_cp.runtime_host_status.

## Phase 1C — Existing Poller Integration

Do not create another scheduler or second poller.

Integrate tribunal/v7/runtime-evidence/escd_polar_host_supervisor.ps1 into the existing DCSE_ClaudeCode_Poller cycle after credentials and heartbeats are established.

Operational call:

. (Join-Path $PSScriptRoot 'escd_polar_host_supervisor.ps1')
$polar = Invoke-EscdPolarHostSupervisor -SupabaseUrl $SupabaseUrl -ServiceKey $ServiceKey -WorkspacePath $WorkspacePath
Write-Log ('POLAR ESCD: ' + ($polar | ConvertTo-Json -Compress))

The helper never logs or returns the Supabase service-role credential.

## Phase 1D — On-Demand Local Worker

Default mode: ON_DEMAND
Worker: DCS-WINDOWS-OLLAMA-01
Worker script: apps/escd/runtime/ollama_worker.py

Behavior:
1. Verify current host is registered and eligible.
2. Inspect durable ESCD REQUESTED turns.
3. If none exist, do nothing.
4. If work exists, confirm local Ollama availability.
5. Start Ollama only when needed if available.
6. Ensure no duplicate ESCD worker process is active.
7. Start the existing ESCD worker with --once.
8. Let the worker use the current atomic claim/lease contract.

## Phase 1E — Remote/Mobile Acceptance

Test from phone/mobile:
1. Open permanent ESCD URL.
2. Authenticate.
3. Submit safe Orchestrate request.
4. Verify the turn persists.
5. Verify Windows 11 host ONLINE.
6. Verify Polar cycle starts or observes worker.
7. Verify worker claim.
8. Verify result.
9. Close browser.
10. Reopen from another client and verify History/Resume.

Then turn Windows 11 off and repeat:
- request persists;
- effective UI shows WAITING_HOST;
- no provider failure is fabricated;
- return Windows 11 to service;
- next Polar cycle processes the same request without resubmission.

## Phase 1F — Secondary Host Decision

Legacy desktop cannot be enabled while on legacy unsupported Windows.

Options:
- upgrade to supported Windows;
- install supported Linux;
- retire as an execution host.

After OS remediation, run host certification before changing security_state to VERIFIED or enabling execution/dispatch eligibility.

## Phase 1G — Enterprise 24/7 Target

Evaluate local mini/server PC, managed VM, and cloud VM against uptime, monthly cost, CPU/RAM/storage, local-model needs, security, remote management, backup/recovery, monitoring, and provider portability.

The enterprise server should eventually hold higher routing priority than personal workstations for suitable workloads.

## Stop Gates

STOP if: exposed Supabase server credential has not been rotated; host is not registered; host security state is not VERIFIED; local worker path is missing; required model/runtime is unavailable; operation cannot be atomically claimed; result cannot be persisted; host identity or heartbeat is ambiguous.

## Required Handoff Evidence

Return host-status snapshot, Task Scheduler status, Polar cycle log, worker heartbeat, operation turn key, claim evidence, provider/model evidence, result/evidence refs, mobile close/reopen proof, offline queue/recovery proof, and unresolved findings.