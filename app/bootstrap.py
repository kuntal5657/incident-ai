"""
Application bootstrap.

Creates shared infrastructure:
- Vector store
- RAG ingestion
- Incident pipeline

This is the SINGLE source of truth for wiring.
"""

from app.flow.incident_pipeline import IncidentPipeline
from app.adapters.vector_store_adapter import InMemoryVectorStore
from app.rag.ingest import RAGIngestor


def build_vector_store():
    """
    Build and populate the vector store.
    Must match previous working setup exactly.
    """
    store = InMemoryVectorStore()
    ingestor = RAGIngestor(store)

    # ---- Ingest historical incident(s) ----
    ingestor.ingest_incident({
        "incident_id": "INC-3001",
        "title": "Database connection exhaustion",
        "description": "Connection pool exhausted under load",
        "service": "orders-db",
        "environment": "prod",
        "logs": ["Too many connections"],
        "alerts": ["DB pool > 95%"]
    })

    return store


def build_pipeline():
    """
    Build the IncidentPipeline with shared infrastructure.
    """
    store = build_vector_store()
    return IncidentPipeline(store)
