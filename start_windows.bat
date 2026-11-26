@echo off
rem Starts your app on Windows. In Command Prompt in this folder, type:  start_windows.bat
rem (Double-clicking this file also works.)
cd /d "%~dp0"
title COMP3278 app - keep this window open

rem Started from inside the zip file? Windows then runs it from a temporary folder.
echo "%~dp0" | find /i "\AppData\Local\Temp" >nul
if not errorlevel 1 (
    echo You opened this file from inside the zip.
    echo Close this window, right-click the zip file, choose "Extract All...",
    echo then open the extracted folder and start the app from there.
    pause
    exit /b 1
)

rem Find a real Python 3 (the "python" shortcut from the Microsoft Store does not count).
set PY=
py -3 --version >nul 2>nul && set PY=py -3
if not defined PY python --version >nul 2>nul && set PY=python
if not defined PY (
    echo Python is not installed.
    echo Install it from https://www.python.org/downloads/ and tick "Add python.exe to PATH"
    echo on the first screen of the installer. Then start this file again.
    pause
    exit /b 1
)

rem A private Python environment for this project, created the first time only
rem (and again if the .venv folder was copied from another computer and does not work here).
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys" >nul 2>nul
    if errorlevel 1 (
        echo The .venv folder does not work on this computer. Setting up Python again...
        rmdir /s /q .venv
    )
)
if not exist ".venv\Scripts\python.exe" (
    echo First start: setting up Python for this project...
    %PY% -m venv .venv
    if errorlevel 1 (
        echo Could not set up Python. Re-install Python from python.org and try again.
        pause
        exit /b 1
    )
)
".venv\Scripts\python.exe" -c "import flask" >nul 2>nul
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r requirements.txt
    if errorlevel 1 (
        echo Could not install Flask. Check your internet connection and try again.
        pause
        exit /b 1
    )
)

echo.
echo Tip: do not click inside this window. Windows pauses the app while text is selected.
echo      If the app seems frozen, click in this window and press Enter.
".venv\Scripts\python.exe" app\app.py %*
pause
