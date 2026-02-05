# Adding tools

A tool is just a function with:
- `name`
- `description`
- `schema` (input keys)
- `run(input) -> ToolResult`

## Step-by-step

1) Implement it in `src/maven_agi/tools/builtins.py`
2) Register it in `src/maven_agi/tools/registry.py`
3) Add an eval case in `evals/datasets/smoke.jsonl`
4) Add a unit test in `tests/test_tools.py`

## Guardrails
Keep tools safe by design:
- Prefer pure functions
- If you touch the filesystem, only use `SandboxFS`
- Avoid network calls (use stubs)
