@echo off
echo ========================================
echo Petpooja Exam Dashboard - Stopping...
echo ========================================
echo.

REM Stop Python (Backend)
echo Stopping Backend Server...
taskkill /F /IM python.exe >nul 2>&1
if %errorlevel%==0 (
    echo Backend stopped successfully
) else (
    echo No backend running
)

REM Stop Node (Frontend)
echo Stopping Frontend Dashboard...
taskkill /F /IM node.exe >nul 2>&1
if %errorlevel%==0 (
    echo Frontend stopped successfully
) else (
    echo No frontend running
)

echo.
echo ========================================
echo All services stopped!
echo ========================================
echo.
pause
