# Tribunal Topic Record: ChatGPT Usage, Resets, and Capacity Management

**Record date:** 2026-08-13  
**Lane:** DCSE / SYSTEM  
**Status:** OPERATING-CAPACITY DISCUSSION RECORD  
**Implementation authority:** NONE

## User-observed state

DCS reported that the visible weekly usage percentage appeared unchanged after substantial work and also reported receiving three usage-limit resets during the prior billing cycle, all of which were used.

A screenshot during the thread showed a weekly reset date/time and no currently available usage-limit resets.

## Distinction established in discussion

Two mechanisms were treated separately:

1. the normal recurring included usage allowance/reset cycle;
2. separately banked or promotional usage-limit resets where available.

The presence or absence of banked resets does not eliminate the normal recurring allowance reset.

## Caution

The visible usage percentage should not be assumed to update after every message or tool action.

An unchanged UI percentage is not proof that work is unmetered or free.

Possible causes discussed include delayed/batched UI refresh, different accounting buckets for different surfaces or reasoning modes, stale UI state, or tool activity represented differently from manually selected model allowance.

## Operating consequence

Do not manage DCSE workload solely by watching the percentage meter.

Instead:

- reserve high-value frontier reasoning for architecture, reconciliation, governance, and difficult review;
- offload bulk inspection and classification;
- use Gemini/Qwen/Antigravity/Codex according to task fit;
- use local Ollama for bounded workloads that fit proven hardware capacity;
- use CLI/scripts for deterministic work;
- preserve evidence so expensive work is not repeated.

## Capacity-routing rule

`DCS objective -> primary controller -> smallest sufficient context packet -> least expensive sufficient authorized execution surface -> evidence -> reconciliation`

## No unsupported claim rule

Do not claim exact remaining account usage unless the product UI exposes it, exact consumption for a tool call unless the provider exposes that accounting, or that a reset occurred unless account/provider evidence confirms it.

## Relationship to website modernization

Usage management is part of the architecture because the SC Digital Estate plan relies on multiple execution surfaces.

The objective is not merely to preserve tokens. It is to create a portable operating system in which premium reasoning is used where it materially improves decisions.