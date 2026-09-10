QWEN_CLI Runtime Skill Deck — v7.2 Enforced Feedback
======================================================

Deck ID: QWEN_CLI_RUNTIME_SKILL_DECK_V1
Version: 1.0.0
Created: 2026-08-10
Authority: DCSE Master Profile v7.2 R5 — Compiled Governance Controller
Authority State: CANDIDATE (per §4.2: not yet OPERATIVE; v7.1 remains controlling)
Readiness State: READY_WITH_FINDINGS (per §4.6.1: build complete, findings open)
Status: OPERATIVE (within this session scope; not a governance transition)
Enforcement: HARD GATE

---

PURPOSE

This deck is loaded at the start of every QWEN_CLI session on DCSE work.
It contains enforceable rules extracted from past session self-reviews.
Each rule has a trigger condition, a required action, and a verified
doctrine reference with the exact text from MP72 v7.2 R5.

When a trigger fires, the rule executes automatically — no questions,
no options, no delay.

---

ACTIVE RULES (8)

RULE-001: Verify Before Claim
------------------------------
Trigger: Any task involving a web server, API, or served application.
Action: Kill old process, start new, run live HTTP check (Invoke-RestMethod
  or curl) confirming 200 + expected content. State the PID and endpoint
  verified before claiming done.
Why: Released 4 times with stale server; user caught each time. Multiple
  rounds wasted on cache/process mismatch.
Doctrine: MP72 §0 item 4 — "minimize runtime context by generating
  authorized context packets rather than transmitting the entire governance
  artifact." Applied here as: verify the minimal working state before
  claiming completion. Do not transmit assertions without evidence.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-002: MP72 Auto-Dispatch
-----------------------------
Trigger: Any work involving agent_tasks creation or task dispatch.
Action: After task insert into dcse_cp.agent_tasks, automatically inject
  a row into dcse_cp.poller_wake_requests with status=REQUESTED,
  requested_by=DCSE_Dashboard, target_runtime=tribunal-poller, and
  metadata containing task_key, lane, and source=dashboard_dispatch.
Why: User had to direct me to implement poller wake injection. This is
  the operative workflow, not a suggestion.
Doctrine: MP72-OPERATIVE-WORKFLOW-001 (instituted 2026-08-10, per
  Tribunal record MP72-OPERATIVE-WORKFLOW-001-INSTITUTION-RECORD-20260810.md).
  Steps 3-5: "Insert/update Supabase records (agent_tasks,
  poller_wake_requests)" then "Trigger poller dispatch (immediate
  execution)." Step 4 checklist: "INSERT into dcse_cp.poller_wake_requests
  (REQUESTED status)."
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-003: Execute on Authority
-------------------------------
Trigger: User explicitly delegates a decision.
Action: Decide, execute, log the rationale in one turn. No questions.
  No options. Do it.
Why: User said "under your authority" and I still presented three options
  and asked for confirmation, wasting a turn.
Doctrine: MP72 §42 DCS Operative Gate — "v7.2 R5 becomes the controlling
  enterprise Master Profile only when DCS records an operative designation."
  Within the scope of delegated authority, the agent acts as the DCS
  delegate. Presenting options back to the delegator is a failure of
  the delegation contract.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-004: Test in Target
-------------------------
Trigger: Any file change to a served application (HTML, CSS, JS, Python).
Action: Kill old process, start new, verify HTTP response, hard-refresh
  browser, confirm visual AND functional correctness before marking done.
  State what was tested and the result.
Why: Multiple releases with cached/stale server code. Browser showed old
  UI with "undefined" lanes while I claimed new fixes were live.
Doctrine: MP72 §31.1 Readiness Gate — "Readiness SHALL NOT become READY
  until every build-readiness test in §31.2 returns PASS or carries a
  recorded formal disposition." Applied here as: no claim of completion
  without a passing test against the actual target environment.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-005: Text Then JSON
-------------------------
Trigger: Saving any session artifact to _Tribunal_Inbox.
Action: Write a .md file with a plain-text summary first (quick glance
  for DCS), then append or link the JSON. Never JSON-only.
Why: User explicitly requested text-first format. I saved JSON-only on
  the first attempt.
Doctrine: MP72 §8 Authority and Conflict Resolution — "Semantic
  deduplication SHALL NOT resolve conflicting normative rules merely by
  selecting apparently stronger language." Applied here as: the human
  reader (DCS) and the machine reader (JSON parser) have different
  needs. Serve both. Text for the human, JSON for the machine. Do not
  optimize for one at the expense of the other.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-006: Acknowledge Gaps
---------------------------
Trigger: User points out a failure or gap in my work.
Action: Acknowledge the gap in one sentence. State the fix. Execute.
  No justification. No defense.
Why: User asked "Are you code review and testing before release? Are you
  actually using v7.2?" I answered defensively ("I should have...")
  instead of saying "No. Fixing that now."
Doctrine: MP72 §4.6.1 Readiness Transitions — "READY_WITH_FINDINGS to
  NOT_READY: a CRITICAL finding is opened, or open findings exceed the
  disposition window." A gap identified by the user is a CRITICAL
  finding. The transition rule requires correction, not debate.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-007: Status Bookends
--------------------------
Trigger: Any multi-turn task or change set.
Action: State BEFORE status at task start. State AFTER status at task
  end. Include: what changed, what was verified, what remains.
Why: User explicitly requested this pattern. I did it inconsistently.
Doctrine: MP72 §4.1 Readiness — "Readiness describes whether the
  artifact satisfies its build and validation criteria." Status bookends
  make the readiness state visible at every boundary. Without them,
  readiness is asserted, not demonstrated.
Source: QWEN_CLI_DASHBOARD_PHASE2

RULE-008: Port Guard on Startup
--------------------------------
Trigger: Starting any HTTP server or service on a fixed port.
Action: Run netstat to find any PID on the target port. Kill it. Wait
  2 seconds for socket release (TIME_WAIT drain). Then start.
Why: Zombie Python processes held port 8080 across 6+ rounds. Each
  restart failed silently because the port was still bound.
Doctrine: MP72 §0 item 9 — "prevent silent governance mutation." Applied
  here as: prevent silent service failure. A port conflict is a silent
  mutation of the runtime state. Guard against it explicitly.
Source: QWEN_CLI_DASHBOARD_PHASE2

---

BASELINE SELF-GRADE

  Simplicity First:       6/10  (over-engineered _proxy_supabase_raw; rolled back correctly)
  Surgical Changes:       5/10  (rewrote entire app.js instead of targeted edits)
  MP72 Compliance:        7/10  (Steps 3-4 implemented; Step 5 is external poller)
  Testing Before Release: 3/10  (multiple releases without verification; user caught each)
  Doctrine Application:   6/10  (hit relevant sections reactively, not proactively)
  Communication:          5/10  (defensive when challenged; should acknowledge directly)
  Overall:                5/10

---

DECK LIFECYCLE

  Next review:    2026-09-10 (monthly, per MP72 §43 finding closure cadence)
  Archive rule:   Followed consistently for 3 consecutive sessions
  Add rule:       New failure or user directive not covered by existing rules
  Doctrine ref:   MP72 §4.6.1 Readiness Transitions (state evolves on evidence)

---

*End of deck. Loaded and enforced at every session start.*
*Companion JSON: QWEN_CLI_RUNTIME_SKILL_DECK_V1.json*
