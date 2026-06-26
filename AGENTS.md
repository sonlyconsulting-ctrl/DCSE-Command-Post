# AGENTS.md

This file governs AI-agent and human operator behavior inside the DCSE Command Center repository.

## Authority

The governed local root for this lane is:

`C:\DS All Things\DCSE_Command_Center`

Treat this repository as a governed Command Center source repo. Do not treat it as a general backup, downloads archive, litigation store, or private activity mirror.

## Default Rule

Non-destructive by default. Read first. Classify before cleanup. Do not delete, move, rename, stage, commit, push, or normalize files unless DCS/DCSE has approved the exact scope.

## Public Repository Rule

Assume committed files may be exported by anyone if the GitHub repository is public. Only public-safe, intentional, reviewed materials may be committed.

Never reproduce secrets, private credentials, personal tokens, or PS/litigation content in chat, commits, docs, logs, or receipts.

## Forbidden Without Separate Approval

Agents must not run or perform:

- `git add .`
- `git add -A`
- broad staging of unreviewed folders
- commits
- pushes
- branch changes
- deletion or cleanup
- nested `.git` removal or modification
- secret rotation
- Supabase or production actions
- PS material routing into GitHub
- live `_Tribunal_Inbox` publication

## Git Staging Rule

Only stage files from an explicit DCS/DCSE allowlist. If the allowlist is ambiguous, stop and ask for clarification.

Preferred flow:

1. `git status --short --branch`
2. review allowlist
3. stage named files only
4. report staged files with `git diff --cached --name-only`
5. wait for commit approval

## PS And Litigation Firewall

The following are excluded from GitHub by default and require separate PS-only offline destination approval before any handling:

- `PS_WIN_WIN_WIN/`
- `DCSE_PS_CP_Project/`
- paths containing `DS Litigation`
- paths or filenames containing `seals`, `823cv489`, `dart`, or `pro se` when tied to PS/litigation context

Do not inspect, summarize, quote, or publish PS litigation content beyond path-level identification needed for exclusion and firewall checks.

## Secrets And Credential Handling

Do not open or print secret values. For sensitive findings, report only:

- path
- file type
- risk category
- recommended exclusion or remediation gate

Credential-risk files include `.env`, `*.env`, `*.env.txt`, password exports, API key files, credential audit CSVs, secret search results, service-role references, tokens, and connection strings.

## Nested Repository Handling

Nested Git repositories exist under the Command Center root. They must not be changed without explicit normalization approval.

Known nested repo areas include:

- `DCSE_CP_Project/.git`
- `DCSE_CP_Project/DCSE_ASSET_PORTAL_APP/.git`
- `_Tribunal_Inbox/.git`

Treat `DCSE_CP_Project` as a normalization candidate, not as a safe bulk-add folder. Treat `_Tribunal_Inbox` as a coordination boundary, not a public mirror.

## Tribunal Inbox Rule

Agents may use `_Tribunal_Inbox` for local coordination only when authorized. GitHub should store schemas, templates, routing rules, and sanitized examples, not raw live activity drops or private receipts.

If `_Tribunal_Inbox` appears as a gitlink/submodule-style entry or nested repo, stop before making repo-structure changes and request DCS/DCSE approval.

## Recommended Public-Safe Areas

Candidate areas for later allowlist review:

- `v6.9/01_Doctrine/`
- `v6.9/02_Registry/`
- `v6.9/08_Templates/`
- `v6.9/13_Open_Items/`
- reviewed `v6.8` Markdown governance files
- `rag_engine/`
- `DCSE_RAG_Prompts_Ingest/`
- reviewed `migrations/`
- reviewed `DCSE_DDNA/` source and SOP files
- sanitized docs for products, website, profile, and architecture

## Local-Only Areas By Default

Do not publish by default:

- `DCSE Tech Only/`
- `DCS_Employment_Workflow/`
- `Inbox_From_Downloads/`
- `DCS_CP/Inbox_From_Downloads/`
- `scratch/`
- `review_lanes/`
- `artifacts/restricted/`
- live `_Tribunal_Inbox` drops
- raw exports, caches, installers, archives, media, logs, and generated binaries

## Normalization Discipline

Normalization must be deliberate and auditable. Prefer copy-plan and rename-map review before moving files. Do not flatten lineage. Keep source-of-truth, archive, superseded, review, and support materials distinguishable.

The public repo should look like a Principal AI Technology Consultant command system: clear, intentional, secure, soulful, and operationally credible.

## Stop-Gates

Stop and report a Governance Stop-Gate receipt if any of these appear:

- already-tracked secret or credential material
- already-tracked PS/litigation material
- unexpected submodule behavior
- branch or remote mismatch
- command requires broad staging or cleanup
- requested action conflicts with `.gitignore`, this file, or DCS/DCSE approval scope

## Receipts

After any authorized write, return a concise receipt with:

- files written
- commands run
- branch and remote
- staged file check
- confirmation of no commit/push/delete/move unless explicitly authorized
- any stop-gate findings
