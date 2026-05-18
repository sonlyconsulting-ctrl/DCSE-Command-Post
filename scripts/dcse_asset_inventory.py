"""
DCSE Asset Inventory Scanner
Asset: DCSE-ASSET-INVENTORY-SCANNER-001
Version: v1
Date: 2026-05-18
Doctrine: Structure Precedes Scale — DBA Stop-Gate Active

Walks a DCSE working directory tree, classifies every file using the
5-layer DDNA signal model and EOD asset cross-reference rules, and
produces a Markdown report and CSV inventory for DCS review.

Usage:
    python dcse_asset_inventory.py <root_path> [--eod-manifest <path>] [--out <reports_dir>]

Defaults:
    --eod-manifest  looks for dcse_eod_daily_asset_ddna_20260517.json in script dir
    --out           ./reports/
"""

import argparse
import csv
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

# ─── Constants ────────────────────────────────────────────────────────────────

SCAN_DATE = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
REPORT_DATE = datetime.now(timezone.utc).strftime("%Y%m%d")

IGNORE_PATTERNS = {".git", "__pycache__", "node_modules", ".next", ".venv", "venv"}
IGNORE_EXTENSIONS = {".tmp", ".log", ".pyc", ".DS_Store"}

# ─── Lane Rules (§3) ──────────────────────────────────────────────────────────

LANE_RULES = [
    (["\\ps\\", "/ps/", "\\ps_", "/ps_"],           "PS"),
    (["sc_home", "sc_about", "sonly", "\\sc\\", "/sc/", "sc_"], "SC"),
    (["sportsociety", "\\ss\\", "/ss/", "ss_"],      "SS"),
    (["dcs_resume", "dcs_hero", "\\emp\\", "/emp/", "\\employment\\", "/employment/", "emp_"], "EMP"),
    (["\\dcse\\", "/dcse/", "dcse_", "\\eod\\", "/eod/", "eod_", "ddna"], "DCSE"),
]

def infer_lane(path_str: str) -> str:
    p = path_str.replace("\\", "/").lower()
    matches = set()
    for patterns, lane in LANE_RULES:
        if any(pat.replace("\\", "/").lower() in p for pat in patterns):
            matches.add(lane)
    if len(matches) == 1:
        return matches.pop()
    if len(matches) > 1:
        return "CROSS"
    return "DCSE"

# ─── Lifecycle Stage Rules (§4) ───────────────────────────────────────────────

STAGE_KEYWORDS = {
    "Promoted":  ["pm_artifacts", "canonical", "committed_and_verified"],
    "Confirmed": ["reviews", "confirmed"],
    "Staged":    ["staging", "inbox", "plan_inbox"],
    "Archive":   ["archive"],
}

def infer_lifecycle(path_str: str, known_status: str | None) -> str:
    if known_status:
        if known_status.upper() in ("COMMITTED_AND_VERIFIED", "PROMOTED"):
            return "Promoted"
        if known_status.lower() == "pending_approval":
            return "Staged"
    p = path_str.replace("\\", "/").lower()
    for stage, keywords in STAGE_KEYWORDS.items():
        if any(kw in p for kw in keywords):
            return stage
    return "Captured"

# ─── Output Type Rules (§5) ───────────────────────────────────────────────────

OUTPUT_TYPE_MAP = {
    ".html": "HTML Module", ".htm": "HTML Module",
    ".sql":  "SQL Script",
    ".py":   "Python Script",
    ".md":   "Doctrine / Doc",
    ".json": "Manifest / Data",
    ".docx": "Word Document", ".doc": "Word Document",
    ".csv":  "Data / Report",
    ".pdf":  "PDF",
    ".txt":  "Text",
    ".png":  "Image / Design Asset", ".jpg": "Image / Design Asset",
    ".jpeg": "Image / Design Asset", ".svg": "Image / Design Asset",
    ".ico":  "Image / Design Asset",
    ".tsx":  "Frontend Code", ".ts": "Frontend Code", ".js": "Frontend Code",
    ".jsx":  "Frontend Code",
}

def infer_output_type(ext: str) -> str:
    return OUTPUT_TYPE_MAP.get(ext.lower(), "Binary / Unknown")

# ─── DDNA Layer Signal Rules (§6) ─────────────────────────────────────────────

