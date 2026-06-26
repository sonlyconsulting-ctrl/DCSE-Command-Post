"""
DCSE RAG Engine — PS Firewall
Doc: DCSE-CP/RAG/FIREWALL/20260624-001
Status: CANDIDATE MATERIAL — DCS REVIEW REQUIRED

Runs before any file is chunked or embedded.
A PS hit on any file halts ingestion of that file and logs the event.
Never modifies source files. Read-only pass.
"""

import os
import logging
from pathlib import Path
from config.sources import PS_INDICATOR_TERMS, EXCLUDED_PATHS

logger = logging.getLogger("dcse.rag.firewall")


def is_excluded_path(file_path: str) -> bool:
    """Return True if file_path falls under a PS-isolated root."""
    resolved = str(Path(file_path).resolve())
    for excluded in EXCLUDED_PATHS:
        if resolved.startswith(str(Path(excluded).resolve())):
            return True
    return False


def scan_file_for_ps_content(file_path: str) -> dict:
    """
    Read file and scan for PS-indicator terms.
    Returns a result dict:
      {
        "safe": bool,
        "file_path": str,
        "hits": list[str],   # terms found
        "action": str        # "APPROVED" | "HALTED"
      }
    """
    result = {
        "safe": True,
        "file_path": file_path,
        "hits": [],
        "action": "APPROVED",
    }

    if is_excluded_path(file_path):
        result["safe"] = False
        result["hits"] = ["PATH_IN_EXCLUDED_ROOT"]
        result["action"] = "HALTED"
        logger.error(
            "PS FIREWALL HALT — file is under a PS-isolated path: %s", file_path
        )
        return result

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except (OSError, IOError) as e:
        logger.warning("Could not read file %s: %s", file_path, e)
        result["action"] = "SKIPPED"
        return result

    for term in PS_INDICATOR_TERMS:
        if term.lower() in content.lower():
            result["hits"].append(term)

    if result["hits"]:
        result["safe"] = False
        result["action"] = "HALTED"
        logger.error(
            "PS FIREWALL HALT — PS-indicator terms found in %s: %s",
            file_path,
            result["hits"],
        )

    return result


def scan_source(source: dict) -> list[dict]:
    """
    Run PS firewall scan across all files in a source definition.
    Returns list of per-file scan results.
    """
    results = []
    source_path = source["path"]

    if source.get("single_file"):
        if os.path.isfile(source_path):
            results.append(scan_file_for_ps_content(source_path))
        return results

    for root, dirs, files in os.walk(source_path):
        # Skip excluded directory patterns
        dirs[:] = [
            d for d in dirs
            if not any(pat in d for pat in [".git", "node_modules", ".next"])
        ]
        for filename in files:
            file_path = os.path.join(root, filename)
            results.append(scan_file_for_ps_content(file_path))

    return results


def run_preflight(sources: list[dict]) -> tuple[bool, list[dict]]:
    """
    Run PS firewall preflight across all approved sources.
    Returns (all_clear: bool, all_results: list[dict]).
    If any file is HALTED, all_clear is False.
    Ingestion pipeline must not proceed until all_clear is True.
    """
    all_results = []
    halt_count = 0

    for source in sources:
        logger.info("PS firewall scanning: %s", source["label"])
        results = scan_source(source)
        all_results.extend(results)
        halted = [r for r in results if r["action"] == "HALTED"]
        if halted:
            halt_count += len(halted)
            logger.error(
                "HALT: %d PS-flagged file(s) in source %s",
                len(halted),
                source["label"],
            )

    all_clear = halt_count == 0
    if all_clear:
        logger.info("PS firewall preflight: CLEAR. %d files scanned.", len(all_results))
    else:
        logger.error(
            "PS firewall preflight: HALT. %d file(s) flagged. Ingestion blocked.",
            halt_count,
        )

    return all_clear, all_results
