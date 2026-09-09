# DCS Employment Rules Harvest and Command Post Module Work Order

**Task ID:** DCS-EMP-20260908-002  
**Originating Engagement:** DCS-ENG-20260908-001  
**Date:** 2026-09-08  
**Authority:** DCS Level 0  
**Lane:** DCS Employment / DCSE Command Post  
**Classification:** CONFIDENTIAL / INTERNAL  
**Status:** STAGED / RULES-HARVEST-PENDING  
**Supabase posture:** HOLD FOR FURTHER WRITES / NO ADDITIONAL DATABASE CHANGE IN THIS CLOSEOUT

## 1. Executive Direction

DCS Employment is to be implemented as a component under DCSE Command Post, not as a separate standalone governance system. D16 remains unchanged as the enterprise DDNA mechanism. Employment-specific rules, candidate logic, workflow enforcement, training artifacts, opportunity tracking, and product candidates are to be handled in the DCS Employment layer and routed through Command Post.

The immediate next phase is a rules harvest and gap analysis before further promotion or application build work.

## 2. Source Basis for Rules Harvest

The first harvest corpus will include, when available and authorized:

1. Historical recruiter emails and exchanges.
2. Submitted resumes and prior targeted variants.
3. Job descriptions and opportunity packets.
4. RTR, rate, compensation, travel, and vendor-chain exchanges.
5. Critical DCS Employment project conversations and DCS corrections.
6. Interview preparation modules, quizzes, study guides, videos, and related training artifacts.
7. Gemini Jim Employment outputs and corrections.
8. TAPIA employment-adjacent training and artifact sources after exact source identification.
9. `DCS Employ Emails.zip`, subject to PII/secret scrubbing before any reusable rule extraction.

Raw sources remain evidence. Harvested rules must exclude SSN/DOB, identity-document data, credentials, private addresses, and other unnecessary PII or secret-bearing content.

## 3. Candidate Rule Families

The rules harvest must evaluate at minimum the following families:

- `EMP-INTAKE-*`: source and opportunity intake.
- `EMP-CLASS-*`: Employment, Contract, Freelance, Consulting/Advisory, Business Opportunity, SC Commercial Opportunity, Mixed.
- `EMP-BA-*`: BA-specific requirements, elicitation, process, requirements, UAT, delivery method, stakeholder and role-altitude logic.
- `EMP-CONTRACT-*`: staffing, W2, 1099, C2C, temporary, fractional, project contract.
- `EMP-FREELANCE-*`: scope, deliverables, price, payment, revisions, IP, acceptance, margin, change control.
- `EMP-CONSULT-*`: expertise-led scope, advisory/implementation balance, executive value, pricing, liability, handoff, repeatability.
- `EMP-LOCATION-*`: out-of-town and recurring onsite economics.
- `EMP-RATE-*`: compensation, benefits, base versus all-inclusive rate, market validation.
- `EMP-RTR-*`: RTR scope, exclusivity, sensitive-data handling, and stage separation.
- `EMP-VENDOR-*`: recruiter, staffing vendor, prime vendor/MSP/VMS, client, duplicate-submission risk.
- `EMP-RESUME-*`: baseline preservation, role identity, role altitude, over-positioning scan, claim control.
- `EMP-COMMS-*`: recruiter/client communications.
- `EMP-TRAINING-*`: interview study, cram modules, quizzes, videos, capability-gap training.
- `EMP-SOURCE-*`: inbound, direct application, outbound, referral/network, freelance marketplace, consulting prospect, partnership/business opportunity.
- `EMP-OUTBOUND-*`: proactive account targeting and cold/warm outreach.
- `EMP-DDNA-*`: Employment-specific DDNA extraction candidates.
- `EMP-CLOSEOUT-*`: outcomes, lessons, effort, conversion and evidence closeout.

## 4. AMG DDNA Candidate Set

The AMG/Beverly pursuit produced seven candidate Employment rules to be validated against the historical corpus before promotion:

1. `DDNA-EMP-20260908-001` - Target Identity Must Override Baseline Gravity.
2. `DDNA-EMP-20260908-002` - Mandatory Role Altitude Gate.
3. `DDNA-EMP-20260908-003` - Resume Visual Baseline Preservation.
4. `DDNA-EMP-20260908-004` - Resume Over-Positioning Scan.
5. `DDNA-EMP-20260908-005` - RTR and Submission Stage Separation.
6. `DDNA-EMP-20260908-006` - Out-of-Town Engagement Economics Gate.
7. `DDNA-EMP-20260908-007` - Employment Effort Ledger and Command Post Module.

D16 is not changed by this candidate set.

## 5. Mandatory Out-of-Town Pre-Screen

