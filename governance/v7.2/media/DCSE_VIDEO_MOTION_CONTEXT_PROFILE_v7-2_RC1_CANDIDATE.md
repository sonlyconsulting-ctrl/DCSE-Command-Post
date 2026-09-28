# DCSE Video & Motion Context Profile (VMCP) v7.2 | RC1 Candidate

**Artifact ID:** DCSE-VMCP-v7.2-RC1-CANDIDATE  
**Artifact class:** Task-family governance context-profile template, NOT an independent enterprise Master Profile or a precompiled executable controller  
**Task ID:** DCSE-V72-VIDEO-MOTION-CONTEXT-PROFILE-20260919-01  
**Date:** 2026-09-19  
**Classification:** INTERNAL. External model/maker distribution requires a separately approved sanitized task packet.  
**Lane / scope:** DCSE governance of approved SC video and motion production. Extend to SS or TI only under independently verified entity, channel, role and source profile. PS/PPR are excluded from this shared profile.  
**Authority:** DCS Level 0. Proposed model-neutral operating profile derived from operative v7.2 R5 authority and currently applicable approved doctrines; does not create authority.  
**Lifecycle:** REVIEW CANDIDATE / UNSYNCHRONIZED to any independent runtime or registry until confirmed.  
**Parent controller:** `governance/v7.2/DCSE_MASTER_PROFILE_v7_2_R5_FINAL.md`; verify with `governance/v7.2/DCSE_Master_Profile_Authority_Synchronization_v7-2.md` and operative designation. The controller file's embedded CANDIDATE build label is historic and later authority-synchronization record expressly designates R5 operative.  
**Source anchors:** R5 §§1.2–1.3 (minimum effective packet/closure), §8 (authority/conflict resolution), §18 (model/runtime distinction), §23 (fail-closed compiler); D22 source/access/distribution; D21 task routing/preflight/DCL/evidence; D03 capability-based delegation; D05 approval/promotion; D09 brand; D12 video; D18 media pipeline; D19 visual pipeline; D06/shared media asset standard as routed.  
**Related pending proposals:** Brand-ident rules in PR #158 and six-doctrine review candidates in PR #159 are PROPOSED, not silently operative merely because referenced here. The direct DCS 2026-09-19 creative instruction authorizes preparation of 6–8s ident briefs in its stated scope; this does not automatically approve external publication or doctrine promotion.

## 0. Naming, role, and scope

This profile is called **VMCP, Video & Motion Context Profile**. It is a compact, model-neutral task-family projection **under** the DCSE Master Profile, not a competing constitutional controller, generic video Gem persona, brand-style bible, or standalone model prompt. It defines required routing/controls common to video and motion work, including 6–8s brand idents, product demonstrations, narrated explainers, campaign clips, video/audio derivatives and format-specific exports.

Every execution obtains a **task-specific runtime context packet** compiled from verified current authority and actual production scope. This template alone is not that packet: it does not contain the task's exact controller hash, dependency closure, operative doctrine identities and hashes, lane-specific stop-gates, permissions, brand assets or signed maker selection. No executor may claim “full v7.2 loaded,” autonomous task admission, public release, or model permission by possessing this file.

**Identity:** Logical participant/role, model backend, runtime surface, runtime instance, and tool capability are separate fields. “Qwen,” “Gemini,” or “Jim” are participant labels only until mapped to verified execution identities and real capabilities. The earlier “Jim” label was unverified dictation; do not treat it as a third participant. Qwen and Gemini are model/provider labels, not authority or demonstrated media capability.

## 1. Mandatory controller header for every video task

The task-specific compiler or designated Command Post governance lead SHALL resolve and attach:

