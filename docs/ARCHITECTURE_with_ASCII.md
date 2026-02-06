# ARCHITECTURE.md
## Incident AI – System Architecture (with ASCII Sequence Diagrams)

> This document defines the **authoritative architecture** of the Incident AI system.
> It includes **ASCII sequence diagrams** so the flow is understandable without tools.

---

## 1. High-Level System Overview

Incident AI is a **production-grade GenAI system** designed around four non-negotiable principles:

1. Safety first
2. Async by default
3. Facts via RAG, behavior via fine-tuning
4. Observability everywhere

---

## 2. Core Components

- Client (API consumer)
- FastAPI (ingress & validation)
- Async Queue
- Worker Pool
- RAG subsystem
- Fine-tuned LLM inference
- Observability layer

---

## 3. Synchronous Request Flow (API Layer)

This flow handles **request acceptance only** — no heavy work.

```
Client
  |
  | POST /incidents
  v
FastAPI
  |
  | Validate input (Pydantic)
  | Normalize + sanitize
  |
  v
Async Queue  ---->  Immediate 202 Accepted
```

### Why this matters
- API stays fast
- No LLM latency exposed
- Traffic spikes are absorbed

---

## 4. Asynchronous Processing Flow (Worker)

This is where **real work happens**.

```
Async Queue
   |
   | dequeue job
   v
Worker
   |
   | re-validate payload
   | normalize (idempotent)
   |
   |-----> RAG Retrieval
   |          |
   |          | embed query
   |          | vector search
   |          | threshold + top-K
   |          v
   |     Context Assembly
   |
   |-----> LLM Inference
   |          |
   |          | select model
   |          | send prompt
   |          | receive response
   |          v
   |     Structured Output
   |
   | update job status
   v
Result Store / DLQ
```

---

## 5. RAG Subsystem Flow

```
Historical Incidents
        |
        | normalize + sanitize
        |
        v
Chunker
        |
        | semantic chunks
        |
        v
Embedding Adapter
        |
        | vectors
        |
        v
Vector Store
```

### Retrieval at inference time

```
New Incident
     |
     | embed
     v
Vector Store
     |
     | similarity search
     | threshold filter
     v
Top-K Context
```

---

## 6. Fine-Tuning Positioning

Fine-tuning **never replaces RAG**.

```
          +------------------+
Context ->| Fine-tuned Model |
          | (behavior only)  |
          +------------------+
```

Order is enforced as:

```
Normalize -> RAG -> Fine-tuned Inference
```

---

## 7. Failure Isolation Diagram

```
Client ----> API (never blocks)
                 |
                 v
              Queue
                 |
                 v
              Worker ----X----> DLQ
```

One job failure **never**:
- crashes API
- blocks other jobs
- loses context

---

## 8. Observability Flow

```
[API] -------> logs
[Worker] ----> logs + metrics
[RAG] -------> latency metrics
[LLM] -------> token metrics
                  |
                  v
               Alerts
```

---

## 9. Scaling Model

```
        Queue
      /   |   \
Worker Worker Worker
```

- Add workers, not threads
- No API scaling required for LLM load

---

## 10. Mental Model (Keep This)

> **FastAPI accepts work, workers do work, RAG provides facts, fine-tuning enforces behavior, observability protects reality.**

---

## 11. Files That Enforce Architecture

- app/api/main.py
- app/bootstrap.py
- app/flow/incident_pipeline.py
- app/asyncio/worker.py
- app/pipeline/retrieve.py
- app/pipeline/infer.py

---

## 12. Summary

This architecture is:
- Safe
- Observable
- Scalable
- Cost-aware

Most importantly:
> **It fails gracefully instead of catastrophically.**
