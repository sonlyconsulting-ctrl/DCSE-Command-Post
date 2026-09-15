"""Voice capability rules.

Voice is any act that reaches another person in the principal's name. This is
where irreversibility stops being an edge case and becomes the dominant class,
because the recipient cannot tell the difference between the assistant and the
principal and therefore cannot apply their own judgment about who they are
dealing with.

The line these rules draw is between composition and transmission. Drafting is
reversible and is never gated. Sending is not and always is. An assistant that
asks permission to think is useless; one that sends without asking is dangerous.
"""
from __future__ import annotations

from model import EVIDENCE, HIGH, IRREVERSIBLE, MODERATE, Operation
from predicates import lane_clear, required, unexpired, when, within_scope
from registry import rule

ORIGIN = "DCSE-GOV-20260913 / acting on behalf of a principal"
SEND = ("send", "transmit", "publish", "reply", "post", "call")


@rule("VOICE-01", "Transmission requires a live authority", ["voice"],
      actions=list(SEND), reversibility=IRREVERSIBLE, consequence=HIGH,
      origin=ORIGIN,
      statement=("Nothing goes out in the principal's name without a standing "
                 "authority that has not expired. An expired authority resolves "
                 "to none."))
def _(op: Operation) -> str:
    return when(op.action in SEND, unexpired(op, "authority_expires_at"))


@rule("VOICE-02", "The recipient is inside the authorised set", ["voice"],
      actions=list(SEND), reversibility=IRREVERSIBLE, consequence=HIGH,
      origin=ORIGIN,
      statement=("Authority names who may be written to. An absent scope is not "
                 "an open scope, it is no scope."))
def _(op: Operation) -> str:
    return when(op.action in SEND, within_scope(op, "recipient", "authorised_recipients"))


@rule("VOICE-03", "The message class is inside the authorised set", ["voice"],
      actions=list(SEND), reversibility=IRREVERSIBLE, consequence=HIGH,
      origin=ORIGIN,
      statement=("Authority to confirm an appointment is not authority to agree "
                 "to terms. Class is bounded separately from recipient."))
def _(op: Operation) -> str:
    return when(op.action in SEND, within_scope(op, "message_class", "authorised_classes"))


@rule("VOICE-04", "Protected lane content is never transmitted outside its lane",
      ["voice"], reversibility=IRREVERSIBLE, consequence=HIGH, origin=ORIGIN,
      statement="Disclosure is the one class with no recovery of any kind.")
def _(op: Operation) -> str:
    return lane_clear(op, ("body", "attachments"))


@rule("VOICE-05", "What was said in your name is readable by you", ["voice"],
      actions=list(SEND), consequence=MODERATE, stage=EVIDENCE, origin=ORIGIN,
      statement=("Every transmission is recorded in full with recipient, time "
                 "and the authority it ran under. You need to be able to read "
                 "what you are supposed to have said."))
def _(op: Operation) -> str:
    return when(op.action in SEND,
                required(op, "transmission_record", "recipient", "authority_ref"))
