# Qodo Agent: Changelog Generator

Automate generation of a well-structured CHANGELOG from merged PRs, closed issues, and commit messages. Supports optional grouping by Conventional Commits (feat, fix, docs, chore, refactor).

---

## Features
- Group entries into Features, Fixes, Documentation, Chores, Others
- Optionally group using Conventional Commits
- Includes PR numbers and authors
- Works for date ranges or tag ranges
- Saves Markdown output suitable for `CHANGELOG.md` or `RELEASE.md`

---

## Arguments
| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `repo` | string | yes | - | GitHub repository in `owner/name` format |
| `since` | string | yes | - | Start date or tag for changelog |
| `until` | string | no | HEAD | End date or tag |
| `output_file` | string | no | CHANGELOG.md | File to save generated changelog |
| `group_conventional` | boolean | no | true | Group by Conventional Commits types |
| `include_issues` | boolean | no | true | Include closed issues |
| `include_prs` | boolean | no | true | Include merged pull requests |
| `include_commits` | boolean | no | true | Include commits not tied to PRs |

---

## Build & Validation

To validate the agent configuration and ensure everything is properly set up:

```bash
# Make the build script executable (if needed)
chmod +x build.sh

# Run the build validation
./build.sh
```

The build script will:
- Validate all configuration files (TOML, YAML)
- Check CI/CD configuration syntax
- Verify Qodo CLI can recognize the agent
- Ensure all required dependencies are available

---

## Usage
Prerequisites:
- Node.js 18+ (for Qodo CLI) or Docker
- `GITHUB_PERSONAL_ACCESS_TOKEN` with `repo` scope (if accessing private repos)

Install Qodo CLI:
```
npm install -g @qodo/command
```

Generate changelog between two tags:
```
qodo changelog_generator \
  --set repo=owner/repo \
  --set since=v1.2.0 \
  --set until=v1.3.0 \
  --set output_file=CHANGELOG.md
```

Generate changelog since previous tag to HEAD and group by Conventional Commits:
```
LAST_TAG=$(git describe --tags --abbrev=0)
qodo changelog_generator --set repo=owner/repo --set since=$LAST_TAG --set group_conventional=true
```

---

## Sample Output (excerpt)
```
## v1.3.0 (2025-09-21)

### Features
- feat: Add OAuth login support (#123) by @alice

### Fixes
- fix: Handle null pointer in user service (#130) by @bob

### Documentation
- docs: Update API usage examples (#128) by @carol

### Chores
- chore: Bump dependencies
```

---

## CI Examples
See `examples/ci-configs/` for GitHub Actions and GitLab CI pipelines that generate and commit the updated `CHANGELOG.md` on new releases.

---

## Tools
- `github`
- `filesystem`
- `shell`

---

## License
See top-level LICENSE.


