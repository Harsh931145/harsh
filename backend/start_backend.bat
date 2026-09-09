@echo off
echo Starting Backend Server...
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your API key
    echo.
    echo Get FREE Groq API key at: https://console.groq.com/
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Installing dependencies...
pip install fastapi uvicorn python-multipart PyPDF2 sentence-transformers faiss-cpu pillow python-dotenv openai pydantic numpy langchain langchain-community groq

echo.
echo ============================================
echo   EXAM DASHBOARD BACKEND
echo ============================================
echo.
echo Checking AI configuration...
echo.
echo If you see "No AI service configured":
echo 1. Get FREE Groq API key at: https://console.groq.com/
echo 2. Add it to backend/.env file
echo 3. See GET_FREE_API_KEY.md for detailed steps
echo.
echo Starting FastAPI server...
echo Backend will be available at http://localhost:8001
echo Press Ctrl+C to stop
echo.

python main.py
