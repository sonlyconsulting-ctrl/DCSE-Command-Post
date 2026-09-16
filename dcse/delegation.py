"""Task packets: work handed to another model through the repository.

The instruction "check GitHub and execute the latest task" needs three things
that do not exist by default: a known location, a known format, and a way for
the executing model to know whether it succeeded without asking anyone.

The format is not new. An Operation already carries entity, capabilities,
action and facts, and the orchestrator already computes whether that operation
executes, writes to a candidate layer, or needs a person. A task packet is an
Operation plus the acceptance criteria that say when it is done, and the
disposition falls out of the rules rather than being asserted by whoever wrote
the task.

That last part is what answers "approve as designed, and not everything". The
packet does not tell you what needs your approval. The rules compute it, and
the packet records the answer so the executing model can see it before starting.

Two refusals, both deliberate and both the same discipline as everywhere else:

    A packet with no acceptance criteria is invalid. A task that cannot be
    shown to have succeeded cannot be delegated, only hoped about.

    A packet whose acceptance is a description rather than a command is
    invalid. "Verify the build works" is not checkable by a model working
    alone at two in the morning. "python -m dcse bench --against
    baseline.json" is.
"""
from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Sequence

from model import (ESCALATE, EXECUTE, EXECUTE_AS_CANDIDATE, HIGH, LOW,
                   MODERATE, Operation, REFUSE, RESIDUAL, REVERSIBLE,
                   IRREVERSIBLE)

def _resolve_tasks_dir() -> str:
    env_dir = os.environ.get("DCSE_TASKS_DIR")
    if env_dir and os.path.isdir(env_dir):
        return env_dir
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    queue_dir = os.path.join(repo_root, "tasks", "queue")
    if os.path.isdir(queue_dir) and any(f.endswith(".json") for f in os.listdir(queue_dir)):
        return queue_dir
    root_tasks = os.path.join(repo_root, "tasks")
    if os.path.isdir(root_tasks) and any(f.endswith(".json") for f in os.listdir(root_tasks)):
        return root_tasks
    module_tasks = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")
    if os.path.isdir(module_tasks):
        return module_tasks
    return root_tasks


TASKS_DIR = _resolve_tasks_dir()


RECON_STATES = ("READY", "HOLD_DCS", "STALE_RECONCILE", "SUPERSEDED", "BLOCKED")
BLOCKING_RECON = ("HOLD_DCS", "STALE_RECONCILE", "SUPERSEDED", "BLOCKED")


class InvalidPacket(ValueError):
    pass


@dataclass
class Acceptance:
    """One checkable claim. `command` runs, `expect` is what proves it."""
    command: str
    expect: str
    why: str = ""

    def validate(self, task_id: str) -> None:
        if not self.command.strip():
            raise InvalidPacket("%s: an acceptance criterion with no command "
                                "cannot be checked by anyone working alone" % task_id)
        if not self.expect.strip():
            raise InvalidPacket("%s: acceptance %r says what to run but not what "
                                "proves it worked" % (task_id, self.command))


