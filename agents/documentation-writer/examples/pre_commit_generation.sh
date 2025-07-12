# Run this just before committing & pushing to ensure README.md is up to date.

#!/usr/bin/env bash
set -euo pipefail

# 1. Generate or update README.md via the doc-writer agent
qodo documentation-writer

# 2. Stage, commit, and push
git add README.md
git commit -m "docs: auto-update README before push"
git push origin