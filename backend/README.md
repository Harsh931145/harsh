# Backend API Documentation

## Overview

FastAPI-based backend for the Exam Dashboard that handles PDF processing, vector search, and AI-powered question answering.

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env  # Then edit with your API key
```

## Running

```bash
python main.py
```

Server will start at `http://localhost:8000`

## API Documentation

Once running, visit:
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| OPENAI_API_KEY | Yes | - | Your OpenAI API key |
| PORT | No | 8000 | Server port |
| HOST | No | 0.0.0.0 | Server host |
| KNOWLEDGE_BASE_PATH | No | ../knowledgebase | Path to PDF storage |

## Project Structure

```
backend/
├── main.py                    # FastAPI application and routes
├── services/
│   ├── pdf_processor.py      # PDF text extraction
│   ├── knowledge_base.py     # Vector storage and search
│   └── ai_service.py         # OpenAI integration
├── requirements.txt          # Python dependencies
└── .env                      # Configuration (not in git)
```

## Key Services

### PDFProcessor
- Extracts text from PDF files
- Chunks text with overlap for better context

### KnowledgeBase
- Manages document embeddings using Sentence Transformers
- Provides semantic search using FAISS
- Persists index to disk

### AIService
- Generates answers using OpenAI GPT-4
- Processes images with GPT-4 Vision
- Includes prompt engineering for exam contexts

## Development

### Adding New Endpoints

Edit `main.py` and add your route:

```python
@app.get("/new-endpoint")
async def new_endpoint():
    return {"message": "Hello"}
```

### Testing

```bash
# Test with curl
curl http://localhost:8000/documents

# Upload a PDF
curl -X POST -F "file=@test.pdf" http://localhost:8000/upload

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is AI?"}'
```

## Performance Considerations

- **Embedding Model**: Uses `all-MiniLM-L6-v2` (fast, good quality)
- **Index Type**: FAISS FlatL2 (exact search, good for <1M vectors)
- **Chunk Size**: 1000 characters with 200 character overlap

## Error Handling

All endpoints return proper HTTP status codes:
- `200`: Success
- `400`: Bad request (e.g., invalid file type)
- `404`: Not found
- `500`: Server error

Error responses include detail messages:
```json
{
  "detail": "Error description here"
}
```
