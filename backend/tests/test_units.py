import pytest
from app.models.workflow import AgentState, GenerateRequest
from app.models.document import IngestRequest

def test_ingest_request_validation():
    """Test that invalid ingest requests raise errors."""
    with pytest.raises(Exception):
        IngestRequest(text="Missing source") # Missing source_name
        
    req = IngestRequest(text="Valid text", source_name="doc.txt")
    assert req.text == "Valid text"

def test_generate_request_defaults():
    """Test default values for generation requests."""
    req = GenerateRequest(topic="HMP155")
    assert req.tone == "technical" # Default value

def test_agent_state_structure():
    """Ensure AgentState TypedDict accepts correct keys."""
    state: AgentState = {
        "query": "test",
        "context": ["data"],
        "draft": "draft",
        "critique": None,
        "revision_count": 0,
        "final_doc": None
    }
    assert state["query"] == "test"