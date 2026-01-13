from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from app.core.config import settings
from app.services.vector_db import VectorDBService
from app.core.logging import logger

class IngestionService:
    """
    Orchestrates the document processing pipeline:
    Raw Text -> Chunking -> Embedding -> Vector DB Storage
    """

    def __init__(self):
        self.vector_db = VectorDBService()
        
        # Initialize OpenAI Embeddings
        # We use text-embedding-3-small for cost/performance balance
        self.embeddings_model = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY,
            model="text-embedding-3-small"
        )
        
        # Initialize Text Splitter
        # Chunk size 1000 is standard for technical docs (approx 2-3 paragraphs)
        # Overlap 200 ensures context isn't lost between cuts
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", " ", ""]
        )

    async def process_document(self, text: str, source_name: str, metadata: dict):
        """
        Full pipeline execution for a single document.
        """
        logger.info(f"⚙️ Processing document: {source_name}")

        # 1. Split Text
        chunks = self.text_splitter.create_documents(
            texts=[text], 
            metadatas=[{"source": source_name, **metadata}]
        )
        logger.info(f"✂️ Split document into {len(chunks)} chunks.")

        if not chunks:
            return {"status": "skipped", "reason": "Text was empty"}

        # 2. Generate Embeddings
        texts_content = [chunk.page_content for chunk in chunks]
        
        try:
            vectors = self.embeddings_model.embed_documents(texts_content)
        except Exception as e:
            logger.error(f"❌ OpenAI Embedding failed: {e}")
            raise e

        # 3. Store in Qdrant
        # We store the text content in the payload so we can retrieve it later
        payloads = [
            {"content": chunk.page_content, **chunk.metadata}
            for chunk in chunks
        ]
        
        self.vector_db.upsert_vectors(vectors=vectors, payloads=payloads)
        
        return {"status": "success", "chunks_processed": len(chunks)}

    async def search_knowledge_base(self, query: str, limit: int = 3):
        """
        Converts query to vector -> searches Qdrant.
        """
        # 1. Embed Query
        query_vector = self.embeddings_model.embed_query(query)
        
        # 2. Search DB
        results = self.vector_db.search(query_vector, limit)
        
        # 3. Format Response
        formatted_results = [
            {
                "content": res.payload.get("content"),
                "source": res.payload.get("source"),
                "score": res.score
            }
            for res in results
        ]
        return formatted_results