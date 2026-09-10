# Tribunal Inbox UX Layer

Status: Active support layer
Root: C:\DS All Things\DCSE_Command_Center\_Tribunal_Inbox

## Purpose

The Tribunal inbox is both a machine-readable relay and a human review console. Root-level `TRIBUNAL_*.json` files remain the live activity files so the current poller can detect changes, advance statuses, trigger agents, and sync through the Git relay.

The dated folders provide a cleaner daily and weekly review experience without breaking the live poller.

## Live Editing Rule

Use the root-level JSON files for active intervention:

- Open the relevant `TRIBUNAL_*.json`.
- Confirm file contents directly.
- Add DCS interjections, corrections, or instructions inside the JSON as needed.
- Save the root file so the poller can detect and relay the change.

## Dated Review Structure

Daily folders live under:

`_Daily\YYYY-MM-DD\`

Each daily folder may contain:

- `ACTIVITY_INDEX.md`
- `ACTIVITY_INDEX.json`
- `TRIBUNAL_*.snapshot.json`
- `DCS_INTERJECTIONS.md`
- `DAILY_INTEL.md`

Weekly folders live under:

`_Weekly\YYYY-W##\`

Each weekly folder may contain:

- `WEEKLY_INTEL.md`
- links or references to daily folders

## Non-Destructive Rule

The dated folders are mirrors, indexes, and notes. They do not replace the root live JSON files. Do not move root `TRIBUNAL_*.json` files into dated folders unless the poller is upgraded to watch recursively.

## Refresh

Run:

`python tribunal_inbox_ux_refresh.py`

That creates or refreshes the current daily folder, snapshots current root Tribunal JSON files, and writes daily and weekly index files.
