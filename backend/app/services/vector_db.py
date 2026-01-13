from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Filter, FieldCondition, MatchValue
from app.core.config import settings
from app.core.logging import logger
from typing import List, Dict, Any, Optional
import uuid

class VectorDBService:
    """
    Service class for interacting with Qdrant Vector Database.
    """

    def __init__(self):
        # Initialize the client
        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )
        self.collection_name = "vaisala_docs"
        self.vector_size = 1536 
        
        self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        try:
            collections = self.client.get_collections()
            exists = any(c.name == self.collection_name for c in collections.collections)

            if not exists:
                logger.info(f"📦 Collection '{self.collection_name}' not found. Creating...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(
                        size=self.vector_size,
                        distance=models.Distance.COSINE
                    )
                )
                logger.info(f"✅ Collection '{self.collection_name}' created successfully.")
            else:
                logger.info(f"✅ Connected to existing collection: '{self.collection_name}'")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Qdrant collection: {e}")
            raise e

    def upsert_vectors(self, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        points = [
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )
            for vector, payload in zip(vectors, payloads)
        ]
        
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        logger.info(f"💾 Upserted {len(points)} chunks into Qdrant.")

    def search(self, vector: List[float], limit: int = 3) -> List[Any]:
        """
        Search for similar vectors in the collection using query_points.
        """
        try:
            # Use query_points with vector query
            results = self.client.query_points(
                collection_name=self.collection_name,
                query=vector,
                limit=limit,
                with_payload=True,
                with_vectors=False
            )
            
            # Return the raw points - ingestion.py expects objects with .payload attribute
            logger.info(f"🔍 Found {len(results.points)} results from vector search")
            return results.points
            
        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise e

    def _format_search_results(self, results):
        """Format search results into a consistent structure."""
        formatted_results = []
        for result in results:
            formatted_results.append({
                "id": result.id,
                "payload": result.payload,
                "score": result.score
            })
        return formatted_results