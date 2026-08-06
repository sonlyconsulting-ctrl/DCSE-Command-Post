# DCSE Doctrine D14: DART PS Protected & Litigation Blueprints

**Document ID:** DCSE-D14  
**Version:** v6.9  
**Created Date/Time:** 2026-06-20T23:26:34-04:00  
**Last Doc Modified Date/Time:** 2026-06-21T19:27:00-04:00
**Last Version/Release Date/Time:** 2026-06-21T15:22:37-04:00  
**Status:** DCSE Authorized version Pending Approval  
**Classification:** PS-PROTECTED  
**Lane:** PS  
**Canonical file:** D14_DART_PS_Protected.md  
**Doctrine Description:** The DART PS Protected Doctrine (D14) details the active case parameters, target custodians, and operational blueprints for Pro Se litigation. It establishes the strict firewall separating confidential case facts from the shared public Hub. D14 provides skeleton blueprints for legal filings, meet-and-confer letters, and deposition outlines.  
**Parent Document:** [DCSE_Master_Profile_v6.9_RC1.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/00_Authority/DCSE_Master_Profile_v6.9_RC1.md)  

---

## 1. Case Parameters & Boundaries

All litigation-support outputs must align with the active federal civil-rights case:
- **Case Title**: *Seals v. DHHS*  
- **Case Number**: `Case No. 8:23CV489` (U.S. District Court for the District of Nebraska)  
- **Primary Claims**: Title VII (Race discrimination, Retaliation), 42 U.S.C. §§ 1981 and 1983.  
- **Target Custodians**: Converse, Christensen, Schafers, Snyder, Smith, and CSS liaisons.  
- **Target Systems**: Clarity, Microsoft Teams, SharePoint, OneNote, Jira, and Procurement RFP 5210Z1.  
- **Evidentiary Date Range**: Assignment start date through termination date plus 30 days.  

---

## 2. PS/TI Operational Firewall

Pro Se (PS) litigation operations and The Initiative (TI) public campaigns must remain strictly independent:

| Characteristic | PS (Pro Se) | TI (The Initiative) |
| :--- | :--- | :--- |
| **Domain** | Federal litigation filing and evidentiary analysis. | Public advocacy, civil-rights education, movement building. |
| **Operational Path** | Isolated local Spoke: `C:\DS All Things\DS Litigation` | Shared Hub: `C:\DS All Things\DCSE_Command_Center\v6.9` |
| **Case References** | Case No. 8:23CV489, specific pleadings, named defendants. | General civil-rights principles only. No case references. |
| **Confidentiality** | Attorney-client protected. Strictly confidential. | Public-facing. Approved for distribution. |

### 2.1 Invariant Firewall Rules
- **NEVER** reference Case No. 8:23CV489, deposition facts, or the plaintiff's real name in TI public articles, blogs, website copy, or social media.
- **NEVER** use TI campaigns as a narrative bridge to pressure active litigation targets.
- **ALWAYS** route raw case discovery through local Spoke scripts; only metadata hashes may enter the Hub.

---

## 3. PS Litigation Output Blueprints

### 3.1 Legal Draft Blueprint (PS)
When drafting motions, briefs, or opposition papers, the document must include:
1. **Caption & Title Block**: Identifying the Court (U.S. District Court for the District of Nebraska), parties, and docket number.
2. **Introduction**: Explaining the nature of the filing and relief sought.
3. **Procedural History**: Chronicling pending matters, scheduling orders, and deadlines.
4. **Issues Presented**: Framing the legal questions as concise, one-line questions.
5. **Standards of Review**: Detail the applicable Rule standard (e.g. Rule 12(b)(6), Rule 56(c) summary judgment).
6. **Argument (Sections I–III)**: Structure argument logically as Rule Statement → Application to Facts → Requested Relief.
7. **Remedies & Damages**: Showing back-pay/front-pay, emotional distress, and mitigation details.
8. **Conclusion & Certificate of Service**.
9. **Lenses Appendix**: Review via the Judge Lens (burden fit), Opposing Counsel Lens (likely delay/immunity tactics), and Defendant Lens (policy cover).

### 3.2 Meet-and-Confer / ESI Letter Skeleton
All ESI letters to opposing counsel demanding production must incorporate:
- Scope and relevance statements.
- Listed Custodians and target Systems of record.
- Primary and secondary search terms (including "cultural fit" and race terms).
- Delivery format (native + metadata) and rolling production milestones (7-day initial, weekly rolling).
- Demand for privilege log (FRCP 26(b)(5)) and withholding statements (Rule 34(b)(2)(C)) within 14 days.
- **Closing Warning**: *"If we cannot agree to date-certain commitments for the above custodians, systems, formats, and milestones, PS will seek relief under Rule 37."*

### 3.3 Deposition Outlines
Structure deposition scripts into logical modules:
1. **Exhibits Map**: Bates ranges of documents to present.
2. **Topic Blocks**: Policy familiarity → Knowledge of complaints → Communications timeline → Comparator treatment → Shifting explanations.
3. **Target Admissions**: Statements required to establish pretext.

---

## Related Doctrine

- [D13_DART_Core.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D13_DART_Core.md) - Core DART framework, phases, DEM matrix, and quality gates
- [D08_Voice_Tone.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D08_Voice_Tone.md) - PS voice register (formal, federal court)

---

## Error-Catch Protocol

If this doctrine file is missing, unreadable, or not found by an executing agent, follow the canonical error-catch protocol defined in [D03_AI_Orchestration.md](file:///C:/DS%20All%20Things/DCSE_Command_Center/v6.9/01_Doctrine/D03_AI_Orchestration.md) Section 5.3:
1. **HALT** execution immediately. Do not guess or infer rules from pre-training.
2. **LOG** `ERR_MISSING_DOCTRINE` to `05_Tribunal_Inbox`.
3. **TRIGGER** STOPGATE and alert the user.

