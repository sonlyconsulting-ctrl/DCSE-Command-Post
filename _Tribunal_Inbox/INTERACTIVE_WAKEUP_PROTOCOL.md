# DCSE Tribunal Relay: Interactive Wakeup Protocol

The DCSE Command Center and Tribunal system is configured to run **24/7 in the background** as persistent daemons (Poller v6/v7, Qwen Agent, AG Agent, etc.).
By default, the poller checks for new files and executes a `git pull` from this GitHub repository every 2 minutes.

However, during interactive sessions or active development, waiting 2 minutes for the background poller to cycle can cause unacceptable delays.

## How to Wake the System for Interactive Use

If you need the system to poll aggressively and process packets immediately (with no activity gaps up to 60 minutes), you can trigger an **Interactive Wakeup Session**. 

### For AI Agents and Python Environments
Execute the following python script from this directory:
```bash
python wake_interactive_session.py
```

### For Human Operators (Windows)
Double-click or run from the command line:
```cmd
wake_interactive_session.bat
```

## What Happens During a Wakeup Session
When the wakeup session is triggered, it will run for **60 minutes**:
1. It immediately pulls the latest commits from GitHub (`DCSE-Tribunal-Relay`).
2. It aggressively "touches" all `TRIBUNAL_*.json` files in the inbox every 10 seconds.
3. This forces the background `job_tribunal_poller.py` daemon's filesystem watcher to immediately process the packets, bypassing its normal 2-minute sleep schedule.
4. After 60 minutes of no activity, the script terminates and the system automatically returns to its standard 24/7 background 2-minute cadence.

> **Note**: You do not need to restart the main daemons (`start_daemons.bat`). The wakeup scripts simply prod the existing, running daemons to act immediately.
