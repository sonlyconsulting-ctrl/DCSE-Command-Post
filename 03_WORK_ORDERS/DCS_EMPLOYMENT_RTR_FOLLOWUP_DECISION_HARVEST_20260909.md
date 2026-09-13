# DCS Employment RTR Follow-up Decision Harvest

**Task ID:** DCS-EMP-20260909-003  
**Date:** 2026-09-09  
**Lane:** DCS Employment / DCSE Command Post  
**Classification:** CONFIDENTIAL / INTERNAL  
**Status:** CANDIDATE / RULES-HARVEST  
**Parent Methodology:** DCSE-METH-EMP-001 v1.1  
**Related Work Order:** DCS-EMP-20260908-002  
**Purpose:** Preserve reusable decision logic from the Trustmark / Aavalar RTR case study while removing unsupported legal conclusions and converting alternate-access behavior into evidence-gated rules.

## 1. Preflight Validation

- Opportunity type: Contract, W2 staffing channel.
- Destination: DCS Employment rules harvest and future decision engine.
- Action: Review, normalize, preserve, and stage candidate rules.
- Authority source: DCS user directive, active DCS Employment methodology, current rules-harvest work order, source case-study transcript.
- Access: Authenticated GitHub repository access verified.
- Secret exposure: None required for this artifact.
- PS exposure: None required. Protected material excluded.
- Approval need: DCS review required before promotion to authoritative ruleset or runtime enforcement.
- Deliverable: Candidate rule harvest note.
- Exit criteria: Useful logic preserved, unsupported claims removed, risks surfaced, rule families mapped, next implementation path identified.

## 2. Case Study Determination

The Trustmark Expert Systems Business Analyst opportunity is a valid high-value test case because the role directly names AION and business rules expertise. That combination materially raises match value relative to ordinary analyst or commodity roles.

The case also exposes a recurring operational problem: effort is spent tailoring, negotiating rate, signing an RTR, and responding promptly, but the recruiter may provide no confirmation that the candidate was actually submitted to the end client.

The correct governance response is not automatic chasing and not automatic bypass. The correct response is evidence-weighted decisioning.

## 3. Accepted Reusable Logic

The following concepts are accepted as candidate rules for historical validation:

1. **RTR and Submission Stage Separation**  
   A signed RTR is evidence of authorization to represent. It is not by itself evidence that the recruiter or vendor actually submitted the candidate to the end client.

2. **Effort-Weighted Follow-up**  
   Follow-up effort should vary by opportunity value. The engine should weigh role fit, rarity of skill alignment, compensation, work model, travel burden, recruiter or agency reliability, elapsed time, and administrative drag.

3. **Niche Match Priority**  
   Rare, direct skill anchors such as AION, legacy business rules, or other uncommon verified capability can justify additional attention compared with low-value or commodity opportunities.

4. **Bounded Outreach**  
   Recruiter follow-up should remain limited and time-boxed. The exact limit should be policy-driven and score-sensitive rather than treated as a universal one-touch or 48-hour rule.

5. **Verified Submission State**  
   When material, the engagement record should distinguish requested RTR, RTR accepted, recruiter acknowledgment, vendor submission claimed, client submission verified, client response received, and interview scheduled.

6. **Alternate Access Path Review**  
   If a high-value opportunity remains unconfirmed, the system may research the employer's direct careers channel, known requisition, or appropriate professional contact. Any direct application or outreach must first pass duplicate-submission, exclusivity, vendor-chain, and contract-risk checks.

7. **Vendor Reliability as Evidence**  
   Recruiter and agency reliability should be inferred from observed DCS history, not stereotype or general staffing-market assumptions. Useful signals include responsiveness, confirmed submissions, interview conversion, duplicate-submission incidents, and closeout quality.

8. **Pipeline Drag Cost**  
   Administrative and cognitive drag are valid decision factors. The system should avoid allowing stale recruiter-mediated opportunities to consume disproportionate effort.

9. **Closeout Learning**  
   Closed, silent, or failed RTR engagements should still produce evidence for future source scoring, recruiter reliability, timing, package effort, and opportunity-selection rules.

## 4. Rejected or Held Claims

The following statements from the source case study are not accepted as governing rules:

### REJECTED: Automatic legal voiding of RTR

Do not state or infer that recruiter silence, lack of a submission ID, or nonperformance automatically makes RTR exclusivity legally void. The actual RTR language, duration, jurisdiction, client and vendor terms, and duplicate-submission consequences must be reviewed.

### REJECTED: Automatic direct bypass after 48 hours

