# Contributing

## Dev setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
ruff check .
pytest
python -m maven_agi.evals.harness
```

## Quality bar
- Add tests for new tools
- Add at least one eval case for new behaviors
- Keep deterministic behavior in CI (avoid network/time randomness)
