import os
from typing import Tuple, List, Optional
import base64
from io import BytesIO
from PIL import Image
import openai
from .knowledge_base import KnowledgeBase
from .image_utils import image_data_url
from .ocr_service import extract_text_with_tesseract
from .answer_selector import (
    answer_from_retrieved_material,
    build_search_question,
    confidence_from_material_answer,
    select_answer_from_material,
)
from .answer_prompts import (
    EXACT_ANSWER_SYSTEM_PROMPT,
    EXACT_RETRY_QUESTION_TEMPLATE,
    EXACT_RETRY_SYSTEM_PROMPT,
    EXACT_TEXT_QUESTION_TEMPLATE,
    OCR_EXTRACTION_PROMPT,
    is_unhelpful_answer,
    normalize_exact_answer,
)


class AIService:
    """Handle AI-powered question answering using OpenAI API"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("WARNING: OPENAI_API_KEY not set. AI features will not work.")
        else:
            openai.api_key = self.api_key
    
    async def answer_question(
        self, 
        question: str, 
        image_base64: Optional[str] = None
    ) -> Tuple[str, List[str], float]:
        """
        Answer a question using the knowledge base
        
        Args:
            question: The user's question
            image_base64: Optional base64-encoded image (screenshot)
            
        Returns:
            Tuple of (answer, sources, confidence)
        """
        if not self.api_key:
            return (
                "AI service not configured. Please set OPENAI_API_KEY in .env file.",
                [],
                0.0
            )
        
        try:
            # Extract text from image if provided
            image_text = ""
            if image_base64:
                image_text = await self._extract_text_from_image(image_base64)
                question = build_search_question(question, image_text)
            
            # Search knowledge base for relevant context
            relevant_chunks = self.knowledge_base.search(question, top_k=12)
            
            if not relevant_chunks:
                return (
                    "I couldn't find relevant information in the knowledge base. Please upload exam materials first.",
                    [],
                    0.0
                )
            
            # Prepare context from relevant chunks
            context = self._prepare_context(relevant_chunks)
            sources = list(set([chunk['filename'] for chunk in relevant_chunks]))

            local_answer = select_answer_from_material(question, relevant_chunks)
            if local_answer:
                return local_answer, sources, confidence_from_material_answer(
                    local_answer,
                    question,
                    relevant_chunks,
                )
            
            # Generate answer using OpenAI
            answer = await self._generate_answer(question, context)
            material_answer = answer_from_retrieved_material(question, relevant_chunks)
            if is_unhelpful_answer(answer) and material_answer:
                return material_answer, sources, confidence_from_material_answer(
                    material_answer,
                    question,
                    relevant_chunks,
                )
            
            # Calculate confidence based on relevance scores
            avg_relevance = sum(chunk['relevance_score'] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.2, 1.0)  # Scale up slightly
            
            return answer, sources, confidence
            
        except Exception as e:
            return f"Error generating answer: {str(e)}", [], 0.0
    
    async def _extract_text_from_image(self, image_base64: str) -> str:
        """Extract text from image using OpenAI Vision API"""
        local_text = extract_text_with_tesseract(image_base64)
        if local_text:
            return local_text

        try:
            # Use OpenAI GPT-4 Vision to extract text
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": OCR_EXTRACTION_PROMPT
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data_url(image_base64)
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                timeout=20.0
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""
    
    def _prepare_context(self, relevant_chunks: List[dict]) -> str:
        """Prepare context from relevant document chunks"""
        context_parts = []
        
        for i, chunk in enumerate(relevant_chunks, 1):
            context_parts.append(
                f"[Source {i}: {chunk['filename']}]\n{chunk['content']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    async def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using OpenAI GPT"""
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
            raise Exception(f"Error calling OpenAI API: {str(e)}")

    async def _create_completion(self, messages: list) -> Optional[str]:
        response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0,
                max_tokens=200,
                timeout=20.0
            )
        return response.choices[0].message.content
