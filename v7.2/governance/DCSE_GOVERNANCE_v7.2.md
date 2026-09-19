# DCSE Operational Governance Framework (v7.2)

## 1. Constitutional Foundations
The DCSE Command Center operates under constitutional authority established by DCS and operational direction from SC.
All actions taken by human engineers, autonomous agents, and pollers must comply with the Master Profile v7.2 rules.

## 2. Core Operational Doctrines

### 2.1 Zero Manual Tasks Mandate
Engineering integrations, deployments, monitoring, and state reconciliations must be fully scripted, parameterized, and executable via CLI. Manual interventions are limited strictly to constitutional approvals and irreversible production cutovers.

### 2.2 Neutral Universal Dispatch Controller
1. The neutral `DCSE_DispatchController` is the single active dispatch authority on this host, running on a 60-second cycle.
2. Legacy pollers (`DCSE_ClaudeCode_Poller`, `DCSE_PollerHealthMonitor`) are classified `ROLLBACK_ONLY` and must remain `Disabled`.
3. Workers cycle under their own non-blocking mutex locks. Message delivery runs under a distinct lock from task execution to prevent message delivery stalls.

### 2.3 Fail-Closed Security & Credential Isolation
1. No service-role keys, private tokens, or secrets may ever be written to plaintext files, logs, commit trees, or UI response bodies.
2. Host credentials must be accessed exclusively through DPAPI-protected CLIXML bundles located in `C:\ProgramData\DCSE\secrets\`.
3. Supabase REST API requests must supply appropriate schema headers (`Accept-Profile: dcse_cp`, `Content-Profile: dcse_cp`).

### 2.4 Incident Remediation Loop
Every runtime defect must follow the standardized loop:
`DETECT -> DIAGNOSE -> REMEDIATE -> FORWARD-TEST -> RECORD EVIDENCE -> RESUME CADENCE`

### 2.5 Multi-Agent Consensus & Open-Source Orchestration
1. Multi-agent communications pass through the Supabase `dcse_cp.agent_messages` bus.
2. Each agent acknowledgment and reply must preserve correlation IDs and round attribution.
3. Open-source models (Qwen, DeepSeek, Hermes via Ollama/LiteLLM) operate as registered execution engines subject to the same Stop-Gate and receipting governance.

### 2.6 Instruction File Governance & Harmonization (AGENTS.md, CLAUDE.md, and v7.2)
1. **Single Source of Truth for Agent Rules**: Operational directives, model switching, and automated execution constraints SHALL be maintained canonically in `AGENTS.md` to prevent split-brain drift. Tool-specific files like `GEMINI.md` act as aliases.
2. **Harmonization with Authorized Contracts**: Files such as `CLAUDE.md` are human/leadership-authored foundational specifications (authored by sonlyconsulting-ctrl). They define immutable core requirements:
   - Input validation before DB access
   - Zero plaintext secret leakage
   - Single-file Vercel serverless architecture (`apps/sc-agent-os/api/index.js`)
   - The 10-point validation test matrix
3. **Integration Relationship**: v7.2 does NOT discard or unilaterally override authorized specifications. Rather, v7.2 provides the **operational orchestration harness** (Universal Dispatch Controller, message bus, open-source model routing, and CLI toolchain) that serves, automates, and verifies compliance with those core requirements. Any behavioral divergence must be authorized by explicit DCS directives.

### 2.7 Pre-v7.2 Intake, Quarantine & Promotion Protocol
When a pre-v7.2 artifact (script, scheduled task, database payload, or branch) is encountered:
1. **Safety First (Fail-Closed)**:
   - A pre-v7.2 artifact SHALL NOT be executed blindly under assumptions of v7.2 compliance.
   - Legacy pollers and unverified worker tasks default to `ROLLBACK_ONLY` and remain disabled.
2. **Handling by Classification**:
   - **Operational Scripts (PowerShell / Python / Node)**: If an active dependency resides in a pre-v7.2 path (e.g. `v7.0/09_WORKERS`), it must be promoted into `v7.2/` with updated paths, leaving the pre-v7.2 file untouched as a historical rollback baseline.
   - **Database Tasks & Payloads (`dcse_cp`)**: If a task payload from a pre-v7.2 schema is claimed, the worker validates required fields. Missing fields trigger a truthful `blocked` result and an evidence receipt to DCS Queue rather than an unhandled crash.
   - **Scheduled Tasks / Host Services**: Any active scheduled task pointing to pre-v7.2 directories is detected by `dcse audit` and re-anchored to the corresponding `v7.2/` launcher.
   - **Documentation & Specifications**: Historical specs in `01_GOVERNANCE/`, `02_ARCHITECTURE/`, and `v7.0/` are preserved as baseline truth. When referenced, they are harmonized and modernized under the v7.2 Evolution Cadence.
3. **Audit Trail**:
   - Every discovery and promotion of a pre-v7.2 item must be logged with SHA-256 evidence in the conversation log or `_Tribunal_Inbox`.

### 2.8 Regression Prevention & Revert Proscription
1. **No Panic Rollbacks**: Wholesale rollbacks or reverts of feature branches (e.g. deleting multimodal UI, authentication integrations, or schema adapters) are strictly PROHIBITED without prior root-cause classification and DCS Level 0 approval.
2. **Isolate Configuration from Code**: When an integration failure occurs in a Vercel preview or branch environment, agents and engineers MUST inspect environment variables, redirect URIs, and database schema before touching application code. Code that functions locally must not be reverted due to cloud configuration asymmetry.

### 2.9 Vercel Preview & Production Parity Contract
1. **Universal Variable Parity**: All environment variables required by serverless functions (including `DDNA_SUPABASE_URL`, `DDNA_SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and `NEXT_PUBLIC_SUPABASE_URL`) MUST be configured across both `Production` and `Preview` environments in Vercel.
2. **Preview Redirect Handling**: Authentication redirects MUST accommodate dynamic Vercel preview hostnames (`https://sc-command-post-*.vercel.app`) using wildcard URI registration or canonical auth proxying to prevent `redirect_uri_mismatch` errors.

