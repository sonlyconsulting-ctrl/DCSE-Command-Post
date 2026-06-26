"""
DCSE RAG Engine — Source Configuration
Doc: DCSE-CP/RAG/CONFIG/20260624-001
Status: CANDIDATE MATERIAL — DCS REVIEW REQUIRED

All approved RAG ingestion source paths per DIRECTORY_INDEX.md (2026-06-24).
PS-isolated paths are defined in EXCLUDED_PATHS — never ingest from these.
"""

import os

# Base root — all paths derive from here
DCSE_ROOT = r"C:\DS All Things\DCSE_Command_Center"

# Approved RAG ingestion sources (PS scan cleared)
APPROVED_SOURCES = [
    {
        "label": "SC_TSL",
        "display": "T&L Recovery Library",
        "path": os.path.join(DCSE_ROOT, "DCSE_CP_Project", "SC_TSL"),
        "lane": "SC",
        "file_types": [".md", ".txt", ".pdf", ".csv", ".json"],
    },
    {
        "label": "SC_CTJ",
        "display": "Client Journey Library",
        "path": os.path.join(DCSE_ROOT, "DCSE_CP_Project", "SC_CTJ"),
        "lane": "SC",
        "file_types": [".md", ".txt", ".pdf", ".csv", ".json"],
        # Caveat: CTJ_LEGAL_LITIGATION_EXCLUSION_MANIFEST.csv references PS-adjacent paths.
        # The manifest itself is safe to ingest. Do NOT follow or dereference listed paths.
        "exclude_path_dereference": True,
    },
    {
        "label": "SC_Gov-OS",
        "display": "Governance OS Library",
        "path": os.path.join(DCSE_ROOT, "DCSE_CP_Project", "SC_Gov-OS"),
        "lane": "DCSE",
        "file_types": [".md", ".txt", ".json", ".sql", ".csv"],
    },
    {
        "label": "CP_Session_Log",
        "display": "CP Session Log",
        "path": os.path.join(DCSE_ROOT, "DCSE_CP_Project", "Command Post", "docs", "CP_Session_Log.md"),
        "lane": "DCSE",
        "file_types": [".md"],
        "single_file": True,
    },
    {
        "label": "CP_Open_Items",
        "display": "CP Open Items",
        "path": os.path.join(DCSE_ROOT, "DCSE_CP_Project", "Command Post", "docs", "CP_Open_Items.md"),
        "lane": "DCSE",
        "file_types": [".md"],
        "single_file": True,
    },
    {
        "label": "DCSE_RAG_Prompts",
        "display": "CP Prompt Library",
        "path": os.path.join(DCSE_ROOT, "DCSE_RAG_Prompts_Ingest"),
        "lane": "DCSE",
        "file_types": [".md", ".txt", ".json"],
    },
]

# PS-isolated paths — hard stop, never ingest
EXCLUDED_PATHS = [
    os.path.join(DCSE_ROOT, "DCSE_PS_CP_Project"),
    r"C:\DS All Things\DS Litigation",
]

# File patterns to always exclude regardless of source
EXCLUDED_PATTERNS = [
    ".env",
    ".env.local",
    ".env.production",
    "node_modules",
    ".next",
    ".git",
]

# PS-indicator terms — if found in file content, halt ingestion of that file
PS_INDICATOR_TERMS = [
    "8:23CV489",
    "Seals v. DHHS",
    "Ballentine",
    "Case 8:23",
    "deposition prep",
    "court filing",
    "discovery items",
    "plaintiff training",
    "DART-PS",
    "PS firewall breach",
]
