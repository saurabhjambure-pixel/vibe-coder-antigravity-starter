import json
from pathlib import Path
import runpy

ROOT = Path(__file__).parent.parent
DEMO = ROOT / "examples" / "demo-run"
ART = DEMO / "artifacts"


def test_demo_run_creates_artifacts(tmp_path):
    # run the demo in-place
    runpy.run_path(str(DEMO / "run_demo.py"))

    for fname in ("tasks.json", "output.md", "qa-report.json"):
        path = ART / fname
        assert path.exists(), f"missing artifact {fname}"

    data = json.loads((ART / "tasks.json").read_text())
    assert data.get("status") == "APPROVED"
    assert len(data.get("tasks", [])) >= 2

    qa = json.loads((ART / "qa-report.json").read_text())
    assert qa.get("status") == "PASS"
