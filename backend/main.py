from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
import base64
import shutil
from pathlib import Path

from backend.services.pdf_processor import PDFProcessor
from backend.services.knowledge_base import KnowledgeBase
from backend.services.ai_service import AIService
from backend.services.groq_service import GroqService
from backend.services.xai_service import XAIService
from backend.services.meta_service import MetaService
from backend.services.fallback_ai_service import FallbackAIService
from backend.services.gemini_service import GeminiService
# Load environment variables
load_dotenv()

app = FastAPI(title="Dashboard API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
BUNDLED_KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "knowledgebase"
DEFAULT_KNOWLEDGE_BASE_VALUES = {
    "",
    "../knowledgebase",
    "knowledgebase",
    "/app/knowledgebase",
}


def resolve_knowledge_base_path() -> tuple[str, bool]:
    """Use Railway persistent volumes automatically when available."""
    configured_path = (os.getenv("KNOWLEDGE_BASE_PATH") or "").strip()
    volume_mount = (os.getenv("RAILWAY_VOLUME_MOUNT_PATH") or "").strip()

    if volume_mount and configured_path in DEFAULT_KNOWLEDGE_BASE_VALUES:
        return str(Path(volume_mount) / "knowledgebase"), True

    if configured_path:
        return configured_path, False

    return str(BUNDLED_KNOWLEDGE_BASE_PATH), False


def seed_persistent_knowledge_base(target_path: str, is_persistent: bool) -> None:
    """Copy bundled PDFs into a fresh persistent volume without overwriting uploads."""
    if not is_persistent or not BUNDLED_KNOWLEDGE_BASE_PATH.exists():
        return

    target = Path(target_path)
    target.mkdir(parents=True, exist_ok=True)

    copied = 0
    for source_pdf in BUNDLED_KNOWLEDGE_BASE_PATH.glob("*.pdf"):
        target_pdf = target / source_pdf.name
        if not target_pdf.exists():
            shutil.copy2(source_pdf, target_pdf)
            copied += 1

    if copied:
        print(f"Seeded {copied} bundled PDFs into persistent knowledge base: {target}")


# Initialize services
knowledge_base_path, knowledge_base_is_persistent = resolve_knowledge_base_path()
seed_persistent_knowledge_base(knowledge_base_path, knowledge_base_is_persistent)
pdf_processor = PDFProcessor()
knowledge_base = KnowledgeBase(knowledge_base_path)

# Choose AI service based on available API keys.
USE_META = os.getenv("META_API_KEY") and os.getenv("META_API_KEY") != "" and os.getenv("META_API_KEY") != "your_meta_api_key_here"
USE_GEMINI = os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_API_KEY") != ""
USE_XAI = os.getenv("XAI_API_KEY") and os.getenv("XAI_API_KEY") != "" and os.getenv("XAI_API_KEY") != "your_xai_api_key_here"
USE_GROQ = os.getenv("GROQ_API_KEY") and os.getenv("GROQ_API_KEY") != ""
USE_OPENAI = os.getenv("OPENAI_API_KEY") and os.getenv("OPENAI_API_KEY") != ""

provider_label = "None"

if USE_GEMINI and USE_GROQ:
    print("✅ Using Gemini primary + Groq fallback")
    ai_service = FallbackAIService([
        ("Gemini", GeminiService(knowledge_base)),
        ("Groq", GroqService(knowledge_base)),
    ])
    provider_label = "Gemini primary + Groq fallback"
elif USE_GEMINI:
    print("✅ Using Gemini AI")
    ai_service = GeminiService(knowledge_base)
    provider_label = "Gemini"
elif USE_META:
    print("✅ Using Meta Muse Glimmer (FREE via NVIDIA! - Multimodal Text+Image)")
    ai_service = MetaService(knowledge_base)
    provider_label = "Meta Muse Glimmer"
elif USE_XAI:
    print("✅ Using xAI Grok (Advanced AI!)")
    ai_service = XAIService(knowledge_base)
    provider_label = "xAI Grok"
elif USE_GROQ:
    print("✅ Using Groq AI (Free & Fast!)")
    ai_service = GroqService(knowledge_base)
    provider_label = "Groq (Free)"
elif USE_OPENAI:
    print("✅ Using OpenAI")
    ai_service = AIService(knowledge_base)
    provider_label = "OpenAI"
else:
    print("⚠️  No AI service configured!")
    print("Get FREE Meta Muse key at: https://build.nvidia.com/meta/muse-glimmer-30b")
    print("Or get Groq key at: https://console.groq.com/")
    ai_service = GroqService(knowledge_base)  # Will show error message


class QuestionRequest(BaseModel):
    question: str
    image_base64: Optional[str] = None


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float


@app.on_event("startup")
async def startup_event():
    """Initialize knowledge base on startup"""
    print("Initializing knowledge base...")
    await knowledge_base.initialize()
    print("Knowledge base ready!")


@app.get("/")
async def root():
    return {
        "message": "Dashboard API",
        "version": "1.0.0",
        "build": os.getenv("RAILWAY_GIT_COMMIT_SHA", "local"),
        "ocr": "tesseract",
        "knowledge_base_path": knowledge_base_path,
        "persistent_storage": knowledge_base_is_persistent,
        "ai_provider": provider_label,
        "status": "Ready" if (USE_META or USE_GEMINI or USE_XAI or USE_GROQ or USE_OPENAI) else "⚠️ No AI configured",
        "get_free_key": "https://aistudio.google.com/app/apikey or https://console.groq.com/" if not (USE_META or USE_GEMINI or USE_XAI or USE_GROQ or USE_OPENAI) else None,
        "endpoints": {
            "/ask": "POST - Ask a question (text or with image)",
            "/upload": "POST - Upload PDF to knowledge base",
            "/documents": "GET - List all documents",
            "/refresh": "POST - Refresh knowledge base",
        }
    }


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer a question using the knowledge base.
    Supports both text questions and questions with images (screenshots).
    """
    try:
        # Process the question
        answer, sources, confidence = await ai_service.answer_question(
            question=request.question,
            image_base64=request.image_base64
        )
        
        return AnswerResponse(
            answer=answer,
            sources=sources,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask-multipart")
async def ask_question_multipart(
    question: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """
    Alternative endpoint that accepts multipart form data.
    Useful for direct file uploads from frontend.
    """
    try:
        image_base64 = None
        if image:
            image_bytes = await image.read()
            image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        
        answer, sources, confidence = await ai_service.answer_question(
            question=question,
            image_base64=image_base64
        )
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document to the knowledge base with progress tracking"""
    import time
    start_time = time.time()
    
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Get file size for logging
        content = await file.read()
        file_size_mb = len(content) / (1024 * 1024)
        
        print(f"📄 Uploading: {file.filename} ({file_size_mb:.2f} MB)")
        
        # Save file to knowledge base directory
        file_path = os.path.join(knowledge_base_path, file.filename)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        upload_time = time.time() - start_time
        print(f"✅ File saved in {upload_time:.2f}s")
        
        # Process the new PDF (this takes the most time)
        process_start = time.time()
        await knowledge_base.add_document(file_path)
        process_time = time.time() - process_start
        
        total_time = time.time() - start_time
        
        print(f"✅ Processing completed in {process_time:.2f}s")
        print(f"📊 Total time: {total_time:.2f}s for {file_size_mb:.2f} MB ({file_size_mb/total_time:.2f} MB/s)")
        
        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "path": file_path,
            "size_mb": round(file_size_mb, 2),
            "upload_time_sec": round(upload_time, 2),
            "processing_time_sec": round(process_time, 2),
            "total_time_sec": round(total_time, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all documents in the knowledge base"""
    try:
        documents = knowledge_base.list_documents()
        return {
            "count": len(documents),
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/refresh")
async def refresh_knowledge_base():
    """Refresh the knowledge base (re-process all documents)"""
    try:
        await knowledge_base.refresh()
        return {
            "message": "Knowledge base refreshed successfully",
            "documents": knowledge_base.list_documents(),
        }
    except Exception as e:
        print(f"Error refreshing knowledge base: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{filename}")
async def delete_document(filename: str):
    """Delete a document from the knowledge base"""
    try:
        await knowledge_base.delete_document(filename)
        return {"message": f"Document {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(app, host=host, port=port)
