import os
import json
import time
import datetime
import subprocess
from pathlib import Path

# Paths config
PROJECT_ROOT = Path(r"C:\DS All Things\DCSE_Command_Center")
INBOX_DIR = PROJECT_ROOT / "_Tribunal_Inbox"
ACTIVITY_DROPS_DIR = INBOX_DIR / "_Activity_Drops"

ROSTER = [
    "AG", "Coder_Qwen", "Codex", "Claude_Code", "CoWork_Gemini", "chatgpt_v5_5",
    "Qwen", "Qwen_Coder", "ChatGPT", "Gemini", "Claude_CP", "DCS"
]

def ts():
    return f"[{datetime.datetime.now():%H:%M:%S}]"

def log(msg):
    print(msg, flush=True)

def get_recent_git_commits():
    try:
        result = subprocess.run(
            ["git", "log", "-n", "3", "--oneline"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split("\n")
    except Exception as e:
        return [f"Git log error: {e}"]

def get_activity_drops():
    """Read all JSON drops from the _Activity_Drops folder and clear them after reading."""
    drops = {}
    if not ACTIVITY_DROPS_DIR.exists():
        ACTIVITY_DROPS_DIR.mkdir(parents=True, exist_ok=True)
        return drops

    for drop_file in ACTIVITY_DROPS_DIR.glob("*.json"):
        try:
            with open(drop_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            participant = data.get("participant", "Unknown")
            activity = data.get("activity", "No activity provided.")
            
            if participant not in drops:
                drops[participant] = []
            drops[participant].append(activity)
            
            # Remove drop file after reading to prevent duplicate processing
            drop_file.unlink()
        except Exception as e:
            log(f"{ts()} Error reading drop {drop_file.name}: {e}")
            
    return drops

def update_pending_slots(drops, commits):
    """Find the most recent TRIBUNAL JSON and fill any PENDING slots with actual activity."""
    # Find active tribunal package
    files = list(INBOX_DIR.glob("TRIBUNAL_*.json"))
    files = [f for f in files if "TEMPLATE" not in f.name and "SYNC_SNAPSHOT" not in f.name and "ACTIVITY_REPORT" not in f.name]
    if not files:
        return
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    latest_json = files[0]

    modified = False
    try:
        with open(latest_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        responses = data.get("RESPONSES", {})
        reproof_responses = data.get("REPROOF_WIN_WIN_WIN", {}).get("RESPONSES", {})

        for participant in ROSTER:
            # Prepare the activity string for this participant
            if participant in drops:
                activity_str = f"Active Report: {' | '.join(drops[participant])} — {datetime.datetime.now().isoformat()}"
            else:
                activity_str = f"No active drops. System context: {commits[0] if commits else 'No recent commits.'}"

            # Check Main Responses
            if responses.get(participant) in ["PENDING", "AWAITING_REPORTER_SYNC"]:
                responses[participant] = activity_str
                modified = True
                log(f"{ts()} Updated {participant} in Main Responses.")

            # Check Reproof Responses
            if reproof_responses.get(participant) in ["PENDING", "AWAITING_REPORTER_SYNC"]:
                reproof_responses[participant] = activity_str
                modified = True
                log(f"{ts()} Updated {participant} in Reproof Responses.")

        if modified:
            with open(latest_json, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            log(f"{ts()} ✅ Updated {latest_json.name} with automated participant activity.")
            
    except Exception as e:
        log(f"{ts()} Error processing {latest_json.name}: {e}")

def main():
    log("=" * 65)
    log("  DCSE Command Center — Participant Activity Reporter")
    log("=" * 65)
    
    if not ACTIVITY_DROPS_DIR.exists():
        ACTIVITY_DROPS_DIR.mkdir(parents=True, exist_ok=True)
    
    while True:
        commits = get_recent_git_commits()
        drops = get_activity_drops()
        
        # Only update if we found new drops or want to enforce PENDING sweeps
        update_pending_slots(drops, commits)
        
        # Optional: Generate a daily summary file if drops were found
        if drops:
            date_str = datetime.datetime.now().strftime("%Y%m%d")
            sync_file = INBOX_DIR / f"TRIBUNAL_ACTIVITY_SYNC_{date_str}.json"
            sync_data = {"date": date_str, "activity": drops, "system_commits": commits}
            
            # Append or create
            if sync_file.exists():
                try:
                    with open(sync_file, "r", encoding="utf-8") as f:
                        existing = json.load(f)
                    for p, acts in drops.items():
                        if p not in existing.get("activity", {}):
                            existing.setdefault("activity", {})[p] = []
                        existing["activity"][p].extend(acts)
                    sync_data = existing
                except:
                    pass
                    
            with open(sync_file, "w", encoding="utf-8") as f:
                json.dump(sync_data, f, indent=2)
                
            log(f"{ts()} 📝 Wrote daily activity sync to {sync_file.name}")
        
        time.sleep(30) # Poll every 30 seconds

if __name__ == "__main__":
    main()
