import os
from typing import Tuple, List, Optional
from openai import OpenAI
from .knowledge_base import KnowledgeBase
from .answer_prompts import (
    EXACT_ANSWER_SYSTEM_PROMPT,
    EXACT_TEXT_QUESTION_TEMPLATE,
    normalize_exact_answer,
)


class XAIService:
    """Handle AI-powered question answering using xAI Grok API"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("XAI_API_KEY")
        self.model = os.getenv("XAI_MODEL", "grok-beta")
        
        if not self.api_key:
            print("WARNING: XAI_API_KEY not set. AI features will not work.")
            self.client = None
        else:
            # xAI uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
    
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
                "AI service not configured. Please set XAI_API_KEY in .env file. Get a key at https://x.ai/",
                [],
                0.0
            )
        
        try:
            # Note: Check if Grok supports vision, for now handling text only
            if image_base64:
                question = f"{question}\n\n(Note: Image uploaded but vision support may be limited. Please describe the image content or use text questions.)"
            
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
            
            # Generate answer using Grok with logical reasoning
            answer = await self._generate_logical_answer(question, context)
            
            # Calculate confidence based on relevance scores and keyword matching
            avg_relevance = sum(chunk['relevance_score'] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.3, 1.0)
            
            return answer, sources, confidence
            
        except Exception as e:
            return f"Error generating answer: {str(e)}", [], 0.0
    
    def _prepare_enhanced_context(self, relevant_chunks: List[dict], question: str) -> str:
        """Prepare context with emphasis on logical connections and keywords"""
        context_parts = []
        
        for i, chunk in enumerate(relevant_chunks, 1):
            relevance = chunk.get('relevance_score', 0)
            context_parts.append(
                f"[Source {i}: {chunk['filename']} | Relevance: {relevance:.2f}]\n{chunk['content']}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    async def _generate_logical_answer(self, question: str, context: str) -> str:
        """Generate answer using xAI Grok with logical reasoning emphasis"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
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
                ],
                model=self.model,
                temperature=0,
                max_tokens=200,
            )
            
            return normalize_exact_answer(chat_completion.choices[0].message.content)
            
        except Exception as e:
            raise Exception(f"Error calling xAI Grok API: {str(e)}")
