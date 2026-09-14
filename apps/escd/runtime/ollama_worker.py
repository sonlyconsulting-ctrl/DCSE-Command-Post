from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib import error, parse, request

PROJECT_REF = "nevgdyfpxdaloacuutal"
WORKER_KEY = os.getenv("ESCD_WORKER_KEY", "DCS-WINDOWS-OLLAMA-01")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:latest")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
POLL_SECONDS = float(os.getenv("ESCD_WORKER_POLL_SECONDS", "2.0"))
LEASE_SECONDS = int(os.getenv("ESCD_WORKER_LEASE_SECONDS", "600"))


class WorkerError(RuntimeError):
    pass


def _config() -> tuple[str, str]:
    url = (os.getenv("SUPABASE_URL") or "").rstrip("/")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or ""
    if not url or not key:
        raise WorkerError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    if parse.urlparse(url).hostname != f"{PROJECT_REF}.supabase.co":
        raise WorkerError("worker must target the SC-Command-Post Supabase project")
    return url, key


def _headers(schema: str = "dcse_cp", *, write: bool = False) -> dict[str, str]:
    _, key = _config()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept-Profile": schema,
        "Content-Type": "application/json",
    }
    if write:
        headers["Content-Profile"] = schema
        headers["Prefer"] = "return=representation"
    return headers


def _http_json(url: str, *, method: str = "GET", headers: dict[str, str] | None = None,
               payload: Any = None, timeout: int = 60) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=body, headers=headers or {}, method=method)
    for attempt in range(2):
        try:
            with request.urlopen(req, timeout=timeout) as response:
                raw = response.read().decode("utf-8")
                return json.loads(raw or "null")
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise WorkerError(f"http_{exc.code}:{detail[:300]}") from None
        except (error.URLError, TimeoutError, OSError) as exc:
            if attempt == 0 and method == "GET":
                time.sleep(1)
                continue
            raise WorkerError(f"connection_failed:{exc}") from None


def _rest(path: str, *, method: str = "GET", payload: Any = None,
          schema: str = "dcse_cp", timeout: int = 30) -> Any:
    url, _ = _config()
    return _http_json(
        f"{url}/rest/v1/{path.lstrip('/')}",
        method=method,
        headers=_headers(schema, write=method != "GET"),
        payload=payload,
        timeout=timeout,
    )


def _rpc(name: str, payload: dict[str, Any]) -> Any:
    return _rest(f"rpc/{name}", method="POST", payload=payload)


def _one(value: Any) -> dict[str, Any] | None:
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _heartbeat(turn_id: str | None = None, status: str = "BUSY") -> None:
    _rpc("escd_worker_heartbeat", {
        "p_worker_key": WORKER_KEY,
        "p_turn_id": turn_id,
        "p_lease_seconds": LEASE_SECONDS,
        "p_status": status,
    })


def _requeue_expired() -> int:
    value = _rpc("escd_requeue_expired_turns", {"p_limit": 25})
    if isinstance(value, int):
        return value
    if isinstance(value, list) and value:
        try:
            return int(value[0])
        except Exception:
            return 0
    return 0


def _claim() -> dict[str, Any] | None:
    rows = _rpc("escd_claim_next_turn", {
        "p_worker_key": WORKER_KEY,
        "p_lease_seconds": LEASE_SECONDS,
    })
    return _one(rows)


def _patch_turn(turn_id: str, update: dict[str, Any]) -> dict[str, Any]:
    safe = parse.quote(turn_id, safe="")
    rows = _rest(
        f"escd_operation_turns?id=eq.{safe}",
        method="PATCH",
        payload=update,
    )
    row = _one(rows)
    if not row:
        raise WorkerError("turn_update_failed")
    return row


def _event(turn_id: str, event_type: str, stage: str, actor_type: str,
           payload: dict[str, Any], *, control: str | None = None,
           evidence_refs: list[Any] | None = None, direction: str = "INTERNAL",
           actor_ref: str | None = None) -> None:
    body = {
        "turn_id": turn_id,
        "event_type": event_type,
        "stage": stage,
        "direction": direction,
        "actor_type": actor_type,
        "actor_ref": actor_ref,
        "control_state": control,
        "payload": payload,
        "evidence_refs": evidence_refs or [],
    }
    _rest("escd_operation_events", method="POST", payload=body)


