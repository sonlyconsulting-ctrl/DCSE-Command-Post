"""Rule register: the object a self-improving rule base is made of.

A rule base that grows is easy. A rule base that gets smaller and stronger
needs three things this module provides.

    A LIFECYCLE      candidate, provisional, active, deprecated, retired, with
                     transitions that fire on recorded evidence rather than on
                     somebody deciding it is time.

    AN ORIGIN        every rule points at what produced it. A rule with no
                     origin cannot be re-examined when its evidence turns out
                     to be wrong.

    A HISTORY        every firing is recorded with its outcome and, when the
                     outcome was validated, by WHAT. That last part is the one
                     that keeps the loop honest.

The trap this module exists to avoid: a rule fires, nothing contradicts it,
the absence of contradiction is read as success, the pattern is promoted, and
the rule base has now learned its own bias and called it doctrine. Absence of
contradiction is not confirmation. So an outcome counts as validated only when
it names an independent source: reality, a person, or a second evaluator that
did not produce the decision.

Standard library only. Same reversibility model as the rest: every change is
recorded with the row as it was before.
"""
from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import time
import uuid
from typing import Any, Dict, Iterable, List, Optional, Tuple

# -- lifecycle -------------------------------------------------------------

CANDIDATE = "candidate"      # proposed, not yet usable
PROVISIONAL = "provisional"  # usable, watched, outcomes count double
ACTIVE = "active"            # earned its place
DEPRECATED = "deprecated"    # failing, superseded, or never used
RETIRED = "retired"          # out of service, kept as history

LIFECYCLE = (CANDIDATE, PROVISIONAL, ACTIVE, DEPRECATED, RETIRED)

# -- rule classes ----------------------------------------------------------

EXTRACTION = "extraction"          # source material into facts
CLASSIFICATION = "classification"  # what a fact represents
TRANSFORMATION = "transformation"  # create, update or link governed objects
CONTROL = "control"                # whether execution is permitted, and how
VALIDATION = "validation"          # whether a result is complete and coherent

CLASSES = (EXTRACTION, CLASSIFICATION, TRANSFORMATION, CONTROL, VALIDATION)

# -- reversibility, which decides the control level ------------------------

REVERSIBLE = "reversible"                  # undo leaves no residue
RESIDUAL = "reversible_with_residue"       # undo works but costs something
IRREVERSIBLE = "irreversible"              # there is no before to return to

EXECUTE = "execute"                        # act, record, move on
EXECUTE_AS_CANDIDATE = "execute_as_candidate"   # act into a draft layer
ESCALATE = "escalate"                      # a person decides

# Consequence is the second axis. Reversibility alone is not enough: a
# migration may be technically reversible and still unacceptable to run
# unvalidated against production.
LOW, MODERATE, HIGH = "low", "moderate", "high"


def control_for(reversibility: str, consequence: str) -> str:
    """The gate minimization principle, as a function rather than a paragraph.

    A gate is not the default. It must earn its operational cost, because a
    gate that fires constantly stops being read.
    """
    if reversibility == IRREVERSIBLE:
        return ESCALATE
    if consequence == HIGH:
        return ESCALATE
    if reversibility == RESIDUAL or consequence == MODERATE:
        return EXECUTE_AS_CANDIDATE
    return EXECUTE


# -- validation sources ----------------------------------------------------
# An outcome is validated only by something that did not produce it.

REALITY = "reality"            # the deploy worked, the hash matched, the test ran
PERSON = "person"              # a human decided
SECOND_EVALUATOR = "second"    # an independent evaluation agreed
SELF = "self"                  # the rule's own evaluator. NOT validation.
SILENCE = "silence"            # nobody complained. NOT validation.

INDEPENDENT_SOURCES = (REALITY, PERSON, SECOND_EVALUATOR)

# -- thresholds, stated once so they can be argued with --------------------

PROMOTE_MIN_VALIDATED = 5      # independently validated firings, candidate to provisional to active
PROMOTE_MIN_DISTINCT_INPUTS = 3  # from distinct input signatures, not five reruns of one case
DEMOTE_EXCEPTION_RATE = 0.25   # exceptions over firings, in the window
BROAD_MATCH_CEILING = 0.60     # a rule matching most of everything is matching nothing
STALE_WINDOW_DAYS = 90         # no firings in this long while inputs flowed
LOSS_STREAK = 8                # generated as a candidate this often, never selected

