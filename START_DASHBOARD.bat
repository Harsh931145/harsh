@echo off
echo ============================================
echo   EXAM DASHBOARD - COMPLETE STARTUP
echo ============================================
echo.

echo Step 1: Starting Backend...
start "Backend Server" cmd /k "cd backend && python main.py"

timeout /t 5 /nobreak >nul

echo Step 2: Starting Frontend...
start "Frontend Server" cmd /k "cd frontend && call npm start"

echo.
echo ============================================
echo   SERVERS STARTING
echo ============================================
echo.
echo Backend:  http://localhost:8001
echo Frontend: http://localhost:3000
echo.
echo Wait a few moments, then browser will open automatically.
echo.
echo Close this window after servers start.
echo ============================================
echo.
timeout /t 3 /nobreak >nul
