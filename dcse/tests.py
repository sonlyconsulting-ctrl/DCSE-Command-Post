"""The suite.

Two coverage assertions run before any individual case, and they are the point
of this file.

    Every registered rule has at least one case.
    Every registered rule has at least one case that expects a refusal.

The second is the one that matters. A rule shown only to allow correct input is
unproven, and a suite reporting twelve of twelve against sixty rules is telling
you about the suite rather than about the rules. If a rule cannot be made to
fail on purpose, either it does nothing or nobody understands it, and both of
those should stop a build.
"""
from __future__ import annotations

import sys
from typing import Any, Dict, List, Sequence, Tuple

sys.path.insert(0, __file__.rsplit("/", 1)[0])

from adapters import AdapterSet, Recording  # noqa: E402
from model import (ACTIVE, CANDIDATE, ESCALATE, EXECUTE, EXECUTE_AS_CANDIDATE,
                   FAIL, PASS, PROVISIONAL, REFUSE, UNKNOWN, Operation)  # noqa: E402
from orchestrator import Orchestrator  # noqa: E402
from registry import REGISTRY, load_rules  # noqa: E402

load_rules()

NOW = 4102444800.0        # well in the future, for authority expiry cases
PAST = 1.0
H = "a" * 64              # a well formed sha256
H2 = "b" * 64


def op(entity: str, action: str = "inspect", caps: Sequence[str] = (),
       **facts: Any) -> Operation:
    return Operation(entity=entity, action=action, capabilities=tuple(caps),
                     facts=facts)


def verdict(rule_id: str, operation: Operation) -> str:
    r = REGISTRY.rule(rule_id)
    if r is None:
        raise KeyError("no such rule: %s" % rule_id)
    return r.check(operation)


