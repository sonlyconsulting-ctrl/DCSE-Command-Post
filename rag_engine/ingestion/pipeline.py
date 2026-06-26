"""
DCSE RAG Engine — Ingestion Pipeline
Doc: DCSE-CP/RAG/INGEST/20260624-001
Status: CANDIDATE MATERIAL — DCS REVIEW REQUIRED

Stack:
  Embeddings  : sentence-transformers (BAAI/bge-small-en-v1.5) — local, no API key
  Chunking    : LlamaIndex SimpleDirectoryReader + SentenceSplitter
  Vector Store: Supabase local Docker + pgvector
  Lane tag    : per-source lane metadata applied to every chunk

Exclusions enforced:
  - PS firewall preflight (ps_firewall.py) — halts on any PS hit
  - EXCLUDED_PATTERNS from sources.py
  - DS Litigation path — hard stop

Run this script only after local Supabase Docker is confirmed operational
and pgvector extension is enabled.
"""

import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("dcse.rag.ingestion")

# Add rag_engine root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from config.sources import APPROVED_SOURCES, EXCLUDED_PATTERNS
from ingestion.ps_firewall import run_preflight


def load_documents(source: dict) -> list:
    """Load documents from a source using LlamaIndex."""
    try:
        from llama_index.core import SimpleDirectoryReader
    except ImportError:
        logger.error("llama_index not installed. Run: pip install llama-index")
        return []

    source_path = source["path"]
    file_types = source.get("file_types", [".md", ".txt"])

    if source.get("single_file"):
        if not os.path.isfile(source_path):
            logger.warning("Single-file source not found: %s", source_path)
            return []
        try:
            reader = SimpleDirectoryReader(input_files=[source_path])
            docs = reader.load_data()
        except Exception as e:
            logger.error("Failed to load single file %s: %s", source_path, e)
            return []
    else:
        if not os.path.isdir(source_path):
            logger.warning("Source directory not found: %s", source_path)
            return []

        # Build exclude list
        exclude_dirs = [p for p in EXCLUDED_PATTERNS]

        try:
            reader = SimpleDirectoryReader(
                input_dir=source_path,
                required_exts=file_types,
                recursive=True,
                exclude_hidden=True,
                # LlamaIndex exclude_dirs filters directory names
                exclude=exclude_dirs,
            )
            docs = reader.load_data()
        except Exception as e:
            logger.error("Failed to load source %s: %s", source["label"], e)
            return []

    # Attach lane and source metadata to every document
    for doc in docs:
        doc.metadata["lane"] = source["lane"]
        doc.metadata["source_label"] = source["label"]
        doc.metadata["source_display"] = source["display"]

    logger.info("Loaded %d document(s) from %s", len(docs), source["label"])
    return docs


def chunk_documents(docs: list) -> list:
    """Split documents into chunks using LlamaIndex SentenceSplitter."""
    if not docs:
        return []

    try:
        from llama_index.core.node_parser import SentenceSplitter
    except ImportError:
        logger.error("llama_index node_parser not available.")
        return []

    splitter = SentenceSplitter(chunk_size=512, chunk_overlap=64)
    nodes = splitter.get_nodes_from_documents(docs)
    logger.info("Chunked into %d node(s)", len(nodes))
    return nodes


def embed_and_store(nodes: list, supabase_url: str, supabase_key: str) -> int:
    """
    Embed nodes using local sentence-transformers and store in Supabase pgvector.
    Returns count of vectors stored.

    supabase_url: local Docker URL, e.g. http://localhost:54321
    supabase_key: anon key for local Docker instance (not service role — read-only ingestion)
    """
    if not nodes:
        logger.warning("No nodes to embed.")
        return 0

    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        from llama_index.vector_stores.supabase import SupabaseVectorStore
        from llama_index.core import VectorStoreIndex, StorageContext
    except ImportError as e:
        logger.error("Missing dependency: %s. See requirements.txt.", e)
        return 0

    logger.info("Loading local embedding model: BAAI/bge-small-en-v1.5")
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    logger.info("Connecting to Supabase vector store at %s", supabase_url)
    try:
        vector_store = SupabaseVectorStore(
            postgres_connection_string=supabase_url,
            collection_name="dcse_rag_vectors",
            dimension=384,  # BAAI/bge-small-en-v1.5 — do not change without re-ingesting all vectors
        )
    except Exception as e:
        logger.error("Failed to connect to Supabase vector store: %s", e)
        return 0

    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    logger.info("Building vector index from %d node(s)...", len(nodes))
    try:
        VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=embed_model,
            show_progress=True,
        )
    except Exception as e:
        logger.error("Failed to build vector index: %s", e)
        return 0

    logger.info("Stored %d vector(s) in Supabase pgvector.", len(nodes))
    return len(nodes)


def run_ingestion(supabase_url: str, supabase_key: str) -> dict:
    """
    Full ingestion run:
    1. PS firewall preflight — halt if any PS content found
    2. Load documents from all approved sources
    3. Chunk documents
    4. Embed and store in Supabase pgvector

    Returns a summary report dict.
    """
    report = {
        "ps_clear": False,
        "sources_loaded": 0,
        "total_documents": 0,
        "total_chunks": 0,
        "vectors_stored": 0,
        "ps_halted_files": [],
        "errors": [],
    }

    # Step 1: PS firewall preflight
    logger.info("Running PS firewall preflight across all approved sources...")
    all_clear, scan_results = run_preflight(APPROVED_SOURCES)

    halted = [r for r in scan_results if r["action"] == "HALTED"]
    report["ps_halted_files"] = [r["file_path"] for r in halted]

    if not all_clear:
        logger.error(
            "PS FIREWALL HALT — ingestion blocked. %d file(s) flagged: %s",
            len(halted),
            report["ps_halted_files"],
        )
        return report

    report["ps_clear"] = True
    logger.info("PS firewall: CLEAR. Proceeding to document load.")

    # Step 2: Load and chunk all sources
    all_nodes = []
    for source in APPROVED_SOURCES:
        docs = load_documents(source)
        if docs:
            report["total_documents"] += len(docs)
            report["sources_loaded"] += 1
            nodes = chunk_documents(docs)
            all_nodes.extend(nodes)

    report["total_chunks"] = len(all_nodes)
    logger.info(
        "Load complete: %d source(s), %d document(s), %d chunk(s)",
        report["sources_loaded"],
        report["total_documents"],
        report["total_chunks"],
    )

    # Step 3: Embed and store
    stored = embed_and_store(all_nodes, supabase_url, supabase_key)
    report["vectors_stored"] = stored

    logger.info("Ingestion complete. Report: %s", report)
    return report


if __name__ == "__main__":
    # Local Supabase Docker defaults
    # Replace with actual local connection string from Supabase Docker output
    # Never hardcode service role key — use anon key for ingestion reads
    SUPABASE_LOCAL_URL = os.environ.get(
        "SUPABASE_LOCAL_URL",
        "postgresql://postgres:postgres@localhost:54322/postgres"
    )
    SUPABASE_LOCAL_KEY = os.environ.get("SUPABASE_LOCAL_ANON_KEY", "")

    if not SUPABASE_LOCAL_KEY:
        logger.error(
            "SUPABASE_LOCAL_ANON_KEY not set. "
            "Export it before running: export SUPABASE_LOCAL_ANON_KEY=your_anon_key"
        )
        sys.exit(1)

    result = run_ingestion(SUPABASE_LOCAL_URL, SUPABASE_LOCAL_KEY)

    print("\n=== DCSE RAG INGESTION REPORT ===")
    for k, v in result.items():
        print(f"  {k}: {v}")
