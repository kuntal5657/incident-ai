# ANTI_PATTERNS_DECISION_TREES.md
## Decision Trees to Avoid GenAI Anti-Patterns

---

## 1. Should I Call the LLM Here?

```
Are you in API layer?
   |
   |-- Yes --> ❌ NEVER
   |
   |-- No
        |
        |-- Is this a worker?
              |
              |-- Yes --> ✔ OK
```

---

## 2. Should I Fine-Tune This?

```
Is this knowledge?
   |
   |-- Yes --> ❌ RAG
   |
   |-- No
        |
        |-- Is it behavior/format?
              |
              |-- Yes --> ✔ Fine-tune
```

---

## 3. Should I Retry This Error?

```
Is error transient?
   |
   |-- Yes --> ✔ Retry
   |
   |-- No --> ❌ DLQ
```

---

## Summary

If unsure:
> Default to safety, async, and isolation.