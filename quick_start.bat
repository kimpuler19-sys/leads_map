@echo off
title AI Lead Scraper Pro
color 0A

:: Super simple launcher untuk client non-teknis

echo.
echo Starting AI Lead Scraper Pro...
echo Please wait...
echo.

:: Install packages if missing
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo First time setup - installing requirements...
    pip install streamlit pandas requests groq
    echo.
)

:: Run the app
streamlit run main.py

pause