#!/usr/bin/env python3
"""Create a sanitized release bundle from a local project folder.

The tool copies a project into a staging directory, excludes common private or
heavy files, scans text files for likely secrets or local-machine paths, and can
write a zip archive for public release.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = [
    ".git",
    ".hg",
    ".svn",
    ".env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.lnk",
    "*.bak",
    "*.bak.*",
    "__pycache__",
    "*.pyc",
    ".venv",
    ".venv*",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    ".cache",
    "logs",
    "*.log",
    "server_stderr_*.log",
    "server_stdout_*.log",
]

DEFAULT_SECRET_PATTERNS = {
    "windows_user_path": r"(?i)\b[A-Z]:\\Users\\[^\\\s]+",
    "unix_home_path": r"(?i)/home/[^/\s]+|/Users/[^/\s]+",
    "env_assignment": r"(?i)\b[A-Z0-9_]*(KEY|TOKEN|SECRET|PASSWORD|PASSWD|COOKIE)[A-Z0-9_]*\s*[:=]\s*['\"]?[^'\"\s]+",
    "private_key": r"-----BEGIN (?:RSA |OPENSSH |EC |DSA |)PRIVATE KEY-----",
    "url_with_token": r"https?://[^\s?#]+[^\s]*(?:token|key|secret|subscribe|sub=)[^\s]*",
    "github_token_like": r"\b(?:ghp|github_pat|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{20,}\b",
    "anthropic_key_like": r"\bsk-ant-[A-Za-z0-9_-]{20,}\b",
    "openai_key_like": r"\bsk-[A-Za-z0-9]{32,}\b",
}

TEXT_EXTENSIONS = {
    ".bat",
    ".cmd",
    ".css",
    ".csv",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".log",
    ".md",
    ".ps1",
    ".py",
    ".toml",
    ".ts",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


@dataclass
class Finding:
    file: str
    pattern: str
    line: int
    preview: str


@dataclass
class Manifest:
    source: str
    staging: str
    zip_path: str | None
    copied_files: int
    skipped_files: int
    findings: list[Finding]


def normalize_path(path: Path) -> str:
    return str(path).replace("\\", "/")


def matches_any(path: Path, root: Path, patterns: Iterable[str]) -> bool:
    rel = normalize_path(path.relative_to(root))
    name = path.name
    parts = path.parts
    for pattern in patterns:
        if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in parts):
            return True
    return False


def load_patterns(extra_patterns: Path | None) -> dict[str, str]:
    patterns = dict(DEFAULT_SECRET_PATTERNS)
    if extra_patterns:
        data = json.loads(extra_patterns.read_text(encoding="utf-8"))
        for name, regex in data.items():
            patterns[str(name)] = str(regex)
    return patterns


def is_probably_text(path: Path, max_probe: int = 4096) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        chunk = path.read_bytes()[:max_probe]
    except OSError:
        return False
    return b"\0" not in chunk


def copy_project(source: Path, staging: Path, excludes: list[str]) -> tuple[int, int]:
    copied = 0
    skipped = 0
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)

    for current_root, dirs, files in os.walk(source):
        root_path = Path(current_root)
        dirs[:] = [d for d in dirs if not matches_any(root_path / d, source, excludes)]
        for file_name in files:
            src = root_path / file_name
            if matches_any(src, source, excludes):
                skipped += 1
                continue
            dest = staging / src.relative_to(source)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            copied += 1
    return copied, skipped


def scan_tree(staging: Path, patterns: dict[str, str]) -> list[Finding]:
    compiled = {name: re.compile(regex) for name, regex in patterns.items()}
    findings: list[Finding] = []
    for path in staging.rglob("*"):
        if not path.is_file() or not is_probably_text(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = normalize_path(path.relative_to(staging))
        for line_no, line in enumerate(text.splitlines(), start=1):
            for name, regex in compiled.items():
                match = regex.search(line)
                if not match:
                    continue
                preview = line.strip()
                if len(preview) > 160:
                    preview = preview[:157] + "..."
                findings.append(Finding(rel, name, line_no, preview))
    return findings


def write_zip(staging: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in staging.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(staging))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a sanitized public release bundle.")
    parser.add_argument("--source", required=True, type=Path, help="Project folder to copy from.")
    parser.add_argument("--staging", required=True, type=Path, help="Clean staging output folder.")
    parser.add_argument("--zip", dest="zip_path", type=Path, help="Optional zip file to create.")
    parser.add_argument("--manifest", type=Path, help="Optional JSON manifest path.")
    parser.add_argument("--extra-exclude", action="append", default=[], help="Additional glob exclude pattern.")
    parser.add_argument("--patterns", type=Path, help="JSON file containing additional scan regexes.")
    parser.add_argument("--fail-on-findings", action="store_true", help="Exit 1 if findings are detected.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    staging = args.staging.resolve()
    if not source.exists() or not source.is_dir():
        print(f"source does not exist or is not a directory: {source}", file=sys.stderr)
        return 2

    excludes = DEFAULT_EXCLUDES + list(args.extra_exclude)
    copied, skipped = copy_project(source, staging, excludes)
    findings = scan_tree(staging, load_patterns(args.patterns))

    zip_path = args.zip_path.resolve() if args.zip_path else None
    if zip_path:
        write_zip(staging, zip_path)

    manifest = Manifest(
        source=str(source),
        staging=str(staging),
        zip_path=str(zip_path) if zip_path else None,
        copied_files=copied,
        skipped_files=skipped,
        findings=findings,
    )
    payload = json.dumps(asdict(manifest), ensure_ascii=False, indent=2)
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(payload + "\n", encoding="utf-8")
    print(payload)

    if findings and args.fail_on_findings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
