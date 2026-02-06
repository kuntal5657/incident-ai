# ARCHITECTURE.md
## Incident AI – End-to-End System Architecture (Deep Dive)

> This document is intentionally **long and detailed (≈3–4 pages)**.  
> It explains **what the architecture is**, **why each decision was made**,  
> **how requests flow**, **where failures happen**, and **which files implement each part**.

If you fully understand this document, you understand **production GenAI system architecture**.

---

## 1. Architectural Goals

Before writing any code, we defined **non-negotiable goals**:

### Functional Goals
- Classify incidents (severity, category)
- Infer probable root cause
- Recommend next actions
- Use historical incidents as context (RAG)

### Non-Functional Goals (VERY IMPORTANT)
- Non-blocking APIs
- Predictable latency
- Controlled cost
- Safe LLM usage
- Observable behavior
- Recoverable failures

These goals **directly shaped the architecture**.

---

## 2. High-Level Architecture Overview

```
+--------+
| Client |
+--------+
     |
     v
+-----------+        (NO LLM CALLS HERE)
| FastAPI  |
|  (API)   |
+-----------+
     |
     v
+------------------+
| Async Job Queue  |
+------------------+
     |
     v
+------------------+
| Worker Process   |
+------------------+
     |
     v
+-------------------------+
| IncidentPipeline        |
|  - NormalizeStep        |
|  - RetrieveContextStep  |
|  - InferenceStep        |
+-------------------------+
     |
     v
+------------------+
| OpenAI APIs      |
+------------------+
```

### One Golden Rule
> **FastAPI never talks to OpenAI directly**

Violating this rule causes:
- API timeouts
- Poor user experience
- Uncontrolled retries
- Cost explosions

---

## 3. Why Asynchronous Architecture Is Mandatory

### Problem with Synchronous LLM Calls

LLM calls:
- Take seconds (5–15s common)
- Are network-dependent
- Can fail transiently
- Are expensive

If we call OpenAI synchronously inside FastAPI:
- Requests block
- Clients time out
- Retries multiply
- API servers collapse under load

### Async Solution

FastAPI:
- Accepts request
- Validates input
- Enqueues job
- Returns immediately

Worker:
- Handles slow, expensive work
- Retries safely
- Isolates failures

### File Mapping
- app/api/main.py
- app/asyncio/queue.py
- app/asyncio/worker.py

---

## 4. Request Lifecycle (Step-by-Step)

### Step 1: Client → FastAPI

```
POST /incidents
```

FastAPI responsibilities:
- Schema validation (Pydantic)
- Request ID generation
- Job creation
- Job enqueue

What FastAPI does NOT do:
- No embeddings
- No OpenAI calls
- No business logic

Files:
- app/api/main.py
- app/api/schemas.py

---

### Step 2: Job Queue

The job queue:
- Decouples API from execution
- Enables backpressure
- Buffers traffic spikes

Job states:
- PENDING
- RUNNING
- SUCCEEDED
- FAILED

Files:
- app/asyncio/job.py
- app/asyncio/status.py
- app/asyncio/queue.py

---

### Step 3: Worker Picks Job

Worker responsibilities:
- Pull job from queue
- Execute pipeline
- Handle retries
- Update job status
- Store result

Why a worker?
- Isolation
- Fault containment
- Horizontal scaling

Files:
- app/asyncio/worker.py
- app/asyncio/retry_policy.py
- app/asyncio/result_store.py
- app/asyncio/dlq.py

---

## 5. IncidentPipeline Architecture

The pipeline is **linear and explicit**.

### Why Linear?
- Predictable behavior
- Easier debugging
- Clear metrics per step

### Pipeline Steps

#### 1. NormalizeStep
Purpose:
- Validate input
- Normalize fields
- Apply safety rules

Files:
- app/pipeline/normalize.py

---

#### 2. RetrieveContextStep (RAG)
Purpose:
- Retrieve similar historical incidents
- Ground LLM output in facts

Files:
- app/pipeline/retrieve.py
- app/adapters/embedding_adapter.py
- app/adapters/vector_store_adapter.py

---

#### 3. InferenceStep
Purpose:
- Call OpenAI
- Apply fine-tuned model
- Produce structured output

Files:
- app/pipeline/infer.py
- app/adapters/openai_adapter.py

---

### Pipeline Orchestration

Files:
- app/flow/incident_pipeline.py

This file:
- Calls steps in order
- Passes outputs explicitly
- Measures latency
- Handles failures

---

## 6. Why RAG + Fine-Tuning (Hybrid)

### RAG Strengths
- Up-to-date facts
- Traceable sources
- No retraining needed

### Fine-Tuning Strengths
- Consistent output format
- Better classification behavior
- Reduced prompt size

### Why Hybrid?
- RAG handles **knowledge**
- Fine-tuning handles **behavior**

Using only one causes failures.

---

## 7. Failure Modes & Isolation

### Failure Types
- OpenAI timeout
- Network error
- Invalid input
- Retrieval miss

### How Architecture Handles Them
- Retries only transient failures
- Permanent failures → DLQ
- API remains responsive

Files:
- app/asyncio/retry_policy.py
- app/asyncio/dlq.py

---

## 8. Observability Built into Architecture

Every layer emits:
- Logs
- Metrics
- Timings

Why?
> You cannot control what you cannot see.

Files:
- app/observability/logger.py
- app/observability/metrics.py
- app/observability/alerts.py

---

## 9. Bootstrap Pattern (Critical)

All wiring happens in **one place**.

Why?
- Prevents hidden dependencies
- Makes async & sync consistent
- Enables testing

File:
- app/bootstrap.py

Anti-pattern:
❌ Creating adapters inside routes

---

## 10. What Breaks If You Ignore This Architecture

If you:
- Call OpenAI in FastAPI → outages
- Skip async → latency spikes
- Skip normalization → unsafe LLM calls
- Skip RAG → hallucinations
- Skip observability → surprise bills

These failures are common in real systems.

---

## 11. Mental Model to Keep

Think of the system as:

FastAPI = traffic controller  
Queue = shock absorber  
Worker = engine room  
Pipeline = assembly line  
LLM = expensive external dependency  

This mental model prevents bad decisions.

---

## 12. Summary

This architecture exists to:
- Protect users
- Protect budgets
- Protect uptime
- Enable scaling
- Make GenAI predictable

This is **how production GenAI systems are actually built**.
