# DCSE-CP RESPONSE PACKET — Supabase/pgvector RAG DDNA Build Plan
**Document ID:** DCSE-CP/CODEX/HANDOFF/20260624-002
**Status:** CANDIDATE MATERIAL — DCS REVIEW REQUIRED
**Posture:** Hand-off material for Codex. Candidate-only.

## 1. Goal Description
Provide a comprehensive build plan for the Supabase/pgvector RAG DDNA architecture. This document serves as the formal hand-off to Codex for implementation. It includes recommendations for a fully no-cost, locally hosted architecture prioritizing learning, training, and data privacy (PS-protected segregation compliance).

## 2. Related Folders & Workspace Intel
The following repositories and local directories have been identified and mapped as part of the DCSE ecosystem.

### GitHub Repositories (Cloned/Verified Local)
- **DCSE-Command-Post:** `c:\DS All Things\DCSE_Command_Center`
- **DCSE-Tribunal-Relay:** `c:\DS All Things\DCSE-Tribunal-Relay`
- **s1-assessment:** `c:\DS All Things\s1-assessment`

### Downloads Target (`\\desktop-pg1jate\Downloads\`)
- `\\desktop-pg1jate\Downloads\DCSE Prompt Library`
- `\\desktop-pg1jate\Downloads\DCSE_Desktop_CoWork`

### TSL & CTJ Intel
- **CTJ (Candidate Target Journey / Job):** 
  - **Folder Identified:** `\\desktop-pg1jate\Downloads\SC GYTO Strategic Clarity Assessment v7.1\DCSE SC GYTO CTJ Build 022026`
  - **Status:** Verified. Inherits Macro Governance and governed as a Micro Governance output family. 
- **TSL:** 
  - **Folder Identified:** *Unknown/Unverified in standard sweeps.* 
  - **Status:** TSL is not defined in any current project file or sweeping up to depth 4 in Downloads. 
  - **Action Required:** Point to the exact TSL files/folder, or authorize an "interview me" pass to define the specifications for TSL so a proper doctrine can be established.

## 3. No-Cost Build Recommendations (Learning/Training Emphasis)
The prior Command Post Intel brief specified LlamaIndex + LangChain + LangSmith, which carries hidden recurring costs (LangSmith trace volume, OpenAI embeddings). 
For a **zero-cost, highly educational** build, we recommend the following stack. This utilizes **Supabase/pgvector** as requested while remaining free by hosting locally:

| Layer | Recommended Zero-Cost Stack | Justification (Learning & Privacy) |
| :--- | :--- | :--- |
| **Retrieval/Index** | **LlamaIndex** | Industry standard for advanced retrieval strategies (hierarchical chunking, sub-question decomposition). |
| **Embeddings** | **Local embeddings** (e.g., `sentence-transformers BAAI/bge-small-en-v1.5` or `all-MiniLM-L6-v2`) | No API key, runs on CPU. Ensures PS-protected data never leaves the local firewall. |
| **Vector Store** | **Supabase (Local Docker) + pgvector** | Replaces ChromaDB. Gives you a production-grade PostgreSQL environment locally. Incredible for training/learning full-stack engineering without cloud costs. |
| **LLM Generation** | **Ollama** (Llama 3.1 8B / Mistral 7B) | Drop-in replacement for paid APIs. Keeps generation entirely local and free. |
| **Orchestration** | **LangChain** (OSS) | Free open-source tier. Excellent for stateful multi-agent workflows. |
| **Observability** | **OpenTelemetry** / local trace log | Replaces LangSmith (which bills past free tier). LlamaIndex supports OTel instrumentation natively. |

## 4. Proposed DDNA Implementation Strategy
The **DDNA (Digital DNA)** layer consists of tone calibration, voice controls, prohibited phrases, and the PS firewall. 

1. **Separation of Concerns:** 
   - RAG (Supabase/pgvector + LlamaIndex) handles **Retrieval**.
   - DDNA lives in the **Generation Envelope** (LangChain prompt wrappers).
2. **Implementation:** 
   - Every generation call via Ollama must be wrapped in a LangChain prompt template that enforces the DDNA constraints *before* output.
   - This prevents the Vector Store from being burdened with stylistic enforcement, keeping pgvector purely optimized for semantic search.

## 5. Codex Hand-Off Instructions
> [!IMPORTANT]
> **To Codex:** Do not proceed with automation or broad code generation until the local Supabase Docker container is verified operational. 

**Execution Steps for Codex:**
1. **Infrastructure Setup:** Initialize the local Supabase instance using Docker CLI. Verify that the `pgvector` extension is enabled in the local PostgreSQL instance.
2. **Ingestion Pipeline:** Build a Python script using LlamaIndex and `sentence-transformers` to chunk and embed documents from the `DCSE Prompt Library`, storing the vectors in Supabase.
3. **Retrieval Service:** Implement a LangChain orchestration layer that queries Supabase/pgvector and passes the retrieved context to Ollama for local generation.
4. **Verification:** Confirm all data remains local (monitor outbound network traffic) and that responses adhere to the DDNA envelope formatting rules.

## 6. Open Questions for DCS
1. **TSL Definition:** Where are the TSL materials located, or should we schedule a spec interview to create them?
2. **Supabase Local vs Cloud:** Confirm that the local Docker approach for Supabase is preferred over the cloud free-tier (which has storage/compute limits).
3. **Target Repositories:** Should Codex write this RAG pipeline into `DCSE-Command-Post` or establish a new dedicated repository?
