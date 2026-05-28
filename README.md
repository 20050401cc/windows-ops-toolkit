# Windows Ops Toolkit

A compact toolkit of Windows-first scripts and templates for local project
diagnostics, cleanup, DOCX handoff work, and agent troubleshooting.

This repository also works as the index for a small public toolkit collection.
See [Tool Index](docs/tool-index.md) for the related standalone tools.

## Included Tools

- `scripts/memory-usage-report.ps1`: group running processes by memory usage.
- `scripts/safe-cache-cleanup.ps1`: dry-run-first cleanup for common cache folders.
- `src/windows_ops_toolkit/docx_report.py`: build a DOCX report from JSON.
- `src/windows_ops_toolkit/docx_integrity.py`: check DOCX zip/read integrity.
- `docs/claude-code-windows-repair-playbook.md`: generic local agent repair checklist.
- `docs/powershell-agent-snippets.md`: safe PowerShell snippets for local automation.
- `scripts/app-install-on-non-c-drive.md`: checklist for installing apps outside `C:`.

## Related Standalone Tools

- [antigravity-zh-patch](https://github.com/20050401cc/antigravity-zh-patch):
  Google Antigravity desktop Chinese UI patch.
- [windows-release-sanitizer](https://github.com/20050401cc/windows-release-sanitizer):
  create sanitized public release bundles from local Windows project folders.
- [teacher-release-packager](https://github.com/20050401cc/teacher-release-packager):
  create clean zip handoff packages for coursework, demos, and teacher submissions.
- [jupyter-preprocessing-template](https://github.com/20050401cc/jupyter-preprocessing-template):
  generate a flatten, normalize, and sigmoid teaching notebook.
- [project-selfcheck-template](https://github.com/20050401cc/project-selfcheck-template):
  run configurable file, compile, and smoke checks for project handoff folders.
- [image-prompt-archive-template](https://github.com/20050401cc/image-prompt-archive-template):
  archive image-generation prompts and export them to Markdown.

## Examples

Memory report:

```powershell
.\scripts\memory-usage-report.ps1 -Top 20 -ExcludeNames msedge,chrome,QQ
```

Cache cleanup dry run:

```powershell
.\scripts\safe-cache-cleanup.ps1
```

Actually clean supported cache folders:

```powershell
.\scripts\safe-cache-cleanup.ps1 -Execute
```

Generate a DOCX report:

```powershell
python .\src\windows_ops_toolkit\docx_report.py `
  --input .\examples\docx-report\report.json `
  --output .\examples\docx-report\report.docx
```

Check DOCX integrity:

```powershell
python .\src\windows_ops_toolkit\docx_integrity.py .\examples\docx-report\report.docx --json
```

## Test

```powershell
python -m pytest tests -q
```

## Safety Notes

- Cleanup defaults to dry run.
- Scripts avoid deleting documents, desktop files, downloads, projects, or user
  source folders.
- Do not commit real API keys, cookies, tokens, local credentials, or private
  project files.

## License

MIT
