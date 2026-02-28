#!/usr/bin/env bash
set -euo pipefail

if command -v pre-commit >/dev/null 2>&1; then
  pre-commit install
fi

{% if copier__enable_semantic_release %}
if command -v npm >/dev/null 2>&1; then
  npm install
else
  echo "npm not found; skipping semantic-release dependency install"
fi
{% endif %}

echo "Local development setup complete."
