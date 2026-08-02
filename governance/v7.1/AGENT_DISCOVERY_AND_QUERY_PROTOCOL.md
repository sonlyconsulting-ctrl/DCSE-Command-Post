# DCSE V7.1 Agent Discovery and Query Protocol

Status: DRAFT CONTROL FOR PR #29
Authority: DCS
Applies to: ChatGPT, Claude, Codex, Qwen, Copilot, local workers, cloud sandboxes, and future approved agents

## 1. Purpose

Prevent false `not found` conclusions caused by general web search, an unconfigured local checkout, one Supabase project, stale code indexes, exact-name matching, or unauthorized credential requests.

A negative result is valid only for the evidence surface actually queried.

## 2. Canonical V7.1 Identifiers

Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`

Canonical branch: `governance/v7.1-owned-product-harness`

Canonical pull request: `#29`

Canonical document path: `governance/v7.1/`

Governance registry project: `DCSE-DDNA` (`uutpzaiqymyufljdgdaa`)

Operational Command Post project: `SC-Command-Post` (`nevgdyfpxdaloacuutal`)

There is no requirement for a branch named exactly `v7.1`. The canonical branch contains the version identifier and descriptive scope. Do not create an alias branch solely to satisfy an exact-name query.

## 3. Access Bootstrap

### 3.1 GitHub

A governed worker must use one of these access modes, in order of preference:

1. authenticated GitHub connector or MCP;
2. authenticated GitHub CLI using `gh auth status`;
3. configured Git remote with fetched origin refs.

For a local workspace, verify:

```bash
git remote -v
git fetch --all --prune
git branch -a
git status --short --branch
```

If no remote exists, configure the canonical repository only through an authenticated environment:

```bash
git remote add origin https://github.com/sonlyconsulting-ctrl/DCSE-Command-Post.git
git fetch origin --prune
git switch --track origin/governance/v7.1-owned-product-harness
```

Do not place GitHub tokens in prompts, files, issue bodies, logs, or command history.

### 3.2 Supabase

A governed model or sandbox must not request or receive a Supabase `service_role` key merely to inspect governance or operations data.

Permitted access modes, in order of preference:

1. authenticated Supabase MCP using OAuth and project-scoped tools;
2. governed Control Plane API or Edge Function with JWT verification and narrow operations;
3. approved local credential broker that does not disclose the credential to the model;
4. publishable or anonymous client access only where RLS expressly permits the required read.

Prohibited:

- pasting a service-role key into chat;
- placing a service-role key in a cloud sandbox environment for model access;
- committing keys to GitHub;
- exposing keys through browser code, logs, screenshots, task payloads, or database records;
- treating absence of raw API credentials as proof that Supabase cannot be queried when MCP or the Control Plane is available.

If Supabase tools are unavailable, report `SUPABASE ACCESS UNAVAILABLE IN THIS EXECUTION SURFACE`. Do not ask DCS to provide a service-role key to the model.

## 4. Mandatory Order of Operations

### Step 0: Resolve the task and lane

Record:

- requested subject or identifier
- repository or product scope
- lane
- confidentiality
- whether the task is governance, operational execution, product work, or research

Stop if the lane cannot be resolved safely.

### Step 1: Load the canonical discovery manifest

Read this protocol and the current governance reference record before searching broadly.

Use the canonical identifiers above unless a promoted successor explicitly supersedes them.

### Step 2: Verify authenticated GitHub repository access

Query the repository directly by full name. Confirm:

- repository identity
- visibility
- permissions
- default branch
- authenticated access status

Do not use public web search as the primary repository-discovery method.

### Step 3: Query GitHub surfaces separately

Search each required surface independently:

1. branches, using partial and exact terms
2. pull requests, open and closed
3. issues, open and closed
4. repository files and paths
5. commits and tags, when version history is material
6. review comments and review threads, when review state is material

Searching only branches does not establish absence from pull requests, issues, files, commits, tags, or Supabase.

### Step 4: Select the Supabase starting project by task class

For governance, architecture, research, promotion, project plans, or enterprise memory, start with `DCSE-DDNA`.

For runtime, worker state, assignments, task events, heartbeats, product operations, or execution receipts, start with `SC-Command-Post`.

For mixed questions, query both.

### Step 5: Query the second Supabase project when reconciliation is material

Governance and product-factory work normally requires comparison of:

- GitHub branch, PR, issue, and file state;
- DCSE-DDNA governance and memory records;
- SC-Command-Post operational tasks and activity.

Do not treat one system as a complete substitute for the others.

### Step 6: Inspect local workspace only as an execution surface

A local workspace is authoritative only for its checked-out commit and files.

Before drawing repository-wide conclusions, verify:

- `git remote -v`
- current branch
- fetched remote refs
- current commit
- shallow or grafted history

If no remote is configured, label every conclusion `LOCAL WORKSPACE ONLY`.

