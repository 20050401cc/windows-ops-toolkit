"""Small configurable self-check runner for project handoff folders."""

from __future__ import annotations

import argparse
import json
import py_compile
import subprocess
import sys
from pathlib import Path


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_required_files(root: Path, required: list[str]) -> list[dict]:
    results = []
    for item in required:
        target = root / item
        results.append({"type": "required_file", "path": item, "ok": target.exists()})
    return results


def check_python_compile(root: Path, patterns: list[str]) -> list[dict]:
    results = []
    for pattern in patterns:
        for file in sorted(root.glob(pattern)):
            if not file.is_file() or file.suffix != ".py":
                continue
            rel = file.relative_to(root).as_posix()
            try:
                py_compile.compile(str(file), doraise=True)
                results.append({"type": "python_compile", "path": rel, "ok": True})
            except py_compile.PyCompileError as exc:
                results.append(
                    {
                        "type": "python_compile",
                        "path": rel,
                        "ok": False,
                        "error": str(exc),
                    }
                )
    return results


def check_commands(root: Path, commands: list[dict]) -> list[dict]:
    results = []
    for command in commands:
        name = command.get("name") or command.get("run")
        run = command["run"]
        timeout = int(command.get("timeout", 30))
        completed = subprocess.run(
            run,
            cwd=root,
            shell=True,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
        results.append(
            {
                "type": "command",
                "name": name,
                "run": run,
                "ok": completed.returncode == 0,
                "returncode": completed.returncode,
                "stdout": completed.stdout[-2000:],
                "stderr": completed.stderr[-2000:],
            }
        )
    return results


def run_checks(root: Path, config: dict) -> dict:
    root = root.resolve()
    checks = []
    checks.extend(check_required_files(root, list(config.get("required_files", []))))
    checks.extend(check_python_compile(root, list(config.get("python_compile", []))))
    checks.extend(check_commands(root, list(config.get("commands", []))))
    return {"root": str(root), "ok": all(item["ok"] for item in checks), "checks": checks}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run project handoff self-checks.")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root.")
    parser.add_argument("--config", type=Path, required=True, help="Self-check config JSON.")
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args(argv)

    report = run_checks(args.root, load_config(args.config))
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
