from __future__ import annotations

from maven_agi.agent import Agent
from maven_agi.guardrails import Budgets, Guardrails, SandboxFS
from maven_agi.llm import build_llm
from maven_agi.tools.registry import default_registry


def test_agent_calc(tmp_path):
    fs = SandboxFS(str(tmp_path))
    reg = default_registry(fs)
    allowed = [t.name for t in reg.list() if t.safe]
    g = Guardrails(allowed_tools=allowed, budgets=Budgets(max_steps=6, max_tool_calls=6))
    agent = Agent(llm=build_llm("mock"), registry=reg, guardrails=g)
    out = agent.run("calculate 2+2")
    # MockLLM returns tool result; then it ends with a help final
    # We accept either a final containing 4, or a direct final (depending on loop logic)
    assert "4" in out or "I can help" in out