SCHEMA = """
PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS rule (
    id             TEXT PRIMARY KEY,
    name           TEXT NOT NULL,
    class          TEXT NOT NULL,
    statement      TEXT NOT NULL,
    predicate      TEXT NOT NULL DEFAULT '',
    lane           TEXT NOT NULL DEFAULT 'DCSE',
    scope          TEXT NOT NULL DEFAULT '',
    lifecycle      TEXT NOT NULL DEFAULT 'candidate',
    reversibility  TEXT NOT NULL DEFAULT 'reversible',
    consequence    TEXT NOT NULL DEFAULT 'low',
    control        TEXT NOT NULL DEFAULT 'execute',
    origin_kind    TEXT NOT NULL DEFAULT 'stated',
    origin_ref     TEXT NOT NULL DEFAULT '',
    proposed_by    TEXT NOT NULL DEFAULT '',
    proposed_at    REAL NOT NULL,
    activated_at   REAL,
    deprecated_at  REAL,
    supersedes     TEXT,
    superseded_by  TEXT,
    version        INTEGER NOT NULL DEFAULT 1,
    body_hash      TEXT NOT NULL DEFAULT '',
    notes          TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS rule_life ON rule(lifecycle, class);

CREATE TABLE IF NOT EXISTS rule_test (
    id       TEXT PRIMARY KEY,
    rule_id  TEXT NOT NULL REFERENCES rule(id),
    name     TEXT NOT NULL,
    passing  INTEGER NOT NULL DEFAULT 0,
    last_run REAL
);

-- One row per time a rule was applied. input_sig groups reruns of the same
-- case so five repeats of one situation cannot look like five confirmations.
CREATE TABLE IF NOT EXISTS firing (
    id            TEXT PRIMARY KEY,
    rule_id       TEXT NOT NULL REFERENCES rule(id),
    at            REAL NOT NULL,
    input_sig     TEXT NOT NULL,
    matched       INTEGER NOT NULL DEFAULT 1,
    selected      INTEGER NOT NULL DEFAULT 1,
    outcome       TEXT NOT NULL DEFAULT 'unknown',
    validated_by  TEXT NOT NULL DEFAULT 'silence',
    exception     INTEGER NOT NULL DEFAULT 0,
    override      INTEGER NOT NULL DEFAULT 0,
    detail        TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS firing_rule ON firing(rule_id, at DESC);
CREATE INDEX IF NOT EXISTS firing_sig  ON firing(input_sig);

-- Candidate transformations that were generated but not chosen. A design that
-- keeps losing is telling you something about the generator.
CREATE TABLE IF NOT EXISTS candidate_outcome (
    id           TEXT PRIMARY KEY,
    at           REAL NOT NULL,
    input_sig    TEXT NOT NULL,
    shape_hash   TEXT NOT NULL,
    label        TEXT NOT NULL DEFAULT '',
    selected     INTEGER NOT NULL DEFAULT 0,
    merged       INTEGER NOT NULL DEFAULT 0,
    score        REAL,
    validated_by TEXT NOT NULL DEFAULT 'silence'
);
CREATE INDEX IF NOT EXISTS cand_shape ON candidate_outcome(shape_hash);

CREATE TABLE IF NOT EXISTS event (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    at        REAL NOT NULL,
    action    TEXT NOT NULL,
    tbl       TEXT NOT NULL,
    row_id    TEXT NOT NULL,
    before    TEXT,
    after     TEXT,
    label     TEXT NOT NULL DEFAULT '',
    undone_at REAL
);
"""


def now() -> float:
    return time.time()


def new_id(p: str) -> str:
    return p + "_" + uuid.uuid4().hex[:12]


def sig(*parts: Any) -> str:
    """A stable signature for a set of inputs, so 'repeated' means repeated
    across different cases rather than the same case five times."""
    raw = "\x1f".join(str(p) for p in parts)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


