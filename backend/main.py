from fastapi import FastAPI, HTTPException
from fastapi import UploadFile, File
from contextlib import asynccontextmanager
from typing import Dict, Any

from app.core.config import settings
from app.core.logging import logger
from app.models.document import IngestRequest, SearchRequest
from app.models.workflow import GenerateRequest, AgentState
from app.services.ingestion import IngestionService
from app.agents.graph import app as agent_workflow

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
        # We allow startup even if DB fails, for easier debugging of API layer
    
    yield
    
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "active", "service": "DocuForge API"}

# --- Knowledge Base Endpoints ---

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

@app.post("/api/v1/ingest/file")
async def ingest_file(file: UploadFile = File(...)):
    """
    Uploads a PDF file, extracts text, and indexes it.
    """
    if not ingestion_service:
        raise HTTPException(status_code=503, detail="Ingestion service not initialized")
    
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        result = await ingestion_service.process_pdf(file)
        return result
    except Exception as e:
        logger.error(f"File upload error: {e}")
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

# --- Agentic Workflow Endpoint (NEW) ---

@app.post("/api/v1/generate")
async def generate_documentation(request: GenerateRequest) -> Dict[str, Any]:
    """
    Triggers the Multi-Agent Drafting Workflow.
    1. Retrieves context from Qdrant based on the topic.
    2. Initializes the LangGraph state.
    3. Runs the Draft -> Critique -> Revise loop.
    4. Returns the final result.
    """
    if not ingestion_service:
        raise HTTPException(status_code=503, detail="Services not ready")

    logger.info(f"🤖 Starting Agent Workflow for topic: {request.topic}")

    # Step 1: Retrieve Context (Grounding)
    # We blindly search for the topic to give the agent raw material
    search_results = await ingestion_service.search_knowledge_base(query=request.topic, limit=5)
    
    # Flatten results into a list of strings
    context_str_list = [
        f"Source ({res['source']}): {res['content']}" 
        for res in search_results
    ]
    
    if not context_str_list:
        logger.warning(f"⚠️ No context found for topic: {request.topic}")
        context_str_list = ["No specific technical context found in database. Rely on general knowledge but be cautious."]

    # Step 2: Initialize State
    initial_state: AgentState = {
        "query": request.topic,
        "context": context_str_list,
        "draft": None,
        "critique": None,
        "revision_count": 0,
        "final_doc": None
    }

    # Step 3: Run the Graph
    # invoke() is synchronous blocking in LangGraph (for now), but fast enough for this demo.
    # For production with long chains, we would use a background task (Celery/Arq).
    try:
        final_state = agent_workflow.invoke(initial_state)
    except Exception as e:
        logger.error(f"❌ Agent Workflow Failed: {e}")
        raise HTTPException(status_code=500, detail=f"Agent workflow failed: {str(e)}")

    # Step 4: Return Result
    # We return the draft and the last critique to show the 'thought process'
    return {
        "final_document": final_state.get("draft"),
        "revisions": final_state.get("revision_count"),
        "final_critique": final_state.get("critique"),
        "used_context": len(context_str_list)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)