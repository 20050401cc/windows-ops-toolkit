from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from project_selfcheck import run_checks


def test_run_checks_passes_for_valid_project(tmp_path):
    root = tmp_path / "project"
    (root / "src").mkdir(parents=True)
    (root / "README.md").write_text("demo", encoding="utf-8")
    (root / "src" / "app.py").write_text("print('ok')", encoding="utf-8")

    report = run_checks(
        root,
        {
            "required_files": ["README.md", "src/app.py"],
            "python_compile": ["src/**/*.py"],
            "commands": [{"name": "run", "run": "python src/app.py"}],
        },
    )

    assert report["ok"] is True
    assert len(report["checks"]) == 4


def test_run_checks_fails_for_missing_file(tmp_path):
    root = tmp_path / "project"
    root.mkdir()
    report = run_checks(root, {"required_files": ["README.md"]})

    assert report["ok"] is False
    assert report["checks"][0]["path"] == "README.md"
