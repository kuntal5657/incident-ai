"""
RetrieveContextStep

Why this step exists:
- Turns vector store into usable knowledge
- Applies retrieval strategy
- Prepares context for LLM consumption
"""

from app.pipeline.base import PipelineStep
from app.adapters.embedding_adapter import EmbeddingAdapter
from app.strategies.retrieval_strategy import TopKThresholdStrategy
from app.rag.query_builder import build_incident_query


class RetrieveContextStep(PipelineStep):
    def __init__(self, vector_store):
        self.embedder = EmbeddingAdapter()
        self.vector_store = vector_store
        self.strategy = TopKThresholdStrategy()

    def run(self, normalized_incident: dict) -> dict:
        """
        Retrieve relevant historical context.

        Returns:
        - context_text: str
        - sources: list of metadata dicts
        """

        # 1️⃣ Build semantic query
        query_text = build_incident_query(normalized_incident)

        # 2️⃣ Embed query
        query_embedding = self.embedder.embed_texts([query_text])[0]

        # 3️⃣ Retrieve candidates
        raw_results = self.vector_store.search(query_embedding)

        # 4️⃣ Assemble context
        context_blocks = []
        sources = []

        for item in raw_results:
            context_blocks.append(item["text"])
            sources.append(item["metadata"])

        context_text = "\n---\n".join(context_blocks)

        return {
            "context_text": context_text,
            "sources": sources,
        }