### 2.10 Migration Single Source of Truth & Concurrency Gate
1. **Single Authoritative Migration Store**: All database DDL migrations must be versioned and committed under `supabase/migrations/` in the authoritative git repository.
2. **No Ad-Hoc Unversioned DDL**: Executing schema changes directly via Supabase Studio or manual SQL editors without a matching versioned migration file committed to Git is prohibited.
3. **Pre-Flight Schema Audit**: Before any deployment or PR promotion, `dcse audit` must run to verify that local migration definitions align with the active Supabase instance.

### 2.11 Deterministic Mechanical Gate Doctrine (Zero-Unverified-Action)
1. **Mechanical Enforcement Over Conversational Memory**: Agents (Antigravity, Codex, Cowork, etc.) SHALL NOT be trusted based on conversational context, natural-language promises, or associative memory alone. Trust is established strictly through deterministic, fail-closed mechanical gates (e.g., git pre-push verification hooks, schema validation linters, and canonical file lookups).
2. **Mandatory Canonical Grounding**: Before proposing any product feature, architecture, entity definition, or deployment target, an agent MUST execute the **Doctrine Preflight Checklist** (§3):
   - Exhaust local and remote canonical repositories (Rule ER-001) before assuming absence or fabricating terms.
   - Ground every acronym and entity in the Master Profile (`DCSE_MASTER_PROFILE_v7_2_R5_OPERATIVE.md`) and D01–D22 source doctrines.
   - Resolve identities deterministically: `CTJ` = Critical Thinker's Journey; `CF` = Conversation Flow; `DDNA` = DCSE DNA (D16); `TSL` = The Sports Lane; `ESCD` = Enterprise Supervisory Control Dashboard.
3. **No Uncited Architecture Claims**: Any agent claim or proposal lacking an explicit citation to a canonical file path, line number, or Task ID fails closed and is classified `UNVERIFIED`.

## 3. Doctrine Preflight Checklist (Mandatory for All Agent Actions)

Before any agent formulates an architectural proposal, executes an automated task, or outputs an integration plan, the following checklist MUST be mechanically satisfied:

- [ ] **1. Canonical Identity & Semantic Resolution Check (Rule ER-002)**  
  Verify all product names, acronyms, and aliases against `DCSE_MASTER_PROFILE_v7_2_R5_OPERATIVE.md` and D01–D22 source doctrines. Zero associative guessing.
- [ ] **2. Canonical File Path & Line Citation Check (Rule ER-001)**  
  Cite the exact repository file path, section, or line number for every architectural dependency and product requirement.
- [ ] **3. Tri-Separation Verification (D16 §3 / D22)**  
  Explicitly distinguish between:
  a) **Source Artifact** (canonical code/text in Git),
  b) **Structured DDNA / Semantic Memory** (distilled knowledge in Supabase), and
  c) **Authority State** (DCS Level 0 decision/directive).
- [ ] **4. Fail-Closed State Machine Classification (Rule ER-003)**  
  Items not immediately found in context must be classified `UNKNOWN` $\rightarrow$ `SEARCHED_NOT_FOUND` $\rightarrow$ `VERIFIED_ABSENT`. Never treat conversational absence as nonexistence.
- [ ] **5. Mechanical Gate Pre-Flight Pass**  
  Automated tests, pre-push safety hooks, and linter gates must pass with machine receipts prior to claiming completion or deployment readiness.

