from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
from urllib import parse

from apps.escd.runtime.mvp_data import (
    MVPServiceError,
    _http_json,
    _postgrest_headers,
    _service_config,
    get_canonical_convergence_items,
    list_assets,
    list_ddna_sources,
    list_knowledge,
)

# Rule 5 Layer A: DCSE Kernel
DCSE_KERNEL = """You are ESCD (Executive Support & Command Dispatch), the minimal operable assistant and operational governance console for DCSE.
OPERATIVE GOVERNANCE:
1. DCS operator directives are the supreme authority.
2. Models (OpenAI, Gemini, OpenRouter) are execution engines, NOT separate personas. Maintain uniform ESCD identity and posture across every model switch.
3. Authority hierarchy: Explicit current DCS directive -> Current project/task state -> Verified ESCD records -> Historical/reference records -> Model inference.
4. Historical, candidate, REVIEW, and HOLD records must remain visibly classified and non-operational unless explicitly activated by DCS.
5. Evidence state taxonomy: VERIFIED, LIKELY, UNKNOWN, ASSUMPTION.
6. Confidentiality: Never expose API keys, internal secrets, or service credentials.
7. Active Entity & Lanes: DCSE, Command Post, SC, SS, Employment, Polar, Tribunal.
"""


@dataclass
class ConversationState:
    conversation_id: str
    title: str = "New Conversation"
    current_goal: str = ""
    current_topic: str = ""
    active_entity_lane: str = "DCSE"
    active_project_task: str = ""
    confirmed_decisions: list[str] = field(default_factory=list)
    unresolved_questions: list[str] = field(default_factory=list)
    commitments_next_actions: list[str] = field(default_factory=list)
    pinned_facts: list[str] = field(default_factory=list)
    superseded_facts: list[str] = field(default_factory=list)
    recent_summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ConversationState:
        fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**fields)


@dataclass
class TurnRecord:
    conversation_id: str
    seq: int
    user_message: str
    assistant_response: str
    provider: str
    model: str
    entity_lane: str = "DCSE"
    project_task: str = ""
    evidence_classification: str = "ASSUMPTION"
    retrieved_refs: list[dict] = field(default_factory=list)
    authority_refs: list[str] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TurnRecord:
        fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**fields)


