## ⚠️ Disclaimer

This project is an **educational and architectural reference**.
It is not a drop-in product and should be adapted to your own security,
compliance, and operational requirements.

# Incident AI
### Production‑Grade GenAI Incident Intelligence System

Incident AI is a **real-world, production‑grade GenAI system** designed to assist engineering teams during incidents by providing **consistent classification, grounded analysis, and actionable recommendations** — safely, asynchronously, and at scale.

This repository is **not a demo**.  
It documents how modern GenAI systems should actually be built in production.

---

## What Incident AI Does

Given an incident report, the system produces:

- **Severity** (P0 / P1 / P2)
- **Category** (performance, infra, deployment, etc.)
- **Probable root cause** (hypothesis, not fact)
- **Recommended actions**
- **Confidence score**
- **Source references** (historical incidents used via RAG)

All outputs are:
- Structured (JSON)
- Deterministic in shape
- Designed for downstream automation

---

## What Incident AI Is NOT

Incident AI is intentionally **not**:

- An autonomous remediation engine
- A chatbot UI
- A synchronous real‑time responder
- A system that stores knowledge inside the LLM

These boundaries are deliberate and critical for safety and reliability.

---

## Core Architectural Principles

- **Async by default** (LLMs are slow & unreliable)
- **RAG for facts, fine‑tuning for behavior**
- **Strict input validation & safety**
- **Observable, measurable, and cost‑controlled**
- **Failure‑isolated by design**

> The architecture — not the model — provides reliability.

---

## Documentation (Start Here)

All documentation lives in the `docs/` directory.

**Read in this order:**

1. `MASTER_DOC.md` ← start here  
2. `ARCHITECTURE.md`  
3. `INPUT_AND_SAFETY.md`  
4. `RAG_DESIGN.md`  
5. `FINETUNING.md`  
6. `ASYNC_AND_RELIABILITY.md`  
7. `OBSERVABILITY_AND_COST.md`  
8. `ERRORS_AND_LESSONS.md`  
9. `ANTI_PATTERNS.md`  
10. `FINAL_REVIEW_CHECKLIST.md`  

Each document is intentionally **deep (3–4+ pages)**.

---

## Who This Is For

- SRE & Platform teams
- Incident commanders
- Internal tooling teams
- Engineers learning **production GenAI architecture**

Not optimized for casual or consumer usage.

---

## Key Mental Model

> **FastAPI accepts work, async workers do work,  
> RAG provides facts, fine‑tuning enforces behavior,  
> observability protects reality.**

If a change violates this sentence, it is probably wrong.

---

## Status

This repository represents a **complete reference architecture** for production GenAI systems.

It is suitable for:
- Internal adoption
- Architecture reviews
- GenAI onboarding
- Long‑term evolution

---
📚 Full documentation: [docs/README.md](docs/README.md)

© Incident AI — Production GenAI, engineered properly.
