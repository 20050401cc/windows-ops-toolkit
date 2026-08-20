# Project Selfcheck Template

A tiny configurable self-check runner for project handoff folders.

It can verify:

- required files exist
- Python files compile
- smoke-test commands exit successfully
- a JSON report is generated for reviewers or future debugging

## Usage

```powershell
python .\src\project_selfcheck.py `
  --root .\examples\sample-project `
  --config .\examples\sample-project\selfcheck.config.json `
  --output .\selfcheck-report.json
```

The command exits with code `0` when all checks pass and `1` when any check
fails.

## Config

```json
{
  "required_files": ["README.md", "src/app.py"],
  "python_compile": ["src/**/*.py"],
  "commands": [
    {
      "name": "sample app starts",
      "run": "python src/app.py",
      "timeout": 10
    }
  ]
}
```

## Test

```powershell
python -m pytest tests -q
```

## License

MIT