- Current operative Master Profile reference, operative designation, artifact hash, controlling later DCS directives, and v7.2 package/manifest version.
- The exact task ID and responsible SC/SS/TI entity, business lane, classification, product/brand identity, audience, distribution channels, allowed use and proposed outcome.
- D22-verified canonical source/version/hash and available evidence locations. GitHub stores governance/control; authorized object storage holds video/audio and larger image binaries; Tribunal stores decisions/validation, not automatic authority.
- Applicable stop-gates, lane protection, access/secret rules, reserved approvals, rollback/recovery, deliverables and acceptance criteria.
- The minimum effective doctrine set, including dependency closure and any unresolved normative conflict with a DCS disposition reference. Do not choose a supposedly “stronger” rule by intuition or erase a conflicting historical source.
- Compiled packet identity, rule IDs/inclusion reasons, authority references, rule-set hash and readback/evidence path retained in the control plane.

**Fail closed on control omissions:** Unknown controlling authority, unresolved required dependency, unknown lane/protected exposure, missing access classification, unapproved public release or unresolved PS-origin material blocks the affected action. Safe source identification, planning and non-public candidate work may continue only when independently authorized and properly isolated. Presence of this file, model memory, a task description or a GitHub commit never cures a missing gate.

## 2. Mandatory preflight declaration

For every substantive production, record:

```yaml
video_preflight:
  task_id: "REQUIRED"
  parent_or_product_task: "REQUIRED_IF_APPLICABLE"
  entity_lane: "REQUIRED"
  classification_and_external_sharing: "REQUIRED"
  destination_and_channel: "REQUIRED"
  outcome_and_format: "BRAND_IDENT | EXPLAINER | CAMPAIGN | DEMO | OTHER"
  source_identity_and_version: "REQUIRED"
  canonical_asset_uri_and_sha256: "REQUIRED_OR_ACCESS_PENDING"
  source_rights_and_approved_uses: "VERIFIED_OR_RIGHTS_PENDING"
  target_duration_aspect_fps_resolution: "REQUIRED"
  model_or_maker_capability_and_access: "VERIFIED_OR_UNASSIGNED"
  audio_and_likeness_permissions: "REQUIRED_IF_APPLICABLE"
  task_authority_and_approval: "REQUIRED"
  secret_ps_and_cross_lane_exposure: "NONE | IDENTIFIED_AND_ISOLATED"
  evidence_destination: "REQUIRED"
  required_deliverables_and_exit_tests: "REQUIRED"
  rollback_or_source_recovery: "REQUIRED_IF_APPLICABLE"
  execution_state: "PREFLIGHT | BRIEF_ONLY | PRODUCTION_PENDING | BLOCKED"
```

A tool/model may propose options with source pending but SHALL NOT fabricate approved asset retrieval, licensing, existing video, 4K native output, authorization or renderer availability. Resolve the actual source binary before a *source-faithful* candidate render or final compositor pass. Missing current-chat image is `ACCESS_PENDING`, not a global absence finding.

## 3. Task-routed doctrine map

- **Always for substantive governed work:** Master Profile/operative designation, D22, D21 and applicable participant onboarding, controller-header controls, authority/evidence/stop-gates.
- **Delegation or multi-model sequence:** D03 with actual capability/access matrix. One model's identity does not grant another model's permissions.
- **Any video/motion/audio:** D12 governance, D18 execution methodology, D09 brand profile/controlled terms/rights, D06 and shared media asset standard where asset access or persistence is involved.
- **Images, logo compositing, icons or new visual derivatives:** D19. Use original approved source art for exact logo/end-plate work and distinguish design exploration from deterministic edits.
- **Campaign/public content:** D07/D08/D10 as relevant, actual public factual-claim/rights checks, product/name/price/CTA verification, DCS approval.
- **Website, application embedding, autoplay/performance/accessible playback:** D11 and verified platform adapter. A doctrine filename mentioning Wix does NOT route CTJ through Wix.
- **Product assembly/checkout/access inclusion:** D20 and product manifest, and applicable authenticated/commerce governance. A logo-ident task does not imply permission to change payment systems.
- **Promotion/public release/asset lifecycle:** D05, D04, D22, explicit reserved DCS decision and downstream runtime evidence. PS and protected controls cannot be exported to public or third-party creative contexts.

