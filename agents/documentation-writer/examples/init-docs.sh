Bootstrap documentation for a GitHub-hosted repo that currently lacks it.

#!/usr/bin/env bash
set -euo pipefail

# 1. Clone the target repo
git clone https://github.com/your-repo.git

# (Optional) ensure you're on the main branch
git checkout main || git checkout master

# 2. Invoke the documentation-writer agent
qodo documentation-writer

# 3. Commit and push the new README.md
git add README.md
git commit -m "docs: generate initial README via agent"
git push origin "$(git rev-parse --abbrev-ref HEAD)"
