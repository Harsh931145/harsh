@echo off
echo ========================================
echo Petpooja Exam Dashboard - Starting...
echo ========================================
echo.

REM Start Backend
echo Starting Backend Server...
start "Petpooja Backend" cmd /k "cd /d %~dp0backend && python main.py"
timeout /t 5 /nobreak >nul

REM Start Frontend
echo Starting Frontend Dashboard...
start "Petpooja Frontend" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ========================================
echo Services Starting!
echo ========================================
echo.
echo Backend will be available at: http://localhost:8001
echo Frontend will be available at: http://localhost:3000
echo.
echo Wait 10-15 seconds for services to fully start
echo Then open: http://localhost:3000
echo.
echo Press any key to exit this window...
pause >nul
