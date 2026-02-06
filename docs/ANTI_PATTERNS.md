# ANTI_PATTERNS.md
## GenAI Anti-Patterns – What NOT to Do (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It lists **explicit anti-patterns observed in real GenAI systems**,  
> explains **why teams fall into them**, **what breaks over time**,  
> and **how this system deliberately avoids them**.

If you remember nothing else, remember this:
> **Most GenAI failures come from repeating the same mistakes.**

This document exists to prevent that.

---

## 1. Why Anti-Patterns Matter More Than Best Practices

Best practices are aspirational.
Anti-patterns are **predictive**.

In GenAI systems:
- You rarely fail in new ways
- You usually fail in familiar ways

This document documents those familiar failures.

---

## 2. Calling OpenAI Directly Inside API Routes

### The Anti-Pattern
```
@app.post("/analyze")
def analyze(payload):
    return openai.chat.completions.create(...)
```

### Why Teams Do This
- Fast to prototype
- Tutorials encourage it
- Works for demos

### What Breaks in Production
- API timeouts
- Thread exhaustion
- Cascading retries
- Cost explosions

### How This System Avoids It
- FastAPI only validates & enqueues
- Workers perform inference

Files enforcing this:
- app/api/main.py
- app/asyncio/worker.py

---

## 3. Treating Fine-Tuning as a Knowledge Store

### The Anti-Pattern
- Putting historical data into fine-tuning
- Expecting the model to “remember” facts

### Why Teams Do This
- Misunderstanding of fine-tuning
- Desire to avoid RAG complexity

### What Breaks
- Stale knowledge
- Expensive retraining cycles
- Debugging impossibility

### Correct Approach
- RAG for facts
- Fine-tuning for behavior

Files:
- app/pipeline/retrieve.py
- app/pipeline/infer.py

---

## 4. Skipping Input Validation Because “The Model Is Smart”

### The Anti-Pattern
- Trusting user input
- Letting the model “figure it out”

### Why Teams Do This
- Overconfidence in LLMs
- Underestimating prompt injection

### Consequences
- Prompt injection succeeds
- PII leaks
- Vector store poisoning

### How This System Avoids It
- Mandatory normalization
- Safety before RAG

Files:
- app/pipeline/normalize.py
- app/api/schemas.py

---

## 5. Blindly Retrying All Failures

### The Anti-Pattern
```
while True:
    retry()
```

### Why Teams Do This
- “Eventually it will work” mindset
- Lack of failure taxonomy

### What Breaks
- Retry storms
- API bans
- Massive bills

### Correct Pattern
- Retry transient failures only
- DLQ for permanent failures

Files:
- app/asyncio/retry_policy.py
- app/asyncio/dlq.py

---

## 6. Overstuffing the Prompt with Context

### The Anti-Pattern
- Injecting every retrieved document
- Assuming more context = better answers

### Why Teams Do This
- Fear of missing information
- No retrieval thresholds

### Consequences
- Hallucinations
- High token cost
- Worse answers

### Correct Design
- Similarity thresholds
- Top-K limits
- Metadata filtering

Files:
- app/pipeline/retrieve.py

---

## 7. Ignoring Observability Until Production

### The Anti-Pattern
- “We’ll add metrics later”
- Logs without structure

### Why Teams Do This
- Focus on features
- Underestimate async complexity

### What Breaks
- Silent failures
- Cost spikes discovered too late
- No root cause visibility

### How This System Avoids It
- Metrics baked into pipeline
- Alerts from day one

Files:
- app/observability/*

---

## 8. Hardcoding Configuration & Secrets

### The Anti-Pattern
- API keys in code
- Model names hardcoded

### Why Teams Do This
- Convenience
- Local testing shortcuts

### Consequences
- Security breaches
- Painful rollbacks
- Environment drift

### Correct Pattern
- Centralized settings
- Environment validation

Files:
- app/config/settings.py

---

## 9. Mixing Sync and Async Logic

### The Anti-Pattern
- Some requests async, some sync
- Inconsistent behavior

### Why Teams Do This
- Incremental evolution
- No clear architecture

### What Breaks
- Unpredictable latency
- Debugging nightmares

### Correct Pattern
- All LLM work async
- Single execution model

Files:
- app/asyncio/*
- app/flow/incident_pipeline.py

---

## 10. No Clear Ownership Boundaries

### The Anti-Pattern
- Business logic in routes
- Infrastructure created everywhere

### Why Teams Do This
- Small team shortcuts
- No bootstrap concept

### Consequences
- Tight coupling
- Impossible testing
- Fragile code

### Correct Pattern
- Single bootstrap wiring
- Clear layer responsibilities

Files:
- app/bootstrap.py

---

## 11. Believing the Model Is the Product

### The Anti-Pattern
- Treating the LLM as “the system”

### Reality
- The model is just one dependency
- Architecture determines success

### This System’s Philosophy
> **The system owns reliability. The model provides intelligence.**

---

## 12. Mental Models to Remember

- LLMs are untrusted dependencies
- Async isolates risk
- RAG grounds truth
- Fine-tuning aligns behavior
- Observability prevents surprises

Forget these, and failures return.

---

## 13. Summary

Anti-patterns persist because:
- They work initially
- They fail slowly
- The cost appears later

This document exists so:
- Future contributors don’t repeat mistakes
- Systems evolve safely
- Hard-won lessons aren’t lost

Avoiding these anti-patterns is as important as following best practices.
