# DCSE Doctrine D21: Doctrine Runtime Engine

**Document ID:** DCSE-D21
**Version:** v6.9
**Created Date/Time:** 2026-07-25T23:00:00-04:00
**Last Doc Modified Date/Time:** 2026-07-25T23:00:00-04:00
**Status:** DCSE Authorized Pending DCS Approval
**Classification:** INTERNAL
**Lane:** DCSE/ALL
**Canonical file:** D21_Doctrine_Runtime_Engine.md
**Doctrine Description:** The Doctrine Runtime Engine (D21) defines two automation mechanisms that govern how doctrine files are selected and audited during task execution: the Dynamic Doctrine Router (DDR) for automated doctrine selection based on task characteristics, and the Doctrine Consideration Log (DCL) for auditable tracking of which doctrines were loaded, applied, excluded, or missing during every substantive output. D21 also defines the Model Capability Watch protocol for detecting when AI model feature changes require doctrine re-evaluation, and the Cybersecurity Baseline that all outputs must clear.
**Parent Document:** DCSE_Master_Profile_v6.9_RC2.md

---

## 1. Purpose

Static doctrine assignment (hardcoded lists of which files apply to which tasks) breaks every time a new doctrine is created, an existing one is deprecated, or a model gains new capabilities. D21 replaces static assignment with two runtime mechanisms:

1. The Dynamic Doctrine Router (DDR) selects applicable doctrines per task.
2. The Doctrine Consideration Log (DCL) records what was selected and why.

Together they make doctrine selection self-maintaining and every output auditable.

---

## 2. Dynamic Doctrine Router (DDR)

### 2.1 Task Declaration

Every substantive task begins with a Task Declaration containing:

- Task Type: build, media, visual, campaign, analysis, employment, legal, governance, infrastructure
- Entity Scope: SC, SS, TI, PS, DCS, DCSE
- Model Tier: 1 (Sovereign), 2 (Internal Collaborator), 3 (External Product Build)
- Capability Profile: list of model capabilities active for this session (text generation, code execution, vision, tool use, web access, file system access, database access)

If the task declaration is implicit (user did not explicitly state all fields), the model infers from context and records the inference in the DCL.

### 2.2 Routing Logic

The DDR evaluates the Task Declaration against doctrine metadata in `dcse_asset_registry`:

1. Query all doctrines where `lifecycle_status = 'Active'` and `asset_type IN ('doctrine', 'methodology')`.
2. Filter by `entity_lane`: include doctrines matching the task entity scope, plus lane "ALL" and lane "DCSE".
3. Filter by tier: exclude doctrines above the model's authorized tier per DCSE_Doctrine_Access_Tiers_v6.9.md.
4. Filter by firewall: exclude PS-Locked doctrines unless PS mode is declared.
5. Match by topic: compare task type against doctrine `topic` field. Match rules:
   - Task type "media" matches topics: media-production, video, audio, visual-creation
   - Task type "build" matches topics: product-assembly, html-wix-app, baseline-promotion
   - Task type "visual" matches topics: visual-creation, brand-identity, media-production
   - Task type "campaign" matches topics: campaign-governance, voice-tone, brand-identity, persona-assets
   - Task type "analysis" matches topics: dart-universal, forward-thinking, forward-backward-chaining
   - Task type "employment" matches topics: dart-universal, brand-identity, voice-tone
   - Task type "governance" matches topics: all non-PS doctrines
   - Task type "infrastructure" matches topics: file-system, database-administration, command-post, ai-orchestration
6. Check for methodology triggers: scan task content for trigger keywords defined in each methodology doctrine (D17 DART triggers, D18 media triggers, D19 visual triggers, D20 product assembly triggers).
7. Return the Doctrine Set: the filtered, matched list of doctrines the model should load and apply.

### 2.3 Always-Loaded Doctrines

Regardless of task type, the following are always in scope for Tier 1 models:

