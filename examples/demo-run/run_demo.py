"""Minimal Planner→Worker→Validator demo.

Writes sample artifacts to examples/demo-run/artifacts/ without external deps.
This is a teaching smoke-test, not production logic.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
ART = ROOT / "artifacts"


def main():
    ART.mkdir(exist_ok=True)

    tasks = {
        "status": "APPROVED",
        "tasks": [
            {
                "id": 1,
                "owner": "Planner",
                "summary": "Draft short product overview",
                "depends_on": [],
                "artifact": "artifacts/output.md",
            },
            {
                "id": 2,
                "owner": "Validator",
                "summary": "QA check overview for clarity and tone",
                "depends_on": [1],
                "artifact": "artifacts/qa-report.json",
            },
        ],
    }
    (ART / "tasks.json").write_text(json.dumps(tasks, indent=2), encoding="utf-8")

    output_md = """[APPROVED]\n# Product Overview\n\nA concise two-paragraph overview of the product with a clear value prop.\n"""
    (ART / "output.md").write_text(output_md, encoding="utf-8")

    qa_report = {
        "status": "PASS",
        "issues": [],
        "checked_artifact": "artifacts/output.md",
        "notes": "Meets clarity and tone requirements."
    }
    (ART / "qa-report.json").write_text(json.dumps(qa_report, indent=2), encoding="utf-8")

    print(f"Demo artifacts written to {ART}")


if __name__ == "__main__":
    main()