def _record_return(turn_id: str, stage: str, provider: str, model: str,
                   payload: dict[str, Any], evidence_refs: list[Any]) -> None:
    _rpc("escd_record_return", {
        "p_turn_id": turn_id,
        "p_event_type": "PROVIDER_RETURN",
        "p_stage": stage,
        "p_actor_type": "PROVIDER",
        "p_actor_ref": f"{provider}/{model}",
        "p_control_state": "RETURN_TO_ORCHESTRATOR",
        "p_payload": payload,
        "p_evidence_refs": evidence_refs,
    })


def _conversation_snapshot(conversation_id: str) -> dict[str, Any]:
    data = _rpc("escd_conversation_snapshot", {"p_conversation_id": conversation_id})
    return _one(data) or (data if isinstance(data, dict) else {})


def _resolve_subjects(text: str) -> list[dict[str, Any]]:
    rows = _rpc("escd_resolve_subjects", {"p_text": text, "p_limit": 10})
    return rows if isinstance(rows, list) else []


def _subject_context(subjects: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    collected: list[dict[str, Any]] = []
    refs: list[str] = []
    for subject in subjects[:5]:
        sid = str(subject.get("id") or "")
        if not sid:
            continue
        safe = parse.quote(sid, safe="")
        links = _rest(
            f"escd_subject_links?subject_id=eq.{safe}&select=*&order=created_at.asc&limit=50"
        )
        subject_block = {
            "subject": subject,
            "links": [],
        }
        for link in (links if isinstance(links, list) else [])[:10]:
            obj_type = str(link.get("object_type") or "")
            obj_ref = str(link.get("object_ref") or "")
            record: Any = None
            if obj_type == "item":
                ref = parse.quote(obj_ref, safe="")
                record = _one(_rest(
                    f"escd_items?id=eq.{ref}&select=id,item_key,title,summary,status,context,source_refs,evidence_refs,updated_at&limit=1"
                ))
                refs.append(f"item://{obj_ref}")
            elif obj_type == "knowledge":
                ref = parse.quote(obj_ref, safe="")
                record = _one(_rest(
                    f"escd_knowledge_records?id=eq.{ref}&select=id,knowledge_key,title,content,authority_classification,confidence,status,evidence_refs,updated_at&limit=1"
                ))
                refs.append(f"knowledge://{obj_ref}")
            elif obj_type == "operation_turn":
                ref = parse.quote(obj_ref, safe="")
                record = _one(_rest(
                    f"escd_operation_turns?id=eq.{ref}&select=turn_key,state,stage,request_text,final_response,created_at,terminal_at&limit=1"
                ))
                refs.append(f"operation://{obj_ref}")
            elif obj_type == "conversation":
                refs.append(f"conversation://{obj_ref}")
            elif obj_type == "file":
                refs.append(f"file://{obj_ref}")
            subject_block["links"].append({
                "type": obj_type,
                "ref": obj_ref,
                "relation": link.get("relation_type"),
                "confidence": link.get("confidence"),
                "record": record,
            })
        collected.append(subject_block)
        refs.append(f"subject://{subject.get('subject_key') or sid}")
    return collected, sorted(set(refs))


def _ollama(messages: list[dict[str, str]], *, json_mode: bool = False,
            timeout: int = 180) -> tuple[str, dict[str, Any]]:
    body: dict[str, Any] = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2, "num_predict": 1800},
    }
    if json_mode:
        body["format"] = "json"
    data = _http_json(
        f"{OLLAMA_BASE_URL}/api/chat",
        method="POST",
        headers={"Content-Type": "application/json"},
        payload=body,
        timeout=timeout,
    )
    content = str((data or {}).get("message", {}).get("content") or "").strip()
    if not content:
        raise WorkerError("ollama_empty_response")
    return content, data if isinstance(data, dict) else {}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _run_rules(candidate: dict[str, Any], turn: dict[str, Any],
               subjects: list[dict[str, Any]], evidence_refs: list[str]) -> dict[str, Any]:
    root = _repo_root()
    dcse_path = str(root / "dcse")
    if dcse_path not in sys.path:
        sys.path.insert(0, dcse_path)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))

    from orchestrator import Orchestrator  # type: ignore
    from model import Operation  # type: ignore

    entity = str(candidate.get("entity") or "task").lower()
    action = str(candidate.get("action") or "evaluate").lower()
    capabilities = tuple(str(x).lower() for x in (candidate.get("capabilities") or ["escd"]))
    objective = str(candidate.get("objective") or turn.get("request_text") or "")
    subject_item = None
    for block in subjects:
        for link in block.get("links") or []:
            if link.get("type") == "item" and isinstance(link.get("record"), dict):
                subject_item = link["record"]
                break
        if subject_item:
            break

    facts = {
        "task_id": (subject_item or {}).get("id") or turn.get("turn_key"),
        "objective": objective[:1000],
        "acceptance_criteria": [
            "response grounded in persisted conversation or subject evidence",
            "provider returns control and payload to orchestrator",
            "no unsupported external-state claim",
        ],
        "owner": "DCS Level 0",
        "state": (subject_item or {}).get("status") or "open",
        "turn_id": turn.get("turn_key"),
        "reversibility": "reversible",
        "consequence": "low",
        "evidence_refs": evidence_refs,
        "subject_count": len(subjects),
    }
    op = Operation(
        entity=entity,
        action=action,
        capabilities=capabilities,
        actor="dcs",
        directive="DCS-ORCHESTRATE-V1",
        facts=facts,
    )
    outcome = Orchestrator().run(op, execute=False, stage="plan")
    results = []
    for result in outcome.plan.results:
        results.append({
            "rule_id": getattr(result, "rule_id", None),
            "verdict": str(getattr(result, "verdict", "UNKNOWN")),
            "mode": str(getattr(result, "mode", "")),
            "name": str(getattr(result, "name", "")),
        })
    return {
        "operation_id": op.id,
        "disposition": outcome.disposition,
        "reason": outcome.reason,
        "rules": results,
        "rule_count": len(results),
        "fail_count": sum(1 for r in results if r["verdict"] == "FAIL"),
        "unknown_count": sum(1 for r in results if r["verdict"] == "UNKNOWN"),
    }


