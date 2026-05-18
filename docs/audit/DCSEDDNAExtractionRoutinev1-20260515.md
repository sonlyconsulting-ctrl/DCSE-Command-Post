# DCSE DDNA Extraction Routine and Design-Oriented Asset Rules

**Asset ID:** DCSE-DDNA-EXTRACT-ROUTINE-001
**Version:** v1
**Date:** 2026-05-15
**Lane:** DCS Enterprise / Cross-Lane Governance Layer
**PS Risk:** None detected
**Release Status:** Internal Prep — Draft for QA Distribution
**Distribution Targets:** ChatGPT, Gemini, NotebookLM, Claude (cross-suite QA)
**Format Note:** Markdown chosen as primary format for cross-model QA readability. HTML production follows after QA sign-off.

---

## 1. Purpose

DDNA is the structured capture of reusable signals from any DCS interaction, conversation, build session, or work product. Until v6, DDNA was a two-layer model — Sentiment signals and Logic signals. That model captured tone and workflow but missed two of the most valuable signal classes that DCSE actually produces: Design decisions and Product candidates.

This routine formalizes the v6+ five-layer DDNA model, defines the 12-step extraction sequence, specifies the Python or Command Post script outline that automates it, evaluates the connector and automation options, and establishes the asset record schema that any DDNA-derived asset must carry.

The output is enforceable. Every Claude session, every NotebookLM run, every ChatGPT exchange, and every internal build session is now subject to DDNA capture under this routine when DCS marks it for extraction.

---

## 2. What Changed in v6+

The v5 model captured:
- **Sentiment signals** — tone, voice, confidence, posture, learning rhythm
- **Logic signals** — workflow steps, routing rules, asset names, release conditions

The v5 model missed:
- **Design signals** — layout patterns, HTML structure, color systems, typography choices, icon direction, information hierarchy, comment discipline, asset badge conventions
- **Product signals** — reusable product candidates, parent/child asset chains, membership content readiness, public-safe draft candidates
- **Technical signals** — script automation opportunities, connector requirements, Command Post ingestion patterns, registry update logic, file handling rules

The v6+ model captures all five. Design and Product signals become first-class extraction targets because the OCE work proved that DCSE generates structural and product value continuously, and losing that value to undocumented exhaust is the actual cost.

---

## 3. The Five-Layer DDNA Model

Each layer has a defined signal set, a capture rule, and a destination in the asset registry. No layer is optional. Every extraction run produces output for all five.

### Layer 1 — Sentiment Signals

**What this captures:** the human and voice dimensions of the interaction.

| Signal Category | Examples |
|---|---|
| Tone | calm executive, cinematic restraint, no hype, no em dashes |
| Voice posture | CTO-direct, strategic, grounded, useful |
| Confidence signals | where DCS is certain, where DCS is hedging, where DCS is ramping |
| Friction signals | where DCS corrects Claude, where Claude misread direction |
| Learning style | structured, scaffolded, analogy-driven, command-post pattern |
| Visual style | dark base + amber/gold accent, editorial typography, no AI slop |
| Executive readiness | which fragments are interview-ready, which need rehearsal |
| Public-safe translation | what gets sanitized before any external release |

**Capture rule:** sentiment signals are read directly from DCS's language, corrections, and stated preferences within the source. Do not infer beyond stated evidence.

### Layer 2 — Logic Signals

**What this captures:** the workflow, routing, and decision architecture.

| Signal Category | Examples |
|---|---|
| Workflow steps | intake → outline → source set → studio → output → destination |
| Routing rules | OCE goes through Command Post, PS material stays in PS lane |
| Trigger conditions | when does a chat become an asset, when does a draft become a release candidate |
| Asset definitions | what counts as a parent asset vs a child asset |
| Release gates | Internal Prep, Public-Safe Draft, Needs Sanitation, Ready for DCS Review, Published |
| Model assignments | which model produces what (Claude for HTML, NotebookLM for video, ChatGPT for outline) |
| QA gates | source verified, lane correct, PS risk checked, claims verified |
| Decision logs | Use/Make decisions, tool selection rationale, abandoned approaches |

**Capture rule:** logic signals are extracted from the structural choices made during the session. Every fork in the path is a signal.

