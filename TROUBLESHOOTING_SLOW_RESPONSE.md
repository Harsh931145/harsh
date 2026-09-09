# 🐌 Troubleshooting: Slow Response / No Answer

## Problem
Dashboard shows "Searching knowledge base..." for a long time and answer never comes.

---

## Common Causes & Solutions

### 1. **Backend Not Running** ❌

**Check:** Is the backend terminal still open and running?

**Fix:**
```cmd
cd c:\Users\Petpooja-607\Desktop\pkt\backend
python main.py
```

---

### 2. **Backend Error (Most Common)** 🔴

**Check:** Look at backend terminal - do you see error messages?

**Common Errors:**
- ❌ "GROQ_API_KEY not set"
- ❌ "Error calling Groq API"
- ❌ "ModuleNotFoundError: No module named 'groq'"

**Fix:**
```cmd
pip install groq
python main.py
```

---

### 3. **Wrong Port / Connection Issue** 🔌

**Check:** Backend running on port 8001?

**Fix:**
1. Check backend terminal - should show: `Uvicorn running on http://0.0.0.0:8001`
2. Check frontend `.env` has: `REACT_APP_API_URL=http://localhost:8001`

---

### 4. **No PDF Uploaded** 📄

**Check:** Did you upload any PDF files?

**Fix:**
1. Click "Manage Documents"
2. Upload at least one PDF
3. Wait for "Document uploaded successfully!"
4. Go back and ask question

---

### 5. **First Time Loading Models** ⏰

**Issue:** First question takes 30-60 seconds (downloading AI models)

**Fix:** Just wait - subsequent questions will be fast!

---

### 6. **Groq API Key Invalid** 🔑

**Check:** Is your Groq API key correct?

**Fix:**
1. Open `backend/.env`
2. Verify `GROQ_API_KEY=gsk_...` (should start with `gsk_`)
3. Get new key at: https://console.groq.com/ if needed
4. Restart backend

---

## Quick Diagnostic Steps

### Step 1: Check Backend Terminal

Look for these messages:

**✅ GOOD:**
```
✅ Using Groq AI (Free & Fast!)
INFO:     Uvicorn running on http://0.0.0.0:8001
Initializing knowledge base...
Knowledge base ready!
```

**❌ BAD:**
```
ERROR: ...
ModuleNotFoundError: ...
⚠️ No AI service configured
```

### Step 2: Test Backend Directly

Open browser, go to: `http://localhost:8001`

**✅ Should see:**
```json
{
  "message": "Exam Dashboard API",
  "ai_provider": "Groq (Free)",
  "status": "Ready"
}
```

**❌ If page doesn't load:** Backend not running!

### Step 3: Check Browser Console

Press **F12** in browser, check Console tab for errors.

**Common errors:**
- `Failed to fetch` → Backend not running
- `Network error` → Wrong port
- `CORS error` → Backend needs restart

---

## Fastest Fix (Try This First!) ⚡

1. **Stop everything:**
   - Close backend terminal (Ctrl+C)
   - Close browser

2. **Fresh start:**
   ```cmd
   cd c:\Users\Petpooja-607\Desktop\pkt\backend
   pip install groq
   python main.py
   ```
   
   Wait for: `✅ Using Groq AI (Free & Fast!)`

3. **Start frontend:**
   ```cmd
   cd c:\Users\Petpooja-607\Desktop\pkt\frontend
   npm start
   ```

4. **Upload PDF first** before asking questions

5. **Ask simple question:** "What is this about?"

---

## Still Not Working?

### Check These Files:

**1. Backend `.env`:**
```env
GROQ_API_KEY=gsk_your_actual_key_here
PORT=8001
```

**2. Frontend `.env`:**
```env
REACT_APP_API_URL=http://localhost:8001
```

**3. Backend running on correct port:**
Look for: `Uvicorn running on http://0.0.0.0:8001`

---

## Expected Timing ⏱️

| Action | Time |
|--------|------|
| First question (models loading) | 30-60 seconds |
| Subsequent questions | 2-5 seconds |
| PDF upload | 5-10 seconds |
| Backend startup | 10-15 seconds |

---

## If Response Takes > 60 Seconds

**Stop and check backend terminal for errors!**

Most likely causes:
1. Groq package not installed
2. API key invalid
3. No PDFs uploaded
4. Backend crashed

---

## Need Help?

1. Check backend terminal for error messages
2. Check browser console (F12) for errors
3. Try restarting both backend and frontend
4. Make sure you uploaded at least one PDF

---

**Quick fix: Restart everything and upload PDF first!** 📚
