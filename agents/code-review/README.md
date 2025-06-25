# Code Review Agent

A comprehensive code review agent that leverages Qodo Merge to provide detailed, actionable feedback on code changes.

## Overview

This agent analyzes code changes and provides:
- **Security vulnerability detection**
- **Performance optimization suggestions**
- **Code maintainability improvements**
- **Best practice recommendations**
- **Categorized feedback by severity**

## Features

- 🔍 **Deep Code Analysis**: Uses Qodo Merge for comprehensive code review
- 🏷️ **Severity Classification**: Categorizes issues as Critical, High, Medium, or Low
- 🛡️ **Security Focus**: Identifies potential security vulnerabilities
- ⚡ **Performance Insights**: Suggests performance optimizations
- 📊 **Structured Output**: JSON output for easy integration
- 🔧 **Configurable**: Customizable severity thresholds and focus areas

## Quick Start

### Basic Usage

```bash
# Review current changes against main branch
qodo code_review

# Review with specific target branch
qodo code_review --target_branch=develop

# Focus on security issues only
qodo code_review --focus_areas=security --severity_threshold=high
```

### Advanced Configuration

```bash
# Comprehensive review with custom settings
qodo code_review \
  --target_branch=main \
  --severity_threshold=medium \
  --focus_areas=security,performance \
  --exclude_files="*.test.js,*.spec.ts" \
  --include_suggestions=true
```

## Configuration

The agent accepts the following parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `target_branch` | string | No | "main" | Branch to compare changes against |
| `severity_threshold` | string | No | "medium" | Minimum severity to report (low/medium/high/critical) |
| `include_suggestions` | boolean | No | true | Include improvement suggestions in output |
| `focus_areas` | string | No | - | Comma-separated focus areas (security, performance, maintainability) |
| `exclude_files` | string | No | - | File patterns to exclude from review |

## Output Format

The agent returns structured JSON output:

```json
{
  "summary": {
    "total_issues": 5,
    "critical_issues": 1,
    "high_issues": 2,
    "medium_issues": 2,
    "low_issues": 0,
    "files_reviewed": 3,
    "overall_score": 7.5
  },
  "issues": [
    {
      "file": "src/auth.js",
      "line": 42,
      "severity": "critical",
      "category": "security",
      "title": "SQL Injection Vulnerability",
      "description": "Direct string concatenation in SQL query allows injection attacks",
      "suggestion": "Use parameterized queries or prepared statements",
      "code_example": "const query = 'SELECT * FROM users WHERE id = ?'; db.query(query, [userId]);"
    }
  ],
  "suggestions": [
    {
      "file": "src/utils.js",
      "type": "performance",
      "description": "Consider using Map instead of Object for frequent lookups",
      "implementation": "Replace object with new Map() for better performance"
    }
  ],
  "approved": false,
  "requires_changes": true
}
```

## Usage

### GitHub Actions

The most common way to use this agent is through GitHub Actions to automatically review pull requests:

```yaml
name: Code Review Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  code-review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      checks: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run code review agent
        uses: qodo-ai/qodo-gen-cli@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          prompt: code-review
          agent-file: path/to/agent.toml
          key-value-pairs: |
            target_branch=${{ github.base_ref }}
            severity_threshold=medium
            focus_areas=security,performance
            exclude_files=package-lock.json,*.md
            include_suggestions=true
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running code review..."
qodo -q --ci code_review --severity_threshold=high

if [ $? -ne 0 ]; then
    echo "Code review failed. Please address the issues before committing."
    exit 1
fi

echo "Code review passed!"
```

### VS Code Integration

```json
{
  "tasks": [
    {
      "label": "Qodo Code Review",
      "type": "shell",
      "command": "qodo",
      "args": ["code_review", "--include_suggestions=true"],
      "group": "build",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      }
    }
  ]
}
```

## Best Practices

### 1. Regular Reviews
Run code reviews on every pull request to maintain code quality.

### 2. Severity Thresholds
- **CI/CD**: Use `high` or `critical` thresholds to prevent blocking
- **Development**: Use `medium` for comprehensive feedback
- **Learning**: Use `low` to catch all potential improvements

### 3. Focus Areas
Specify focus areas based on your project needs:
- **New features**: `security,maintainability`
- **Performance critical**: `performance,security`
- **Legacy refactoring**: `maintainability,performance`

### 4. Exclusions
Exclude generated files and test fixtures:
```bash
--exclude_files="*.generated.js,test/fixtures/*,dist/*"
```

## Troubleshooting

### Common Issues

**Agent not finding changes:**
- Ensure you're in a git repository
- Check that there are uncommitted changes or specify target branch

**Missing Qodo Merge integration:**
- Verify Qodo Merge server is installed: `npm list -g @qodo/merge-server`
- Check authentication with Qodo services

**Performance issues with large diffs:**
- Use `exclude_files` to skip large generated files
- Consider reviewing smaller changesets

### Debug Mode

```bash
# Save log output for debugging
qodo code_review --log=debug.log

# Save output for analysis with silent mode to suppress console output other than final results
qodo -q code_review > review-output.json 2> review-debug.log
```

## Requirements

- GitHub repository with appropriate permissions
- `GITHUB_TOKEN` with read access to contents and write access to pull requests and checks
- `QODO_API_KEY` for the Qodo platform, get one at [Qodo](https://qodo.ai)
- Repository should have the agent configuration file accessible

## Examples

See the [examples](examples/) directory for:
- Different GitHub Actions configurations
- CI/CD platform integrations
- IDE integration examples
- Custom agent configurations

## Contributing

Found an issue or want to improve this agent? Please see our [Contributing Guide](../../CONTRIBUTING.md).

### Reporting Issues
- Include sample code that reproduces the issue
- Provide the agent configuration used
- Include relevant error messages or unexpected output

### Suggesting Improvements
- Describe the enhancement and its benefits
- Provide examples of the desired behavior
- Consider backward compatibility

## License

This agent is part of the Qodo Agent Reference Implementations and is licensed under the MIT License.