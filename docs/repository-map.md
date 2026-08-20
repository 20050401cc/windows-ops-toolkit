# Repository Map

This repository is the single entry point for reusable utilities. Product repositories remain independent; small workflow tools are grouped here by purpose.

## Toolkit layout

- `ops/`: Windows diagnostics, release sanitizing, project self-checks, and teacher handoff packaging.
- `templates/`: reusable prompt-archive and Jupyter teaching templates.
- `experiments/`: small AI/automation experiments that are useful but not yet products.
- `scripts/`, `src/`, `tests/`: the original Windows Ops Toolkit code and tests.

## Consolidated tools

| Path | Former repository | Role |
| --- | --- | --- |
| `ops/teacher-release-packager/` | teacher-release-packager | Clean coursework/demo handoff packages |
| `ops/windows-release-sanitizer/` | windows-release-sanitizer | Remove private/heavy files and scan release folders |
| `ops/project-selfcheck/` | project-selfcheck-template | Required-file, compile, and smoke checks |
| `templates/image-prompt-archive/` | image-prompt-archive-template | JSONL prompt archive and Markdown export |
| `templates/jupyter-preprocessing/` | jupyter-preprocessing-template | Generate teaching notebooks |
| `experiments/computer-use-lite/` | computer-use-lite | Screenshot-driven computer-use proof of concept |

The original repositories are retained as migration references for now. After this branch is reviewed, their READMEs can be changed to point here before any archival or deletion decision.
