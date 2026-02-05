from __future__ import annotations

from typing import Dict, Iterable, List

from maven_agi.guardrails import SandboxFS
from maven_agi.tools.builtins import (
    calc_tool,
    http_get_stub,
    list_files_tool_factory,
    note_append_tool_factory,
    read_file_tool_factory,
    write_file_tool_factory,
)
from maven_agi.tools.protocol import ToolSpec
from maven_agi.tools.rag_tools import rag_search_tool_factory
from maven_agi.rag import TinyIndex


class ToolRegistry:
    def __init__(self, tools: Iterable[ToolSpec]) -> None:
        self._tools: Dict[str, ToolSpec] = {t.name: t for t in tools}

    def get(self, name: str) -> ToolSpec:
        if name not in self._tools:
            raise KeyError(f"Unknown tool: {name}")
        return self._tools[name]

    def list(self) -> List[ToolSpec]:
        return list(self._tools.values())


def default_registry(fs: SandboxFS) -> ToolRegistry:
    tools = [
        # Local docs retrieval index (Markdown)
        _idx = TinyIndex.from_docs_dir('docs')

        ToolSpec(
            name="calc",
            description="Safely evaluate a basic arithmetic expression.",
            schema={"expr": "string"},
            run=calc_tool,
            safe=True,
        ),
        ToolSpec(
            name="note_append",
            description="Append a line to workspace/notes.txt.",
            schema={"text": "string"},
            run=note_append_tool_factory(fs),
            safe=True,
        ),
        ToolSpec(
            name="write_file",
            description="Write a text file under the sandboxed workspace.",
            schema={"path": "string", "content": "string"},
            run=write_file_tool_factory(fs),
            safe=True,
        ),
        ToolSpec(
            name="read_file",
            description="Read a text file under the sandboxed workspace.",
            schema={"path": "string"},
            run=read_file_tool_factory(fs),
            safe=True,
        ),
        ToolSpec(
            name="list_files",
            description="List files under the sandboxed workspace.",
            schema={},
            run=list_files_tool_factory(fs),
            safe=True,
        ),
        ToolSpec(
            name="rag_search",
            description="Search local docs/ (tiny retrieval, offline).",
            schema={"query": "string"},
            run=rag_search_tool_factory(_idx),
            safe=True,
        ),
        ToolSpec(
            name="http_get_stub",
            description="Stub for HTTP GET (network disabled by default).",
            schema={"url": "string"},
            run=http_get_stub,
            safe=False,
        ),
    ]
    return ToolRegistry(tools)
