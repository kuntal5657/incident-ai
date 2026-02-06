"""
Vector Store Adapter (In-Memory)

Why this exists:
- Clean abstraction
- No vendor lock-in
- Easy to swap later
"""

import math
from typing import List, Dict


class InMemoryVectorStore:
    def __init__(self):
        self.vectors = []

    def add(self, embedding: List[float], metadata: Dict, text: str):
        self.vectors.append({
            "embedding": embedding,
            "metadata": metadata,
            "text": text,
        })

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        return dot / (norm_a * norm_b)

    def search(self, query_embedding: List[float], top_k: int = 5):
        """
        Return top-K most similar chunks with similarity scores.
        """
        scored = []

        for item in self.vectors:
            score = self._cosine_similarity(query_embedding, item["embedding"])
            scored.append({
                "score": score,
                "text": item["text"],
                "metadata": item["metadata"],
            })

        scored.sort(reverse=True, key=lambda x: x["score"])
        return scored[:top_k]
