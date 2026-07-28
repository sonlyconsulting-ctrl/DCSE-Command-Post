# Communication Doctrine Rename and Copy Plan 001

No originals are deleted. The initial inventory contains 70 files, 511,296 bytes, and zero byte-identical duplicate groups. Every initial file is classified in `INITIAL_FILE_INVENTORY_001.csv`.

## Canonical imports from PR 14

| Source | Governed destination | Class | Decision |
|---|---|---|---|
| `02_ARCHITECTURE/V7_AGENT_WORKER_ARCHITECTURE.md` | same path | REVIEW | Copy as communication architecture input; later engines remain outside this wave. |
| Thirteen `supabase/migrations/*_v7_*.sql` files | same paths | ACTIVE | Copy exact Git blobs; preserve migration order and history contradiction for review. |
| `supabase/functions/v7-worker-token/index.ts` | same path | ACTIVE | Canonical enrollment-secret token broker. |
| `supabase/functions/v7-result-bridge/index.ts` | same path | ACTIVE | Canonical service-role-gated manual bridge entry point. |
| `supabase/rollback/v7_restricted_rpc_rollback.sql` | same path | REVIEW | Preserve rollback contract; destructive dc_event conversion stays commented. |
| `supabase/seed/v7_worker_identities.sql` | same path | SUPPORT | Registration template only; contains no secrets. |
| Four PR 14 certification receipts | `EVIDENCE_PACKET/SOURCE_RECEIPTS/` | ARCHIVE | Preserve contradictory historical states and lineage. |

## Explicit exclusions and supersessions

| Source | Class | Disposition |
|---|---|---|
| `supabase/functions/v7-worker-auth/index.ts` | SUPERSEDED | Do not copy into the canonical tree. Its deployed staging instance is unsafe and must be decommissioned before promotion. |
| `workers/claude-reviewer-worker.js` | SUPERSEDED | Replaced by `workers/claude-reviewer-operational.js`, whose hash matches the PASS receipt. |
| `DEPLOYMENT_GUIDE_CLAUDE_REVIEWER_WORKER.md` | SUPERSEDED | Contains obsolete unauthenticated token guidance and destructive rollback language; preserve only in PR 14 history. |
| Acceptance, promotion, completion, rule, skill, workflow, Runtime Compiler implementations in PR 14 | REVIEW | Do not import in this communication-only wave. |
| `package-lock.json` | REVIEW | Preserve untouched and untracked. It is an empty root lockfile with no root `package.json` and no Git history. Exclude from every closeout commit. |

## CR-SEC-001 additions

| Source | Governed destination | Class | Decision |
|---|---|---|---|
| Staging `v7-worker-auth` version 1 source | `supabase/rollback/v7-worker-auth-v1/index.ts` | ARCHIVE | Preserve exact vulnerable lineage for audit; never redeploy without a new security review. |
| CR-SEC-001 deny-all handler | `supabase/decommission/v7-worker-auth/index.ts` | ACTIVE | Deploy only to the staging `v7-worker-auth` slug as a reversible HTTP 410 tombstone. |
| Remediation record | `CR_SEC_001_REMEDIATION_PLAN.md` | FINAL | Preserve deployment facts, validation requirements, and restoration procedure. |

The rename map is intentionally conservative: authoritative files retain stable paths, historical receipts move only into the governed evidence packet, and no destructive cleanup is authorized.