class RuleBase:
    def __init__(self, path: str):
        self.path = os.path.abspath(path)
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.db.commit()

    # -- writes, all reversible -------------------------------------------

    def _event(self, action: str, tbl: str, row_id: str,
               before: Optional[Dict], after: Optional[Dict], label: str) -> None:
        self.db.execute(
            "INSERT INTO event(at, action, tbl, row_id, before, after, label) "
            "VALUES(?,?,?,?,?,?,?)",
            (now(), action, tbl, row_id,
             json.dumps(before) if before else None,
             json.dumps(after) if after else None, label))

    def rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        r = self.db.execute("SELECT * FROM rule WHERE id = ?", (rule_id,)).fetchone()
        return dict(r) if r else None

    def propose(self, rule_id: str, name: str, klass: str, statement: str,
                predicate: str = "", lane: str = "DCSE", scope: str = "",
                reversibility: str = REVERSIBLE, consequence: str = LOW,
                origin_kind: str = "stated", origin_ref: str = "",
                proposed_by: str = "", notes: str = "",
                supersedes: Optional[str] = None) -> Dict[str, Any]:
        """Every rule enters as a candidate. Nothing is born active."""
        if klass not in CLASSES:
            raise ValueError("unknown rule class: %s" % klass)
        body = "\x1f".join([statement, predicate, klass, scope])
        rec = {
            "id": rule_id, "name": name, "class": klass, "statement": statement,
            "predicate": predicate, "lane": lane, "scope": scope,
            "lifecycle": CANDIDATE, "reversibility": reversibility,
            "consequence": consequence,
            "control": control_for(reversibility, consequence),
            "origin_kind": origin_kind, "origin_ref": origin_ref,
            "proposed_by": proposed_by, "proposed_at": now(),
            "activated_at": None, "deprecated_at": None,
            "supersedes": supersedes, "superseded_by": None, "version": 1,
            "body_hash": hashlib.sha256(body.encode("utf-8")).hexdigest(),
            "notes": notes,
        }
        cols = ",".join(rec)
        marks = ",".join(":" + k for k in rec)
        self.db.execute("INSERT INTO rule(%s) VALUES(%s)" % (cols, marks), rec)
        self._event("insert", "rule", rule_id, None, rec, "proposed " + name)
        if supersedes:
            self.db.execute("UPDATE rule SET superseded_by = ? WHERE id = ?",
                            (rule_id, supersedes))
        self.db.commit()
        return rec

    def bind_test(self, rule_id: str, test_name: str, passing: bool = False) -> None:
        tid = new_id("t")
        self.db.execute(
            "INSERT INTO rule_test(id, rule_id, name, passing, last_run) VALUES(?,?,?,?,?)",
            (tid, rule_id, test_name, 1 if passing else 0, now() if passing else None))
        self._event("insert", "rule_test", tid, None,
                    {"rule_id": rule_id, "name": test_name}, "bound test")
        self.db.commit()

    def set_test_result(self, rule_id: str, test_name: str, passing: bool) -> None:
        self.db.execute(
            "UPDATE rule_test SET passing = ?, last_run = ? WHERE rule_id = ? AND name = ?",
            (1 if passing else 0, now(), rule_id, test_name))
        self.db.commit()

    def record_firing(self, rule_id: str, input_sig: str, matched: bool = True,
                      selected: bool = True, outcome: str = "ok",
                      validated_by: str = SILENCE, exception: bool = False,
                      override: bool = False, detail: str = "") -> str:
        fid = new_id("f")
        self.db.execute(
            "INSERT INTO firing(id, rule_id, at, input_sig, matched, selected, "
            "outcome, validated_by, exception, override, detail) "
            "VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            (fid, rule_id, now(), input_sig, int(matched), int(selected), outcome,
             validated_by, int(exception), int(override), detail))
        self.db.commit()
        return fid

    def record_candidate(self, input_sig: str, label: str, shape: Any,
                         selected: bool = False, merged: bool = False,
                         score: Optional[float] = None,
                         validated_by: str = SILENCE) -> str:
        cid = new_id("c")
        self.db.execute(
            "INSERT INTO candidate_outcome(id, at, input_sig, shape_hash, label, "
            "selected, merged, score, validated_by) VALUES(?,?,?,?,?,?,?,?,?)",
            (cid, now(), input_sig, sig(json.dumps(shape, sort_keys=True)), label,
             int(selected), int(merged), score, validated_by))
        self.db.commit()
        return cid

    # -- the loop ---------------------------------------------------------

    def stats(self, rule_id: str, window_days: Optional[int] = None) -> Dict[str, Any]:
        where, args = "rule_id = ?", [rule_id]
        if window_days:
            where += " AND at >= ?"
            args.append(now() - window_days * 86400)
        rows = [dict(r) for r in self.db.execute(
            "SELECT * FROM firing WHERE " + where, args)]
        fired = len(rows)
        matched = sum(1 for r in rows if r["matched"])
        selected = sum(1 for r in rows if r["selected"])
        exceptions = sum(1 for r in rows if r["exception"])
        overrides = sum(1 for r in rows if r["override"])
        validated = [r for r in rows
                     if r["validated_by"] in INDEPENDENT_SOURCES and not r["exception"]]
        return {
            "fired": fired, "matched": matched, "selected": selected,
            "exceptions": exceptions, "overrides": overrides,
            "validated": len(validated),
            "distinct_validated_inputs": len({r["input_sig"] for r in validated}),
            "exception_rate": (exceptions / fired) if fired else 0.0,
            "match_rate": (matched / fired) if fired else 0.0,
            "last_fired": max((r["at"] for r in rows), default=None),
            "by_source": {s: sum(1 for r in rows if r["validated_by"] == s)
                          for s in (REALITY, PERSON, SECOND_EVALUATOR, SELF, SILENCE)},
        }

    def _move(self, rule_id: str, to: str, why: str) -> Dict[str, Any]:
        before = self.rule(rule_id)
        if not before:
            raise KeyError(rule_id)
        after = dict(before)
        after["lifecycle"] = to
        if to == ACTIVE:
            after["activated_at"] = now()
        if to in (DEPRECATED, RETIRED):
            after["deprecated_at"] = now()
        self.db.execute(
            "UPDATE rule SET lifecycle = ?, activated_at = ?, deprecated_at = ?, "
            "notes = ? WHERE id = ?",
            (to, after["activated_at"], after["deprecated_at"],
             (before["notes"] + "\n" if before["notes"] else "") + why, rule_id))
        after["notes"] = (before["notes"] + "\n" if before["notes"] else "") + why
        self._event("update", "rule", rule_id, before, after,
                    "%s -> %s" % (before["lifecycle"], to))
        self.db.commit()
        return after

    def reassess(self, rule_id: str) -> Tuple[str, str]:
        """Deterministic lifecycle. Returns (lifecycle, reason).

        Nothing here is a judgment call. If you disagree with a transition,
        the threshold is the thing to argue with, and it is a named constant.
        """
        r = self.rule(rule_id)
        if not r:
            raise KeyError(rule_id)
        life = r["lifecycle"]
        if life == RETIRED:
            return life, "retired, no further transitions"
        if r["superseded_by"]:
            if life != DEPRECATED:
                self._move(rule_id, DEPRECATED, "superseded by " + r["superseded_by"])
            return DEPRECATED, "superseded by " + r["superseded_by"]

        tests = [dict(t) for t in self.db.execute(
            "SELECT * FROM rule_test WHERE rule_id = ?", (rule_id,))]
        s = self.stats(rule_id)
        s_win = self.stats(rule_id, STALE_WINDOW_DAYS)

        # candidate to provisional: it has to be testable and tested.
        if life == CANDIDATE:
            if not tests:
                return life, "no bound test, so it cannot be shown to work"
            if not all(t["passing"] for t in tests):
                return life, "bound tests are not all passing"
            if not r["origin_ref"]:
                return life, "no origin evidence recorded"
            self._move(rule_id, PROVISIONAL,
                       "tests bound and passing, origin recorded")
            return PROVISIONAL, "promoted on tests and origin"

        # demotion beats promotion. A rule earning its way up while failing in
        # practice is the exact thing that should not happen.
        if s_win["fired"] and s_win["exception_rate"] > DEMOTE_EXCEPTION_RATE:
            if life != DEPRECATED:
                self._move(rule_id, DEPRECATED,
                           "exception rate %.0f%% over %d firings, above the %.0f%% ceiling"
                           % (s_win["exception_rate"] * 100, s_win["fired"],
                              DEMOTE_EXCEPTION_RATE * 100))
            return DEPRECATED, "exception rate above ceiling"

        if life == PROVISIONAL:
            if s["validated"] < PROMOTE_MIN_VALIDATED:
                return life, ("%d independently validated firings, needs %d"
                              % (s["validated"], PROMOTE_MIN_VALIDATED))
            if s["distinct_validated_inputs"] < PROMOTE_MIN_DISTINCT_INPUTS:
                return life, ("validated on %d distinct cases, needs %d. Five reruns "
                              "of one case is one confirmation."
                              % (s["distinct_validated_inputs"],
                                 PROMOTE_MIN_DISTINCT_INPUTS))
            self._move(rule_id, ACTIVE,
                       "%d validated firings across %d distinct cases"
                       % (s["validated"], s["distinct_validated_inputs"]))
            return ACTIVE, "promoted on independent validation"

        if life == ACTIVE and s_win["fired"] == 0:
            self._move(rule_id, DEPRECATED,
                       "no firings in %d days" % STALE_WINDOW_DAYS)
            return DEPRECATED, "stale, never fires"

        return life, "no transition warranted"

    def reassess_all(self) -> List[Tuple[str, str, str]]:
        out = []
        for r in self.db.execute("SELECT id FROM rule ORDER BY id"):
            life, why = self.reassess(r["id"])
            out.append((r["id"], life, why))
        return out

    # -- health, the part that keeps the base small ------------------------

    def health(self) -> List[Dict[str, Any]]:
        """Eight findings. Each is a fact about the register, not an opinion
        about a rule."""
        f: List[Dict[str, Any]] = []
        rules = [dict(r) for r in self.db.execute(
            "SELECT * FROM rule WHERE lifecycle NOT IN ('retired')")]
        by_id = {r["id"]: r for r in rules}

        # 1. duplicate: identical body.
        seen: Dict[str, str] = {}
        for r in rules:
            key = r["body_hash"]
            if key in seen:
                f.append({"check": "duplicate", "rule": r["id"],
                          "detail": "same statement and predicate as " + seen[key]})
            else:
                seen[key] = r["id"]

        # 2. overlapping: two rules firing on the same inputs most of the time.
        sigs: Dict[str, set] = {}
        for r in rules:
            sigs[r["id"]] = {x["input_sig"] for x in self.db.execute(
                "SELECT DISTINCT input_sig FROM firing WHERE rule_id = ? AND matched = 1",
                (r["id"],))}
        ids = sorted(sigs)
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if not sigs[a] or not sigs[b]:
                    continue
                if by_id[a]["class"] != by_id[b]["class"]:
                    continue
                shared = len(sigs[a] & sigs[b])
                smaller = min(len(sigs[a]), len(sigs[b]))
                if smaller >= 3 and shared / smaller >= 0.8:
                    f.append({"check": "overlapping", "rule": a,
                              "detail": "fires on %d of %s's %d inputs, consider merging"
                                        % (shared, b, smaller)})

        # 3. contradictory: same input, incompatible outcomes.
        rows = [dict(x) for x in self.db.execute(
            "SELECT rule_id, input_sig, outcome FROM firing WHERE matched = 1")]
        by_sig: Dict[str, Dict[str, set]] = {}
        for x in rows:
            by_sig.setdefault(x["input_sig"], {}).setdefault(x["rule_id"], set()).add(
                x["outcome"])
        for s, per_rule in by_sig.items():
            outcomes = {o for outs in per_rule.values() for o in outs}
            if len(per_rule) > 1 and len(outcomes) > 1 and "unknown" not in outcomes:
                f.append({"check": "contradictory", "rule": ",".join(sorted(per_rule)),
                          "detail": "same input produced %s" % sorted(outcomes)})

        # 4. never fires.
        for r in rules:
            if r["lifecycle"] in (ACTIVE, PROVISIONAL):
                st = self.stats(r["id"], STALE_WINDOW_DAYS)
                if st["fired"] == 0:
                    f.append({"check": "never_fires", "rule": r["id"],
                              "detail": "no firings in %d days" % STALE_WINDOW_DAYS})

        # 5. fires too broadly. A matcher that catches most of everything has
        #    stopped discriminating. This is the shape of the classic bug where
        #    a bare negation pattern swallows half a document.
        for r in rules:
            st = self.stats(r["id"])
            if st["fired"] >= 20 and st["match_rate"] > BROAD_MATCH_CEILING:
                f.append({"check": "fires_too_broadly", "rule": r["id"],
                          "detail": "matches %.0f%% of inputs seen, above the %.0f%% ceiling"
                                    % (st["match_rate"] * 100, BROAD_MATCH_CEILING * 100)})

        # 6. repeatedly loses.
        for r in rules:
            st = self.stats(r["id"])
            losses = st["fired"] - st["selected"]
            if losses >= LOSS_STREAK and st["selected"] == 0:
                f.append({"check": "repeatedly_loses", "rule": r["id"],
                          "detail": "generated %d times, never selected" % losses})

        # 7. exception rate climbing.
        for r in rules:
            st = self.stats(r["id"], STALE_WINDOW_DAYS)
            if st["fired"] >= 8 and st["exception_rate"] > DEMOTE_EXCEPTION_RATE / 2:
                f.append({"check": "exceptions_climbing", "rule": r["id"],
                          "detail": "%.0f%% exceptions over %d firings"
                                    % (st["exception_rate"] * 100, st["fired"])})

        # 8. convergent transformations: the same generated shape keeps winning
        #    across different cases. That is a deterministic rule waiting to be
        #    written, which is the whole point of the loop.
        conv = self.db.execute(
            "SELECT shape_hash, label, COUNT(DISTINCT input_sig) cases, COUNT(*) n "
            "FROM candidate_outcome WHERE selected = 1 "
            "AND validated_by IN ('reality','person','second') "
            "GROUP BY shape_hash HAVING cases >= ?", (PROMOTE_MIN_DISTINCT_INPUTS,))
        for c in conv:
            f.append({"check": "convergent", "rule": "(generative)",
                      "detail": "'%s' selected and validated across %d distinct cases, "
                                "encode it deterministically" % (c["label"], c["cases"])})
        return f

    # -- reporting ---------------------------------------------------------

    def summary(self) -> Dict[str, Any]:
        counts = {l: self.db.execute(
            "SELECT COUNT(*) c FROM rule WHERE lifecycle = ?", (l,)).fetchone()["c"]
            for l in LIFECYCLE}
        by_class = {k: self.db.execute(
            "SELECT COUNT(*) c FROM rule WHERE class = ? AND lifecycle NOT IN "
            "('retired','deprecated')", (k,)).fetchone()["c"] for k in CLASSES}
        by_control = {k: self.db.execute(
            "SELECT COUNT(*) c FROM rule WHERE control = ? AND lifecycle NOT IN "
            "('retired','deprecated')", (k,)).fetchone()["c"]
            for k in (EXECUTE, EXECUTE_AS_CANDIDATE, ESCALATE)}
        return {"lifecycle": counts, "by_class": by_class, "by_control": by_control,
                "firings": self.db.execute("SELECT COUNT(*) c FROM firing").fetchone()["c"]}

    def table(self, lifecycle: Optional[str] = None) -> str:
        sql = "SELECT * FROM rule"
        args: List[Any] = []
        if lifecycle:
            sql += " WHERE lifecycle = ?"
            args.append(lifecycle)
        sql += " ORDER BY class, id"
        rows = [dict(r) for r in self.db.execute(sql, args)]
        if not rows:
            return "  (none)"
        w = max(len(r["id"]) for r in rows) + 2
        out = []
        for r in rows:
            out.append("  %-*s %-15s %-12s %-20s %s"
                       % (w, r["id"], r["class"], r["lifecycle"], r["control"],
                          r["name"]))
        return "\n".join(out)


