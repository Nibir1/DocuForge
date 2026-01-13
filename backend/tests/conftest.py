import sys
import os
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Generator

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.config import settings

# 1. Override Settings
@pytest.fixture(scope="session", autouse=True)
def test_settings():
    settings.ENVIRONMENT = "test"
    settings.OPENAI_API_KEY = "sk-fake-key"
    settings.QDRANT_HOST = "localhost"

# 2. Mock External Dependencies (Qdrant, OpenAI, AND pypdf)
@pytest.fixture(autouse=True)
def mock_external_deps():
    """
    Patches all external libraries.
    """
    with patch("app.services.vector_db.QdrantClient") as mock_qdrant, \
         patch("app.services.ingestion.OpenAIEmbeddings") as mock_embed, \
         patch("app.agents.nodes.ChatOpenAI") as mock_llm, \
         patch("app.services.ingestion.pypdf.PdfReader") as mock_pdf: # <--- NEW PATCH
        
        # --- Setup Qdrant Mock ---
        mock_client_instance = mock_qdrant.return_value
        # Mock 'search' return
        mock_client_instance.query_points.return_value.points = [
            MagicMock(payload={"content": "Test Content", "source": "test.pdf"}, score=0.9)
        ]
        # Mock 'collection exists' check
        mock_client_instance.get_collections.return_value.collections = []
        
        # --- Setup OpenAI Embeddings Mock ---
        # Return a list of floats (vector)
        mock_embed.return_value.embed_documents.return_value = [[0.1] * 1536]
        mock_embed.return_value.embed_query.return_value = [0.1] * 1536
        
        # --- Setup LLM Mock ---
        mock_llm.return_value.invoke.return_value.content = "Mocked LLM Response"

        # --- Setup PDF Mock (NEW) ---
        # When PdfReader is called, return an object with a 'pages' attribute
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Mocked PDF content found here."
        mock_pdf.return_value.pages = [mock_page]
        
        yield {
            "qdrant": mock_client_instance,
            "embed": mock_embed,
            "llm": mock_llm,
            "pdf": mock_pdf
        }

# 3. Test Client
@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c