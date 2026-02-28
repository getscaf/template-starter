<p align="center">
  <img src="scaf-logo.png" width="250px">
</p>

**template-starter** is a generic scaf base for creating new scaf templates.

It intentionally excludes cloud, Kubernetes, and deployment-specific implementation so you can compose specialized templates on top.

## What This Base Template Focuses On

- Copier questions and validation patterns
- CI scaffolding for GitHub or GitLab
- Optional semantic-release setup and config
- Optional secret scanning in CI
- Template correctness CI (renders template in CI)
- Choice of local task runner (`make`, `task`, or `just`) with `init`/`check`
- Project docs for template usage and upgrade path

## Quick Start

```bash
# Local path
scaf my-template ./template-starter

# Git URL
scaf my-template https://github.com/getscaf/template-starter.git
```

Then run local init in the generated project using the selected runner.

## Generated Project Docs

Each generated project includes:

- `docs/using-template.md`
- `docs/upgrading.md`

These cover day-to-day usage and copier update workflow for downstream projects.