def _append_assistant_turn(turn: dict[str, Any], content: str, metadata: dict[str, Any]) -> dict[str, Any]:
    data = _rpc("escd_append_conversation_turn", {
        "p_conversation_id": turn["conversation_id"],
        "p_actor_label": "ESCD",
        "p_actor_role": "assistant",
        "p_summary": content,
        "p_metadata": metadata,
    })
    row = _one(data)
    if not row:
        raise WorkerError("assistant_turn_persistence_failed")
    return row


def _usage(raw: dict[str, Any]) -> dict[str, Any]:
    p = int(raw.get("prompt_eval_count") or 0)
    c = int(raw.get("eval_count") or 0)
    return {
        "prompt_tokens": p,
        "completion_tokens": c,
        "total_tokens": p + c,
        "cost_usd": 0.0,
        "cost_label": "$0.0000 (Local)",
        "provider": "ollama",
        "model": OLLAMA_MODEL,
    }


def _complete(turn: dict[str, Any], content: str, *, evidence_refs: list[str],
              usage: dict[str, Any], rule_evidence: dict[str, Any] | None = None) -> None:
    _patch_turn(turn["id"], {
        "state": "RESPONDING",
        "stage": "RESPONSE",
        "control_state": "ORCHESTRATOR",
    })
    metadata = {
        "lane": "operational" if (turn.get("request_payload") or {}).get("mode") == "orchestrate" else "conversational",
        "provider": "ollama",
        "model": OLLAMA_MODEL,
        "worker": WORKER_KEY,
        "usage": usage,
        "evidence_refs": evidence_refs,
        "operation_turn_key": turn.get("turn_key"),
        "rule_evidence": rule_evidence or {},
    }
    assistant_turn = _append_assistant_turn(turn, content, metadata)
    final = {
        "content": content,
        "control": "COMPLETE",
        "provider": "ollama",
        "model": OLLAMA_MODEL,
        "worker": WORKER_KEY,
        "evidence_refs": evidence_refs,
        "usage": usage,
        "rule_evidence": rule_evidence or {},
    }
    _event(
        turn["id"], "FINAL_RESPONSE", "RESPONSE", "ORCHESTRATOR",
        final, control="COMPLETE", evidence_refs=evidence_refs,
        actor_ref=WORKER_KEY,
    )
    _patch_turn(turn["id"], {
        "response_turn_id": assistant_turn["id"],
        "final_response": final,
        "state": "COMPLETE",
        "stage": "TERMINAL",
        "control_state": "TERMINAL",
        "active_provider": "ollama",
        "active_model": OLLAMA_MODEL,
    })


