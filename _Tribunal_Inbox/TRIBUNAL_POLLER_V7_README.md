# DCSE Tribunal Poller v7 Candidate

Status: `CANDIDATE`  
Default execution: one-pass, audit-only  
Production activation: prohibited until a separate launcher/daemon approval  
Claude/Fable exchange: fail-closed and pending a verified headless adapter

## What v7 changes

Poller v7 separates observation, authorization, dispatch, and verification. It does not contain Git commands, does not mutate its source packets, and does not move anything into quarantine. A malformed or unauthorized task receives a `QUARANTINE_PENDING` receipt while the original remains in place.

The v7 state sequence is:

`RECEIVED -> VALIDATED -> AUTHORIZED -> DISPATCHED -> VERIFYING -> COMPLETED`

Failure and governance branches terminate at `FAILED` or `QUARANTINE_PENDING`.

`COMPLETED` requires all of the following:

- worker process exit code `0`;
- a successful Codex JSONL event stream;
- a schema-constrained final JSON object;
- exact task-ID match;
- exact source SHA-256 match;
- `COMPLETED` worker status;
- every declared output reported and present inside the authorized working directory.

## Source files

- `job_tribunal_poller_v7.py` - scanner, authorization gate, dispatch, and receipts.
- `tribunal_v7_state_machine.py` - task validation, state transitions, hashing, atomic writes, and completion verification.
- `tribunal_v7_codex_adapter.py` - bounded noninteractive Codex CLI worker.
- `tribunal_v7_fable_adapter.py` - disabled fail-closed Fable/Claude placeholder.

The existing v6 poller and controller are not imported or modified.

## Explicit task contract

Only a `TRIBUNAL_*.json` packet containing a top-level `POLLER_V7` object is eligible. Example:

```json
{
  "TRIBUNAL_MESSAGE_ID": "TRIB-EXAMPLE",
  "POLLER_V7": {
    "task_id": "CP-EXAMPLE-001",
    "worker": "codex",
    "working_directory": "C:\\DS All Things\\DCSE_Command_Center\\example-product",
    "sandbox": "workspace-write",
    "timeout_seconds": 900,
    "prompt": "Create the bounded candidate described in this work order and run its local tests.",
    "expected_outputs": [
      "candidate/index.html",
      "candidate/verification.json"
    ],
    "authorization": {
      "decision": "GO",
      "approved_by": "DCS Level 0",
      "approved_at": "2026-07-23T20:00:00-04:00"
    }
  }
}
```

Output paths must be relative to `working_directory`. The working directory must already exist and be inside an allowlisted root.

## Commands

Audit one pass without executing a worker:

```powershell
python .\job_tribunal_poller_v7.py --once
```

Dispatch explicitly authorized tasks once:

```powershell
python .\job_tribunal_poller_v7.py --once --dispatch --allow-root "C:\DS All Things\DCSE_Command_Center"
```

Continue polling after candidate verification:

```powershell
python .\job_tribunal_poller_v7.py --watch --dispatch --poll-interval 120 --allow-root "C:\DS All Things\DCSE_Command_Center"
```

Receipts are written atomically under `_Poller_v7_Runtime\receipts`. A terminal receipt with the same task ID and source hash prevents repeat execution.

## Codex worker

The adapter uses the installed `codex exec` interface with:

- the documented `windows.sandbox="unelevated"` fallback because the elevated Windows sandbox helper returns access denied for background workers on this host;
- global `--sandbox` and `--ask-for-approval never` controls before `exec`;
- `--ephemeral`;
- an explicit `read-only` or `workspace-write` sandbox;
- an explicit working directory;
- `--json` event output;
- `--output-schema`;
- `--output-last-message`.

The unelevated fallback still uses a restricted Windows token and ACL-based filesystem boundaries. The adapter never selects `danger-full-access`. It removes common secret-bearing environment variables and outer Codex desktop permission variables before launching the worker. Authentication continues through the installed Codex CLI's saved login and host configuration.

## Fable/Claude status

`tribunal_v7_fable_adapter.py` intentionally does not call Claude. Cowork availability is interactive access, not a verified unattended worker contract. A task assigned to `fable` fails closed with `PENDING_CLAUDE_CODE_INSTALL_OR_APPROVED_API_ADAPTER`.

Fable activation requires a separate approved change that proves:

1. the headless executable or API adapter is available to the poller process;
2. credentials are noninteractive and appropriately scoped;
3. timeouts and exit codes are captured;
4. a schema-constrained result includes the exact task ID and source hash;
5. expected outputs are verified by the poller;
6. failure cannot be reported as success.

## Deliberately excluded

- `git add`, commit, pull, push, or branch actions;
- launcher and daemon changes;
- automatic quarantine move or rename;
- modification of existing Tribunal packets;
- Supabase writes;
- production deployment;
- automatic activation of Fable/Claude.
