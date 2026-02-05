# MavenAGI — Operating Instructions

This repo is structured so you can **ship small**, then **harden** with guardrails and evals.

## Run modes

### Interactive chat
```bash
mavenagi chat
```

### One-shot run
```bash
mavenagi run --input "calculate 12*(3+4)"
```

### Evals
```bash
python -m maven_agi.evals.harness
```

## Guardrails checklist

- Set `MAX_STEPS` to a sane value (default 8)
- Keep tool allowlist tight
- Sandbox file writes under `./workspace/`
- Trace every step and tool call

## Extension points

- Swap the LLM provider: implement `BaseLLM` in `src/maven_agi/llm.py`
- Add tools: follow `docs/ADDING_TOOLS.md`
- Add evals: follow `docs/EVALS.md`
