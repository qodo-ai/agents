# PR README Updater Agent

## Overview

This agent automates the process of updating the README file when new community agents are added via pull requests. It reviews merged PRs, analyzes the new agents, and automatically creates a documentation update PR with proper attribution to contributors.

## Features

- **Automated PR Analysis**: Fetches and analyzes merged pull requests to identify new agents
- **Smart Categorization**: Automatically categorizes agents into appropriate sections (Security & Compliance, Development Workflow, etc.)
- **README Updates**: Updates the Community Agents section with proper formatting and attribution
- **Branch Management**: Creates feature branches and pull requests for documentation updates
- **Contributor Attribution**: Ensures proper credit is given to community contributors

## Requirements

- GitHub Personal Access Token with repository access
- Qodo Command installed globally (`npm install -g @qodo/command`)
- Git configured for the repository
- GitHub CLI tool (`gh`) installed (optional but recommended)

## Usage

### Basic Usage

```bash
# Update README for a specific merged PR
qodo pr-readme-updater --pr_number=10

# Specify different repository
qodo pr-readme-updater --pr_number=15 --repo_owner=myorg --repo_name=my-agents

# Use custom branch prefix
qodo pr-readme-updater --pr_number=20 --branch_prefix=docs/community-update
```

### Environment Setup

Make sure you have the required environment variable set:

```bash
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_token_here"
```

### Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `pr_number` | number | Yes | - | The PR number to review and document |
| `repo_owner` | string | No | "qodo-ai" | Repository owner |
| `repo_name` | string | No | "agents" | Repository name |
| `base_branch` | string | No | "main" | Base branch to create feature branch from |
| `branch_prefix` | string | No | "docs/update-readme" | Prefix for the new branch name |

## How It Works

### 1. PR Analysis Phase
- Fetches the specified PR details using GitHub API
- Verifies the PR is merged and contains agent-related changes
- Extracts information about new agents:
  - Agent name and directory location
  - Description and functionality
  - Contributor information
  - Files added or modified

### 2. Categorization
The agent automatically categorizes new agents into appropriate sections:

- **Development Workflow Agents**: Code review, testing, CI/CD, development automation
- **Security & Compliance**: Security scanning, compliance checks, vulnerability management
- **Data & Analytics**: Data processing, analysis, reporting agents
- **Infrastructure & DevOps**: Deployment, monitoring, infrastructure management
- **Documentation**: Documentation generation, maintenance, validation
- **Quality Assurance**: Testing, quality checks, performance analysis

### 3. README Update
- Reads the current README.md file
- Locates the "Community Agents" section
- Adds new agent entries with consistent formatting:
  ```markdown
  - **[Agent Name](agents/agent-directory/)** - Brief description *(contributed by [@username](https://github.com/username))*
  ```

### 4. PR Creation
- Creates a new branch: `{branch_prefix}-pr-{pr_number}`
- Commits changes with descriptive message
- Pushes branch to repository
- Creates pull request with comprehensive description

## Example Output

When processing PR #10 (OpenSSF Scorecard Fixer), the agent would:

1. **Analyze PR #10**: "feat: add OpenSSF Scorecard fixer agent" by @lirantal
2. **Identify Agent**: `agents/openssf-scorecard-fixer/` directory
3. **Categorize**: Security & Compliance
4. **Update README**: Add entry with proper attribution
5. **Create Branch**: `docs/update-readme-pr-10`
6. **Create PR**: Documentation update with reference to original PR

## Error Handling

The agent handles various error scenarios:

- **PR Not Found**: Clear error message if PR doesn't exist
- **PR Not Merged**: Verification that PR is actually merged
- **No Agent Files**: Detection when PR doesn't contain agent changes
- **README Issues**: Validation of README syntax and formatting
- **Branch Conflicts**: Alternative branch name suggestions
- **API Failures**: Fallback strategies for GitHub API issues

## Validation

The agent performs comprehensive validation:

### Pre-flight Checks
- ✅ PR exists and is merged
- ✅ Agent files are present in changes
- ✅ README.md exists and is writable

### Post-update Validation
- ✅ README syntax is valid
- ✅ New entry is properly formatted
- ✅ Links are correctly formed
- ✅ Attribution is accurate

## Integration

This agent can be integrated into various workflows:

### Manual Usage
```bash
# After a community PR is merged
qodo pr-readme-updater --pr_number=25
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Update README for merged PR
  run: qodo pr-readme-updater --pr_number=${{ github.event.pull_request.number }}
  env:
    GITHUB_PERSONAL_ACCESS_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Webhook Integration
Set up webhooks to automatically trigger README updates when PRs are merged.

## Contributing

When contributing to this agent:

1. Maintain the existing categorization logic
2. Ensure proper error handling for edge cases
3. Test with various PR types and scenarios
4. Update documentation for any new features
5. Follow the existing code style and patterns

## Troubleshooting

### Common Issues

**GitHub API Rate Limits**
- Use authenticated requests with proper token
- Implement retry logic for rate-limited requests

**Branch Creation Failures**
- Check for existing branches with same name
- Ensure proper Git configuration and permissions

**README Formatting Issues**
- Validate Markdown syntax before committing
- Test links and references

**Attribution Errors**
- Verify contributor information from PR data
- Handle cases where contributor info is missing

## Related Agents

- **[Code Review](../code-review/)** - Analyzes code changes for quality
- **[GitHub Issue Handler](../github-issue-handler/)** - Processes GitHub issues automatically

---

**Built with ❤️ for the Qodo community**