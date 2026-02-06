# ERROR_TIMELINES.md
## Failure Timelines & Debugging Sequences

This document visualizes **how failures unfold over time**.

---

## 1. Missing Environment Variable

```
uvicorn start
    |
    v
Settings.load()
    |
    X  OPENAI_API_KEY missing
```

Lesson:
> Fail fast at startup.

---

## 2. Async Validation Bypass

```
API validates ✔
   |
Queue
   |
Worker
   |
X ValidationError
```

Fix:
- Re-validate inside worker

---

## 3. Retry Storm Scenario

```
LLM timeout
   |
retry
   |
retry
   |
retry
   |
API ban 💥
```

Fix:
- Retry taxonomy
- Backoff
- DLQ

---

## 4. Token Explosion Timeline

```
RAG returns 12 chunks
   |
Prompt grows
   |
Token cost spikes
   |
Billing alert 🚨
```

Fix:
- top-K
- thresholds