# ---------------------------------------------------------------------------
# Seed: the doctrine this session actually produced, with its origin evidence.
# Filed as candidates, because nothing is born active.
# ---------------------------------------------------------------------------

SESSION = "session/2026-09-13 ESCD Phase 1 correction and v7.2 rule program"

SEED: List[Dict[str, Any]] = [
    dict(rule_id="CTL-GATE-MIN-001", name="Gate minimization",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Governance does not use a gate where evidence, bounded authority, "
                    "deterministic validation and reliable reversibility give a cheaper "
                    "and stronger control. A gate must earn its operational cost."),
         predicate="control_for(reversibility, consequence)",
         origin_ref=SESSION + " / stated by DCS",
         notes="A gate that fires constantly stops being read. That is its failure mode."),

    dict(rule_id="CTL-REV-002", name="Reversibility decides the control level",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Reversible and low consequence executes. Residual or moderate "
                    "executes into a candidate layer. Irreversible or high consequence "
                    "escalates. Reversibility alone is not sufficient: an action that "
                    "can be reversed may still have an unacceptable interim consequence."),
         predicate="reversibility x consequence -> execute | candidate | escalate",
         origin_ref=SESSION + " / DCS correction to the absolute form"),

    dict(rule_id="CTL-VALID-SRC-003", name="Validation must be independent",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("An outcome counts as validated only when it names a source that "
                    "did not produce it: reality, a person, or a second evaluator. "
                    "Absence of contradiction is not confirmation."),
         predicate="validated_by in (reality, person, second)",
         origin_ref=SESSION + " / the five ESCD defects, each found after the fact",
         notes=("Without this the learning loop promotes its own evaluator's bias "
                "into doctrine and calls it experience.")),

    dict(rule_id="CTL-DEST-004", name="A destination must resolve",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=HIGH,
         statement=("An operation writing to storage is permitted only when a single "
                    "pre-provisioned destination resolves, the object is confirmed "
                    "present, and the metadata references it. Any one false denies "
                    "the whole operation and writes no metadata."),
         predicate="exists(dest) and write_ok and readback_hash == write_hash",
         origin_ref=SESSION + " / ESCD attachment defect, and Desk store.put_blob",
         notes="Replace 'defined' with 'resolves' wherever it appears."),

    dict(rule_id="VAL-FACT-FRAME-005", name="Facts and frames are separate objects",
         klass=VALIDATION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("A fact records what the evidence establishes. A frame records an "
                    "interpretation of that fact against an objective. 'RCD protection "
                    "is absent' is a fact; calling it a gap is a frame. They are stored "
                    "as different objects with a link, never merged."),
         predicate="fact.id != frame.id and frame.derived_from includes fact.id",
         origin_ref=SESSION + " / stated by DCS"),

    dict(rule_id="VAL-ABSTAIN-006", name="Abstain rather than invent",
         klass=VALIDATION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Material that cannot be classified with confidence is retained as "
                    "UNCLASSIFIED with its source. It is never dropped silently and "
                    "never assigned a class to populate a field."),
         predicate="confidence < threshold -> status = UNCLASSIFIED, value = null",
         origin_ref=SESSION + " / DCS amendment to Desk's drop behaviour",
         notes=("Desk drops, which suits a personal tool. Enterprise evidence is "
                "retained, because an unread line may matter later.")),

    dict(rule_id="VAL-TOBE-TRACE-007", name="To-Be must trace to an objective",
         klass=VALIDATION, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("A desired-state statement is valid only when it traces to a stated "
                    "objective, requirement, doctrine reference or explicit direction. "
                    "A To-Be with no trace is a proposal, labelled as one."),
         predicate="to_be.traces_to is not null else status = PROPOSAL",
         origin_ref=SESSION + " / DCS, on AI-generated wishful thinking"),

    dict(rule_id="CLS-GAP-DEF-008", name="Gap is a computed difference",
         klass=CLASSIFICATION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("GAP equals the required or desired condition minus the verified "
                    "as-is condition. It is not the set of sentences containing "
                    "negative words."),
         predicate="gap = required_condition - verified_as_is",
         origin_ref=SESSION + " / DCS",
         notes=("Lexical negation detection is a first-pass extractor feeding this, "
                "not a substitute for it.")),

    dict(rule_id="EXT-WORDBOUND-009", name="Lexical matching respects word boundaries",
         klass=EXTRACTION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Phrase matching over source text anchors on word boundaries. "
                    "Substring matching produces false classifications that read as "
                    "confident findings."),
         predicate=r"(?<!\w)phrase(?!\w)",
         origin_ref=SESSION + " / 'installed' matched 'stalled' and filed a fact as a failure",
         notes="Caught by a test, not by review. The test is the control here."),

    dict(rule_id="EXT-NEGATION-010", name="Negation indicates absence",
         klass=EXTRACTION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Auxiliary plus not, contractions, and 'no X is present' forms "
                    "indicate an absence regardless of the grammatical tense."),
         predicate=r"(is|are|has|have|was|were)\s+not | no\s+\w+\s+(is|are|was)\s+present",
         origin_ref=SESSION + " / 'No RCD protection is present' read as a condition",
         notes=("WATCH: the bare 'not <word>' arm of this rule is a "
                "fires-too-broadly candidate. Measure its match rate before "
                "promoting it past provisional.")),

    dict(rule_id="TRF-SUPERSEDE-011", name="Derivations supersede, never overwrite",
         klass=TRANSFORMATION, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Rereading, reframing or regenerating produces a new derived "
                    "version and marks the previous one superseded. The earlier "
                    "derivation is retained."),
         predicate="new.supersedes = old.id; old.superseded_by = new.id",
         origin_ref=SESSION + " / Desk store.save_reading and save_frame"),

    dict(rule_id="TRF-BOUNDED-GEN-012", name="Bounded generative transformation",
         klass=TRANSFORMATION, reversibility=RESIDUAL, consequence=MODERATE,
         statement=("Where several conforming representations are possible, the "
                    "generator produces alternatives and a deterministic evaluator "
                    "scores them against fidelity, objective fit, doctrine fit, reuse, "
                    "duplication, extensibility, complexity, traceability, "
                    "reversibility, interoperability, completeness and assumptions. "
                    "Selection and merging are deterministic; generation is not."),
         predicate="generate(n) -> score(criteria) -> select|merge|escalate",
         origin_ref=SESSION + " / DCS, on creativity with conformity",
         notes=("Escalate only when two materially different options score within "
                "tolerance, or an unsupported assumption determines the design.")),

    dict(rule_id="CTL-PROMOTE-013", name="Repeated validated decisions become rules",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("A generative decision pattern validated independently across at "
                    "least three distinct input signatures becomes a candidate "
                    "deterministic rule. Repeats of one case count once."),
         predicate="distinct_validated_inputs >= 3 -> propose deterministic rule",
         origin_ref=SESSION + " / DCS learning loop, with the input-matching correction"),

    dict(rule_id="CTL-DEMOTE-014", name="Repeated exceptions demote a rule",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("A rule whose exception rate exceeds the ceiling over its window "
                    "is deprecated for revision rather than left active. A rule that "
                    "has not fired within the stale window is deprecated as unused."),
         predicate="exception_rate > 0.25 or fired_in_window == 0 -> deprecate",
         origin_ref=SESSION + " / DCS rule quality alert"),
