SHELL := bash

.PHONY: test-template-render test-template-render-github test-template-render-gitlab

test-template-render: test-template-render-github test-template-render-gitlab

# Validate GitHub-scaffolded output and task-runner pruning.
test-template-render-github:
	@set -euo pipefail; \
	out_dir="$$(mktemp -d /tmp/scaf-template-github-XXXXXX)"; \
	copier copy . "$$out_dir" --trust --defaults \
	  -d copier__project_name_raw="Sample GitHub Template" \
	  -d copier__project_slug="sample_github_template" \
	  -d copier__description="Sample github generated project" \
	  -d copier__author_name="Sample Author" \
	  -d copier__email="sample@example.com" \
	  -d copier__version="0.1.0" \
	  -d copier__ci_provider="github" \
	  -d copier__enable_semantic_release=false \
	  -d copier__github_semantic_release_auth="github_token" \
	  -d copier__enable_secret_scanning=true \
	  -d copier__task_runner="task"; \
	test -f "$$out_dir/README.md"; \
	test -f "$$out_dir/.copier-answers.yml"; \
	test -f "$$out_dir/Taskfile.yml"; \
	test ! -f "$$out_dir/Makefile"; \
	test ! -f "$$out_dir/justfile"; \
	test -f "$$out_dir/.github/workflows/template-correctness.yaml"; \
	test -f "$$out_dir/.github/workflows/secret-scan.yaml"; \
	test ! -f "$$out_dir/.github/workflows/semantic-release.yaml"; \
	test ! -f "$$out_dir/.gitlab-ci.yml"; \
	rm -rf "$$out_dir"

# Validate GitLab-scaffolded output and task-runner pruning.
test-template-render-gitlab:
	@set -euo pipefail; \
	out_dir="$$(mktemp -d /tmp/scaf-template-gitlab-XXXXXX)"; \
	copier copy . "$$out_dir" --trust --defaults \
	  -d copier__project_name_raw="Sample GitLab Template" \
	  -d copier__project_slug="sample_gitlab_template" \
	  -d copier__description="Sample gitlab generated project" \
	  -d copier__author_name="Sample Author" \
	  -d copier__email="sample@example.com" \
	  -d copier__version="0.1.0" \
	  -d copier__ci_provider="gitlab" \
	  -d copier__enable_semantic_release=false \
	  -d copier__enable_secret_scanning=true \
	  -d copier__task_runner="just"; \
	test -f "$$out_dir/README.md"; \
	test -f "$$out_dir/.copier-answers.yml"; \
	test -f "$$out_dir/justfile"; \
	test ! -f "$$out_dir/Makefile"; \
	test ! -f "$$out_dir/Taskfile.yml"; \
	test -f "$$out_dir/.gitlab-ci.yml"; \
	test ! -d "$$out_dir/.github"; \
	rm -rf "$$out_dir"
