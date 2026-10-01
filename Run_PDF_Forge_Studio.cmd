@echo off
setlocal
set "APP=%~dp0PDF_Forge_Studio.py"
where python.exe >nul 2>&1
if not errorlevel 1 (
    python "%APP%"
    goto :eof
)
where py.exe >nul 2>&1
if not errorlevel 1 (
    py "%APP%"
    goto :eof
)
echo Python is not installed.
echo Install Python, then run this file again.
pause
