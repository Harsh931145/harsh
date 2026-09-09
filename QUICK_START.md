# 🚀 Quick Start Guide

## Before You Start

You need an **OpenAI API Key**. Get one here: https://platform.openai.com/api-keys

## Setup (One Time Only)

### Step 1: Add Your API Key

1. Open the file: `backend/.env`
2. Replace `your_api_key_here` with your actual OpenAI API key
3. Save the file

Example:
```env
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

## Running the Dashboard

### Option 1: Automatic Startup (Easiest)

**Double-click `START_HERE.bat`**

This will:
- Open two command windows (backend and frontend)
- Install all dependencies automatically
- Start both servers

Wait ~30 seconds, then open: **http://localhost:3000**

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install
npm start
```

## First Time Use

1. **Open Dashboard**: http://localhost:3000
2. **Click "Manage Documents"**
3. **Upload a PDF** with your exam materials
4. **Go back** and ask a question!

## Example Questions

- "What is the definition of photosynthesis?"
- "Explain Newton's second law"
- "What are the main causes of World War I?"
- Upload a screenshot of a question from your textbook

## Troubleshooting

### "OPENAI_API_KEY not set"
- Edit `backend/.env` and add your API key

### "Cannot connect to backend"
- Make sure backend is running on port 8000
- Check backend terminal for errors

### "Module not found" errors
- Run: `pip install -r requirements.txt` in backend folder
- Run: `npm install` in frontend folder

### PowerShell Script Execution Error
- Use the `.bat` files instead of PowerShell commands
- Or run in Command Prompt (cmd) instead of PowerShell

## Stop the Servers

Press `Ctrl+C` in each terminal window

## Need More Help?

See **SETUP.md** for detailed instructions.

---

**Ready?** Double-click `START_HERE.bat` to begin! 🎓