# (rule_id, label, operation, expected)
CASES: List[Tuple[str, str, Operation, str]] = [

    # -- task ---------------------------------------------------------
    ("TASK-01", "an id is present", op("task", task_id="T-1"), PASS),
    ("TASK-01", "no id", op("task"), UNKNOWN),
    ("TASK-02", "objective stated", op("task", objective="ship it"), PASS),
    ("TASK-02", "no objective", op("task"), UNKNOWN),
    ("TASK-03", "criteria present", op("task", acceptance_criteria=["green"]), PASS),
    ("TASK-03", "empty criteria list", op("task", acceptance_criteria=[]), UNKNOWN),
    ("TASK-04", "owner named", op("task", owner="DCS"), PASS),
    ("TASK-04", "unowned", op("task"), UNKNOWN),
    ("TASK-05", "known state", op("task", state="open"), PASS),
    ("TASK-05", "invented state", op("task", state="nearly"), FAIL),
    ("TASK-06", "complete with evidence",
     op("task", action="complete", state="complete", completion_evidence="ev_1"), PASS),
    ("TASK-06", "complete with no evidence is a failed claim, not a gap",
     op("task", action="complete", state="complete"), FAIL),
    ("TASK-06", "not complete, rule is vacuous", op("task", state="open"), PASS),
    ("TASK-07", "blocked names the blocker",
     op("task", state="blocked", blocker_ref="dpl_err"), PASS),
    ("TASK-07", "blocked names nothing", op("task", state="blocked"), FAIL),
    ("TASK-08", "superseded points forward",
     op("task", state="superseded", superseded_by="T-2"), PASS),
    ("TASK-08", "superseded and complete at once",
     op("task", state="superseded", superseded_by="T-2", completion_evidence="e"), FAIL),

    # -- idea ---------------------------------------------------------
    ("IDEA-01", "id present", op("idea", idea_id="I-1"), PASS),
    ("IDEA-01", "no id", op("idea"), UNKNOWN),
    ("IDEA-02", "states itself", op("idea", statement="use one registry"), PASS),
    ("IDEA-02", "title only", op("idea"), UNKNOWN),
    ("IDEA-03", "origin recorded", op("idea", origin_ref="session/2026-09-13"), PASS),
    ("IDEA-03", "no origin", op("idea"), UNKNOWN),
    ("IDEA-04", "known state", op("idea", state="candidate"), PASS),
    ("IDEA-04", "presented as something else", op("idea", state="approved"), FAIL),
    ("IDEA-05", "adoption carries a decision",
     op("idea", action="adopt", decision_ref="d_1"), PASS),
    ("IDEA-05", "adopted by assertion", op("idea", action="adopt"), FAIL),

    # -- asset --------------------------------------------------------
    ("ASSET-01", "id present", op("asset", asset_id="A-1"), PASS),
    ("ASSET-01", "no id", op("asset"), UNKNOWN),
    ("ASSET-02", "well formed hash", op("asset", content_hash=H), PASS),
    ("ASSET-02", "a filename is not a hash", op("asset", content_hash="report.pdf"), FAIL),
    ("ASSET-03", "destination resolves",
     op("asset", action="store", storage_ref="files/aa/x", object_present=True), PASS),
    ("ASSET-03", "destination named but nothing there",
     op("asset", action="store", storage_ref="files/aa/x", object_present=False), FAIL),
    ("ASSET-04", "readback matches",
     op("asset", action="store", content_hash=H, readback_hash=H), PASS),
    ("ASSET-04", "readback differs",
     op("asset", action="store", content_hash=H, readback_hash=H2), FAIL),
    ("ASSET-04", "no readback at all", op("asset", action="store", content_hash=H), FAIL),
    ("ASSET-05", "does not touch the source",
     op("asset", action="update", mutates_source=False), PASS),
    ("ASSET-05", "rewrites the original", op("asset", action="update", mutates_source=True), FAIL),
    ("ASSET-06", "generated names its parents",
     op("asset", generated=True, derived_from=["A-1"]), PASS),
    ("ASSET-06", "generated from nowhere", op("asset", generated=True), FAIL),
    ("ASSET-07", "both removed",
     op("asset", action="delete", object_removed=True, metadata_removed=True), PASS),
    ("ASSET-07", "row removed, object left",
     op("asset", action="delete", object_removed=False, metadata_removed=True), FAIL),

    # -- ddna ---------------------------------------------------------
    ("DDNA-01", "id present", op("ddna", record_id="D-1"), PASS),
    ("DDNA-01", "no id", op("ddna"), UNKNOWN),
    ("DDNA-02", "lane declared", op("ddna", lane="DCSE"), PASS),
    ("DDNA-02", "no lane", op("ddna"), UNKNOWN),
    ("DDNA-03", "sensitivity carried", op("ddna", sensitivity="internal"), PASS),
    ("DDNA-03", "no sensitivity verdict", op("ddna"), UNKNOWN),
    ("DDNA-04", "promotion carries a decision",
     op("ddna", action="promote", decision_ref="d_2"), PASS),
    ("DDNA-04", "promoted by extraction alone", op("ddna", action="promote"), FAIL),
    ("DDNA-05", "same lane throughout", op("ddna", lanes_touched=["DCSE"]), PASS),
    ("DDNA-05", "protected lane reached from outside it",
     op("ddna", lanes_touched=["DCSE", "PS"]), FAIL),

    # -- knowledge ----------------------------------------------------
    ("KN-01", "id present", op("knowledge", knowledge_id="K-1"), PASS),
    ("KN-01", "no id", op("knowledge"), UNKNOWN),
    ("KN-02", "source named", op("knowledge", source_ref="doc_7"), PASS),
    ("KN-02", "no source", op("knowledge"), UNKNOWN),
    ("KN-03", "known authority level", op("knowledge", authority="stated"), PASS),
    ("KN-03", "invented authority level", op("knowledge", authority="obvious"), FAIL),
    ("KN-04", "retained with its source",
     op("knowledge", authority="unclassified", source_ref="doc_7", value_inferred=False), PASS),
    ("KN-04", "unclassified with no source to go back to",
     op("knowledge", authority="unclassified"), FAIL),
    ("KN-04", "value was inferred to fill a field",
     op("knowledge", authority="stated", value_inferred=True), FAIL),
    ("KN-05", "revision supersedes",
     op("knowledge", action="revise", supersedes="K-1"), PASS),
    ("KN-05", "revision overwrites", op("knowledge", action="revise"), FAIL),

    # -- escd ---------------------------------------------------------
    ("ESCD-01", "intent and reading both held",
     op("task", caps=["escd"], principal_intent="book it", interpretation="he means friday"), PASS),
    ("ESCD-01", "a reading with no stated intent behind it",
     op("task", caps=["escd"], interpretation="he means friday"), FAIL),
    ("ESCD-02", "reading is labelled",
     op("task", caps=["escd"], interpretation="x", interpretation_labelled=True), PASS),
    ("ESCD-02", "reading presented plain",
     op("task", caps=["escd"], interpretation="x", interpretation_labelled=False), FAIL),
    ("ESCD-03", "conflict raised",
     op("task", caps=["escd"], conflicts_with_record=True, contradiction_surfaced=True), PASS),
    ("ESCD-03", "conflict suppressed to stay agreeable",
     op("task", caps=["escd"], conflicts_with_record=True, contradiction_surfaced=False), FAIL),
    ("ESCD-04", "ambiguity routed",
     op("task", caps=["escd"], ambiguous=True, assumed_resolution=False), PASS),
    ("ESCD-04", "ambiguity guessed",
     op("task", caps=["escd"], ambiguous=True, assumed_resolution=True), FAIL),
    ("ESCD-05", "bounded execution",
     op("task", action="execute", caps=["escd"], confidence=0.9, authority_ref="a_1"), PASS),
    ("ESCD-05", "execution with no authority",
     op("task", action="execute", caps=["escd"], confidence=0.9), FAIL),

    # -- voice --------------------------------------------------------
    ("VOICE-01", "live authority",
     op("task", action="send", caps=["voice"], authority_expires_at=NOW), PASS),
    ("VOICE-01", "expired authority resolves to none",
     op("task", action="send", caps=["voice"], authority_expires_at=PAST), FAIL),
    ("VOICE-01", "no authority at all", op("task", action="send", caps=["voice"]), FAIL),
    ("VOICE-02", "recipient in scope",
     op("task", action="send", caps=["voice"], recipient="plumber",
        authorised_recipients=["plumber", "electrician"]), PASS),
    ("VOICE-02", "recipient outside scope",
     op("task", action="send", caps=["voice"], recipient="the bank",
        authorised_recipients=["plumber"]), FAIL),
    ("VOICE-02", "no scope is not an open scope",
     op("task", action="send", caps=["voice"], recipient="plumber"), FAIL),
    ("VOICE-03", "class in scope",
     op("task", action="send", caps=["voice"], message_class="confirm",
        authorised_classes=["confirm"]), PASS),
    ("VOICE-03", "confirming is not agreeing to terms",
     op("task", action="send", caps=["voice"], message_class="agree_terms",
        authorised_classes=["confirm"]), FAIL),
    ("VOICE-04", "ordinary lane", op("task", caps=["voice"], lanes_touched=["SC"]), PASS),
    ("VOICE-04", "protected material leaving its lane",
     op("task", caps=["voice"], lanes_touched=["SC", "PS"]), FAIL),
    ("VOICE-05", "transmission recorded",
     op("task", action="send", caps=["voice"], transmission_record="r_1",
        recipient="plumber", authority_ref="a_1"), PASS),
    ("VOICE-05", "sent with no readable record",
     op("task", action="send", caps=["voice"], recipient="plumber"), FAIL),

    # -- supabase -----------------------------------------------------
    ("SB-01", "write read back",
     op("asset", action="insert", caps=["supabase"], readback_verified=True), PASS),
    ("SB-01", "write reported, not confirmed",
     op("asset", action="insert", caps=["supabase"], readback_verified=False), FAIL),
    ("SB-02", "clean payload",
     op("asset", caps=["supabase"], payload="name = 'kitchen'"), PASS),
    ("SB-02", "credential shape in a row",
     op("asset", caps=["supabase"],
        payload="SERVICE_ROLE_KEY = 'NOTREAL_aaaaaaaaaaaaaaaaaaaaaaaa'"), FAIL),
    ("SB-03", "schema change via migration",
     op("asset", action="add_column", caps=["supabase"], migration_ref="m_12"), PASS),
    ("SB-03", "ad hoc ddl", op("asset", action="add_column", caps=["supabase"]), FAIL),
    ("SB-04", "destruction with a way back",
     op("asset", action="drop", caps=["supabase"], reversal_script="r.sql",
        backup_verified=True), PASS),
    ("SB-04", "destruction with an unverified backup",
     op("asset", action="drop", caps=["supabase"], reversal_script="r.sql",
        backup_verified=False), FAIL),
    ("SB-05", "agent role", op("asset", caps=["supabase"], uses_service_role=False), PASS),
    ("SB-05", "agent holding the service role",
     op("asset", caps=["supabase"], uses_service_role=True), FAIL),

    # -- github -------------------------------------------------------
    ("GH-01", "envelope complete",
     op("task", action="commit", caps=["github"], agent_id="a", agent_class="A2",
        directive="d", policy_hash=H), PASS),
    ("GH-01", "envelope missing the rulebook hash",
     op("task", action="commit", caps=["github"], agent_id="a", agent_class="A2",
        directive="d"), FAIL),
    ("GH-02", "approved namespace",
     op("task", action="push", caps=["github"], branch="fix/escd-build"), PASS),
    ("GH-02", "invented namespace",
     op("task", action="push", caps=["github"], branch="wip-scratch"), FAIL),
    ("GH-03", "live branch",
     op("task", action="merge", caps=["github"], branch_superseded=False), PASS),
    ("GH-03", "wholesale merge of a superseded branch",
     op("task", action="merge", caps=["github"], branch_superseded=True), FAIL),
    ("GH-04", "inside declared scope",
     op("task", action="push", caps=["github"], changed_paths=["apps/a.py"],
        declared_scope=["apps/"]), PASS),
    ("GH-04", "one file outside scope fails the whole transaction",
     op("task", action="push", caps=["github"], changed_paths=["apps/a.py", "policy/x.yaml"],
        declared_scope=["apps/"]), FAIL),
    ("GH-05", "clean diff", op("task", caps=["github"], diff="+ x = 1"), PASS),
    ("GH-05", "credential in an added line",
     op("task", caps=["github"], diff="+ AKIAZZZZZZZZZZZZZZZZ"), FAIL),

    # -- deployment ---------------------------------------------------
    ("DEP-01", "commit is on main",
     op("task", action="promote", caps=["deployment"], commit_sha="db8ed1f",
        is_ancestor_of_main=True), PASS),
    ("DEP-01", "commit is not on main",
     op("task", action="promote", caps=["deployment"], commit_sha="db8ed1f",
        is_ancestor_of_main=False), FAIL),
    ("DEP-02", "a real build produced a real artifact",
     op("task", action="promote", caps=["deployment"], build_output_path="public/",
        build_artifact_present=True, build_command_is_validator=False), PASS),
    ("DEP-02", "the validator is sitting in the build command slot",
     op("task", action="promote", caps=["deployment"],
        build_command_is_validator=True), FAIL),
    ("DEP-02", "gate passed and nothing was built",
     op("task", action="promote", caps=["deployment"], build_output_path=".next",
        build_artifact_present=False), FAIL),
    ("DEP-03", "preflight strict and passing",
     op("task", action="promote", caps=["deployment"], preflight_passed=True,
        preflight_allows_fallback=False), PASS),
    ("DEP-03", "a validator with a fallback validates nothing",
     op("task", action="promote", caps=["deployment"], preflight_passed=True,
        preflight_allows_fallback=True), FAIL),
    ("DEP-04", "author and promoter differ",
     op("task", action="promote", caps=["deployment"], author="codex", promoter="dcs"), PASS),
    ("DEP-04", "promoting your own change",
     op("task", action="promote", caps=["deployment"], author="dcs", promoter="dcs"), FAIL),
    ("DEP-05", "runtime probed",
     op("task", action="certify", caps=["deployment"], deployment_id="dpl_1",
        health_probe_passed=True), PASS),
    ("DEP-05", "ready is not healthy",
     op("task", action="certify", caps=["deployment"], deployment_id="dpl_1",
        health_probe_passed=False), FAIL),

    # -- file handling ------------------------------------------------
    ("FILE-01", "intake verified",
     op("asset", action="take", caps=["filehandling"], content_hash=H, readback_hash=H), PASS),
    ("FILE-01", "recorded without reading it back",
     op("asset", action="take", caps=["filehandling"], content_hash=H), FAIL),
    ("FILE-02", "one destination, pre-provisioned, resolving",
     op("asset", action="take", caps=["filehandling"], runtime_provisioned=False,
        fallback_used=False, storage_ref="files/aa/x", object_present=True), PASS),
    ("FILE-02", "application created its own bucket mid request",
     op("asset", action="take", caps=["filehandling"], runtime_provisioned=True,
        fallback_used=False, storage_ref="files/aa/x", object_present=True), FAIL),
    ("FILE-02", "fell back to a second destination",
     op("asset", action="take", caps=["filehandling"], runtime_provisioned=False,
        fallback_used=True, storage_ref="files/aa/x", object_present=True), FAIL),
    ("FILE-03", "reread supersedes",
     op("asset", action="reread", caps=["filehandling"], overwrites_prior_reading=False), PASS),
    ("FILE-03", "reread destroys the earlier reading",
     op("asset", action="reread", caps=["filehandling"], overwrites_prior_reading=True), FAIL),
    ("FILE-04", "frames cite their facts",
     op("asset", caps=["filehandling"], facts_list=["a"], facts=["a"],
        frames=["gap"], frame_derived_from=["f1"]), PASS),
    ("FILE-04", "a frame with no facts under it",
     op("asset", caps=["filehandling"], frames=["gap"]), FAIL),
    ("FILE-05", "desired state traces",
     op("asset", caps=["filehandling"], to_be="replace unit", objective_ref="obj_1"), PASS),
    ("FILE-05", "desired state with nothing behind it",
     op("asset", caps=["filehandling"], to_be="replace unit"), FAIL),
]


