from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger
from app.models.document import IngestRequest, SearchRequest
from app.services.ingestion import IngestionService

# Global Service Instances
ingestion_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager.
    Initializes services on startup.
    """
    global ingestion_service
    
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode...")
    
    # Initialize Logic Services (connects to Qdrant)
    try:
        ingestion_service = IngestionService()
        logger.info("✅ Ingestion Service initialized (Knowledge Base connected).")
    except Exception as e:
        logger.error(f"❌ Failed to initialize services: {e}")
        # We don't exit here, so the API stays up for debugging, but services won't work.
    
    yield
    
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "active", "service": "DocuForge API"}

# --- New Endpoints for Phase 2 ---

@app.post("/api/v1/ingest")
async def ingest_document(request: IngestRequest):
    """
    Upload text to the Knowledge Base.
    """
    if not ingestion_service:
        raise HTTPException(status_code=503, detail="Ingestion service not initialized")
        
    try:
        result = await ingestion_service.process_document(
            text=request.text,
            source_name=request.source_name,
            metadata=request.metadata
        )
        return result
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/search")
async def search_knowledge(request: SearchRequest):
    """
    Test semantic search against the Knowledge Base.
    """
    if not ingestion_service:
        raise HTTPException(status_code=503, detail="Ingestion service not initialized")
        
    results = await ingestion_service.search_knowledge_base(
        query=request.query,
        limit=request.limit
    )
    return {"matches": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)