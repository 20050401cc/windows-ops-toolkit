"""Append image-generation prompt records to a portable JSONL archive."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def append_record(
    archive: Path,
    prompt: str,
    image: str | None = None,
    tool: str | None = None,
    tags: list[str] | None = None,
    notes: str | None = None,
) -> dict:
    record = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "image": image,
        "tool": tool,
        "tags": tags or [],
        "notes": notes,
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    with archive.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def read_records(archive: Path) -> list[dict]:
    if not archive.exists():
        return []
    records = []
    for line in archive.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def export_markdown(archive: Path, output: Path) -> int:
    records = read_records(archive)
    lines = ["# Image Prompt Archive", ""]
    for index, record in enumerate(records, start=1):
        lines.append(f"## {index}. {record.get('created_at', '')}")
        if record.get("image"):
            lines.append(f"- Image: `{record['image']}`")
        if record.get("tool"):
            lines.append(f"- Tool: `{record['tool']}`")
        if record.get("tags"):
            lines.append("- Tags: " + ", ".join(f"`{tag}`" for tag in record["tags"]))
        lines.append("")
        lines.append("```text")
        lines.append(record.get("prompt", ""))
        lines.append("```")
        if record.get("notes"):
            lines.append("")
            lines.append(record["notes"])
        lines.append("")
    output.write_text("\n".join(lines), encoding="utf-8")
    return len(records)


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive image prompts as JSONL.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="Append one prompt record.")
    add.add_argument("--archive", type=Path, default=Path("prompts.jsonl"))
    add.add_argument("--prompt", required=True)
    add.add_argument("--image")
    add.add_argument("--tool")
    add.add_argument("--tags", nargs="*", default=[])
    add.add_argument("--notes")

    export = subparsers.add_parser("export-md", help="Export archive to Markdown.")
    export.add_argument("--archive", type=Path, default=Path("prompts.jsonl"))
    export.add_argument("--output", type=Path, default=Path("prompts.md"))

    args = parser.parse_args()
    if args.command == "add":
        record = append_record(args.archive, args.prompt, args.image, args.tool, args.tags, args.notes)
        print(json.dumps(record, indent=2, ensure_ascii=False))
        return 0

    count = export_markdown(args.archive, args.output)
    print(f"exported {count} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