# ---------------------------------------------------------------------------

def run() -> int:
    failures: List[str] = []
    checked = 0

    print("\n  coverage")
    covered = {c[0] for c in CASES}
    registered = set(REGISTRY.ids())
    uncovered = sorted(registered - covered)
    unknown_ids = sorted(covered - registered)
    refuting = {c[0] for c in CASES if c[3] in (FAIL, UNKNOWN)}
    unrefuted = sorted(registered - refuting)

    def cov(label: str, ok: bool, detail: str = "") -> None:
        print("    %-4s %s%s" % ("PASS" if ok else "FAIL", label,
                                 "" if ok else ": " + detail))
        if not ok:
            failures.append(label)

    cov("every registered rule has a case", not uncovered, str(uncovered[:8]))
    cov("every case names a registered rule", not unknown_ids, str(unknown_ids[:8]))
    cov("every rule has been shown to refuse", not unrefuted, str(unrefuted[:8]))

    print("\n  rules  (%d registered, %d cases)" % (len(registered), len(CASES)))
    by_rule: Dict[str, List[str]] = {}
    for rule_id, label, operation, expected in CASES:
        checked += 1
        got = verdict(rule_id, operation)
        ok = got == expected
        by_rule.setdefault(rule_id, []).append("ok" if ok else "bad")
        if not ok:
            failures.append("%s %s" % (rule_id, label))
            print("    FAIL %-12s %-58s expected %s, got %s"
                  % (rule_id, label[:58], expected, got))
    for rule_id in sorted(by_rule):
        if all(x == "ok" for x in by_rule[rule_id]):
            print("    PASS %-12s %d cases" % (rule_id, len(by_rule[rule_id])))

    print("\n  orchestrator")
    orch_failures = orchestrator_cases()
    failures.extend(orch_failures)

    print("\n" + "=" * 72)
    print("  DCSE suite: %d rules, %d rule cases, %d failures"
          % (len(registered), checked, len(failures)))
    print("=" * 72 + "\n")
    return 0 if not failures else 1


