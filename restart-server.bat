@echo off
REM Complete server restart with cache clearing for Windows

echo =========================================
echo   KCM Converter - Complete Restart
echo =========================================
echo.

cd /d "%~dp0"

REM Kill any running Python servers
echo Stopping any running servers...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *kcm*" 2>nul
timeout /t 2 /nobreak >nul

REM Clear all Python cache
echo Clearing Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul

echo.
echo Python cache cleared
echo.

REM Start fresh server
echo Starting fresh server...
cd kcm-converter
start "KCM Converter Server" python kcm_converter_server.py

timeout /t 3 /nobreak >nul

REM Open browser
start "" clipboard.html

echo.
echo =========================================
echo Server should now be running on port 5000
echo Check the server window for any errors
echo =========================================
pause
