# Usage Examples

This document provides practical examples of using the Clean Code Description Agent in various workflows — locally, in CI/CD pipelines, and within IDEs.

## 🧩 Basic Usage

### Review Current Code for Documentation Quality

```bash
# Review all unstaged and staged changes
qodo clean_code_description

# Review against a specific branch
qodo clean_code_description --target_branch=develop

# Include suggestions for improvement
qodo clean_code_description --include_suggestions=true
```

### Focus on Specific Areas
```bash
# Focus on missing or outdated docstrings
qodo clean_code_description --focus_areas=docstrings

# Focus on poor naming and redundant comments
qodo clean_code_description --focus_areas=naming,comments

# Comprehensive review across all areas
qodo clean_code_description --focus_areas=docstrings,comments,naming,consistency
```

## ⚙️ Advanced Configuration

### Exclude Specific Files

```bash
# Exclude test and auto-generated files
qodo clean_code_description --exclude_files="*.test.py,*.generated.js,__pycache__/*"

# Exclude documentation and build directories
qodo clean_code_description --exclude_files="docs/*,build/*,dist/*"
```

### Language-Specific Examples

#### 🐍 Python (Flask/Django)

```bash
qodo clean_code_description \
  --target_branch=main \
  --focus_areas=docstrings,comments,naming \
  --exclude_files="migrations/*,__pycache__/*" \
  --include_suggestions=true
```

#### 🧠 JavaScript/TypeScript
```bash
qodo clean_code_description \
  --target_branch=develop \
  --focus_areas=comments,naming \
  --exclude_files="node_modules/*,*.config.js" \
  --include_suggestions=true
```

#### ☕ Java / Kotlin
```bash
qodo clean_code_description \
  --target_branch=main \
  --focus_areas=docstrings,naming \
  --exclude_files="target/*,*.class" \
  --include_suggestions=true
```


## 🧰 CI/CD Integration

### GitHub Actions

```yaml
name: Clean Code Description Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  clean-code-check:
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
            exclude_files=*.md,docs/*
            include_suggestions=true
```

### GitLab CI (Added Quality Gate - Fail Build on Poor Documentation)

```yaml
stages:
  - documentation-review
  - quality-gate

clean-code-description:
  stage: documentation-review
  image: node:18
  before_script:
    - npm install -g @qodo/gen
  script:
    - |
      qodo -q --ci clean_code_description \
        --target_branch=$CI_MERGE_REQUEST_TARGET_BRANCH_NAME \
        --focus_areas=docstrings,comments,naming,consistency \
        --exclude_files="node_modules/*,dist/*" \
        > clean-code-review.json
    - cat clean-code-review.json
  artifacts:
    paths:
      - clean-code-review.json
    expire_in: 1 hour
  only:
    - merge_requests

quality-gate:
  stage: quality-gate
  image: alpine:latest
  dependencies:
    - clean-code-description
  before_script:
    - apk add --no-cache jq
  script:
    - |
      missing_docstrings=$(jq -r '.summary.missing_docstrings' clean-code-review.json)
      outdated=$(jq -r '.summary.outdated_descriptions' clean-code-review.json)
      poor_names=$(jq -r '.summary.poor_names' clean-code-review.json)

      echo "📊 Documentation Issues Summary:"
      echo "  Missing Docstrings: $missing_docstrings"
      echo "  Outdated Descriptions: $outdated"
      echo "  Poor Naming: $poor_names"

      if [ "$missing_docstrings" -gt 5 ]; then
        echo "❌ Quality gate failed: Too many missing docstrings"
        exit 1
      fi

      if [ "$outdated" -gt 3 ]; then
        echo "❌ Quality gate failed: Outdated docstrings found"
        exit 1
      fi

      if [ "$poor_names" -gt 3 ]; then
        echo "⚠️ Warning: Poorly named functions or variables detected"
      fi

      echo "✅ Documentation quality gate passed"
  only:
    - merge_requests

```

### Jenkins Pipeline (Quality Gate + Reporting)
```bash
// Jenkins pipeline for Clean Code Description Agent with quality gate
pipeline {
    agent any

    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Setup') {
            steps {
                // install qodo CLI or use docker image; choose one approach
                sh 'npm install -g @qodo/gen || true'
            }
        }

        stage('Clean Code Description Review') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'
                    // Run agent and save JSON output
                    sh """
                      qodo -q --ci clean_code_description \
                        --target_branch=${targetBranch} \
                        --focus_areas=docstrings,comments,naming,consistency \
                        --exclude_files="node_modules/*,dist/*,docs/*" \
                        > clean-code-review.json
                    """
                    // Print results for logs
                    sh 'cat clean-code-review.json'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def json = readFile('clean-code-review.json')
                    // Use groovy JsonSlurper to parse
                    def parser = new groovy.json.JsonSlurper()
                    def results = parser.parseText(json)

                    def missing = results.summary?.missing_docstrings ?: 0
                    def outdated = results.summary?.outdated_descriptions ?: 0
                    def poorNames = results.summary?.poor_names ?: 0
                    def overallScore = results.summary?.overall_score ?: 0.0

                    echo "Documentation summary: missing=${missing}, outdated=${outdated}, poor_names=${poorNames}, score=${overallScore}"

                    // Fail build if thresholds exceeded
                    if (missing > 5) {
                        error("Quality gate failed: ${missing} missing docstrings (threshold: 5)")
                    }
                    if (outdated > 3) {
                        error("Quality gate failed: ${outdated} outdated descriptions (threshold: 3)")
                    }
                    // Warn but do not fail for poor names
                    if (poorNames > 3) {
                        echo "WARNING: ${poorNames} poor naming instances detected"
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'clean-code-review.json', fingerprint: true
        }
    }
}
```