def orchestrator_cases() -> List[str]:
    bad: List[str] = []

    def check(label: str, cond: bool, detail: str = "") -> None:
        print("    %-4s %s%s" % ("PASS" if cond else "FAIL", label,
                                 "" if cond else ": " + detail))
        if not cond:
            bad.append(label)

    # A candidate rule base blocks nothing. This is the shadow gate.
    o = Orchestrator()
    broken = op("task", action="complete", state="complete")
    out = o.run(broken, execute=False)
    check("candidate rules do not refuse anything",
          out.disposition in (EXECUTE, EXECUTE_AS_CANDIDATE, ESCALATE),
          out.disposition)
    check("but they are still evaluated and recorded",
          any(r.rule_id == "TASK-06" and r.verdict == FAIL for r in out.plan.results))
    check("and they are marked as shadow",
          all(not r.binding for r in out.plan.results))

    # Promote the set and the same operation is refused.
    REGISTRY.bind_all(PROVISIONAL)
    out2 = o.run(broken, execute=False)
    check("once binding, the same operation is refused",
          out2.disposition == REFUSE, out2.disposition)
    check("and the refusal names the rule", "TASK-06" in out2.reason, out2.reason)

    # A complete, valid task executes.
    good = op("task", action="complete", task_id="T-1", objective="x",
              acceptance_criteria=["c"], owner="DCS", state="complete",
              completion_evidence="ev")
    out3 = o.run(good, execute=False)
    check("a satisfied operation is permitted",
          out3.disposition in (EXECUTE, EXECUTE_AS_CANDIDATE), out3.disposition)

    # Missing knowledge escalates rather than refusing.
    thin = op("task", action="inspect", task_id="T-2")
    out4 = o.run(thin, execute=False)
    check("missing facts escalate rather than refuse",
          out4.disposition == ESCALATE, out4.disposition)

    # Irreversible work escalates even when every rule passes.
    send = op("task", action="send", caps=["voice"], task_id="T-3", objective="x",
              acceptance_criteria=["c"], owner="DCS", state="open",
              authority_expires_at=NOW, recipient="plumber",
              authorised_recipients=["plumber"], message_class="confirm",
              authorised_classes=["confirm"], lanes_touched=["SC"],
              transmission_record="r", authority_ref="a")
    out5 = o.run(send, execute=False)
    check("an irreversible act escalates with every rule passing",
          out5.disposition == ESCALATE, "%s / %s" % (out5.disposition, out5.reason))
    check("and no rule failed to get there", not out5.plan.failures())

    # Adapters: nothing claims to have acted when nothing is wired.
    out6 = o.run(good, execute=True)
    check("an unwired capability reports that it did nothing",
          out6.executed is False and "no adapter wired" in out6.execution.get("reason", ""),
          str(out6.execution))

    rec = Recording("task")
    wired = AdapterSet()
    wired.wire("escd", rec)
    o2 = Orchestrator(adapters=wired)
    good_escd = op("task", action="complete", caps=["escd"], task_id="T-4",
                   objective="x", acceptance_criteria=["c"], owner="DCS",
                   state="complete", completion_evidence="ev",
                   principal_intent="finish", interpretation="done",
                   interpretation_labelled=True)
    out7 = o2.run(good_escd, execute=True)
    check("a wired capability is actually called",
          out7.executed is True and len(rec.calls) == 1, str(out7.execution))

    # The register bridge records firings and refuses to promote on silence.
    try:
        sys.path.insert(0, "/home/claude/desk")
        import importlib
        rb_mod = importlib.import_module("rulebase")
        import tempfile, os
        tmp = tempfile.mkdtemp()
        rb = rb_mod.RuleBase(os.path.join(tmp, "r.sqlite3"))
        rb.propose(rule_id="TASK-06", name="Complete requires completion evidence",
                   klass=rb_mod.CONTROL, statement="x", origin_ref="suite")
        rb.bind_test("TASK-06", "suite: TASK-06 complete with no evidence", passing=True)
        from orchestrator import bridge_to_register
        o3 = Orchestrator(recorder=bridge_to_register(rb))
        for i in range(9):
            o3.run(op("task", action="complete", state="complete",
                      task_id="T-%d" % i), execute=False)
        life, why = rb.reassess("TASK-06")
        check("firings reach the register", rb.stats("TASK-06")["fired"] >= 9)
        check("nine unvalidated firings do not promote the rule",
              life == rb_mod.PROVISIONAL, "%s / %s" % (life, why))
    except Exception as exc:  # noqa: BLE001
        check("register bridge", False, "%s: %s" % (type(exc).__name__, exc))

    # Delegation and rule staging verification
    import delegation
    packets = delegation.load_all()
    check("delegation packets loaded", len(packets) == 4)
    for p in packets:
        p.validate()
    check("all 4 packets validate", True)

    try:
        delegation.TaskPacket(id="T-ERR1", title="x", objective="y", issued_by="me",
                              directive="DIR", capabilities=("github",), scope=("foo/",),
                              steps=("step1",), reconciliation="HOLD_DCS", reconciliation_note="",
                              action="edit", entity="task", status="open",
                              acceptance=[delegation.Acceptance("cmd", "exp")]).validate()
        check("reject hold without note", False)
    except delegation.InvalidPacket:
        check("reject hold without note", True)

    try:
        delegation.TaskPacket(id="T-ERR2", title="x", objective="y", issued_by="me",
                              directive="DIR", capabilities=("github",), scope=("foo/",),
                              steps=("step1",), reconciliation="READY", reconciliation_note="",
                              action="edit", entity="task", status="done",
                              acceptance=[delegation.Acceptance("cmd", "exp")]).validate()
        check("reject status done in packet", False)
    except delegation.InvalidPacket:
        check("reject status done in packet", True)

    try:
        delegation.TaskPacket(id="T-ERR3", title="x", objective="y", issued_by="me",
                              directive="DIR", capabilities=("github",), scope=("foo/",),
                              steps=("step1",), reconciliation="READY", reconciliation_note="",
                              action="edit", entity="task", status="open",
                              acceptance=[delegation.Acceptance("", "exp")]).validate()
        check("reject empty acceptance command", False)
    except delegation.InvalidPacket:
        check("reject empty acceptance command", True)

    t2 = [p for p in packets if p.id == "T-002"][0]
    t2_op = t2.operation()
    plan_rules = o.resolve(t2_op, stage="plan")
    check("plan stage skips evidence rules", "GH-05" not in [r.id for r in plan_rules])
    plan_out = o.run(t2_op, execute=False, stage="plan")
    check("plan stage allows reversible attempt without premature diff escalation",
          plan_out.disposition in (EXECUTE, EXECUTE_AS_CANDIDATE),
          plan_out.disposition)

    ev_rules = o.resolve(t2_op, stage="evidence")
    check("evidence stage includes GH-05", "GH-05" in [r.id for r in ev_rules])
    ev_out = o.run(t2_op, execute=False, stage="evidence")
    gh05_res = [r for r in ev_out.plan.results if r.rule_id == "GH-05"]
    check("evidence stage preserves UNKNOWN without evidence",
          bool(gh05_res and gh05_res[0].verdict == UNKNOWN))

    d_t001 = [p for p in packets if p.id == "T-001"][0].disposition(o)
    d_t002 = [p for p in packets if p.id == "T-002"][0].disposition(o)
    d_t003 = [p for p in packets if p.id == "T-003"][0].disposition(o)
    d_t004 = [p for p in packets if p.id == "T-004"][0].disposition(o)

    check("T-001 held by DCS", d_t001["needs_approval"] == "True" and "HOLD_DCS" in d_t001["reason"])
    check("T-002 ready for auto", d_t002["needs_approval"] == "False" and d_t002["disposition"] in (EXECUTE, EXECUTE_AS_CANDIDATE))
    check("T-003 held by DCS", d_t003["needs_approval"] == "True" and "HOLD_DCS" in d_t003["reason"])
    check("T-004 stale reconcile", d_t004["needs_approval"] == "True" and "STALE_RECONCILE" in d_t004["reason"])

    runnable = delegation.next_open(packets)
    check("only T-002 is runnable next", [r.id for r in runnable] == ["T-002"])

    return bad


if __name__ == "__main__":
    raise SystemExit(run())
