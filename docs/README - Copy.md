incident-ai/
├── README.md
├── pyproject.toml
├── .env.example
├── app/
│   ├── main.py                 # API entrypoint
│   ├── flow/
│   │   └── incident_pipeline.py
│   ├── pipeline/
│   │   ├── base.py
│   │   ├── normalize.py
│   │   ├── retrieve.py
│   │   ├── route.py
│   │   ├── infer.py
│   │   └── validate.py
│   ├── strategies/
│   │   ├── model_strategy.py
│   │   └── retrieval_strategy.py
│   ├── adapters/
│   │   ├── openai_adapter.py
│   │   ├── vector_store_adapter.py
│   │   └── telemetry_adapter.py
│   ├── schemas/
│   │   └── incident_output.py
│   ├── safety/
│   │   ├── pii_scrubber.py
│   │   └── injection_guard.py
│   ├── config/
│   │   └── settings.py
│   └── observability/
│       └── tracing.py
├── eval/
├── scripts/
└── data/

## Environment Setup

1. Copy the example environment file:

```bash
cp .env.example .env

2. Set your OpenAI API key:

OPENAI_API_KEY=sk-...

3. Create a fresh venv

python -m venv venv

4. Activate it

Windows (PowerShell):
venv\Scripts\activate

5. Install dependencies:
pip install -e .

6. (Optional) Verify OpenAI connectivity:

python scripts/test_openai_connection.py



## Input Validation & Safety

All incident inputs go through a strict normalization pipeline:

- Schema validation (Pydantic)
- PII scrubbing (emails, IPs, secrets)
- Prompt injection sanitization
- Canonical normalization

This ensures:
- LLM safety
- Legal compliance
- Predictable behavior

## Retrieval-Augmented Generation (RAG)

This system uses RAG to ground LLM outputs in historical data.

### Ingestion Flow
1. Normalized incidents are chunked semantically
2. Each chunk is embedded using OpenAI embeddings
3. Embeddings are stored in a vector store with metadata

### Design Notes
- Chunking is metadata-aware
- Embeddings are generated offline
- Vector store is adapter-based and swappable

python scripts/test_rag_ingestion.py


## Context Retrieval (RAG)

During inference, the system:

1. Builds a semantic query from the incident
2. Embeds the query using OpenAI embeddings
3. Retrieves top-K similar chunks
4. Filters weak matches
5. Assembles LLM-ready context

If no strong context is found, the system proceeds with empty context.

python scripts/test_retrieval.py

## LLM Inference & Classification

The system uses structured prompting and schema validation to produce
machine-consumable incident classifications.

Key properties:
- Deterministic inference (temperature = 0)
- Base vs fine-tuned model routing
- Strict JSON schema enforcement
- Fail-fast on invalid outputs

python scripts/test_full_pipeline.py

Dataset File Structure
-------------------------
data/
└── fine_tuning/
    ├── README.md
    ├── train.jsonl
    └── eval.jsonl

python scripts/train_finetune.py
Copy the job ID
Job ID: ftjob-abc123

python scripts/check_finetune_status.py