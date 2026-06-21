# DCSE Doctrine D16: DDNA Governance

**Document ID:** DCSE-D16  
**Version:** v6.9  
**Created Date/Time:** 2026-06-21T20:00:00-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T20:00:00-04:00  
**Last Version/Release Date/Time:** 2026-06-21T20:00:00-04:00  
**Status:** CANDIDATE  
**Classification:** INTERNAL  
**Lane:** ALL  
**Canonical file:** D16_DDNA_Governance.md  
**Doctrine Description:** The DDNA Governance Doctrine (D16) defines the production pipeline for extracting, classifying, storing, and promoting reusable signals from every DCS session, transcript, build log, and artifact. DDNA (Digital DNA) is the five-layer signal model that captures Sentiment, Logic, Design, Product, and Technical value generated continuously across the DCSE ecosystem. D16 establishes the canonical save destinations for all DDNA output types, the 12-step extraction sequence, the trigger conditions that initiate extraction, the approval gates that govern asset promotion, and the feedback loop that routes DDNA outputs back into the doctrine and product registry. D16 governs what agents produce. D03 governs how agents behave. These are complementary, not overlapping.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)

---

## 1. The Five-Layer DDNA Model

Every DCSE session, transcript, build log, or artifact is a source of structured signal. DDNA is the system that captures that signal before it is lost to undocumented exhaust. The v6+ model captures five layers. No layer is optional. Every extraction run produces output for all five.

### Layer 1 — Sentiment Signals
What DCS sounds like, how DCS thinks, and where the posture is strong or still ramping.

| Signal Category | Examples |
| :--- | :--- |
| Tone | Calm executive, cinematic restraint, no hype, no em dashes |
| Voice posture | CTO-direct, strategic, grounded, useful |
| Confidence signals | Where DCS is certain, where DCS is hedging, where DCS is ramping |
| Friction signals | Where DCS corrects a model, where a model misread direction |
| Learning style | Structured, scaffolded, analogy-driven, Command Post pattern |
| Visual style | Dark base, amber/gold accent, editorial typography, no AI-generated filler |
| Executive readiness | Which fragments are interview-ready, which need rehearsal |
| Public-safe translation | What gets sanitized before any external release |

**Capture rule:** Read directly from DCS's language, corrections, and stated preferences. Do not infer beyond stated evidence.

### Layer 2 — Logic Signals
The workflow, routing, and decision architecture produced during the session.

| Signal Category | Examples |
| :--- | :--- |
| Workflow steps | Intake → outline → source set → studio → output → destination |
| Routing rules | OCE goes through Command Post; PS material stays in PS lane |
| Trigger conditions | When does a chat become an asset; when does a draft become a release candidate |
| Asset definitions | What counts as a parent asset vs a child asset |
| Release gates | Internal Prep, Public-Safe Draft, Needs Sanitation, Ready for DCS Review, Published |
| Model assignments | Which model produces what (Claude for architecture, Gemini for visual audit) |
| QA gates | Source verified, lane correct, PS risk checked, claims verified |
| Decision logs | Use/Make decisions, tool selection rationale, abandoned approaches |

**Capture rule:** Extract from the structural choices made during the session. Every fork in the path is a signal.

### Layer 3 — Design Signals
The visual, structural, and formatting decisions that give DCSE its distinctive presence.

| Signal Category | Examples |
| :--- | :--- |
| Layout patterns | Masthead + module nav + section blocks + footer bar |
| HTML comment discipline | Every CSS block, every section, every functional element commented |
| Color systems | Lane-specific accent colors (gold for learning, rust for accent, teal for verified) |
| Typography pairings | Playfair Display + Source Serif + JetBrains Mono; Syne + Epilogue + JetBrains Mono |
| Icon direction | Radar pulse, circuit path, gear-in-brief, funnel-forward, hex-gate |
| Information hierarchy | Situation intelligence → DCS positioning → executive overview → mapping → enterprise principles |
| Asset badge conventions | DCS-LANE-PRODUCT-INSTANCE-NNN, version, date, PS risk, release status |
| Module interconnection | Cross-link navigation between related assets |

**Capture rule:** Extract from any visual artifact produced — HTML, SVG, diagrams, slide outlines, video direction. The pattern that recurs is the signal worth preserving.

### Layer 4 — Product Signals
The reusable product candidates and asset family relationships emerging from the work.

| Signal Category | Examples |
| :--- | :--- |
| Reusable product candidates | Cram Engine module, NotebookLM video prompt template, 4-module HTML pattern |
| Parent/child asset chains | OCE-001 → OCE-NLM-001 → OCE-NLM-VIDEO-001 → OCE-USECASE-001 |
| Cross-lane reuse | SC consulting use of OCE format; SS storytelling use of cinematic video style |
| Membership content readiness | Which modules are member-gated, which are public-eligible after sanitation |
| Public-safe draft candidates | Sanitized methodology as SC product; agentic teaching video as SS content |
| Template extraction | The cram module structure is a template; the NotebookLM prompt is a template |
| Productization gaps | What is missing before any asset becomes sellable or publishable |