### Layer 3 — Design Signals (NEW IN v6+)

**What this captures:** the visual, structural, and formatting decisions that give DCSE its distinctive presence.

| Signal Category | Examples |
|---|---|
| Layout patterns | masthead + module nav + section blocks + footer bar |
| HTML comment discipline | every CSS block, every section, every functional element commented for learning |
| Color systems | lane-specific accent colors (gold for learning, rust for accent, teal for verified) |
| Typography pairings | Playfair Display + Source Serif + JetBrains Mono; Syne + Epilogue + JetBrains Mono |
| Icon direction | radar pulse, circuit path, gear-in-brief, funnel-forward, hex-gate |
| Information hierarchy | situation intelligence → DCS positioning → executive overview → mapping → enterprise principles |
| Asset badge conventions | DCS-LANE-PRODUCT-INSTANCE-NNN, version, date, PS risk, release status |
| Website/Admin Members placement | gated, ungated, member content, public-safe |
| Module interconnection | cross-link navigation between related assets |

**Capture rule:** design signals are extracted from any visual artifact produced — HTML, SVG, diagrams, slide outlines, video direction. The pattern that recurs is the signal worth preserving.

### Layer 4 — Product Signals (NEW IN v6+)

**What this captures:** the reusable product candidates and asset family relationships emerging from the work.

| Signal Category | Examples |
|---|---|
| Reusable product candidates | OCE Cram Engine itself, NotebookLM video prompt template, 4-module HTML pattern |
| Parent/child asset chains | OCE-001 → OCE-NLM-001 → OCE-NLM-VIDEO-001 → OCE-USECASE-001 |
| Cross-lane reuse | SC consulting use of OCE format, SS storytelling use of cinematic video style |
| Membership content readiness | which OCE modules are member-gated, which are public-eligible after sanitation |
| Public-safe draft candidates | sanitized OCE methodology as SC product, agentic teaching video as SS content |
| Template extraction | the cram module structure is a template; the NotebookLM prompt is a template |
| Brand product opportunities | icon system from this session can become DCSE Employment Workflow visual identity |
| Productization gaps | what is missing before any of these becomes a sellable or publishable product |

**Capture rule:** product signals are extracted by asking three questions of every artifact — can this be reused, can this be templated, can this be sold or distributed.

### Layer 5 — Technical Signals

**What this captures:** the automation, scripting, and infrastructure implications of the work.

| Signal Category | Examples |
|---|---|
| Script automation candidates | DDNA extraction itself, file naming enforcement, registry record writing |
| Connector requirements | NotebookLM upload, Google Drive folder routing, Command Post asset registration |
| Command Post ingestion | how outputs enter the registry, what metadata is required |
| Registry update logic | when status changes, when version bumps, when archives happen |
| File handling rules | naming convention enforcement, folder taxonomy, version control |
| HTML builder queue | which content types need HTML conversion, in what order |
| API touchpoints | which workflows could use Anthropic API, OpenAI API, Google API |
| Supabase/Next.js implications | what needs database schema, what needs RLS policies, what is client vs server |

**Capture rule:** technical signals are extracted by asking what could be automated, what currently requires manual work, and what infrastructure must exist before automation is safe.

---

## 4. The 12-Step Extraction Routine

This is the formal sequence. Every DDNA extraction follows it. No steps are optional. No steps reorder.

```
STEP 01  load_source
STEP 02  classify_source
STEP 03  detect_lane_and_ps_risk
STEP 04  extract_sentiment_signals
STEP 05  extract_logic_signals
STEP 06  extract_design_signals
STEP 07  extract_product_signals
STEP 08  extract_technical_signals
STEP 09  propose_assets
STEP 10  assign_release_status
STEP 11  write_registry_records
STEP 12  export_summary
```

### Step 01 — load_source

**Input:** chat transcript, document, build session log, video transcript, or artifact bundle.
**Process:** read entire source. Do not summarize during this pass. Capture timestamps, speaker turns, and artifact references.
**Output:** normalized source object with metadata.
**Quality gate:** confirm the entire source loaded. Partial loads halt the routine.

### Step 02 — classify_source

