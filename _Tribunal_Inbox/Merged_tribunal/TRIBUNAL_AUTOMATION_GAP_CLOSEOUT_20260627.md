# Tribunal Automation Gap Closeout Candidate - 2026-06-27

## Purpose
Create a single audit-first control surface for the Tribunal automation lane before any live daemon launch, move, quarantine, git relay, or file-promotion behavior is expanded.

## Local Findings
- Governed root verified: `C:\DS All Things\DCSE_Command_Center`.
- Live Tribunal inbox verified: `C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox`.
- Existing launcher `start_daemons.bat` starts the poller, AG daemon, and participant activity reporter, but does not launch `job_qwen_coder_agent.py`.
- Existing participant reporter updates only the newest eligible `TRIBUNAL_*.json`, so older `PENDING` and `AWAITING_REPORTER_SYNC` slots can remain unresolved.
- Existing poller combines compliance quarantine, Claude triggering, git pull, git add/commit, and git push in one persistent process.
- Quarantine files are already present, proving move/rename behavior has happened in the lane.

## Candidate Closure Package
- `tribunal_automation_controller.py`: dry-run controller that audits launcher coverage, pending slots, quarantine files, and activity drops.
- `START_TRIBUNAL_AUTOMATION_DRYRUN.cmd`: one-click dry-run receipt launcher. It does not start daemons.
- This closeout note: DCS-readable explanation of the automation gap and recommended sequence.

## Recommended Execution Sequence
1. Use the dry-run controller as the Tribunal cockpit.
2. Approve a unified persistent launcher only after reviewing the dry-run receipt.
3. Patch the reporter so it sweeps all eligible Tribunal JSON files, not just the newest file.
4. Split poller side effects into explicit modes: audit-only, local-sync, quarantine-apply, and relay-push.
5. Require a move manifest before relocating anything: source, destination, reason, SHA256, and DCS approval.

## DCS Gate
This package is not live automation. It is a candidate control layer. It does not move, copy, rename, delete, commit, push, or start persistent processes.
