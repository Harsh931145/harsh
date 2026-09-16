import os
from typing import Tuple, List, Optional
from openai import OpenAI
from .knowledge_base import KnowledgeBase
from .answer_prompts import (
    EXACT_ANSWER_SYSTEM_PROMPT,
    EXACT_IMAGE_QUESTION_TEMPLATE,
    EXACT_TEXT_QUESTION_TEMPLATE,
)


class MetaService:
    """Handle AI-powered question answering using Meta Muse Glimmer (FREE via NVIDIA)"""
    
    def __init__(self, knowledge_base: KnowledgeBase):
        self.knowledge_base = knowledge_base
        self.api_key = os.getenv("META_API_KEY")
        self.model = os.getenv("META_MODEL", "meta/muse-glimmer-30b")
        
        if not self.api_key:
            print("WARNING: META_API_KEY not set. AI features will not work.")
            self.client = None
        else:
            # Meta Muse via NVIDIA uses OpenAI-compatible API
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://integrate.api.nvidia.com/v1"
            )
            print(f"🤖 Meta Muse Glimmer initialized with model: {self.model}")
    
    async def answer_question(
        self, 
        question: str, 
        image_base64: Optional[str] = None
    ) -> Tuple[str, List[str], float]:
        """
        Answer a question using logical reasoning and keyword matching
        Supports both text and image inputs (multimodal)
        
        Args:
            question: The user's question
            image_base64: Optional base64-encoded image (screenshot)
            
        Returns:
            Tuple of (answer, sources, confidence)
        """
        if not self.client:
            return (
                "AI service not configured. Please set META_API_KEY in .env file. Get a FREE key at https://build.nvidia.com/",
                [],
                0.0
            )
        
        try:
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
            
            # Generate answer using Meta Muse with multimodal support
            answer = await self._generate_logical_answer(question, context, image_base64)
            
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
    
    async def _generate_logical_answer(self, question: str, context: str, image_base64: Optional[str] = None) -> str:
        """Generate answer using Meta Muse API with logical reasoning and multimodal support"""
        try:
            # Build messages with multimodal support
            messages = [
                {
                    "role": "system",
                    "content": EXACT_ANSWER_SYSTEM_PROMPT
                }
            ]
            
            # Add user message with optional image
            if image_base64:
                # Meta Muse supports multimodal input
                user_content = [
                    {
                        "type": "text",
                        "text": EXACT_IMAGE_QUESTION_TEMPLATE.format(
                            question=question,
                            context=context,
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    }
                ]
                messages.append({
                    "role": "user",
                    "content": user_content
                })
            else:
                # Text-only query
                messages.append({
                    "role": "user",
                    "content": EXACT_TEXT_QUESTION_TEMPLATE.format(
                        question=question,
                        context=context,
                    )
                })
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0,
                max_tokens=80,
            )
            
            return chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error calling Meta Muse API: {str(e)}")
