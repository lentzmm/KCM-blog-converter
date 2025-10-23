@echo off
echo ============================================
echo   KCM Blog Converter - South Jersey
echo ============================================
echo.
echo Starting server...
echo Server will run on http://localhost:5000
echo.
echo Opening web interface in your browser...
echo.
start clipboard.html
echo.
echo Server is running. Press CTRL+C to stop.
echo ============================================
echo.
py kcm_converter_server.py
