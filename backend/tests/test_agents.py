from unittest.mock import MagicMock, patch
from app.agents.nodes import drafter_node, critic_node
from app.models.workflow import AgentState
from langchain_core.messages import AIMessage

class TestAgentNodes:
    
    @patch("app.agents.nodes.llm") # Mock the global LLM object in nodes.py
    def test_drafter_node(self, mock_llm):
        # Setup mock response
        mock_llm.invoke.return_value = AIMessage(content="Generated Draft Content")
        
        # Input state
        state: AgentState = {
            "query": "How to install?",
            "context": ["Context 1"],
            "draft": None,
            "critique": None,
            "revision_count": 0,
            "final_doc": None
        }
        
        # Run Node
        new_state = drafter_node(state)
        
        # Assertions
        assert new_state["draft"] == "Generated Draft Content"
        assert new_state["revision_count"] == 1
        # Verify prompt construction handled correctly (implicitly)

    @patch("app.agents.nodes.llm")
    def test_critic_node(self, mock_llm):
        # Setup mock response
        mock_llm.invoke.return_value = AIMessage(content="APPROVE")
        
        state: AgentState = {
            "query": "Test",
            "context": [],
            "draft": "Perfect draft",
            "critique": None,
            "revision_count": 1,
            "final_doc": None
        }
        
        new_state = critic_node(state)
        
        assert new_state["critique"] == "APPROVE"