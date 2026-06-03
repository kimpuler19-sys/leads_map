@echo off
title AI Lead Scraper Pro - Dependency Fixer
color 0C

cls
echo ============================================================
echo    🔧 DEPENDENCY FIXER - AI LEAD SCRAPER PRO 🔧
echo ============================================================
echo.
echo This tool will fix common dependency issues.
echo.

:: Clear pip cache
echo [1/4] Clearing pip cache...
python -m pip cache purge
echo Done!
echo.

:: Reinstall core packages
echo [2/4] Reinstalling core packages...
python -m pip uninstall streamlit pandas requests groq -y
python -m pip install --no-cache-dir streamlit pandas requests groq
echo Done!
echo.

:: Check for updates
echo [3/4] Checking for updates...
python -m pip install --upgrade streamlit pandas requests groq
echo Done!
echo.

:: Verify installation
echo [4/4] Verifying installation...
python -c "import streamlit; import pandas; import requests; import groq; print('All packages imported successfully!')"
if %errorlevel% neq 0 (
    echo [ERROR] Some packages failed to install!
    echo.
    echo Try running this fixer as Administrator
    echo Or install manually: pip install streamlit pandas requests groq
) else (
    echo [SUCCESS] All packages are working!
)
echo.

echo ============================================================
echo    ✅ DEPENDENCY FIX COMPLETE! ✅
echo ============================================================
echo.
echo You can now run 'launcher.bat' to start the application.
echo.
pause