"""
DCSE RAG Engine — DDNA Generation Envelope
Doc: DCSE-CP/RAG/GEN/20260624-001
Status: CANDIDATE MATERIAL — DCS REVIEW REQUIRED

Every Ollama generation call is wrapped in this envelope.
The envelope enforces:
  - DCSE voice profile (precise, no hype, no em dashes, no emoji)
  - PS firewall check on retrieved context before generation
  - Dual-mode output: structured_data (JSON) + narrative_summary (Markdown)

LLM: Ollama local (Llama 3.1 8B or Mistral 7B)
Orchestration: LangChain OSS
"""

import json
import logging
import re
from typing import Any

logger = logging.getLogger("dcse.rag.generation")

# DCSE voice enforcement rules embedded in system prompt
DCSE_SYSTEM_PROMPT = """
You are the DCSE Command Post intelligence layer. You operate under v6.9 governance.

VOICE RULES — enforce strictly:
- Precise, load-bearing, zero ornamentation.
- No hype. No celebration language. No generic business language.
- No em dashes (never use -- or the em dash character).
- No emoji of any kind.
- Every sentence does work. No filler.
- Do not use I, we, or us unless the query explicitly requests first-person.
- Tone: command center at operational tempo. Calm, clear, ready.

PS FIREWALL — absolute rule:
- If any retrieved context contains PS material (case facts, court strategy, discovery,
  Ballentine references, Seals v. DHHS content, docket references, or anything tagged
  lane=PS), do not include it in your response. Output a stop-gate message instead:
  "PS material detected in context. Output halted. Route to PS-designated session."

OUTPUT FORMAT — always return valid JSON with exactly these two keys:
{
  "structured_data": {
    "source_files": [],
    "status_tags": [],
    "confidence": 0.0,
    "affected_modules": [],
    "lane": "DCSE"
  },
  "narrative_summary": "Markdown string"
}

Do not return plain text. Do not wrap the JSON in code fences. Return raw JSON only.
""".strip()

PS_CONTEXT_INDICATORS = [
    "8:23CV489",
    "Seals v. DHHS",
    "Ballentine",
    "Case 8:23",
    "deposition prep",
    "court filing",
    "lane=PS",
    "lane: PS",
    "PS firewall breach",
]


def check_context_for_ps(context: str) -> bool:
    """Return True if context contains PS-indicator terms."""
    context_lower = context.lower()
    for term in PS_CONTEXT_INDICATORS:
        if term.lower() in context_lower:
            logger.error(
                "PS FIREWALL HALT — PS-indicator term found in retrieved context: %s",
                term,
            )
            return True
    return False


def build_user_prompt(query: str, context: str, lane: str = "DCSE") -> str:
    return f"""
Lane: {lane}
Governance: v6.9

Retrieved context:
{context}

Query:
{query}

Return your response as a JSON object with structured_data and narrative_summary keys.
""".strip()


def parse_dual_mode_response(raw: str) -> dict:
    """
    Parse LLM response into dual-mode payload.
    Handles cases where the model wraps JSON in markdown fences.
    """
    # Strip markdown fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
        if "structured_data" in parsed and "narrative_summary" in parsed:
            return parsed
    except json.JSONDecodeError:
        pass

    # Fallback: return raw as narrative_summary
    return {
        "structured_data": {
            "source_files": [],
            "status_tags": ["parse_error"],
            "confidence": 0.0,
            "affected_modules": [],
            "lane": "DCSE",
        },
        "narrative_summary": raw,
    }


def generate(
    query: str,
    context: str,
    lane: str = "DCSE",
    ollama_model: str = "llama3.1:8b",
    ollama_base_url: str = "http://localhost:11434",
) -> dict[str, Any]:
    """
    Run a DDNA-enveloped generation call.

    1. PS check on context — halt if PS content detected
    2. Build prompt with DCSE voice system prompt
    3. Call Ollama via LangChain
    4. Parse and return dual-mode payload

    Returns the dual-mode payload dict or a halt record.
    """

    # PS firewall check on retrieved context
    if check_context_for_ps(context):
        return {
            "structured_data": {
                "source_files": [],
                "status_tags": ["PS_HALT"],
                "confidence": 0.0,
                "affected_modules": [],
                "lane": "PS_BLOCKED",
            },
            "narrative_summary": (
                "PS material detected in retrieved context. "
                "Output halted. Route to PS-designated session."
            ),
        }

    try:
        from langchain_ollama import OllamaLLM
        from langchain_core.messages import HumanMessage, SystemMessage
        from langchain_core.prompts import ChatPromptTemplate
    except ImportError as e:
        logger.error("LangChain/Ollama dependency missing: %s. Run: pip install langchain-ollama langchain-core", e)
        return {
            "structured_data": {"source_files": [], "status_tags": ["dependency_error"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": f"Generation dependency error: {e}",
        }

    llm = OllamaLLM(
        model=ollama_model,
        base_url=ollama_base_url,
        temperature=0.1,
    )

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", DCSE_SYSTEM_PROMPT),
        ("human", "{user_prompt}"),
    ])

    user_prompt = build_user_prompt(query, context, lane)

    try:
        chain = prompt_template | llm
        raw_response = chain.invoke({"user_prompt": user_prompt})
    except Exception as e:
        logger.error("Ollama generation failed: %s", e)
        return {
            "structured_data": {"source_files": [], "status_tags": ["generation_error"], "confidence": 0.0, "affected_modules": [], "lane": lane},
            "narrative_summary": f"Generation failed: {e}",
        }

    return parse_dual_mode_response(raw_response)
