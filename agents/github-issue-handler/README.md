# GitHub Issue Handler Agent

An intelligent agent that automatically processes GitHub issues by analyzing their content, answering questions, implementing code changes, and creating pull requests.

## Overview

This agent monitors GitHub issues and takes appropriate actions based on the issue type:
- **Questions**: Provides comprehensive answers by researching the codebase
- **Bug Reports**: Investigates issues and implements fixes
- **Feature Requests**: Implements new features following project conventions
- **Documentation**: Updates documentation as needed

## Features

- Automatic issue categorization and processing
- Code implementation with proper branching strategy
- Pull request creation with detailed descriptions
- Progress updates via issue comments
- Respects project conventions and contribution guidelines
- Configurable file change limits
- Test execution and validation

## Configuration

The agent accepts the following parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `issue_number` | string | Yes | - | The GitHub issue number to handle |
| `repo_path` | string | No | "." | Path to the repository |
| `base_branch` | string | No | "main" | Base branch to create feature branches from |
| `auto_merge` | boolean | No | false | Automatically merge PR if all checks pass |
| `max_file_changes` | number | No | 50 | Maximum number of files to modify in a single PR |
| `work_in_progress_updates` | boolean | No | true | Post progress updates as comments on the issue |

## Usage

### GitHub Actions

The most common way to use this agent is through GitHub Actions to automatically handle new issues:

```yaml
name: Automatic Issue Handler
on:
  issues:
    types: [opened]

jobs:
  handle-new-issue:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      issues: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run issue handler agent
        uses: qodo-ai/qodo-gen-cli@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          prompt: github-issue-handler
          agent-file: path/to/agent.toml
          key-value-pairs: |
            issue_number=${{ github.event.issue.number }}
```

## Workflow

1. **Issue Analysis**: The agent fetches and analyzes the issue to determine its type
2. **Repository Setup**: Clones or updates the repository and checks out the base branch
3. **Action Execution**: 
   - For questions: Researches and posts comprehensive answers
   - For code changes: Creates a feature branch and implements changes
4. **Pull Request**: Creates a PR with detailed description and links it to the issue
5. **Communication**: Posts updates and results as issue comments

## Best Practices

- The agent respects existing code patterns and conventions
- It runs available tests before creating pull requests
- Breaking changes are clearly documented
- Complex issues are identified and suggestions for splitting are provided
- All interactions maintain professional communication

## Requirements

- GitHub repository with appropriate permissions
- `GITHUB_TOKEN` with write access to contents, issues, and pull requests
- `QODO_API_KEY` for the Qodo platform, get one at [Qodo](https://qodo.ai)
- Repository should have the agent configuration file accessible

## Examples

See the [examples](examples/) directory for:
- Different GitHub Actions configurations
- Handling various issue types
- Custom agent configurations
- Integration with different CI/CD platforms