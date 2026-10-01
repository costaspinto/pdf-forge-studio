@echo off
setlocal EnableExtensions EnableDelayedExpansion
title PDF Forge Studio v2.1.1 - Installer

set "APPDIR=%USERPROFILE%\Downloads\PDF_Forge_Studio"
set "PYFILE=%APPDIR%\PDF_Forge_Studio.py"

echo.
echo ==============================================================
echo                    PDF FORGE STUDIO
echo                    Version 2.1.1
echo                  Developer: Costas Pinto
echo ==============================================================
echo.
echo READ BEFORE INSTALLING:
echo If Windows downloaded this package from the Internet, Windows may
echo mark the files as untrusted. Do NOT disable Smart App Control.
echo If the ZIP has an "Unblock" option in Properties, use that before
echo extracting the ZIP.
echo.
pause

if not exist "%APPDIR%" mkdir "%APPDIR%"

echo.
echo [1/4] Detecting Python...

set "PYTHONEXE="

for /f "delims=" %%P in ('where python.exe 2^>nul') do (
    if not defined PYTHONEXE set "PYTHONEXE=%%P"
)

if defined PYTHONEXE goto PYTHON_OK

set "PYLAUNCHER="
for /f "delims=" %%P in ('where py.exe 2^>nul') do (
    if not defined PYLAUNCHER set "PYLAUNCHER=%%P"
)

if defined PYLAUNCHER (
    set "PYTHONEXE=%PYLAUNCHER%"
    goto PYTHON_OK
)

echo Python was not found.
echo.
echo Attempting installation using Windows Package Manager...
echo.

where winget.exe >nul 2>&1
if errorlevel 1 (
    echo ERROR: winget is not available.
    echo Install Python from https://www.python.org/downloads/windows/
    echo and run this installer again.
    pause
    exit /b 1
)

winget install --id Python.Python.3.13 -e --source winget --accept-package-agreements --accept-source-agreements

echo.
echo Python installation has completed.
echo Windows may require a new terminal session to expose Python.
echo.

set "PATH=%LocalAppData%\Programs\Python\Python313;%LocalAppData%\Programs\Python\Python313\Scripts;%PATH%"

for /f "delims=" %%P in ('where python.exe 2^>nul') do (
    if not defined PYTHONEXE set "PYTHONEXE=%%P"
)

if not defined PYTHONEXE (
    echo Python is installed but this terminal cannot see it yet.
    echo.
    echo Close this window and double-click this installer again.
    pause
    exit /b 1
)

:PYTHON_OK

echo Python launcher:
echo %PYTHONEXE%
"%PYTHONEXE%" --version

echo.
echo [2/4] Installing PDF libraries...
"%PYTHONEXE%" -m pip install --upgrade pymupdf pillow

if errorlevel 1 (
    echo First attempt failed. Retrying...
    "%PYTHONEXE%" -m pip install pymupdf pillow
)

if errorlevel 1 (
    echo.
    echo ERROR: Could not install PyMuPDF and Pillow.
    echo Check your Internet connection or install them manually with:
    echo %PYTHONEXE% -m pip install pymupdf pillow
    pause
    exit /b 1
)

echo.
echo [3/4] Copying application...
copy /Y "%~dp0PDF_Forge_Studio.py" "%PYFILE%" >nul

if errorlevel 1 (
    echo ERROR: Could not copy PDF_Forge_Studio.py.
    echo Make sure both files are in the same extracted folder.
    pause
    exit /b 1
)

echo.
echo [4/4] Testing application imports...
"%PYTHONEXE%" -c "import fitz; from PIL import Image; print('Dependencies OK')"

if errorlevel 1 (
    echo.
    echo ERROR: Dependencies failed validation.
    pause
    exit /b 1
)

echo.
echo ==============================================================
echo                  INSTALLATION COMPLETE
echo ==============================================================
echo.
echo Application:
echo %APPDIR%
echo.
echo Starting PDF Forge Studio...
echo.

"%PYTHONEXE%" "%PYFILE%"

if errorlevel 1 (
    echo.
    echo PDF Forge Studio closed with an error.
    echo.
    echo Check:
    echo %APPDIR%\Logs\pdf_forge.log
    echo.
    pause
)

endlocal
