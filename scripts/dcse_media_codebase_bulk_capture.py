#!/usr/bin/env python3
"""DCSE Bulk Media + Creative Codebase Capture Tool.

Provider-neutral, standard-library-only utility for AG/local executors.

Default behavior is READ-ONLY inventory:
- scan approved roots
- hash files
- classify domain + role
- deduplicate by SHA-256
- discover local references from HTML/CSS/JS/JSON/YAML/MD
- emit JSON + CSV manifests

Optional --stage copies selected working assets into:
  <stage_root>/assets/<domain>/<role>/

Safety:
- never deletes or mutates source files
- never overwrites a staged file with different content
- large files are manifest-only unless --include-large
- source/canonical authority is NOT inferred from file existence
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import mimetypes
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

SKIP_DIRS = {".git", "node_modules", ".next", ".turbo", "__pycache__", ".venv", "venv", "dist", "build"}
MEDIA_EXTS = {
    ".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg",
    ".mp4", ".webm", ".mov", ".m4v", ".ogg", ".mp3", ".wav", ".m4a",
    ".pdf"
}
CODE_EXTS = {".html", ".htm", ".css", ".js", ".jsx", ".ts", ".tsx", ".json", ".yaml", ".yml", ".md"}
DEFAULT_ROLE_MAP = {
    "video": {".mp4", ".webm", ".mov", ".m4v"},
    "audio": {".ogg", ".mp3", ".wav", ".m4a"},
    "docs": {".pdf"},
    "images": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"},
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip())
    return re.sub(r"-+", "-", value).strip("-") or "asset"


def iter_files(roots: List[Path]) -> Iterable[Tuple[Path, Path]]:
    for root in roots:
        if not root.exists():
            continue
        for current, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                yield root, Path(current) / name


def load_config(path: Path) -> Dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("config must be a JSON object")
    return data


def classify_domain(path: Path, rules: List[Dict[str, str]], default: str) -> str:
    text = str(path).lower()
    for rule in rules:
        pattern = str(rule.get("pattern", "")).strip()
        domain = str(rule.get("domain", "")).strip()
        if pattern and domain and re.search(pattern, text, flags=re.I):
            return slug(domain.lower())
    return slug(default.lower())


def classify_role(path: Path, keyword_rules: List[Dict[str, str]]) -> str:
    name = path.name.lower()
    for rule in keyword_rules:
        pattern = str(rule.get("pattern", "")).strip()
        role = str(rule.get("role", "")).strip()
        if pattern and role and re.search(pattern, name, flags=re.I):
            return slug(role.lower())
    ext = path.suffix.lower()
    for role, exts in DEFAULT_ROLE_MAP.items():
        if ext in exts:
            return role
    return "other"


def extract_refs(path: Path) -> List[str]:
    if path.suffix.lower() not in CODE_EXTS:
        return []
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    refs = set()
    patterns = [
        r'''(?:src|href|poster)\s*=\s*["']([^"'#?]+)["']''',
        r'''url\(\s*["']?([^)"']+)["']?\s*\)''',
        r'''["']([^"']+\.(?:png|jpe?g|webp|gif|svg|mp4|webm|mov|m4v|ogg|mp3|wav|m4a|pdf))["']''',
    ]
    for pattern in patterns:
        for value in re.findall(pattern, text, flags=re.I):
            if isinstance(value, tuple):
                value = next((v for v in value if v), "")
            value = str(value).strip()
            if value and not re.match(r"^(?:https?:|data:|mailto:|tel:)", value, flags=re.I):
                refs.add(value.replace("\\", "/"))
    return sorted(refs)


def safe_stage(source: Path, dest_dir: Path, digest: str) -> Tuple[Optional[Path], str]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / source.name
    if dest.exists():
        if sha256_file(dest) == digest:
            return dest, "ALREADY_STAGED_SAME_HASH"
        dest = dest_dir / f"{source.stem}-{digest[:10]}{source.suffix.lower()}"
        if dest.exists() and sha256_file(dest) == digest:
            return dest, "ALREADY_STAGED_HASH_SUFFIX"
    shutil.copy2(source, dest)
    return dest, "COPIED"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="JSON config path")
    ap.add_argument("--output", required=True, help="output directory for manifests")
    ap.add_argument("--stage-root", help="creative codebase root for optional asset staging")
    ap.add_argument("--stage", action="store_true", help="copy eligible assets into stage-root/assets")
    ap.add_argument("--include-large", action="store_true", help="allow copies above max_copy_bytes")
    args = ap.parse_args()

    cfg = load_config(Path(args.config))
    roots = [Path(p) for p in cfg.get("roots", [])]
    domain_rules = list(cfg.get("domain_rules", []))
    role_rules = list(cfg.get("role_rules", []))
    default_domain = str(cfg.get("default_domain", "unclassified"))
    include_exts = {str(x).lower() for x in cfg.get("include_exts", sorted(MEDIA_EXTS))}
    max_copy_bytes = int(cfg.get("max_copy_bytes", 25 * 1024 * 1024))

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    stage_root = Path(args.stage_root).resolve() if args.stage_root else None
    if args.stage and stage_root is None:
        raise SystemExit("--stage requires --stage-root")

    code_refs: Dict[str, List[str]] = defaultdict(list)
    for root, path in iter_files(roots):
        if path.suffix.lower() in CODE_EXTS:
            for ref in extract_refs(path):
                code_refs[Path(ref).name.lower()].append(str(path))

    records = []
    by_hash: Dict[str, List[str]] = defaultdict(list)
    errors = []

    for root, path in iter_files(roots):
        if path.suffix.lower() not in include_exts:
            continue
        try:
            digest = sha256_file(path)
            stat = path.stat()
            domain = classify_domain(path, domain_rules, default_domain)
            role = classify_role(path, role_rules)
            mime, _ = mimetypes.guess_type(path.name)
            consumed_by = sorted(set(code_refs.get(path.name.lower(), [])))
            stage_state = "NOT_REQUESTED"
            staged_path = None

            if args.stage:
                if stat.st_size > max_copy_bytes and not args.include_large:
                    stage_state = "SKIPPED_LARGE_MANIFEST_ONLY"
                else:
                    dest_dir = stage_root / "assets" / domain / role
                    staged, stage_state = safe_stage(path, dest_dir, digest)
                    staged_path = str(staged) if staged else None

            rec = {
                "source_root": str(root),
                "source_path": str(path),
                "filename": path.name,
                "sha256": digest,
                "bytes": stat.st_size,
                "mime_type": mime,
                "domain": domain,
                "role": role,
                "consumed_by_count": len(consumed_by),
                "consumed_by": consumed_by,
                "stage_state": stage_state,
                "staged_path": staged_path,
                "canonical_status": "UNVERIFIED",
                "rights_status": "UNVERIFIED",
                "release_status": "UNVERIFIED",
            }
            records.append(rec)
            by_hash[digest].append(str(path))
        except Exception as exc:
            errors.append({"path": str(path), "error": f"{type(exc).__name__}: {exc}"})

    duplicate_groups = [
        {"sha256": digest, "paths": paths}
        for digest, paths in by_hash.items() if len(paths) > 1
    ]

    manifest = {
        "schema_version": "1.0",
        "tool": "dcse_media_codebase_bulk_capture.py",
        "mode": "STAGE" if args.stage else "INVENTORY",
        "source_mutation": False,
        "roots": [str(p) for p in roots],
        "asset_count": len(records),
        "unique_hash_count": len(by_hash),
        "duplicate_group_count": len(duplicate_groups),
        "consumed_asset_count": sum(1 for r in records if r["consumed_by_count"]),
        "errors": errors,
        "assets": records,
        "duplicate_groups": duplicate_groups,
    }

    json_path = out_dir / "DCSE_MEDIA_CAPTURE_MANIFEST.json"
    json_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    csv_path = out_dir / "DCSE_MEDIA_CAPTURE_MANIFEST.csv"
    fields = [
        "source_path", "filename", "sha256", "bytes", "mime_type",
        "domain", "role", "consumed_by_count", "stage_state", "staged_path",
        "canonical_status", "rights_status", "release_status",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for rec in records:
            writer.writerow({k: rec.get(k) for k in fields})

    summary = {
        "asset_count": len(records),
        "unique_hash_count": len(by_hash),
        "duplicate_group_count": len(duplicate_groups),
        "consumed_asset_count": manifest["consumed_asset_count"],
        "error_count": len(errors),
        "json_manifest": str(json_path),
        "csv_manifest": str(csv_path),
        "staged": bool(args.stage),
    }
    print(json.dumps(summary, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
