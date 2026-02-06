# ASYNC_AND_RELIABILITY.md
## Asynchronous Processing, Reliability & Failure Isolation (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It explains **why async is mandatory for GenAI**, **how reliability is achieved**,  
> **how failures are isolated**, and **which files implement each guarantee**.

If you understand this document, you understand **how GenAI systems survive real traffic and failures**.

---

## 1. Why Asynchronous Processing Is Non-Negotiable

### The Reality of LLM Calls

LLM inference:
- Takes seconds (often 5–20s)
- Depends on external networks
- Can fail transiently
- Is expensive per call

If handled synchronously:
- APIs block
- Clients time out
- Retries multiply
- Costs explode

Therefore:
> **Async is not an optimization — it is a safety requirement.**

---

## 2. Sync vs Async: A Concrete Comparison

### Synchronous Model (Anti-Pattern)

Client → API → LLM → Response

Problems:
- API threads blocked
- No retry control
- No failure isolation
- Poor UX

### Asynchronous Model (This System)

Client → API → Queue → Worker → LLM

Benefits:
- Fast API responses
- Controlled retries
- Failure containment
- Horizontal scalability

---

## 3. Core Async Components

### 3.1 Job Queue

Purpose:
- Decouple request ingestion from execution
- Buffer traffic spikes
- Enable backpressure

Job states:
- PENDING
- RUNNING
- SUCCEEDED
- FAILED

Files:
- app/asyncio/queue.py
- app/asyncio/job.py
- app/asyncio/status.py

---

### 3.2 Background Worker

Responsibilities:
- Pull jobs from queue
- Execute pipeline
- Handle retries
- Update job state
- Persist results

Why workers exist:
- Isolation from API layer
- Independent scaling
- Fault containment

Files:
- app/asyncio/worker.py

---

## 4. Retry Strategy (Most Common Failure Area)

### 4.1 Not All Failures Are Equal

Failures fall into two categories:

#### Transient Failures
- Network timeout
- Temporary OpenAI error
- Rate limit

✔ Safe to retry

#### Permanent Failures
- Invalid input
- Schema violation
- Logic error

❌ Retrying makes things worse

---

### 4.2 Retry Policy Design

Rules enforced:
- Retry only transient errors
- Maximum retry attempts (default: 3)
- Exponential backoff

Files:
- app/asyncio/retry_policy.py

Why this matters:
- Prevents retry storms
- Controls cost
- Protects external APIs

---

## 5. Dead Letter Queue (DLQ)

### 5.1 Why DLQ Exists

Some jobs must fail permanently.

Without DLQ:
- Jobs retry forever
- Queues clog
- Costs spiral

DLQ ensures:
- Failures are captured
- System continues operating
- Engineers can investigate later

Files:
- app/asyncio/dlq.py

---

### 5.2 What Goes Into DLQ

- Job payload
- Error details
- Retry count
- Timestamp

This data is critical for:
- Debugging
- Post-mortems
- Model improvement

---

## 6. Idempotency & Job Safety

### Why Idempotency Matters

Async systems may:
- Retry jobs
- Restart workers
- Replay messages

Design rule:
> **Running the same job twice must not corrupt state.**

Strategies:
- Immutable job payloads
- Explicit job IDs
- Result overwrite safety

Files:
- app/asyncio/job.py
- app/asyncio/result_store.py

---

## 7. Failure Isolation

Failures are isolated at multiple levels:

- API layer never fails due to LLM
- Worker failures do not crash API
- Single job failure does not affect others

This is achieved by:
- Process separation
- Explicit job states
- Defensive error handling

---

## 8. Observability for Async Systems

Async systems are invisible without metrics.

We track:
- Queue depth
- Job latency
- Retry counts
- Failure rates
- DLQ size

Files:
- app/observability/metrics.py
- app/observability/logger.py

Why:
> You cannot debug what you cannot see.

---

## 9. Scaling the Async System

Scaling options:
- Multiple workers
- Separate worker pools per task type
- Priority queues

This architecture supports:
- Horizontal scaling
- Load isolation
- Graceful degradation

---

## 10. Common Async Anti-Patterns

❌ Retrying all failures  
❌ Blocking inside worker  
❌ No DLQ  
❌ No backpressure  
❌ Mixing API and worker logic  

These lead to:
- Cascading failures
- Cost explosions
- System outages

---

## 11. Mental Model to Keep

Think of async processing as:
> **An air traffic control system**

Planes (jobs) are:
- Scheduled
- Tracked
- Retried safely
- Diverted if necessary

Without control, chaos follows.

---

## 12. Summary

Async + reliability patterns:
- Protect APIs
- Control cost
- Isolate failures
- Enable scale

They are **foundational**, not optional.

This system applies them deliberately and consistently.
