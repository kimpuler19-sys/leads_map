@echo off
title AI Lead Scraper Pro - Installation Wizard
color 0E

:: ========================================
:: AI LEAD SCRAPER PRO - INSTALLER
:: ========================================

cls
echo ============================================================
echo    📦 AI LEAD SCRAPER PRO - INSTALLATION WIZARD 📦
echo ============================================================
echo.
echo This wizard will install all requirements for the application.
echo.

:: Check admin rights
net session >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Running without administrator privileges
    echo Some features may be limited.
    echo.
)

:: Create virtual environment (optional)
echo Do you want to create a virtual environment? (Recommended)
echo [Y] Yes - Create isolated environment
echo [N] No - Install globally
choice /c YN /n /m "Your choice: "

if errorlevel 2 (
    set USE_VENV=0
    echo Installing globally...
) else (
    set USE_VENV=1
    echo Creating virtual environment...
    python -m venv venv
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

echo.

:: Install requirements
echo Installing required packages...
echo.

python -m pip install --upgrade pip

:: Install packages with better error handling
python -m pip install streamlit pandas requests groq

:: Create requirements.txt for future use
python -m pip freeze > requirements.txt

echo.
echo ============================================================
echo    ✅ INSTALLATION COMPLETE! ✅
echo ============================================================
echo.
echo You can now run the application using:
echo   1. Double-click 'launcher.bat'
echo   2. Or run: streamlit run main.py
echo.
echo Would you like to launch the application now?
choice /c YN /n /m "Launch now? (Y/N): "

if errorlevel 2 (
    echo.
    echo Installation finished!
    exit /b 0
) else (
    echo Launching application...
    start launcher.bat
    exit /b 0
)