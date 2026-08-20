from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_archive import append_record, export_markdown, read_records


def test_append_and_export(tmp_path):
    archive = tmp_path / "prompts.jsonl"
    append_record(
        archive,
        prompt="A clean product photo on a neutral background",
        image="exports/image-001.png",
        tool="example-generator",
        tags=["product", "clean"],
        notes="Keep lighting consistent.",
    )

    records = read_records(archive)
    assert len(records) == 1
    assert records[0]["prompt"].startswith("A clean product")

    output = tmp_path / "prompts.md"
    count = export_markdown(archive, output)
    assert count == 1
    assert "Image Prompt Archive" in output.read_text(encoding="utf-8")
