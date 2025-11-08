@echo off
REM KCM Converter Startup Script - CLEAN VERSION
REM Clears cache and ensures fresh start
REM Created: 2025-11-07

echo ========================================
echo   KCM Blog Converter - CLEAN START
echo ========================================
echo.

REM Change to root directory
cd /d "%~dp0"

echo Step 1: Clearing Python cache...
echo.

REM Delete all __pycache__ folders
for /d /r . %%d in (__pycache__) do @if exist "%%d" (
    echo   Deleting: %%d
    rd /s /q "%%d" 2>nul
)

REM Delete all .pyc files
del /s /q "*.pyc" 2>nul

echo   Cache cleared!
echo.

echo Step 2: Checking which branch we're on...
git branch --show-current
echo.

echo Step 3: Checking Python version...
python --version
echo.

echo Step 4: Installing/updating dependencies...
pip install -r shared/requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo   Dependencies OK!
echo.

echo Step 5: Changing to kcm-converter directory...
cd /d "%~dp0kcm-converter"
echo.

echo Step 6: Verifying files exist...
echo   Checking for kcm_prompt_ACTIVE.md...
if exist "kcm_prompt_ACTIVE.md" (
    echo   ✓ Found
    REM Show first line (version)
    powershell -Command "Get-Content kcm_prompt_ACTIVE.md -First 1"
) else (
    echo   ✗ NOT FOUND - This is a problem!
    pause
    exit /b 1
)
echo.

echo   Checking for kcm_converter_server.py...
if exist "kcm_converter_server.py" (
    echo   ✓ Found
) else (
    echo   ✗ NOT FOUND - This is a problem!
    pause
    exit /b 1
)
echo.

echo   Checking for wordpress_taxonomy.py in shared folder...
if exist "%~dp0shared\wordpress_taxonomy.py" (
    echo   ✓ Found
) else (
    echo   ✗ NOT FOUND - This is a problem!
    pause
    exit /b 1
)
echo.

echo ========================================
echo   Starting Flask server...
echo   Server will run on http://localhost:5000
echo.
echo   WATCH FOR ERRORS in this window!
echo   If you see "Failed to generate SEO metadata"
echo   take a screenshot and send it to Claude
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
