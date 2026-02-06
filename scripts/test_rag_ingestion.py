from app.flow.incident_pipeline import IncidentPipeline
from app.adapters.vector_store_adapter import InMemoryVectorStore
from app.rag.ingest import RAGIngestor

# Step 1: Normalize input
pipeline = IncidentPipeline()
normalized = pipeline.run({
    "incident_id": "INC-2001",
    "title": "Database connection saturation",
    "description": "Connections exhausted after traffic spike",
    "service": "orders-db",
    "environment": "prod",
    "logs": ["Too many connections from 10.1.2.3"],
    "alerts": ["DB connection pool > 95%"]
})

# Step 2: Ingest into vector store
store = InMemoryVectorStore()
ingestor = RAGIngestor(store)
ingestor.ingest_incident(normalized)

print(f"Stored vectors: {len(store.vectors)}")
