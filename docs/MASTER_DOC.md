# MASTER_DOC.md
## Incident AI – Complete System Guide (What It Is, Why It Exists, and How to Read Everything)

> This is the **single authoritative entry point** for the Incident AI system.
>
> This document intentionally combines:
> - **System definition (what this system is / is not)**
> - **How to read the documentation**
> - **A map of every document and code area**
> - **Mental models and long-term guardrails**
>
> Nothing from earlier versions is removed — this is a **superset**.

---

- [ARCHITECTURE.md](ARCHITECTURE.md)
- [INPUT_AND_SAFETY.md](INPUT_AND_SAFETY.md)
- [RAG_DESIGN.md](RAG_DESIGN.md)
- [ASYNC_AND_RELIABILITY.md](ASYNC_AND_RELIABILITY.md)
- [FINETUNING.md](FINETUNING.md)
- [OBSERVABILITY_AND_COST.md](OBSERVABILITY_AND_COST.md)
- [ERROR_TIMELINES.md](ERROR_TIMELINES.md)
- [ERRORS_AND_LESSONS.md](ERRORS_AND_LESSONS.md)
- [ANTI_PATTERNS.md](ANTI_PATTERNS.md)
- [FUTURE_EVOLUTION.md](FUTURE_EVOLUTION.md)

# PART 1 — WHAT THIS SYSTEM IS (FOUNDATIONAL CONTEXT)

## 1. What This System Is

**Incident AI** is a **production-grade, GenAI-powered incident intelligence system**.

At a high level, it:
- Accepts incident reports from humans or systems
- Analyzes them using GenAI
- Grounds analysis in historical incidents (RAG)
- Produces structured, machine-readable outputs
- Operates safely, asynchronously, and observably

It is designed to:
- Run continuously in production
- Handle real failures
- Scale under load
- Be auditable and cost-controlled

This is **not a demo system**.

---

## 2. What Problem This System Solves

Real-world incident response suffers from:

- Inconsistent severity classification
- Repeated analysis of similar incidents
- Tribal knowledge locked in people’s heads
- Slow human triage during outages
- Noisy and incomplete incident descriptions

Incident AI addresses this by:
- Standardizing classification (severity, category)
- Reusing historical incident patterns (RAG)
- Accelerating root-cause hypotheses
- Recommending actionable next steps
- Doing all of the above safely and at scale

---

## 3. What This System Actually Does (Concrete Outputs)

For every incident input, the system produces:

- **Severity** (P0 / P1 / P2)
- **Category** (performance, infra, deployment, etc.)
- **Probable root cause** (hypothesis, not fact)
- **Recommended actions** (human-verifiable)
- **Confidence score**
- **Source references** (historical incidents used)

All outputs are:
- Structured (JSON)
- Deterministic in shape
- Safe for downstream automation

---

## 4. What This System Explicitly Does NOT Do

This system is intentionally **not**:

- An autonomous remediation engine
- A replacement for human judgment
- A knowledge store inside the LLM
- A synchronous real-time responder
- A chatbot UI

Why these are excluded:
- Autonomous action requires higher trust
- Knowledge must remain auditable (RAG)
- Sync LLM calls destroy reliability
- UI concerns distract from core intelligence

Boundaries protect reliability.

---

## 5. Who This System Is For

Primary users:
- SRE teams
- Platform engineers
- Incident commanders
- Internal tooling teams

Secondary users:
- Automation pipelines
- Alerting systems
- Incident management platforms

This is **not optimized for casual end-users**.

---

## 6. Non-Technical Mental Model

Think of Incident AI as:

> **A junior incident analyst who is fast, consistent, and well-read — but never acts alone.**

It:
- Reads the incident
- Checks historical patterns
- Suggests hypotheses
- Recommends next steps
- Leaves final decisions to humans

---

# PART 2 — HOW TO READ THIS DOCUMENTATION

## 7. How to Read the Docs (Order Matters)

These documents are **deep and intentional**. Do not read randomly.

### Recommended Order

1. ARCHITECTURE.md  
2. INPUT_AND_SAFETY.md  
3. RAG_DESIGN.md + RAG_DESIGN_ASCII.md  
4. FINETUNING.md  
5. ASYNC_AND_RELIABILITY.md  
6. OBSERVABILITY_AND_COST.md  
7. ERRORS_AND_LESSONS.md + ERROR_TIMELINES.md  
8. ANTI_PATTERNS.md + decision trees  
9. FINAL_REVIEW_CHECKLIST.md  

---

# PART 3 — DOCUMENT MAP (WHAT EACH FILE COVERS)

## 8. ARCHITECTURE.md
**Explains**
- End-to-end system structure
- Sync vs async boundaries
- Request lifecycle
- Failure isolation

**Key Files**
- app/api/main.py
- app/bootstrap.py
- app/flow/incident_pipeline.py

---

## 9. INPUT_AND_SAFETY.md
**Explains**
- Validation & normalization
- Prompt injection defense
- PII handling
- Safety before RAG

**Key Files**
- app/api/schemas.py
- app/pipeline/normalize.py

---

## 10. RAG_DESIGN.md
**Explains**
- Why RAG exists
- Chunking strategy
- Retrieval thresholds
- Hallucination control

**Key Files**
- app/rag/ingest.py
- app/pipeline/retrieve.py

---

## 11. FINETUNING.md
**Explains**
- What fine-tuning is / is not
- Dataset design
- Eval strategy
- Rollback safety

**Key Files**
- scripts/train_finetune.py
- app/pipeline/infer.py

---

## 12. ASYNC_AND_RELIABILITY.md
**Explains**
- Background processing
- Retry taxonomy
- DLQ design
- Idempotency

**Key Files**
- app/asyncio/worker.py
- app/asyncio/dlq.py

---

## 13. OBSERVABILITY_AND_COST.md
**Explains**
- Metrics & logs
- Token accounting
- Alerts
- Cost guardrails

**Key Files**
- app/observability/*

---

## 14. ERRORS_AND_LESSONS.md
**Explains**
- Real failures encountered
- Root causes
- Mental model evolution

**Key Files**
- app/config/settings.py
- app/asyncio/worker.py

---

## 15. ANTI_PATTERNS.md
**Explains**
- Explicit DO NOTs
- Why shortcuts fail
- Architectural guardrails

**Key Files**
- app/bootstrap.py
- app/pipeline/*

---

## 16. FINAL_REVIEW_CHECKLIST.md
**Explains**
- Production readiness checks
- Hard deploy gates

---

# PART 4 — SYSTEM-WIDE MENTAL MODELS & GUARDRAILS

## 17. One-Sentence System Rule

> **FastAPI accepts work, async workers do work, RAG provides facts, fine-tuning enforces behavior, observability protects reality.**

If a change violates this sentence, it is probably wrong.

---

## 18. Allowed vs Disallowed Evolution

### Allowed
- Swapping vector stores
- Adding worker pools
- Adding fine-tuned models
- Improving retrieval strategies

### Disallowed
- Direct LLM calls in API
- Knowledge in fine-tuning
- Skipping safety
- Removing async boundaries

---

## 19. Why This Document Exists

Systems fail when:
- Context is lost
- Decisions are tribal
- Shortcuts go undocumented

This document:
- Preserves intent
- Prevents regressions
- Accelerates onboarding

---

## 20. Final Note

This repository treats GenAI as:

> **A powerful but untrusted dependency inside a carefully engineered system.**

The architecture — not the model — delivers reliability.

---

End of MASTER_DOC.md
