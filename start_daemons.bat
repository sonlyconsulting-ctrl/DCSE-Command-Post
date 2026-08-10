@echo off
title DCSE Command Center — Startup Launcher
mode con: cols=85 lines=25
color 0B

echo =================================================================================
echo   D C S E   C O M M A N D   C E N T E R   -   S T A R T U P   L A U N C H E R
echo   Governance Baseline v6+ / PS Bridge Active
echo =================================================================================
echo.

echo [Step 1/5] Routing Downloads...
python job_downloads_archive_router.py
echo.

echo [Step 2/5] Processing Staged HTML Files...
python job_html_processor.py
echo.

echo [Step 3/5] Rebuilding PS DDNA Inventory Registry...
python job_ps_inventory.py
echo.

echo [Step 4/5] Launching main Tribunal Poller (Persistent)...
start "DCSE Tribunal Poller v6+" /min python -u -X utf8 job_tribunal_poller.py
echo   - Launched in background (minimized).
echo.

echo [Step 5/7] Launching Anti-Gravity Agent Daemon (Persistent)...
start "DCSE Anti-Gravity Agent v6+" /min python -u -X utf8 job_ag_agent.py
echo   - Launched in background (minimized).
echo.

echo [Step 6/7] Launching Qwen Coder Agent Daemon (Persistent)...
start "DCSE Qwen Coder Agent v6+" /min python -u -X utf8 _Tribunal_Inbox\job_qwen_coder_agent.py
echo   - Launched in background (minimized).
echo.

echo [Step 7/7] Launching Participant Activity Reporter (Persistent)...
start "DCSE Activity Reporter v6+" /min python -u -X utf8 job_participant_activity_reporter.py
echo   - Launched in background (minimized).
echo.

echo =================================================================================
echo   [SUCCESS] All startup routines complete and daemons spawned.
echo =================================================================================
timeout /t 5
