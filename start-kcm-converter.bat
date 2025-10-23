@echo off
REM KCM Converter Startup Script
REM Starts the Flask server and opens the browser interface

echo ========================================
echo   KCM Blog Converter - Starting...
echo ========================================
echo.

REM Change to the kcm-converter directory
cd /d "%~dp0kcm-converter"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Starting Flask server...
echo Server will run on http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Wait 2 seconds then open browser
start /b timeout /t 2 /nobreak >nul && start "" "%~dp0kcm-converter\clipboard.html"

REM Start the Python server (this will block until Ctrl+C)
python kcm_converter_server.py

REM This only runs after Ctrl+C
echo.
echo Server stopped.
pause