def retrieve_governed_context(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Retrieve task-routed records from Tasks, Ideas, Assets, DDNA, and Knowledge (Rule 5 Layer C)."""
    if not query or not query.strip():
        return []
    terms = set(re.findall(r"\w+", query.lower()))
    if not terms:
        return []

    collected: list[dict[str, Any]] = []

    # Knowledge
    for k in list_knowledge(limit=100):
        text = f"{k.get('title','')} {k.get('content','')}".lower()
        if any(t in text for t in terms):
            collected.append({
                "type": "Knowledge",
                "id": k.get("id"),
                "title": k.get("title"),
                "summary": (k.get("content") or "")[:250],
                "authority": k.get("authority_classification", "HISTORICAL_RECOVERED"),
            })

    # Assets
    try:
        for a in list_assets(limit=100):
            text = f"{a.get('file_name','')} {a.get('topic','')} {a.get('asset_type','')}".lower()
            if any(t in text for t in terms):
                collected.append({
                    "type": "Asset",
                    "id": a.get("asset_id") or a.get("id"),
                    "title": a.get("file_name"),
                    "summary": a.get("topic") or a.get("asset_type"),
                    "status": a.get("lifecycle_status"),
                })
    except Exception:
        pass

    # DDNA
    try:
        for d in list_ddna_sources(limit=100):
            text = f"{d.get('source_title','')} {d.get('source_ref_id','')} {d.get('source_type','')}".lower()
            if any(t in text for t in terms):
                collected.append({
                    "type": "DDNA",
                    "id": d.get("source_ref_id") or d.get("id"),
                    "title": d.get("source_title"),
                    "lane": d.get("lane"),
                    "status": d.get("status"),
                })
    except Exception:
        pass

    return collected[:limit]


def assemble_context_packet(
    state: ConversationState,
    current_turn: str,
    turns: list[TurnRecord],
    retrieved: list[dict[str, Any]],
) -> list[dict[str, str]]:
    """Assemble 4-layer governed context packet server-side (Rule 5)."""
    messages: list[dict[str, str]] = []

    # Layer A: DCSE Kernel
    kernel_text = DCSE_KERNEL.strip()

    # Layer B: Structured Conversation State
    state_lines = [
        "CONVERSATION STATE (Governed Canonical):",
        f"- Active Entity/Lane: {state.active_entity_lane}",
    ]
    if state.current_goal:
        state_lines.append(f"- Current Goal: {state.current_goal}")
    if state.active_project_task:
        state_lines.append(f"- Active Project/Task: {state.active_project_task}")
    if state.confirmed_decisions:
        state_lines.append("- Confirmed Decisions:")
        for d in state.confirmed_decisions:
            state_lines.append(f"  * {d}")
    if state.superseded_facts:
        state_lines.append("- Superseded Facts (Do NOT resurrect): ")
        for sf in state.superseded_facts:
            state_lines.append(f"  * {sf}")
    if state.pinned_facts:
        state_lines.append("- Pinned Facts:")
        for pf in state.pinned_facts:
            state_lines.append(f"  * {pf}")
    if state.unresolved_questions:
        state_lines.append("- Unresolved Questions:")
        for uq in state.unresolved_questions:
            state_lines.append(f"  * {uq}")
    if state.recent_summary:
        state_lines.append(f"- Prior Conversation Summary: {state.recent_summary}")

    # Layer C: Retrieved Governed Context
    context_lines = []
    if retrieved:
        context_lines.append("RETRIEVED GOVERNED CONTEXT (Rule 6: Retrieval similarity does not establish authority):")
        for item in retrieved:
            context_lines.append(f"- [{item.get('type')}] {item.get('title')} (ID: {item.get('id')}) | {item.get('summary') or ''}")

    system_content = "\n\n".join(filter(None, [kernel_text, "\n".join(state_lines), "\n".join(context_lines)]))
    messages.append({"role": "system", "content": system_content})

    # Layer D: Raw Transcript outranks summary (Rule 4) + Current User Turn
    for t in turns[-12:]:
        messages.append({"role": "user", "content": t.user_message})
        messages.append({"role": "assistant", "content": t.assistant_response})

    messages.append({"role": "user", "content": current_turn})
    return messages


def extract_state_updates(user_msg: str, assistant_msg: str, state: ConversationState) -> None:
    """Extract confirmed decisions, goal changes, and sequence updates across turns."""
    um = user_msg.strip()

    # Detect primary execution sequence establishment:
    # e.g., 'We are finishing ESCD first. After ESCD comes CTJ, then TSL.'
    seq_match = re.search(r"(?:finishing|finish|start with)\s+([A-Z0-9_-]+)[^.]*\.\s*After\s+\1\s+comes\s+([A-Z0-9_-]+),?\s+then\s+([A-Z0-9_-]+)", um, re.IGNORECASE)
    if seq_match:
        step1 = seq_match.group(1).upper()
        step2 = seq_match.group(2).upper()
        step3 = seq_match.group(3).upper()
        new_dec = f"Execution Sequence: {step1} -> {step2} -> {step3}"
        state.confirmed_decisions = [d for d in state.confirmed_decisions if not d.startswith("Execution Sequence:")]
        state.confirmed_decisions.append(new_dec)
        state.current_goal = f"Complete {step1}, followed by {step2}, then {step3}"
        state.pinned_facts.append(f"Sequence established: {step1} -> {step2} -> {step3}")

    # Detect re-ordering or prioritization directives:
    # e.g., 'Move TSL ahead of CTJ'
    move_match = re.search(r"Move\s+([A-Z0-9_-]+)\s+ahead\s+of\s+([A-Z0-9_-]+)", um, re.IGNORECASE)
    if move_match:
        target = move_match.group(1).upper()
        after = move_match.group(2).upper()
        found = False
        for idx, dec in enumerate(list(state.confirmed_decisions)):
            if dec.startswith("Execution Sequence:"):
                parts = [p.strip() for p in dec.replace("Execution Sequence:", "").split("->")]
                if target in parts and after in parts:
                    state.superseded_facts.append(dec)
                    parts.remove(target)
                    insert_idx = parts.index(after)
                    parts.insert(insert_idx, target)
                    new_dec = f"Execution Sequence: {' -> '.join(parts)}"
                    state.confirmed_decisions[idx] = new_dec
                    state.pinned_facts.append(f"Re-ordering: Moved {target} ahead of {after}")
                    state.current_goal = f"Complete {' -> '.join(parts)}"
                    found = True
        if not found:
            state.confirmed_decisions.append(f"Prioritize {target} over {after}")

    # Detect general decision statements
    dec_match = re.search(r"(?:we decided|confirm|decide that|decision:)\s+([^.]*)", um, re.IGNORECASE)
    if dec_match:
        d_text = dec_match.group(1).strip()
        if d_text and d_text not in state.confirmed_decisions:
            state.confirmed_decisions.append(d_text)


def validate_response(response_text: str, state: ConversationState) -> tuple[bool, str]:
    """Validate response against DCSE identity, entity/lane, and confirmed decisions (Rule 9)."""
    if not response_text or not response_text.strip():
        return False, "empty_response"

    low = response_text.lower()
    # Check for unauthorized model persona
    if any(p in low for p in ["i am chatgpt", "i am claude", "as an ai developed by openai", "as a language model by google"]):
        return False, "unauthorized_external_persona"

    # Check for contradiction with confirmed sequence
    for dec in state.confirmed_decisions:
        if dec.startswith("Execution Sequence:"):
            parts = [p.strip() for p in dec.replace("Execution Sequence:", "").split("->")]
            if len(parts) >= 3:
                first, second, third = parts[0], parts[1], parts[2]
                if f"{third} comes after {first}" in response_text or f"{third} is next after {first}" in response_text:
                    if f"{second}" not in response_text.split(first)[-1].split(third)[0]:
                        return False, f"contradicts_confirmed_sequence:{dec}"

    return True, ""


class ConversationStore:
    """Unified, resilient Supabase store for conversation continuity (Rules 1, 2, 11, 15)."""

    _cache: dict[str, dict[str, Any]] = {}

    @classmethod
    def get_conversation(cls, conversation_id: str) -> tuple[ConversationState, list[TurnRecord]]:
        conversation_id = str(conversation_id or "").strip()
        if not conversation_id:
            conversation_id = "conv_default"

        # 1. Try dedicated tables: dcse_cp.escd_conversations and dcse_cp.escd_conversation_turns
        try:
            url, key = _service_config()
            safe_cid = parse.quote(conversation_id, safe="")
            code, conv_data = _http_json(
                f"{url}/rest/v1/escd_conversations?conversation_id=eq.{safe_cid}&select=*&limit=1",
                headers=_postgrest_headers(key, "dcse_cp"),
            )
            if code == 200 and isinstance(conv_data, list) and conv_data:
                raw_conv = conv_data[0]
                state = ConversationState(
                    conversation_id=conversation_id,
                    title=raw_conv.get("title") or "Conversation",
                    current_goal=raw_conv.get("current_goal") or "",
                    active_entity_lane=raw_conv.get("active_entity_lane") or "DCSE",
                    active_project_task=raw_conv.get("active_project_id") or "",
                    confirmed_decisions=raw_conv.get("confirmed_decisions") or [],
                    pinned_facts=raw_conv.get("pinned_facts") or [],
                    superseded_facts=raw_conv.get("superseded_facts") or [],
                    unresolved_questions=raw_conv.get("open_questions") or [],
                )
                _, turns_data = _http_json(
                    f"{url}/rest/v1/escd_conversation_turns?conversation_id=eq.{safe_cid}&select=*&order=seq.asc",
                    headers=_postgrest_headers(key, "dcse_cp"),
                )
                turns = [TurnRecord.from_dict(t) for t in (turns_data or [])] if isinstance(turns_data, list) else []
                return state, turns
        except Exception:
            pass

        # 2. Resilient Fallback to dcse_cp.escd_items (Rule 15: Reuse existing structures without new DDL)
        try:
            url, key = _service_config()
            safe_cid = parse.quote(f"conv_{conversation_id}", safe="")
            code, item_data = _http_json(
                f"{url}/rest/v1/escd_items?item_key=eq.{safe_cid}&select=*&limit=1",
                headers=_postgrest_headers(key, "dcse_cp"),
            )
            if code == 200 and isinstance(item_data, list) and item_data:
                refs = item_data[0].get("source_refs") or {}
                state_dict = refs.get("state") or {}
                turns_list = refs.get("turns") or []
                state = ConversationState.from_dict(state_dict) if state_dict else ConversationState(conversation_id=conversation_id)
                turns = [TurnRecord.from_dict(t) for t in turns_list]
                return state, turns
        except Exception:
            pass

        # 3. In-memory / session cache fallback
        cached = cls._cache.get(conversation_id)
        if cached:
            return cached["state"], cached["turns"]

        init_state = ConversationState(conversation_id=conversation_id)
        cls._cache[conversation_id] = {"state": init_state, "turns": []}
        return init_state, []

    @classmethod
    def persist_turn(
        cls,
        state: ConversationState,
        turn: TurnRecord,
    ) -> None:
        cid = state.conversation_id
        # Update cache
        if cid not in cls._cache:
            cls._cache[cid] = {"state": state, "turns": []}
        cls._cache[cid]["state"] = state
        cls._cache[cid]["turns"].append(turn)

        # 1. Attempt persist to dedicated tables
        dedicated_ok = False
        try:
            url, key = _service_config()
            headers = dict(_postgrest_headers(key, "dcse_cp"))
            headers["Prefer"] = "resolution=merge-duplicates,return=minimal"
            conv_payload = {
                "conversation_id": cid,
                "title": state.title,
                "current_goal": state.current_goal,
                "active_entity_lane": state.active_entity_lane,
                "active_project_id": state.active_project_task or None,
                "confirmed_decisions": state.confirmed_decisions,
                "pinned_facts": state.pinned_facts,
                "superseded_facts": state.superseded_facts,
                "open_questions": state.unresolved_questions,
                "state": state.to_dict(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            code1, _ = _http_json(f"{url}/rest/v1/escd_conversations", method="POST", headers=headers, payload=conv_payload)
            if code1 in {200, 201, 204}:
                turn_payload = turn.to_dict()
                code2, _ = _http_json(f"{url}/rest/v1/escd_conversation_turns", method="POST", headers=headers, payload=turn_payload)
                if code2 in {200, 201, 204}:
                    dedicated_ok = True
        except Exception:
            dedicated_ok = False

        if dedicated_ok:
            return

        # 2. Resilient fallback: Persist in dcse_cp.escd_items (Rule 15)
        try:
            url, key = _service_config()
            headers = dict(_postgrest_headers(key, "dcse_cp"))
            headers["Prefer"] = "resolution=merge-duplicates,return=minimal"
            all_turns = [t.to_dict() for t in cls._cache[cid]["turns"]]
            item_payload = {
                "item_key": f"conv_{cid}",
                "title": f"Conversation: {state.title[:60]}",
                "summary": state.current_goal or (f"Turns: {len(all_turns)}"),
                "status": "captured",
                "task_class": "COMMUNICATE",
                "context": "conversation",
                "actionable": False,
                "explicit_priority": 0,
                "source_system": "escd_continuity",
                "source_id": cid,
                "normalized_intent": "multi-model governed conversation",
                "source_refs": {
                    "state": state.to_dict(),
                    "turns": all_turns,
                },
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            _http_json(f"{url}/rest/v1/escd_items", method="POST", headers=headers, payload=item_payload)
        except Exception:
            pass