Any recurring onsite opportunity outside DCS's normal local commuting market must invoke a consistent location-economics pre-screen before final pursuit economics are approved.

The screen must consider:

- worksite and local market;
- onsite cadence and nights away;
- airfare/mileage;
- lodging;
- rental car/rideshare/local transportation;
- parking/tolls;
- meals/per diem;
- travel-time burden;
- reimbursement and relocation assistance;
- W2/C2C/1099 structure and benefits;
- state/local tax differences where relevant;
- cost-of-living and housing differential;
- nearby lower-cost communities;
- base professional rate;
- all-inclusive break-even rate;
- effective rate after unreimbursed costs;
- alternative cadence scenarios such as concentrated onsite periods.

Required outcome: `GO`, `CONDITIONAL GO`, or `NO-GO`, with the economic assumptions visible.

## 6. Reactive and Proactive Employment Pipelines

DCS Employment must track both opportunity conversion and opportunity creation.

### Reactive / inbound
- recruiter contact;
- job-board discovery;
- direct application;
- inbound referral.

### Proactive / outbound
- strategic account research;
- target-role family identification;
- warm or cold outreach;
- relationship development;
- problem-led freelance or consulting prospecting.

Named strategic accounts that must remain visible through future dashboard work include Crowe, Munich Re, and Hyatt. They are to be represented as account-level targets rather than disappearing solely because an individual requisition closes.

Hyatt also supports a broader hospitality transformation campaign candidate. The campaign may include Hyatt, Marriott, Hilton, OUTRIGGER, and other appropriate hospitality organizations, with Hawaii treated as a bounded market experiment when commercially justified. A June 2027 Hawaii travel window may inform timing but must not be used to make an otherwise uneconomic engagement appear viable.

## 7. Employment Learning / Readiness Component

Training is a first-class Employment asset class, not an attachment-only function. The future Command Post Employment component should track:

- interview study modules;
- role-specific cram packages;
- quizzes and knowledge checks;
- training videos;
- capability-gap remediation;
- AI/BA/architecture transition study;
- TAPIA employment-adjacent training after source verification;
- evidence of completion and reuse.

## 8. Product Hypothesis

The internal DCS Employment component may support a sanitized commercial derivative. Product design should separate the engine from the interface.

Two user modes are to be evaluated:

### Quick Pursuit
One opportunity, potentially one-day use, minimal persistence, local/session storage, optional export.

### Career Campaign
Longer-running search or opportunity-generation process, authenticated persistence, pipeline history, recruiter/account history, training, rates, effort, analytics, and lessons learned.

Preferred product architecture: local-first or session-first quick use with optional authenticated cloud persistence when the user elects to save a campaign.

No commercial release, product naming, public claim, or pricing is approved by this work order.

## 9. Proposed Rule/Script Package

The rules harvest should produce a minimum-file implementation package for review:

- `DCS_EMPLOYMENT_RULESET_v1.yaml`
- `DCS_EMPLOYMENT_RULE_HARVEST_REPORT_v1.md`
- `DCS_EMPLOYMENT_GAP_ANALYSIS_v1.md`
- `employment_rules_engine.py`
- `employment_rule_harvester.py`
- `employment_gap_analyzer.py`
- `tests/`
- `SOURCE_MANIFEST.json`

Candidate rules remain non-authoritative until DCS review and promotion.

## 10. Tribunal Request Routing

When DCS explicitly requests a Tribunal record, the preferred operational behavior is:

1. Prepare the durable Tribunal record from verified task evidence.
2. If an authenticated Tribunal/Command Post write path is available in the current runtime, write the record to `_Tribunal_Inbox` or the currently governing Tribunal intake path.
3. Do not claim a Work-mode handoff unless a real Work handoff/execution surface is available and invoked.
4. A normal ChatGPT conversation cannot programmatically switch itself into ChatGPT Work mode. When no Work handoff is available, the fallback is a durable Tribunal Inbox file using the authenticated repository/file path available.
5. Never claim Tribunal completion solely because text was drafted in chat.

## 11. Definition of Done for Next Phase

The rules-harvest phase is complete when:

1. The source manifest is assembled and classified.
2. Sensitive/PII-bearing historical material is scrubbed before rule extraction.
3. Existing versus new versus duplicate versus conflicting versus obsolete rules are identified.
4. AMG candidate rules are validated, merged, revised, or rejected based on the larger corpus.
5. BA, contract, freelance, consulting/advisory, location, outbound, training, and closeout rule gaps are documented.
6. The human-readable ruleset and script skeleton pass tests against representative historical opportunities.
7. No D16 change is required unless a genuinely enterprise-wide DDNA governance defect is independently identified.
8. No further Supabase write occurs until DCS lifts the current hold.

Structure Precedes Scale.
