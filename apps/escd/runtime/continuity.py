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

# Rule 5 Layer A: DCSE Kernel (Strictly ESCD - no name expansion)
DCSE_KERNEL = """You are ESCD, the minimal operable assistant and operational governance console for DCS Enterprise (DCSE).
OPERATIVE IDENTITY & GOVERNANCE:
1. Identity & Role: You are ESCD. When asked "Who are you and what is your role?", identify as ESCD operating for DCS Enterprise across OpenAI, Gemini, and OpenRouter execution engines. Never adopt external model personas or refer to yourself as ChatGPT, Claude, or a generic AI model.
2. Authority: DCS operator directives are the supreme authority.
3. Model Neutrality: Models (OpenAI, Gemini, OpenRouter) are interchangeable reasoning and generation engines, NOT separate personas. Maintain uniform ESCD identity, context, and operational posture across every model switch.
4. Authority Hierarchy: Explicit current DCS directive -> Current project/task state -> Verified ESCD records -> Historical/reference records -> Model inference.
5. Record Classification: Historical, candidate, REVIEW, and HOLD records remain visibly classified and non-operational unless explicitly activated by DCS.
6. Evidence Taxonomy: VERIFIED, LIKELY, UNKNOWN, ASSUMPTION.
7. Active Entity & Lanes: DCSE, Command Post, SC, SS, Employment, Polar, Tribunal.
8. Confidentiality: Never expose API keys, internal secrets, or service credentials.
"""


@dataclass
class ConversationState:
    conversation_id: str
    title: str = "New Conversation"
    active_entity_lane: str = "DCSE"
    active_project_task: str = ""

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
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TurnRecord:
        fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**fields)


def retrieve_governed_context(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """Retrieve task-routed records from Tasks, Ideas, Assets, DDNA, and Knowledge."""
    if not query or not query.strip():
        return []
    terms = set(re.findall(r"\w+", query.lower()))
    if not terms:
        return []

    collected: list[dict[str, Any]] = []

    # Knowledge
    try:
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
    except Exception:
        pass

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
    """Assemble governed context packet: DCSE kernel + visible conversation transcript + relevant ESCD retrieval + current user message."""
    messages: list[dict[str, str]] = []

    # System instruction: DCSE Kernel + relevant retrieved context (if any)
    system_sections = [DCSE_KERNEL.strip()]

    if retrieved:
        retrieval_lines = ["RELEVANT ESCD CONTEXT (Retrieval similarity does not establish authority):"]
        for item in retrieved:
            retrieval_lines.append(f"- [{item.get('type')}] {item.get('title')} (ID: {item.get('id')}) | {item.get('summary') or ''}")
        system_sections.append("\n".join(retrieval_lines))

    messages.append({"role": "system", "content": "\n\n".join(system_sections)})

    # Visible conversation transcript: raw transcript outranks inferred summaries
    for t in turns[-14:]:
        messages.append({"role": "user", "content": t.user_message})
        messages.append({"role": "assistant", "content": t.assistant_response})

    # Current user turn
    messages.append({"role": "user", "content": current_turn})
    return messages


def validate_response(response_text: str, state: ConversationState | None = None) -> tuple[bool, str]:
    """Validate response against DCSE identity and external personas."""
    if not response_text or not response_text.strip():
        return False, "empty_response"

    low = response_text.lower()
    # Check for unauthorized model persona
    if any(p in low for p in ["i am chatgpt", "i am claude", "as an ai developed by openai", "as a language model by google"]):
        return False, "unauthorized_external_persona"

    return True, ""


class ConversationStore:
    """In-memory active session store with explicit on-demand saved chat persistence in dcse_cp.escd_items."""

    _cache: dict[str, dict[str, Any]] = {}

    @classmethod
    def get_conversation(cls, conversation_id: str) -> tuple[ConversationState, list[TurnRecord]]:
        cid = str(conversation_id or "conv_default").strip() or "conv_default"
        if cid not in cls._cache:
            cls._cache[cid] = {"state": ConversationState(conversation_id=cid), "turns": []}
        return cls._cache[cid]["state"], cls._cache[cid]["turns"]

    @classmethod
    def record_turn(cls, state: ConversationState, turn: TurnRecord) -> None:
        cid = state.conversation_id
        if cid not in cls._cache:
            cls._cache[cid] = {"state": state, "turns": []}
        cls._cache[cid]["state"] = state
        cls._cache[cid]["turns"].append(turn)

    @classmethod
    def persist_turn(cls, state: ConversationState, turn: TurnRecord) -> None:
        """Alias for record_turn to record active turn in session cache without automatic DB conversion."""
        cls.record_turn(state, turn)

    @classmethod
    def save_explicit_chat(cls, conversation_id: str, title: str = "") -> dict[str, Any]:
        """Explicitly save conversation into existing dcse_cp.escd_items when operator clicks Save Chat."""
        cid = str(conversation_id or "conv_default").strip() or "conv_default"
        state, turns = cls.get_conversation(cid)
        if not turns:
            raise MVPServiceError("No conversation turns to save")

        resolved_title = str(title or "").strip()
        if not resolved_title:
            resolved_title = f"Saved Chat: {turns[0].user_message[:50]}" if turns else f"Saved Chat ({cid})"

        summary_preview = (turns[0].user_message[:120] + "...") if turns else "Saved conversation"
        timestamp = int(datetime.now(timezone.utc).timestamp())
        item_key = f"saved_chat_{cid}_{timestamp}"

        item_payload = {
            "item_key": item_key,
            "title": resolved_title[:90],
            "summary": summary_preview,
            "status": "captured",
            "task_class": "COMMUNICATE",
            "context": "conversation",
            "actionable": False,
            "explicit_priority": 0,
            "source_system": "escd_saved_chat",
            "source_id": cid,
            "normalized_intent": "explicit saved conversation",
            "source_refs": {
                "conversation_id": cid,
                "saved_at": datetime.now(timezone.utc).isoformat(),
                "turn_count": len(turns),
                "turns": [t.to_dict() for t in turns],
            },
            "evidence_refs": [],
        }

        try:
            url, key = _service_config()
            headers = dict(_postgrest_headers(key, "dcse_cp"))
            headers["Prefer"] = "return=representation"
            code, data = _http_json(
                f"{url}/rest/v1/escd_items",
                method="POST",
                headers=headers,
                payload=item_payload,
            )
            if code in {200, 201} and isinstance(data, list) and data:
                return data[0]
            if isinstance(data, dict):
                return data
        except Exception as exc:
            raise MVPServiceError(f"Failed to save chat: {exc}") from None

        return item_payload

    @classmethod
    def list_saved_chats(cls, limit: int = 50) -> list[dict[str, Any]]:
        """List explicitly saved chats from dcse_cp.escd_items."""
        try:
            url, key = _service_config()
            safe_source = parse.quote("escd_saved_chat", safe="")
            query = f"escd_items?source_system=eq.{safe_source}&select=*&order=created_at.desc,id.asc&limit={max(1, min(limit, 100))}"
            code, data = _http_json(
                f"{url}/rest/v1/{query}",
                headers=_postgrest_headers(key, "dcse_cp"),
            )
            if code == 200 and isinstance(data, list):
                return data
        except Exception:
            pass
        return []
