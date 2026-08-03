# DCSE Doctrine D13: DART Core (Discovery, Attack, Rebuttal, Trial)

**Document ID:** DCSE-D13  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T19:27:00-04:00
**Last Version/Release Date/Time:** 2026-06-21T15:22:37-04:00  
**Status:** DCSE Authorized version Pending Approval  
**Classification:** PS-PROTECTED  
**Lane:** PS  
**Canonical file:** D13_DART_Core.md  
**Doctrine Description:** The DART Core Doctrine (D13) defines the structured litigation-support phases (Discovery, Attack, Rebuttal, Trial) and quality check gates. It establishes the ESI-first discovery norms, deficiency tracking criteria, and the Discovery Evolution Matrix (DEM) schema. The doctrine enforces rigorous self-check quality gates to guarantee Bates range validation and evidentiary tracing.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. DART Core Architecture & Phases

The DART framework organizes litigation support into four distinct phases, ensuring absolute rigor and evidentiary verification.

### 1.1 Discovery Phase
- **ESI-First Discovery Norms**: Enforce rigorous data requests mapping:
  - **Custodians**: Decision-makers and liaisons.
  - **Systems of Record**: Active software platforms (Outlook, Teams, SharePoint, Jira, Procurement databases).
  - **Search Terms**: Validated keywords defined per case in the companion PS-Protected file (see [D14_DART_PS_Protected.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D14_DART_PS_Protected.md) Section 1).
  - **Formats**: Mandatory native format productions with complete metadata.
  - **Milestones**: Weekly rolling production schedules.
  - **Withholding Rules**: Enforce FRCP Rule 34(b)(2)(C) withholding statements and Rule 26(b)(5) privilege logs.
- **Discovery deficiency tracking**: Trigger a deficiency flag if a party uses boilerplate objections, fails to certify diligent search, or yields empty interim responses across two or more rounds.

### 1.2 Attack Phase
- **Rule A1 (Motion to Compel)**: Draft a Motion to Compel (MTC) within 48 hours of detecting a persistent discovery deficiency.
- **Rule A2 (New Objections)**: If a party asserts a new objection without showing burden particulars, auto-draft a Supplemental RFP/ROG demanding custodians, systems, and date ranges.
- **Rule A3 (Contradictions)**: Flag inconsistent responses between RFPs, ROGs, and RFAs for trial impeachment.
- **Rule A4 (Decision-Maker Mapping)**: Identify and flag named actors for deposition outlines.
- **Rule A5 (Comparator Analytics)**: Log differential treatment records (pay, overtime, assignments) into the Comparator Matrix (Name, Race, Title, Treatment, Pretext Score).
- **Rule A6 (Shift to Admission)**: Pin shifts from denial to admission for judicial notice.

### 1.3 Rebuttal Phase
- Proactively counter standard defense objections using McDonnell Douglas burden-shifting standards:
  - *Unduly Burdensome*: Propose a narrowed scope (specific custodians, systems, dates) referencing EEOC and Lyoch/Turner precedent.
  - *Relevance*: Anchor requests directly to motive using comparator evidence and decision-maker communications.
  - *Privilege*: Demand a Rule 26(b)(5) privilege log within 14 days; failure to produce constitutes waiver.
  - *Possession*: Demand agency-controlled vendor data, requiring Rule 34 certification of diligent search.
- Anchor all rebuttal points to authenticated Bates-numbered exhibits and chronologies.

### 1.4 Trial Phase
- **Rule T1 (Exhibit Flow)**: Map exhibits to witness order and impeachment triggers.
- **Rule T2 (Binder Metadata)**: Index all binders, tagging exhibits with DART hashes.
- **Rule T3 (Mock Cross-Exams)**: Synthesize deposition admissions for witness scripting.
- **Rule T4 (PS/TI Synchronization)**: Strip case-specific facts to archive; derive generalized civil-rights lessons for TI.

---

## 2. Discovery Evolution Matrix (DEM)

All discovery requests must be tracked within the DEM layout:

`Request ID | Category | Round 1 (Status + Bates) | Round 2 | Round 3 | Current Tag(s) | Attack Actions | Rebuttal Points | SJ Nexus | Trial Nexus`

### 2.1 Response Evolution Tags
- **Unchanged**: Content identical across rounds.
- **Newly Answered**: Substantive answer appears where none existed.
- **Amended Response**: Text modified; adds Bates ranges or narrative detail.
- **New Objection**: Objection appears that was not previously asserted.
- **Objection Withdrawn**: Prior objection removed or narrowed.
- **Contradictory**: Conflicting factual assertions across rounds.
- **Persistent Deficiency**: Two or more rounds without a substantive response.

---

## 3. DART Processing Quality Gates (Self-Checks)

Every DART analysis or document draft must clear the 8 Quality Gates:
1. **Chain-of-Thought**: Model must document its logic step-by-step before drafting.
2. **Verifier Pattern**: Pose clarifying questions regarding gaps before proceeding.
3. **Fact Verification**: Trace every fact to Bates-numbered evidence; citation accuracy is non-negotiable.
4. **Legal Authority Validation**: Precedent holdings must be verified with subsequent history checks.
5. **Metadata Compliance**: Hash all deliverables using SHA-256 signatures.
6. **Bates Range Validation**: Sequence check all production ranges and flag gaps.
7. **Privilege Log Audit**: Verify FRCP 26(b)(5) compliance of defense privilege logs.
8. **Duplication Detection**: Scan logic outputs against prior versions to merge redundancies.

---

## Related Doctrine

- [D14_DART_PS_Protected.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D14_DART_PS_Protected.md) - Case-specific parameters, custodians, search terms, and litigation blueprints
- [D02_Forward_Backward_Chaining.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D02_Forward_Backward_Chaining.md) - Chaining logic applied to DART quality gates

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.

