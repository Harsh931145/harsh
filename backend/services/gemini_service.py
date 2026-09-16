import os
from typing import List, Optional, Tuple

import httpx

from .answer_prompts import (
    EXACT_ANSWER_SYSTEM_PROMPT,
    EXACT_RETRY_QUESTION_TEMPLATE,
    EXACT_RETRY_SYSTEM_PROMPT,
    EXACT_TEXT_QUESTION_TEMPLATE,
    is_unhelpful_answer,
    normalize_exact_answer,
)
from .answer_selector import (
    IMAGE_TEXT_UNREADABLE_MESSAGE,
    answer_from_retrieved_material,
    build_search_question,
    confidence_from_material_answer,
    is_placeholder_image_question,
    select_answer_from_material,
)
from .knowledge_base import KnowledgeBase
from .ocr_service import extract_text_with_tesseract


class GeminiService:
    """Handle AI-powered question answering using Google Gemini API."""

    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

        if not self.api_key:
            print("WARNING: GEMINI_API_KEY not set. Gemini features will not work.")
        else:
            print(f"🤖 Gemini initialized with model: {self.model}")

    async def answer_question(
        self,
        question: str,
        image_base64: Optional[str] = None,
    ) -> Tuple[str, List[str], float]:
        if not self.api_key:
            return (
                "AI service not configured. Please set GEMINI_API_KEY in environment variables.",
                [],
                0.0,
            )

        try:
            if image_base64:
                image_text = extract_text_with_tesseract(image_base64)
                if image_text:
                    print(f"Image OCR extracted {len(image_text)} characters")
                elif is_placeholder_image_question(question):
                    return IMAGE_TEXT_UNREADABLE_MESSAGE, [], 0.0
                question = build_search_question(question, image_text)

            relevant_chunks = self.knowledge_base.search(question, top_k=8)

            if not relevant_chunks:
                return (
                    "I couldn't find relevant information in the knowledge base. Please upload exam materials first.",
                    [],
                    0.0,
                )

            sources = list(set([chunk["filename"] for chunk in relevant_chunks]))

            local_answer = select_answer_from_material(question, relevant_chunks)
            if local_answer:
                return local_answer, sources, confidence_from_material_answer(
                    local_answer,
                    question,
                    relevant_chunks,
                )

            context = self._prepare_context(relevant_chunks)
            answer = await self._generate_answer(question, context)
            material_answer = answer_from_retrieved_material(question, relevant_chunks)
            if is_unhelpful_answer(answer) and material_answer:
                return material_answer, sources, confidence_from_material_answer(
                    material_answer,
                    question,
                    relevant_chunks,
                )

            avg_relevance = sum(chunk["relevance_score"] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.3, 1.0)

            return answer, sources, confidence

        except Exception as e:
            return f"Error generating answer: {str(e)}", [], 0.0

    def _prepare_context(self, relevant_chunks: List[dict]) -> str:
        context_parts = []
        for index, chunk in enumerate(relevant_chunks, 1):
            relevance = chunk.get("relevance_score", 0)
            context_parts.append(
                f"[Source {index}: {chunk['filename']} | Relevance: {relevance:.2f}]\n{chunk['content']}\n"
            )
        return "\n---\n".join(context_parts)

    async def _generate_answer(self, question: str, context: str) -> str:
        answer = await self._create_completion(
            system_prompt=EXACT_ANSWER_SYSTEM_PROMPT,
            user_prompt=EXACT_TEXT_QUESTION_TEMPLATE.format(
                question=question,
                context=context,
            ),
        )
        if not is_unhelpful_answer(answer):
            return normalize_exact_answer(answer)

        retry_answer = await self._create_completion(
            system_prompt=EXACT_RETRY_SYSTEM_PROMPT,
            user_prompt=EXACT_RETRY_QUESTION_TEMPLATE.format(
                question=question,
                context=context,
            ),
        )
        return normalize_exact_answer(retry_answer)

    async def _create_completion(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/{self.model}:generateContent"
        )
        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}],
            },
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0,
                "maxOutputTokens": 80,
            },
        }

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "x-goog-api-key": self.api_key,
                },
                json=payload,
            )

        if response.status_code >= 400:
            raise Exception(f"Error calling Gemini API: {response.status_code} - {response.text}")

        data = response.json()
        candidates = data.get("candidates") or []
        if not candidates:
            raise Exception("Error calling Gemini API: no answer returned")

        parts = candidates[0].get("content", {}).get("parts") or []
        text_parts = [part.get("text", "") for part in parts if part.get("text")]
        return "\n".join(text_parts).strip()