**Input:** loaded source.
**Process:** identify the source type — chat session, build session, learning session, recruiter exchange, internal planning, PS material, or hybrid.
**Output:** source type label.
**Quality gate:** if hybrid contains PS material, the PS portion isolates before any further processing.

### Step 03 — detect_lane_and_ps_risk

**Input:** classified source.
**Process:** assign lane (SC, SS, PS, DCSE Command Post, DCS Employment, Cross-Lane). Run PS risk check against the lane's firewall rules.
**Output:** lane assignment and PS risk score (None / Low / Medium / High / Critical).
**Quality gate:** any PS risk above None requires DCS authorization before extraction continues. Critical halts extraction entirely.

### Steps 04 through 08 — Layer Extraction

Each layer extraction follows the same pattern:

**Input:** classified, lane-tagged source.
**Process:** scan for the signal categories defined for that layer. Record each signal as a discrete entry with its source location, the verbatim or paraphrased evidence, and the proposed reuse case.
**Output:** signal table for that layer.
**Quality gate:** every signal must have evidence. Signals without source evidence are flagged for DCS review, not auto-included.

### Step 09 — propose_assets

**Input:** all five signal tables.
**Process:** identify which signal clusters can become standalone assets. Apply the parent/child asset rules. Generate proposed asset IDs following the naming convention.
**Output:** asset proposal list with Asset ID, name, parent, layer source, and brief description.
**Quality gate:** proposed assets must pass the Use/Make Decision Point (see Section 6) before any build begins.

### Step 10 — assign_release_status

**Input:** asset proposal list.
**Process:** apply the release status taxonomy: Internal Prep, Public-Safe Draft, Needs Sanitation, Needs Verification, Ready for DCS Review, Release Candidate, Published, Archive, Blocked.
**Output:** each asset proposal carries a release status.
**Quality gate:** Public-Safe Draft and Release Candidate require human review before status assignment.

### Step 11 — write_registry_records

**Input:** asset proposals with release status.
**Process:** generate Command Post registry records using the schema in Section 7. Write to the appropriate folder in the OCE taxonomy.
**Output:** registry record files, one per asset.
**Quality gate:** every record must populate every required field. Records with missing required fields cannot write.

### Step 12 — export_summary

**Input:** complete extraction.
**Process:** generate a DDNA Extraction Summary document covering all five layers, the proposed assets, the registry write results, and the open items requiring DCS attention.
**Output:** summary file in markdown for QA, optional HTML for archival.
**Quality gate:** summary distributes only after PS risk check passes and DCS marks the routine complete.

---

## 5. Python / Command Post Script Outline

The 12-step routine maps to a Python module that any Command Post automation can call. Function names below match the routine steps exactly. This outline is implementation-ready.

