from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from maven_agi.agent import Agent
from maven_agi.guardrails import Budgets, Guardrails, SandboxFS
from maven_agi.llm import build_llm
from maven_agi.tools.registry import default_registry
from maven_agi.tracing import Tracer


@dataclass
class Case:
    id: str
    input: str
    must_contain: Optional[str] = None
    match_regex: Optional[str] = None


def load_cases(path: Path) -> List[Case]:
    cases: List[Case] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            cases.append(
                Case(
                    id=obj["id"],
                    input=obj["input"],
                    must_contain=obj.get("must_contain"),
                    match_regex=obj.get("match_regex"),
                )
            )
    return cases


def build_agent_for_evals() -> Agent:
    fs = SandboxFS(os.getenv("MAVENAGI_WORKSPACE", "workspace"))
    registry = default_registry(fs)
    allowed = [t.name for t in registry.list() if t.safe]
    budgets = Budgets(max_steps=8, max_tool_calls=8)
    guardrails = Guardrails(allowed_tools=allowed, budgets=budgets)
    tracer = Tracer(os.getenv("MAVENAGI_TRACES_DIR", "traces"))
    llm = build_llm("mock")
    return Agent(llm=llm, registry=registry, guardrails=guardrails, tracer=tracer)


def check(case: Case, out: str) -> bool:
    if case.must_contain is not None:
        return case.must_contain in out
    if case.match_regex is not None:
        return re.search(case.match_regex, out) is not None
    return True


def main() -> None:
    dataset = Path("evals/datasets/smoke.jsonl")
    if not dataset.exists():
        print("Missing dataset: evals/datasets/smoke.jsonl", file=sys.stderr)
        raise SystemExit(2)

    cases = load_cases(dataset)
    agent = build_agent_for_evals()

    ok = 0
    for c in cases:
        out = agent.run(c.input)
        passed = check(c, out)
        status = "PASS" if passed else "FAIL"
        print(f"{status} {c.id}: {c.input} -> {out}")
        ok += 1 if passed else 0

    total = len(cases)
    print(f"\n{ok}/{total} passed")
    if ok != total:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
