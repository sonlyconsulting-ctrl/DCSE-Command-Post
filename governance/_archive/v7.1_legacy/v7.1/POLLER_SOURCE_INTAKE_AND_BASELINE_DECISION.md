# DCSE V7.1 Poller Source Intake and Baseline Decision

Status: ACTIVE CONTROLLED USE
Authority: DCS
Task: V7_1_ACTION_1_POLLER_HARDENING

## Decision

The uploaded poller materials establish that multiple prior implementations exist. No new poller is authorized.

The repair baseline is the existing `job_tribunal_poller_v7.py` candidate and its documented state-machine and adapter architecture. The existing `claude_code_poller.ps1` is a separate SC-Command-Post worker poller and must be reviewed as an operational transport implementation, not silently merged into the Tribunal v7 code path.

## Evidence received

| Source | SHA-256 | Classification | Disposition |
|---|---|---|---|
| `job_tribunal_poller.py` | `508a8ccbbdedbc3982faf17bf33ef0dc168181f1c1fbeadd990ddd251d711ebe` | Legacy portable v6-style bridge | RETAIN AS EVIDENCE ONLY |
| `job_tribunal_poller (1).py` | `508a8ccbbdedbc3982faf17bf33ef0dc168181f1c1fbeadd990ddd251d711ebe` | Exact duplicate | DEDUPLICATE, DO NOT PROMOTE |
| `job_tribunal_poller (2).py` | `3eb074293524c2a358a61dc72118b1999a0c18e20b8c0ba12a09fd508a538f6c` | Windows v6-style variant with compliance hook | RETAIN AS EVIDENCE ONLY |
| `job_tribunal_poller_v7.py` | `08326db815c5e1b8a22ca7b726d1e851819ebb8362d0c37645f433ebfdd35087` | Governed v7 candidate | REPAIR BASELINE |
| `claude_code_poller.ps1` | `c19c82d2816b8b99893e5f990cebc9991b0ed907b7b9548b47cdb069f5e4467e` | SC-Command-Post worker poller | RETAIN, TEST, HARDEN |
| `TRIBUNAL_POLLER_V7_README.md` | `6faa4427fbec5d4a1b6d7b4171a1de9e55971dca900b7830c9faab2358c05caa` | Candidate architecture documentation | RETAIN AND RECONCILE |
| `TRIBUNAL_20260721_POLLER_V7_PREFLIGHT_RESPONSE.snapshot.json` | `b1739f9fa9c9f7d53568bc8504b28a4091afb742f2f08a99a8dcefba532fd880` | Prior governance review evidence | RETAIN |
| `poller_log.txt` | `6797a3f10fed2b737ec653c0a62efcb5ac66a393092a1087c81add62ab84ffbf` | Runtime evidence | RETAIN, ANALYZE |
| `poller_state.json` | `f912db24328bfd5b449e88f996f1da771a2ac9353a527b9d603ebc57f38701e1` | Runtime state evidence | RETAIN, DO NOT TREAT AS CANONICAL CONFIG |
| `start_tribunal_poller_20260604.cmd` | `bbad7fa2ed0718f6bd434efc19dc5aed0df32b1f73909d1b71afc3256e4fbe48` | Legacy launcher | RETAIN AS EVIDENCE, DO NOT ACTIVATE |

## Verified defects in legacy v6-style variants

The legacy Python variants perform direct Git pull, broad `git add .`, commit, and push operations. They can mark a file modified merely because Claude was triggered, even when Claude fails or times out. One variant also renames failed files to a quarantine suffix. These behaviors conflict with the v7 separation of observation, authorization, dispatch, verification, and publication.

## Verified strengths in the v7 candidate

The v7 candidate is audit-only by default, requires `--dispatch`, requires an explicit `POLLER_V7` authorization block, preserves source packets as read-only, uses terminal receipts for idempotency, verifies task ID and source hash, and separates worker adapters from the state machine.

## Missing dependencies and unresolved items

The uploaded v7 candidate imports the following files, which were not included in the upload set and were not found by repository code search:

- `tribunal_v7_state_machine.py`
- `tribunal_v7_codex_adapter.py`
- `tribunal_v7_fable_adapter.py`

Coder must locate these files on the network device or prior repository history before any replacement is considered. If they cannot be located, Coder may reconstruct them only from the documented interfaces and acceptance criteria, in a new bounded candidate branch, with independent review.

## Operating boundary

1. Do not create a parallel poller.
2. Do not activate the legacy launch command.
3. Do not broaden Git staging or direct publication behavior.
4. Do not change production credentials.
5. Do not create new Supabase tables unless a documented schema gap is proven and separately reviewed.
6. Preserve all evidence and hashes.
7. Use the V7 candidate as the architectural baseline and the PowerShell worker poller as an implementation to test and harden.
