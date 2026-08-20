# Teacher Release Packager

A small Python CLI for turning a working project folder into a clean handoff
package for teachers, reviewers, or demo users.

It copies only the files that should be delivered, excludes common development
artifacts, verifies required files, writes a manifest, and optionally creates a
zip archive.

## Why this exists

Coursework and demo projects often contain files that should not be sent:

- virtual environments
- caches
- logs
- `.env` files
- local backups
- temporary files
- editor or OS metadata

This tool gives you a repeatable packaging step instead of manually deleting
files before every submission.

## Quick Start

```powershell
python .\src\teacher_release_packager.py `
  --source .\examples\lesson-project `
  --staging .\dist\lesson-project-public `
  --zip .\dist\lesson-project-public.zip `
  --config .\examples\packager.config.json
```

The output folder includes a `release-manifest.json` file with copied and
skipped paths.

## Config

Create a JSON file like this:

```json
{
  "required": ["README.md", "run.bat", "src/main.py"],
  "include": ["README.md", "run.bat", "src/**", "docs/**"],
  "exclude": ["docs/private-notes.md"],
  "readme": "Run run.bat to start the demo."
}
```

Fields:

- `required`: files or folders that must exist before packaging.
- `include`: glob patterns to copy. Defaults to `["**"]`.
- `exclude`: extra glob patterns to remove from the package.
- `readme`: optional fallback README text if the staged package has no README.

## Default Excludes

The tool excludes common unsafe or noisy files by default:

- `.env`, `.env.*`
- `.git`
- virtual environments
- `node_modules`
- Python caches
- test/tool caches
- `*.log`, `*.tmp`, `*.bak`
- Office lock files
- OS metadata files

## Test

```powershell
python -m pytest tests -q
```

## License

MIT