# -- Acting on behalf of a principal ----------------------------------
    # A senior assistant does something a document system never does: it acts
    # in someone else's name. That is where the irreversible class lives, and
    # it stops being an edge case and becomes the dominant one.

    dict(rule_id="ACT-TRANSMIT-015", name="Transmission in the principal's name escalates",
         klass=CONTROL, reversibility=IRREVERSIBLE, consequence=HIGH,
         statement=("Any act that reaches another person in the principal's name "
                    "is irreversible and escalates, absent a bounded standing "
                    "authority covering that recipient class, message class and "
                    "time window. A correction can be sent. Nothing can be unsent."),
         predicate="reaches_third_party and in_principal_name -> escalate unless standing_authority",
         origin_ref=SESSION + " / ESCD reframed as the DCSE personal assistant"),

    dict(rule_id="ACT-DRAFT-016", name="Draft freely, send never without authority",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=LOW,
         statement=("Composition is reversible and is never gated. The gate sits on "
                    "transmission, never on drafting. An assistant that asks "
                    "permission to think is useless; one that sends without it is "
                    "dangerous."),
         predicate="compose -> execute; transmit -> ACT-TRANSMIT-015",
         origin_ref=SESSION + " / the reversibility function applied to speech acts"),

    dict(rule_id="ACT-STANDING-017", name="Standing authority is bounded, never general",
         klass=CONTROL, reversibility=RESIDUAL, consequence=HIGH,
         statement=("A standing authority to act names a recipient class, a message "
                    "class and an expiry. General authority to communicate in the "
                    "principal's name is not granted. An expired authority resolves "
                    "to none."),
         predicate="authority.recipients and authority.message_class and authority.expires_at",
         origin_ref=SESSION + " / same failure mode as an expiring capability class"),

    dict(rule_id="ACT-RECORD-018", name="What was said in your name is readable by you",
         klass=VALIDATION, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("Every communication issued in the principal's name is recorded "
                    "in a form the principal can read, in full, without asking. "
                    "They need to know what they are supposed to have said."),
         predicate="transmitted -> record(full_content, recipient, at, authority_ref)",
         origin_ref=SESSION + " / acting on behalf, recipient cannot tell the difference"),

    dict(rule_id="ASSIST-CONTRADICT-019", name="Surface the contradiction unasked",
         klass=VALIDATION, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("Where a proposed action contradicts a recorded prior decision, "
                    "commitment or constraint, the assistant surfaces it without "
                    "being asked. Suppressing it to stay agreeable is a defect, not "
                    "tact. This is also what qualifies the assistant as an "
                    "independent validation source under CTL-VALID-SRC-003."),
         predicate="proposed conflicts_with recorded -> surface before acting",
         origin_ref=SESSION + " / senior assistant role, beyond office management",
         notes=("An assistant that cannot disagree cannot validate, and a loop "
                "with no independent validator confirms its own bias.")),

    dict(rule_id="ASSIST-TRIAGE-020", name="Escalation has a cost and is itself an action",
         klass=CONTROL, reversibility=REVERSIBLE, consequence=LOW,
         statement=("The assistant's default is to absorb, not to forward. Bringing "
                    "something to the principal spends their attention, so it is "
                    "weighed like any other action rather than treated as the safe "
                    "option. Forwarding everything is not caution, it is abdication."),
         predicate="escalate only when decision is reserved, irreversible, or genuinely novel",
         origin_ref=SESSION + " / gate minimization applied to the principal's attention"),

    dict(rule_id="ASSIST-CONTINUITY-021", name="State belongs to the assistant, not the surface",
         klass=TRANSFORMATION, reversibility=REVERSIBLE, consequence=MODERATE,
         statement=("Context, evidence, decisions and standing authorities are held "
                    "by the assistant and are identical on every surface. A phone, a "
                    "desktop and a tablet are views. None of them is where anything "
                    "lives, and none may hold state the others cannot see."),
         predicate="state.location == assistant and surface is presentation only",
         origin_ref=SESSION + " / DCS: not limited to physical devices"),

]



