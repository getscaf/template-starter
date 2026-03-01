<p align="center">
  <img src="scaf-logo.png" width="250px">
</p>

**template-starter** is a generic Scaf base for creating new Scaf templates.

## What This Starter Provides

Use this starter to generate new Scaf templates with validated Copier prompts,
GitHub/GitLab CI templates, optional semantic-release wiring (GitHub token or
GitHub App), optional gitleaks scanning, and generated `make`/`task`/`just`
`init`/`check` commands.

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

- `copier__ci_provider`: `github` or `gitlab` (only asked when repo setup is disabled; otherwise inferred from `copier__repo_provider`)
- `copier__enable_semantic_release`: include release automation
- `copier__github_semantic_release_auth`: `github_token` or `github_app` (GitHub + semantic-release only)
- `copier__enable_secret_scanning`: include gitleaks CI
- `copier__task_runner`: `make`, `task`, or `just`
- `copier__configure_repo`: enable repository remote setup
- `copier__repo_provider`: `github` or `gitlab`
- `copier__repo_org`: organization/group name
- `copier__repo_name`: repository name
- `copier__create_repo`: create provider repo automatically when missing (`gh` for GitHub, `glab` for GitLab)
- `copier__repo_visibility`: `private` or `public` for automatic repo creation

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
