@echo off
title AI Lead Scraper Pro - Uninstaller
color 0C

cls
echo ============================================================
echo    🗑️  AI LEAD SCRAPER PRO - UNINSTALLER 🗑️
echo ============================================================
echo.
echo WARNING: This will remove the application and all data!
echo.
echo Are you sure you want to uninstall? (Y/N)
choice /c YN /n /m "Your choice: "

if errorlevel 2 (
    echo Uninstall cancelled.
    pause
    exit /b 0
)

echo.
echo [1/4] Removing Python packages...
python -m pip uninstall streamlit pandas requests groq -y
echo Done!
echo.

echo [2/4] Removing virtual environment...
if exist "venv" (
    rmdir /s /q venv
    echo Virtual environment removed!
)
echo Done!
echo.

echo [3/4] Removing data folders...
if exist "history" (
    rmdir /s /q history
    echo History folder removed!
)
if exist ".client_locks" (
    rmdir /s /q .client_locks
    echo License locks removed!
)
echo Done!
echo.

echo [4/4] Removing configuration files...
if exist "requirements.txt" del requirements.txt
if exist "__pycache__" rmdir /s /q __pycache__
echo Done!
echo.

echo ============================================================
echo    ✅ UNINSTALL COMPLETE! ✅
echo ============================================================
echo.
echo All components have been removed.
echo.
pause