"""Build a clean, shareable delivery bundle for coursework or demos."""

from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import sys
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


DEFAULT_EXCLUDES = [
    ".git",
    ".git/**",
    ".env",
    ".env.*",
    "__pycache__",
    "__pycache__/**",
    ".pytest_cache",
    ".pytest_cache/**",
    ".mypy_cache",
    ".mypy_cache/**",
    ".ruff_cache",
    ".ruff_cache/**",
    ".venv",
    ".venv/**",
    "venv",
    "venv/**",
    "node_modules",
    "node_modules/**",
    "*.pyc",
    "*.pyo",
    "*.log",
    "*.tmp",
    "*.bak",
    "~$*",
    "Thumbs.db",
    ".DS_Store",
]


@dataclass(frozen=True)
class BundleConfig:
    required: list[str]
    include: list[str]
    exclude: list[str]
    readme: str | None


def load_config(path: Path | None) -> BundleConfig:
    if path is None:
        return BundleConfig(required=[], include=["**"], exclude=[], readme=None)

    data = json.loads(path.read_text(encoding="utf-8"))
    return BundleConfig(
        required=list(data.get("required", [])),
        include=list(data.get("include", ["**"])),
        exclude=list(data.get("exclude", [])),
        readme=data.get("readme"),
    )


def to_posix(path: Path) -> str:
    return PurePosixPath(*path.parts).as_posix()


def matches_any(relative_posix: str, patterns: list[str]) -> bool:
    return any(
        fnmatch.fnmatch(relative_posix, pattern)
        or fnmatch.fnmatch(PurePosixPath(relative_posix).name, pattern)
        for pattern in patterns
    )


def should_copy(relative_posix: str, config: BundleConfig) -> bool:
    excludes = DEFAULT_EXCLUDES + config.exclude
    if matches_any(relative_posix, excludes):
        return False
    return matches_any(relative_posix, config.include)


def verify_required(source: Path, config: BundleConfig) -> list[str]:
    missing: list[str] = []
    for item in config.required:
        if not (source / item).exists():
            missing.append(item)
    return missing


def copy_bundle(source: Path, staging: Path, config: BundleConfig) -> dict:
    copied: list[str] = []
    skipped: list[str] = []

    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)

    for path in sorted(source.rglob("*")):
        if path == staging or staging in path.parents:
            continue
        relative = path.relative_to(source)
        relative_posix = to_posix(relative)

        if path.is_dir():
            continue

        if not should_copy(relative_posix, config):
            skipped.append(relative_posix)
            continue

        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied.append(relative_posix)

    return {"copied": copied, "skipped": skipped}


def write_readme(staging: Path, config: BundleConfig) -> None:
    if not config.readme:
        return
    readme = staging / "README.md"
    if readme.exists():
        return
    readme.write_text(config.readme.strip() + "\n", encoding="utf-8")


def write_manifest(staging: Path, report: dict) -> Path:
    manifest = staging / "release-manifest.json"
    manifest.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return manifest


def create_zip(staging: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(staging.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(staging).as_posix())


def build_bundle(
    source: Path,
    staging: Path,
    zip_path: Path | None,
    config_path: Path | None,
) -> dict:
    source = source.resolve()
    staging = staging.resolve()
    config = load_config(config_path)

    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"Source folder does not exist: {source}")
    if source == staging or source in staging.parents:
        raise ValueError("Staging folder must be outside the source folder.")

    missing = verify_required(source, config)
    if missing:
        raise FileNotFoundError("Missing required files: " + ", ".join(missing))

    result = copy_bundle(source, staging, config)
    write_readme(staging, config)

    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": str(source),
        "staging": str(staging),
        "zip": str(zip_path.resolve()) if zip_path else None,
        "copied_count": len(result["copied"]),
        "skipped_count": len(result["skipped"]),
        "copied": result["copied"],
        "skipped": result["skipped"],
    }
    write_manifest(staging, report)

    if zip_path:
        create_zip(staging, zip_path.resolve())
    return report


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a clean zip package for coursework, demos, or handoff."
    )
    parser.add_argument("--source", required=True, type=Path, help="Project folder to package.")
    parser.add_argument("--staging", required=True, type=Path, help="Clean output folder.")
    parser.add_argument("--zip", dest="zip_path", type=Path, help="Optional zip output path.")
    parser.add_argument("--config", type=Path, help="Optional JSON packaging config.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        report = build_bundle(args.source, args.staging, args.zip_path, args.config)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
