from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional

from maven_agi.types import Action


@dataclass
class Turn:
    role: str  # "user" | "assistant" | "tool"
    content: str


class BaseLLM:
    def next_action(self, history: List[Turn], tools: List[str]) -> Action:
        raise NotImplementedError


class MockLLM(BaseLLM):
    """Deterministic offline planner.

    It chooses a tool based on simple patterns so:
    - CI is stable
    - repo works with no keys
    """

    def next_action(self, history: List[Turn], tools: List[str]) -> Action:
        user_msg = ""
        for t in reversed(history):
            if t.role == "user":
                user_msg = t.content.strip()
                break

        msg = user_msg.lower()

        # calc
        m = re.search(r"(?:calculate|calc)\s*[:]?\s*(.+)$", msg)
        if m and "calc" in tools:
            expr = m.group(1).strip()
            return Action(type="tool", name="calc", input={"expr": expr})

        # note
        m = re.search(r"(?:write a note|note)\s*[:]?\s*(.+)$", msg)
        if m and "note_append" in tools:
            text = m.group(1).strip()
            return Action(type="tool", name="note_append", input={"text": text})

        # search docs (RAG)
        m = re.search(r"(?:search docs for|docs search)\s*[:]?\s*(.+)$", msg)
        if m and "rag_search" in tools:
            q = m.group(1).strip()
            return Action(type="tool", name="rag_search", input={"query": q})

        # list files
        if ("list files" in msg or "show files" in msg) and "list_files" in tools:
            return Action(type="tool", name="list_files", input={})

        return Action(
            type="final",
            output=(
                "I can help with: "
                "calc (e.g., 'calculate 2+2'), "
                "notes (e.g., 'write a note: ...'), "
                "and docs retrieval (e.g., 'search docs for: guardrails')."
            ),
        )


def build_llm(provider: Optional[str] = None) -> BaseLLM:
    # Placeholder for future providers (OpenAI/Anthropic/local)
    # Keep deterministic default.
    _ = provider
    return MockLLM()
