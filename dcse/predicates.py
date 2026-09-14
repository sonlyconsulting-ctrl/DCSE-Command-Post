"""Shared predicate library.

A condition is written here once and referenced by every rule that needs it.
Two rules expressing the same condition in two slightly different ways is how
a rule base starts contradicting itself, and it is what the register's
duplicate and overlap checks are there to catch after the fact. Writing the
condition once avoids the problem instead of detecting it.

Every helper returns one of PASS, FAIL, UNKNOWN. The distinction between the
last two is the important one and it is not a judgment call:

    UNKNOWN   the fact is simply not present and nothing required it
    FAIL      a triggered rule required this fact and it was not supplied

That difference came out of the other surface's work and it is correct. A Task
marked COMPLETE with no completion evidence is not a knowledge gap. It is a
claim that failed.
"""
from __future__ import annotations

import re
from typing import Any, Optional, Sequence, Tuple

from model import FAIL, PASS, UNKNOWN, Operation

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")


# -- presence --------------------------------------------------------------

def present(op: Operation, *keys: str) -> str:
    """All keys present and non-empty, else UNKNOWN with the missing ones."""
    return PASS if all(op.has(k) for k in keys) else UNKNOWN


def required(op: Operation, *keys: str) -> str:
    """All keys REQUIRED by a rule that has already triggered. Absence is FAIL,
    not UNKNOWN, because the rule asked and the answer was not given."""
    return PASS if all(op.has(k) for k in keys) else FAIL


def missing_of(op: Operation, *keys: str) -> Tuple[str, ...]:
    return tuple(k for k in keys if not op.has(k))


# -- conditional shapes ----------------------------------------------------

def when(condition: bool, then: str) -> str:
    """A rule whose body only applies under a condition. When the condition is
    false the rule is satisfied vacuously rather than unknown."""
    return then if condition else PASS


def equals(op: Operation, key: str, value: Any) -> bool:
    return op.get(key) == value


def one_of(op: Operation, key: str, allowed: Sequence[Any]) -> str:
    if not op.has(key):
        return UNKNOWN
    return PASS if op.get(key) in allowed else FAIL


def truthy(op: Operation, key: str) -> str:
    """A boolean fact that must be true. Absent is UNKNOWN, false is FAIL."""
    if key not in op.facts or op.get(key) is None:
        return UNKNOWN
    return PASS if bool(op.get(key)) else FAIL


def falsy(op: Operation, key: str) -> str:
    if key not in op.facts or op.get(key) is None:
        return UNKNOWN
    return FAIL if bool(op.get(key)) else PASS


# -- identity and integrity ------------------------------------------------

def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA256_RE.match(value.lower()))


def is_sha1(value: Any) -> bool:
    return isinstance(value, str) and bool(SHA1_RE.match(value.lower()))


def hash_ok(op: Operation, key: str = "content_hash") -> str:
    if not op.has(key):
        return UNKNOWN
    return PASS if is_sha256(op.get(key)) else FAIL


def resolves(op: Operation, ref_key: str, proof_key: str) -> str:
    """The substitution that runs through the whole standard: a reference is
    not enough, it has to resolve. The ref names a destination; the proof says
    something was actually found there."""
    if not op.has(ref_key):
        return UNKNOWN
    return PASS if bool(op.get(proof_key)) else FAIL


# -- text and secrets ------------------------------------------------------

CREDENTIAL_SHAPES = (
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\."),
    re.compile(r"\bsb_secret_[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}"),
    re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    re.compile(r"\bsk-(?:or-v1-)?[A-Za-z0-9]{20,}"),
    re.compile(r"postgres(?:ql)?://[^\s:@/]+:[^\s@/]{6,}@"),
    re.compile(r"SERVICE_ROLE_KEY\s*[:=]\s*['\"]?[A-Za-z0-9._-]{20,}"),
)


def carries_credential(text: Any) -> bool:
    if not isinstance(text, str):
        return False
    return any(rx.search(text) for rx in CREDENTIAL_SHAPES)


def no_credentials(op: Operation, *keys: str) -> str:
    """Absence of a payload is UNKNOWN. A payload with a credential shape in it
    is FAIL, and there is no third option."""
    seen = False
    for k in keys:
        if not op.has(k):
            continue
        seen = True
        value = op.get(k)
        chunks = value if isinstance(value, (list, tuple)) else [value]
        for c in chunks:
            if carries_credential(c):
                return FAIL
    return PASS if seen else UNKNOWN


# -- lanes -----------------------------------------------------------------

PROTECTED_LANES = ("PS",)


def lane_clear(op: Operation, content_keys: Sequence[str] = ()) -> str:
    """Protected lane material must not leave its lane. This is the one
    condition in the library that never softens: a cross lane transaction
    touching a protected lane fails, it does not resolve to unknown."""
    declared = (op.lane or "").upper()
    touched = op.get("lanes_touched") or [declared]
    touched = [str(t).upper() for t in touched]
    if declared not in PROTECTED_LANES and any(t in PROTECTED_LANES for t in touched):
        return FAIL
    if op.has("protected_content") and bool(op.get("protected_content")):
        return PASS if declared in PROTECTED_LANES else FAIL
    return PASS


# -- authority -------------------------------------------------------------

def within_scope(op: Operation, value_key: str, scope_key: str) -> str:
    """A value that must fall inside a declared scope. An absent scope is not
    an open scope, it is no scope, and that fails."""
    if not op.has(scope_key):
        return FAIL
    if not op.has(value_key):
        return UNKNOWN
    scope = op.get(scope_key)
    value = op.get(value_key)
    values = value if isinstance(value, (list, tuple)) else [value]
    return PASS if all(v in scope for v in values) else FAIL


def unexpired(op: Operation, key: str = "authority_expires_at") -> str:
    """An expired authority resolves to none. Self cleaning and fail closed."""
    if not op.has(key):
        return FAIL
    try:
        return PASS if float(op.get(key)) > op.at else FAIL
    except (TypeError, ValueError):
        return FAIL


def different_identities(op: Operation, a_key: str, b_key: str) -> str:
    """Separation of duties. Whoever did the thing may not approve the thing."""
    if not (op.has(a_key) and op.has(b_key)):
        return UNKNOWN
    return PASS if str(op.get(a_key)) != str(op.get(b_key)) else FAIL


def all_pass(*verdicts: str) -> str:
    """Conjunction with the right precedence: any FAIL fails, else any UNKNOWN
    is unknown, else pass."""
    if FAIL in verdicts:
        return FAIL
    if UNKNOWN in verdicts:
        return UNKNOWN
    return PASS
