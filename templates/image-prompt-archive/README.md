# Image Prompt Archive Template

A tiny JSONL-based workflow for saving image-generation prompts, output image
paths, tags, tool names, and notes.

It is useful when you generate many images and want reusable prompt history
without depending on a specific media manager.

## Usage

Add a record:

```powershell
python .\src\prompt_archive.py add `
  --archive .\prompts.jsonl `
  --prompt "A clean product photo on a neutral background" `
  --image "exports/image-001.png" `
  --tool "example-generator" `
  --tags product clean `
  --notes "Keep lighting consistent."
```

Export Markdown:

```powershell
python .\src\prompt_archive.py export-md --archive .\prompts.jsonl --output .\prompts.md
```

## Test

```powershell
python -m pytest tests -q
```

## License

MIT