@dataclass
class TaskPacket:
    id: str
    title: str
    objective: str
    issued_by: str
    directive: str
    entity: str
    action: str
    capabilities: Sequence[str]
    scope: Sequence[str]                 # paths the executor may touch
    steps: Sequence[str]
    acceptance: Sequence[Acceptance]
    reversibility: str = REVERSIBLE
    consequence: str = LOW
    forbidden: Sequence[str] = field(default_factory=tuple)
    report: Sequence[str] = field(default_factory=tuple)
    depends_on: Sequence[str] = field(default_factory=tuple)
    status: str = "open"
    facts: Dict[str, Any] = field(default_factory=dict)

    # Reconciliation state, separate from status and from the computed
    # disposition. Adopted from the second surface, and it closes a real gap:
    # my model computed approval from risk alone and had no way to say that DCS
    # has paused an area, or that a packet has gone stale because the world
    # moved after it was written. Risk is not the only reason not to run
    # something.
    reconciliation: str = "READY"   # READY | HOLD_DCS | STALE_RECONCILE
                                    # | SUPERSEDED | BLOCKED
    reconciliation_note: str = ""
    hold_ref: str = ""              # the directive or decision that holds it

    # -- validity -------------------------------------------------------

    def validate(self) -> None:
        if not self.acceptance:
            raise InvalidPacket(
                "%s has no acceptance criteria. A task that cannot be shown to "
                "have succeeded cannot be delegated, only hoped about." % self.id)
        for a in self.acceptance:
            a.validate(self.id)
        if not self.scope:
            raise InvalidPacket(
                "%s declares no scope. An executor with no boundary will find "
                "one, and it will be wider than you meant." % self.id)
        if not self.steps:
            raise InvalidPacket("%s has no steps" % self.id)
        if self.reconciliation not in RECON_STATES:
            raise InvalidPacket("%s has an invented reconciliation state %r"
                                % (self.id, self.reconciliation))
        if self.reconciliation in BLOCKING_RECON and not self.reconciliation_note:
            raise InvalidPacket(
                "%s is %s with no note. A hold nobody can read is "
                "indistinguishable from a hold nobody meant."
                % (self.id, self.reconciliation))
        if self.status == "done":
            raise InvalidPacket(
                "%s is marked done in the packet. Done is established by "
                "execution evidence, not by the field being set (TASK-06)."
                % self.id)

    # -- what the rules say about it ------------------------------------

    STATUS_TO_STATE = {"open": "open", "blocked": "blocked",
                       "done": "complete", "cancelled": "cancelled",
                       "superseded": "superseded"}

    def operation(self) -> Operation:
        """A packet is a Task, so it answers the Task rules with its own fields.

        This is not a convenience. A packet that cannot satisfy TASK-01 through
        TASK-05 is a badly formed task, and it should escalate rather than be
        handed to anyone. Note what falls out: a packet marked done with no
        completion evidence fails TASK-06, which means the delegation layer is
        governed by the same rules as the work it delegates.
        """
        facts = {
            "task_id": self.id,
            "objective": self.objective,
            "owner": self.issued_by,
            "acceptance_criteria": [a.command for a in self.acceptance],
            "declared_scope": list(self.scope),
            "reversibility": self.reversibility,
            "consequence": self.consequence,
        }
        # The packet's own status belongs to the packet, which is a Task. The
        # operation's subject may be something else entirely, with its own state
        # vocabulary, and pushing a task status onto an idea produces an invented
        # state that fails IDEA-04. Found by T-004 reporting as needing approval
        # for a reason that had nothing to do with its risk.
        if self.entity == "task":
            facts["state"] = self.STATUS_TO_STATE.get(self.status, self.status)
        facts.update(self.facts)
        return Operation(entity=self.entity, action=self.action,
                         capabilities=tuple(self.capabilities),
                         actor="delegated-executor", directive=self.directive,
                         facts=facts)

    def disposition(self, orchestrator: Any) -> Dict[str, str]:
        """Computed, not asserted. The packet author does not get to decide
        whether their own task needs approval.

        Reconciliation outranks risk. A reversible edit on a branch is an
        EXECUTE by the rules, and it still must not run if DCS has paused that
        area or the packet has gone stale. Computed risk says whether the work
        is safe. It cannot say whether the work is still wanted.
        """
        if self.reconciliation in BLOCKING_RECON:
            return {"disposition": ESCALATE,
                    "reason": "%s: %s" % (self.reconciliation,
                                          self.reconciliation_note),
                    "needs_approval": "True",
                    "held_by": self.hold_ref or "unrecorded"}
        # Plan stage only. A packet is judged on what can be known before the
        # work exists, or every delegable task escalates on a question nobody
        # could have answered yet.
        outcome = orchestrator.run(self.operation(), execute=False, stage="plan")
        return {"disposition": outcome.disposition, "reason": outcome.reason,
                "needs_approval": str(outcome.disposition in (ESCALATE, REFUSE))}

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["acceptance"] = [asdict(a) for a in self.acceptance]
        return d


def from_dict(raw: Dict[str, Any]) -> TaskPacket:
    raw = dict(raw)
    raw["acceptance"] = [Acceptance(**a) for a in raw.get("acceptance", [])]
    return TaskPacket(**raw)


def load_all(directory: str = TASKS_DIR) -> List[TaskPacket]:
    packets: List[TaskPacket] = []
    if not os.path.isdir(directory):
        return packets
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(directory, name), "r", encoding="utf-8") as fh:
            packets.append(from_dict(json.load(fh)))
    return packets


def save(packet: TaskPacket, directory: str = TASKS_DIR) -> str:
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, packet.id + ".json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(packet.to_dict(), fh, indent=2, sort_keys=True)
    return path


def next_open(packets: Sequence[TaskPacket]) -> List[TaskPacket]:
    """Open tasks whose dependencies are done. This is what "the latest task"
    actually means: not the newest file, the next runnable one."""
    done = {p.id for p in packets if p.status == "done"}
    return [p for p in packets
            if p.status == "open" and p.reconciliation == "READY"
            and all(d in done for d in p.depends_on)]


def report(packets: Sequence[TaskPacket], orchestrator: Any = None) -> str:
    lines = ["", "  %-8s %-17s %-8s %s"
             % ("TASK", "RECONCILIATION", "APPROVAL", "TITLE")]
    runnable = {p.id for p in next_open(packets)}
    for p in packets:
        approval = "?"
        if orchestrator is not None:
            approval = "yours" if p.disposition(orchestrator)["needs_approval"] == "True" \
                else "auto"
        mark = "->" if (p.id in runnable and p.reconciliation == "READY") else "  "
        lines.append("%s %-8s %-17s %-8s %s"
                     % (mark, p.id, p.reconciliation, approval, p.title))
    lines.append("")
    lines.append("  -> marks the next runnable task. Blocked tasks wait on depends_on.")
    return "\n".join(lines)