```python
"""
DCSE DDNA Extraction Routine
Asset: DCSE-DDNA-EXTRACT-ROUTINE-001
Version: v1
Doctrine: Structure Precedes Scale

This module implements the 12-step DDNA extraction routine.
It is callable from Command Post, from a local CLI, or from any
scheduled automation. It does not write to any external system
without explicit DCS authorization checks.
"""

from typing import Literal, TypedDict

# ----------------------------------------------------------
# TYPE DEFINITIONS
# ----------------------------------------------------------

LaneType = Literal["SC", "SS", "PS", "DCSE", "EMP", "CROSS"]
PSRiskType = Literal["None", "Low", "Medium", "High", "Critical"]
ReleaseStatusType = Literal[
    "Internal Prep", "Public-Safe Draft", "Needs Sanitation",
    "Needs Verification", "Ready for DCS Review",
    "Release Candidate", "Published", "Archive", "Blocked"
]

class SourceObject(TypedDict):
    source_id: str
    source_type: str
    raw_content: str
    metadata: dict

class Signal(TypedDict):
    layer: str
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


# ----------------------------------------------------------
# STEP 01 — LOAD SOURCE
# ----------------------------------------------------------
def load_source(source_path: str) -> SourceObject:
    """
    Read entire source content. Do not summarize.
    Halts on partial loads.
    """
    pass


# ----------------------------------------------------------
# STEP 02 — CLASSIFY SOURCE
# ----------------------------------------------------------
def classify_source(source: SourceObject) -> str:
    """
    Identify source type: chat, build, learning, recruiter,
    internal_planning, PS, or hybrid.
    Hybrid sources require PS isolation before further steps.
    """
    pass


# ----------------------------------------------------------
# STEP 03 — DETECT LANE AND PS RISK
# ----------------------------------------------------------
def detect_lane_and_ps_risk(
    source: SourceObject, source_type: str
) -> tuple[LaneType, PSRiskType]:
    """
    Assign lane. Run PS firewall check.
    Critical PS risk halts the routine.
    """
    pass


# ----------------------------------------------------------
# STEPS 04 THROUGH 08 — LAYER EXTRACTORS
# All five functions follow the same shape.
# ----------------------------------------------------------
def extract_sentiment_signals(source: SourceObject) -> list[Signal]:
    """Capture tone, posture, voice, friction, learning style."""
    pass

def extract_logic_signals(source: SourceObject) -> list[Signal]:
    """Capture workflow, routing, triggers, gates, model assignments."""
    pass

def extract_design_signals(source: SourceObject) -> list[Signal]:
    """Capture layout, typography, color, icons, hierarchy, comments."""
    pass

def extract_product_signals(source: SourceObject) -> list[Signal]:
    """Capture reusable products, parent/child chains, membership candidates."""
    pass

def extract_technical_signals(source: SourceObject) -> list[Signal]:
    """Capture automation candidates, connectors, scripts, infrastructure."""
    pass


# ----------------------------------------------------------
# STEP 09 — PROPOSE ASSETS
# ----------------------------------------------------------
def propose_assets(
    sentiment: list[Signal],
    logic: list[Signal],
    design: list[Signal],
    product: list[Signal],
    technical: list[Signal],
) -> list[AssetProposal]:
    """
    Identify signal clusters that warrant standalone assets.
    Apply parent/child rules. Generate Asset IDs.
    Every proposal must pass the Use/Make Decision Point.
    """
    pass


# ----------------------------------------------------------
# STEP 10 — ASSIGN RELEASE STATUS
# ----------------------------------------------------------
def assign_release_status(
    proposals: list[AssetProposal]
) -> list[AssetProposal]:
    """
    Apply release taxonomy. Public-Safe and Release Candidate
    require human review before status sets.
    """
    pass


# ----------------------------------------------------------
# STEP 11 — WRITE REGISTRY RECORDS
# ----------------------------------------------------------
def write_registry_records(
    proposals: list[AssetProposal],
    target_path: str
) -> list[str]:
    """
    Generate one registry record file per asset.
    Records missing required fields cannot write.
    Returns list of written file paths.
    """
    pass


# ----------------------------------------------------------
# STEP 12 — EXPORT SUMMARY
# ----------------------------------------------------------
def export_summary(
    source: SourceObject,
    all_signals: dict[str, list[Signal]],
    proposals: list[AssetProposal],
    registry_writes: list[str],
    output_path: str
) -> str:
    """
    Produce the DDNA Extraction Summary in markdown.
    HTML version generated separately by the HTML builder.
    Returns summary file path.
    """
    pass


# ----------------------------------------------------------
# MAIN ORCHESTRATOR
# ----------------------------------------------------------
def run_ddna_extraction(source_path: str, output_path: str) -> dict:
    """
    Execute the full 12-step routine.
    Halts at any quality gate failure.
    Returns extraction summary with status.
    """
    source = load_source(source_path)
    source_type = classify_source(source)
    lane, ps_risk = detect_lane_and_ps_risk(source, source_type)

    # PS firewall enforcement
    if ps_risk == "Critical":
        return {"status": "halted", "reason": "PS Critical"}

    # Layer extraction
    sentiment = extract_sentiment_signals(source)
    logic = extract_logic_signals(source)
    design = extract_design_signals(source)
    product = extract_product_signals(source)
    technical = extract_technical_signals(source)

    # Asset proposals and release
    proposals = propose_assets(sentiment, logic, design, product, technical)
    proposals = assign_release_status(proposals)

    # Registry writes
    writes = write_registry_records(proposals, output_path)

    # Summary export
    summary_path = export_summary(
        source,
        {
            "sentiment": sentiment,
            "logic": logic,
            "design": design,
            "product": product,
            "technical": technical,
        },
        proposals,
        writes,
        output_path
    )

    return {
        "status": "complete",
        "lane": lane,
        "ps_risk": ps_risk,
        "asset_count": len(proposals),
        "summary_path": summary_path
    }
```

