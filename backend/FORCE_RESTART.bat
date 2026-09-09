@echo off
echo ============================================
echo   FORCE RESTART - SWITCHING TO GROQ
echo ============================================
echo.

echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul
echo Done!
echo.

echo Step 2: Installing Groq package...
pip install groq
echo.

echo Step 3: Verifying .env file...
echo Checking for GROQ_API_KEY...
findstr /C:"GROQ_API_KEY=gsk_" .env >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Groq API key found!
) else (
    echo ❌ ERROR: Groq API key not found in .env
    echo Please make sure .env has: GROQ_API_KEY=gsk_...
    pause
    exit /b 1
)
echo.

echo Step 4: Starting backend with Groq...
echo.
echo ============================================
echo   Look for: "✅ Using Groq AI (Free & Fast!)"
echo ============================================
echo.

python main.py

pause
