# Documentation Guide – Incident AI

Welcome to the **Incident AI documentation**.

This directory contains **deep, production-grade documentation** explaining how the system is designed, why certain architectural decisions were made, and how to safely evolve it over time.

If you are new to this repository, **start here**.

---

## How to Read These Docs (Very Important)

These documents are **not tutorials**.  
They are written to document a **real production GenAI system**.

👉 **Do not read them randomly.**  
Each document builds context for the next.

### Recommended Reading Order

1. **MASTER_DOC.md**  
   *Authoritative entry point*  
   Explains:
   - What the system is / is not
   - Mental models
   - How all documents fit together

2. **ARCHITECTURE.md**  
   End-to-end system structure, request flow, async boundaries

3. **INPUT_AND_SAFETY.md**  
   Input validation, prompt injection defense, PII handling

4. **RAG_DESIGN.md**  
   Retrieval-Augmented Generation design and reasoning

5. **RAG_DESIGN_ASCII.md**  
   Visual (ASCII) diagrams for chunking, retrieval, thresholds

6. **FINETUNING.md**  
   Fine-tuning strategy, dataset design, and misconceptions

7. **ASYNC_AND_RELIABILITY.md**  
   Background processing, retries, DLQ, idempotency

8. **OBSERVABILITY_AND_COST.md**  
   Metrics, logging, alerting, token & cost control

9. **ERRORS_AND_LESSONS.md**  
   Real failures encountered and how design evolved

10. **ERROR_TIMELINES.md**  
    Visual failure timelines and debugging sequences

11. **ANTI_PATTERNS.md**  
    Explicit DO-NOT-DO rules

12. **ANTI_PATTERNS_DECISION_TREES.md**  
    Fast decision trees for reviews and design choices

13. **FINAL_REVIEW_CHECKLIST.md**  
    Hard production readiness checklist

14. **FUTURE_EVOLUTION.md**  
    How the system may evolve safely over time

---

## What These Docs Are Optimized For

These documents are written for:

- SRE & Platform engineers
- Backend engineers building GenAI systems
- Architecture reviewers
- Engineers onboarding into the system

They are **not optimized for casual readers or UI usage**.

---

## Design Philosophy (Quick Summary)

All documentation is written with these assumptions:

- LLMs are **untrusted external dependencies**
- Architecture provides reliability, not models
- Async execution is mandatory
- RAG provides facts, fine-tuning enforces behavior
- Observability is a first-class requirement

If a design contradicts these assumptions, it is probably wrong.

---

## Where to Start (TL;DR)

If you have limited time:

- **New to the system?** → Read `MASTER_DOC.md`
- **Reviewing architecture?** → Read `ARCHITECTURE.md`
- **Debugging bad outputs?** → Read `RAG_DESIGN.md` + `ERRORS_AND_LESSONS.md`
- **Preparing for production?** → Read `FINAL_REVIEW_CHECKLIST.md`

---

## Contribution Rule

If you add a new document:

1. Link it here
2. Link it from `MASTER_DOC.md`
3. Preserve existing mental models

Documentation drift is treated as a bug.

👉 Start here: [MASTER_DOC.md](MASTER_DOC.md)


---

End of docs/README.md
