# OBSERVABILITY_AND_COST.md
## Observability, Metrics, Alerts & Cost Control (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It explains **what to observe**, **why it matters**, **how metrics are designed**,  
> **how cost is controlled**, and **which files implement each capability**.

If you understand this document, you understand **how GenAI systems stay reliable and affordable in production**.

---

## 1. Why Observability Is Non‑Optional for GenAI

GenAI systems fail in *non-obvious* ways:
- Latency slowly creeps up
- Token usage spikes silently
- Error rates stay low but costs explode
- Partial failures degrade quality

Without observability:
> **You only discover problems after the bill arrives or users complain.**

Therefore, observability is treated as a **core architectural layer**, not an afterthought.

---

## 2. Observability Goals

We designed observability to answer four questions **at all times**:

1. Is the system healthy?
2. Is it fast enough?
3. Is it safe?
4. Is it affordable?

Every metric, log, and alert maps back to one of these questions.

---

## 3. Structured Logging (The Foundation)

### 3.1 Why Structured Logs

Plain text logs:
- Are hard to search
- Cannot be aggregated reliably
- Lose context in async systems

Structured logs:
- Are machine‑readable
- Preserve context across async boundaries
- Enable correlation

---

### 3.2 What We Log

Every log entry includes:
- timestamp
- log level
- component name
- request_id / job_id (when available)
- message
- contextual metadata

Example:
```json
{
  "timestamp": "2026-02-06T13:41:23.391495",
  "level": "INFO",
  "logger": "incident_pipeline",
  "request_id": "75aa51c8",
  "step": "start",
  "message": "Pipeline started"
}
```

Files:
- app/observability/logger.py

---

## 4. Metrics Design (Counters & Timers)

### 4.1 Why Metrics Are Different from Logs

Logs explain *what happened*.
Metrics answer *how often* and *how bad*.

We use metrics to:
- Detect trends
- Trigger alerts
- Control cost

---

### 4.2 Core Metrics Tracked

#### Request Metrics
- pipeline.requests.total
- pipeline.requests.success
- pipeline.requests.failed

#### Latency Metrics (per step)
- pipeline.normalize.latency_ms
- pipeline.retrieve.latency_ms
- pipeline.infer.latency_ms

#### Async Metrics
- queue.depth
- job.runtime_ms
- retry.count
- dlq.size

Files:
- app/observability/metrics.py

---

## 5. Token Accounting (Cost Visibility)

### 5.1 Why Token Tracking Matters

LLM cost = **tokens × price**

Without token visibility:
- Small prompt changes cause huge cost jumps
- RAG misconfiguration goes unnoticed
- Fine‑tuned models hide inefficiency

---

### 5.2 What We Track

For every inference:
- prompt_tokens
- completion_tokens
- total_tokens
- model_name

These are logged and aggregated.

Files:
- app/pipeline/infer.py
- app/observability/metrics.py

---

## 6. Latency Budgets & Guardrails

### 6.1 Why Latency Budgets Exist

Users don’t care *why* it’s slow — only that it *is* slow.

We define budgets:
- Normalize: < 5 ms
- Retrieve (RAG): < 500 ms
- Inference: < 15 s

If budgets are exceeded:
- Alerts trigger
- Investigations start

---

## 7. Alerting Strategy (Actionable Only)

### 7.1 Alert Fatigue Is Dangerous

Bad alerts:
- Trigger constantly
- Get ignored
- Hide real incidents

Good alerts:
- Are rare
- Are actionable
- Point to root causes

---

### 7.2 Alerts Implemented

Examples:
- error_rate_exceeded
- avg_latency_exceeded
- dlq_size_exceeded
- token_spike_detected

Files:
- app/observability/alerts.py

---

## 8. Cost Control Strategies (Very Important)

### 8.1 Architectural Cost Controls

- Async processing (no blocked retries)
- Centralized OpenAI adapter
- RAG limits (top‑K, thresholds)
- Fine‑tuned model selection

---

### 8.2 Runtime Cost Controls

- Max tokens per request
- Prompt size limits
- Context truncation
- Fallback to base model

Files:
- app/pipeline/infer.py
- app/config/settings.py

---

## 9. Observability in Async Systems

Async breaks naive observability:
- Logs arrive out of order
- Context is lost
- Failures are delayed

Solutions:
- request_id propagation
- job_id correlation
- explicit job state logging

Files:
- app/asyncio/worker.py
- app/observability/logger.py

---

## 10. Failure Scenarios & Detection

| Failure | Detected By |
|------|-----------|
| Token explosion | token_spike alert |
| RAG slowdown | retrieve latency |
| OpenAI timeout | retry metrics |
| Silent errors | error rate alert |

Observability turns *unknown unknowns* into *known problems*.

---

## 11. What Breaks Without Observability

If you skip this layer:
- Costs explode silently
- Latency regressions go unnoticed
- DLQ fills without alerts
- Failures become user-visible

This is how GenAI projects die in production.

---

## 12. Mental Model to Keep

Think of observability as:
> **The flight instruments of your system**

Flying without them works… until it doesn’t.

---

## 13. Summary

Observability and cost control:
- Are inseparable
- Must be designed, not added later
- Protect budgets, users, and teams

This system embeds observability **into the architecture itself**, not around it.
