@echo off
title AI Lead Scraper Pro - Premium Launcher
color 0A

:: ========================================
:: AI LEAD SCRAPER PRO - PREMIUM LAUNCHER
:: FULLY AUTOMATED - NO USER INPUT REQUIRED
:: ========================================

setlocal enabledelayedexpansion

:: Set console window size
mode con: cols=80 lines=30

:: Header
cls
echo ============================================================
echo    👑 AI LEAD SCRAPER PRO - PREMIUM EDITION 👑
echo ============================================================
echo.
echo    Developed by: Kimpuler Tech
echo    Version: 2.0 Premium
echo.
echo ============================================================
echo.

:: Step 1: Check Python
echo [1/5] Checking Python installation...
echo.

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python manually from: https://python.org
    echo Make sure to check 'Add Python to PATH' during installation
    echo.
    echo After installing Python, run this launcher again.
    echo.
    pause
    exit /b 1
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python found: Version %PYTHON_VERSION%
echo.

:: Step 2: Check pip
echo [2/5] Checking pip package manager...
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] pip not found! Installing pip...
    python -m ensurepip --upgrade >nul 2>nul
)
echo [SUCCESS] pip is ready
echo.

:: Step 3: Upgrade pip (silent mode)
echo [3/5] Upgrading pip to latest version...
python -m pip install --upgrade pip --quiet --no-warn-script-location >nul 2>nul
echo [SUCCESS] pip upgraded
echo.

:: Step 4: Install requirements (silent mode)
echo [4/5] Installing required packages...
echo.

:: Create requirements.txt if not exists
if not exist "requirements.txt" (
    (
        echo streamlit>=1.28.0
        echo pandas>=2.0.0
        echo requests>=2.31.0
        echo groq>=0.4.0
    ) > requirements.txt
)

:: Install packages one by one silently
set PACKAGES=streamlit pandas requests groq
for %%p in (%PACKAGES%) do (
    echo    Installing %%p...
    python -m pip install %%p --quiet --upgrade --no-warn-script-location >nul 2>nul
    if !errorlevel! neq 0 (
        echo    [RETRY] Retrying %%p...
        python -m pip install %%p --quiet --upgrade --no-warn-script-location >nul 2>nul
    )
    echo    [DONE] %%p installed
)
echo.
echo [SUCCESS] All packages installed
echo.

:: Step 5: Check core files
echo [5/5] Verifying application files...
echo.

if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo.
    echo Please make sure the following files are in this folder:
    echo   1. main.py
    echo   2. core.py
    echo.
    pause
    exit /b 1
)

if not exist "core.py" (
    echo [WARNING] core.py not found!
    echo The application may not work correctly.
    echo.
)

echo [SUCCESS] Application files verified
echo.

:: Create necessary folders silently
if not exist "history" mkdir history >nul 2>nul
if not exist ".client_locks" mkdir .client_locks >nul 2>nul

:: Launch application
cls
echo ============================================================
echo    🚀 LAUNCHING AI LEAD SCRAPER PRO 🚀
echo ============================================================
echo.
echo    Status: Starting Streamlit server...
echo    URL: http://localhost:8501
echo.
echo    IMPORTANT:
echo    - Do NOT close this window while using the app
echo    - Your browser will open automatically in 3 seconds
echo    - Press Ctrl+C in this window to stop the server
echo.
echo ============================================================
echo.

:: Open browser after 3 seconds
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:8501"

:: Run streamlit
streamlit run main.py --server.address localhost --server.port 8501 --browser.gatherUsageStats false

:: If streamlit fails, try alternative
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start Streamlit!
    echo.
    echo Trying alternative method...
    python -m streamlit run main.py --server.address localhost --server.port 8501
)

pause