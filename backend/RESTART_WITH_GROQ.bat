@echo off
echo ============================================
echo   RESTARTING WITH GROQ API
echo ============================================
echo.

echo Step 1: Installing Groq package...
pip install groq
echo.

echo Step 2: Stopping any running backend...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>nul
timeout /t 2 /nobreak >nul
echo.

echo Step 3: Starting backend with Groq...
echo.
python main.py

pause