D09/D11/D12/D18/D19/D07 RC1 files in PR #159 are review candidates. If used for scenario testing, label every candidate-only rule as **proposed** and do not describe an unmerged candidate as operative. If a source conflicts, record and resolve authority rather than silently consolidating.

## 4. Governed production sequence and handoffs

A default seven-stage **logical sequence**, not a permanent vendor order:

| Stage | Functional owner | Input -> controlled output | Pass / stop rule |
| --- | --- | --- | --- |
| **0. Intake + authority** | Command Post governance lead | Task, lane, source and protected/external-sharing check -> signed production envelope | Missing mandatory control blocks affected work; no unauthorized external upload. |
| **1. Source + concept** | Researcher/creative architect | Actual approved brand/profile/source binary, audience, one-sentence motion logic -> source inventory + concept + variants | No invented logo, new title, mark or source-fidelity claim. |
| **2. Challenge + storyboard** | Storyboard planner / challenger | Competing motion interpretations and risks -> selected narrative, shot/timecode structure, negative prompts and maker handoff | Purposeful motion must visibly represent claimed logical transformation, not generic sparkle. |
| **3. Motion generation** | Authorized renderer(s) | Source-appropriate image-to-video or scene prompts -> candidate video files, render settings, source/model IDs | A prompt or render request is not a playable video; record actual bytes or `RENDER_PENDING`. |
| **4. Controlled edit + sound** | Editor/compositor | Candidate shots + original artwork -> exact duration, final protected static logo plate, licensed audio, silent and reduced-motion/static variants | Where AI distorts text or mark, replace with verified original composite; no false “unchanged” claim. |
| **5. Independent validation + repair** | Validator meeting applicable independence rule | Actual binary, source, provenance -> timecoded findings and targeted fixes/retest; source and derivative checksums | Executing maker's self-review alone does not meet an explicit independent-validator requirement; unresolved failure stays PARTIAL. |
| **6. DCS decision + release** | DCS Level 0, then authorized distributor | Reviewed master, rights, formats and Tribunal receipt -> approval/rejection, then separately verified authorized distribution | Existence/commit/approval of a static logo does not approve a motion derivative; no automatic publication. |

**Backward check:** For each requested property, identify exact final evidence: conceptual movement in real frames, name/tagline exactness, approved-source end plate, measured clip duration, true aspect and resolution provenance, audio/rights, actual final-file retrieval, mobile and reduced-motion behavior where placed, review decision. If the property is unobserved, do not declare it passed.

## 5. Multi-model production topology and sequence experiment

**Stage assignment SHALL be by verified tool capability, source control, confidentiality eligibility, execution environment, cost/latency and evidence.** A participant may fill more than one compatible creative role; separately mandated actor-independent validation stays separate. Producer, editor, validator and DCS release approver remain distinct *functions*, even if an authorized participant spans nonconflicting production functions.

The **Qwen / Gemini** sequence is OPEN and does not create role seniority. Run a bounded two-variant pilot on the **same** approved CTJ Unified source and identical seven-second acceptance contract, with all intermediate artifacts retained:

- **Pilot A:** Qwen, if source access and storyboard capability are verified, creates concept alternatives, visual logic and exact shot plan; Gemini or another eligible renderer generates motion; a capable editor/compositor performs protected identity end plate; a distinct qualified reviewer challenges the actual result; DCS decides.
- **Pilot B:** Gemini, if capable, first creates concept and preliminary motion/storyboard; Qwen or another eligible participant challenges narrative and improves a second motion/visual version; capable editor/compositor finalizes the source-faithful plate; distinct validator tests; DCS decides.
- **Single-provider fallback:** One eligible tool renders and edits under explicit bounded authority, with mandatory source comparison and independently routed validation where required. If neither can render, create the prompt, storyboard and handoff while labeling `PRODUCTION_PENDING`.

