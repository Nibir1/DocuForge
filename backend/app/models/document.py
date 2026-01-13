from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class IngestRequest(BaseModel):
    """
    Schema for uploading raw text content to the knowledge base.
    """
    text: str = Field(..., description="The raw content of the engineering note or specification.")
    source_name: str = Field(..., description="Filename or origin of the document (e.g., 'sensor_specs_v1.pdf').")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Arbitrary tags like version, author, date.")

class SearchRequest(BaseModel):
    """
    Schema for testing semantic search.
    """
    query: str = Field(..., description="The question or topic to search for.")
    limit: int = Field(3, description="Number of context chunks to retrieve.")

class DocumentChunk(BaseModel):
    """
    Represents a single piece of retrieved context.
    """
    content: str
    source: str
    score: float