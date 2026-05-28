# Windows Ops Toolkit

A compact toolkit of Windows-first scripts and templates for local project
diagnostics, cleanup, DOCX handoff work, and agent troubleshooting.

## Included Tools

- `scripts/memory-usage-report.ps1`: group running processes by memory usage.
- `scripts/safe-cache-cleanup.ps1`: dry-run-first cleanup for common cache folders.
- `src/windows_ops_toolkit/docx_report.py`: build a DOCX report from JSON.
- `src/windows_ops_toolkit/docx_integrity.py`: check DOCX zip/read integrity.
- `docs/claude-code-windows-repair-playbook.md`: generic local agent repair checklist.
- `docs/powershell-agent-snippets.md`: safe PowerShell snippets for local automation.
- `scripts/app-install-on-non-c-drive.md`: checklist for installing apps outside `C:`.

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
