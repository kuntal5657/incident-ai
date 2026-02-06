# RAG_DESIGN_ASCII.md
## RAG with ASCII Diagrams – Chunking, Retrieval & Thresholds

This document **extends RAG_DESIGN.md** with concrete ASCII diagrams to make
retrieval behavior, thresholds, and failure modes visually obvious.

---

## 1. Ingestion Pipeline (Offline)

```
Raw Incident
    |
    | normalize + sanitize
    v
+-------------+
|  Chunker    |
|-------------|
| summary     |
| logs        |
| alerts      |
+-------------+
    |
    | semantic chunks
    v
Embedding Adapter
    |
    | vectors
    v
Vector Store
```

### Key Rule
> Embeddings are generated **once**, reused many times.

---

## 2. Retrieval Pipeline (Inference Time)

```
Incoming Incident
      |
      | normalize
      | embed
      v
+----------------+
| Vector Store   |
|----------------|
| similarity     |
| search         |
+----------------+
      |
      | top-K + threshold
      v
Relevant Context
```

---

## 3. Threshold Filtering (Critical)

```
Similarity Scores:
0.92  ✔ keep
0.87  ✔ keep
0.61  ✘ drop
0.43  ✘ drop
```

Why:
- Low similarity = hallucination risk
- Fewer chunks = lower cost

---

## 4. Context Assembly

```
[Context]
- Incident A (summary)
- Incident A (alerts)
- Incident B (summary)
```

Injected as **facts**, never instructions.

---

## 5. Failure Modes

```
No Matches
   |
   v
LLM runs WITHOUT context
(no hallucinated history)
```

---

## Summary

ASCII diagrams enforce one mental rule:

> Retrieval is a filter, not a memory dump.