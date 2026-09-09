import os
from typing import Tuple, List, Optional
import base64
from io import BytesIO
from PIL import Image
import openai
from .knowledge_base import KnowledgeBase


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
                if image_text:
                    question = f"{question}\n\nText from screenshot: {image_text}"
            
            # Search knowledge base for relevant context
            relevant_chunks = self.knowledge_base.search(question, top_k=5)
            
            if not relevant_chunks:
                return (
                    "I couldn't find relevant information in the knowledge base. Please upload exam materials first.",
                    [],
                    0.0
                )
            
            # Prepare context from relevant chunks
            context = self._prepare_context(relevant_chunks)
            sources = list(set([chunk['filename'] for chunk in relevant_chunks]))
            
            # Generate answer using OpenAI
            answer = await self._generate_answer(question, context)
            
            # Calculate confidence based on relevance scores
            avg_relevance = sum(chunk['relevance_score'] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.2, 1.0)  # Scale up slightly
            
            return answer, sources, confidence
            
        except Exception as e:
            return f"Error generating answer: {str(e)}", [], 0.0
    
    async def _extract_text_from_image(self, image_base64: str) -> str:
        """Extract text from image using OpenAI Vision API"""
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
                                "text": "Extract all text from this image. If it contains a question, mathematical formula, or diagram, describe it clearly."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000
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
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert exam preparation assistant. Your role is to provide precise, accurate answers to exam questions based on the provided study materials.

Guidelines:
- Answer questions directly and concisely
- Use information from the provided context
- If the question involves calculations, show step-by-step work
- If explaining concepts, be clear and structured
- If the context doesn't contain enough information, acknowledge it
- For multiple choice questions, explain why the correct answer is right
- Format answers with bullet points or numbered lists when appropriate"""
                    },
                    {
                        "role": "user",
                        "content": f"""Based on the following exam materials, please answer this question:

Question: {question}

Relevant Study Materials:
{context}

Please provide a precise, well-structured answer."""
                    }
                ],
                temperature=0.3,
                max_tokens=1500
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error calling OpenAI API: {str(e)}")
