#!/usr/bin/env python3
"""
DCSE Shared Action Protocol & Acceptance Criteria Automated Enforcement Check.
Validates:
1. No prohibited punctuation (em dashes, en dashes) in public or implementation markdown.
2. No unauthorized absolute outcome promises ('guarantees', 'guaranteeing' in substantive content).
3. Lifecycle state consistency: CANDIDATE docs must not claim CANONICAL or ACTIVE_RATIFIED authority.
4. Receipts must contain complete Shared Action Contract metadata fields.
5. Specialized legal frameworks (e.g. McDonnell Douglas) must not leak into universal/commercial implementations.
"""
from __future__ import annotations
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PROHIBITED_CHARS = ["\u2014", "\u2013"] # em dash, en dash
REQUIRED_CONTRACT_FIELDS = [
    "Task ID",
    "Authority source",
    "Artifact lifecycle state",
    "Authorized next actions",
    "Reserved actions",
    "Applicable DART route",
    "Acceptance criteria",
    "Handoff ID"
]

def check_file(path: Path) -> list[str]:
    errors = []
    text = path.read_text(encoding="utf-8")
    rel_path = path.relative_to(ROOT)
    is_receipt_or_meta = "RECEIPT" in path.name.upper() or "CHECKLIST" in path.name.upper() or "SPEC" in path.name.upper()

    # 1. Prohibited punctuation
    for line_no, line in enumerate(text.splitlines(), start=1):
        for char in PROHIBITED_CHARS:
            if char in line:
                char_name = "em dash" if char == "\u2014" else "en dash"
                errors.append(f"{rel_path}:{line_no} Prohibited punctuation detected ({char_name}).")

    # 2. Check for unauthorized absolute outcome claims in substantive content
    if not is_receipt_or_meta:
        for line_no, line in enumerate(text.splitlines(), start=1):
            if re.search(r'\b(guarantees|guaranteeing)\b', line, re.IGNORECASE):
                errors.append(f"{rel_path}:{line_no} Unsupported outcome guarantee detected: '{line.strip()}'.")

    # 3. Check lifecycle consistency for CANDIDATE documents
    if "Status:** CANDIDATE" in text or "state:** CANDIDATE" in text or "Status: CANDIDATE" in text:
        if re.search(r'Status:\*\*\s*(CANONICAL|Active Governance|ACTIVE_RATIFIED)', text):
            errors.append(f"{rel_path} Lifecycle contradiction: declared CANDIDATE but contains active canonical status.")

    # 4. Check for specialized legal frameworks leaking into commercial/universal implementations
    if "implementations" in str(rel_path) and "ps" not in str(rel_path).lower() and not is_receipt_or_meta:
        if "McDonnell Douglas" in text:
            errors.append(f"{rel_path} Specialized legal framework (McDonnell Douglas) leaked into commercial/universal implementation.")

    # 5. Check receipts for contract fields
    if "RECEIPT" in path.name.upper():
        for field in REQUIRED_CONTRACT_FIELDS:
            if field.lower() not in text.lower():
                errors.append(f"{rel_path} Missing mandatory Shared Action Contract field: '{field}'.")

    return errors


def main() -> int:
    target_files = sys.argv[1:]
    if not target_files:
        # Default scan on governance implementations and rule-foundry
        paths = list((ROOT / "governance" / "v7.2" / "implementations").glob("*.md"))
        paths.extend((ROOT / "governance" / "v7.2" / "rule-foundry").glob("*.md"))
    else:
        paths = [Path(f).resolve() for f in target_files]

    total_errors = []
    checked_count = 0
    for p in paths:
        if p.is_file() and p.suffix == ".md":
            checked_count += 1
            errs = check_file(p)
            if errs:
                total_errors.extend(errs)

    print(f"[DCSE PROTOCOL CHECK] Inspected {checked_count} file(s).")
    if total_errors:
        print(f"[DCSE PROTOCOL CHECK FAILED] Found {len(total_errors)} violation(s):")
        for e in total_errors:
            print(f"  - {e}")
        return 1

    print("[DCSE PROTOCOL CHECK PASSED] All acceptance rules and contract fields satisfied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
