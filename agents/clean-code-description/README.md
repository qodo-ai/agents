# 🧹 Clean Code Description Agent

A specialized Qodo agent that ensures your codebase remains clean, readable, and well-documented by reviewing docstrings, comments, and naming conventions.

## 🧭 Overview

This agent analyzes your codebase to maintain high documentation quality and consistency by checking for:

- 📝 **Missing or incomplete docstrings**

- 🔄 **Outdated or inaccurate descriptions**

- 💬 **Redundant or low-value comments**

- ⚖️ **Inconsistent documentation styles**

- 🧩 **Poorly named functions, classes, or variables**

It helps developers ensure that documentation matches code behavior and follows consistent standards, improving maintainability and onboarding for teams.

## ✨ Features

- 🧠 **Context-Aware Analysis**: Uses `qodo_merge` to compare documentation and code logic

- 🧾 **Docstring Review**: Detects missing, incomplete, or misleading docstrings

- 🧩 **Naming Convention Audit**: Flags unclear or inconsistent names

- 🧹 **Comment Clarity Check**: Removes redundancy and improves explanations

- 📊 **Documentation Quality Score**: Summarizes code cleanliness on a 0–10 scale

- 🔧 **Actionable Suggestions**: Provides example rewrites and improvements


## 🚀 Quick Start

**Basic Usage**
```bash
# Run the agent to review code documentation
qodo clean_code_description

# Compare current changes against the main branch
qodo clean_code_description --target_branch=main

# Focus only on docstrings and naming issues
qodo clean_code_description --focus_areas=docstrings,naming
```

**Advanced Configuration**
```bash
qodo clean_code_description \
  --target_branch=develop \
  --severity_threshold=medium \
  --focus_areas=docstrings,comments,naming \
  --exclude_files="tests/*,*.md" \
  --include_suggestions=true
```

## ⚙️ Configuration
The agent accepts the following parameters:

| Parameter             | Type    | Required | Default    | Description                                                            |
| --------------------- | ------- | -------- | ---------- | ---------------------------------------------------------------------- |
| `target_branch`       | string  | No       | `"main"`   | Branch to compare changes against                                      |
| `severity_threshold`  | string  | No       | `"medium"` | Minimum severity to report (low/medium/high/critical)                  |
| `include_suggestions` | boolean | No       | `true`     | Include improvement suggestions in output                              |
| `focus_areas`         | string  | No       | -          | Comma-separated list of areas to review (docstrings, comments, naming) |
| `exclude_files`       | string  | No       | -          | File patterns to exclude from analysis                                 |


## Output Format

The agent returns structured JSON output:

```json
{
  "summary": {
    "total_issues": 8,
    "critical_issues": 0,
    "high_issues": 3,
    "medium_issues": 4,
    "low_issues": 1,
    "files_reviewed": 5,
    "overall_score": 7.8,
    "missing_docstrings": 3,
    "outdated_descriptions": 2,
    "redundant_comments": 2,
    "poor_names": 1
  },
  "issues": [
    {
      "file": "src/utils/formatter.py",
      "line": 12,
      "severity": "medium",
      "category": "docstring",
      "title": "Missing function docstring",
      "description": "The function `format_name` lacks a docstring, making its behavior unclear.",
      "suggestion": "Add a concise docstring describing the purpose and parameters.",
      "code_example": "\"\"\"Format the input name by capitalizing each word.\"\"\""
    }
  ],
  "suggestions": [
    {
      "file": "src/models/user.py",
      "type": "naming",
      "description": "Rename variable `usrObj` to `user` for clarity",
      "implementation": "Use descriptive names that reflect purpose instead of type"
    }
  ],
  "approved": false,
  "requires_changes": true
}
```

## 🧰 Tools Used
This agent uses the following tools from the Qodo ecosystem:

- 🧠 **qodo_merge** – Analyzes code diffs and merges semantic context for intelligent reviews

- 📂 **filesystem** – Reads local file structures and extracts docstrings/comments

- 🐙 **git** – Compares branches and identifies changed files for focused analysis

## 🧑‍💻 Usage Examples

### GitHub Actions (Pull Request Reviews)

The most common way to use this agent is through GitHub Actions to automatically review pull requests:

```yaml
name: Clean Code Description Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  clean-code:
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

      - name: Run Clean Code Description Agent
        uses: qodo-ai/command@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          prompt: clean_code_description
          agent-file: path/to/agent.toml
          key-value-pairs: |
            target_branch=${{ github.base_ref }}
            focus_areas=docstrings,comments,naming
            severity_threshold=medium
            include_suggestions=true
```

### Pre-commit Hook

```bash
#!/bin/bash
echo "Running Clean Code Description Agent..."
qodo clean_code_description --severity_threshold=medium

if [ $? -ne 0 ]; then
    echo "❌ Code cleanliness check failed. Please fix documentation issues before committing."
    exit 1
fi

echo "✅ Code documentation looks great!"
```

### VS Code Integration

```json
{
  "label": "Qodo Clean Code Review",
  "type": "shell",
  "command": "qodo",
  "args": ["clean_code_description", "--include_suggestions=true"],
  "group": "build",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "panel": "shared"
  }
}
```

## Best Practices

### 1. Regular Reviews
Run code reviews on every pull request to maintain clean code documentaion.

### 2. Severity Thresholds
- **CI/CD**: Use `high` or `critical` thresholds to prevent blocking
- **Development**: Use `medium` for comprehensive feedback
- **Learning**: Use `low` to catch all potential improvements

### 3. Focus Areas
Specify focus areas based on your project needs.

### 4. Exclusions
Exclude generated files and test fixtures:

```bash
--exclude_files="test/*,build/*"
```

## ⚠️ Troubleshooting

### Agent not finding changes

Ensure you’re in a Git repository with uncommitted changes or specify `--target_branch`.

### Too many false positives

Adjust `--severity_threshold` or limit `--focus_areas`.

### Performance issues

Exclude large files or vendor directories using `--exclude_files`.

## 🔑 Requirements

- GitHub repository with appropriate permissions
- `GITHUB_TOKEN` with read access to contents and write access to pull requests and checks
- `QODO_API_KEY` get one at [Qodo](https://qodo.ai)
- Repository should have the agent configuration file accessible

## 🧱 Examples

See `examples/` for:

- CI/CD pipelines

- Pre-commit setup

- IDE task runners

- Custom configuration templates

## 📜 License
MIT License.