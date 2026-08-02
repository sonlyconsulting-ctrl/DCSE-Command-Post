# DCSE V7.1 Agent Discovery and Query Protocol

Status: DRAFT CONTROL FOR PR #29
Authority: DCS
Applies to: ChatGPT, Claude, Codex, Qwen, Copilot, local workers, cloud sandboxes, and future approved agents

## 1. Purpose

Prevent false `not found` conclusions caused by general web search, an unconfigured local checkout, one Supabase project, stale code indexes, or exact-name matching.

A negative result is valid only for the evidence surface actually queried.

## 2. Canonical V7.1 Identifiers

Repository: `sonlyconsulting-ctrl/DCSE-Command-Post`

Canonical branch: `governance/v7.1-owned-product-harness`

Canonical pull request: `#29`

Canonical document path: `governance/v7.1/`

Governance registry project: `DCSE-DDNA` (`uutpzaiqymyufljdgdaa`)

Operational Command Post project: `SC-Command-Post` (`nevgdyfpxdaloacuutal`)

There is no requirement for a branch named exactly `v7.1`. The canonical branch contains the version identifier and descriptive scope. Do not create an alias branch solely to satisfy an exact-name query.

## 3. Mandatory Order of Operations

### Step 0: Resolve the task and lane

Record:

- requested subject or identifier
- repository or product scope
- lane
- confidentiality
- whether the task is governance, operational execution, product work, or research

Stop if the lane cannot be resolved safely.

### Step 1: Read the authority locator

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

### Step 4: Query DCSE-DDNA first for governance and enterprise-memory work

Use `DCSE-DDNA` for:

- governance directives
- architecture decisions
- project plans
- promotion records
- governance references
- research sources
- enterprise memory

### Step 5: Query SC-Command-Post for runtime and operational work

Use `SC-Command-Post` for:

- agent tasks
- assignments
- task events
- runtime state
- worker heartbeats
- product-operation activity
- execution receipts

### Step 6: Reconcile GitHub and both Supabase projects

For governance or product-factory work, compare:

- GitHub branch, PR, issue, and file state
- DCSE-DDNA governance and memory records
- SC-Command-Post operational tasks and activity

Do not treat one system as a complete substitute for the others.

### Step 7: Inspect local workspace only as an execution surface

A local workspace is authoritative only for its checked-out commit and files.

Before drawing repository-wide conclusions, verify:

- `git remote -v`
- current branch
- fetched remote refs
- current commit
- shallow or grafted history

If no remote is configured, label every conclusion `LOCAL WORKSPACE ONLY`.

### Step 8: Report evidence coverage

Every review or search result must state:

- GitHub repository verified: YES or NO
- GitHub branches queried: YES or NO
- GitHub PRs queried: YES or NO
- GitHub issues queried: YES or NO
- GitHub files queried: YES or NO
- DCSE-DDNA queried: YES or NO
- SC-Command-Post queried: YES or NO
- local workspace status
- authentication status
- unresolved access limitations

## 4. Negative-Finding Rule

Permitted language:

- `No exact branch named v7.1 was found. The canonical V7.1 branch is governance/v7.1-owned-product-harness.`
- `No V7.1 record was found in SC-Command-Post. DCSE-DDNA was not inspected.`
- `No V7.1 marker was found in the isolated local workspace. The live repository was not connected.`

Prohibited language:

- `V7.1 does not exist` when only one evidence surface was searched.
- `The repository is private` without repository metadata verification.
- `No issues or PRs exist` when only branch or code search was used.
- `No GitHub material exists` when the local checkout has no remote.

## 5. Automatic Discovery Manifest

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

## 6. Automatic Routing Rule

- Governance, architecture, research, promotion, and enterprise-memory questions start in `DCSE-DDNA`, then reconcile to GitHub, then check `SC-Command-Post` for execution state.
- Runtime, worker, product-operation, and task-execution questions start in `SC-Command-Post`, then reconcile to GitHub, then check `DCSE-DDNA` for authority.
- GitHub PR, issue, branch, or code-review questions start in authenticated GitHub, then reconcile to the applicable Supabase registry.
- Local workspace questions start locally, but no enterprise-wide conclusion is permitted until authenticated GitHub and the applicable Supabase project are checked.

## 7. Completion Gate

A V7.1 discovery or review task is incomplete unless:

1. canonical identifiers were loaded;
2. authenticated GitHub was queried directly;
3. the relevant GitHub surfaces were queried separately;
4. both Supabase projects were queried or expressly marked not applicable;
5. local workspace limitations were disclosed;
6. every negative conclusion was scoped to the evidence surface;
7. GitHub and Supabase records were reconciled.

## 8. Current Resolution

Copilot correctly found `governance/v7.1-owned-product-harness` but exact-name matching led it to suggest creating an unnecessary `v7.1` branch.

Resolution: retain the existing canonical branch. Do not create a duplicate alias branch. Use the manifest and ordered discovery protocol above.