def _fail(turn: dict[str, Any], exc: Exception) -> None:
    message = str(exc)[:500]
    try:
        _event(
            turn["id"], "ERROR", turn.get("stage") or "EXECUTION", "SYSTEM",
            {"error": message}, control="FAIL", actor_ref=WORKER_KEY,
        )
        _patch_turn(turn["id"], {
            "state": "FAILED",
            "stage": "TERMINAL",
            "control_state": "TERMINAL",
            "error_code": message,
            "active_provider": "ollama",
            "active_model": OLLAMA_MODEL,
        })
    except Exception:
        pass


def _process_conversation(turn: dict[str, Any]) -> None:
    payload = turn.get("request_payload") or {}
    messages = payload.get("messages") or []
    clean = []
    for msg in messages[-30:]:
        role = str(msg.get("role") or "user")
        content = str(msg.get("content") or "").strip()
        if content and role in {"system", "user", "assistant"}:
            clean.append({"role": role, "content": content[:12000]})
    if not clean:
        clean = [{"role": "user", "content": turn.get("request_text") or ""}]
    clean.insert(0, {
        "role": "system",
        "content": (
            "You are ESCD's local conversational inference worker. Respond naturally and directly. "
            "This lane is conversational only: do not claim that tools, deployments, database writes, "
            "or governed actions occurred. Return only the conversational answer."
        ),
    })

    _patch_turn(turn["id"], {"state": "INTERPRETING", "stage": "PRECONDITION",
                             "active_provider": "ollama", "active_model": OLLAMA_MODEL})
    _heartbeat(turn["id"])
    _patch_turn(turn["id"], {"state": "PLANNING", "stage": "PRECONDITION"})
    _patch_turn(turn["id"], {"state": "EXECUTING", "stage": "EXECUTION"})
    content, raw = _ollama(clean)
    usage = _usage(raw)
    payload_return = {"content": content, "mode": "conversation", "usage": usage}
    refs = [f"ollama://{WORKER_KEY}/{OLLAMA_MODEL}/{turn['turn_key']}"]
    _record_return(turn["id"], "EXECUTION", "ollama", OLLAMA_MODEL, payload_return, refs)
    _patch_turn(turn["id"], {"state": "VERIFYING", "stage": "POSTCONDITION"})
    _event(
        turn["id"], "AUDIT", "AUDIT", "AUDITOR",
        {"checks": {"nonempty_response": bool(content), "governed_actions_claimed": False}},
        evidence_refs=refs, actor_ref="dcse-conversation-audit",
    )
    _complete(turn, content, evidence_refs=refs, usage=usage, rule_evidence={
        "lane": "conversation",
        "governed_actions": 0,
    })


