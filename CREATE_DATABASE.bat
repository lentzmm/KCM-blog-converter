@echo off
echo ========================================
echo   Creating Notion Conversion Database
echo ========================================
echo.

cd /d "%~dp0"

python create_notion_database.py

echo.
pause
