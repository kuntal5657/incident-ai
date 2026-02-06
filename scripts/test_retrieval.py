from app.flow.incident_pipeline import IncidentPipeline
from app.adapters.vector_store_adapter import InMemoryVectorStore
from app.rag.ingest import RAGIngestor

# Prepare vector store
store = InMemoryVectorStore()
ingestor = RAGIngestor(store)

# Ingest historical incident
ingestor.ingest_incident({
    "incident_id": "INC-111",
    "title": "Database saturation",
    "description": "Connection pool exhausted",
    "service": "orders-db",
    "environment": "prod",
    "logs": ["Too many DB connections"],
    "alerts": ["DB pool > 90%"]
})

# Run pipeline
pipeline = IncidentPipeline(store)

result = pipeline.run({
    "incident_id": "INC-222",
    "title": "Order API latency",
    "description": "Latency spike under load",
    "service": "orders-db",
    "environment": "prod",
    "logs": [],
    "alerts": []
})

print("Retrieved context:")
print(result["retrieval"]["context_text"])
print("\nSources:")
print(result["retrieval"]["sources"])
