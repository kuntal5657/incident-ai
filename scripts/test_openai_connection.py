"""
Quick sanity check to ensure OpenAI credentials and connectivity work.
"""

from app.adapters.openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter()

response = adapter.classify_incident(
    system_prompt="You are a strict classifier.",
    user_prompt="Database latency spike after deployment.",
)

print("OpenAI response:")
print(response)
