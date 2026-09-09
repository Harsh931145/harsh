@echo off
echo ============================================
echo   EXAM DASHBOARD - STATUS CHECK
echo ============================================
echo.

echo 1. Checking if backend is running...
netstat -ano | findstr :8001
if %ERRORLEVEL% EQU 0 (
    echo ✅ Backend is running on port 8001
) else (
    echo ❌ Backend is NOT running!
    echo    Start it with: cd backend && python main.py
)
echo.

echo 2. Checking Groq API key...
findstr /C:"GROQ_API_KEY=gsk_" backend\.env >nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Groq API key is set
) else (
    echo ❌ Groq API key NOT found
    echo    Add it to backend\.env
)
echo.

echo 3. Checking if Groq is installed...
pip show groq >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Groq package is installed
) else (
    echo ❌ Groq package NOT installed
    echo    Run: pip install groq
)
echo.

echo 4. Checking knowledge base...
if exist knowledgebase\*.pdf (
    echo ✅ PDF files found in knowledge base
    dir /B knowledgebase\*.pdf
) else (
    echo ⚠️  No PDF files found
    echo    Upload PDFs using "Manage Documents"
)
echo.

echo 5. Testing backend API...
curl -s http://localhost:8001 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Backend API is responding
) else (
    echo ❌ Backend API not responding
    echo    Backend might not be running
)
echo.

echo ============================================
echo   SUMMARY
echo ============================================
echo.
echo If you see ❌ marks above, fix those issues!
echo.
pause
