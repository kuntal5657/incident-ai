# FINAL_REVIEW_CHECKLIST.md
## Production Readiness Checklist for GenAI Systems

Use this before **any production deploy**.

---

## Architecture
- [ ] No LLM calls in API layer
- [ ] Async worker isolated
- [ ] Bootstrap wiring centralized

## Safety
- [ ] Pydantic validation everywhere
- [ ] Prompt injection sanitized
- [ ] PII scrubbed

## RAG
- [ ] Chunking semantic
- [ ] Similarity threshold applied
- [ ] top-K enforced

## Fine-Tuning
- [ ] Dataset >= 50 train / 10 eval
- [ ] Behavior-only tuning
- [ ] Fallback model configured

## Reliability
- [ ] Retry taxonomy defined
- [ ] DLQ enabled
- [ ] Idempotent jobs

## Observability
- [ ] Token metrics enabled
- [ ] Latency budgets enforced
- [ ] Alerts configured

## Cost
- [ ] Max tokens capped
- [ ] Context truncation active

---

## Final Rule

If you cannot check every box:
> **Do not deploy.**