LAYER_SIGNALS = {
    "Sentiment": ["sweep", "posture", "morale", "voice", "tone", "friction", "readiness"],
    "Logic":     ["workflow", "routing", "gate", "trigger", "lifecycle", "stage",
                  "doctrine", "rule", "decision", "audit"],
    "Design":    ["html", "css", "color", "typography", "layout", "playfair",
                  "amber", "obsidian", "tab", "nav", "icon", "badge"],
    "Product":   ["candidate", "template", "home", "about", "resume", "hero",
                  "glossary", "services", "guide", "prototype"],
    "Technical": ["rls", "policy", "migration", "service_role", "anon_key",
                  "supabase", "insert", "alter", "create", "cron", "ddna",
                  "extract", "registry"],
}
LAYER_EXT_MAP = {
    "Design":    {".html", ".htm", ".svg", ".css"},
    "Technical": {".sql", ".py"},
}

def infer_ddna_layers(filename: str, ext: str, content_head: str) -> list[str]:
    target = (filename + " " + content_head).lower()
    layers = []
    for layer, keywords in LAYER_SIGNALS.items():
        if any(kw in target for kw in keywords):
            layers.append(layer)
        elif layer in LAYER_EXT_MAP and ext.lower() in LAYER_EXT_MAP[layer]:
            if layer not in layers:
                layers.append(layer)
    return layers if layers else ["Unknown"]

# ─── Risk / Gate Flags (§7) ───────────────────────────────────────────────────

CREDENTIAL_PATTERNS = [
    "service_role_key", "anon_key", "supabase_url",
    "SUPABASE_URL", "SERVICE_ROLE_KEY", "ANON_KEY",
]

def compute_flags(
    path_str: str, ext: str, content_head: str, lane: str, pending: bool
) -> dict:
    flags = {
        "ps_risk_flag":            False,
        "dba_stop_gate_required":  False,
        "rls_unverified":          False,
        "credential_exposure_risk": False,
        "codebase_gate_active":    False,
        "pending_dcs_review":      pending,
    }
    p_lower = path_str.replace("\\", "/").lower()

    if lane == "PS" or "ps_risk" in p_lower:
        flags["ps_risk_flag"] = True

    if ext.lower() == ".sql":
        if "migrations" not in p_lower and "migration" not in p_lower:
            flags["dba_stop_gate_required"] = True
        if "enable row level security" not in content_head.lower():
            flags["rls_unverified"] = True
        if "supabase" in content_head.lower() or "migration" in content_head.lower():
            flags["codebase_gate_active"] = True

    if not path_str.lower().endswith((".env", ".env.local", ".env.example")):
        if any(pat in content_head for pat in CREDENTIAL_PATTERNS):
            flags["credential_exposure_risk"] = True

    return flags

# ─── EOD Manifest Loader (§8) ─────────────────────────────────────────────────

def load_eod_manifest(manifest_path: str | None) -> dict:
    """
    Returns dict keyed by normalized external_id → {title, status, group}
    Also builds a set of normalized filename fragments for fuzzy matching.
    """
    if not manifest_path or not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, encoding="utf-8") as f:
        data = json.load(f)
    lookup = {}
    assets_root = data.get("assets", {})
    reconciliation_status = data.get("reconciliation", {}).get("audit_status", "")
    for group_key, assets in assets_root.items():
        for asset in assets:
            eid = asset.get("external_id", "")
            lookup[eid] = {
                "title":  asset.get("title", ""),
                "status": asset.get("status", reconciliation_status),
                "group":  group_key,
            }
    return lookup

def match_manifest(filename: str, manifest: dict) -> tuple[str, str, str | None]:
    """Returns (known_external_id, known_asset_title, status) or ('', '', None)."""
    stem = Path(filename).stem.upper().replace("-", "_").replace(" ", "_")
    # Direct substring match against external_id
    for eid, info in manifest.items():
        eid_norm = eid.upper().replace("-", "_")
        if eid_norm in stem or stem in eid_norm:
            return eid, info["title"], info["status"]
    return "", "", None

# ─── File Content Reader ───────────────────────────────────────────────────────

def read_head(filepath: str, max_lines: int = 200) -> str:
    try:
        with open(filepath, encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)
        return "".join(lines)
    except (PermissionError, OSError):
        return ""

# ─── Scanner ─────────────────────────────────────────────────────────────────

