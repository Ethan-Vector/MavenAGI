from __future__ import annotations

from dataclasses import asdict
from typing import Dict, List, Optional, Tuple

from maven_agi.guardrails import Guardrails
from maven_agi.llm import BaseLLM, Turn
from maven_agi.tools.protocol import ToolSpec
from maven_agi.tools.registry import ToolRegistry
from maven_agi.tracing import Tracer
from maven_agi.types import Action, ToolResult


class Agent:
    def __init__(
        self,
        llm: BaseLLM,
        registry: ToolRegistry,
        guardrails: Guardrails,
        tracer: Optional[Tracer] = None,
    ) -> None:
        self.llm = llm
        self.registry = registry
        self.guardrails = guardrails
        self.tracer = tracer or Tracer()
        self.history: List[Turn] = []

    def _tool_names(self) -> List[str]:
        return [t.name for t in self.registry.list() if t.name in self.guardrails.allowed_tools]

    def run(self, user_input: str) -> str:
        self.history.append(Turn(role="user", content=user_input))

        tool_calls = 0
        for step in range(self.guardrails.budgets.max_steps):
            self.guardrails.check_step_budget(step)
            self.guardrails.check_tool_budget(tool_calls)

            action = self.llm.next_action(self.history, tools=self._tool_names())
            self.tracer.emit({"event": "agent_action", "step": step, "action": asdict(action)})

            if action.type == "final":
                out = action.output or ""
                self.history.append(Turn(role="assistant", content=out))
                self.tracer.emit({"event": "agent_final", "step": step, "output": out})
                return out

            if action.type == "tool":
                name = action.name or ""
                inp = action.input or {}
                self.guardrails.check_tool_allowed(name)

                tool_spec = self.registry.get(name)
                tool_calls += 1

                res = tool_spec.run(inp)
                self.tracer.emit(
                    {
                        "event": "tool_call",
                        "step": step,
                        "tool": name,
                        "input": inp,
                        "result": {"ok": res.ok, "output": res.output, "meta": res.meta},
                    }
                )
                self.history.append(Turn(role="tool", content=f"{name}: {res.output}"))

                # After tool call, let the LLM decide next action (loop continues)
                continue

        # Safety net
        out = "Stopped: step budget exceeded."
        self.history.append(Turn(role="assistant", content=out))
        self.tracer.emit({"event": "agent_stop", "output": out})
        return out
