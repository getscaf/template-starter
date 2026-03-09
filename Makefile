SHELL := bash

.PHONY: test-template-render test-template-render-github test-template-render-gitlab

test-template-render: test-template-render-github test-template-render-gitlab

# Validate generated template repository structure.
test-template-render-github:
	@set -euo pipefail; \
	out_dir="$$(mktemp -d /tmp/scaf-template-github-XXXXXX)"; \
	copier copy . "$$out_dir" --vcs-ref=HEAD --trust --defaults \
	  -d copier__project_name_raw="Sample GitHub Template" \
	  -d copier__project_slug="sample_github_template" \
	  -d copier__description="Sample github generated project" \
	  -d copier__author_name="Sample Author" \
	  -d copier__email="sample@example.com" \
	  -d copier__version="0.1.0" \
	  -d copier__ci_provider="github" \
	  -d copier__enable_semantic_release=false \
	  -d copier__github_semantic_release_auth="github_token" \
	  -d copier__create_repo=false \
	  -d copier__enable_secret_scanning=true \
	  -d copier__task_runner="task"; \
	test -f "$$out_dir/copier.yml"; \
	test -f "$$out_dir/Taskfile.yml"; \
	test ! -f "$$out_dir/Makefile"; \
	test ! -f "$$out_dir/justfile"; \
	test -f "$$out_dir/README.md"; \
	test -f "$$out_dir/LICENSE"; \
	test -f "$$out_dir/.github/workflows/template-correctness.yaml"; \
	test -f "$$out_dir/.copier-answers.yml"; \
	test -f "$$out_dir/scripts/test-template-render.sh"; \
	test -f "$$out_dir/template/README.md"; \
	test -f "$$out_dir/template/LICENSE"; \
	test -f "$$out_dir/template/.scaf/post-copy.py"; \
	test -f "$$out_dir/template/Taskfile.yml"; \
	test ! -f "$$out_dir/template/Makefile"; \
	test ! -f "$$out_dir/template/justfile"; \
	test -f "$$out_dir/template/.github/workflows/template-correctness.yaml"; \
	test -f "$$out_dir/template/.github/workflows/secret-scan.yaml"; \
	test ! -f "$$out_dir/template/.github/workflows/semantic-release.yaml"; \
	test ! -f "$$out_dir/template/.github/workflows/semantic-pull-request.yaml"; \
	test ! -f "$$out_dir/template/.gitlab-ci.yml"; \
	test ! -f "$$out_dir/template/package.json"; \
	test ! -f "$$out_dir/template/dependencies-init.txt"; \
	test ! -f "$$out_dir/template/dependencies-dev-init.txt"; \
	test -f "$$out_dir/template/{{_copier_conf.answers_file}}"; \
	grep -Fq '{{ copier__project_name }}' "$$out_dir/template/README.md"; \
	grep -Fq 'copier copy . /path/to/new-project --trust' "$$out_dir/README.md"; \
	grep -Eq '^copier__project_name_raw:' "$$out_dir/copier.yml"; \
	(cd "$$out_dir" && bash ./scripts/test-template-render.sh); \
	render_dir="$$(mktemp -d /tmp/scaf-template-rendered-gh-XXXXXX)"; \
	copier copy "$$out_dir" "$$render_dir" --trust --defaults \
	  -d copier__configure_repo=false \
	  -d copier__enable_semantic_release=false \
	  -d copier__enable_secret_scanning=false \
	  -d copier__ci_provider="github" \
	  -d copier__task_runner="task"; \
	test -f "$$render_dir/.copier-answers.yml"; \
	test -f "$$render_dir/LICENSE"; \
	test ! -f "$$render_dir/{{_copier_conf.answers_file}}"; \
	rm -rf "$$render_dir"; \
	rm -rf "$$out_dir"

# Validate generated template repository structure.
test-template-render-gitlab:
	@set -euo pipefail; \
	out_dir="$$(mktemp -d /tmp/scaf-template-gitlab-XXXXXX)"; \
	copier copy . "$$out_dir" --vcs-ref=HEAD --trust --defaults \
	  -d copier__project_name_raw="Sample GitLab Template" \
	  -d copier__project_slug="sample_gitlab_template" \
	  -d copier__description="Sample gitlab generated project" \
	  -d copier__author_name="Sample Author" \
	  -d copier__email="sample@example.com" \
	  -d copier__version="0.1.0" \
	  -d copier__ci_provider="gitlab" \
	  -d copier__enable_semantic_release=false \
	  -d copier__create_repo=false \
	  -d copier__enable_secret_scanning=true \
	  -d copier__task_runner="just"; \
	test -f "$$out_dir/copier.yml"; \
	test -f "$$out_dir/justfile"; \
	test ! -f "$$out_dir/Makefile"; \
	test ! -f "$$out_dir/Taskfile.yml"; \
	test -f "$$out_dir/README.md"; \
	test -f "$$out_dir/LICENSE"; \
	test -f "$$out_dir/.github/workflows/template-correctness.yaml"; \
	test -f "$$out_dir/.copier-answers.yml"; \
	test -f "$$out_dir/scripts/test-template-render.sh"; \
	test -f "$$out_dir/template/README.md"; \
	test -f "$$out_dir/template/LICENSE"; \
	test -f "$$out_dir/template/.scaf/post-copy.py"; \
	test -f "$$out_dir/template/justfile"; \
	test ! -f "$$out_dir/template/Makefile"; \
	test ! -f "$$out_dir/template/Taskfile.yml"; \
	test -f "$$out_dir/template/.gitlab-ci.yml"; \
	test ! -d "$$out_dir/template/.github"; \
	test ! -f "$$out_dir/template/package.json"; \
	test ! -f "$$out_dir/template/dependencies-init.txt"; \
	test ! -f "$$out_dir/template/dependencies-dev-init.txt"; \
	test -f "$$out_dir/template/{{_copier_conf.answers_file}}"; \
	grep -Fq '{{ copier__project_name }}' "$$out_dir/template/README.md"; \
	grep -Fq 'copier copy . /path/to/new-project --trust' "$$out_dir/README.md"; \
	grep -Eq '^copier__project_name_raw:' "$$out_dir/copier.yml"; \
	(cd "$$out_dir" && bash ./scripts/test-template-render.sh); \
	render_dir="$$(mktemp -d /tmp/scaf-template-rendered-gl-XXXXXX)"; \
	copier copy "$$out_dir" "$$render_dir" --trust --defaults \
	  -d copier__configure_repo=false \
	  -d copier__enable_semantic_release=false \
	  -d copier__enable_secret_scanning=false \
	  -d copier__ci_provider="gitlab" \
	  -d copier__task_runner="just"; \
	test -f "$$render_dir/.copier-answers.yml"; \
	test -f "$$render_dir/LICENSE"; \
	test ! -f "$$render_dir/{{_copier_conf.answers_file}}"; \
	rm -rf "$$render_dir"; \
	rm -rf "$$out_dir"
