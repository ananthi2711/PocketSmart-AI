@echo off
title PocketSmart AI Launcher
echo ========================================================
echo               PocketSmart AI Launcher
echo     "Your Smart Budget & Recommendation Assistant"
echo ========================================================
echo.

:: Move to script directory
cd /d "%~dp0"

:: Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo [INFO] Activating virtual environment (.venv)...
    call .venv\Scripts\activate.bat
) else (
    echo [NOTICE] .venv not found. Using system Python...
)

echo [INFO] Starting PocketSmart AI via Streamlit...
echo [INFO] URL: http://localhost:8501
echo.

python -m streamlit run app.py

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Application terminated with error code %ERRORLEVEL%.
    pause
)