- DCSE_Master_Profile_v6.9_RC2.md (constitutional authority)
- D21_Doctrine_Runtime_Engine.md (this file; governs the routing itself)
- DCSE_Doctrine_Index_v6.9.md (canonical index)

For Tier 2: Master Profile (redacted) and Doctrine Index (redacted).
For Tier 3: Product Build Extract only.

### 2.4 New Doctrine Auto-Discovery

When a new doctrine is registered in `dcse_asset_registry` with `lifecycle_status = 'Active'` and a populated `topic` field, the DDR automatically includes it in future routing without requiring instruction updates. This is the core automation benefit: register once, route everywhere.

---

## 3. Doctrine Consideration Log (DCL)

### 3.1 DCL Format

Every substantive task output must include a DCL block (machine-readable, appended to output or stored in Supabase). The DCL contains:

```
DCL_START
  task_id: [auto-generated or user-provided]
  task_type: [from Task Declaration]
  entity_scope: [from Task Declaration]
  model_id: [executing model name and version]
  model_tier: [1, 2, or 3]
  timestamp: [ISO 8601]

  LOADED:
    - [doctrine_id]: [file_name] — [reason loaded]

  APPLIED:
    - [doctrine_id]: [file_name] — [specific sections/rules applied]

  EVALUATED_NOT_APPLIED:
    - [doctrine_id]: [file_name] — [reason not applied: wrong entity, wrong task type, not relevant]

  EXCLUDED_BY_TIER:
    - [doctrine_id]: [file_name] — [tier restriction]

  EXCLUDED_BY_FIREWALL:
    - [doctrine_id]: [file_name] — [firewall rule: PS-Locked, PPR-Protected]

  GAPS_DETECTED:
    - [description of guidance needed but no doctrine covers it]

  METHODOLOGY_TRIGGERS:
    - [methodology_id]: [trigger type: explicit/skill/implicit] — [trigger evidence]

  CYBERSECURITY_CLEARANCE:
    - secrets_scan: [PASS/FAIL]
    - input_validation: [PASS/FAIL/NA]
    - output_sanitization: [PASS/FAIL/NA]
    - cors_compliance: [PASS/FAIL/NA]
    - credential_exposure: [PASS/FAIL]
DCL_END
```

### 3.2 DCL Storage

- For Claude Code sessions: DCL is written to `05_Tribunal_Inbox` as a JSON file when the task involves file creation, product build, or governance changes.
- For Chat/Cowork sessions: DCL is appended as a collapsed block at the end of the response.
- For Tier 2/3 models: DCL is returned as part of the output for Tier 1 models to ingest and store.
- All DCLs are registered in `dcse_asset_registry` with `asset_type: 'dcl'`.

### 3.3 Gap Escalation

When GAPS_DETECTED is non-empty, the model must:

1. Log the gap in the DCL.
2. Announce: "Doctrine gap detected: [description]. No current doctrine covers this requirement."
3. If the gap is recurring (detected in 3+ tasks), flag for new doctrine creation.

---

## 4. Model Capability Watch (MCW)

### 4.1 Capability Registry

Each model's known capabilities are tracked in `dcse_asset_registry` with `asset_type: 'model_capability_profile'`:

- Model name and version
- Capabilities: text generation, code execution, vision, audio processing, tool use, web browsing, file system access, database access, image generation, video generation
- Capability version date (when the capability was confirmed)
- Doctrine implications (which doctrines are affected by this capability)

### 4.2 Capability Change Detection

When a model detects it has a capability not listed in its capability profile (new tool, new modality, new API access), it must:

1. Log a Capability Change Event in the DCL.
2. Run a Heuristic QA check (per Qwen instructions): does the new capability conflict with any doctrine assumption?
3. If conflict detected: halt the capability use and flag for DCS review.
4. If no conflict: proceed but log the new capability for profile update.

### 4.3 Doctrine Capability Requirements

