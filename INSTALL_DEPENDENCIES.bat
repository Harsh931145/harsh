@echo off
echo ========================================
echo Petpooja Exam Dashboard - Installation
echo ========================================
echo.
echo This will install all required dependencies...
echo.
pause

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Python is installed
) else (
    echo [ERROR] Python not found! Please install Python 3.8+
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Node.js
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel%==0 (
    echo [OK] Node.js is installed
) else (
    echo [ERROR] Node.js not found! Please install Node.js 14+
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installing Backend Dependencies...
echo ========================================
cd /d %~dp0backend
pip install -r requirements.txt
if %errorlevel%==0 (
    echo [OK] Backend dependencies installed
) else (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installing Frontend Dependencies...
echo ========================================
cd /d %~dp0frontend
call npm install
if %errorlevel%==0 (
    echo [OK] Frontend dependencies installed
) else (
    echo [ERROR] Failed to install frontend dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Add your NVIDIA API key to backend\.env
echo    META_API_KEY=nvapi-YOUR_KEY_HERE
echo.
echo 2. Run START_ALL.bat to launch the dashboard
echo.
echo 3. Upload Petpooja PDFs in "Manage Documents"
echo.
pause
