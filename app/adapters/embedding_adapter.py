"""
OpenAI Embedding Adapter

Why this exists:
- Isolates embedding generation
- Allows future provider swap
- Centralizes embedding configuration
"""

from openai import OpenAI
from app.config.settings import Settings


class EmbeddingAdapter:
    def __init__(self):
        self.client = OpenAI(
            api_key=Settings.OPENAI_API_KEY,
            timeout=Settings.OPENAI_TIMEOUT_SECONDS,
        )

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.

        Returns:
        - List of embedding vectors (list[float])
        """

        response = self.client.embeddings.create(
            model="text-embedding-3-large",
            input=texts,
        )

        # Preserve ordering
        return [item.embedding for item in response.data]
