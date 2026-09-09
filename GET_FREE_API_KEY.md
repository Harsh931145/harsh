# 🆓 Get Your FREE Groq API Key (2 Minutes)

## Why Groq?

- ✅ **100% FREE** - No credit card required!
- ✅ **Very Fast** - Faster than OpenAI for many tasks
- ✅ **Generous Limits** - More than enough for studying
- ✅ **Easy Setup** - Just like OpenAI

---

## Step-by-Step Guide

### 1. Visit Groq Console

Go to: **https://console.groq.com/**

### 2. Sign Up (30 seconds)

Click **"Sign Up"** and choose:
- Sign in with **Google**, or
- Sign in with **GitHub**, or
- Use email

### 3. Create API Key (30 seconds)

1. Once logged in, go to **"API Keys"** section
2. Click **"Create API Key"**
3. Give it a name (e.g., "Exam Dashboard")
4. Click **"Create"**
5. **Copy the key** (starts with `gsk_...`)

### 4. Add to Your Project (1 minute)

1. Open file: `backend/.env`
2. Find the line:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
3. Replace `your_groq_api_key_here` with your actual key:
   ```
   GROQ_API_KEY=gsk_abc123xyz789...
   ```
4. Save the file

### 5. Install Groq Package

Open Command Prompt in backend folder:
```bash
cd backend
pip install groq
```

### 6. Restart Backend Server

If backend is running:
1. Press Ctrl+C to stop
2. Run again: `python main.py`

---

## ✅ Done!

Your exam dashboard now uses **FREE Groq AI**!

Test it:
1. Upload a PDF with study materials
2. Ask a question
3. Get instant answers!

---

## Rate Limits (Free Tier)

Groq Free Tier includes:
- **30 requests per minute**
- **14,400 requests per day**

This is MORE than enough for personal exam prep! 🎓

---

## Need Help?

If you see errors:
1. Check your API key is copied correctly
2. Make sure no extra spaces in `.env` file
3. Restart the backend server

---

## Alternative: Use OpenAI

If you prefer OpenAI and have credits:
1. Keep your OpenAI key in `.env`
2. Comment out (add `#` before) the GROQ_API_KEY line
3. The system will automatically use OpenAI

The code supports BOTH! It will use Groq if available, otherwise OpenAI.

---

**Get started now: https://console.groq.com/** 🚀
