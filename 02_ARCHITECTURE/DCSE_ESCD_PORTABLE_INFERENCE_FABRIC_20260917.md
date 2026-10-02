# DCSE / ESCD Portable Inference Fabric

**Task ID:** DCSE-AI-PORTABLE-HARNESS-001  
**Date:** 2026-09-17  
**Lane:** DCSE / ESCD / Command Post  
**Status:** CANDIDATE ARCHITECTURE  
**Authority:** DCS-directed record and knowledge capture  
**Handoff ID:** DCSE-AI-PORTABLE-HARNESS-001-H01

## Purpose

Extend the existing DCSE hybrid/open-model architecture so the governed ESCD harness is separated from the physical machine performing inference. Consumer hardware limitations must not bind DCSE to one workstation, runtime, model, or provider.

This asset extends, rather than replaces, `DCSE_OPEN_MODEL_AND_VIDEO_PRODUCTION_ARCHITECTURE_20260713.md`, whose direction establishes provider independence and models/providers as replaceable production resources.

## Architecture Decision

ESCD owns orchestration and governance. Inference nodes are interchangeable execution resources. A governed request may execute on the primary Windows laptop, an Android/mobile device, an authorized temporary workstation, remote GPU infrastructure, or an approved hosted open-model provider.

Where practical, adapters should expose an OpenAI-compatible interface so consuming applications do not require machine-specific integration.

## Portable Inference Fabric

```text
ESCD
 └── Portable Inference Fabric
      ├── Node Discovery
      ├── Hardware Profiler
      ├── Model Registry
      ├── Runtime Adapter
      ├── Capability Router
      ├── OpenAI-Compatible Interface
      ├── Benchmark / Acceptance Suite
      ├── Ephemeral Node Mode
      └── Security / Cleanup Gate
```

Node Discovery identifies authorized execution nodes. Hardware Profiler records OS, CPU, RAM, GPU/accelerator, storage and practical model limits. Model Registry records model/version, source, license, quantization/checkpoint, requirements, capabilities, benchmarks, approved lanes and provenance. Runtime Adapter abstracts Ollama, llama.cpp-class runtimes, mobile runtimes, remote servers and hosted providers. Capability Router selects eligible execution based on task capability, privacy, context, quality, latency, cost and hardware availability. Acceptance testing validates compatibility, stability, resource consumption and governance controls.

## Execution Tiers

- **Tier 0 — Mobile:** appropriately sized quantized open-weight models for portable/offline/specialized inference.
- **Tier 1 — Primary Local:** normal DCSE workstation for models within practical hardware limits, RAG, embeddings, development and testing.
- **Tier 2 — Opportunistic/Ephemeral Compute:** an authorized alternate machine temporarily becomes a DCSE worker after profiling and acceptance testing.
- **Tier 3 — Remote GPU:** remote capacity executes workloads exceeding local hardware while ESCD retains routing, provenance and policy control.
- **Tier 4 — Hosted Open Models:** approved providers expose open-model families without DCSE operating inference hardware.

## Ephemeral Node Security Rule

School, library, shared, borrowed, or otherwise non-DCSE-owned machines are untrusted/ephemeral unless separately approved. Do not persist production credentials, private RAG corpora, protected enterprise data, API secrets, privileged browser sessions, service-role credentials, or protected-lane material.

Lifecycle:

```text
authorize
> hardware profile
> select compatible runtime/model
> initialize temporary node
> acceptance test
> execute permitted workload
> capture non-sensitive evidence
> terminate runtime
> remove transient data and credentials
> deregister node
```

Machine-owner and institutional policies remain authoritative. DCSE must not bypass administrative, security, installation, network, or acceptable-use restrictions.

## Portable Node Package Concept

```text
dcse-ai-node/
├── config/models.yaml
├── harness/
├── prompts/
├── tests/
├── scripts/
├── models/          # optional
└── start-node.*
```

The package contains configuration and validation logic, not embedded secrets.

## Required Evidence Per Execution

Record task/work ID, node identity/ownership class, hardware profile, runtime/version, model/checkpoint/quantization, routing rationale, acceptance status, execution status, relevant latency/resource observations, provenance/artifact references, and cleanup/deregistration evidence for ephemeral nodes.

## Preflight Validation

**VERIFIED:** Existing Command Post architecture establishes provider independence, Ollama's local-runtime role, model registry requirements, benchmark-driven routing, provenance, and DCSE ownership of workflow/production logic while models/providers remain replaceable resources.

**VERIFIED:** `02_ARCHITECTURE` is an existing repository architecture surface.

**UNKNOWN / TO VALIDATE:** Exact Android runtime/model compatibility for current mobile hardware; limits of specific alternate 8 GB machines; institutional permissions on school/library equipment; integration details with the current ESCD recovery/multi-provider implementation.

## Implementation Sequence

1. Reconcile this candidate with the current ESCD multi-provider recovery baseline.
2. Define a provider-neutral inference-node contract.
3. Implement hardware profiling and node capability registration.
4. Extend model registry for quantization, runtime compatibility and node eligibility.
5. Implement capability-based routing.
6. Define ephemeral-node security and cleanup verification.
7. Build a portable acceptance/smoke-test package.
8. Certify primary laptop as first node.
9. Certify one Android node if technically suitable.
10. Certify one authorized alternate PC and one remote/hosted provider.
11. Demonstrate the same governed ESCD request across interchangeable nodes.

## Exit Criteria

The architecture is implementation-ready when the same ESCD request can be routed without application rewrite to multiple approved execution targets, with each run recording model, runtime, node capability, routing rationale, result and evidence.

Production promotion requires security validation, current ESCD contract reconciliation, successful acceptance testing and DCS approval.

## Adversarial Review

Portability does not remove RAM, VRAM, thermal, storage, context, or performance constraints. An 8 GB PC or phone must not be represented as capable of efficiently running arbitrary large models. Temporary public/shared machines must not become trusted DCSE endpoints merely because the harness can execute there.

## Handoff

**Handoff ID:** DCSE-AI-PORTABLE-HARNESS-001-H01  
**Next owner:** ESCD / Command Post implementation lane  
**Next action:** reconcile with the active ESCD multi-provider baseline and produce the provider-neutral inference-node contract before implementation or OPERATIVE promotion.
