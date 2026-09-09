@echo off
echo ============================================
echo   FINDING WORKING GROQ MODEL
echo ============================================
echo.

cd backend

echo Step 1: Testing which Groq models work...
python test_groq_models.py

echo.
echo.
echo Step 2: Restarting backend with updated model...
echo.
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

python main.py

pause