---

## 6. Use This or Make This — Decision Point

Every proposed automation, connector, or tool selection passes through this decision block. The block is the v6+ formalization of how DCSE chooses between adopting an existing tool and building a custom one.

### Decision Block Structure

For each automation candidate, the block produces:

```
DECISION POINT: [Automation Candidate Name]

USE THIS — [Existing Tool Option]
  What it gives you:
  What it costs:
  What it lacks:
  Lock-in risk:

MAKE THIS — [Custom Build Option]
  What it gives you:
  What it costs:
  Build effort:
  Maintenance burden:

DCSE DECISION CRITERIA
  Lane fit:
  Governance fit:
  PS firewall compatibility:
  Reusability across lanes:
  Time-to-value:

v6+ DOCTRINE FLAG
  Becomes reusable doctrine entry: yes / no
  If yes, doctrine asset ID:

DDNA SIGNAL CAPTURE
  This decision logged as Logic-layer signal: yes / no
  Routing rule for future identical decisions:

VERDICT: Use This / Make This / Hybrid / Defer
RATIONALE:
```

### Decision Points for the DDNA Extraction Routine

The routine itself proposes several automation candidates. Each gets a decision block.

---

**DECISION POINT 01: DDNA Extraction Script Runtime**

**USE THIS — Existing Python Environment**
- What it gives you: full control, runs locally, no external dependencies, fits Command Post pattern
- What it costs: free, requires Python install
- What it lacks: no built-in UI, requires CLI familiarity
- Lock-in risk: none

**MAKE THIS — Custom Streamlit or Next.js Dashboard**
- What it gives you: visual UI for DDNA runs, signal preview, asset proposal review
- What it costs: build time, hosting, ongoing maintenance
- Build effort: 2-3 weeks for first release
- Maintenance burden: ongoing

**DCSE DECISION CRITERIA**
- Lane fit: high — fits DCSE Command Post
- Governance fit: high — local execution keeps all data inside DCSE perimeter
- PS firewall compatibility: high — no external service touches PS-tagged sources
- Reusability across lanes: high
- Time-to-value: Python option is days; UI is weeks

**v6+ DOCTRINE FLAG**
- Becomes reusable doctrine entry: yes
- Doctrine Asset ID: DCSE-DOCT-AUTOMATION-RUNTIME-001

**DDNA SIGNAL CAPTURE**
- This decision logged as Logic-layer signal: yes
- Routing rule for future identical decisions: when an internal automation candidate exists, default to local Python unless a stakeholder-facing UI is the primary use case

**VERDICT: Use This (Python first, UI later)**
**RATIONALE:** Local Python script meets the immediate need, preserves PS firewall integrity, fits the Command Post pattern, and defers the UI investment until extraction volume justifies it.

---

**DECISION POINT 02: NotebookLM Source Upload Connector**

**USE THIS — Manual Upload Through NotebookLM Web Interface**
- What it gives you: zero build cost, full NotebookLM feature access
- What it costs: manual time per session
- What it lacks: no automation, no batch processing
- Lock-in risk: low

**MAKE THIS — Custom Drive-to-NotebookLM Bridge**
- What it gives you: scheduled or triggered uploads, batch processing
- What it costs: API access (NotebookLM API surface is limited as of this writing — needs verification)
- Build effort: depends on API availability
- Maintenance burden: vulnerable to NotebookLM API changes

**DCSE DECISION CRITERIA**
- Lane fit: medium
- Governance fit: high for manual, unknown for custom
- PS firewall compatibility: manual upload is auditable; automated upload requires lane checks before send
- Reusability across lanes: medium
- Time-to-value: manual is immediate

**v6+ DOCTRINE FLAG**
- Becomes reusable doctrine entry: yes
- Doctrine Asset ID: DCSE-DOCT-EXTERNAL-CONNECTOR-001

**DDNA SIGNAL CAPTURE**
- This decision logged as Logic-layer signal: yes
- Routing rule for future identical decisions: when an external service has limited or unverified API, prefer manual workflow with audit logging until DCSE volume justifies bridge investment