def scan_directory(root: str, manifest: dict) -> list[dict]:
    records = []
    scan_id = str(uuid.uuid4())
    root_path = Path(root)

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune ignored directories in-place
        dirnames[:] = [
            d for d in dirnames
            if d not in IGNORE_PATTERNS and not d.startswith(".")
        ]

        for filename in sorted(filenames):
            ext = Path(filename).suffix
            if ext.lower() in IGNORE_EXTENSIONS or filename.startswith("."):
                continue

            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root)

            try:
                stat = os.stat(filepath)
                file_size = stat.st_size
                last_modified = datetime.fromtimestamp(
                    stat.st_mtime, tz=timezone.utc
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
            except OSError:
                file_size = 0
                last_modified = ""

            depth = len(Path(rel_path).parts) - 1
            folder = Path(dirpath).name

            lane = infer_lane(rel_path)

            # Skip content scan for PS lane (metadata only per rules §10)
            if lane == "PS":
                content_head = ""
            else:
                content_head = read_head(filepath)

            eid, etitle, estatus = match_manifest(filename, manifest)
            lifecycle = infer_lifecycle(rel_path, estatus)
            output_type = infer_output_type(ext)
            ddna_layers = infer_ddna_layers(filename, ext, content_head)
            flags = compute_flags(rel_path, ext, content_head, lane, estatus == "pending_approval")

            notes_parts = []
            if flags["credential_exposure_risk"]:
                notes_parts.append("CREDENTIAL EXPOSURE — review immediately")
            if flags["ps_risk_flag"] and flags["dba_stop_gate_required"]:
                notes_parts.append("PS lane + DBA gate — dual review required")
            if flags["rls_unverified"] and flags["dba_stop_gate_required"]:
                notes_parts.append("SQL outside migrations/ with no RLS — DBA review required")

            records.append({
                "scan_id":                 scan_id,
                "scan_date":               SCAN_DATE,
                "file_path":               rel_path,
                "folder":                  folder,
                "subfolder_depth":         depth,
                "filename":                filename,
                "extension":               ext.lower(),
                "file_size_bytes":         file_size,
                "last_modified":           last_modified,
                "output_type":             output_type,
                "lane":                    lane,
                "lifecycle_stage":         lifecycle,
                "ddna_layers":             " | ".join(ddna_layers),
                "known_external_id":       eid,
                "known_asset_title":       etitle,
                "ps_risk_flag":            flags["ps_risk_flag"],
                "dba_stop_gate_required":  flags["dba_stop_gate_required"],
                "rls_unverified":          flags["rls_unverified"],
                "credential_exposure_risk": flags["credential_exposure_risk"],
                "codebase_gate_active":    flags["codebase_gate_active"],
                "pending_dcs_review":      flags["pending_dcs_review"],
                "notes":                   "; ".join(notes_parts),
            })

    return records

# ─── Report Writers ───────────────────────────────────────────────────────────

FIELDS = [
    "scan_id", "scan_date", "file_path", "folder", "subfolder_depth",
    "filename", "extension", "file_size_bytes", "last_modified",
    "output_type", "lane", "lifecycle_stage", "ddna_layers",
    "known_external_id", "known_asset_title",
    "ps_risk_flag", "dba_stop_gate_required", "rls_unverified",
    "credential_exposure_risk", "codebase_gate_active", "pending_dcs_review",
    "notes",
]

def write_csv(records: list[dict], out_path: str):
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)
    print(f"CSV written → {out_path}")

