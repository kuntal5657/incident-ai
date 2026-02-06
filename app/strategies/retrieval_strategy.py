"""
Retrieval Strategy

Why this exists:
- Retrieval behavior must be configurable
- Avoids hard-coded top-K logic
- Enables experimentation and tuning
"""

from typing import List, Dict


class RetrievalStrategy:
    """
    Base interface for retrieval strategies.
    """

    def select(
        self,
        vector_store,
        query_embedding: List[float],
    ) -> List[Dict]:
        raise NotImplementedError


class TopKThresholdStrategy(RetrievalStrategy):
    """
    Default retrieval strategy:
    - Retrieve top-K results
    - Drop results below similarity threshold
    """

    def __init__(self, top_k: int = 5, min_score: float = 0.25):
        self.top_k = top_k
        self.min_score = min_score

    def select(self, vector_store, query_embedding):
        """
        Retrieve top-K vectors and filter weak matches.
        """
        raw_results = vector_store.search(
            query_embedding=query_embedding,
            top_k=self.top_k,
        )

        # Filter out weak semantic matches
        filtered = [
            r for r in raw_results
            if r["score"] >= self.min_score
        ]

        return filtered
