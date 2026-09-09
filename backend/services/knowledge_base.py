import os
import pickle
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from .pdf_processor import PDFProcessor


class KnowledgeBase:
    """Manage the document knowledge base with vector embeddings"""
    
    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = knowledge_base_path
        self.pdf_processor = PDFProcessor()
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dimension = 384
        
        # Initialize FAISS index
        self.index = None
        self.documents = []  # Store document chunks with metadata
        self.index_path = os.path.join(knowledge_base_path, '.index.faiss')
        self.docs_path = os.path.join(knowledge_base_path, '.documents.pkl')
        
    async def initialize(self):
        """Initialize or load existing knowledge base"""
        os.makedirs(self.knowledge_base_path, exist_ok=True)
        
        # Try to load existing index
        if os.path.exists(self.index_path) and os.path.exists(self.docs_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.docs_path, 'rb') as f:
                    self.documents = pickle.load(f)
                print(f"Loaded existing knowledge base with {len(self.documents)} chunks")
                return
            except Exception as e:
                print(f"Error loading existing index: {e}")
        
        # Create new index
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        
        # Process all PDFs in the knowledge base directory
        await self.refresh()
    
    async def add_document(self, pdf_path: str):
        """Add a new document to the knowledge base with optimized processing"""
        import time
        start_time = time.time()
        
        try:
            # Extract text from PDF
            extract_start = time.time()
            pdf_data = self.pdf_processor.extract_text_from_pdf(pdf_path)
            extract_time = time.time() - extract_start
            print(f"  📖 Text extraction: {extract_time:.2f}s")
            
            # Chunk the text
            chunk_start = time.time()
            chunks = self.pdf_processor.chunk_text(pdf_data['full_text'])
            chunk_time = time.time() - chunk_start
            print(f"  ✂️  Text chunking: {chunk_time:.2f}s ({len(chunks)} chunks)")
            
            # Create embeddings (this is the slowest part)
            embed_start = time.time()
            embeddings = self.embedding_model.encode(
                chunks,
                show_progress_bar=False,  # Disable progress bar for speed
                batch_size=32  # Process in batches for efficiency
            )
            embed_time = time.time() - embed_start
            print(f"  🧠 Embeddings: {embed_time:.2f}s")
            
            # Add to FAISS index
            index_start = time.time()
            self.index.add(np.array(embeddings).astype('float32'))
            
            # Store document chunks with metadata
            for i, chunk in enumerate(chunks):
                self.documents.append({
                    'filename': pdf_data['metadata']['filename'],
                    'chunk_id': i,
                    'content': chunk,
                    'source': pdf_path
                })
            
            # Save index and documents
            self._save_index()
            index_time = time.time() - index_start
            print(f"  💾 Indexing: {index_time:.2f}s")
            
            total_time = time.time() - start_time
            print(f"  ✅ Total: {total_time:.2f}s for {len(chunks)} chunks")
            
        except Exception as e:
            raise Exception(f"Error adding document: {str(e)}")
    
    async def refresh(self):
        """Refresh the entire knowledge base by reprocessing all PDFs"""
        # Clear existing data
        self.index = faiss.IndexFlatL2(self.embedding_dimension)
        self.documents = []
        
        # Process all PDF files
        pdf_files = [f for f in os.listdir(self.knowledge_base_path) if f.endswith('.pdf')]
        
        if not pdf_files:
            print("No PDF files found in knowledge base directory")
            return
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(self.knowledge_base_path, pdf_file)
            try:
                await self.add_document(pdf_path)
            except Exception as e:
                print(f"Error processing {pdf_file}: {e}")
        
        print(f"Knowledge base refreshed with {len(self.documents)} total chunks")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """
        Enhanced search with keyword expansion and logical reasoning
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of relevant document chunks with scores
        """
        if not self.documents or self.index.ntotal == 0:
            return []
        
        # Expand query with related terms for better matching
        expanded_query = self._expand_query(query)
        
        # Create query embedding with expanded terms
        query_embedding = self.embedding_model.encode([expanded_query])
        
        # Search more results initially for better filtering
        search_k = min(top_k * 3, len(self.documents))
        
        # Search in FAISS index
        distances, indices = self.index.search(
            np.array(query_embedding).astype('float32'), 
            search_k
        )
        
        # Prepare results with enhanced scoring
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                
                # Calculate base relevance score
                base_score = float(1 / (1 + dist))
                
                # Boost score if keywords match
                keyword_boost = self._calculate_keyword_boost(query, doc['content'])
                
                # Final score combines semantic similarity and keyword matching
                doc['relevance_score'] = min(base_score * (1 + keyword_boost), 1.0)
                results.append(doc)
        
        # Sort by relevance score and return top_k
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        return results[:top_k]
    
    def _expand_query(self, query: str) -> str:
        """
        Expand query with related terms and logical variations
        Helps find answers even when exact words don't match
        """
        # Common exam question patterns and expansions
        expansions = {
            'what is': 'definition meaning explanation describe',
            'how to': 'method process steps procedure way',
            'why': 'reason cause purpose explanation',
            'difference between': 'compare contrast versus vs distinction',
            'advantage': 'benefit pro positive merit',
            'disadvantage': 'drawback con negative limitation',
            'example': 'instance case illustration sample',
            'types of': 'kinds categories classifications forms',
            'define': 'definition meaning explanation',
            'explain': 'describe clarify elaborate detail',
            'list': 'enumerate mention name identify',
            'calculate': 'compute solve find determine',
            'prove': 'demonstrate show verify establish',
            'compare': 'difference contrast similar versus',
        }
        
        expanded = query.lower()
        for pattern, terms in expansions.items():
            if pattern in expanded:
                expanded += ' ' + terms
        
        return expanded
    
    def _calculate_keyword_boost(self, query: str, content: str) -> float:
        """
        Calculate boost score based on keyword matching
        Helps prioritize chunks with important matching terms
        """
        # Extract keywords from query (remove common words)
        stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'in', 'on', 'at', 
                     'to', 'for', 'of', 'and', 'or', 'but', 'what', 'how', 'why', 
                     'when', 'where', 'which', 'who', 'that', 'this', 'these', 'those'}
        
        query_words = set(query.lower().split()) - stop_words
        content_lower = content.lower()
        
        # Count keyword matches
        matches = sum(1 for word in query_words if len(word) > 2 and word in content_lower)
        
        # Boost score based on match ratio
        if len(query_words) > 0:
            match_ratio = matches / len(query_words)
            return match_ratio * 0.3  # Up to 30% boost
        
        return 0.0
    
    def list_documents(self) -> List[str]:
        """List all unique documents in the knowledge base"""
        pdf_files = [f for f in os.listdir(self.knowledge_base_path) if f.endswith('.pdf')]
        return pdf_files
    
    async def delete_document(self, filename: str):
        """Delete a document from the knowledge base"""
        file_path = os.path.join(self.knowledge_base_path, filename)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            # Refresh the knowledge base to rebuild index without this document
            await self.refresh()
        else:
            raise FileNotFoundError(f"Document {filename} not found")
    
    def _save_index(self):
        """Save the FAISS index and documents to disk"""
        faiss.write_index(self.index, self.index_path)
        with open(self.docs_path, 'wb') as f:
            pickle.dump(self.documents, f)
