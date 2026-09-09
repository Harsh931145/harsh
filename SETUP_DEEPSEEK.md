# 🚀 Setup DeepSeek AI (FREE!)

## What is DeepSeek?

DeepSeek is a powerful, FREE AI model available through NVIDIA's API platform. It's excellent for logical reasoning and exam questions!

---

## ✨ Why DeepSeek?

✅ **100% FREE** - No credit card needed!  
✅ **Fast responses** - Quick inference  
✅ **Great reasoning** - Excellent for exam questions  
✅ **Easy setup** - Just get API key from NVIDIA  

---

## 🎯 Quick Setup (3 Steps)

### Step 1: Get FREE API Key

1. Go to: **https://build.nvidia.com/**
2. Sign in with your email or Google/GitHub
3. Find "DeepSeek V4 Pro" model
4. Click **"Get API Key"** or **"Generate API Key"**
5. Copy the key (starts with `nvapi-...`)

### Step 2: Add to .env File

Edit `backend/.env`:

```env
DEEPSEEK_API_KEY=nvapi-your_actual_key_here
DEEPSEEK_MODEL=deepseek-ai/deepseek-v4-pro-0813
```

### Step 3: Restart Backend

```cmd
cd backend
taskkill /F /IM python.exe
python main.py
```

Look for: **"✅ Using DeepSeek AI (FREE via NVIDIA!)"**

---

## 📋 Complete .env Example

```env
# Option 1: DeepSeek AI (FREE via NVIDIA!) - Recommended!
DEEPSEEK_API_KEY=nvapi-abc123xyz789...
DEEPSEEK_MODEL=deepseek-ai/deepseek-v4-pro-0813

# Option 2: xAI Grok (fallback)
XAI_API_KEY=your_xai_api_key_here

# Option 3: Groq (fallback)
GROQ_API_KEY=gsk_...

PORT=8001
HOST=0.0.0.0
KNOWLEDGE_BASE_PATH=../knowledgebase
```

---

## 🎓 Priority Order

The system will use AI in this order:

1. **DeepSeek** (if key is set) ← Best for free!
2. **xAI Grok** (if key is set)
3. **Groq** (if key is set)
4. **OpenAI** (if key is set)

---

## 🔧 Different DeepSeek Models

NVIDIA offers different DeepSeek versions:

| Model | Description |
|-------|-------------|
| `deepseek-ai/deepseek-v4-pro-0813` | Latest, best quality |
| `deepseek-ai/deepseek-v3` | Faster, good quality |
| `deepseek-ai/deepseek-coder-6.7b` | Best for code |

Change in `.env`:
```env
DEEPSEEK_MODEL=deepseek-ai/deepseek-v3
```

---

## ✅ Verify It's Working

After restart, check:

1. Terminal shows: **"✅ Using DeepSeek AI (FREE via NVIDIA!)"**
2. Go to: http://localhost:8001
3. Should show: `"ai_provider": "DeepSeek AI (Free)"`
4. Upload PDF and ask question
5. Get answer!

---

## 🆘 Troubleshooting

### Error: "DEEPSEEK_API_KEY not set"
- Check `.env` file has the key
- Make sure it's not `your_deepseek_api_key_here`
- No spaces around `=` sign
- Restart backend

### Error: "Model not found"
- Your key might not have access to that model
- Try: `deepseek-ai/deepseek-v3`
- Check NVIDIA Build for available models

### Still using Groq?
- DeepSeek key might be invalid
- Check you copied the full key from NVIDIA
- Make sure key starts with `nvapi-`

---

## 💡 Tips

✅ **Get key from NVIDIA Build** - https://build.nvidia.com/  
✅ **No credit card required** - Completely free!  
✅ **Good rate limits** - Generous for personal use  
✅ **Great for students** - Perfect for exam prep  

---

## 🎯 Next Steps

1. Get your FREE key at https://build.nvidia.com/
2. Add to `backend/.env`
3. Restart backend
4. Start studying with DeepSeek AI!

---

**DeepSeek is FREE, fast, and perfect for exam preparation!** 🚀📚
