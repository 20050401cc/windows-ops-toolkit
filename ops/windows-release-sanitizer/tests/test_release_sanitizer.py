import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "release_sanitizer.py"


def test_sample_project_sanitizes(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("# demo\n", encoding="utf-8")
    (source / "app.py").write_text("print('ok')\n", encoding="utf-8")
    (source / ".env").write_text("API_KEY=secret\n", encoding="utf-8")
    (source / "debug.log").write_text("local log\n", encoding="utf-8")

    staging = tmp_path / "staging"
    manifest = tmp_path / "manifest.json"
    zip_path = tmp_path / "bundle.zip"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source",
            str(source),
            "--staging",
            str(staging),
            "--zip",
            str(zip_path),
            "--manifest",
            str(manifest),
            "--fail-on-findings",
        ],
        text=True,
        capture_output=True,
        check=True,
    )

    payload = json.loads(result.stdout)
    assert payload["copied_files"] == 2
    assert payload["skipped_files"] == 2
    assert payload["findings"] == []
    assert (staging / "README.md").exists()
    assert not (staging / ".env").exists()
    assert zip_path.exists()


def test_findings_fail_when_sensitive_path_is_copied(tmp_path: Path) -> None:
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("local path: C:\\Users\\Alice\\secret\n", encoding="utf-8")
    staging = tmp_path / "staging"

    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--source",
            str(source),
            "--staging",
            str(staging),
            "--fail-on-findings",
        ],
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["findings"][0]["pattern"] == "windows_user_path"
