#!/usr/bin/env python3
"""Validate the DCSE v7.1 doctrine candidate corpus without external packages."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


SOURCE_RE = re.compile(r"\*\*Source doctrine:\*\* `([^`]+)`")
SOURCE_HASH_RE = re.compile(r"\*\*Source SHA-256:\*\* `([0-9a-f]{64})`")
TEST_RE = re.compile(r"\| (D\d{2}-\d{3}) \|")
DOC_RE = re.compile(r"DCSE-D(\d{2})-v7\.1-RC3-CANDIDATE")
LOCAL_PATH_RE = re.compile(r"file:///|[A-Za-z]:\\")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME)\b")


@dataclass
class Result:
    path: str
    doctrine_id: str | None
    sha256: str
    source_path: str | None
    source_hash_expected: str | None
    source_hash_actual: str | None
    test_ids: list[str]
    errors: list[str]
    warnings: list[str]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_candidate(repo: Path, path: Path) -> Result:
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    doc_match = DOC_RE.search(text)
    doctrine_id = f"D{doc_match.group(1)}" if doc_match else None
    source_match = SOURCE_RE.search(text)
    source_hash_match = SOURCE_HASH_RE.search(text)
    source_path = source_match.group(1) if source_match else None
    expected = source_hash_match.group(1) if source_hash_match else None
    actual = None

    if any(byte > 127 for byte in raw):
        errors.append("NON_ASCII_CONTENT")
    if text.count("```") % 2:
        errors.append("UNBALANCED_CODE_FENCES")
    if LOCAL_PATH_RE.search(text):
        errors.append("LOCAL_PATH_DEPENDENCY")
    if PLACEHOLDER_RE.search(text):
        errors.append("UNRESOLVED_PLACEHOLDER")
    if "**Promotion effect:**" not in text:
        errors.append("MISSING_PROMOTION_EFFECT")
    if "## " not in text:
        errors.append("MISSING_SECTIONS")

    if source_path:
        source = repo / source_path
        if not source.exists():
            errors.append("SOURCE_NOT_FOUND")
        else:
            actual = digest(source)
            if expected != actual:
                errors.append("SOURCE_HASH_MISMATCH")
    else:
        warnings.append("NO_SOURCE_DOCTRINE_FIELD")

    tests = TEST_RE.findall(text)
    if doctrine_id and not tests:
        errors.append("NO_MECHANICAL_TESTS")
    if len(tests) != len(set(tests)):
        errors.append("DUPLICATE_TEST_ID_IN_FILE")

    if doctrine_id == "D17":
        retired = re.compile(
            r"\b(?:discovery|attack|rebuttal|trial|litigation|case law|court|pro se|ps[- /])\b",
            re.IGNORECASE,
        )
        if retired.search(text):
            errors.append("D17_RETIRED_VOCABULARY")

    return Result(
        path=str(path.relative_to(repo)),
        doctrine_id=doctrine_id,
        sha256=digest(path),
        source_path=source_path,
        source_hash_expected=expected,
        source_hash_actual=actual,
        test_ids=tests,
        errors=errors,
        warnings=warnings,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    candidate_root = repo / "governance/v7.1/candidates/20260803_doctrine_executability"
    candidates = sorted(candidate_root.glob("D*_v7.1_RC3_CANDIDATE.md"))
    results = [validate_candidate(repo, path) for path in candidates]

    all_tests: dict[str, str] = {}
    duplicate_global: list[str] = []
    for result in results:
        for test_id in result.test_ids:
            if test_id in all_tests:
                duplicate_global.append(test_id)
            all_tests[test_id] = result.path

    processed = sorted({r.doctrine_id for r in results if r.doctrine_id})
    expected = [f"D{i:02d}" for i in range(1, 23)]
    missing = [item for item in expected if item not in processed]
    candidate_validation_pass = (
        not duplicate_global and all(not r.errors for r in results)
    )
    corpus_complete = not missing
    final_pass = candidate_validation_pass and corpus_complete
    report = {
        "schema_version": "1.0",
        "candidate_count": len(results),
        "processed_doctrines": processed,
        "missing_doctrines": missing,
        "duplicate_global_test_ids": duplicate_global,
        "candidate_validation_pass": candidate_validation_pass,
        "corpus_complete": corpus_complete,
        "final_pass": final_pass,
        "results": [asdict(r) for r in results],
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["final_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
