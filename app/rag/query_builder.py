"""
Query Builder

Why this exists:
- Query embeddings should be intentional
- Logs ≠ alerts ≠ summaries
"""

def build_incident_query(normalized_incident: dict) -> str:
    """
    Build a semantic query from the normalized incident.
    """

    parts = [
        f"Title: {normalized_incident['title']}",
        f"Service: {normalized_incident['service']}",
        f"Environment: {normalized_incident['environment']}",
    ]

    if normalized_incident.get("description"):
        parts.append(f"Description: {normalized_incident['description']}")

    return "\n".join(parts)
