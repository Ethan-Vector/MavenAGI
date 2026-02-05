from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional

from maven_agi.types import ToolResult


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    schema: Dict[str, Any]
    run: Callable[[Dict[str, Any]], ToolResult]
    safe: bool = True
    timeout_s: Optional[float] = None