**Capture rule:** Ask three questions of every artifact — can this be reused, can this be templated, can this be sold or distributed.

### Layer 5 — Technical Signals
The automation, scripting, and infrastructure implications of the work.

| Signal Category | Examples |
| :--- | :--- |
| Script automation candidates | DDNA extraction itself, file naming enforcement, registry record writing |
| Connector requirements | NotebookLM upload, Google Drive routing, Command Post asset registration |
| Command Post ingestion | How outputs enter the registry, what metadata is required |
| Registry update logic | When status changes, when version bumps, when archives happen |
| File handling rules | Naming convention enforcement, folder taxonomy, version control |
| HTML builder queue | Which content types need HTML conversion, in what order |
| API touchpoints | Which workflows could use Anthropic API, OpenAI API, Google API |
| Supabase implications | What needs database schema, what needs RLS policies, what is client vs server |

**Capture rule:** Ask what could be automated, what currently requires manual work, and what infrastructure must exist before automation is safe.

---

## 2. Canonical Save Destinations

All DDNA output types have exactly one canonical home within the v6.9 Hub. No DDNA output may be placed outside these paths without a documented exception in `13_Open_Items`.

| Output Type | Canonical Path | Notes |
| :--- | :--- | :--- |
| Signal tables (all 5 layers) | `11_Receipts\DDNA\` | One file per extraction run, timestamped |
| Asset proposals (pending approval) | `13_Open_Items\DDNA_Staging\` | Held here until Level 0 approval |
| Registry records (approved assets) | `02_Registry\DDNA_Assets\` | One file per approved asset |
| DDNA Extraction Summaries | `11_Receipts\DDNA\Summaries\` | Markdown primary; HTML optional for archival |
| Approved assets (promoted) | `07_Projects\[lane]\` | Routed to the correct lane after Level 0 approval |
| Extraction script and tooling | `09_Tools\ddna\` | `dcse_ddna_extraction_v01.py` and successors |
| DDNA Product Matrix | `02_Registry\DDNA_Assets\DCSE_DDNA_PRODUCT_MATRIX.md` | Governed here; not a loose root file |

**Rule:** The extraction script must write to these paths exclusively. Any script that writes outside these destinations without an active STOPGATE exception is non-compliant.

---

## 3. Extraction Trigger Conditions

DDNA extraction is not automatic for every session. The following conditions trigger extraction:

| Trigger | Condition | Who Initiates |
| :--- | :--- | :--- |
| **Manual mark** | DCS marks a session for extraction during or after the session | DCS operator |
| **Asset threshold** | A session produces 3 or more distinct product signal candidates | Agent flags for DCS review |
| **Design artifact produced** | Any HTML, SVG, or visual layout is generated | Auto-trigger at session close |
| **New doctrine contribution** | Any session that modifies a file in `01_Doctrine\` | Auto-trigger, Class A impact |
| **Scheduled sweep** | Weekly pass over `13_Open_Items\DDNA_Staging\` for aged proposals | Command Post daemon |

**PS Risk override:** If PS risk is detected at Step 03 of the extraction routine, extraction halts regardless of trigger condition. The PS portion isolates to the offline Spoke before any further processing.

---

## 4. The 12-Step Extraction Sequence

Every DDNA extraction follows this sequence exactly. No steps are optional. No steps reorder. The canonical implementation lives at `09_Tools\ddna\dcse_ddna_extraction_v01.py`.

```
STEP 01  load_source           → Normalize source; confirm full load
STEP 02  classify_source       → Label source type (chat, build, log, artifact, hybrid)
STEP 03  detect_lane_ps_risk   → Assign lane; run PS risk check; halt if risk > None without DCS auth
STEP 04  extract_sentiment     → Layer 1 signal table
STEP 05  extract_logic         → Layer 2 signal table
STEP 06  extract_design        → Layer 3 signal table
STEP 07  extract_product       → Layer 4 signal table
STEP 08  extract_technical     → Layer 5 signal table
STEP 09  propose_assets        → Generate asset proposals with IDs, parent/child chains, release status
STEP 10  assign_release_status → Apply taxonomy; flag Public-Safe Draft and RC for human review
STEP 11  write_registry_records → Write to 02_Registry\DDNA_Assets\ (approved) or 13_Open_Items\DDNA_Staging\ (pending)
STEP 12  export_summary        → Write summary to 11_Receipts\DDNA\Summaries\
```

**Quality gate at every step:** if the step cannot complete with evidence-backed output, it flags to `13_Open_Items` and halts — it does not estimate or infer.

---

## 5. Release Status Taxonomy

Every asset proposal carries exactly one release status at all times. Status may only advance through human review at the gates marked below.

| Status | Definition | Gate Required |
| :--- | :--- | :--- |
| Internal Prep | Raw signal, not yet reviewed | None |
| Needs Sanitation | Contains information requiring PS scrub before any external use | DCS review |
| Needs Verification | Claims or signals unverified against sources | DCS review |
| Public-Safe Draft | Sanitized and verified; ready for external review | **Level 1 approval** |
| Ready for DCS Review | Complete draft awaiting DCS sign-off | DCS review |
| Release Candidate | DCS-approved; queued for publish | **Level 0 approval** |
| Published | Live on destination (website, Wix, blog, video, etc.) | Post-publish receipt in `11_Receipts` |
| Archive | Superseded or retired; preserved in `10_Archive` | None |
| Blocked | Halted by STOPGATE, PS risk, or missing source | STOPGATE resolution required |

---

## 6. Approval Gates and Promotion Pathway

```
[Signal extracted] → [Asset proposed in 13_Open_Items\DDNA_Staging\]
        ↓
