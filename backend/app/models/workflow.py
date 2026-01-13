from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """
    The 'Memory' of the agent workflow.
    This dict is passed between all nodes in the graph.
    """
    # Inputs
    query: str                # The user's original request
    context: List[str]        # Retrieved RAG chunks
    
    # Internal State
    draft: Optional[str]      # The current content being written
    critique: Optional[str]   # The editor's feedback
    revision_count: int       # Safety breaker to prevent infinite loops
    
    # Output
    final_doc: Optional[str]  # The approved text

# --- NEW: Request Model for API ---
class GenerateRequest(BaseModel):
    """
    Schema for triggering the Agentic Workflow.
    """
    topic: str = Field(..., description="The subject to write about (e.g., 'HMP155 Power Requirements').")
    tone: str = Field("technical", description="Desired tone: 'technical', 'marketing', or 'summary'.")