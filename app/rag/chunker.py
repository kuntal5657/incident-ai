"""
Chunker

Why this exists:
- RAG quality depends more on chunking than models
- We chunk by meaning, not arbitrary token counts
"""

from typing import List, Dict


class Chunker:
    MAX_CHARS = 800  # conservative for embeddings

    def chunk_incident(self, incident: Dict) -> List[Dict]:
        """
        Convert a normalized incident into embedding-ready chunks.
        """

        chunks = []

        base_metadata = {
            "incident_id": incident["incident_id"],
            "service": incident["service"],
            "environment": incident["environment"],
        }

        # Title + description chunk
        header_text = f"""
        Title: {incident['title']}
        Description: {incident['description']}
        """.strip()

        chunks.append({
            "text": header_text,
            "metadata": base_metadata | {"type": "summary"}
        })

        # Log chunks
        for log in incident.get("logs", []):
            if log.strip():
                chunks.append({
                    "text": log[: self.MAX_CHARS],
                    "metadata": base_metadata | {"type": "log"}
                })

        # Alert chunks
        for alert in incident.get("alerts", []):
            if alert.strip():
                chunks.append({
                    "text": alert[: self.MAX_CHARS],
                    "metadata": base_metadata | {"type": "alert"}
                })

        return chunks