> [!NOTE]
> The Jenkins pipeline uses either a locally-installed qodo CLI or the qodo Docker image — adapt the sh commands based on your environment.
> Adjust thresholds (missing > 5, outdated > 3) to match your project's standards.


## IDE Integration

### VS Code Tasks

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Clean Code Description - Full Review",
      "type": "shell",
      "command": "qodo",
      "args": [
        "clean_code_description",
        "--focus_areas=docstrings,comments,naming,consistency",
        "--include_suggestions=true"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Clean Code Description - Quick Docstring Check",
      "type": "shell",
      "command": "qodo",
      "args": [
        "clean_code_description",
        "--focus_areas=docstrings"
      ],
      "group": "test"
    }
  ]
}
```

### IntelliJ IDEA External Tool
```xml
<tool name="Clean Code Description" description="Analyze docstrings, comments, and naming consistency" showInMainMenu="true" showInEditor="true" showInProject="true" showInSearchPopup="true" disabled="false" useConsole="true" showConsoleOnStdOut="false" showConsoleOnStdErr="false" synchronizeAfterRun="true">
  <exec>
    <option name="COMMAND" value="qodo" />
    <option name="PARAMETERS" value="clean_code_description --focus_areas=docstrings,comments,naming --include_suggestions=true" />
    <option name="WORKING_DIRECTORY" value="$ProjectFileDir$" />
  </exec>
</tool>
```

## Pre-commit Hooks

### Using pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: clean-code-description
        name: Check for missing or outdated docstrings
        entry: qodo
        args: [clean_code_description, --focus_areas=docstrings,naming]
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

### Git Hook Script

```yaml
#!/bin/bash
# .git/hooks/pre-commit

echo "🧹 Running Clean Code Description check..."

qodo -q --ci clean_code_description --focus_areas=docstrings,comments,naming > /tmp/clean-code-review.json

if [ $? -ne 0 ]; then
    echo "❌ Review failed"
    cat /tmp/clean-code-review.json
    exit 1
fi

missing_docstrings=$(jq -r '.summary.missing_docstrings' /tmp/clean-code-review.json)
outdated=$(jq -r '.summary.outdated_descriptions' /tmp/clean-code-review.json)
poor_names=$(jq -r '.summary.poor_names' /tmp/clean-code-review.json)

echo "Docstring Issues: $missing_docstrings"
echo "Outdated Descriptions: $outdated"
echo "Poor Naming Instances: $poor_names"

if [ "$missing_docstrings" -gt 0 ] || [ "$outdated" -gt 0 ] || [ "$poor_names" -gt 0 ]; then
  echo "⚠️ Please update documentation before committing."
  exit 1
fi

echo "✅ Code documentation looks clean!"
exit 0
```

## 🧪 Output Examples

#### ✅ Clean Code
```json
{
  "summary": {
    "total_issues": 0,
    "critical_issues": 0,
    "high_issues": 0,
    "medium_issues": 0,
    "low_issues": 0,
    "missing_docstrings": 0,
    "outdated_descriptions": 0,
    "redundant_comments": 0,
    "poor_names": 0,
    "files_reviewed": 8,
    "overall_score": 9
  },
  "approved": true,
  "requires_changes": false
}
```

### ⚠️ Documentation Warnings

```json
{
  "summary": {
    "total_issues": 7,
    "critical_issues": 2,
    "high_issues": 1,
    "medium_issues": 2,
    "low_issues": 2,
    "missing_docstrings": 3,
    "outdated_descriptions": 2,
    "redundant_comments": 1,
    "poor_names": 1,
    "files_reviewed": 6,
    "overall_score": 6
  },
  "issues": [
    {
      "file": "src/utils/math_utils.py",
      "line": 10,
      "type": "missing_docstring",
      "description": "Function 'calculate_ratio' lacks a docstring"
    },
    {
      "file": "src/api/routes.js",
      "line": 35,
      "type": "outdated_description",
      "description": "Comment describes old parameter 'token' which was removed"
    }
  ],
  "approved": false,
  "requires_changes": true
}
```

