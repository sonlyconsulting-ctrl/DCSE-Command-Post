@echo off
setlocal
set "SCRIPT_DIR=%~dp0"

if not exist "%SCRIPT_DIR%START_VOW_AND_GO.ps1" (
  echo ERROR: START_VOW_AND_GO.ps1 was not found beside this launcher.
  pause
  exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%START_VOW_AND_GO.ps1"
set "EXIT_CODE=%ERRORLEVEL%"

if not "%EXIT_CODE%"=="0" (
  echo.
  echo Vow ^& Go could not start. Review the error above.
  pause
)

exit /b %EXIT_CODE%
