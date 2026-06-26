# DCSE RAG Engine
**Doc:** DCSE-CP/RAG/20260624-001
**Status:** CANDIDATE MATERIAL — DCS REVIEW REQUIRED
**Authority:** Claude CP (CTO)

## Structure

```
rag_engine/
  config/
    sources.py          Approved RAG source paths, PS-isolated paths, exclusion rules
  ingestion/
    ps_firewall.py      PS firewall preflight — runs before any chunking or embedding
    pipeline.py         Full ingestion pipeline (load, chunk, embed, store)
  retrieval/
    query.py            Lane-filtered retrieval + DDNA generation envelope call
  generation/
    ddna_envelope.py    DDNA voice wrapper, PS context check, dual-mode output
  requirements.txt      All OSS dependencies — zero cloud API cost
```

## Prerequisites

1. Supabase local Docker running: `supabase start`
2. Confirm pgvector extension is enabled in local Postgres
3. Ollama installed and model pulled: `ollama pull llama3.1:8b`
4. Python dependencies: `pip install -r requirements.txt --break-system-packages`

## Environment Variables

```bash
export SUPABASE_LOCAL_URL="postgresql://postgres:postgres@localhost:54322/postgres"
export SUPABASE_LOCAL_ANON_KEY="your_local_anon_key"
```

Never hardcode credentials. Never commit `.env` files.

## Running Ingestion

```bash
cd rag_engine
python ingestion/pipeline.py
```

PS firewall runs first. Ingestion halts on any PS hit. Check logs for report.

## Running Validation Queries

```bash
cd rag_engine
python retrieval/query.py
```

Runs all three example queries from the execution spec and prints dual-mode output.

## Output Format

Every query returns:
```json
{
  "structured_data": {
    "source_files": [],
    "status_tags": [],
    "confidence": 0.0,
    "affected_modules": [],
    "lane": "DCSE"
  },
  "narrative_summary": "Markdown string"
}
```

## Gates

- Step 2 complete when: ingestion runs clean, PS firewall clears, vector count reported to Claude CP
- Step 4 gate: all three validation queries return valid dual-mode payloads — Claude CP reviews before Step 5
