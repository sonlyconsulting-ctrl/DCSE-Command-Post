# DCSE Command Center

DCSE Command Center is a governed AI operations workspace for doctrine, agent coordination, RAG/DDNA architecture, command-post workflows, and controlled product intelligence. This repository is intended to represent the public-safe source layer of the Command Center, not a full mirror of the local working directory.

The project is organized around a simple principle: publish only what is intentional, useful, auditable, and safe to share. Local operational material, secrets, private inbox activity, PS/litigation content, personal exports, caches, and large generated assets are excluded by design.

## Current Repository Role

This repo is the professional source-of-truth frame for:

- Governance doctrine and operating rules
- Agent instructions, handoff patterns, and approval gates
- RAG and DDNA source modules
- Database migration review files
- Product and website documentation after sanitization
- Public-safe architecture notes, templates, and runbooks

It is not a backup of the full `DCSE_Command_Center` filesystem.

## Public Safety Posture

If this GitHub repository is public, every committed file should be treated as exportable by anyone. Do not commit private materials, credentials, live inbox activity, litigation material, local-only receipts, or files that require DCS/DCSE approval for publication.

Excluded by default:

- `.env` files, API keys, tokens, credentials, password exports, and secret-search reports
- `PS_WIN_WIN_WIN`, `DCSE_PS_CP_Project`, and PS/litigation related material
- Live `_Tribunal_Inbox` activity drops and private agent receipts
- Local scratch folders, downloads intake, raw exports, caches, and build outputs
- Large media, installers, archives, and generated binaries

## Proposed Public Structure

The normalized public repo should move toward this shape through controlled, reviewed steps:

```text
README.md
AGENTS.md
.gitignore

docs/
  governance/
  architecture/
  products/
  website/
  profile/

doctrine/
  v6.8/
  v6.9/

agents/
  skills/
  triggers/
  handoffs/
  schemas/

rag_engine/
ddna/
migrations/
tribunal/
  schemas/
  templates/
  routing_rules/
  sanitized_examples/

products/
  asset-portal/
  rag-ddna/
  tribunal-router/
  command-center/

website/
  pages/
  copy/
  sanitized-previews/
```

## Active Local Source Areas

The local Command Center currently contains several important source areas. These should be classified before publication:

- `v6.9`: active doctrine and governance lane
- `v6.8`: prior approved governance lane and adapter set
- `rag_engine`: RAG source code and package structure
- `DCSE_DDNA`: DDNA routines, SOPs, and architecture materials
- `DCSE_RAG_Prompts_Ingest`: prompt ingestion materials and source maps
- `migrations`: database/schema migration files, requiring secret and data review
- `DCSE_CP_Project`: nested project area requiring normalization review before inclusion
- `_Tribunal_Inbox`: live or submodule-like coordination area, not public content by default

## Branching Guidance

Branches represent work states, not folder categories.

Recommended branch posture:

- `main`: approved stable public-safe Command Center source
- `release/v6.9`: controlled release branch if needed for a v6.9 promotion
- `feature/*`: temporary work branches for reviewed changes
- `hotfix/*`: urgent corrective changes

Do not create permanent branches simply for folders like `rag_engine`, `migrations`, or `v6.9`.

## Normalization Rule

Normalization should happen through an allowlist, not broad adds or bulk moves. The safe order is:

1. Maintain containment with `.gitignore`.
2. Review the allowlist for public-safe source groups.
3. Create or update repo framing docs.
4. Copy or move only approved materials into the normalized structure.
5. Run read-only status and review receipts.
6. Stage only explicitly approved files.
7. Commit and push only after DCS/DCSE approval.

## Human And Agent Use

Humans and AI agents should read `AGENTS.md` before modifying this repository. The agent rules define approval gates, privacy restrictions, PS exclusions, branch discipline, and safe handling of nested repo areas.