Do not automatically submit directly to the end client after a fixed silence period. Direct application may create duplicate representation, vendor conflict, submission rejection, or contractual dispute.

### HELD: Universal one-touch rule

A one-touch follow-up may be a useful default for ordinary opportunities, but it is not yet validated as a universal DCS rule. High-value niche opportunities may justify a different cadence if the added effort is economically rational and does not weaken professional posture.

### HELD: Fixed match-score constants

Values such as 0.95 for AION matches, 0.80 for direct vendors, or 0.20 for intermediaries are illustrative only until calibrated against observed DCS pipeline outcomes.

## 5. Proposed Candidate Rule IDs

These IDs are staged for the broader rules-harvest process and are not authoritative:

- `EMP-RTR-001`: RTR Authorization Does Not Equal Verified Client Submission.
- `EMP-RTR-002`: RTR Scope and Exclusivity Must Be Verified Before Alternate Application.
- `EMP-FOLLOWUP-001`: Follow-up Effort Must Be Weighted by Opportunity Value and Administrative Cost.
- `EMP-FOLLOWUP-002`: Follow-up Cadence Must Be Bounded but Configurable by Score and Evidence.
- `EMP-VENDOR-001`: Vendor Reliability Must Be Based on Observed DCS Evidence.
- `EMP-SOURCE-001`: Alternate Access Paths Require Duplicate-Submission and Representation-Risk Review.
- `EMP-CLOSEOUT-001`: Silent RTR Outcomes Must Feed Pipeline Learning and Source Scoring.

## 6. Decision Model Direction

The future Python decision engine should separate scoring from hard stop-gates.

### Scored factors

- verified role fit;
- niche skill rarity;
- compensation or economic value;
- work arrangement and travel burden;
- probability based on observed source history;
- recruiter responsiveness;
- elapsed time;
- effort already spent;
- incremental effort required;
- strategic value beyond the immediate role.

### Hard stop-gates

- unresolved RTR exclusivity or representation terms;
- duplicate-submission risk;
- conflicting recruiter or vendor claims;
- unknown end client when identity is material;
- unsafe or unnecessary sensitive-data request;
- compensation or travel economics below approved floor without strategic exception;
- unsupported direct-application legal assumption.

The engine may recommend `FOLLOW_UP`, `WAIT`, `RESEARCH_DIRECT_PATH`, `CLOSE`, `ESCALATE_REPRESENTATION_RISK`, or `HOLD_FOR_TERMS_REVIEW`. It must not convert a recommendation into an external submission without required authorization and evidence.

## 7. Bidirectional Validation

### Forward test

Given the actual recruiter correspondence, RTR language, role fit, compensation, timing, vendor facts, and known client channels, what action is supported without assumption?

### Backward audit

Given the desired outcome of preserving access to a high-value opportunity while preventing wasted effort and duplicate representation, what evidence and controls must exist before follow-up, direct outreach, or closeout is valid?

If either direction fails, hold or narrow the action.

## 8. Evidence Status

**Verified:** The source case contains a high-value AION / business-rules role, a signed RTR sequence, a rate confirmation, and a recruiter follow-up with no response shown in the supplied material.

**Likely:** Recruiter silence can create material pipeline drag and may justify alternate-channel research for high-value roles.

**Unknown:** Whether the recruiter actually submitted the candidate, whether Aavalar holds exclusive or preferred vendor access, whether Trustmark would accept a direct duplicate application, and whether the RTR contains enforceable duration or exclusivity terms beyond the quoted correspondence.

## 9. Implementation Handoff

**Handoff ID:** DCS-HO-20260909-003

Route these candidate rules into the pending DCS Employment rules harvest under:

- `EMP-RTR-*`
- `EMP-VENDOR-*`
- `EMP-SOURCE-*`
- `EMP-CLOSEOUT-*`

Then incorporate them into the planned `DCS_EMPLOYMENT_RULESET_v1.yaml` and `employment_rules_engine.py` only after historical validation and DCS promotion.

## 10. Completion Audit

- Expected source set: source case study plus active v7.2 Employment methodology and current rules-harvest work order.
- Processed: Yes.
- Unsupported legal conclusion removed: Yes.
- Duplicate-submission risk added: Yes.
- Candidate rules mapped to existing rule families: Yes.
- PS leakage check: Pass.
- Secret leakage check: Pass.
- Unsupported claim check: Pass after corrections above.
- Promotion status: Not promoted.
- Final status: COMPLETE AS CANDIDATE RULE-HARVEST ARTIFACT.

Structure Precedes Scale.
