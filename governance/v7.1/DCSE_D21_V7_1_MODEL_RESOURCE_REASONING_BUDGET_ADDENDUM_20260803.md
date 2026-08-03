# DCSE D21 V7.1 Model Resource and Reasoning Budget Addendum

Date: 2026-08-03
Authority: DCS
Parent doctrine: D21 Doctrine Runtime Engine
Supporting doctrine: D03 AI Orchestration
Status: ACTIVE FOR V7.1 RERUNS

## Purpose

This addendum makes model availability, token consumption, reasoning effort, fallback, and reserve management executable runtime controls.

Model usage is a governed resource. A named model's unavailability or quota pressure is a routing event, not a routine Stop-Gate.

## Mandatory preflight

Before task admission, the orchestrator records:

1. provider and exact model;
2. authentication mode;
3. reported remaining usage or budget;
4. reset date when verified;
5. reasoning effort;
6. maximum turns or bounded work units;
7. context-reuse plan;
8. minimum reserve;
9. fallback model and capability limits;
10. actual usage and completion disposition.

Unverified quota-reset dates are recorded as UNKNOWN and cannot drive scheduling.

## Reasoning levels

| Level | Authorized work |
|---|---|
| LOW | file enumeration, status reads, deterministic checks, formatting, hashing, receipt construction, known-command execution |
| MEDIUM | standard implementation, repository analysis, test diagnosis, cross-file reconciliation, routine audit synthesis |
| HIGH | security, RLS, authentication, architecture conflict, data-integrity disputes, rollback design, independent review of material findings |
| XHIGH or MAX | exceptional unresolved critical-risk analysis only; requires measured quality need and resource check |

No runtime may select high effort for all phases merely because the product is complex.

## BOW-003R allocation

### Claude Code with Claude Sonnet 4.6

| Phase | Effort |
|---|---|
| admission, file inventory and evidence collection | LOW |
| nine-category audit and test interpretation | MEDIUM |
| security, RLS, authorization, sports-data integrity conflicts | HIGH |
| report assembly and receipt formatting | LOW |
| final production-readiness synthesis | HIGH only when material conflicts remain; otherwise MEDIUM |

Controls:

- use bounded prompts by audit category;
- reuse a stable session when context remains valid;
- avoid rereading unchanged large files;
- cap unattended turns and emit partial receipts before retry;
- record actual cost or usage when the runtime exposes it.

### Codex

User-reported availability at admission: 53 percent.
Verification timestamp: 2026-08-03.
Verified reset date: 2026-08-08.

Codex allocation:

- bulk inventory and first-pass audit: NOT ASSIGNED;
- independent technical review: MEDIUM default;
- critical security, RLS, authorization, architecture, or evidence dispute: HIGH;
- GitHub and Supabase reconciliation: LOW;
- reserve floor after BOW-003R review: 35 percent where platform metering permits;
- conservation warning: 40 percent remaining;
- fallback below reserve: preserve Codex for final disposition and route bounded retests to another admitted runtime.

The user-reported 53 percent and August 8, 2026 reset date are DCS planning inputs. Provider-side metering remains authoritative when available.

## Rerun portfolio allocation

| BOW | Primary workload | Default effort | High-effort trigger |
|---|---|---|---|
| BOW-001R | poller and recovery | MEDIUM | concurrency, credential, recovery or integrity failure |
| BOW-002R | CTJ audit | MEDIUM | source conflict, architecture or commercial-risk dispute |
| BOW-003R | TSL production audit | MEDIUM | security, RLS, auth, sports-data integrity or critical architecture |
| BOW-004R | CTJ remediation planning | MEDIUM | destructive migration, rollback, production or material architecture decision |

## Routing hierarchy

1. Use deterministic scripts and database queries before model reasoning.
2. Use low effort for mechanical evidence production.
3. Use medium effort as the normal execution setting.
4. Escalate individual findings to high effort, not the entire task.
5. Preserve premium-model capacity for independent review and unresolved material risk.
6. Fall back by capability when quota, authentication, or availability changes.
7. Never accept a lower-capability runtime's operational claim without tool evidence.

## Pass conditions

A resource-management receipt passes only when it records:

- planned provider, model, and effort;
- actual provider and model used;
- phase-level effort changes;
- actual or unavailable usage metrics;
- retries and fallback events;
- reserve status;
- effect on evidence quality;
- next-task capacity.

## Stop conditions

Resource conditions stop execution only when:

- no admitted runtime can perform a required capability;
- remaining budget is below the protected reserve and no fallback exists;
- authentication failure prevents all eligible runtimes;
- degraded capacity would make required security or integrity validation unreliable.

Otherwise, the router continues with a capable fallback and records the change.

## Controlling rule

The cheapest adequate reasoning level governs. High effort is reserved for measured complexity, material risk, or unresolved conflict. Model prestige and product importance alone do not justify maximum reasoning expenditure.
