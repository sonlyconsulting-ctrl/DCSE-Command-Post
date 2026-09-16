#!/usr/bin/env python3
"""DCSE Creative Orchestration Cycle.

Provider-neutral executable wrapper for design/media/creative work.

Purpose:
- enforce a minimum Product Start Gate before creative execution;
- preserve an approved/current baseline for MODIFY work;
- assemble a bounded context/codebase handoff;
- validate returned browser-renderable work deterministically;
- emit evidence and DDNA/RAG seed records without self-promoting output.

This script does not make reserved DCS decisions and does not publish.
It is designed to call, or be called by, provider-specific adapters later
(Claude Design MCP/CLI, image/video generators, other creative workers).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

REQUIRED_CONTEXT = (
    "_dcse_context/START_HERE.md",
    "_dcse_context/DCSE_PRODUCT_START_DECLARATION.yaml",
    "_dcse_context/CD_CORRECTION_ORDER.md",
    "_dcse_context/PRESERVE_CHANGE_MATRIX.yaml",
    "_dcse_context/QA_ACCEPTANCE_CRITERIA.md",
)

DEFAULT_LEAK_PATTERNS = (
    r"\bD10\b",
    r"\bTask ID\b",
    r"\bDCS-E Certified\b",
    r"\bissue\s*#\d+\b",
)

MEDIA_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".mp4", ".webm", ".ogg", ".mp3", ".wav"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def iter_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and ".git" not in path.parts:
            yield path


def build_manifest(root: Path) -> Dict[str, object]:
    files = []
    for path in iter_files(root):
        rel = path.relative_to(root).as_posix()
        files.append({
            "path": rel,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
            "media": path.suffix.lower() in MEDIA_EXTS,
        })
    return {
        "root": str(root),
        "file_count": len(files),
        "media_count": sum(1 for item in files if item["media"]),
        "files": files,
    }


def preflight(root: Path) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    for rel in REQUIRED_CONTEXT:
        if not (root / rel).is_file():
            failures.append(f"missing_context:{rel}")

    htmls = list(root.glob("*.html"))
    if not htmls:
        failures.append("missing_browser_artifact:root_html")
    if not (root / "assets").exists() and not (root / "uploads").exists():
        failures.append("missing_asset_surface:assets_or_uploads")

    declaration = root / "_dcse_context/DCSE_PRODUCT_START_DECLARATION.yaml"
    if declaration.is_file():
        text = declaration.read_text(encoding="utf-8", errors="ignore").lower()
        required_terms = ("mode", "destination", "url", "baseline", "acceptance")
        for term in required_terms:
            if term not in text:
                failures.append(f"start_declaration_missing_term:{term}")

    return (not failures, failures)


def extract_refs(html_text: str) -> List[str]:
    refs = re.findall(r'(?:src|href)=[\"\']([^\"\']+)[\"\']', html_text, flags=re.I)
    return [r for r in refs if not re.match(r"^(?:https?:|data:|mailto:|tel:|#)", r)]


def validate_html(root: Path, html_path: Path, expected_sections: int = 18) -> Dict[str, object]:
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    refs = extract_refs(text)
    missing_refs = []
    for ref in refs:
        clean = ref.split("?", 1)[0].split("#", 1)[0]
        if clean and not (html_path.parent / clean).exists():
            missing_refs.append(ref)

    leaks = []
    for pattern in DEFAULT_LEAK_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            leaks.append(pattern)

    metrics = {
        "sections": len(re.findall(r"<section\b", text, flags=re.I)),
        "image_slots": len(re.findall(r"<image-slot\b", text, flags=re.I)),
        "img_tags": len(re.findall(r"<img\b", text, flags=re.I)),
        "video_tags": len(re.findall(r"<video\b", text, flags=re.I)),
        "audio_tags": len(re.findall(r"<audio\b", text, flags=re.I)),
        "inputs": len(re.findall(r"<input\b", text, flags=re.I)),
        "buttons": len(re.findall(r"<button\b", text, flags=re.I)),
        "onclick": len(re.findall(r"onClick\s*=", text)),
        "onchange": len(re.findall(r"onChange\s*=", text)),
        "ontimeupdate": len(re.findall(r"onTimeUpdate\s*=", text)),
        "em_dash_count": text.count("—"),
        "en_dash_count": text.count("–"),
        "dead_hash_links": len(re.findall(r'href=[\"\']#[\"\']', text, flags=re.I)),
    }

    failures = []
    if metrics["sections"] != expected_sections:
        failures.append(f"section_count:{metrics['sections']}!=expected:{expected_sections}")
    if metrics["em_dash_count"] or metrics["en_dash_count"]:
        failures.append("d08_dash_violation")
    if metrics["dead_hash_links"]:
        failures.append("dead_hash_links")
    if missing_refs:
        failures.append("missing_local_references")
    if leaks:
        failures.append("internal_surface_leak_pattern")

    return {
        "artifact": html_path.relative_to(root).as_posix(),
        "artifact_sha256": sha256_file(html_path),
        "metrics": metrics,
        "missing_refs": sorted(set(missing_refs)),
        "leak_patterns_found": leaks,
        "pass": not failures,
        "failures": failures,
    }


def ddna_seed(root: Path, manifest: Dict[str, object], validation: Dict[str, object]) -> Dict[str, object]:
    return {
        "record_type": "creative_orchestration_evidence",
        "source_title": "DCSE Creative Orchestration Cycle Evidence",
        "source_path": str(root),
        "authority_status": "observed_evidence_not_authority",
        "sensitivity": "internal",
        "harvest_eligibility": "eligible",
        "metadata": {
            "file_count": manifest["file_count"],
            "media_count": manifest["media_count"],
            "validation_pass": validation["pass"],
            "artifact_sha256": validation["artifact_sha256"],
            "purpose": "RAG/DDNA source seed; does not create promotion authority",
        },
    }


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def cmd_prepare(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ok, failures = preflight(root)
    manifest = build_manifest(root)
    out = root / ".dcse_run"
    write_json(out / "creative_cycle_manifest.json", manifest)
    write_json(out / "preflight.json", {"pass": ok, "failures": failures})
    print(json.dumps({"pass": ok, "failures": failures, "manifest": str(out / "creative_cycle_manifest.json")}, indent=2))
    return 0 if ok else 2


def cmd_validate(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    html = root / args.html
    if not html.is_file():
        print(json.dumps({"pass": False, "failures": ["html_not_found"], "path": str(html)}, indent=2))
        return 2
    result = validate_html(root, html, expected_sections=args.sections)
    write_json(root / ".dcse_run/validation.json", result)
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


def cmd_closeout(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    ok, failures = preflight(root)
    manifest = build_manifest(root)
    html = root / args.html
    validation = validate_html(root, html, expected_sections=args.sections) if html.is_file() else {
        "pass": False, "failures": ["html_not_found"], "artifact_sha256": None
    }
    record = {
        "preflight": {"pass": ok, "failures": failures},
        "manifest": manifest,
        "validation": validation,
        "status": "TECHNICALLY_COMPLETE" if validation.get("pass") else "PARTIAL",
        "promotion_state": "NOT_PROMOTED",
    }
    out = root / ".dcse_run"
    write_json(out / "completion_evidence.json", record)
    write_json(out / "ddna_source_seed.json", ddna_seed(root, manifest, validation))
    print(json.dumps({
        "status": record["status"],
        "promotion_state": "NOT_PROMOTED",
        "evidence": str(out / "completion_evidence.json"),
        "ddna_seed": str(out / "ddna_source_seed.json"),
    }, indent=2))
    return 0 if validation.get("pass") and ok else 1


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="DCSE provider-neutral creative orchestration cycle")
    sub = ap.add_subparsers(dest="command", required=True)

    for name, fn in (("prepare", cmd_prepare), ("validate", cmd_validate), ("closeout", cmd_closeout)):
        p = sub.add_parser(name)
        p.add_argument("--root", required=True, help="creative codebase/context root")
        p.add_argument("--html", default="Persona Essence Atlas.dc.html")
        p.add_argument("--sections", type=int, default=18)
        p.set_defaults(fn=fn)
    return ap


def main() -> int:
    args = build_parser().parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