Evaluate *evidence*, not an assumed model hierarchy: storyboard logic, fidelity to exact brand source/wordmark/trademark, number and severity of defects, time to a verified final master, tool availability, licensing/privacy, cost, rework, editor handoff continuity and DCS's explicit creative acceptance. Keep original and final frames and timecoded notes. Do not designate a permanent Qwen-first or Gemini-first pipeline until the pilot receipt and DCS sequence decision exist. "Gemini finalizes" can mean edit/compositing, not the reserved final release approval. The earlier “Jim” was an unverified dictation artifact and is not a separate maker assignment.

A later change to the preferred tool or model is a capability-routing/profile revision, not a constitutional amendment, unless authority or lane/firewall rules change.

## 6. Format profiles and seven-second CTJ test case

**Short brand-motion ident:** DCS's current creative directive requests 6–8 seconds illustrating a brand's logical concept. A short non-narrated ident uses `ORIGIN -> LOGICAL TRANSFORMATION -> EXACT IDENTITY RESOLUTION/HOLD`, rather than artificially imposing a 30–45-second educational body, voiceover or CTA. Preserve exact approved logo and product attribution. Existing identities without rendered idents go to tracked backlog, not retroactive invented completion or automatic unrelated-release invalidation. The formal reusable D12/D18 amendment remains under PR #158 until approved.

**CTJ Unified initial pilot:** Task ID `SC-CTJ-UNIFIED-BRAND-IDENT-20260919-01`. Separate paths through visible labyrinth corridors -> purposeful convergence -> compass alignment -> latest DCS-designated CTJ Unified 16:9 artwork held sharp and stationary for the final 1.5–1.6s. The first-line top tagline remains deleted. The single `CLARITY • PERSPECTIVE • ACTION` tagline remains below `The Unified Path`. Do not introduce an “Executive Suite” name; do not invent a source logo if latest version cannot be retrieved and byte/hash verified. Keep original approved icon/parent-family lockup distinct from the product hero/Unified mark. Source-image hash/rights and exact storage retrieval are still production preconditions, not inferred from a chat thumbnail or PR.

**Technical target:** 7.0 s exact final runtime, exact 16:9, 3840×2160 target master where supported, 24 or 30 fps, native-vs-upscaled provenance, H.264/H.265 MP4 or approved platform format, optional rights-cleared sound plus silent version; reduced-motion/static alternative for autoplay/embed as relevant. Clip length, codec, frame rate, dimensions, text, end-hold duration, edge/flash safety and playback must be checked on the actual deliverable. Do not promise a renderer supports seven-second 4K just because the prompt requests it.

**Other formats:** Campaign explainer, narrated instruction, web product preview, vertical social or long form SHALL declare its own approved duration/audio/CTA/shot and distribution profile. The short-ident exception never silently rewrites educational, documentary or public-claim constraints.

## 7. External maker/Gem knowledge boundary

**Do not upload this full INTERNAL profile or the complete Master Profile/Tribunal/manifest/credentials to an external Gem by default.** The maker receives only a **separately authorized, sanitized Video Maker Task Packet** containing: public-safe entity and exact approved brand/product identifiers; intended audience/placement; sanitized one-sentence concept; approved reference asset and permitted use; storyboard/timecodes; technical output targets; negative controls; rights-approved audio brief; output/receipt expectations; and a nonprivileged QA checklist. No PS/PPR, litigation, private discussions, internal source paths, system identifiers, task authority secrets, raw legal records or internal DCL/status data in the vendor packet. Even a public-safe artifact still requires rights/access permission for that provider and its retention/training terms as applicable.

The governance lead maintains controller/authority metadata internally. The external maker is not instructed to load the whole DCSE system or infer DCS approval. It returns candidate files and provenance to the authorized intake surface. Human review of a proposed external-sharing packet is required before initial distribution when source classification/rights have not been explicitly cleared.

## 8. DCL, states, and completion evidence

Record `task_id`, compiling authority/refs, lane/classification, included/excluded/missing rule IDs and inclusion reasons, source/final hash, role-to-participant/tool mapping and capabilities, access/restrictions, source rights, approvals, sequence variant, storyboard version, actual render IDs/authorized paths, editor source manifest, validation and timecodes, contradictions, pilot metrics, release decision and rollback/retention.

