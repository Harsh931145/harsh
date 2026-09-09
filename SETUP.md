# Complete Setup Guide

This guide will walk you through setting up the Exam Dashboard from scratch.

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.8 or higher installed
- [ ] Node.js 16 or higher installed
- [ ] npm (comes with Node.js)
- [ ] OpenAI API key (get one at https://platform.openai.com/api-keys)
- [ ] Git (optional, for cloning)
- [ ] Text editor (VS Code recommended)

### Verify Prerequisites

```bash
# Check Python version
python --version
# Should show Python 3.8.x or higher

# Check Node.js version
node --version
# Should show v16.x.x or higher

# Check npm version
npm --version
# Should show 7.x.x or higher
```

## Step-by-Step Installation

### Part 1: Backend Setup (15 minutes)

#### 1.1 Navigate to Backend
```bash
cd backend
```

#### 1.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in your terminal.

#### 1.3 Install Python Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- FastAPI and Uvicorn (web server)
- PyPDF2 (PDF processing)
- Sentence Transformers (embeddings)
- FAISS (vector search)
- OpenAI SDK
- Other dependencies

⏱️ **Time**: ~5 minutes (depending on internet speed)

#### 1.4 Configure Environment

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

#### 1.5 Add Your OpenAI API Key

Edit `backend/.env` file:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxx
PORT=8000
HOST=0.0.0.0
KNOWLEDGE_BASE_PATH=../knowledgebase
```

**How to get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Paste into `.env` file

#### 1.6 Test Backend

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Initializing knowledge base...
Knowledge base ready!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Visit http://localhost:8000 in your browser - you should see API info.

**Keep this terminal running!**

### Part 2: Frontend Setup (10 minutes)

#### 2.1 Open New Terminal

Keep backend running, open a NEW terminal window.

#### 2.2 Navigate to Frontend
```bash
cd frontend
```

#### 2.3 Install Node Dependencies
```bash
npm install
```

⏱️ **Time**: ~3 minutes

#### 2.4 Configure Environment (Optional)

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Only needed if your backend runs on different URL.

#### 2.5 Start Frontend

```bash
npm start
```

Your browser should automatically open to http://localhost:3000

You should see the Exam Dashboard interface!

## Part 3: First Use

### 3.1 Upload Study Materials

1. Click **"Manage Documents"** button in header
2. Click **"Upload PDF"** button
3. Select a PDF file with study materials
4. Wait for "Document uploaded successfully!" message

### 3.2 Ask Your First Question

1. Click back (X button) to return to main dashboard
2. Type a question related to your uploaded material
3. Click **"Get Answer"**
4. Wait for AI-generated response

### 3.3 Try Screenshot Feature

1. Take a screenshot of a question (use Snipping Tool/Screenshot app)
2. Click the 📷 camera icon in search box
3. Upload your screenshot
4. Click **"Get Answer"**
5. See extracted text and answer

## Troubleshooting Common Issues

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure you're in virtual environment
# You should see (venv) in terminal

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

---

**Problem**: `OPENAI_API_KEY not set`

**Solution**:
- Check `.env` file exists in `backend/` folder
- Verify API key is correct (no spaces)
- Make sure `.env` file is not named `.env.txt`

---

**Problem**: `Address already in use`

**Solution**:
```bash
# Change port in backend/.env
PORT=8001

# Or kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Problem**: Blank page or "Cannot connect to backend"

**Solution**:
1. Verify backend is running (check terminal with `python main.py`)
2. Check backend URL: http://localhost:8000
3. Edit `frontend/.env` if needed:
   ```env
   REACT_APP_API_URL=http://localhost:8000
   ```
4. Restart frontend (`Ctrl+C` then `npm start`)

---

**Problem**: `npm: command not found`

**Solution**:
- Install Node.js from https://nodejs.org/
- Restart terminal after installation
- Verify: `node --version`

---

**Problem**: Port 3000 already in use

**Solution**:
```bash
# Kill process on port 3000
# Windows
netstat -ano | findstr :3000
taskkill /PID <process_id> /F

# macOS/Linux
lsof -ti:3000 | xargs kill -9

# Or run on different port
# When prompted, type 'Y' to run on different port
```

## Verification Checklist

After setup, verify:

- [ ] Backend running at http://localhost:8000
- [ ] Frontend running at http://localhost:3000
- [ ] Can access dashboard in browser
- [ ] "Manage Documents" button works
- [ ] Can upload a PDF successfully
- [ ] Can ask a text question and get answer
- [ ] Can upload screenshot and get answer
- [ ] Answers show confidence scores
- [ ] Source documents are displayed

## Next Steps

- Upload all your exam materials
- Test with sample questions
- Explore document management features
- Try screenshot functionality
- Review API documentation at http://localhost:8000/docs

## Getting Help

If you encounter issues:

1. Check the error message in terminal
2. Review this troubleshooting section
3. Check backend logs for details
4. Verify all prerequisites are installed
5. Ensure API key is valid and has credits

## Production Deployment

For production use:

1. Set up proper authentication
2. Use environment-specific `.env` files
3. Build frontend: `npm run build`
4. Use production ASGI server (Gunicorn + Uvicorn)
5. Set up HTTPS
6. Configure CORS properly
7. Monitor API usage and costs

---

**Setup Time**: ~25 minutes
**Difficulty**: Beginner-friendly

Enjoy studying with your AI-powered exam assistant! 🎓
