import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

class TestAPI:
    
    def test_health_check(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "active"

    def test_ingest_text(self, client: TestClient):
        # This now runs the REAL IngestionService logic!
        payload = {
            "text": "This is a test spec.",
            "source_name": "test_spec.txt",
            "metadata": {"author": "QA"}
        }
        response = client.post("/api/v1/ingest", json=payload)
        assert response.status_code == 200
        # Verify it actually "processed" chunks
        assert response.json()["chunks_processed"] > 0

    def test_search_knowledge(self, client: TestClient):
        payload = {"query": "voltage", "limit": 1}
        response = client.post("/api/v1/search", json=payload)
        assert response.status_code == 200
        assert len(response.json()["matches"]) > 0

    def test_ingest_pdf_upload(self, client: TestClient):
        files = {'file': ('test.pdf', b'%PDF-1.4 fake content', 'application/pdf')}
        response = client.post("/api/v1/ingest/file", files=files)
        assert response.status_code == 200

    # For the agent workflow, we still mock the LLM response via conftest,
    # but we let the Graph object run naturally.
    def test_generate_workflow(self, client: TestClient):
        payload = {"topic": "Wiring Guide"}
        
        # The mock LLM in conftest returns "Mocked LLM Response"
        # The critic will see that and likely trigger a "revise" or "approve" depending on prompt.
        # To make it deterministic for "success", we can patch the node behavior specifically here if needed,
        # but the default mock ensures the code runs without crashing.
        
        response = client.post("/api/v1/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "final_document" in data