Doctrine files in `dcse_asset_registry` may include a `capability_requirements` field listing which model capabilities they assume:

- D18 (Media Production Pipeline) requires: text generation, tool use (for storyboard generation)
- D19 (Visual Creation Pipeline) requires: text generation, image generation knowledge (prompt engineering)
- D20 (Product Assembly) requires: code execution, file system access, web browsing (for live preview)
- D11 (HTML/Wix/App) requires: code execution, web browsing
- D15 (Database Administration) requires: database access

The DDR cross-references task capabilities against doctrine requirements. If a model lacks a required capability, the doctrine is loaded as reference-only (rules apply but the model cannot execute the methodology phases itself).

---

## 5. Cybersecurity Baseline

Every output processed through the Doctrine Runtime Engine must clear the following cybersecurity checks. These are integrated into the DCL as the CYBERSECURITY_CLEARANCE block.

### 5.1 Secrets Scan (All Outputs)

Before any output is delivered, committed, or published:

- Scan for API keys, tokens, passwords, connection strings, and Supabase project credentials.
- Scan for private file paths that reveal system architecture to unauthorized tiers.
- If detected: HALT delivery. Redact the secret. Log the detection in the DCL.
- Zero tolerance: no output may contain a secret, even in code comments or debug output.

### 5.2 Input Validation (Build Outputs)

For any product, app, or HTML output:

- All user-facing inputs must be validated at the boundary (type, length, format).
- All rendered content must be sanitized against XSS (escape HTML entities, sanitize URLs).
- SQL queries must use parameterized statements; no string concatenation of user input.
- File uploads must validate type, size, and content before processing.

### 5.3 Output Sanitization (Public-Facing Outputs)

For any output destined for public channels (web, email, social, video metadata):

- Strip internal metadata (doctrine IDs, Tribunal references, Command Post labels).
- Strip entity-internal references that violate the entity firewall.
- Verify GYTO suppression for public-facing content.
- Verify PS content suppression for non-PS channels.

### 5.4 CORS and Transport (Web Outputs)

For any web application or API endpoint:

- CORS policies must be explicit and restrictive. No wildcard origins in production.
- All API calls must go through backend mediation. No direct database calls from client-side code.
- HTTPS required for all production endpoints.
- Content Security Policy headers required for all HTML pages.

### 5.5 Credential Isolation (Infrastructure Outputs)

- Public-safe anonymous keys only in browser-facing code.
- Service role keys only in server-side code, never in client bundles.
- Environment variables containing secrets must not be logged, committed, or exposed in error messages.
- Pre-commit hooks must scan for credential patterns before any Git push.

### 5.6 Cybersecurity Escalation

If any cybersecurity check fails:

1. HALT the output.
2. Log the failure in the DCL with the specific check that failed.
3. Remediate: fix the vulnerability before re-attempting delivery.
4. If remediation is not possible within the current session, flag for DCS review and do not deliver the output.

---

## 6. Live Preview Mandate

### 6.1 Non-Negotiable First-Contact Standard

Any product, app, or HTML output that can be rendered in a browser MUST pass a live preview before being reported as complete. "It compiles" or "tests pass" is not sufficient. The output must survive first human contact.

### 6.2 Preview Protocol

1. Start the dev server or open the output in a browser preview.
2. Verify the golden path renders correctly (primary user flow works end-to-end).
3. Check for console errors, network failures, and rendering issues.
4. Verify responsive layout at mobile, tablet, and desktop breakpoints.
5. Verify brand compliance (correct colors, fonts, entity voice).
6. Verify cybersecurity baseline (no secrets in client code, no XSS vectors, proper CORS).
7. Capture a screenshot or proof of successful preview.
8. If any check fails: fix before reporting complete.

### 6.3 Preview Exceptions

Live preview is not required when:

