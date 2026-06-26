"""
DCSE RAG Engine — Retrieval Service
Doc: DCSE-CP/RAG/RETRIEVAL/20260624-001
Status: CANDIDATE MATERIAL — DCS REVIEW REQUIRED

Queries Supabase pgvector via LlamaIndex.
Passes retrieved context to DDNA generation envelope (ddna_envelope.py).
Lane filter applied at query time — every call must include a lane parameter.
"""

import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("dcse.rag.retrieval")

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from generation.ddna_envelope import generate

VALID_LANES = {"SC", "SS", "DCSE"}
PS_LANES = {"PS"}


def retrieve_and_generate(
    query: str,
    lane: str,
    supabase_connection_string: str,
    top_k: int = 5,
    ollama_model: str = "llama3.1:8b",
    ollama_base_url: str = "http://localhost:11434",
) -> dict:
    """
    Full RAG pipeline for a single query:
    1. Validate lane (halt if PS)
    2. Retrieve top_k chunks from Supabase pgvector filtered by lane
    3. Pass context to DDNA generation envelope
    4. Return dual-mode payload

    lane must be one of: SC, SS, DCSE
    PS queries are hard-stopped — route to PS-designated session instead.
    """

    # Lane validation
    if lane in PS_LANES:
        logger.error("PS lane query attempted via main retrieval service. HALT.")
        return {
            "structured_data": {
                "source_files": [],
                "status_tags": ["PS_LANE_HALT"],
                "confidence": 0.0,
                "affected_modules": [],
                "lane": "PS_BLOCKED",
            },
            "narrative_summary": (
                "PS lane queries cannot be routed through the main retrieval service. "
                "Route to PS-designated session with explicit DCS Level 0 authorization."
            ),
        }

    if lane not in VALID_LANES:
        logger.warning("Unknown lane '%s' — defaulting to DCSE.", lane)
        lane = "DCSE"

    # Load embeddings and vector store
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        from llama_index.vector_stores.supabase import SupabaseVectorStore
        from llama_index.core import VectorStoreIndex, StorageContext
        from llama_index.core.vector_stores import MetadataFilter, MetadataFilters
    except ImportError as e:
        logger.error("Missing dependency: %s", e)
        return {
            "structured_data": {"source_files": [], "status_tags": ["dependency_error"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": f"Retrieval dependency error: {e}",
        }

    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    try:
        vector_store = SupabaseVectorStore(
            postgres_connection_string=supabase_connection_string,
            collection_name="dcse_rag_vectors",
            dimension=384,  # BAAI/bge-small-en-v1.5 — do not change without re-ingesting all vectors
        )
    except Exception as e:
        logger.error("Failed to connect to Supabase vector store: %s", e)
        return {
            "structured_data": {"source_files": [], "status_tags": ["connection_error"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": f"Vector store connection failed: {e}",
        }

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
        storage_context=storage_context,
    )

    # Lane-filtered retrieval
    lane_filter = MetadataFilters(
        filters=[MetadataFilter(key="lane", value=lane)]
    )

    retriever = index.as_retriever(
        similarity_top_k=top_k,
        filters=lane_filter,
    )

    logger.info("Retrieving top %d chunks for query (lane=%s)...", top_k, lane)
    try:
        nodes = retriever.retrieve(query)
    except Exception as e:
        logger.error("Retrieval failed: %s", e)
        return {
            "structured_data": {"source_files": [], "status_tags": ["retrieval_error"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": f"Retrieval failed: {e}",
        }

    if not nodes:
        logger.warning("No results returned for query.")
        return {
            "structured_data": {"source_files": [], "status_tags": ["no_results"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": "No relevant content found for this query in the current knowledge base.",
        }

    # Build context string from retrieved nodes
    context_parts = []
    source_files = []
    for node in nodes:
        context_parts.append(node.get_content())
        src = node.metadata.get("file_path") or node.metadata.get("source_label", "unknown")
        if src not in source_files:
            source_files.append(src)

    context = "\n\n---\n\n".join(context_parts)
    logger.info("Retrieved %d chunk(s) from sources: %s", len(nodes), source_files)

    # Generate via DDNA envelope
    result = generate(
        query=query,
        context=context,
        lane=lane,
        ollama_model=ollama_model,
        ollama_base_url=ollama_base_url,
    )

    # Patch source files from retrieval into structured_data
    if result.get("structured_data"):
        result["structured_data"]["source_files"] = source_files
        result["structured_data"]["lane"] = lane

    return result


# Example queries for validation (Step 4 gate — run all three)
VALIDATION_QUERIES = [
    {
        "query": "Show me the current open action items related to the T&L Recovery project and highlight the primary owner according to session logs.",
        "lane": "SC",
    },
    {
        "query": "What are the governance guidelines under Gov-OS for registering a new asset under the Untous Investors Journey?",
        "lane": "DCSE",
    },
    {
        "query": "Summarize the priority decisions made regarding the Claude CTO and Qwen CCO models during the last three CP sessions.",
        "lane": "DCSE",
    },
]


if __name__ == "__main__":
    SUPABASE_LOCAL_URL = os.environ.get(
        "SUPABASE_LOCAL_URL",
        "postgresql://postgres:postgres@localhost:54322/postgres"
    )

    print("\n=== DCSE RAG VALIDATION QUERIES ===\n")
    for i, vq in enumerate(VALIDATION_QUERIES, 1):
        print(f"Query {i} (lane={vq['lane']}):\n  {vq['query']}")
        result = retrieve_and_generate(
            query=vq["query"],
            lane=vq["lane"],
            supabase_connection_string=SUPABASE_LOCAL_URL,
        )
        print(f"  structured_data: {result.get('structured_data')}")
        print(f"  narrative_summary: {result.get('narrative_summary', '')[:200]}...")
        print()
