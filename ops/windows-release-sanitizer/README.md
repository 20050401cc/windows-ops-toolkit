# Windows Release Sanitizer

Create a clean public release bundle from a local Windows project folder.

The tool copies a source folder into a staging directory, excludes common private
or heavy files, scans text files for likely secrets or local-machine paths, and
optionally writes a ZIP archive.

## Why

Before publishing a local project to GitHub, it is easy to accidentally include:

- `.env` files, keys, cookies, and credential snippets
- Windows shortcuts and backup files
- local paths such as `C:\Users\...`
- logs, virtual environments, `node_modules`, caches, and build junk
- private subscription URLs or one-off machine files

This script gives you a repeatable preflight step before making a repository
public.

## Quick Start

```powershell
python .\src\release_sanitizer.py `
  --source "D:\Projects\my-app" `
  --staging "D:\Releases\my-app-public" `
  --zip "D:\Releases\my-app-public.zip" `
  --manifest "D:\Releases\manifest.json" `
  --fail-on-findings
```

If findings are detected, inspect the manifest, remove or rewrite the sensitive
content, then run the command again.

## Example

```powershell
python .\src\release_sanitizer.py `
  --source .\examples\sample-project `
  --staging .\examples\sample-project-public `
  --zip .\examples\sample-project-public.zip `
  --manifest .\examples\manifest.json
```

## Default Excludes

The default exclude list includes:

- VCS folders: `.git`, `.hg`, `.svn`
- secrets: `.env`, `.env.*`, `*.pem`, `*.key`, `*.p12`, `*.pfx`
- Windows/user artifacts: `*.lnk`, `*.bak`, `*.bak.*`
- generated or heavy folders: `.venv`, `venv`, `node_modules`, `dist`, `build`, `.cache`
- logs and caches: `logs`, `*.log`, `__pycache__`, `*.pyc`

You can add more:

```powershell
python .\src\release_sanitizer.py `
  --source "D:\Projects\my-app" `
  --staging "D:\Releases\my-app-public" `
  --extra-exclude "*.docx" `
  --extra-exclude "private-notes"
```

## Extra Scan Patterns

Add a JSON file with custom regular expressions:

```json
{
  "student_id": "\\b20\\d{8}\\b",
  "internal_domain": "internal\\.example\\.com"
}
```

Then run:

```powershell
python .\src\release_sanitizer.py `
  --source "D:\Projects\my-app" `
  --staging "D:\Releases\my-app-public" `
  --patterns ".\patterns.json" `
  --fail-on-findings
```

## Notes

This tool is a safety net, not a guarantee. Always review the generated staging
directory before publishing.
