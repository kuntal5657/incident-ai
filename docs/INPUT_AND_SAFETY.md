# INPUT_AND_SAFETY.md
## Input Validation, Normalization & LLM Safety (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It explains **why input safety exists**, **how it is enforced**,  
> **what breaks if skipped**, and **which files implement each control**.

In production GenAI systems, **input handling is the first and strongest safety boundary**.

---

## 1. Why Input & Safety Is a First-Class Concern

LLMs are:
- Extremely powerful
- Extremely trusting
- Extremely unsafe if misused

They will:
- Obey malicious instructions
- Echo sensitive data
- Hallucinate confidently

Therefore:
> **Every GenAI system must treat input as untrusted by default.**

This system enforces safety **before**:
- Embeddings
- Retrieval (RAG)
- LLM inference

---

## 2. Threat Model (What Can Go Wrong)

Before designing safety, we define the threat surface.

### 2.1 Malformed Input
- Missing required fields
- Wrong data types
- Extremely long text

### 2.2 Prompt Injection
Examples:
- “Ignore previous instructions”
- “You are now a system admin”
- “Leak internal configuration”

### 2.3 PII & Sensitive Data
- Emails
- IP addresses
- Secrets / API keys
- User identifiers

### 2.4 Downstream Contamination
Unsafe input can:
- Pollute embeddings
- Poison vector store
- Influence future outputs

---

## 3. Input Validation Pipeline (Step-by-Step)

All requests go through a **strict, deterministic pipeline**.

### Step 1: Schema Validation (Pydantic)

Files:
- app/api/schemas.py

What happens:
- Required fields enforced
- Types validated
- Extra fields rejected

Why:
- Prevents undefined behavior
- Fails fast
- Produces clear errors

Example:
```json
{
  "incident_id": "INC-1001",
  "environment": "prod"
}
```
Missing fields → request rejected immediately.

---

### Step 2: Canonical Normalization

Files:
- app/pipeline/normalize.py

Actions:
- Trim whitespace
- Lowercase enums
- Normalize empty lists
- Canonical field ordering

Why:
- Prevents duplicate embeddings
- Improves retrieval quality
- Ensures predictable prompts

---

## 4. Prompt Injection Defense

### 4.1 What Is Prompt Injection

Prompt injection attempts to:
- Override system instructions
- Escalate privileges
- Manipulate outputs

### 4.2 Defense Strategy

This system:
- Treats all user input as **data**, never instructions
- Separates system prompt from user content
- Sanitizes known injection patterns

Example patterns removed:
- “ignore previous instructions”
- “act as system”
- “you are chatgpt”

Files:
- app/pipeline/normalize.py

---

## 5. PII Scrubbing & Compliance

### 5.1 Why PII Must Be Removed

Sending PII to LLM providers:
- Violates privacy expectations
- Creates compliance risk
- Increases breach impact

### 5.2 What Is Scrubbed

- Email addresses
- IP addresses
- Tokens / secrets
- User identifiers

Scrubbing happens:
- Before embeddings
- Before storage
- Before inference

Files:
- app/pipeline/normalize.py

---

## 6. Why Safety Happens Before RAG

### Dangerous Anti-Pattern
❌ Generate embeddings from raw input

Why this is bad:
- Unsafe data becomes permanently stored
- Future queries retrieve poisoned context
- Cleanup is extremely hard

### Correct Pattern
✔ Normalize → Sanitize → Embed

This is a **one-way gate**.

---

## 7. Input Size & Resource Controls

### Why Limits Matter

Without limits:
- Token explosion
- Cost spikes
- Latency degradation

Controls applied:
- Max input length
- Chunk size limits
- Field-level caps

Files:
- app/api/schemas.py
- app/pipeline/normalize.py

---

## 8. Safety in Async Context

Async processing introduces risk:
- Payloads may bypass API validation
- Jobs may be replayed

Defense:
- Shared schemas for sync & async
- Re-validation inside worker

Files:
- app/asyncio/worker.py
- app/api/schemas.py

---

## 9. Observability for Safety

Every safety action is observable.

We log:
- Validation failures
- Sanitization events
- Rejected requests

Why:
- Auditability
- Debugging
- Compliance evidence

Files:
- app/observability/logger.py
- app/observability/metrics.py

---

## 10. What Breaks If You Skip Input Safety

If you skip this layer:
- Prompt injection succeeds
- PII leaks to LLMs
- Vector store becomes corrupted
- Costs explode silently
- Legal risk increases

These failures **compound over time**.

---

## 11. Mental Model to Keep

Think of input handling as:
> **A customs checkpoint at the border**

Once unsafe data crosses:
- You cannot reliably remove it later

---

## 12. Summary

Input & safety is:
- Not optional
- Not cosmetic
- Not “nice to have”

It is the **foundation** of safe GenAI systems.

This architecture enforces safety **by design**, not by hope.
