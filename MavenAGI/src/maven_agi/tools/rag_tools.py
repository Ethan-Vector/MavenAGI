from __future__ import annotations

from typing import Dict

from maven_agi.rag import TinyIndex
from maven_agi.types import ToolResult


def rag_search_tool_factory(index: TinyIndex):
    def _run(inp: Dict[str, object]) -> ToolResult:
        q = str(inp.get("query", "")).strip()
        if not q:
            return ToolResult(ok=False, output="Missing 'query'.")
        hits = index.search(q, k=5)
        if not hits:
            return ToolResult(ok=True, output="(no hits)")
        lines = []
        for h in hits:
            lines.append(f"- {h.doc_id} (score={h.score:.3f}): {h.snippet}")
        return ToolResult(ok=True, output="\n".join(lines))
    return _run
