"""
Test script to find which Groq models are currently available
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("ERROR: GROQ_API_KEY not set")
    exit(1)

client = Groq(api_key=api_key)

# Test different model names
models_to_try = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant", 
    "llama3-70b-8192",
    "llama3-8b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
    "gemma2-9b-it",
]

print("Testing Groq models...")
print("=" * 50)

for model in models_to_try:
    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hi"}],
            model=model,
            max_tokens=10
        )
        print(f"✅ {model} - WORKS!")
    except Exception as e:
        error_msg = str(e)
        if "decommissioned" in error_msg.lower():
            print(f"❌ {model} - Decommissioned")
        elif "not found" in error_msg.lower() or "does not exist" in error_msg.lower():
            print(f"❌ {model} - Does not exist")
        else:
            print(f"⚠️  {model} - Error: {error_msg[:50]}")

print("=" * 50)
print("\nUse a model marked with ✅ in your code!")
