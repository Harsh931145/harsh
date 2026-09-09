import os
from typing import Tuple, List, Optional
from groq import Groq
from .knowledge_base import KnowledgeBase


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
            # Note: Groq doesn't support vision yet, so we'll handle text only
            if image_base64:
                question = f"{question}\n\n(Note: Image uploaded but Groq doesn't support vision yet. Please describe the image content or use text questions.)"
            
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
            
            # Generate answer using Groq with logical reasoning
            answer = await self._generate_logical_answer(question, context)
            
            # Calculate confidence based on relevance scores and keyword matching
            avg_relevance = sum(chunk['relevance_score'] for chunk in relevant_chunks) / len(relevant_chunks)
            confidence = min(avg_relevance * 1.3, 1.0)  # Higher weight for logical matches
            
            return answer, sources, confidence
            
        except Exception as e:
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
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert exam preparation assistant with strong logical reasoning abilities. Your role is to provide precise, accurate answers to exam questions based on the provided study materials.

Guidelines:
- Use LOGICAL REASONING to connect concepts and draw conclusions
- Look for KEYWORDS and RELATED TERMS in the study materials
- Even if exact words don't match, use logical inference to find the answer
- Answer questions directly and concisely
- If the question involves calculations, show step-by-step work
- If explaining concepts, be clear and structured
- Use analogies and examples when helpful
- For multiple choice questions, explain the reasoning for the correct answer
- Connect related concepts even if they use different terminology
- Format answers with bullet points or numbered lists when appropriate

IMPORTANT: Use logical thinking and keyword analysis. The answer might be expressed differently in the study materials - look for the underlying concepts and meaning."""
                    },
                    {
                        "role": "user",
                        "content": f"""Based on the following exam materials, please answer this question using logical reasoning and keyword analysis:

Question: {question}

Relevant Study Materials:
{context}

Instructions:
1. Analyze the question to identify key concepts and keywords
2. Look for related information in the study materials (even if worded differently)
3. Use logical reasoning to connect concepts
4. Provide a precise, well-reasoned answer

Please provide your answer:"""
                    }
                ],
                model="openai/gpt-oss-120b",  # Current active Groq model (as of 2024)
                temperature=0.2,
                max_tokens=1500,
            )
            
            return chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error calling Groq API: {str(e)}")
