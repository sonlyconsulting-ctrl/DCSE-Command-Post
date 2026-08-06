# DCSE V7.1 Universal Agent Onboarding and Access Standard

Status: IMMEDIATE CONTROLLED USE
Authority: DCS
Applies to: every newly approved or existing model, agent, worker, coding sandbox, desktop agent, cloud agent, reviewer, and automation participating in DCSE work
Confidentiality: INTERNAL

## 1. Purpose

Ensure every approved participant can accurately locate, access, reconcile, and report from GitHub and Supabase without false absence findings, secret exposure, lane leakage, or dependence on one model vendor.

No participant may begin substantive DCSE work until the onboarding gate is completed or an explicit DCS exception is recorded.

## 2. Canonical systems

GitHub repository:
`sonlyconsulting-ctrl/DCSE-Command-Post`

V7.1 branch:
`governance/v7.1-owned-product-harness`

V7.1 pull request:
`#29`

Governance registry:
`DCSE-DDNA`
Project ID: `uutpzaiqymyufljdgdaa`

Operations registry:
`SC-Command-Post`
Project ID: `nevgdyfpxdaloacuutal`

## 3. Required access methods

### GitHub

Approved methods:

1. Authenticated GitHub connector or GitHub App
2. GitHub CLI authenticated through `gh auth login`
3. Git remote authenticated through an approved credential helper, token broker, or SSH configuration

General web search is not an authoritative GitHub inventory method.

### Supabase

Approved methods:

1. Supabase MCP authenticated through OAuth
2. Governed DCSE Control Plane API or Supabase Edge Function
3. Approved local credential broker
4. Publishable client access limited by RLS, only when the required read is intentionally exposed

Prohibited:

- placing a service-role key in a prompt
- placing a service-role key in a model-visible workspace
- committing secrets to GitHub
- using browser-side privileged keys
- treating absence of raw credentials as proof that Supabase access is unavailable

## 4. Mandatory onboarding sequence

Every participant must perform these steps before substantive work.

### Gate A: Identity and lane

Record:

- participant name and model
- execution environment
- assigned role
- authorized lane
- prohibited lanes
- confidentiality ceiling
- task type

PS access is denied unless separately and expressly authorized.

### Gate B: GitHub bootstrap

1. Resolve repository by exact full name.
2. Verify authentication.
3. Verify repository visibility and permissions.
4. Verify default branch.
5. Verify canonical V7.1 branch.
6. Verify PR #29.
7. Verify required governance files.
8. If operating locally, verify `git remote -v`, fetched refs, current branch, current commit, and shallow or grafted history.

### Gate C: Supabase bootstrap

1. Discover Supabase MCP or the governed Control Plane interface.
2. Authenticate through OAuth or the approved broker.
3. List accessible projects.
4. Verify DCSE-DDNA by name and project ID.
5. Verify SC-Command-Post by name and project ID.
6. Execute one safe read against each applicable project.
7. Record the access method. Do not record secrets.

### Gate D: Authority and operations reconciliation

For governance, architecture, research, promotion, or enterprise-memory tasks:

`DCSE-DDNA -> GitHub -> SC-Command-Post`

For runtime, worker, product-operation, or execution tasks:

`SC-Command-Post -> GitHub -> DCSE-DDNA`

For GitHub branch, PR, issue, code, or review tasks:

`GitHub -> applicable Supabase project -> second Supabase project when material`

### Gate E: Startup acknowledgment

The participant must output or record:

```text
PARTICIPANT: <name/model>
ROLE: <assigned role>
LANE: <authorized lane>
GITHUB AUTHENTICATED: YES/NO
REPOSITORY VERIFIED: YES/NO
CANONICAL BRANCH VERIFIED: YES/NO
PR #29 VERIFIED: YES/NO
DCSE-DDNA VERIFIED: YES/NO/NOT APPLICABLE
SC-COMMAND-POST VERIFIED: YES/NO/NOT APPLICABLE
LOCAL WORKSPACE: CONNECTED/LOCAL-ONLY/NOT USED
ACCESS METHOD: CONNECTOR/MCP/CLI/BROKER/CONTROL-PLANE
SECRETS EXPOSED: NO
LIMITATIONS: <none or exact limitation>
```

