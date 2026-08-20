from pathlib import Path
import json
import zipfile

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from teacher_release_packager import build_bundle


def test_build_bundle_excludes_noise_and_writes_manifest(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "README.md").write_text("Demo\n", encoding="utf-8")
    (source / "run.bat").write_text("@echo off\n", encoding="utf-8")
    (source / "src").mkdir()
    (source / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
    (source / ".env").write_text("API_KEY=example\n", encoding="utf-8")
    (source / "debug.log").write_text("debug\n", encoding="utf-8")

    config = tmp_path / "config.json"
    config.write_text(
        json.dumps(
            {
                "required": ["README.md", "run.bat", "src/main.py"],
                "include": ["README.md", "run.bat", "src/**"],
            }
        ),
        encoding="utf-8",
    )

    staging = tmp_path / "public"
    zip_path = tmp_path / "public.zip"
    report = build_bundle(source, staging, zip_path, config)

    assert report["copied_count"] == 3
    assert (staging / "README.md").exists()
    assert (staging / "run.bat").exists()
    assert (staging / "src" / "main.py").exists()
    assert not (staging / ".env").exists()
    assert not (staging / "debug.log").exists()
    assert (staging / "release-manifest.json").exists()

    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())
    assert "README.md" in names
    assert "src/main.py" in names
    assert ".env" not in names


def test_missing_required_file_fails(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    config = tmp_path / "config.json"
    config.write_text(json.dumps({"required": ["README.md"]}), encoding="utf-8")

    try:
        build_bundle(source, tmp_path / "public", None, config)
    except FileNotFoundError as exc:
        assert "README.md" in str(exc)
    else:
        raise AssertionError("missing required file should fail")
