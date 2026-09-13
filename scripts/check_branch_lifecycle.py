#!/usr/bin/env python3
"""Fail CI when a PR attempts to reuse a superseded branch."""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / ".github" / "superseded-branches.txt"


def main() -> int:
    branch = (os.getenv("GITHUB_HEAD_REF") or os.getenv("GITHUB_REF_NAME") or "").strip()
    blocked = {
        line.strip()
        for line in REGISTRY.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if branch in blocked:
        print(f"[BRANCH LIFECYCLE FAILED] {branch} is superseded and read-only.")
        return 1
    print(f"[BRANCH LIFECYCLE PASSED] {branch or 'unknown/local'} is not superseded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
