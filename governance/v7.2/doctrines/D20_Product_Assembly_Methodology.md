# DCSE Doctrine D20: Product Assembly Methodology

**Document ID:** DCSE-D20
**Version:** v7.2
**Effective Date:** 2026-09-10
**Status:** ACTIVE / OPERATIVE
**Approved By:** DCS Level 0
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D20_Product_Assembly_Methodology.md

## Purpose

D20 governs the end-to-end product assembly lifecycle across DCSE. It sequences intake, architecture, build, test, package, promote, deploy, and reuse capture. Existing source doctrines retain their specialized authority.

## 1. Reuse Before Redesign

Before designing, configuring, integrating, or implementing a product or technical capability, DCSE shall determine whether a previously validated architecture, component, integration, configuration pattern, workflow, or implementation satisfies all or part of the requirement.

Proven solutions shall be reused, duplicated, composed, or adapted when technically and operationally appropriate. Redesign or reconstruction from scratch requires material justification based on changed requirements, security, compatibility, scale, performance, maintainability, cost, governance, obsolescence, or demonstrated deficiency.

Successful implementation knowledge shall not be repeatedly rediscovered. Once a Vercel, Supabase, GitHub, API, MCP, plugin, connector, authentication, environment-variable, secrets/Vault, storage, CRUD, deployment, testing, rollback, or comparable technology pattern has been successfully implemented and validated, its reusable architecture and configuration requirements shall be captured so subsequent work can begin from that proven baseline.

Secret values, tokens, passwords, API keys, private keys, connection strings, recovery codes, and MFA data shall never be copied into reusable architecture records. Reuse records may capture secret names, roles, expected locations, injection mechanisms, access boundaries, rotation expectations, and validation procedures.

### 1.1 Mandatory Reuse Decision Gate

Every applicable build shall record one of the following dispositions before architecture or implementation proceeds:

- REUSE: use an existing validated solution substantially unchanged.
- ADAPT: reuse a validated solution with bounded modifications.
- COMPOSE: combine validated components or patterns from multiple prior solutions.
- REDESIGN: create a materially new solution only when reuse is insufficient and the reason is documented.

The decision record shall identify the prior implementation or pattern considered, evidence of its validated status, material differences in the current requirement, dependencies, compatibility constraints, and the reason for the selected disposition.

### 1.2 Proven Solution Capture

After successful validation, reusable implementation knowledge shall be externalized into a governed reusable-pattern registry or equivalent controlled record. At minimum the record shall include:

- pattern or architecture identifier
- purpose and supported use cases
- source implementation and provenance
- validation evidence
- technology and provider dependencies
- environment-variable names or roles, without secret values
- required Supabase schemas, RLS, RPC/API, Storage, Vault, or database dependencies where applicable
- hosting/deployment configuration where applicable
- MCP, plugin, connector, or API dependencies where applicable
- version and compatibility information
- known constraints and failure modes
- rollback or recovery considerations
- security and access boundaries
- last validated date and validation source

A successful build that introduces a new reusable pattern shall feed that pattern back into the registry after validation.

## 2. Product Assembly Lifecycle

D20 uses the following sequence:

1. Intake
2. Search Proven Solutions
3. Reuse / Adapt / Compose / Redesign Decision
4. Architecture
5. Build
6. Test
7. Capture or Update Reusable Pattern
8. Package
9. Promote
10. Deploy
11. Production Verification and Feedback

### 2.1 Intake

Define the product, entity, audience, requirements, destination, security posture, integrations, dependencies, and applicable doctrine routing before implementation begins.

### 2.2 Search Proven Solutions

Search governed DCSE architecture records, prior products, code, deployment receipts, GitHub history, Supabase registries, integration records, and validated technology patterns for reusable capability before creating a new design.

### 2.3 Architecture and Build

Prefer composable, reusable components. Preserve validated data contracts, backend boundaries, RLS patterns, environment-variable conventions, secrets handling, deployment patterns, and tested integration approaches unless a documented requirement justifies change.

### 2.4 Test

Validate functionality, browser behavior when applicable, responsive behavior, accessibility targets, security boundaries, secrets isolation, database/RLS behavior, integration behavior, failure states, and rollback/recovery. A code-complete state is not equivalent to validated completion.

### 2.5 Package, Promote, and Deploy

Package governed artifacts, dependencies, evidence, checksums, and rollback information. Promotion authority remains governed separately from ordinary build activity. Deployment does not supersede required validation.

### 2.6 Reuse Feedback Loop

A successfully validated implementation shall be evaluated for reusable value. Reusable portions shall be registered so future work can locate and leverage them without repeating discovery, configuration, or debugging already resolved by prior validated work.

## 3. Enterprise Scope

This doctrine applies across DCSE product and technical implementation surfaces, including but not limited to Vercel, Supabase, GitHub, APIs, MCP services, plugins, connectors, authentication, environment variables, secrets/Vault mechanisms, database schemas, RLS, Storage, CRUD, file handling, RAG, model/provider integrations, testing, deployment, monitoring, rollback, and future technologies.

## 4. Authority and Effective Status

This v7.2 D20 amendment was explicitly approved, confirmed, promoted, and activated by DCS Level 0 on 2026-09-10. No further substantive approval is required for its operative status. Remaining repository, registry, Supabase, receipt, and distribution updates are synchronization and evidence activities, not approval gates.

**Operative principle:** Reuse proven architecture by default. Redesign only when material evidence justifies the change.
