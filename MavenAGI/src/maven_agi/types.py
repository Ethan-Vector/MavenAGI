from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional


ActionType = Literal["tool", "final"]


@dataclass(frozen=True)
class ToolResult:
    ok: bool
    output: str
    meta: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class Action:
    type: ActionType
    name: Optional[str] = None
    input: Optional[Dict[str, Any]] = None
    output: Optional[str] = None
