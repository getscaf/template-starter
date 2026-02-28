<p align="center">
  <img src="scaf-logo.png" width="250px">
</p>

**template-starter** is a generic Scaf base for creating new Scaf templates.

## What This Starter Provides

This starter provides a clean, reusable foundation for building new Scaf templates.
It standardizes template authoring concerns such as Copier inputs, CI scaffolding,
release automation options, secret scanning, and local developer workflows.

## Features

- Copier prompts with input validation and conditional logic
- CI scaffolding for GitHub or GitLab
- Optional semantic-release setup and config
- Optional secret scanning in CI
- Template correctness CI (Copier render checks)
- Choice of local task runner (`make`, `task`, or `just`) with `init`/`check`
- Generated project docs for usage and upgrade flow
- Apache-2.0 license by default (license selection via Copier option planned)

## Copier Options

- `copier__ci_provider`: `github` or `gitlab`
- `copier__enable_semantic_release`: include release automation
- `copier__github_semantic_release_auth`: `github_token` or `github_app` (GitHub + semantic-release only)
- `copier__enable_secret_scanning`: include gitleaks CI
- `copier__task_runner`: `make`, `task`, or `just`
- `copier__repo_url`: optional remote URL to configure as `origin` during generation

## Quick Start

```bash
# Local path
scaf my-template ./template-starter

# Git URL
scaf my-template https://github.com/getscaf/template-starter.git
```

## Testing This Starter Template

Run local render tests:

```bash
make test-template-render
```

CI runs the same command in `.github/workflows/template-render-tests.yaml`.

## Generated Project Docs

Each generated project includes:

- `docs/using-template.md`
- `docs/upgrading.md`
- `docs/semantic-release-github.md` (when GitHub + semantic-release is enabled)

These cover day-to-day usage and copier update workflow for downstream projects.

## License

Apache-2.0. See [LICENSE](LICENSE).
