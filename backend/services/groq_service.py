import asyncio
import os
from typing import Tuple, List, Optional
from groq import Groq
from .knowledge_base import KnowledgeBase
from .ocr_service import extract_text_with_tesseract
from .answer_selector import (
    IMAGE_TEXT_UNREADABLE_MESSAGE,
    answer_from_retrieved_material,
    build_search_question,
    confidence_from_material_answer,
    is_placeholder_image_question,
    select_answer_from_material,
)
from .answer_prompts import (
    EXACT_ANSWER_SYSTEM_PROMPT,
    EXACT_RETRY_QUESTION_TEMPLATE,
    EXACT_RETRY_SYSTEM_PROMPT,
    EXACT_TEXT_QUESTION_TEMPLATE,
    is_unhelpful_answer,
    normalize_exact_answer,
)


class GroqService:
    """Handle AI-powered question answering using Groq API (FREE!)"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            print("WARNING: GROQ_API_KEY not set. AI features will not work.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)
    
    async def answer_question(
        self, 
        question: str, 
        image_base64: Optional[str] = None
    ) -> Tuple[str, List[str], float]:
        """
        Answer a question using logical reasoning and keyword matching
        
        Args:
            question: The user's question
            image_base64: Optional base64-encoded image (screenshot)
            
        Returns:
            Tuple of (answer, sources, confidence)
        """
        if not self.client:
            return (
                "AI service not configured. Please set GROQ_API_KEY in .env file. Get a free key at https://console.groq.com/",
                [],
                0.0
            )
        
        try:
            if image_base64:
                image_text = extract_text_with_tesseract(image_base64)
                if image_text:
                    print(f"Image OCR extracted {len(image_text)} characters")
                elif is_placeholder_image_question(question):
                    return IMAGE_TEXT_UNREADABLE_MESSAGE, [], 0.0
                question = build_search_question(question, image_text)
            
            # Enhanced search with more results for better logical matching
            relevant_chunks = self.knowledge_base.search(question, top_k=8)
            
            if not relevant_chunks:
                return (
                    "I couldn't find relevant information in the knowledge base. Please upload exam materials first.",
                    [],
                    0.0
                )
            
            # Prepare context with logical connections
            context = self._prepare_enhanced_context(relevant_chunks, question)
            sources = list(set([chunk['filename'] for chunk in relevant_chunks]))

            local_answer = select_answer_from_material(question, relevant_chunks)
            if local_answer:
                return local_answer, sources, confidence_from_material_answer(
                    local_answer,
                    question,
                    relevant_chunks,
                )
            
            # Generate answer using Groq with logical reasoning
            answer = await self._generate_logical_answer(question, context)
            material_answer = answer_from_retrieved_material(question, relevant_chunks)
            if is_unhelpful_answer(answer) and material_answer:
                return material_answer, sources, confidence_from_material_answer(
                    material_answer,
                    question,
                    relevant_chunks,
                )
            
            # Calculate confidence based on relevance scores and keyword matching
            avg_relevance = sum(chunk['relevance_score'] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.3, 1.0)  # Higher weight for logical matches
            
            return answer, sources, confidence
            
        except Exception as e:
            if _is_rate_limit_error(e):
                return (
                    "Groq rate limit reached. Please wait a minute and try again.",
                    [],
                    0.0,
                )
            return f"Error generating answer: {str(e)}", [], 0.0
    
    def _prepare_context(self, relevant_chunks: List[dict]) -> str:
        """Prepare context from relevant document chunks"""
        context_parts = []
        
        for i, chunk in enumerate(relevant_chunks, 1):
            context_parts.append(
                f"[Source {i}: {chunk['filename']}]\n{chunk['content']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def _prepare_enhanced_context(self, relevant_chunks: List[dict], question: str) -> str:
        """
        Prepare context with emphasis on logical connections and keywords
        """
        context_parts = []
        
        # Extract keywords from question
        question_keywords = set(question.lower().split())
        
        for i, chunk in enumerate(relevant_chunks, 1):
            # Highlight relevance score
            relevance = chunk.get('relevance_score', 0)
            context_parts.append(
                f"[Source {i}: {chunk['filename']} | Relevance: {relevance:.2f}]\n{chunk['content']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    async def _generate_logical_answer(self, question: str, context: str) -> str:
        """Generate answer using Groq API with logical reasoning emphasis"""
        try:
            messages = [
                    {
                        "role": "system",
                        "content": EXACT_ANSWER_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": EXACT_TEXT_QUESTION_TEMPLATE.format(
                            question=question,
                            context=context,
                        )
                    }
                ]

            answer = await self._create_completion(messages)
            if not is_unhelpful_answer(answer):
                return normalize_exact_answer(answer)

            retry_messages = [
                {
                    "role": "system",
                    "content": EXACT_RETRY_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": EXACT_RETRY_QUESTION_TEMPLATE.format(
                        question=question,
                        context=context,
                    )
                }
            ]
            return normalize_exact_answer(await self._create_completion(retry_messages))
            
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")

    async def _create_completion(self, messages: list) -> Optional[str]:
        for attempt in range(2):
            try:
                chat_completion = self.client.chat.completions.create(
                    messages=messages,
                    model="openai/gpt-oss-120b",
                    temperature=0,
                    max_tokens=80,
                )
                message = chat_completion.choices[0].message
                return getattr(message, "content", None)
            except Exception as e:
                if attempt == 0 and _is_rate_limit_error(e):
                    await asyncio.sleep(4)
                    continue
                raise


def _is_rate_limit_error(error: Exception) -> bool:
    message = str(error).lower()
    status_code = getattr(error, "status_code", None)
    return status_code == 429 or "rate limit" in message or "too many requests" in message
