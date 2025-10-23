@echo off
echo Testing KCM Converter Server...
echo.

REM Test if server is running
echo 1. Testing if server responds on http://localhost:5000/health
curl -X GET http://localhost:5000/health 2>nul
if errorlevel 1 (
    echo.
    echo ERROR: Server is not responding on http://localhost:5000
    echo.
    echo Please make sure:
    echo 1. The server is running (double-click start-kcm-converter.bat)
    echo 2. You see "Running on http://127.0.0.1:5000" in the server window
    echo 3. The server window is still open
) else (
    echo.
    echo SUCCESS: Server is running!
)

echo.
pause
