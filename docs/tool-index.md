# Tool Index

This page groups the public tools by workflow. Each tool is kept in its own
repository so it can stay small, focused, and easy to reuse.

## Windows Operations

| Tool | Purpose |
| --- | --- |
| [windows-ops-toolkit](https://github.com/20050401cc/windows-ops-toolkit) | Windows diagnostics, cache cleanup, DOCX helpers, local agent repair notes, and PowerShell snippets. |
| [windows-release-sanitizer](https://github.com/20050401cc/windows-release-sanitizer) | Build sanitized public release folders and zip archives from local Windows projects. |

## Project Handoff

| Tool | Purpose |
| --- | --- |
| [teacher-release-packager](https://github.com/20050401cc/teacher-release-packager) | Create clean handoff zip packages for coursework, demos, or teacher submissions. |
| [project-selfcheck-template](https://github.com/20050401cc/project-selfcheck-template) | Run required-file, Python compile, and smoke-test checks before delivery. |

## Documents and Teaching

| Tool | Purpose |
| --- | --- |
| [jupyter-preprocessing-template](https://github.com/20050401cc/jupyter-preprocessing-template) | Generate a runnable flatten, normalize, and sigmoid Jupyter notebook. |
| [windows-ops-toolkit DOCX helpers](https://github.com/20050401cc/windows-ops-toolkit/tree/main/src/windows_ops_toolkit) | Generate simple DOCX reports and check DOCX integrity. |

## AI Workflow Utilities

| Tool | Purpose |
| --- | --- |
| [image-prompt-archive-template](https://github.com/20050401cc/image-prompt-archive-template) | Save image-generation prompts, output paths, tags, and notes as JSONL, then export Markdown. |
| [antigravity-zh-patch](https://github.com/20050401cc/antigravity-zh-patch) | Apply a lightweight Chinese UI patch for Google Antigravity desktop. |

## Recommended Order

1. Use `windows-release-sanitizer` before publishing a local folder.
2. Use `project-selfcheck-template` before handing off a project.
3. Use `teacher-release-packager` when the output should be a clean zip.
4. Use `windows-ops-toolkit` for Windows diagnostics and DOCX support.
5. Use `image-prompt-archive-template` to preserve prompt history.
6. Use `jupyter-preprocessing-template` for teaching notebooks.
