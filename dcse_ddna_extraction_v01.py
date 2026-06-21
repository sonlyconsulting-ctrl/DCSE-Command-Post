"""
DCSE DDNA Extractor v0.1 — Production-Code Dry Run

Asset ID: DCSE-DDNA-PYTHON-EXTRACTOR-V01
Parent:   DCSE-DDNA-EXTRACT-ROUTINE-001 (v1 doctrine)
Lane:     DCSE Governance Layer
PS Risk:  None (PS-tagged sources halt at Step 03)

Implements the 12-step DDNA extraction routine defined in
DCSE-DDNA-Extraction-Routine-v1-20260515.md.

Design constraints:
  - Standard library only. No third-party deps until governance review approves them.
  - Single file for v0.1. Splits into a package at v0.2 when v6+ features land.
  - File-based registry writes for v0.1. Supabase backend is the v0.2 target,
    gated on RLS verification and credential rotation.
  - PS Critical halt is hard-coded, not configurable.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Literal, Optional, TypedDict


# ---- Type contracts (act as schema) ----

LaneType = Literal["SC", "SS", "PS", "DCSE", "EMP", "CROSS"]
PSRiskType = Literal["None", "Low", "Medium", "High", "Critical"]
ReleaseStatusType = Literal[
    "Internal Prep", "Public-Safe Draft", "Needs Sanitation",
    "Needs Verification", "Ready for DCS Review",
    "Release Candidate", "Published", "Archive", "Blocked"
]
LayerName = Literal["sentiment", "logic", "design", "product", "technical"]


class SourceObject(TypedDict):
    source_id: str
    source_path: str
    source_type: str
    raw_content: str
    metadata: dict


class Signal(TypedDict):
    signal_id: str
    layer: LayerName
    category: str
    evidence: str
    source_location: str
    proposed_reuse: str


class AssetProposal(TypedDict):
    asset_id: str
    asset_name: str
    parent_asset: str
    layer_origin: list
    description: str
    release_status: ReleaseStatusType


# ---- Step 01: load_source ----

def load_source(source_path: str) -> SourceObject:
    """Read source file into a normalized SourceObject. Full read by design — sources are session-scale."""
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path}")

    raw_content = path.read_text(encoding="utf-8")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    return {
        "source_id": f"SRC-{path.stem}-{timestamp}",
        "source_path": str(path.absolute()),
        "source_type": "",
        "raw_content": raw_content,
        "metadata": {
            "filename": path.name,
            "size_bytes": path.stat().st_size,
            "line_count": raw_content.count("\n") + 1,
            "loaded_at": datetime.now().isoformat(),
        },
    }


# ---- Step 02: classify_source ----

# Keyword sets are the audit surface for classification. Update here when source
# patterns drift. v0.2 may add LLM-assisted classification for ambiguous inputs.
_TYPE_SIGNALS = {
    "chat_session": ["chat", "message", "claude", "chatgpt", "gemini", "assistant"],
    "build_session": ["html", "<style>", "asset id", "def ", "function", "version"],
    "learning_session": ["module", "study", "quiz", "flashcard", "lesson"],
    "recruiter_exchange": ["recruiter", "rate", "position", "candidate", "client"],
    "planning_session": ["workflow", "doctrine", "v6+", "roadmap", "spec"],
    "ps_material": ["pro se", "discovery", "deposition", "plaintiff", "court"],
}


def classify_source(source: SourceObject) -> str:
    """Classify source by keyword density. Returns 'hybrid_<types>' when multiple categories tie."""
    content = source["raw_content"].lower()
    hits = {
        stype: sum(1 for kw in kws if kw in content)
        for stype, kws in _TYPE_SIGNALS.items()
    }
    hits = {k: v for k, v in hits.items() if v > 0}

    if not hits:
        return "generic"

    max_count = max(hits.values())
    top_types = [t for t, c in hits.items() if c == max_count]

    return "hybrid_" + "_".join(sorted(top_types)) if len(top_types) > 1 else top_types[0]


# ---- Step 03: detect_lane_and_ps_risk ----

# PS marker sets are deliberately broad. False positives at this gate are
# acceptable; false negatives are not. Critical → hard halt downstream.
_PS_MARKERS_CRITICAL = [
    "pro se", "plaintiff", "deposition", "discovery",
    "court order", "ballentine", "frcp", "necivr",
]
_PS_MARKERS_MEDIUM = ["litigation", "case", "judge", "attorney", "lawsuit"]
_PS_MARKERS_LOW = ["legal", "compliance", "regulatory"]

_LANE_MARKERS = {
    "PS":    ["pro se", "litigation", "case-related", "discovery"],
    "EMP":   ["recruiter", "interview", "opportunity", "cram engine", "oce-"],
    "SC":    ["sonly", "consulting", "consulting service", "client engagement"],
    "SS":    ["smoove", "lifestyle", "storytelling", "cultural"],
    "CROSS": ["cross-lane", "governance", "ddna", "doctrine"],
}


def detect_lane_and_ps_risk(
    source: SourceObject,
    source_type: str,
) -> tuple[LaneType, PSRiskType]:
    """Assign lane and PS risk. Governance-critical step — misclassification here can leak PS material."""
    content = source["raw_content"].lower()

    if any(m in content for m in _PS_MARKERS_CRITICAL):
        ps_risk: PSRiskType = "Critical"
    elif any(m in content for m in _PS_MARKERS_MEDIUM):
        ps_risk = "Medium"
    elif any(m in content for m in _PS_MARKERS_LOW):
        ps_risk = "Low"
    else:
        ps_risk = "None"

    lane: LaneType = "DCSE"
    for candidate, markers in _LANE_MARKERS.items():
        if any(m in content for m in markers):
            lane = candidate  # type: ignore[assignment]
            break

    # PS risk above Medium overrides any other lane assignment.
    # This is a hard rule — DCS authorization is required to override it.
    if ps_risk in ("Critical", "High"):
        lane = "PS"

    return lane, ps_risk


# ---- Steps 04–08: layer extractors ----

def _signal(layer: LayerName, category: str, evidence: str,
            location: str, reuse: str, seq: int) -> Signal:
    """Centralized Signal constructor. Keeps signal records uniform across extractors."""
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "signal_id": f"SIG-{layer.upper()}-{seq:03d}-{ts}",
        "layer": layer,
        "category": category,
        "evidence": evidence,
        "source_location": location,
        "proposed_reuse": reuse,
    }


def extract_sentiment_signals(source: SourceObject) -> list[Signal]:
    """Voice, posture, friction, learning-style signals."""
    content = source["raw_content"]
    signals: list[Signal] = []
    seq = 1

    if re.search(r"em dash|em-dash", content, re.IGNORECASE):
        signals.append(_signal("sentiment", "tone_enforcement",
            "Source rejects em dash use",
            "user_preferences_or_correction",
            "Voice rule for all DCSE outputs", seq))
        seq += 1

    if re.search(r"no hype|without the hype|no excitement", content, re.IGNORECASE):
        signals.append(_signal("sentiment", "anti_hype_posture",
            "Source explicitly rejects hype language",
            "instruction_blocks", "Voice rule across lanes", seq))
        seq += 1

    if re.search(r"cto-direct|executive|strategic|grounded", content, re.IGNORECASE):
        signals.append(_signal("sentiment", "voice_posture",
            "CTO-direct strategic voice required",
            "voice_declaration", "Voice template for SC and DCSE", seq))
        seq += 1

    if re.search(r"active ramp|architecture fluency|production-readiness",
                 content, re.IGNORECASE):
        signals.append(_signal("sentiment", "honest_ramp_posture",
            "Honest skill positioning enforced",
            "interview_prep_materials",
            "Resume and interview language template", seq))
        seq += 1

    return signals


def extract_logic_signals(source: SourceObject) -> list[Signal]:
    """Workflow, routing, gates, triggers, model assignments."""
    content = source["raw_content"]
    signals: list[Signal] = []
    seq = 1

    if "intake" in content.lower() and "outline" in content.lower():
        signals.append(_signal("logic", "workflow_pattern",
            "Intake → outline → source set → studio output pattern",
            "oce_workflow", "Universal DCSE production workflow", seq))
        seq += 1

    if re.search(r"\[oce\]-|DCS-[A-Z]+-", content):
        signals.append(_signal("logic", "naming_convention",
            "Asset ID format DCS-LANE-PRODUCT-INSTANCE-NNN",
            "asset_badges", "Enforced across DCSE asset generation", seq))
        seq += 1

    if "internal prep" in content.lower() and "release candidate" in content.lower():
        signals.append(_signal("logic", "release_taxonomy",
            "Release status taxonomy enforced",
            "final_destination_doctrine",
            "All assets carry release_status field", seq))
        seq += 1

    if "ps firewall" in content.lower() or "ps risk" in content.lower():
        signals.append(_signal("logic", "ps_firewall_rule",
            "PS material isolated from all non-PS lanes",
            "governance_doctrine",
            "Hard rule, never overridden without DCS authorization", seq))
        seq += 1

    return signals


def extract_design_signals(source: SourceObject) -> list[Signal]:
    """Layout, typography, color, hierarchy, icon, comment-discipline signals. v6+ layer."""
    content = source["raw_content"]
    signals: list[Signal] = []
    seq = 1

    if re.search(r"masthead.*module-nav.*footer-bar", content,
                 re.IGNORECASE | re.DOTALL):
        signals.append(_signal("design", "module_layout_pattern",
            "Masthead + module nav + section blocks + footer bar",
            "html_module_structure",
            "Reusable template for OCE-style HTML modules", seq))
        seq += 1

    if "playfair display" in content.lower() and "jetbrains mono" in content.lower():
        signals.append(_signal("design", "typography_pairing",
            "Display serif + body serif + technical monospace pairing",
            "css_font_imports",
            "Font system template for DCSE documents", seq))
        seq += 1

    if "asset-badge" in content.lower() or "asset_badge" in content.lower():
        signals.append(_signal("design", "asset_badge_convention",
            "Monospace pill row carrying asset ID, version, lane, PS risk",
            "html_header_pattern",
            "Required on every DCSE-generated HTML asset", seq))
        seq += 1

    if "icon concept" in content.lower() or re.search(
            r"five.*icon", content, re.IGNORECASE):
        signals.append(_signal("design", "icon_system_seed",
            "Five-icon brand system pattern",
            "icon_concept_session",
            "Seed for Auto-Branding Workflow asset", seq))
        seq += 1

    return signals


def extract_product_signals(source: SourceObject) -> list[Signal]:
    """Reusable product candidates, parent/child chains, member-content readiness. v6+ layer."""
    content = source["raw_content"]
    signals: list[Signal] = []
    seq = 1

    if re.search(r"template|reusable|repeatable", content, re.IGNORECASE):
        signals.append(_signal("product", "reusable_template_candidate",
            "Source contains templateable patterns",
            "various_locations",
            "Candidate for productization stage gate", seq))
        seq += 1

    if "opportunity cram engine" in content.lower() or "oce" in content.lower():
        signals.append(_signal("product", "oce_methodology",
            "OCE is productizable methodology, not yet a packaged product",
            "oce_session",
            "SC consulting service offering candidate", seq))
        seq += 1

    if "admin members" in content.lower() or "member content" in content.lower():
        signals.append(_signal("product", "member_content_candidate",
            "Content suitable for member-gated placement",
            "destination_routing",
            "Wix Admin Members placement candidate", seq))
        seq += 1

    if re.search(r"parent asset|child asset|root asset", content, re.IGNORECASE):
        signals.append(_signal("product", "asset_chain_pattern",
            "Hierarchical parent-child-root asset relationship",
            "asset_record_schema",
            "Required structure for product family tracking", seq))
        seq += 1

    return signals


def extract_technical_signals(source: SourceObject) -> list[Signal]:
    """Automation candidates, connector needs, infrastructure implications."""
    content = source["raw_content"]
    signals: list[Signal] = []
    seq = 1

    if re.search(r"manual|by hand|cut and paste", content, re.IGNORECASE):
        signals.append(_signal("technical", "automation_candidate",
            "Manual process identified",
            "workflow_discussion",
            "Python or workflow automation target", seq))
        seq += 1

    if re.search(r"wix|notebooklm|powerdirector", content, re.IGNORECASE):
        signals.append(_signal("technical", "connector_requirement",
            "External service connector needed",
            "tool_discussion",
            "Bridge agent or MCP integration target", seq))
        seq += 1

    if "registry" in content.lower() and "asset" in content.lower():
        signals.append(_signal("technical", "registry_write_requirement",
            "Asset registry writes needed",
            "command_post_discussion",
            "File-based for v0.1; Supabase for v0.2", seq))
        seq += 1

    if "supabase" in content.lower() or "next.js" in content.lower():
        signals.append(_signal("technical", "managed_backend_implication",
            "Managed Postgres or SSR framework relevant",
            "tech_stack_discussion",
            "v0.2 migration target for cross-lane registry", seq))
        seq += 1

    return signals


# ---- Step 09: propose_assets ----

def propose_assets(
    sentiment: list[Signal],
    logic: list[Signal],
    design: list[Signal],
    product: list[Signal],
    technical: list[Signal],
) -> list[AssetProposal]:
    """
    Surface signal clusters as proposed assets.

    v0.1 rule: any layer with 3+ signals produces one aggregate asset.
    v0.2 will replace this with semantic clustering and importance scoring
    (DCSE-DDNA-Extraction-Routine-v2-Spec, Section 4).
    """
    proposals: list[AssetProposal] = []
    timestamp = datetime.now().strftime("%Y%m%d")
    layers = {
        "sentiment": sentiment, "logic": logic, "design": design,
        "product": product, "technical": technical,
    }

    for layer_name, sigs in layers.items():
        if len(sigs) >= 3:
            proposals.append({
                "asset_id": f"DCSE-DDNA-{layer_name.upper()}-AGG-{timestamp}",
                "asset_name": f"DDNA {layer_name.capitalize()} Aggregate Asset",
                "parent_asset": "DCSE-DDNA-EXTRACT-ROUTINE-001",
                "layer_origin": [layer_name],
                "description": f"Aggregated {len(sigs)} {layer_name} signals from current extraction",
                "release_status": "Internal Prep",
            })

    return proposals


# ---- Step 10: assign_release_status ----

def assign_release_status(proposals: list[AssetProposal]) -> list[AssetProposal]:
    """
    Apply release taxonomy.

    Conservative default: everything starts at Internal Prep.
    No automated promotion. Stage advancement requires human review per
    DCSE-Distribution-Methodology-v1.
    """
    for p in proposals:
        if not p["release_status"]:
            p["release_status"] = "Internal Prep"
    return proposals


# ---- Step 11: write_registry_records ----

def write_registry_records(
    proposals: list[AssetProposal],
    output_path: str,
    all_signals: dict[str, list[Signal]],
    source: SourceObject,
    lane: LaneType,
    ps_risk: PSRiskType,
) -> list[str]:
    """
    Write one JSON record per proposed asset.

    v0.1 writes flat files. v0.2 will target Supabase public.dcse_plan_inbox
    once RLS policies are verified and credentials are confirmed rotated.
    Until then, file-based avoids any browser-side write exposure.
    """
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []

    for p in proposals:
        record = {
            "asset_id": p["asset_id"],
            "asset_name": p["asset_name"],
            "parent_asset": p["parent_asset"],
            "source_opportunity": source["source_id"],
            "output_type": "DDNA Aggregate Asset",
            "lane": lane,
            "layer_origin": p["layer_origin"],
            "file_location": str(output_dir.absolute()),
            "destination": "Command Post Registry",
            "product_status": "draft",
            "release_status": p["release_status"],
            "ps_risk": ps_risk,
            "ddna_sentiment_signals": [s["signal_id"] for s in all_signals["sentiment"]],
            "ddna_logic_signals":     [s["signal_id"] for s in all_signals["logic"]],
            "ddna_design_signals":    [s["signal_id"] for s in all_signals["design"]],
            "ddna_product_signals":   [s["signal_id"] for s in all_signals["product"]],
            "ddna_technical_signals": [s["signal_id"] for s in all_signals["technical"]],
            "next_action": "DCS review and confirm asset registration",
            "version": "v1",
            "date_created": datetime.now().strftime("%Y-%m-%d"),
            "doctrine_flag": "no",
        }
        path = output_dir / f"{p['asset_id']}.json"
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        written.append(str(path))

    return written


# ---- Step 12: export_summary ----

def export_summary(
    source: SourceObject,
    all_signals: dict[str, list[Signal]],
    proposals: list[AssetProposal],
    registry_writes: list[str],
    output_path: str,
    lane: LaneType,
    ps_risk: PSRiskType,
) -> str:
    """Produce markdown summary. Format is intentionally friendly to cross-suite QA ingestion."""
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "# DDNA Extraction Summary",
        "",
        f"**Source:** {source['source_path']}",
        f"**Source ID:** {source['source_id']}",
        f"**Lane:** {lane}",
        f"**PS Risk:** {ps_risk}",
        f"**Extraction Date:** {datetime.now().isoformat()}",
        "",
        "## Signal Counts by Layer",
        "",
    ]
    for layer_name, sigs in all_signals.items():
        lines.append(f"- **{layer_name.capitalize()}:** {len(sigs)} signals")

    lines.extend([
        "",
        f"## Proposed Assets ({len(proposals)})",
        "",
        "| Asset ID | Name | Release Status |",
        "|---|---|---|",
    ])
    for p in proposals:
        lines.append(f"| {p['asset_id']} | {p['asset_name']} | {p['release_status']} |")

    lines.extend(["", f"## Registry Files Written ({len(registry_writes)})", ""])
    for fp in registry_writes:
        lines.append(f"- `{fp}`")
    lines.append("")

    summary_path = output_dir / f"DDNA-Summary-{source['source_id']}.md"
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return str(summary_path)


# ---- Orchestrator ----

def run_ddna_extraction(source_path: str, output_path: str) -> dict[str, Any]:
    """
    Execute the full 12-step routine.

    Halts on PS Critical without writing any registry records. All console
    output is part of the audit trail — keep it readable.
    """
    print("=" * 60)
    print("DCSE DDNA EXTRACTION — STARTING")
    print(f"Source: {source_path}")
    print(f"Output: {output_path}")
    print("=" * 60)

    print("\n[01] Loading source...")
    source = load_source(source_path)
    print(f"  Loaded {source['metadata']['size_bytes']} bytes")

    print("\n[02] Classifying source...")
    source_type = classify_source(source)
    source["source_type"] = source_type
    print(f"  Classification: {source_type}")

    print("\n[03] Detecting lane and PS risk...")
    lane, ps_risk = detect_lane_and_ps_risk(source, source_type)
    print(f"  Lane: {lane}, PS Risk: {ps_risk}")

    # Hard governance halt. No registry writes. No summary export.
    # Routine exits with a partial extraction log only.
    if ps_risk == "Critical":
        print("\n*** HALTED: PS Critical risk detected ***")
        print("Routine cannot proceed without DCS authorization.")
        return {
            "status": "halted",
            "reason": "PS Critical",
            "source_id": source["source_id"],
        }

    print("\n[04-08] Extracting signals across five layers...")
    sentiment = extract_sentiment_signals(source)
    logic = extract_logic_signals(source)
    design = extract_design_signals(source)
    product = extract_product_signals(source)
    technical = extract_technical_signals(source)
    print(f"  Sentiment: {len(sentiment)} | Logic: {len(logic)} | "
          f"Design: {len(design)} | Product: {len(product)} | Technical: {len(technical)}")

    all_signals = {
        "sentiment": sentiment, "logic": logic, "design": design,
        "product": product, "technical": technical,
    }

    print("\n[09] Proposing assets...")
    proposals = propose_assets(sentiment, logic, design, product, technical)
    print(f"  Proposed {len(proposals)} assets")

    print("\n[10] Assigning release status...")
    proposals = assign_release_status(proposals)

    print("\n[11] Writing registry records...")
    writes = write_registry_records(proposals, output_path, all_signals,
                                    source, lane, ps_risk)
    print(f"  Wrote {len(writes)} registry files")

    print("\n[12] Exporting summary...")
    summary_path = export_summary(source, all_signals, proposals, writes,
                                  output_path, lane, ps_risk)
    print(f"  Summary: {summary_path}")

    print("\n" + "=" * 60)
    print("DCSE DDNA EXTRACTION — COMPLETE")
    print("=" * 60)

    return {
        "status": "complete",
        "source_id": source["source_id"],
        "lane": lane,
        "ps_risk": ps_risk,
        "asset_count": len(proposals),
        "signal_count": sum(len(s) for s in all_signals.values()),
        "summary_path": summary_path,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dcse_ddna_extraction_v01.py <source_path> <output_path>")
        print("Example: python dcse_ddna_extraction_v01.py chat.md ./ddna_output/")
        sys.exit(1)

    result = run_ddna_extraction(sys.argv[1], sys.argv[2])

    # Exit codes for shell chaining: 0=ok, 1=error, 2=governance halt.
    if result["status"] == "complete":
        sys.exit(0)
    elif result["status"] == "halted":
        sys.exit(2)
    else:
        sys.exit(1)
