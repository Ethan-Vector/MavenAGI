# Evals

Evals are **small, cheap regression tests** for agent behavior.

## Dataset format (JSONL)

Each line:
- `id`
- `input`
- `must_contain` (string) OR `match_regex` (regex)
- optional: `notes`

Example:
```json
{"id":"calc_1","input":"calculate 2+2","must_contain":"4"}
```

## Run
```bash
python -m maven_agi.evals.harness
```

## Philosophy
- Keep the suite small but representative
- Add cases for every bug you fix
- Run in CI on every PR
