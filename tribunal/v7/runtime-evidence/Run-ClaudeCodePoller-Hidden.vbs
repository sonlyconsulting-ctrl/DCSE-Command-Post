Set objShell = CreateObject("WScript.Shell")
objShell.Run "powershell.exe -NoProfile -ExecutionPolicy Bypass -File ""C:\DS All Things\DCSE_Command_Center\v7.0\09_WORKERS\claude_code_poller.ps1"" -CredentialFile ""C:\ProgramData\DCSE\secrets\worker-nevgdyfpxdaloacuutal.clixml""", 0, True