def write_markdown(records: list[dict], root: str, out_path: str):
    total = len(records)

    # Summaries
    by_lane: dict[str, int] = {}
    by_stage: dict[str, int] = {}
    by_type: dict[str, int] = {}
    flags_summary = {
        "credential_exposure_risk": 0,
        "dba_stop_gate_required": 0,
        "rls_unverified": 0,
        "ps_risk_flag": 0,
        "pending_dcs_review": 0,
        "codebase_gate_active": 0,
    }
    credential_files = []
    known_matched = []
    pending_files = []

    for r in records:
        by_lane[r["lane"]] = by_lane.get(r["lane"], 0) + 1
        by_stage[r["lifecycle_stage"]] = by_stage.get(r["lifecycle_stage"], 0) + 1
        by_type[r["output_type"]] = by_type.get(r["output_type"], 0) + 1
        for flag in flags_summary:
            if r[flag]:
                flags_summary[flag] += 1
        if r["credential_exposure_risk"]:
            credential_files.append(r["file_path"])
        if r["known_external_id"]:
            known_matched.append(r)
        if r["pending_dcs_review"]:
            pending_files.append(r)

    # Group records by folder for the detail section
    by_folder: dict[str, list[dict]] = {}
    for r in records:
        folder_key = str(Path(r["file_path"]).parent)
        by_folder.setdefault(folder_key, []).append(r)

    lines = [
        f"# DCSE Asset Inventory Report",
        f"**Scan Date:** {SCAN_DATE}  ",
        f"**Root Path:** `{root}`  ",
        f"**Total Files Scanned:** {total}  ",
        f"**Scan ID:** `{records[0]['scan_id'] if records else 'N/A'}`  ",
        f"**Governed by:** DBA Stop-Gate Active — DCS approval required before any promotion",
        "",
        "---",
        "",
    ]

    # ── Credential Exposure (top of report per §10) ──
    if credential_files:
        lines += [
            "## ⚠ CREDENTIAL EXPOSURE — Immediate Review Required",
            "",
            "The following files contain credential strings outside `.env` files:",
            "",
        ]
        for fp in credential_files:
            lines.append(f"- `{fp}`")
        lines += ["", "**Action:** Rotate all referenced credentials before any external push.", "", "---", ""]

    # ── Executive Summary ──
    lines += [
        "## 1. Executive Summary",
        "",
        "### Files by Lane",
        "",
        "| Lane | Count |",
        "|---|---|",
    ]
    for lane, count in sorted(by_lane.items()):
        lines.append(f"| {lane} | {count} |")

    lines += [
        "",
        "### Files by Lifecycle Stage",
        "",
        "| Stage | Count |",
        "|---|---|",
    ]
    for stage, count in sorted(by_stage.items()):
        lines.append(f"| {stage} | {count} |")

    lines += [
        "",
        "### Files by Output Type",
        "",
        "| Type | Count |",
        "|---|---|",
    ]
    for otype, count in sorted(by_type.items(), key=lambda x: -x[1]):
        lines.append(f"| {otype} | {count} |")

    lines += [
        "",
        "### Risk and Gate Flags",
        "",
        "| Flag | Count |",
        "|---|---|",
    ]
    for flag, count in flags_summary.items():
        if count:
            lines.append(f"| {flag.replace('_', ' ').title()} | {count} |")

    lines += ["", "---", ""]

    # ── Known EOD Asset Cross-Reference ──
    lines += [
        "## 2. Known EOD Asset Cross-Reference",
        "",
        f"Files matched against EOD manifest: **{len(known_matched)}** of {total}",
        "",
        "| External ID | Known Title | File | Lane | Stage |",
        "|---|---|---|---|---|",
    ]
    for r in sorted(known_matched, key=lambda x: x["known_external_id"]):
        lines.append(
            f"| `{r['known_external_id']}` | {r['known_asset_title']} "
            f"| `{r['filename']}` | {r['lane']} | {r['lifecycle_stage']} |"
        )

    lines += ["", "---", ""]

    # ── Pending DCS Review ──
    lines += [
        "## 3. Pending DCS Review",
        "",
        f"**{len(pending_files)}** files carry `pending_approval` status from the EOD manifest.",
        "",
        "| File | Lane | Output Type | Known Title |",
        "|---|---|---|---|",
    ]
    for r in pending_files:
        lines.append(
            f"| `{r['filename']}` | {r['lane']} | {r['output_type']} | {r['known_asset_title']} |"
        )

    lines += ["", "---", ""]

    # ── Folder-by-Folder Detail ──
    lines += [
        "## 4. Folder-by-Folder Inventory",
        "",
    ]
    for folder_path in sorted(by_folder.keys()):
        folder_records = by_folder[folder_path]
        lines += [
            f"### `{folder_path or '(root)'}`",
            "",
            f"Files: {len(folder_records)}",
            "",
            "| Filename | Type | Lane | Stage | DDNA Layers | Flags |",
            "|---|---|---|---|---|---|",
        ]
        for r in sorted(folder_records, key=lambda x: x["filename"]):
            active_flags = [
                k.replace("_", " ") for k, v in {
                    "ps_risk":       r["ps_risk_flag"],
                    "dba gate":      r["dba_stop_gate_required"],
                    "rls?":          r["rls_unverified"],
                    "creds!":        r["credential_exposure_risk"],
                    "gate active":   r["codebase_gate_active"],
                    "pending":       r["pending_dcs_review"],
                }.items() if v
            ]
            flag_str = ", ".join(active_flags) if active_flags else "—"
            lines.append(
                f"| `{r['filename']}` | {r['output_type']} | {r['lane']} "
                f"| {r['lifecycle_stage']} | {r['ddna_layers']} | {flag_str} |"
            )
        lines.append("")

    lines += ["---", ""]

    # ── Open Items ──
    lines += [
        "## 5. Open Items for DCS",
        "",
        "Generated from active flags. Resolve before any promotion or push.",
        "",
    ]
    open_items = []
    if flags_summary["credential_exposure_risk"]:
        open_items.append(f"- [ ] Rotate credentials for {flags_summary['credential_exposure_risk']} flagged file(s)")
    if flags_summary["dba_stop_gate_required"]:
        open_items.append(f"- [ ] DBA review required for {flags_summary['dba_stop_gate_required']} SQL file(s) outside `migrations/`")
    if flags_summary["rls_unverified"]:
        open_items.append(f"- [ ] Verify or add RLS for {flags_summary['rls_unverified']} SQL file(s)")
    if flags_summary["ps_risk_flag"]:
        open_items.append(f"- [ ] DCS authorization required before extracting {flags_summary['ps_risk_flag']} PS-lane file(s)")
    if flags_summary["pending_dcs_review"]:
        open_items.append(f"- [ ] Manually review and approve/reject {flags_summary['pending_dcs_review']} pending asset(s) in staging console")
    if flags_summary["codebase_gate_active"]:
        open_items.append(f"- [ ] Resolve codebase gate (v0.2 Supabase migration blocked — see sweep 2026-05-16) for {flags_summary['codebase_gate_active']} file(s)")

    if open_items:
        lines.extend(open_items)
    else:
        lines.append("No open items. All flags clear.")

    lines += ["", "---", "", "*End of DCSE Asset Inventory Report*", ""]

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Report written → {out_path}")

# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="DCSE Asset Inventory Scanner — read-only directory walk"
    )
    parser.add_argument(
        "root",
        help="Root directory to scan (e.g. 'C:\\DS All Things\\dcse-sc-sportsociety')"
    )
    parser.add_argument(
        "--eod-manifest",
        default=None,
        help="Path to EOD asset manifest JSON. Defaults to dcse_eod_daily_asset_ddna_20260517.json beside this script."
    )
    parser.add_argument(
        "--out",
        default=None,
        help="Output directory for report and CSV. Defaults to ./reports/ beside this script."
    )
    args = parser.parse_args()

    root = args.root
    if not os.path.isdir(root):
        print(f"ERROR: Root path not found or not a directory: {root}")
        sys.exit(1)

    script_dir = Path(__file__).parent
    manifest_path = args.eod_manifest or str(
        script_dir.parent / "docs" / "audit" / "dcse_eod_daily_asset_ddna_20260517.json"
    )
    # Fallback: same directory as script
    if not os.path.exists(manifest_path):
        manifest_path = str(script_dir / "dcse_eod_daily_asset_ddna_20260517.json")

    out_dir = args.out or str(script_dir.parent / "reports")
    os.makedirs(out_dir, exist_ok=True)

    print(f"DCSE Asset Inventory Scanner v1")
    print(f"Root:     {root}")
    print(f"Manifest: {manifest_path}")
    print(f"Output:   {out_dir}")
    print(f"Scan ID:  (generated per run)")
    print()

    manifest = load_eod_manifest(manifest_path)
    print(f"EOD manifest loaded: {len(manifest)} known assets")

    print("Scanning directory tree...")
    records = scan_directory(root, manifest)
    print(f"Scan complete: {len(records)} files indexed")
    print()

    csv_path = os.path.join(out_dir, f"asset-inventory-{REPORT_DATE}.csv")
    md_path  = os.path.join(out_dir, f"asset-inventory-{REPORT_DATE}.md")

    write_csv(records, csv_path)
    write_markdown(records, root, md_path)

    # Summary to console
    print()
    print("─" * 60)
    print(f"Total files:          {len(records)}")
    cred_count = sum(1 for r in records if r["credential_exposure_risk"])
    pending_count = sum(1 for r in records if r["pending_dcs_review"])
    print(f"Credential flags:     {cred_count}")
    print(f"Pending DCS review:   {pending_count}")
    print("─" * 60)
    if cred_count:
        print("⚠  CREDENTIAL EXPOSURE FLAGS PRESENT — rotate before any push")

if __name__ == "__main__":
    main()
