# place this script in .git/hooks/pre-push
#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Running Documentation Writer Agent..."
# Generate or update README.md via QODO agent
qodo documentation-writer

# If README.md changed, commit it before push
if ! git diff --quiet -- ./README.md; then
  echo "✏️  README.md updated by agent, committing..."
  git add README.md
  git commit -m "docs: auto-update README via Documentation Writer Agent"
else
  echo "✅ README.md is up to date."
fi

# allow push to proceed
exit 0

# Make this script executable. Run the following command in your terminal:
# chmod +x .git/hooks/pre-push
