# DCSE V7.1 Gate Control and Violation Register

Date: 2026-08-03  
Primary runtime doctrine: D21  
Supporting gate doctrines: D03, D05, D22

## Gate ownership

| Control | Governing authority | Required behavior |
|---|---|---|
| Runtime doctrine selection | D21 DDR and DCL | determine, record, and version every applicable doctrine before execution |
| Session readiness Stop-Gate | D03 plus V7.1 First-Assignment Readiness and Fail-Fast Gate | stop only for missing authority, security, destructive action, unavailable required input, or a DCS-reserved decision |
| Baseline and promotion Pass-Gate | D05 | require completed evidence, review receipt, rollback readiness, and reconciled lifecycle state |
| Source and drift gate | D22 | reconcile canonical GitHub artifact, runtime registry, and Supabase record |
| Product phase gates | D20 | Intake, Build, Test, Package, Promote, Deploy receipts |

## Violation register

| ID | Violation | Doctrine conflict | Corrective action | Status |
|---|---|---|---|---|
| V-001 | Runtime map stopped at D09 | D21, D22 | replace with D01-D22 inventory and route | CORRECTED IN PACKAGE |
| V-002 | D21 and D22 omitted from always-on path | D21, D22 | make both mandatory for every rerun | CORRECTED IN PACKAGE |
| V-003 | Existing execution tasks carry incomplete doctrine paths | D21 | preserve as Baseline Set A and supersede with rerun tasks | PENDING DB WRITE |
| V-004 | V7.1 label used without DDR and DCL evidence | D21 | require DCL before claim or execution | CORRECTED IN CONTRACT |
| V-005 | Prior BOW evidence used mixed legacy and v7.0 sources | D05, D22 | hash and freeze baseline, then rerun from canonical V7.1 | PENDING RERUN |
| V-006 | BOW-002 scope drifted from intended CTJ audit | D03, D20, D21 | bind task title, acceptance criteria, product target and output schema | CORRECTED IN RERUN SCOPE |
| V-007 | BOW-003 had claims without retrievable output | D04, D05, D20 | prohibit completion when output references are empty or files are zero length | CORRECTED IN CONTRACT |
| V-008 | Mailbox insertion was treated as delivery | D04 | require consumer acknowledgement or verified processing event | CORRECTED IN CONTRACT |
| V-009 | Governance registry omits multiple doctrines | D21, D22 | register D01-D22 with V7.1 hashes and canonical paths | PENDING DB WRITE |
| V-010 | Risk of PS doctrine leakage into SYSTEM work | D13, D14, D21 | explicitly exclude D13 and D14 from BOW-001 through BOW-004 | ACTIVE CONTROL |
| V-011 | Named-model availability produced unnecessary stoppage | D03, D21 | use capability-selected fallback and record accountable runtime identity | CORRECTED IN CONTRACT |
| V-012 | Poller overlap and credential failure could produce false progress | D03, D04, D05 | require single-instance lock, credential preflight, nonempty receipt and fresh heartbeat | CORRECTED IN RERUN 001 |

## Confluence rule

When multiple doctrines converge, the strictest applicable safety or evidence requirement governs. A lower-level task description cannot waive D03 readiness, D05 promotion evidence, D21 runtime logging, or D22 reconciliation. Conflicts must be recorded in the DCL and resolved by source authority. Routine availability of a named model is not a constitutional Stop-Gate.

## Conversation governance correction

This critical runtime discovery conversation is governed primarily by D21 Doctrine Runtime Engine. D04 governs its communications and delivery receipts. D03 governs readiness and fail-fast behavior. D05 governs approval and promotion. D22 governs authoritative source reconciliation. The earlier D04-only classification was incomplete and is superseded.