[DCS reviews proposal]
        ↓
[Level 0 approval granted]
        ↓
[Registry record written to 02_Registry\DDNA_Assets\]
        ↓
[Asset routed to 07_Projects\[lane]\ for build]
        ↓
[Build complete → Level 1 review]
        ↓
[Published to destination]
        ↓
[Receipt written to 11_Receipts\]
```

**Level 0 required for:** Release Candidate promotion, any asset that modifies a doctrine file, any asset routed to a public-facing destination (website, Wix store, blog, video platform).

**Level 1 required for:** Public-Safe Draft approval, internal distribution to collaborators.

---

## 7. DDNA Feedback Loop Into Doctrine and Registry

DDNA does not terminate at asset promotion. Extracted signals feed back into the ecosystem:

### 7.1 Product Signal → SC Lane Expansion
When a Product signal identifies a new SC lane product candidate, it triggers the SC lane expansion checklist in D06 Section 10.3 before any build begins.

### 7.2 Technical Signal → D15 or D06 Update
When a Technical signal identifies a new automation opportunity, script, or file path requirement, it creates a Class C or Class D update report per D03 Section 8.2 and routes it to D15 or D06 for doctrine revision.

### 7.3 Design Signal → D09 or D11 Update
When a Design signal identifies a new brand pattern, typography pairing, or layout convention that should become a standard, it routes to D09 (Brand Identity) or D11 (HTML/Wix) for incorporation.

### 7.4 Sentiment Signal → D08 Update
When a Sentiment signal identifies a new voice rule, forbidden phrase, or tone correction, it routes to D08 (Voice and Tone) with a diff logged to `12_Diffs`.

### 7.5 Logic Signal → D03 Update
When a Logic signal identifies a new workflow step, model assignment, or routing rule, it creates a Class A update report per D03 Section 8.2.

---

## 8. Asset Naming Convention

All DDNA-produced assets follow this naming schema:

```
DCS-[LANE]-[PRODUCT]-[INSTANCE]-[NNN]
```

| Field | Values |
| :--- | :--- |
| LANE | SC, SS, PS, DCSE, EMP, CROSS |
| PRODUCT | CTJ, TSL, GOVOS, OCE, SJL, or custom product code |
| INSTANCE | HTML, VIDEO, AUDIO, BLOG, EMAIL, RESUME, DB, REPORT |
| NNN | Zero-padded sequence number (001, 002, etc.) |

Every asset record also carries: version, created date, PS risk score, release status, and the extraction run ID that produced it.

---

## 9. Session-Close DDNA Check

At the close of every session (D03 Section 6, Phase 5), the active agent runs a DDNA surface check:

```
1. Did this session produce any design artifacts?          → Flag for Layer 3 extraction
2. Did this session modify any doctrine file?              → Auto-trigger extraction; Class A report
3. Did this session generate 3+ product signal candidates? → Flag for DCS review
4. Did this session produce any new automation candidates? → Flag for Layer 5 extraction
5. Did any output drift from DDNA voice or brand posture?  → Log to 13_Open_Items for correction
```

If any flag is raised, the agent writes a DDNA Surface Notice to `05_Tribunal_Inbox` before the session closes.

---

## Related Doctrine

- [D01_Forward_Thinking.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D01_Forward_Thinking.md) - Forward posture enforced in Sentiment signal capture
- [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) - Section 7 governs DDNA mindset enforcement; Section 8 governs update classification
- [D05_Baseline_Promotion.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D05_Baseline_Promotion.md) - Release Candidate promotion aligns with baseline promotion gates
- [D06_File_System.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D06_File_System.md) - All canonical save paths in Section 2 are governed by D06 routing rules
- [D08_Voice_Tone.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D08_Voice_Tone.md) - Sentiment signal feedback destination
- [D09_Brand_Identity.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D09_Brand_Identity.md) - Design signal feedback destination
- [D11_HTML_Wix_App.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D11_HTML_Wix_App.md) - Design signal feedback destination for HTML/Wix patterns
- [D15_Database_Administration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D15_Database_Administration.md) - Technical signal feedback destination for Supabase and schema changes

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.
