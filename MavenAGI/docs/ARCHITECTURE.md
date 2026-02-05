# Architecture

MavenAGI is built around **one invariant**: the agent is a loop that produces either:
1) a **tool call** (structured), or
2) a **final** answer

## Components

- `Agent` (`agent.py`)
  - owns the loop: plan → act → observe → trace → stop
- `ToolRegistry` (`tools/registry.py`)
  - maps `tool_name` to an implementation
- `Guardrails` (`guardrails.py`)
  - budgets + allowlist + filesystem sandbox
- `Tracing` (`tracing.py`)
  - JSONL events for replay/debugging
- `RAG` (`rag/index.py`)
  - tiny local index for quick retrieval

## Contract: Tool action schema

Tools are invoked via an `Action`:
```json
{"type":"tool","name":"calc","input":{"expr":"19*7"}}
```

Final answers:
```json
{"type":"final","output":"The result is 133."}
```

The default MockLLM outputs these actions deterministically.
