# Meta Muse Glimmer 30B Setup Guide

## Overview
Meta Muse Glimmer is a **FREE multimodal AI model** from NVIDIA that supports:
- ✅ Text-only questions
- ✅ Image + text questions (screenshots)
- ✅ Logical reasoning
- ✅ 30B parameters - high quality answers

## Getting Your FREE API Key

1. Visit: https://build.nvidia.com/meta/muse-glimmer-30b
2. Click **"Generate API Key"** button (top right)
3. Copy the API key (starts with `nvapi-...`)

## Configuration

1. Open `backend/.env`
2. Replace `your_meta_api_key_here` with your actual key:

```env
META_API_KEY=nvapi-YOUR_ACTUAL_KEY_HERE
META_MODEL=meta/muse-glimmer-30b
```

3. Restart the backend:
```bash
cd backend
# Stop any running backend
taskkill /F /IM python.exe

# Start fresh
python main.py
```

## Verification

You should see:
```
✅ Using Meta Muse Glimmer (FREE via NVIDIA! - Multimodal Text+Image)
🤖 Meta Muse Glimmer initialized with model: meta/muse-glimmer-30b
```

## Features

### Text Questions
Ask any exam question:
- "What is the difference between TCP and UDP?"
- "Explain the concept of inheritance in OOP"
- "Calculate the compound interest for..."

### Image + Text Questions
Paste screenshots (Ctrl+V) and ask:
- "Solve this math problem" (with screenshot of equation)
- "Explain this diagram" (with screenshot of flowchart)
- "What's wrong with this code?" (with screenshot of code)

### Logical Reasoning
The system will:
- Search your uploaded PDFs for relevant content
- Use keywords and related terms
- Apply logical reasoning to connect concepts
- Provide precise, well-structured answers

## Advantages of Meta Muse

1. **Multimodal Support**: Works with both text and images
2. **FREE**: Unlimited usage via NVIDIA
3. **High Quality**: 30B parameter model
4. **Fast**: Good response times
5. **Latest Model**: Updated 29 days ago

## Priority Order

The system checks API keys in this order:
1. **Meta Muse** (Multimodal - best for screenshots)
2. DeepSeek (Text-only, but powerful)
3. xAI Grok (Advanced, requires key)
4. Groq (Fast fallback)
5. OpenAI (Paid, not recommended)

## Troubleshooting

### Error: 403 Authorization Failed
- Your API key is invalid or expired
- Generate a new key at https://build.nvidia.com/meta/muse-glimmer-30b
- Make sure you're logged in to NVIDIA

### Error: Model Not Found
- Check that `META_MODEL=meta/muse-glimmer-30b` in `.env`
- Verify the model name matches the NVIDIA documentation

### Backend Not Starting
- Make sure Python dependencies are installed: `pip install -r requirements.txt`
- Check if port 8001 is available
- Look for error messages in the console

## Testing

1. Start backend (should show "Using Meta Muse Glimmer")
2. Open dashboard at http://localhost:3000
3. Try text question: "What is Python?"
4. Try image question: Paste a screenshot (Ctrl+V) and ask about it
5. Check confidence score and sources

## Support

For issues:
- NVIDIA API Docs: https://docs.api.nvidia.com/
- Meta Muse Model Page: https://build.nvidia.com/meta/muse-glimmer-30b
- Check backend logs for detailed error messages