Substantive work may begin only after this acknowledgment passes.

## 5. Negative finding control

A negative finding must name the exact evidence surface queried.

Permitted:

- `No exact branch named v7.1 was found. The canonical branch is governance/v7.1-owned-product-harness.`
- `No V7.1 record was found in SC-Command-Post. DCSE-DDNA was not inspected.`
- `No V7.1 marker was found in the local workspace. The live repository was not connected.`

Prohibited:

- `V7.1 does not exist` after a partial search
- `No issues exist` after only branch search
- `Supabase is unavailable` merely because no service-role key is present
- `The repository is private` without repository metadata verification

## 6. Automatic participant packet

Every governed task compiler, relay, or orchestrator should attach this packet:

```yaml
participant_contract: DCSE_V7_1_UNIVERSAL_AGENT_ONBOARDING
repository: sonlyconsulting-ctrl/DCSE-Command-Post
canonical_branch: governance/v7.1-owned-product-harness
canonical_pr: 29
governance_path: governance/v7.1/
supabase:
  governance:
    name: DCSE-DDNA
    project_id: uutpzaiqymyufljdgdaa
    access_priority: governance_first
  operations:
    name: SC-Command-Post
    project_id: nevgdyfpxdaloacuutal
    access_priority: operations_first
required_access:
  github_authenticated: true
  supabase_mcp_or_control_plane: true
  service_role_to_model: false
required_checks:
  - repository_metadata
  - branches
  - pull_requests
  - issues
  - files
  - governance_registry
  - operations_registry
negative_finding_policy: scoped_only
startup_ack_required: true
```

## 7. Coder operating profile

Coder is approved as a prime candidate for high-volume bounded work because of availability and usage economics.

Preferred assignments:

- repository inventory
- migration and schema inspection
- test generation
- build-plan decomposition
- route and component audits
- evidence-manifest generation
- bounded refactors
- deterministic code tasks
- GitHub and Supabase reconciliation
- issue and PR preparation

Coder restrictions:

- no promotion authority
- no secret handling in prompts
- no unreviewed production deployment
- no destructive database change without an approved task
- no PS lane access absent express authorization
- no enterprise-wide negative conclusion from a local-only workspace

Coder output must be reviewed according to task risk. Planner, Builder, Verifier separation remains required for material product changes.

## 8. Existing-agent re-onboarding

Every existing participant must complete this standard at the next governed task or before receiving additional authority, whichever occurs first.

Prior successful access does not establish current access. Authentication, branch state, project access, and execution environment must be revalidated.

## 9. Failure handling

If GitHub authentication fails:

1. report the exact failure;
2. attempt approved connector or CLI authentication;
3. do not substitute public search;
4. stop before repository-wide conclusions.

If Supabase access fails:

1. discover MCP and Control Plane options;
2. attempt OAuth authentication;
3. report the exact project and interface tested;
4. do not request or expose a service-role key;
5. continue only with the evidence surfaces actually available.

## 10. Completion standard

A participant is onboarding-complete only when:

1. identity, role, lane, and confidentiality are recorded;
2. authenticated GitHub is verified;
3. the canonical branch and PR are verified;
4. the applicable Supabase projects are verified through approved access;
5. one safe read succeeds on each applicable project;
6. the startup acknowledgment is recorded;
7. no secret is exposed;
8. negative findings are scoped;
9. the participant accepts DCS promotion authority and Stop-Gates.

## 11. Current status

Operational use: AUTHORIZED IMMEDIATELY
Enterprise promotion: PENDING DCS RATIFICATION WITH V7.1
Automatic packet attachment: REQUIRED BUILD ITEM
Coder classification: PRIME BOUNDED-EXECUTION CANDIDATE
