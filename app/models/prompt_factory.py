"""
Prompt Factory

Why this exists:
- Prompts are versioned artifacts
- Keeps pipeline logic clean
- Enables prompt iteration safely
"""

def system_prompt() -> str:
    return """
You are an SRE incident classification system.

STRICT RULES:
- Output MUST be a single JSON object
- Do NOT nest the output inside any other key
- Do NOT include explanations or comments
- Do NOT wrap the result in 'classification' or any other object

The JSON object MUST have exactly these fields:
- severity (one of: P0, P1, P2, P3)
- category (string)
- probable_root_cause (string)
- recommended_actions (array of strings)
- confidence (number between 0 and 1)

Return ONLY valid JSON.
""".strip()

def user_prompt(incident: dict, context: str) -> str:
    """
    User prompt including incident data and retrieved context.
    """
    return f"""
Incident:
Title: {incident['title']}
Service: {incident['service']}
Environment: {incident['environment']}
Description: {incident['description']}

Relevant Historical Context:
{context if context else "No relevant historical context found."}

Classify the incident and provide recommendations.
""".strip()