### Step 7: Report evidence coverage

Every review or search result must state:

- GitHub repository verified: YES or NO
- GitHub branches queried: YES or NO
- GitHub PRs queried: YES or NO
- GitHub issues queried: YES or NO
- GitHub files queried: YES or NO
- DCSE-DDNA queried: YES or NO
- SC-Command-Post queried: YES or NO
- Supabase access mode used
- local workspace status
- authentication status
- unresolved access limitations

## 5. Negative-Finding Rule

Permitted language:

- `No exact branch named v7.1 was found. The canonical V7.1 branch is governance/v7.1-owned-product-harness.`
- `No V7.1 record was found in SC-Command-Post. DCSE-DDNA was not inspected.`
- `No V7.1 marker was found in the isolated local workspace. The live repository was not connected.`
- `Supabase MCP was unavailable in this execution surface. Supabase was not inspected.`

Prohibited language:

- `V7.1 does not exist` when only one evidence surface was searched.
- `The repository is private` without repository metadata verification.
- `No issues or PRs exist` when only branch or code search was used.
- `No GitHub material exists` when the local checkout has no remote.
- `Supabase requires a service-role key` when MCP, a governed API, or a credential broker has not been checked.

## 6. Automatic Discovery Manifest

Every governed agent task should include or retrieve this manifest:

```yaml
repository: sonlyconsulting-ctrl/DCSE-Command-Post
canonical_branch: governance/v7.1-owned-product-harness
canonical_pr: 29
governance_path: governance/v7.1/
supabase:
  governance:
    name: DCSE-DDNA
    project_id: uutpzaiqymyufljdgdaa
  operations:
    name: SC-Command-Post
    project_id: nevgdyfpxdaloacuutal
access_policy:
  github:
    preferred: authenticated_connector_or_mcp
    fallback: authenticated_gh_cli_or_configured_remote
  supabase:
    preferred: oauth_mcp
    fallback: governed_control_plane_api_or_credential_broker
    service_role_to_model: prohibited
required_surfaces:
  - github_repository
  - github_branches
  - github_pull_requests
  - github_issues
  - github_files
  - supabase_governance
  - supabase_operations
negative_finding_policy: scoped_only
```

The relay or task compiler should attach this manifest automatically for V7.1 tasks.

## 7. Automatic Routing Rule

- Governance, architecture, research, promotion, and enterprise-memory questions start in `DCSE-DDNA`, then reconcile to authenticated GitHub, then check `SC-Command-Post` for execution state.
- Runtime, worker, product-operation, and task-execution questions start in `SC-Command-Post`, then reconcile to authenticated GitHub, then check `DCSE-DDNA` for authority.
- GitHub PR, issue, branch, or code-review questions start in authenticated GitHub, then reconcile to the applicable Supabase registry.
- Local workspace questions start locally, but no enterprise-wide conclusion is permitted until authenticated GitHub and the applicable Supabase project are checked.

## 8. Automatic Startup Self-Test

Before a governed worker begins a V7.1 task, it should run or request these checks:

1. Resolve the canonical repository.
2. Confirm authenticated GitHub access.
3. Confirm the canonical branch or PR exists.
4. Confirm the required governance path is readable.
5. Discover available Supabase tools.
6. Verify access to both named projects through MCP or the governed API.
7. Record the evidence-coverage manifest.
8. Stop with a scoped access error if any required surface is unavailable.

A successful startup acknowledgment should state:

```text
GITHUB: AUTHENTICATED
REPOSITORY: VERIFIED
CANONICAL BRANCH: VERIFIED
PR #29: VERIFIED
DCSE-DDNA: VERIFIED OR NOT APPLICABLE
SC-COMMAND-POST: VERIFIED OR NOT APPLICABLE
LOCAL WORKSPACE: CONNECTED OR LOCAL-ONLY
SECRETS EXPOSED: NO
```

## 9. Completion Gate

A V7.1 discovery or review task is incomplete unless:

1. canonical identifiers were loaded;
2. authenticated GitHub was queried directly;
3. the relevant GitHub surfaces were queried separately;
4. both Supabase projects were queried or expressly marked not applicable;
5. the Supabase access mode was disclosed;
6. local workspace limitations were disclosed;
7. every negative conclusion was scoped to the evidence surface;
8. GitHub and Supabase records were reconciled;
9. no privileged credential was exposed to the model.

## 10. Current Resolution

Copilot correctly found `governance/v7.1-owned-product-harness` but exact-name matching led it to suggest creating an unnecessary `v7.1` branch.

Coder later connected the correct GitHub remote and verified the canonical branch. Its subsequent statement that Supabase required raw API credentials was incomplete. The approved path is Supabase MCP OAuth or the governed Control Plane API, not disclosure of service-role credentials.

Resolution: retain the existing canonical branch, use the ordered discovery protocol, and prohibit direct privileged-key distribution to models or sandboxes.