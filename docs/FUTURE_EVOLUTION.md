# FUTURE_EVOLUTION.md
## How This System Should Evolve (Without Breaking It)

This document defines **how Incident AI may evolve over time** while preserving its core guarantees.

It exists to prevent architectural drift.

---

## 1. Why Evolution Needs Rules

Most systems don’t fail because of bad initial design.  
They fail because **later changes violate original assumptions**.

GenAI systems are especially vulnerable because:
- Models change rapidly
- Teams rotate
- Pressure to “just ship” increases

This document defines **safe evolution paths**.

---

## 2. Core Invariants (Must Never Change)

These invariants are **non‑negotiable**:

1. No LLM calls in API layer  
2. All LLM work is async  
3. RAG supplies facts  
4. Fine‑tuning shapes behavior  
5. Input safety happens before embeddings  
6. Observability is mandatory  

Breaking any of these reintroduces known failures.

---

## 3. Multi‑Tenant Support

### Safe Additions
- Tenant ID in schemas
- Per‑tenant vector namespaces
- Per‑tenant rate limits
- Per‑tenant cost tracking

### Unsafe Approaches
- Shared vector space without isolation
- Cross‑tenant retrieval
- Single fine‑tuned model without controls

Multi‑tenancy must preserve isolation at **every layer**.

---

## 4. Enterprise & SOC2 Readiness

Recommended additions:
- Audit log persistence
- Access control around ingestion
- PII redaction evidence
- Configuration immutability

Already aligned:
- Structured logs
- Deterministic outputs
- Explicit safety boundaries

---

## 5. Scaling the System

### Safe Scaling
- Add more workers
- Split worker pools by task type
- Horizontal vector store scaling

### Unsafe Scaling
- Increasing API timeouts
- Increasing retries
- Making inference synchronous

Scaling must preserve async boundaries.

---

## 6. Model Evolution

Safe:
- Swap base models via config
- Add new fine‑tuned models
- A/B test inference behavior

Unsafe:
- Embedding knowledge in fine‑tuning
- Removing fallback models
- Hardcoding model names

Models must remain **replaceable dependencies**.

---

## 7. RAG Evolution

Safe:
- Better chunking strategies
- Metadata enrichment
- Hybrid retrieval (BM25 + vectors)

Unsafe:
- Removing thresholds
- Over‑stuffing context
- Storing unsafe raw data

RAG quality controls must strengthen over time, not weaken.

---

## 8. Automation & Remediation

Possible future:
- Human‑approved remediation
- Recommendation → approval → execution

Never allowed:
- Autonomous remediation without approval
- LLM‑initiated actions

Trust must increase **slowly and deliberately**.

---

## 9. What Success Looks Like Long‑Term

- Predictable cost
- Stable latency
- High trust in outputs
- Easy onboarding
- Few production surprises

If evolution reduces predictability, it is wrong.

---

## 10. Final Rule

> **Evolve capabilities, not assumptions.**

Assumptions are what keep the system safe.

---

End of FUTURE_EVOLUTION.md