**VERDICT: Use This (manual upload, log every send)**
**RATIONALE:** NotebookLM's API surface is not stable enough as of current knowledge to commit to a custom bridge. Manual upload remains auditable, preserves PS firewall integrity, and avoids investment in a connector vulnerable to upstream changes.

---

**DECISION POINT 03: Command Post Registry Backend**

**USE THIS — Supabase Postgres + RLS**
- What it gives you: managed Postgres, built-in auth, RLS policies, fits the SC tech stack
- What it costs: free tier covers initial use, paid tier scales
- What it lacks: requires schema work, RLS verification
- Lock-in risk: moderate, but exportable

**MAKE THIS — Local SQLite or Flat-File JSON Registry**
- What it gives you: zero external dependencies, full local control
- What it costs: free, build effort minimal
- Build effort: hours
- Maintenance burden: low for single-user, breaks at multi-user

**DCSE DECISION CRITERIA**
- Lane fit: high for either
- Governance fit: Supabase offers RLS for cross-lane isolation; local files require manual lane separation
- PS firewall compatibility: PS records should never touch Supabase. Local file isolation is mandatory for PS material regardless of which option chosen for non-PS lanes.
- Reusability across lanes: Supabase scales across SC, SS, DCSE; PS stays local-only
- Time-to-value: local is immediate, Supabase is days

**v6+ DOCTRINE FLAG**
- Becomes reusable doctrine entry: yes
- Doctrine Asset ID: DCSE-DOCT-REGISTRY-BACKEND-001

**DDNA SIGNAL CAPTURE**
- This decision logged as Logic-layer signal: yes
- Routing rule for future identical decisions: PS lane registries are always local-only; non-PS lanes can use Supabase with verified RLS

**VERDICT: Hybrid**
**RATIONALE:** Local flat-file or SQLite for PS lane and for initial DDNA bootstrapping. Supabase Postgres with RLS for cross-lane SC/SS/DCSE registry once schema is verified and lane isolation is tested.

---

**DECISION POINT 04: Workflow Orchestration Tool**

**USE THIS — n8n (self-hosted)**
- What it gives you: visual workflow builder, large connector library, self-hostable on local hardware
- What it costs: free if self-hosted, hosting infrastructure required
- What it lacks: limited DCSE-specific governance hooks; PS firewall must be manually enforced
- Lock-in risk: low, workflows are exportable

**USE THIS — Zapier or Make**
- What they give you: managed orchestration, no infrastructure
- What they cost: subscription, data passes through their cloud
- What they lack: PS firewall compatibility is questionable for sensitive lanes
- Lock-in risk: moderate to high

**MAKE THIS — Custom Python Orchestrator**
- What it gives you: full DCSE governance integration, native PS firewall enforcement
- What it costs: build effort
- Build effort: 2-4 weeks for production orchestrator
- Maintenance burden: ongoing

**DCSE DECISION CRITERIA**
- Lane fit: custom Python fits best; n8n acceptable for non-PS
- Governance fit: custom is highest; n8n second; Zapier/Make are unacceptable for PS material
- PS firewall compatibility: only custom Python and self-hosted n8n meet the standard
- Reusability across lanes: all three options are reusable
- Time-to-value: Zapier fastest, n8n medium, custom slowest

**v6+ DOCTRINE FLAG**
- Becomes reusable doctrine entry: yes
- Doctrine Asset ID: DCSE-DOCT-ORCHESTRATION-001

**DDNA SIGNAL CAPTURE**
- This decision logged as Logic-layer signal: yes
- Routing rule for future identical decisions: PS material never routes through third-party SaaS orchestration; non-PS work can use n8n self-hosted; cross-lane core orchestration is custom Python

**VERDICT: Hybrid (n8n for non-PS, custom Python for cross-lane core)**
**RATIONALE:** n8n self-hosted handles non-PS workflows with visual maintainability. Cross-lane core orchestration involving DDNA, registry writes, and lane routing stays in custom Python where DCSE governance can be enforced in code.

---

## 7. Asset Record Schema

Every asset produced by the DDNA routine carries this schema. Records missing any required field cannot write to the registry.

