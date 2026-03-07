#!/usr/bin/env bash
set -euo pipefail

if command -v pre-commit >/dev/null 2>&1 && git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  pre-commit install || echo "pre-commit install failed; continuing"
fi

{% if copier__enable_semantic_release %}
if command -v npm >/dev/null 2>&1; then
  xargs npm install < dependencies-init.txt
  xargs npm install --save-dev < dependencies-dev-init.txt
elif command -v docker >/dev/null 2>&1; then
  docker run --rm --user "$(id -u):$(id -g)" -w "/app" -v "$(pwd):/app" -e npm_config_cache=/tmp/.npm node:lts /bin/bash -c \
    "xargs npm install < dependencies-init.txt"
  docker run --rm --user "$(id -u):$(id -g)" -w "/app" -v "$(pwd):/app" -e npm_config_cache=/tmp/.npm node:lts /bin/bash -c \
    "xargs npm install --save-dev < dependencies-dev-init.txt"
else
  echo "docker and npm not found; skipping semantic-release dependency install"
fi
{% endif %}

echo "Local development setup complete."