- The output is a governance document, doctrine file, or metadata record.
- The output is a backend-only script with no browser-facing component.
- The output is a database migration or schema change (verify via query, not preview).
- The dev server infrastructure does not exist yet (flag this as a gap in the DCL).

### 6.4 Preview Logging

Preview results are logged in the DCL under a PREVIEW_RESULT block:

```
PREVIEW_RESULT:
  preview_type: [dev-server/static-file/browser-preview]
  golden_path: [PASS/FAIL — description]
  console_errors: [PASS/FAIL — count and description]
  responsive: [PASS/FAIL — breakpoints tested]
  brand_compliance: [PASS/FAIL — issues found]
  cybersecurity: [PASS/FAIL — checks run]
  screenshot_captured: [true/false]
  overall: [PASS/FAIL]
```

---

## 7. DCSE Doctrine Replacement Protocol

### 7.1 Doctrine Supersession

When a doctrine is replaced (new version or restructured into a different document number):

1. The old doctrine's `lifecycle_status` is set to `Deprecated` in `dcse_asset_registry`.
2. The new doctrine's registry entry includes a `supersedes` field pointing to the old document ID.
3. The DDR automatically routes to the new doctrine. Models that cached the old doctrine will pick up the replacement on their next DDR query.
4. The DCL logs the supersession event: "D[old] superseded by D[new] as of [date]."

### 7.2 Instruction Set Impact

When new doctrines are created or existing ones restructured:

- CLAUDE.md auto-loads and references the doctrine stack. Add new methodology doctrines to the stack list.
- Claude Chat/Cowork, Qwen, Codex/ChatGPT instructions reference doctrine by number. Update the DART section pattern to include new methodology sections.
- Tier 3 Product Build Extract may need a new section if the methodology has external-safe content.

The DDR handles runtime routing automatically. Instruction updates are needed only for the static reference lists in custom instructions.

---

## 8. Trigger Mechanism (D21-Specific)

D21 activates automatically on every substantive task. It does not require explicit invocation.

The DDR runs before task execution. The DCL runs during and after task execution. The MCW runs when capability changes are detected. The Cybersecurity Baseline runs before output delivery. The Live Preview Mandate runs before any browser-renderable output is reported complete.

No model may skip D21 processing. If a model cannot execute the full DCL (Tier 3 models with no structured output capability), it must at minimum declare which doctrines it applied in plain text at the end of its output.

---

## 9. Tier Access

| Tier | D21 Access |
|---|---|
| Tier 1 Sovereign | Full DDR, DCL, MCW, Cybersecurity, Live Preview. Write DCLs to Supabase. |
| Tier 2 Internal Collaborator | DDR routing (read-only from Supabase). DCL output in response. Cybersecurity checks required. Live Preview required for build outputs. |
| Tier 3 External Product Build | No DDR access. Must declare applied rules in plain text. Cybersecurity checks are the responsibility of the Tier 1 model that reviews the output. |

---

## Related Doctrine

- DCSE_Doctrine_Access_Tiers_v6.9.md — Tier definitions that the DDR enforces
- DCSE_Runtime_Access_Map_v6.9.md — Runtime access architecture the DDR extends
- D03_AI_Orchestration.md — Agent write-path permissions referenced by DDR
- D17_DART_Universal_Methodology.md — First methodology doctrine with trigger mechanism pattern
- D18_Media_Production_Pipeline.md — Media methodology routed by DDR
- D19_Visual_Creation_Pipeline.md — Visual methodology routed by DDR
- D20_Product_Assembly_Methodology.md — Product assembly methodology routed by DDR

---

## Error-Catch Protocol

If this doctrine file is missing or unreadable, follow the canonical error-catch protocol:
1. HALT execution. Do not infer DDR/DCL rules from pre-training.
2. LOG `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. TRIGGER STOPGATE and alert the user.
4. FALLBACK: If D21 is unavailable, models must manually declare which doctrines they applied (static fallback). The DDR automation is suspended until D21 is restored.
