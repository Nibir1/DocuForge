from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI.
    Handles startup and shutdown logic.
    """
    # 1. Startup Logic
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} in {settings.ENVIRONMENT} mode...")
    logger.info(f"✅ Configuration loaded. Vector DB target: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
    
    yield
    
    # 2. Shutdown Logic
    logger.info(f"🛑 Shutting down {settings.PROJECT_NAME}...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint to verify container status.
    """
    return {
        "status": "active",
        "environment": settings.ENVIRONMENT,
        "service": "DocuForge API"
    }

if __name__ == "__main__":
    import uvicorn
    # Local development entry point
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)