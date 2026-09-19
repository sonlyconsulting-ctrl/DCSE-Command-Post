"""CTJ Conversation Flow runtime primitives for ESCD.

Candidate v7.2 implementation. Conversation context is evidence, not the
system of record. Enterprise retrieval is performed by the caller/adapters.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

CONFIG_PATH = Path(__file__).with_name("ctj_conversation_flow.v7.2.json")


@dataclass
class CFState:
    literal_request: str
    canonical_objects: list[str] = field(default_factory=list)
    request_classes: list[str] = field(default_factory=list)
    action_modes: list[str] = field(default_factory=list)
    resolution_state: str = "UNKNOWN"
    variables: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    ddna_candidates: list[dict[str, Any]] = field(default_factory=list)
    hard_stop: str | None = None


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _norm(text: str) -> str:
    return " ".join(text.lower().replace("’", "'").split())


def resolve_ctj_objects(text: str, config: dict[str, Any] | None = None) -> list[str]:
    cfg = config or load_config()
    normalized = _norm(text)
    hits: list[tuple[int, str]] = []
    for canonical_id, aliases in cfg["entry_aliases"].items():
        for alias in aliases:
            pos = normalized.find(_norm(alias))
            if pos >= 0:
                hits.append((pos, canonical_id))
                break
    # Preserve conversational order and de-duplicate.
    result: list[str] = []
    for _, canonical_id in sorted(hits):
        if canonical_id not in result:
            result.append(canonical_id)
    return result


def classify_request(text: str) -> list[str]:
    t = _norm(text)
    mapping = {
        "INVENTORY": ("inventory", "what products", "all ctj"),
        "REVIEW": ("review", "show me", "send me", "link", "find"),
        "CREATE": ("create", "make", "build", "new"),
        "TRANSFORM": ("transform", "convert", "turn into", "logo"),
        "CORRECT": ("wrong", "correct", "not what", "instead"),
        "PACKAGE": ("package", "zip", "bundle"),
        "BRAND_MEDIA": ("image", "logo", "video", "brand", "visual"),
        "COMMERCIALIZE": ("stripe", "price", "sell", "checkout", "commerce"),
        "DEPLOY": ("deploy", "vercel", "netlify", "publish"),
        "TEST": ("test", "validate", "playwright", "e2e"),
        "RELEASE": ("release", "promote", "production"),
        "SUPPORT": ("customer", "support", "receipt", "fulfillment"),
        "GOVERNANCE": ("doctrine", "rule", "governance", "ddna", "cf")
    }
    classes = [name for name, words in mapping.items() if any(word in t for word in words)]
    return classes or ["REVIEW"]


def action_modes_for(classes: Iterable[str]) -> list[str]:
    classes = set(classes)
    modes = ["READ", "ANALYZE"]
    if classes & {"CREATE", "BRAND_MEDIA"}:
        modes.append("GENERATE")
    if "TRANSFORM" in classes:
        modes.append("TRANSFORM")
    if classes & {"COMMERCIALIZE", "DEPLOY", "PACKAGE", "SUPPORT"}:
        modes.append("MUTATE")
    if classes & {"TEST", "RELEASE"}:
        modes.append("VALIDATE")
    if "RELEASE" in classes:
        modes.append("PROMOTE")
    return modes


def next_resolution_state(current: str, *, searched_all: bool = False,
                          affirmative_absence: bool = False) -> str:
    if affirmative_absence:
        return "VERIFIED_ABSENT"
    if current == "UNKNOWN" and searched_all:
        return "SEARCHED_NOT_FOUND"
    return current


def should_escalate_to_user(state: CFState, *, retrievable_sources_remaining: bool) -> bool:
    if state.hard_stop:
        return True
    if state.resolution_state == "UNKNOWN" and retrievable_sources_remaining:
        return False
    return state.resolution_state in {"SEARCHED_NOT_FOUND", "VERIFIED_ABSENT"}


def extract_variables(text: str, *, session: dict[str, Any] | None = None,
                      task: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "turn": {"literal_request": text},
        "session": session or {},
        "task": task or {},
        "product": {},
        "entity": {"family": "CTJ", "entity": "Sonly Consulting"},
        "preference": {},
        "governance": {"floor": "DCSE-v7.2"},
        "derived": {}
    }


def correction_ddna_candidate(prior_behavior: str, correction: str) -> dict[str, Any]:
    return {
        "family": "DCS_INTERACTION_CORRECTION_DNA",
        "status": "CANDIDATE",
        "authority": "DCS_EXPLICIT_CORRECTION",
        "confidence": 1.0,
        "evidence": {"prior_behavior": prior_behavior, "correction": correction},
        "promotion": "REQUIRES_DEDUP_CONTRADICTION_VALIDATION"
    }


def start_ctj_cf(request: str, *, session: dict[str, Any] | None = None,
                 task: dict[str, Any] | None = None) -> CFState:
    cfg = load_config()
    state = CFState(literal_request=request)
    state.canonical_objects = resolve_ctj_objects(request, cfg)
    state.request_classes = classify_request(request)
    state.action_modes = action_modes_for(state.request_classes)
    state.variables = extract_variables(request, session=session, task=task)
    state.variables["product"]["canonical_objects"] = state.canonical_objects
    return state
