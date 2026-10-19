"""Explicit chat snapshots. All database access uses the authenticated caller's RLS client."""
from datetime import datetime, timezone
import hashlib
from urllib.parse import quote

from apps.escd.runtime.mvp_data import MVPServiceError
from apps.escd.runtime.repository import RepositoryError


def valid_messages(messages):
    if not isinstance(messages, list):
        raise MVPServiceError("invalid_chat_messages")
    result = []
    for message in messages:
        if not isinstance(message, dict):
            raise MVPServiceError("invalid_chat_messages")
        role, content = message.get("role"), message.get("content")
        if role not in {"user", "assistant"} or not isinstance(content, str):
            raise MVPServiceError("invalid_chat_messages")
        if content.strip():
            result.append({key: message[key] for key in
                           ("role", "content", "model", "provider", "seq", "governance", "error")
                           if key in message})
    return result


def seed_chat_history(user_id, conversation_id, messages, state_data=None):
    """Restore visible history for continuation without sharing the process cache across users."""
    from apps.escd.runtime.continuity import ConversationState, ConversationStore, TurnRecord
    cid = "chat_" + hashlib.sha256((user_id + "\n" + conversation_id).encode()).hexdigest()
    state = ConversationState.from_dict({**(state_data if isinstance(state_data, dict) else {}), "conversation_id": cid})
    turns, pending = [], None
    for message in valid_messages(messages):
        if message.get("error"):
            continue
        if message["role"] == "user":
            pending = message["content"]
        elif pending is not None:
            turns.append(TurnRecord(cid, len(turns) + 1, pending, message["content"],
                                    message.get("provider") or "", message.get("model") or ""))
            pending = None
    ConversationStore._cache[cid] = {"state": state, "turns": turns}
    return cid


def _path(user_id, suffix=""):
    if not user_id:
        raise MVPServiceError("chat_owner_required")
    return ("escd_items?source_system=eq.escd_saved_chat&created_by_user_id=eq."
            + quote(user_id, safe="") + suffix)


def list_chats(repo, user_id, limit=50):
    return repo._call("GET", _path(user_id,
        "&select=id,title,source_id,created_at,updated_at&order=updated_at.desc,id.asc&limit="
        + str(max(1, min(int(limit), 100)))))


def get_chat(repo, user_id, *, record_id=None, conversation_id=None):
    field, value = ("id", record_id) if record_id else ("source_id", conversation_id)
    rows = repo._call("GET", _path(user_id, "&" + field + "=eq."
        + quote(str(value), safe="") + "&select=*&order=updated_at.desc,id.asc&limit=1"))
    if not rows:
        raise MVPServiceError("saved_chat_not_found")
    record = rows[0]
    refs = record.get("source_refs")
    if not isinstance(refs, dict):
        raise MVPServiceError("invalid_saved_chat")
    messages = refs.get("messages")
    if messages is None:  # Read legacy snapshots without modifying them.
        messages = []
        for turn in refs.get("turns", []):
            messages.append({"role": "user", "content": turn.get("user_message", "")})
            messages.append({"role": "assistant", "content": turn.get("assistant_response", ""),
                             "provider": turn.get("provider"), "model": turn.get("model")})
    return {"id": record["id"], "title": record["title"],
            "conversation_id": record["source_id"], "messages": valid_messages(messages),
            "state": refs.get("state") if isinstance(refs.get("state"), dict) else {}}


def save_chat_snapshot(repo, user_id, conversation_id, messages, title="", record_id=None, state=None):
    cid = str(conversation_id or "").strip()
    if not cid or len(cid) > 200:
        raise MVPServiceError("invalid_conversation_id")
    transcript = valid_messages(messages)
    if not any(m["role"] == "user" and not m.get("error") for m in transcript):
        raise MVPServiceError("No conversation messages to save")
    # Never infer ownership from the browser or fall back to the service-role client.
    existing = None
    if record_id:
        existing = get_chat(repo, user_id, record_id=record_id)
        if existing["conversation_id"] != cid:
            raise MVPServiceError("saved_chat_thread_mismatch")
    else:
        try:
            existing = get_chat(repo, user_id, conversation_id=cid)
        except MVPServiceError as exc:
            if str(exc) != "saved_chat_not_found":
                raise
    first = next(m["content"] for m in transcript if m["role"] == "user")
    now = datetime.now(timezone.utc).isoformat()
    payload = {"title": (str(title).strip() or "Saved Chat: " + first[:50])[:90],
               "summary": first[:120], "updated_at": now,
               "source_refs": {"version": 2, "conversation_id": cid, "saved_at": now,
                               "messages": transcript, "state": state if isinstance(state, dict) else {}}}
    if existing:
        rows = repo._call("PATCH", _path(user_id, "&id=eq." + quote(existing["id"], safe="")), payload)
    else:
        key = "saved_chat_" + hashlib.sha256((user_id + "\n" + cid).encode()).hexdigest()
        payload.update({"item_key": key, "status": "captured", "task_class": "COMMUNICATE",
                        "context": "conversation", "actionable": False, "explicit_priority": 0,
                        "source_system": "escd_saved_chat", "source_id": cid,
                        "normalized_intent": "explicit saved conversation", "evidence_refs": [],
                        "created_by_user_id": user_id})
        try:
            rows = repo._call("POST", "escd_items", payload)
        except RepositoryError as exc:
            if str(exc) != "postgrest_409":
                raise
            # Concurrent first-save conflict: leave the winning snapshot intact.
            raise MVPServiceError("Chat was saved concurrently. Reopen it before saving again.") from None
    if not isinstance(rows, list) or not rows:
        raise MVPServiceError("chat_save_not_confirmed")
    return {"id": rows[0]["id"], "conversation_id": cid, "title": rows[0]["title"]}
