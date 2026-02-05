from __future__ import annotations

import argparse
import os
import sys

from maven_agi.agent import Agent
from maven_agi.guardrails import Budgets, Guardrails, SandboxFS
from maven_agi.llm import build_llm
from maven_agi.tools.registry import default_registry
from maven_agi.tracing import Tracer


def _build_agent() -> Agent:
    fs = SandboxFS(os.getenv("MAVENAGI_WORKSPACE", "workspace"))
    registry = default_registry(fs)
    allowed = [t.name for t in registry.list() if t.safe]  # allow safe tools by default
    budgets = Budgets(
        max_steps=int(os.getenv("MAX_STEPS", "8")),
        max_tool_calls=int(os.getenv("MAX_TOOL_CALLS", "8")),
    )
    guardrails = Guardrails(allowed_tools=allowed, budgets=budgets)
    tracer = Tracer(os.getenv("MAVENAGI_TRACES_DIR", "traces"))
    llm = build_llm(os.getenv("LLM_PROVIDER"))
    return Agent(llm=llm, registry=registry, guardrails=guardrails, tracer=tracer)


def cmd_chat() -> int:
    agent = _build_agent()
    print("MavenAGI chat. Type 'exit' to quit.")
    while True:
        try:
            user = input("> ").strip()
        except EOFError:
            break
        if user.lower() in {"exit", "quit"}:
            break
        out = agent.run(user)
        print(out)
    print(f"trace: {agent.tracer.path}")
    return 0


def cmd_run(text: str) -> int:
    agent = _build_agent()
    out = agent.run(text)
    print(out)
    print(f"trace: {agent.tracer.path}", file=sys.stderr)
    return 0


def main() -> None:
    p = argparse.ArgumentParser(prog="mavenagi")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("chat", help="Interactive chat loop")
    pr = sub.add_parser("run", help="Run a single input")
    pr.add_argument("--input", required=True)

    args = p.parse_args()
    if args.cmd == "chat":
        raise SystemExit(cmd_chat())
    if args.cmd == "run":
        raise SystemExit(cmd_run(args.input))
    raise SystemExit(2)


if __name__ == "__main__":
    main()