# Tests that already exist and pass in this codebase, bound to the rules they
# prove. A rule with no entry here is doctrine that has not yet been shown to
# work, which is exactly what the register is for saying out loud.
KNOWN_TESTS: Dict[str, List[str]] = {
    "CTL-GATE-MIN-001": ["rulebase: a reversible low consequence rule executes"],
    "CTL-REV-002": ["rulebase: an irreversible rule escalates",
                    "rulebase: a reversible high consequence rule still escalates",
                    "rulebase: a residual rule executes as a candidate"],
    "CTL-VALID-SRC-003": ["rulebase: six unvalidated firings do not promote",
                          "rulebase: the rule's own evaluator does not promote it",
                          "rulebase: five reruns of one case do not promote"],
    "CTL-DEST-004": ["desk: the stored object resolves and matches its hash",
                     "desk: an unknown address refuses rather than inventing a path"],
    "EXT-WORDBOUND-009": ["desk: as-is found the boiler"],
    "EXT-NEGATION-010": ["desk: the pdf line lands in the gap band",
                         "desk: a table row that reads badly is caught"],
    "TRF-SUPERSEDE-011": ["desk: rereading supersedes rather than overwrites"],
    "CTL-PROMOTE-013": ["rulebase: independent validation across distinct cases promotes"],
    "CTL-DEMOTE-014": ["rulebase: a climbing exception rate demotes an active rule",
                       "rulebase: a superseded rule deprecates"],
}


