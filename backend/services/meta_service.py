import os
from typing import Tuple, List, Optional
from openai import OpenAI
from .knowledge_base import KnowledgeBase


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
                    "content": """You are an expert Petpooja product specialist and MCQ exam assistant. You analyze screenshots of multiple-choice questions about Petpooja products and identify the correct answer.

PETPOOJA PRODUCTS CONTEXT:
- Petpooja POS: Point of Sale system for restaurants
- Petpooja Dashboard: Analytics and management dashboard
- Petpooja Payroll (Attendo): Employee attendance and payroll management
- Petpooja Finance: Financial management and accounting

MCQ ANALYSIS GUIDELINES:
1. CAREFULLY READ the question in the screenshot
2. IDENTIFY all available options (A, B, C, D or numbered options)
3. **CRITICAL: Look for the BOLD option - this is the correct answer**
4. The correct answer will be displayed in BOLD text in the screenshot
5. EXTRACT KEYWORDS from the question and bold answer
6. Provide reasoning based on Petpooja product knowledge

ANSWER FORMAT:
- Start with: "**Answer: [Option Letter/Number] - [Bold Option Text]**"
- Then provide brief reasoning explaining why this is correct
- Reference relevant study materials if available

VISUAL CUE PRIORITY:
1. **FIRST**: Identify which option is BOLD in the screenshot
2. **SECOND**: Extract the text of the bold option
3. **THIRD**: Provide reasoning based on product knowledge

REASONING APPROACH:
- Explain why the bold answer makes sense
- Connect to Petpooja product features and functionality
- Use keywords that match the question
- Reference study materials as supporting evidence
- Apply domain knowledge about POS, payroll, finance, and dashboard systems

IMPORTANT: 
- The correct answer is shown in BOLD in the screenshot
- Always look for bold text formatting first
- The bold option is always the correct answer
- Provide confident reasoning for the bold answer"""
                }
            ]
            
            # Add user message with optional image
            if image_base64:
                # Meta Muse supports multimodal input
                user_content = [
                    {
                        "type": "text",
                        "text": f"""Analyze this MCQ screenshot about Petpooja products and identify the correct answer.

CONTEXT: This is a multiple-choice question about Petpooja products (POS, Dashboard, Payroll/Attendo, Finance).

**IMPORTANT**: The correct answer is shown in **BOLD** text in the screenshot. Look for the bold option first!

YOUR TASK:
1. Look at the screenshot and identify which option is in BOLD text
2. The BOLD option is the correct answer
3. Read the question carefully
4. Extract keywords related to Petpooja products
5. Provide reasoning why the bold answer is correct

STUDY MATERIALS (for reference):
{context}

ADDITIONAL QUESTION/CONTEXT: {question}

Please provide:
- **Answer: [Option Letter/Number] - [Bold Option Text]** (always bold the answer)
- Reasoning: Explain why this bold answer is correct (2-3 sentences with Petpooja product knowledge)
- Keywords: Key terms from question and answer
- Confidence: High (since answer is provided in bold)

Remember: Look for the BOLD option in the screenshot - that is always the correct answer!"""
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
                    "content": f"""Answer this MCQ question about Petpooja products using the study materials.

CONTEXT: This is about Petpooja products (POS, Dashboard, Payroll/Attendo, Finance).

Question: {question}

STUDY MATERIALS:
{context}

INSTRUCTIONS:
1. Identify keywords in the question
2. Match with Petpooja product features from study materials
3. Use logical reasoning to find the correct answer
4. If options are provided in the question, select from those options

Please provide:
- Answer: [Clear answer or option]
- Reasoning: Why this is correct (keywords and logic)
- References: Which study materials support this answer"""
                })
            
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=self.model,
                temperature=0.2,
                max_tokens=1500,
            )
            
            return chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Error calling Meta Muse API: {str(e)}")
