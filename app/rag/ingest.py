"""
RAG Ingestion Pipeline

Why this exists:
- Offline / async ingestion
- Keeps inference path fast
"""

from app.adapters.embedding_adapter import EmbeddingAdapter
from app.adapters.vector_store_adapter import InMemoryVectorStore
from app.rag.chunker import Chunker

class RAGIngestor:
    def __init__(self, vector_store: InMemoryVectorStore):
        self.embedder = EmbeddingAdapter()
        self.chunker = Chunker()
        self.vector_store = vector_store

    def ingest_incident(self, normalized_incident: dict):
        """
        Chunk, embed, and store an incident.
        """
        chunks = self.chunker.chunk_incident(normalized_incident)
        texts = [c["text"] for c in chunks]

        embeddings = self.embedder.embed_texts(texts)

        for chunk, embedding in zip(chunks, embeddings):
            self.vector_store.add(
                embedding=embedding,
                metadata=chunk["metadata"],
                text=chunk["text"],
            )
