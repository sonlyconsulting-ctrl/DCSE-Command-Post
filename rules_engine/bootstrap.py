#!/usr/bin/env python3
"""DCSE Rules Engineering bootstrap.

PLACE IN DCSE
-------------
Canonical launcher for the OPERATIVE rules-engine package stored in this
repository. It materializes the exact promoted archive and optionally executes
the regression suite.

This bootstrap is intentionally small. The actual rule files, comments,
metadata, registry, tests, and blueprint are preserved inside the promoted
archive. Extraction does not alter the archive.
"""
from __future__ import annotations
import argparse
import subprocess
import sys
import tarfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCHIVE = HERE / "DCSE_Rules_Engineering_Operative_v0_2.tar.gz"
RUNTIME = HERE / "runtime"
ROOT = RUNTIME / "DCSE_Rules_Engineering_Operative_v0_2"

def materialize() -> Path:
    if not ARCHIVE.exists():
        raise SystemExit(f"Missing promoted archive: {ARCHIVE}")
    RUNTIME.mkdir(parents=True, exist_ok=True)
    if not ROOT.exists():
        with tarfile.open(ARCHIVE, "r:gz") as tf:
            tf.extractall(RUNTIME)
    return ROOT

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--test", action="store_true", help="run packaged regression tests")
    args = ap.parse_args()
    root = materialize()
    print(root)
    if args.test:
        return subprocess.call(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=root,
        )
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
