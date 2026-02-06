# RAG_DESIGN.md
## Retrieval‑Augmented Generation (RAG) – Deep Design & Trade‑offs

> This document is intentionally **deep (≈3–4 pages)**.  
> It explains **why RAG exists**, **how it is implemented**, **design trade‑offs**,  
> **failure modes**, and **exact file‑level mapping**.

If you understand this document fully, you understand **how to ground LLMs in reality**.

---

## 1. Why RAG Exists (The Core Problem)

Large Language Models:
- Do not have real memory
- Are frozen at training time
- Hallucinate when unsure

Fine‑tuning **cannot solve this**:
- Fine‑tuning encodes behavior, not facts
- Updating data would require retraining
- Historical incidents change frequently

Therefore:
> **We must fetch real data at inference time**

This is exactly what RAG does.

---

## 2. What RAG Is (In This System)

RAG = **Retrieve relevant historical incidents**  
→ **Inject them as context into the LLM prompt**  
→ **Ground the response in real data**

In this system, RAG is used for:
- Root‑cause grounding
- Pattern recognition
- Historical similarity

RAG is **not** used for:
- Output formatting
- Classification consistency (fine‑tuning handles that)

---

## 3. RAG High‑Level Flow

### Ingestion (Offline / Admin Time)

1. Historical incident arrives
2. Input normalization & safety applied
3. Content is chunked
4. Each chunk is embedded
5. Embeddings stored with metadata

### Retrieval (Inference Time)

1. Incoming incident is normalized
2. Query embedding is generated
3. Vector similarity search runs
4. Top‑K chunks selected
5. Context assembled for prompt

---

## 4. Ingestion Pipeline (Detailed)

### 4.1 Why Ingestion Is Separate

We **never embed at request time** for historical data.

Why:
- Embedding is expensive
- Data is reused many times
- Safety must be guaranteed once

Files:
- app/rag/ingest.py

---

### 4.2 Chunking Strategy (Critical)

#### Naïve Chunking (Anti‑Pattern)
❌ Fixed token length chunks  
❌ Breaks semantic meaning  
❌ Loses incident boundaries  

#### Correct Chunking (This System)
✔ Semantic sections (summary, logs, alerts)  
✔ Metadata‑aware chunks  
✔ Stable identifiers  

Example metadata:
- incident_id
- service
- environment
- chunk_type

Why this matters:
- Better retrieval relevance
- Traceable sources
- Reduced hallucination

---

### 4.3 Embedding Generation

Embeddings are generated using OpenAI embedding models.

Files:
- app/adapters/embedding_adapter.py

Design decisions:
- Single adapter interface
- Model configurable
- Retry & error handling centralized

Why adapter?
> To avoid vendor lock‑in and enable testing.

---

### 4.4 Vector Store Design

The vector store:
- Stores embeddings + metadata
- Supports similarity search
- Returns scores

Files:
- app/adapters/vector_store_adapter.py

Design principles:
- Adapter‑based
- Swappable backend
- Explicit search contract

Why this matters:
- Easy migration (FAISS → Pinecone → pgvector)
- Consistent retrieval behavior

---

## 5. Retrieval Pipeline (Inference Time)

### 5.1 Query Embedding

Incoming incident:
- Is normalized & sanitized
- Converted into query embedding

Files:
- app/pipeline/retrieve.py

---

### 5.2 Similarity Search

Vector search returns:
- Top‑K chunks
- Similarity scores
- Metadata

We do **not blindly trust results**.

---

### 5.3 Threshold & Filtering Strategy

Why filtering matters:
- Low‑similarity chunks confuse the LLM
- Too much context increases token cost

Controls:
- Minimum similarity threshold
- Max number of chunks
- Metadata filtering (service, env)

This prevents:
- Context dilution
- Hallucination amplification

---

## 6. Context Assembly

Retrieved chunks are:
- Ordered by relevance
- Deduplicated
- Structured into sections

Injected into prompt as:
- “Historical context”
- Not instructions

Why:
> Context must inform, not control, the LLM.

Files:
- app/pipeline/retrieve.py

---

## 7. RAG Failure Modes (Very Important)

### 7.1 No Relevant Results

Behavior:
- Retrieval returns empty
- LLM runs with no context

Design choice:
- Fail gracefully
- Do NOT hallucinate past incidents

---

### 7.2 Irrelevant Results

Causes:
- Poor chunking
- Weak embeddings
- Missing metadata filters

Mitigation:
- Threshold tuning
- Better chunk design

---

### 7.3 Stale Data

RAG only works if:
- Ingestion is maintained
- Old data is archived

Operational note:
> RAG requires data hygiene.

---

## 8. Why RAG Is Before Fine‑Tuned Inference

Order matters:

Normalize  
→ RAG  
→ LLM  

If reversed:
- LLM guesses before seeing facts
- Output quality drops

This order is enforced in:
- app/flow/incident_pipeline.py

---

## 9. Observability for RAG

We measure:
- Retrieval latency
- Number of chunks returned
- Similarity distribution

Why:
- Tune thresholds
- Detect retrieval drift

Files:
- app/observability/metrics.py

---

## 10. What Breaks If You Skip Proper RAG

Without proper RAG:
- LLM hallucinates root causes
- Recommendations become generic
- Trust in system erodes

This is one of the **most common GenAI production failures**.

---

## 11. Mental Model to Keep

Think of RAG as:
> **A fact‑checking assistant sitting next to the LLM**

Without it, the LLM is guessing.

---

## 12. Summary

RAG exists to:
- Ground LLM output in reality
- Reduce hallucination
- Preserve traceability
- Enable continuous learning

Fine‑tuning shapes behavior.  
RAG supplies facts.

Both are required.
