from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Iterable, Set


@dataclass
class Budgets:
    max_steps: int = 8
    max_tool_calls: int = 8


class Guardrails:
    def __init__(self, allowed_tools: Iterable[str], budgets: Budgets | None = None) -> None:
        self.allowed_tools: Set[str] = set(allowed_tools)
        self.budgets = budgets or Budgets()

    def check_tool_allowed(self, name: str) -> None:
        if name not in self.allowed_tools:
            raise PermissionError(f"Tool '{name}' is not in allowlist.")

    def check_step_budget(self, step_idx: int) -> None:
        if step_idx >= self.budgets.max_steps:
            raise RuntimeError(f"Max steps exceeded: {self.budgets.max_steps}")

    def check_tool_budget(self, tool_calls: int) -> None:
        if tool_calls > self.budgets.max_tool_calls:
            raise RuntimeError(f"Max tool calls exceeded: {self.budgets.max_tool_calls}")


class SandboxFS:
    def __init__(self, root: str | None = None) -> None:
        self.root = os.path.abspath(root or os.getenv("MAVENAGI_WORKSPACE", "workspace"))
        os.makedirs(self.root, exist_ok=True)

    def _safe_path(self, rel_path: str) -> str:
        rel_path = rel_path.lstrip("/").replace("..", "")
        path = os.path.abspath(os.path.join(self.root, rel_path))
        if not path.startswith(self.root):
            raise PermissionError("Path escapes sandbox.")
        return path

    def write_text(self, rel_path: str, content: str) -> str:
        path = self._safe_path(rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def read_text(self, rel_path: str) -> str:
        path = self._safe_path(rel_path)
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def append_text(self, rel_path: str, content: str) -> str:
        path = self._safe_path(rel_path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(content)
        return path

    def list_files(self) -> list[str]:
        out: list[str] = []
        for dirpath, _, filenames in os.walk(self.root):
            for fn in filenames:
                full = os.path.join(dirpath, fn)
                out.append(os.path.relpath(full, self.root))
        out.sort()
        return out
