# DCSE Operations Specification

An **Operation** is the fundamental atomic unit of governance and execution in DCSE.
Every task packet wraps an Operation along with acceptance criteria and execution bounds.

## Schema

```json
{
  "entity": "task | idea | asset | ddna | knowledge",
  "action": "edit | create | read | promote | delete | emit",
  "capabilities": ["github", "escd", "deployment", "supabase", "filehandling", "voice"],
  "actor": "delegated-executor | human | system",
  "directive": "L0 directive or decision reference",
  "facts": {
    "task_id": "T-001",
    "objective": "...",
    "declared_scope": ["path/..."],
    "reversibility": "reversible | reversible_with_residue | irreversible",
    "consequence": "low | moderate | high"
  }
}
```

## Reversibility and Consequence

- **REVERSIBLE / LOW**: Standard autonomous execution (`EXECUTE` or `EXECUTE_AS_CANDIDATE`). Reading, local testing, branch modifications inside scope.
- **IRREVERSIBLE / HIGH**: Requires explicit human authority (`ESCALATE` or `REFUSE`). Production deployments, secret updates, public communications, schema migrations without rollback.
