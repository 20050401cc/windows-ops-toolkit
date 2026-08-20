# Windows Ops Toolkit

A single entry point for small, reusable Windows, project-handoff, teaching, and AI-workflow utilities.

The rule is simple: finished products stay in their own repositories; small reusable tools live here.

## Structure

- `scripts/` and `src/windows_ops_toolkit/`: the original Windows diagnostics, cleanup, and DOCX helpers.
- `ops/`: release sanitizing, project self-checks, and teacher handoff packaging.
- `templates/`: image-prompt archiving and Jupyter teaching templates.
- `experiments/`: useful automation experiments that are not products yet.
- `docs/repository-map.md`: the complete consolidation map.

## Core Windows Tools

- `scripts/memory-usage-report.ps1`: group running processes by memory usage.
- `scripts/safe-cache-cleanup.ps1`: dry-run-first cleanup for common cache folders.
- `src/windows_ops_toolkit/docx_report.py`: build a DOCX report from JSON.
- `src/windows_ops_toolkit/docx_integrity.py`: check DOCX zip/read integrity.
- `docs/claude-code-windows-repair-playbook.md`: local agent repair checklist.
- `docs/powershell-agent-snippets.md`: safe PowerShell snippets for local automation.

## Consolidated Utilities

| Path | Purpose |
| --- | --- |
| `ops/windows-release-sanitizer/` | Build sanitized public release folders and zip archives. |
| `ops/project-selfcheck/` | Run required-file, Python compile, and smoke checks. |
| `ops/project-selfcheck/` | Validate a project before delivery. |
| `tools/teacher-release-packager/` | Create clean coursework and demo handoff packages. |
| `templates/image-prompt-archive/` | Save prompts as JSONL and export Markdown. |
| `templates/jupyter-preprocessing/` | Generate a runnable teaching notebook. |
| `experiments/computer-use-lite/` | Screenshot-driven computer-use proof of concept. |

## Examples

Memory report:

```powershell
.\scripts\memory-usage-report.ps1 -Top 20 -ExcludeNames msedge,chrome,QQ
```

Cache cleanup dry run:

```powershell
.\scripts\safe-cache-cleanup.ps1
```

Generate a DOCX report:

```powershell
python .\src\windows_ops_toolkit\docx_report.py \
  --input .\examples\docx-report\report.json \
  --output .\examples\docx-report\report.docx
```

## Safety

- Cleanup defaults to dry run.
- Do not commit API keys, cookies, tokens, local credentials, or private project files.
- The original standalone repositories remain as migration references until their archive/delete decisions are made separately.

## License

MIT
