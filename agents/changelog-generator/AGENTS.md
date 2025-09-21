# Repository Guidelines

## Project Structure & Module Organization

This is a Qodo Agent for automated changelog generation. The repository contains:
- `agent.toml` and `agent.yaml` - Agent configuration files defining the changelog generator command
- `README.md` - Main documentation and usage examples
- `examples/ci-configs/` - CI/CD pipeline configurations for GitHub Actions and GitLab CI

## Build, Test, and Development Commands

```bash
# Install Qodo CLI (prerequisite)
npm install -g @qodo/command

# Run the changelog generator
qodo changelog_generator \
  --set repo=owner/repo \
  --set since=v1.2.0 \
  --set until=v1.3.0 \
  --set output_file=CHANGELOG.md

# Generate changelog since last tag
LAST_TAG=$(git describe --tags --abbrev=0)
qodo changelog_generator --set repo=owner/repo --set since=$LAST_TAG --set group_conventional=true
```

## Coding Style & Naming Conventions

- **Configuration format**: TOML and YAML for agent definitions
- **Commit conventions**: Conventional Commits (feat, fix, docs, chore, refactor)
- **File naming**: Lowercase with hyphens (e.g., `github-actions.yml`)
- **Documentation**: Markdown format with clear section headers

## Testing Guidelines

- **Framework**: Manual testing via Qodo CLI execution
- **Test approach**: Validate against real repositories with various commit patterns
- **Validation**: Verify generated changelog format and content accuracy

## Commit & Pull Request Guidelines

- **Commit format**: Conventional Commits format (e.g., `docs(changelog): update for v1.3.0`)
- **Categories**: feat, fix, docs, chore, refactor
- **Examples from CI configs**: `docs(changelog): update for ${CI_COMMIT_REF_NAME}`

---

# Repository Tour

## 🎯 What This Repository Does

Qodo Agent: Changelog Generator is a specialized agent that automates the generation of well-structured changelogs from merged PRs, closed issues, and commit messages, with optional grouping by Conventional Commits.

**Key responsibilities:**
- Fetch and analyze GitHub repository data (PRs, issues, commits)
- Group changes into logical categories (Features, Fixes, Documentation, Chores, Others)
- Generate human-readable Markdown changelogs suitable for CHANGELOG.md or RELEASE.md files

---

## 🏗️ Architecture Overview

### System Context
```
[GitHub Repository] → [Qodo Agent] → [Generated CHANGELOG.md]
        ↓                ↓
[GitHub API]      [Local Filesystem]
```

### Key Components
- **Agent Configuration** - Defines command arguments, tools, and execution strategy
- **GitHub Integration** - Fetches repository data via GitHub API using MCP server
- **Content Processor** - Groups and formats changelog entries based on Conventional Commits
- **File Generator** - Outputs structured Markdown changelog files

### Data Flow
1. User provides repository details and date/tag range via Qodo CLI
2. Agent authenticates with GitHub API using personal access token
3. Repository data (PRs, issues, commits) is fetched for the specified range
4. Content is categorized using Conventional Commit patterns or heuristic grouping
5. Formatted Markdown changelog is generated and saved to specified output file

---

## 📁 Project Structure [Partial Directory Tree]

```
changelog-generator/
├── agent.toml              # TOML agent configuration
├── agent.yaml              # YAML agent configuration (alternative format)
├── README.md               # Documentation and usage examples
└── examples/               # CI/CD integration examples
    └── ci-configs/         # Pipeline configurations
        ├── github-actions.yml  # GitHub Actions workflow
        └── gitlab-ci.yml       # GitLab CI pipeline
```

### Key Files to Know

| File | Purpose | When You'd Touch It |
|------|---------|---------------------|
| `agent.toml` | Primary agent configuration | Modifying command arguments or tools |
| `agent.yaml` | Alternative YAML configuration | Preferring YAML over TOML format |
| `README.md` | Documentation and examples | Updating usage instructions |
| `examples/ci-configs/github-actions.yml` | GitHub Actions integration | Setting up automated changelog generation |
| `examples/ci-configs/gitlab-ci.yml` | GitLab CI integration | Configuring GitLab pipeline automation |

---

## 🔧 Technology Stack

### Core Technologies
- **Platform:** Qodo Agent Framework - Provides the execution environment and CLI interface
- **Configuration:** TOML/YAML - Agent definition and command specification
- **API Integration:** GitHub API via MCP (Model Context Protocol) - Repository data access
- **Output Format:** Markdown - Human-readable changelog generation

### Key Libraries
- **GitHub MCP Server** - Handles GitHub API authentication and data fetching
- **Shell MCP Server** - Provides shell command execution capabilities
- **Filesystem Tools** - File reading and writing operations

### Development Tools
- **Qodo CLI** - Command execution and agent management
- **Node.js 18+** - Runtime requirement for Qodo CLI
- **Git** - Version control and tag management

---

## 🌐 External Dependencies

### Required Services
- **GitHub API** - Repository data source (PRs, issues, commits, tags)
- **GitHub Personal Access Token** - Authentication for private repository access

### Optional Integrations
- **CI/CD Platforms** - GitHub Actions, GitLab CI for automated changelog generation
- **Docker** - Alternative runtime environment for Qodo CLI

### Environment Variables

```bash
# Required for private repositories
GITHUB_PERSONAL_ACCESS_TOKEN=  # GitHub API authentication token with 'repo' scope

# CI/CD specific (examples)
GITHUB_TOKEN=                  # GitHub Actions built-in token
GITLAB_TOKEN=                  # GitLab CI access token
```

---

## 🔄 Common Workflows

### Manual Changelog Generation
1. Install Qodo CLI: `npm install -g @qodo/command`
2. Set GitHub token: `export GITHUB_PERSONAL_ACCESS_TOKEN=your_token`
3. Run command with repository and version range
4. Review generated CHANGELOG.md file

**Code path:** `qodo CLI` → `agent.toml` → `GitHub MCP` → `CHANGELOG.md`

### Automated CI/CD Integration
1. Configure CI pipeline using provided examples
2. Pipeline triggers on new tags or manual dispatch
3. Determines version range (previous tag to current)
4. Generates changelog and commits back to repository

**Code path:** `CI Trigger` → `Qodo CLI` → `Agent` → `Git Commit` → `Repository`

---

## 📈 Performance & Scale

### Performance Considerations
- **API Rate Limits:** GitHub API has rate limits; agent respects these automatically
- **Repository Size:** Performance scales with number of PRs/issues in date range
- **Caching:** No built-in caching; each run fetches fresh data

### Monitoring
- **Success Metrics:** Changelog generation success, commit/PR/issue counts
- **Error Handling:** GitHub API errors, authentication failures, file write permissions

---

## 🚨 Things to Be Careful About

### 🔒 Security Considerations
- **Token Management:** GitHub Personal Access Token should have minimal required scopes
- **CI/CD Secrets:** Store tokens securely in CI platform secret management
- **Repository Access:** Token grants access to all repositories within scope

### Configuration Management
- **Conventional Commits:** Ensure team follows conventional commit format for best categorization
- **Date Ranges:** Verify tag existence and date formats to avoid empty changelogs
- **Output Conflicts:** Multiple CI runs may conflict when committing changelog updates

*Updated at: 2024-12-19 UTC*