import pytest
from unittest.mock import MagicMock, patch
from app.agents.graph import should_continue
from app.services.vector_db import VectorDBService

class TestGraphLogic:
    """Targeting app/agents/graph.py"""

    def test_should_continue_approve(self):
        """If critic approves, end the loop."""
        state = {"critique": "The text is perfect. APPROVE.", "revision_count": 0}
        assert should_continue(state) == "end"

    def test_should_continue_revise(self):
        """If critic rejects, go back to drafter."""
        state = {"critique": "Too passive.", "revision_count": 0}
        assert should_continue(state) == "revise"

    def test_should_continue_max_retries(self):
        """If max retries reached, force end."""
        state = {"critique": "Still bad.", "revision_count": 3}
        assert should_continue(state) == "end"

class TestVectorDBLogic:
    """Targeting app/services/vector_db.py"""

    def test_ensure_collection_creates_if_missing(self):
        """Test the initialization logic when collection is missing."""
        with patch("app.services.vector_db.QdrantClient") as MockClient:
            # Setup: Collection list is empty
            mock_instance = MockClient.return_value
            mock_instance.get_collections.return_value.collections = []
            
            # Run
            db = VectorDBService()
            
            # Assert create_collection was called
            mock_instance.create_collection.assert_called_once()

    def test_ensure_collection_skips_if_exists(self):
        """Test the initialization logic when collection exists."""
        with patch("app.services.vector_db.QdrantClient") as MockClient:
            # Setup: Collection exists
            mock_instance = MockClient.return_value
            mock_collection = MagicMock()
            mock_collection.name = "vaisala_docs"
            mock_instance.get_collections.return_value.collections = [mock_collection]
            
            # Run
            db = VectorDBService()
            
            # Assert create_collection was NOT called
            mock_instance.create_collection.assert_not_called()