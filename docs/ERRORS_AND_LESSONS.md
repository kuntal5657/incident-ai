# ERRORS_AND_LESSONS.md
## Errors, Failures, Mental Context & Lessons Learned (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It captures **real errors encountered while building the system**,  
> **why they happened**, **how they were fixed**, and most importantly  
> **how our mental model evolved** after each failure.

This is the document most teams never write — and the one that saves the most time later.

---

## 1. Why This Document Exists

Most documentation explains:
- What the system does
- How it works when everything is fine

Almost none explain:
- What broke
- Why it broke
- How thinking changed after fixing it

In production GenAI systems:
> **Failures are the fastest teachers — if you preserve the lesson.**

This document preserves those lessons.

---

## 2. Error Category Overview

We encountered failures in five major categories:

1. Environment & configuration
2. Schema & validation
3. Async execution
4. RAG & vector store integration
5. LLM & fine-tuning assumptions

Each category changed how the system was designed.

---

## 3. Environment & Configuration Errors

### 3.1 OPENAI_API_KEY Not Found (uvicorn reload)

**Symptom**
```
RuntimeError: OPENAI_API_KEY is not set
```

**Context**
- Code worked in scripts
- Failed when running `uvicorn --reload`

**Root Cause**
- Reload process did not inherit environment variables
- `.env` was placed in a subdirectory

**Fix**
- Move `.env` to project root
- Explicit environment validation at startup

**Files Involved**
- app/config/settings.py
- app/api/main.py

**Lesson Learned**
> Environment configuration must fail fast and loudly.

Never assume runtime environments are identical.

---

## 4. Schema & Validation Failures

### 4.1 Async Jobs Bypassing Validation

**Symptom**
```
ValidationError: environment field required
```

**Context**
- Sync pipeline worked
- Async worker failed randomly

**Root Cause**
- Async jobs were created from raw dicts
- Validation only existed at API boundary

**Fix**
- Shared Pydantic schema
- Re-validate payload inside worker

**Files Involved**
- app/api/schemas.py
- app/asyncio/worker.py

**Mental Model Shift**
> Validation is not a one-time event — it is a contract enforced everywhere.

---

## 5. Async & Execution Errors

### 5.1 Worker Crashing Pipeline

**Symptom**
- Entire pipeline stopped after one job failure

**Root Cause**
- Exceptions not isolated per job
- Worker process shared execution context

**Fix**
- Per-job try/except
- Explicit job state transitions

**Files Involved**
- app/asyncio/worker.py
- app/asyncio/status.py

**Lesson**
> One job must never be able to kill the system.

---

## 6. RAG & Vector Store Failures

### 6.1 Vector Store Contract Mismatch

**Symptom**
```
AttributeError: object has no attribute 'search'
```

**Context**
- Pipeline assumed a vector store interface
- Placeholder implementation did not comply

**Root Cause**
- No explicit interface contract
- Vector store instantiated ad-hoc

**Fix**
- Adapter-based vector store
- Single bootstrap wiring point

**Files Involved**
- app/adapters/vector_store_adapter.py
- app/bootstrap.py

**Mental Model Shift**
> Infrastructure must be wired once, not everywhere.

---

## 7. RAG Quality Failures

### 7.1 Irrelevant Context Returned

**Symptom**
- LLM responses were generic
- Root causes didn’t match history

**Root Cause**
- No similarity threshold
- Too many chunks injected

**Fix**
- Top-K limit
- Similarity threshold
- Metadata filtering

**Files Involved**
- app/pipeline/retrieve.py

**Lesson**
> More context is often worse than less context.

---

## 8. Fine-Tuning Assumption Errors

### 8.1 Fine-Tuning Job Failing

**Symptom**
```
invalid_n_examples: must have at least 10 examples
```

**Root Cause**
- Insufficient training/eval data
- Misunderstanding fine-tuning requirements

**Fix**
- Enforced dataset size rules
- Clear separation of train vs eval

**Files Involved**
- scripts/train_finetune.py

**Mental Model Shift**
> Fine-tuning is strict, not forgiving.

---

## 9. Misplaced Expectations from Fine-Tuning

**Initial Assumption**
- Fine-tuning would “remember” incidents

**Reality**
- Fine-tuning only affects behavior

**Correction**
- Move all knowledge to RAG
- Use fine-tuning for structure & consistency

**Result**
- Better accuracy
- Easier updates
- Lower retraining cost

---

## 10. Observability Gaps

### 10.1 No Counters Visible

**Symptom**
- Logs existed
- Metrics were empty

**Root Cause**
- Metrics snapshot logged before increments

**Fix**
- Emit metrics after pipeline completion
- Centralized metric recording

**Files Involved**
- app/observability/metrics.py
- app/flow/incident_pipeline.py

**Lesson**
> Observability must reflect reality, not intention.

---

## 11. Cost-Related Near Misses

### 11.1 Token Usage Spike

**Context**
- RAG returned too many chunks
- Prompt size grew silently

**Detection**
- Token metrics showed spike

**Fix**
- Context truncation
- Max token limits

**Files Involved**
- app/pipeline/infer.py

**Lesson**
> Cost issues are latency issues in disguise.

---

## 12. Mental Models That Emerged

Over time, these models became guiding principles:

- **FastAPI is a traffic controller, not a brain**
- **LLMs are external dependencies, not libraries**
- **Async isolates failure**
- **RAG provides facts, fine-tuning provides behavior**
- **Observability is part of architecture**

These models now guide all decisions.

---

## 13. What We Would Do Differently

If starting again:
- Define vector store interface earlier
- Add similarity thresholds from day one
- Enforce schema everywhere immediately
- Add token metrics sooner

These changes would save weeks.

---

## 14. Why This Document Matters

Most production issues repeat because:
- Past failures are forgotten
- Context is lost
- New engineers repeat old mistakes

This document:
- Preserves institutional memory
- Accelerates onboarding
- Prevents regressions

---

## 15. Summary

Errors were not setbacks — they were **design inputs**.

By:
- Capturing them
- Understanding them
- Adjusting architecture

We built a system that is:
- Safer
- More reliable
- Easier to operate

This is how real GenAI systems mature.
