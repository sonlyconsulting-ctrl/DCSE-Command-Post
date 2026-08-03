@echo off
set PYTHONUTF8=1
cd /d "C:\DS All Things\DCSE_Command_Center"
"C:\Users\dsead\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" "C:\DS All Things\DCSE_Command_Center\job_tribunal_poller.py" > "C:\DS All Things\DCSE_Command_Center\tribunal_poller_20260604.log" 2>&1