def bind_known(rb: "RuleBase") -> int:
    """Bind the tests that already pass. Doctrine with no test stays a
    candidate, visibly."""
    bound = 0
    for rule_id, tests in KNOWN_TESTS.items():
        if not rb.rule(rule_id):
            continue
        have = {r["name"] for r in rb.db.execute(
            "SELECT name FROM rule_test WHERE rule_id = ?", (rule_id,))}
        for name in tests:
            if name in have:
                continue
            rb.bind_test(rule_id, name, passing=True)
            bound += 1
    return bound


def seed(rb: "RuleBase") -> int:
    added = 0
    for spec in SEED:
        if rb.rule(spec["rule_id"]):
            continue
        rb.propose(origin_kind="stated", proposed_by="DCS/Claude session", **spec)
        added += 1
    return added


# ---------------------------------------------------------------------------

def selftest(path: str) -> int:
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="rulebase-")
    rb = RuleBase(os.path.join(tmp, "rules.sqlite3"))
    checks: List[Tuple[str, bool, str]] = []

    def check(label: str, cond: bool, detail: str = "") -> None:
        checks.append((label, bool(cond), detail))

    n = seed(rb)
    check("session doctrine registers", n == len(SEED), "%d of %d" % (n, len(SEED)))
    check("nothing is born active",
          all(r["lifecycle"] == CANDIDATE for r in
              [rb.rule(s["rule_id"]) for s in SEED]))

    # Control level is derived, not typed in.
    check("an irreversible rule escalates",
          control_for(IRREVERSIBLE, LOW) == ESCALATE)
    check("a reversible high consequence rule still escalates",
          control_for(REVERSIBLE, HIGH) == ESCALATE,
          "reversibility alone is not enough")
    check("a reversible low consequence rule executes",
          control_for(REVERSIBLE, LOW) == EXECUTE)
    check("a residual rule executes as a candidate",
          control_for(RESIDUAL, LOW) == EXECUTE_AS_CANDIDATE)

    rid = "EXT-NEGATION-010"
    life, why = rb.reassess(rid)
    check("a candidate with no test cannot promote", life == CANDIDATE, why)

    rb.bind_test(rid, "test_negation_detects_absence", passing=False)
    life, why = rb.reassess(rid)
    check("a failing test still cannot promote", life == CANDIDATE, why)

    rb.set_test_result(rid, "test_negation_detects_absence", True)
    life, why = rb.reassess(rid)
    check("tests passing plus origin promotes to provisional", life == PROVISIONAL, why)

    # Silence is not validation.
    for i in range(6):
        rb.record_firing(rid, sig("doc", i), validated_by=SILENCE)
    life, why = rb.reassess(rid)
    check("six unvalidated firings do not promote", life == PROVISIONAL, why)

    # Neither is the rule's own evaluator.
    for i in range(6):
        rb.record_firing(rid, sig("doc", 100 + i), validated_by=SELF)
    life, why = rb.reassess(rid)
    check("the rule's own evaluator does not promote it", life == PROVISIONAL, why)

    # Five validations of the SAME case is one confirmation.
    for i in range(5):
        rb.record_firing(rid, sig("same", "case"), validated_by=REALITY)
    life, why = rb.reassess(rid)
    check("five reruns of one case do not promote", life == PROVISIONAL, why)

    # Distinct cases, independently validated, do.
    for i in range(5):
        rb.record_firing(rid, sig("real", i), validated_by=REALITY)
    life, why = rb.reassess(rid)
    check("independent validation across distinct cases promotes", life == ACTIVE, why)

    # Then it starts failing.
    for i in range(12):
        rb.record_firing(rid, sig("later", i), exception=True, outcome="wrong band",
                         validated_by=PERSON)
    life, why = rb.reassess(rid)
    check("a climbing exception rate demotes an active rule", life == DEPRECATED, why)

    # Supersession.
    rb.propose(rule_id="EXT-NEGATION-010b", name="Negation, narrowed",
               klass=EXTRACTION, statement="Narrowed negation matcher.",
               predicate="auxiliary + not", origin_ref=SESSION,
               supersedes=rid)
    life, why = rb.reassess(rid)
    check("a superseded rule deprecates", life == DEPRECATED, why)

    # Health checks.
    broad = "EXT-BROAD-TEST"
    rb.propose(rule_id=broad, name="Deliberately broad matcher", klass=EXTRACTION,
               statement="Matches nearly everything.", predicate=r"not \w+",
               origin_ref=SESSION)
    for i in range(30):
        rb.record_firing(broad, sig("b", i), matched=(i % 10 != 0))
    findings = {f["check"] for f in rb.health()}
    check("fires too broadly is detected", "fires_too_broadly" in findings,
          str(sorted(findings)))

    dup = "EXT-DUP-TEST"
    rb.propose(rule_id=dup, name="Same body as the broad one", klass=EXTRACTION,
               statement="Matches nearly everything.", predicate=r"not \w+",
               origin_ref=SESSION)
    check("duplicate bodies are detected",
          any(f["check"] == "duplicate" for f in rb.health()))

    loser = "TRF-LOSER-TEST"
    rb.propose(rule_id=loser, name="Never selected", klass=TRANSFORMATION,
               statement="A shape that keeps losing.", origin_ref=SESSION)
    for i in range(10):
        rb.record_firing(loser, sig("l", i), selected=False)
    check("a rule that never wins is detected",
          any(f["check"] == "repeatedly_loses" for f in rb.health()))

    for i in range(4):
        rb.record_candidate(sig("case", i), "separated profiles with shared contract",
                            {"shape": "B+C"}, selected=True, validated_by=REALITY)
    check("a convergent generated shape becomes a rule candidate",
          any(f["check"] == "convergent" for f in rb.health()))

    # The register knows its own shape.
    s = rb.summary()
    check("the register reports its control distribution",
          sum(s["by_control"].values()) > 0, json.dumps(s["by_control"]))

    width = max(len(c[0]) for c in checks) + 2
    print()
    for label, ok, detail in checks:
        print("  %-4s %-*s %s" % ("PASS" if ok else "FAIL", width, label,
                                  "" if ok else detail))
    passed = sum(1 for c in checks if c[1])
    print("\n" + "=" * 70)
    print("  Rule register selftest: %d of %d passed" % (passed, len(checks)))
    print("=" * 70 + "\n")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if passed == len(checks) else 1


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="rulebase",
                                 description="Rule lifecycle register.")
    ap.add_argument("--db", default=os.path.join(
        os.path.expanduser("~"), "Desk", "rules.sqlite3"))
    ap.add_argument("--seed", action="store_true", help="register session doctrine")
    ap.add_argument("--bind", action="store_true",
                    help="bind the tests that already pass in this codebase")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--health", action="store_true")
    ap.add_argument("--reassess", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        return selftest(a.db)

    rb = RuleBase(a.db)
    if a.seed:
        print("  registered %d new rules as candidates" % seed(rb))
    if a.bind:
        print("  bound %d passing tests to their rules" % bind_known(rb))
    if a.reassess:
        for rid, life, why in rb.reassess_all():
            print("  %-24s %-12s %s" % (rid, life, why))
    if a.health:
        f = rb.health()
        print("\n  Rule base health: %d findings" % len(f))
        for x in f:
            print("    %-20s %-22s %s" % (x["check"], x["rule"], x["detail"]))
    if a.report or not (a.seed or a.health or a.reassess or a.bind):
        print("\n  Register: %s" % a.db)
        print("  %s\n" % json.dumps(rb.summary()))
        print(rb.table())
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