def _process_orchestrate(turn: dict[str, Any]) -> None:
    request_text = str(turn.get("request_text") or "")
    snapshot = _conversation_snapshot(turn["conversation_id"])
    resolved = _resolve_subjects(request_text)
    subjects, evidence_refs = _subject_context(resolved)
    evidence_refs.append(f"conversation://{turn['conversation_id']}")
    evidence_refs.append(f"operation://{turn['turn_key']}")
    evidence_refs = sorted(set(evidence_refs))

    _patch_turn(turn["id"], {
        "state": "INTERPRETING",
        "stage": "PRECONDITION",
        "active_provider": "ollama",
        "active_model": OLLAMA_MODEL,
    })
    _heartbeat(turn["id"])

    interpretation_prompt = {
        "request": request_text,
        "conversation": {
            "title": (snapshot.get("conversation") or {}).get("title"),
            "recent_turns": (snapshot.get("turns") or [])[-8:],
        },
        "resolved_subjects": subjects,
        "required_schema": {
            "operation_candidate": {
                "entity": "task|idea|asset|ddna|knowledge",
                "action": "evaluate|inspect|create|edit|read",
                "capabilities": ["escd"],
                "objective": "string",
                "confidence": 0.0,
            }
        },
    }
    interpretation_text, raw_interpret = _ollama([
        {
            "role": "system",
            "content": (
                "Interpret the user's request as a bounded DCSE operation candidate. "
                "Use only the supplied persisted context. Do not claim execution. "
                "Return valid JSON only with key operation_candidate which is an object containing: "
                "entity, action, capabilities, objective, confidence."
            ),
        },
        {"role": "user", "content": json.dumps(interpretation_prompt, default=str)},
    ], json_mode=True)
    try:
        interpreted = json.loads(interpretation_text)
        candidate = interpreted.get("operation_candidate")
        if candidate is None and isinstance(interpreted, dict):
            candidate = interpreted
    except Exception as exc:
        raise WorkerError(f"operation_candidate_invalid_json:{exc}") from None

    if isinstance(candidate, str):
        candidate = {
            "objective": candidate,
            "entity": "task",
            "action": "evaluate",
            "capabilities": ["escd"],
            "confidence": 0.9,
        }
    elif isinstance(candidate, dict):
        if not candidate.get("objective"):
            candidate["objective"] = candidate.get("summary") or candidate.get("title") or candidate.get("task") or turn.get("request_text") or "bounded operation"
        candidate.setdefault("entity", "task")
        candidate.setdefault("action", "evaluate")
        candidate.setdefault("capabilities", ["escd"])
        candidate.setdefault("confidence", 0.9)
    else:
        candidate = {
            "objective": str(turn.get("request_text") or "bounded operation"),
            "entity": "task",
            "action": "evaluate",
            "capabilities": ["escd"],
            "confidence": 0.9,
        }

    _patch_turn(turn["id"], {
        "operation_candidate": candidate,
        "state": "PLANNING",
        "stage": "PRECONDITION",
    })

    rule_evidence = _run_rules(candidate, turn, subjects, evidence_refs)
    _event(
        turn["id"], "RULE_EVALUATION", "PRECONDITION", "ORCHESTRATOR",
        rule_evidence, evidence_refs=evidence_refs, actor_ref="dcse-rule-runtime",
    )

    disposition = str(rule_evidence.get("disposition") or "")
    if disposition in {"REFUSE", "REJECT"}:
        _patch_turn(turn["id"], {
            "state": "REFUSED",
            "stage": "TERMINAL",
            "control_state": "TERMINAL",
            "final_response": {
                "content": f"Operation refused by DCSE rules: {rule_evidence.get('reason')}",
                "control": "REFUSED",
                "evidence_refs": evidence_refs,
                "rule_evidence": rule_evidence,
            },
        })
        return
    if disposition in {"ESCALATE"}:
        _patch_turn(turn["id"], {
            "state": "WAITING_USER",
            "stage": "PRECONDITION",
            "control_state": "WAITING_USER",
            "final_response": {
                "content": f"DCS decision required before continuation: {rule_evidence.get('reason')}",
                "control": "NEEDS_USER",
                "evidence_refs": evidence_refs,
                "rule_evidence": rule_evidence,
            },
        })
        return

    _patch_turn(turn["id"], {"state": "EXECUTING", "stage": "EXECUTION"})
    _heartbeat(turn["id"])

    response_input = {
        "request": request_text,
        "operation_candidate": candidate,
        "rule_evaluation": rule_evidence,
        "resolved_subjects": subjects,
        "conversation_recent_turns": (snapshot.get("turns") or [])[-8:],
        "evidence_refs": evidence_refs,
    }
    response_text, raw_response = _ollama([
        {
            "role": "system",
            "content": (
                "Produce the ESCD answer for the user using only the supplied persisted context and rule evaluation. "
                "Do not invent files, schemas, deployments, rule results, or external actions. "
                "Clearly distinguish verified facts, likely interpretations, unknowns, and recommended next actions. "
                "Return valid JSON only with keys content, facts_used, unknowns, recommendations."
            ),
        },
        {"role": "user", "content": json.dumps(response_input, default=str)},
    ], json_mode=True)
    try:
        response_obj = json.loads(response_text)
        if isinstance(response_obj, dict):
            content = str(response_obj.get("content") or "").strip()
            if not content:
                content = str(response_obj.get("answer") or response_obj.get("response") or response_obj.get("summary") or "").strip()
            if not content and (response_obj.get("recommendations") or response_obj.get("facts_used")):
                parts = []
                if response_obj.get("facts_used"):
                    parts.append("Facts: " + "; ".join(str(x) for x in response_obj["facts_used"]))
                if response_obj.get("recommendations"):
                    parts.append("Recommendations: " + "; ".join(str(x) for x in response_obj["recommendations"]))
                content = "\n\n".join(parts).strip()
        else:
            response_obj = {"content": str(response_obj)}
            content = str(response_obj["content"]).strip()
    except Exception:
        response_obj = {"content": response_text.strip()}
        content = response_text.strip()
    if not content:
        content = f"Governed evaluation complete for: {candidate.get('objective') or request_text}."

    usage = _usage(raw_response)
    provider_payload = {
        "content": content,
        "facts_used": response_obj.get("facts_used") or [],
        "unknowns": response_obj.get("unknowns") or [],
        "recommendations": response_obj.get("recommendations") or [],
        "operation_candidate": candidate,
        "usage": usage,
    }
    provider_ref = f"ollama://{WORKER_KEY}/{OLLAMA_MODEL}/{turn['turn_key']}"
    evidence_refs = sorted(set(evidence_refs + [provider_ref]))
    _record_return(turn["id"], "EXECUTION", "ollama", OLLAMA_MODEL, provider_payload, evidence_refs)

    _patch_turn(turn["id"], {"state": "VERIFYING", "stage": "POSTCONDITION"})
    audit = {
        "provider_return_has_payload": bool(provider_payload),
        "provider_return_control": "RETURN_TO_ORCHESTRATOR",
        "response_nonempty": bool(content),
        "subject_resolution_count": len(subjects),
        "evidence_ref_count": len(evidence_refs),
        "rules_evaluated": rule_evidence.get("rule_count", 0),
        "rules_failed": rule_evidence.get("fail_count", 0),
        "rules_unknown": rule_evidence.get("unknown_count", 0),
    }
    _event(
        turn["id"], "AUDIT", "AUDIT", "AUDITOR",
        audit, evidence_refs=evidence_refs, actor_ref="dcse-independent-contract-audit",
    )
    _complete(
        turn,
        content,
        evidence_refs=evidence_refs,
        usage=usage,
        rule_evidence=rule_evidence,
    )


def process_turn(turn: dict[str, Any]) -> None:
    try:
        mode = str((turn.get("request_payload") or {}).get("mode") or "orchestrate")
        if mode == "conversation":
            _process_conversation(turn)
        else:
            _process_orchestrate(turn)
    except Exception as exc:
        _fail(turn, exc)
    finally:
        try:
            _heartbeat(None, "IDLE")
        except Exception:
            pass


def run(*, once: bool = False) -> int:
    _requeue_expired()
    _heartbeat(None, "IDLE")
    processed = 0
    while True:
        turn = _claim()
        if not turn:
            if once:
                return processed
            _heartbeat(None, "IDLE")
            time.sleep(POLL_SECONDS)
            continue
        process_turn(turn)
        processed += 1
        if once:
            return processed


def main() -> int:
    parser = argparse.ArgumentParser(description="DCSE/ESCD local Ollama orchestration worker")
    parser.add_argument("--once", action="store_true", help="Process at most one queued turn and exit")
    args = parser.parse_args()
    return run(once=args.once)


if __name__ == "__main__":
    raise SystemExit(main())
