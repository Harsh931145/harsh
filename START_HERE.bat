@echo off
echo ============================================
echo    EXAM DASHBOARD - STARTUP SCRIPT
echo ============================================
echo.

REM Check if .env exists in backend
if not exist backend\.env (
    echo ERROR: Backend .env file not found!
    echo.
    echo Please follow these steps:
    echo 1. Copy backend\.env.example to backend\.env
    echo 2. Edit backend\.env and add your OPENAI_API_KEY
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && start_backend.bat"

timeout /t 5 /nobreak >nul

echo Starting Frontend Server...
start "Frontend Server" cmd /k "cd frontend && start_frontend.bat"

echo.
echo ============================================
echo Both servers are starting in separate windows
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Wait a few moments for servers to start,
echo then open http://localhost:3000 in your browser
echo ============================================
echo.
pause
