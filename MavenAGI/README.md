# MavenAGI

A **clean, minimal, production-friendly** template repo for building and operating AI Agents:
- **Agent loop** (tool calls + final answers)
- **Tool registry** (typed tools, allowlist)
- **Guardrails** (budgets, sandboxed filesystem)
- **Tracing** (JSONL events)
- **Evals harness** (smoke dataset + regression hook)
- **Tests + CI + Docker**

> This repo ships with a deterministic **Mock LLM** so everything runs offline.
> You can plug in a real provider later via the `LLM_PROVIDER` interface.

---

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 2) Run the CLI
```bash
mavenagi chat
```

Try:
- `calculate (19*7)+3`
- `write a note: launch checklist: evals, budgets, tracing`
- `search docs for: guardrails`

### 3) Run tests + evals
```bash
pytest
python -m maven_agi.evals.harness
```

---

## Repo layout

- `src/maven_agi/`
  - `agent.py` — agent loop (steps, tool calls, final)
  - `llm.py` — offline `MockLLM` + provider interface
  - `tools/` — tool protocol + built-ins
  - `rag/` — tiny local retrieval (no external deps)
  - `guardrails.py` — budgets, allowlist, sandbox
  - `tracing.py` — JSONL traces
  - `cli.py` — `mavenagi` command
- `evals/` — datasets (JSONL) and config
- `tests/` — unit + smoke
- `.github/workflows/ci.yml` — lint + tests + smoke evals
- `Dockerfile`, `docker-compose.yml`

---

## Design constraints (intentional)

- **No network required.** Tools are sandboxed; `http_get_stub` exists as a placeholder.
- **Deterministic by default.** The Mock LLM uses pattern-based tool selection so CI is stable.
- **Operational primitives included.** Tracing + budgets + evals are first-class.

---

## Add a new tool (2 minutes)

1. Create a tool in `src/maven_agi/tools/builtins.py` (or a new module).
2. Register it in `src/maven_agi/tools/registry.py`.
3. Add an eval example in `evals/datasets/smoke.jsonl`.

See `docs/ADDING_TOOLS.md`.

---

## License

MIT — see `LICENSE`.
