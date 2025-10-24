@echo off
REM Sync latest changes from git and restart with clean cache

echo =========================================
echo   KCM Converter - Sync and Restart
echo =========================================
echo.

cd /d "%~dp0"

echo [1/5] Pulling latest changes from git...
git pull origin claude/file-cleanup-011CUQjdtDvLeqouejGocfab
if errorlevel 1 (
    echo ERROR: Git pull failed
    pause
    exit /b 1
)
echo.

echo [2/5] Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *kcm*" 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.

echo [3/5] Clearing ALL Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo Python cache cleared!
echo.

echo [4/5] Starting fresh server...
cd kcm-converter
start "KCM Converter Server" python kcm_converter_server.py
timeout /t 3 /nobreak >nul
echo.

echo [5/5] Opening browser...
start "" clipboard.html
echo.

echo =========================================
echo DONE! Server running with latest code
echo All fixes are now active:
echo - Categories/tags use proper names
echo - Images named with focus keyphrase
echo - No Claude thinking text in output
echo =========================================
pause
