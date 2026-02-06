## Fine-Tuning Dataset Guidelines

This dataset fine-tunes the model for:
- Severity consistency (P0–P3)
- Stable taxonomy
- Strict JSON output

Rules:
- Do NOT include new knowledge
- Do NOT include speculative facts
- If evidence is weak, lower confidence
- Keep outputs concise and actionable

Severity guidance:
- P0: Full outage, revenue impact
- P1: Major degradation, partial outage
- P2: Degraded performance, workaround exists
- P3: Minor issue, no immediate impact
