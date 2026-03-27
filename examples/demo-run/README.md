# Demo Run: Planner → Worker → Validator

Quick smoke test that produces artifacts without external dependencies.

## Run
```bash
python3 examples/demo-run/run_demo.py
```

## Artifacts produced
- `artifacts/tasks.json` — approved task list
- `artifacts/output.md` — worker draft (status-tagged)
- `artifacts/qa-report.json` — validator verdict

Use this as a template for your own flows or for CI smoke tests.