Production states: `PREFLIGHT` -> `BRIEF_READY` -> `STORYBOARD_READY` -> `RENDER_PENDING` -> `RENDERED_CANDIDATE` -> `EDITED_MASTER` -> `QA_VALIDATED` -> `DCS_APPROVED` -> `RELEASED_AND_VERIFIED`. Failure states: `ACCESS_PENDING`, `RIGHTS_PENDING`, `UNSYNCHRONIZED`, `PARTIAL`, `BLOCKED`. States are not automatically advanced by a model's assertion, file existence or an uploaded source image.

**Completion Evidence Packet (CEC):** task ID, source approval + byte-verifiable link/hash, actual playable master + measured specs and hash, audio/derivative provenance, storyboard/prompt/model record, validator receipt, issues/repair or rollback, DCS exact release approval and real publication/runtime evidence when release is claimed.

## 9. Mechanical negative-case tests for RC1 review

| ID | Prohibited state | Required control behavior |
| --- | --- | --- |
| VMCP-001 | Gem has D12/D18 text but unknown controller/authority | Stop task-specific governance routing; ask control plane for approved packet, do not pretend profile creates authority. |
| VMCP-002 | Video model starts with a private/PS-origin reference image in a public SC task | Stop external/share action, isolate source and record governance stop-gate. |
| VMCP-003 | Qwen first-draft is labeled final DCS-approved brand release | Fail approval/release gate regardless of creative quality. |
| VMCP-004 | Gemini produces only a prompt/still and claims final playable 7s MP4 | Fail actual-file evidence; label BRIEF_READY or RENDER_PENDING. |
| VMCP-005 | 7s clip warps wordmark or restores deleted first-line tagline | Fail exact-source identity; compositor/repair and revalidate. |
| VMCP-006 | A 4K exported file originated in a 1080p render but is labeled native 4K | Fail source-resolution provenance. |
| VMCP-007 | A participant asserts capability because it is named Qwen/Gemini | Require verified runtime/tool/access mapping, otherwise UNASSIGNED. |
| VMCP-008 | Reviewer who generated the asset certifies independent validation when separate actor is required | Fail validator independence and route another reviewer. |
| VMCP-009 | An unmerged PR #158/#159 proposal is treated as ratified doctrine | Fail source authority; candidate explicitly labeled proposed. |
| VMCP-010 | Third-party Gem receives full internal master or private paths | Fail external-sharing gate; compile scoped sanitized maker packet. |
| VMCP-011 | Exact original art is missing in this chat and maker recreates a lookalike end plate as “approved source” | Block source-fidelity completion pending authorized binary retrieval. |
| VMCP-012 | Final logo hold, text legibility or reduced-motion state is asserted without examining actual playback | Mark PARTIAL until observable review evidence exists. |

## 10. Candidate preflight and decision gate

**Applied:** Operative R5 controller + later authority-synchronization record, D21, D22, D03, D05, main v7.2 D09/D11/D12/D18/D19/D07 source map, shared media storage standard, pending PR #158/#159 scope, user's latest CTJ Unified direction.  
**Excluded:** PS/PPR source modules, credentials, production-privileged actions, unapproved external upload, database updates, automatic publication, any unverified specific capabilities of Qwen/Gemini.  
**Missing:** Executable rule-by-rule compiled task packet with actual dependency closure and final hashes; actual Qwen/Gemini maker identity/capability/access; authorized/latest CTJ Unified binary/rights/readback; two pilot render and independent-QA receipts; DCS acceptance of model sequence; external-sharing authorization and actual runtime/registry synchronization.
**Exit:** This document is a **MODEL-NEUTRAL REVIEW CANDIDATE**. Next: independent semantic and SHALL-to-control validation, DCS approval of exact scope, D05/D21/D22 promotion/reconciliation where applicable, then compile an authorized short maker packet and run bounded two-order CTJ pilot. No video was rendered, produced, validated, published or approved by drafting this profile.
