# Documentation Writer Agent

A QODO agent that auto-generates and updates your project’s README.md via a customizable TOML prompt.

## Features

- Fresh generation: create a new README.md.
- In-place updates: modify existing files in place.
- Configurable: customize sections via agent.yml.
- CLI & CI/CD: integrate with Git hooks, GitHub Actions, or scripts.

## Quick Start

1. Copy `agent.toml` from the cloned repo into the project root.
2. Run `qodo documentation-writer` in PowerShell or Git Bash.
3. Review, commit, and push the updated README.md.

## Usage

Install qodo terminal if not already installed.

Place `agent.toml` in the repo root, then run:

```bash
qodo documentation-writer
```

## Git Hook

To auto-run on push, save this as `.git/hooks/pre-push` and make executable:

```bash
#!/usr/bin/env bash
set -euo pipefail
qodo documentation-writer
if ! git diff --quiet -- README.md; then
  git add README.md && git commit -m "docs: auto-update README"
fi
```

```bash
chmod +x .git/hooks/pre-push
```

## License

MIT © 2025