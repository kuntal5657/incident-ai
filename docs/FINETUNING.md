# FINETUNING.md
## Fine-Tuning Strategy – Behavior Alignment, Not Knowledge (Deep Dive)

> This document is intentionally **deep (≈3–4 pages)**.  
> It explains **what fine-tuning is**, **what it is NOT**, **how to design datasets**,  
> **how it interacts with RAG**, and **why misuse causes failures**.

If you understand this document, you understand **when fine-tuning helps and when it harms**.

---

## 1. Why Fine-Tuning Exists (And Why It’s Often Misused)

Fine-tuning is one of the **most misunderstood** parts of GenAI systems.

Many teams believe:
- “Fine-tuning stores knowledge” ❌
- “Fine-tuning replaces RAG” ❌
- “More data always helps” ❌

Reality:
> **Fine-tuning aligns behavior, not facts.**

---

## 2. What Fine-Tuning Is (In This System)

In Incident AI, fine-tuning is used for:

- Severity classification consistency
- Category labeling consistency
- Output structure stability
- Reduced prompt complexity

Fine-tuning ensures that:
- P1 vs P2 decisions are consistent
- Output JSON schema is respected
- Model tone and format are stable

---

## 3. What Fine-Tuning Is NOT Used For

Fine-tuning is explicitly **NOT** used for:

❌ Storing historical incidents  
❌ Learning logs or alerts  
❌ Replacing retrieval  
❌ Long-term memory  

Why?
- Fine-tuned models are static
- Updating data requires retraining
- Cost increases rapidly
- Debugging becomes impossible

Historical data belongs in **RAG**, not fine-tuning.

---

## 4. Behavioral vs Knowledge Learning

### Behavioral Learning (Fine-Tuning)
- “How should the model respond?”
- “What format should it use?”
- “How strict should severity be?”

### Knowledge Learning (RAG)
- “What happened before?”
- “Which incidents are similar?”
- “What patterns exist historically?”

This separation is **non-negotiable**.

---

## 5. Dataset Design (Most Important Section)

### 5.1 Dataset Format

Fine-tuning data uses **JSONL** format.

Each line:
- Input prompt (incident summary)
- Expected structured output

Files:
- scripts/train_finetune.py

---

### 5.2 Training vs Evaluation Data

Training data:
- Teaches behavior
- Model learns patterns

Evaluation data:
- Measures generalization
- Detects overfitting

Rules enforced:
- ≥ 50 training examples
- ≥ 10 evaluation examples

Why?
> Smaller datasets cause overfitting and unstable models.

---

### 5.3 Example Training Record

```json
{
  "messages": [
    {"role": "system", "content": "You are an incident classifier"},
    {"role": "user", "content": "Order API latency spike in production"},
    {"role": "assistant", "content": "{\"severity\":\"P1\",\"category\":\"Performance\"}"}
  ]
}
```

Key rule:
> Outputs must be deterministic.

---

## 6. Common Dataset Mistakes (And Consequences)

### Mistake 1: Putting Knowledge in Fine-Tuning
Result:
- Stale answers
- Retraining required for updates

### Mistake 2: No Eval Dataset
Result:
- Silent overfitting
- False confidence

### Mistake 3: Inconsistent Outputs
Result:
- Broken downstream parsing

---

## 7. Fine-Tuning Job Lifecycle

1. Prepare train.jsonl & eval.jsonl
2. Upload files to OpenAI
3. Start fine-tuning job
4. Monitor status
5. Capture model ID
6. Use model in inference

Files:
- scripts/train_finetune.py
- scripts/check_finetune_status.py

---

## 8. Using Fine-Tuned Model in Production

The system:
- Dynamically selects fine-tuned model if configured
- Falls back to base model otherwise

Files:
- app/pipeline/infer.py
- app/config/settings.py

Why fallback matters:
- Fine-tuned model may be unavailable
- Rollback must be instant

---

## 9. Why Fine-Tuning Comes AFTER RAG

Order:
Normalize → RAG → Fine-Tuned Inference

Why:
- Facts first
- Behavior second

Reversing this causes:
- Guessing before context
- Worse results

---

## 10. Cost & Latency Considerations

Fine-tuned models:
- Often faster for classification
- Reduce prompt length
- But cost more per token

Trade-off:
> Fine-tune for high-volume, repetitive tasks.

---

## 11. Failure Modes

### Overfitting
Cause:
- Small or biased dataset

Mitigation:
- Eval set
- Conservative dataset size

### Dataset Drift
Cause:
- Incident patterns change

Mitigation:
- Periodic retraining
- RAG handles freshness

---

## 12. Mental Model to Keep

Think of fine-tuning as:
> **Training a junior analyst on how to think, not what happened.**

The facts still come from reports (RAG).

---

## 13. Summary

Fine-tuning:
- Shapes behavior
- Enforces consistency
- Reduces prompt complexity

It does NOT:
- Store knowledge
- Replace RAG
- Eliminate safety needs

Used correctly, it makes systems reliable.  
Used incorrectly, it creates silent failures.