| Field | Required | Description |
|---|---|---|
| asset_id | yes | DCS-LANE-PRODUCT-INSTANCE-NNN format |
| asset_name | yes | human-readable name |
| parent_asset | conditional | parent Asset ID if this is a child asset |
| root_asset | conditional | top-of-chain Asset ID for traceability |
| source_opportunity | yes | originating opportunity, project, or topic |
| output_type | yes | document, HTML module, video, script, prompt, etc. |
| lane | yes | SC, SS, PS, DCSE, EMP, CROSS |
| layer_origin | yes | which DDNA layer(s) produced this asset |
| file_location | yes | absolute or relative path |
| destination | yes | website, Admin Members, Command Post, PowerDirector, YouTube, etc. |
| product_status | yes | draft, candidate, ready, archived |
| release_status | yes | from the release taxonomy |
| ps_risk | yes | None, Low, Medium, High, Critical |
| public_eligible | yes | yes / no / needs sanitation |
| html_needed | yes | yes / no |
| powerdirector_needed | yes | yes / no |
| youtube_eligible | yes | yes / no / after sanitation |
| website_admin_placement | conditional | path if applicable |
| ddna_sentiment_signals | yes | reference IDs to extracted signals |
| ddna_logic_signals | yes | reference IDs to extracted signals |
| ddna_design_signals | yes | reference IDs to extracted signals |
| ddna_product_signals | yes | reference IDs to extracted signals |
| ddna_technical_signals | yes | reference IDs to extracted signals |
| next_action | yes | concrete next step |
| version | yes | v1, v2, etc. |
| date_created | yes | YYYY-MM-DD |
| date_modified | yes | YYYY-MM-DD |
| doctrine_flag | yes | does this become a reusable doctrine entry |
| doctrine_asset_id | conditional | if doctrine_flag is yes |

---

## 8. Distribution and Enforcement

### Who Uses Which Layer

| Consumer | Primary Layer Need |
|---|---|
| DCS (Founder) | All layers, with emphasis on Product and Logic |
| Claude (CTO role) | Design, Technical, Logic |
| ChatGPT (intake, outline) | Logic, Sentiment |
| Gemini / NotebookLM | Sentiment, Design (for video and audio production) |
| Command Post script | Technical, Logic, registry writes |
| Future DCSE team or contractors | All five, with PS firewall enforcement at the lane check |

### Enforcement Rule

DDNA extraction is mandatory on the following triggers:
- Any session DCS marks for extraction
- Any chat that produces a deliverable destined for the registry
- Any build session that introduces new design patterns or product candidates
- Any external model exchange that produces reusable assets

DDNA extraction is forbidden on:
- PS-tagged material unless DCS expressly authorizes
- Sessions explicitly marked Ephemeral by DCS

The 12-step routine cannot be partially run. If a quality gate fails, the routine halts and writes a partial extraction log for DCS review. No partial registry writes are permitted.

---

## 9. Open Questions for QA Pass

These items are flagged for ChatGPT, Gemini, and Claude cross-review during the QA distribution:

1. Does the five-layer model miss any signal class the QA reviewer believes is high value?
2. Is the 12-step routine the right sequence, or should layer extraction parallelize?
3. Should the Use/Make Decision Point itself become a separate doctrine asset, or is it correctly embedded here?
4. Should the asset record schema add fields for cost tracking and time tracking?
5. Is the PS firewall enforcement strict enough at Step 03, or should it be a more granular check at each subsequent step?
6. Should DDNA extraction outputs be versioned independently from their source assets?

---

## 10. Next Actions

1. Distribute this markdown to ChatGPT, Gemini, and NotebookLM for QA review.
2. Run the Neutral Validation Pass (companion file: `DCSE-DDNA-NeutralPass-OCE-Chat-v1-20260515.md`) to test the routine against the source chat.
3. Reconcile QA feedback and produce v2 of this routine.
4. Build the Python implementation following the outline in Section 5.
5. Once Python implementation is verified, build the HTML version of this asset for Admin Members or internal training distribution.

---

**End of DCSE DDNA Extraction Routine v1 Draft**

**Asset trail:** This document itself is now an asset under the schema it defines.
Asset ID: DCSE-DDNA-EXTRACT-ROUTINE-001
Doctrine Flag: yes
Doctrine Asset ID: DCSE-DOCT-DDNA-EXTRACT-001
