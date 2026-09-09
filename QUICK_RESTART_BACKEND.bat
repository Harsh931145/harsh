@echo off
echo Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Starting backend with fixed Groq model...
cd backend
python main.py
