# 🚀 Setup xAI Grok for Exam Dashboard

## What is xAI Grok?

xAI Grok is Elon Musk's advanced AI model. It's powerful and has great reasoning abilities!

---

## Quick Setup

### Step 1: Add Your xAI API Key

Edit `backend/.env` file and replace:

```env
XAI_API_KEY=your_actual_xai_key_here
```

**Where to get xAI API key:**
- Visit: https://x.ai/
- Sign up and get your API key
- Or use the model: `grok-beta`

### Step 2: (Optional) Change Model

If you want to use a specific Grok model, edit `.env`:

```env
XAI_MODEL=grok-beta
```

Or if you mentioned `gpt-oss-120b`, use:
```env
XAI_MODEL=gpt-oss-120b
```

### Step 3: Restart Backend

```cmd
cd backend
taskkill /F /IM python.exe
python main.py
```

You should see: **"✅ Using xAI Grok (Advanced AI!)"**

---

## Priority Order

The system will use AI in this priority:

1. **xAI Grok** (if `XAI_API_KEY` is set)
2. **Groq** (if `GROQ_API_KEY` is set)
3. **OpenAI** (if `OPENAI_API_KEY` is set)

---

## Your Current .env File

```env
# Option 1: xAI Grok (Use this!)
XAI_API_KEY=your_xai_api_key_here
XAI_MODEL=grok-beta

# Option 2: Groq API (Fallback)
GROQ_API_KEY=your_groq_api_key_here
```

---

## Testing

After adding your xAI key:

1. Start backend: `python main.py`
2. Check terminal shows: "✅ Using xAI Grok"
3. Upload PDF
4. Ask question
5. Get answer from Grok!

---

## Troubleshooting

**Error: "XAI_API_KEY not set"**
- Make sure you edited `.env` correctly
- No spaces around the `=` sign
- Key should not be in quotes

**Error: "Model not found"**
- Check your xAI account for available models
- Try: `grok-beta` or the model you have access to
- Update `XAI_MODEL` in `.env`

**Still using Groq instead of xAI?**
- Make sure `XAI_API_KEY` is not `your_xai_api_key_here`
- Restart backend after editing `.env`

---

## Benefits of xAI Grok

✅ Advanced reasoning  
✅ Great at logical thinking  
✅ Fast responses  
✅ Good at understanding context  

---

**Add your xAI API key to `.env` and restart the backend!** 🚀
