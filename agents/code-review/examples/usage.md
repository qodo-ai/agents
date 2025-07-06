# Usage Examples

This document provides practical examples of using the Code Review Agent in various scenarios.

## Basic Usage

### Review Current Changes
```bash
# Review all unstaged and staged changes
qodo code_review

# Review against specific branch
qodo code_review --target_branch=develop

# Review with custom severity threshold
qodo code_review --severity_threshold=high
```

### Focus on Specific Areas
```bash
# Focus on security issues only
qodo code_review --focus_areas=security

# Review multiple focus areas
qodo code_review --focus_areas=security,performance,maintainability

# Include improvement suggestions
qodo code_review --include_suggestions=true
```

## Advanced Configuration

### Exclude Specific Files
```bash
# Exclude test files and generated code
qodo code_review --exclude_files="*.test.js,*.spec.ts,dist/*,build/*"

# Exclude configuration and documentation
qodo code_review --exclude_files="*.config.js,*.md,docs/*"

# Exclude multiple patterns
qodo code_review --exclude_files="node_modules/*,*.generated.ts,__tests__/*"
```

### Project-Specific Examples

#### Node.js/Express API
```bash
# Review API changes with security focus
qodo code_review \
  --target_branch=main \
  --focus_areas=security,performance \
  --exclude_files="package-lock.json,node_modules/*" \
  --severity_threshold=medium
```

#### Python Django Project
```bash
# Review Django app changes
qodo code_review \
  --target_branch=develop \
  --focus_areas=security,maintainability \
  --exclude_files="*.pyc,__pycache__/*,migrations/*" \
  --include_suggestions=true
```

#### Java Spring Boot
```bash
# Review Spring Boot changes
qodo code_review \
  --target_branch=main \
  --focus_areas=security,performance \
  --exclude_files="target/*,*.class" \
  --severity_threshold=high
```

## CI/CD Integration

### GitHub Actions Workflow
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
        uses: qodo-ai/command@v1
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

### GitLab CI Pipeline
```yaml
stages:
  - code-review
  - quality-gate

code-review:
  stage: code-review
  image: node:18
  before_script:
    - npm install -g @qodo/gen
  script:
    - |
      qodo -q --ci code_review \
        --target_branch=$CI_MERGE_REQUEST_TARGET_BRANCH_NAME \
        --severity_threshold=medium \
        --focus_areas=security,performance,maintainability \
        --exclude_files="node_modules/*,dist/*" \
        > review-results.json
    - cat review-results.json
  artifacts:
    paths:
      - review-results.json
    reports:
      junit: review-results.xml
    expire_in: 1 hour
  only:
    - merge_requests

quality-gate:
  stage: quality-gate
  image: alpine:latest
  dependencies:
    - code-review
  before_script:
    - apk add --no-cache jq
  script:
    - |
      critical_issues=$(jq -r '.summary.critical_issues' review-results.json)
      high_issues=$(jq -r '.summary.high_issues' review-results.json)
      overall_score=$(jq -r '.summary.overall_score' review-results.json)
      
      echo "Critical issues: $critical_issues"
      echo "High issues: $high_issues"
      echo "Overall score: $overall_score"
      
      if [ "$critical_issues" -gt 0 ]; then
        echo "❌ Quality gate failed: Critical issues found"
        exit 1
      fi
      
      if [ "$high_issues" -gt 3 ]; then
        echo "❌ Quality gate failed: Too many high severity issues"
        exit 1
      fi
      
      if [ "$(echo "$overall_score < 7.0" | bc)" -eq 1 ]; then
        echo "❌ Quality gate failed: Overall score too low"
        exit 1
      fi
      
      echo "✅ Quality gate passed"
  only:
    - merge_requests
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    
    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g @qodo/gen'
            }
        }
        
        stage('Code Review') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'
                    sh """
                        qodo -q --ci code_review \
                          --target_branch=${targetBranch} \
                          --severity_threshold=medium \
                          --focus_areas=security,performance \
                          --exclude_files="Jenkinsfile,*.md" \
                          > review-results.json
                    """
                    
                    def results = readJSON file: 'review-results.json'
                    
                    echo "Code Review Summary:"
                    echo "Overall Score: ${results.summary.overall_score}/10"
                    echo "Total Issues: ${results.summary.total_issues}"
                    echo "Critical Issues: ${results.summary.critical_issues}"
                    
                    if (results.summary.critical_issues > 0) {
                        error("Critical issues found in code review")
                    }
                    
                    // Set build description
                    currentBuild.description = "Score: ${results.summary.overall_score}/10, Issues: ${results.summary.total_issues}"
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    def results = readJSON file: 'review-results.json'
                    
                    if (results.summary.overall_score < 7.0) {
                        unstable("Code quality score below threshold")
                    }
                    
                    if (results.summary.high_issues > 5) {
                        unstable("Too many high severity issues")
                    }
                }
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'review-results.json', fingerprint: true
            
            script {
                def results = readJSON file: 'review-results.json'
                
                // Publish test results if available
                if (fileExists('review-results.xml')) {
                    publishTestResults testResultsPattern: 'review-results.xml'
                }
                
                // Send notification
                if (results.summary.critical_issues > 0) {
                    slackSend(
                        color: 'danger',
                        message: "🚨 Critical issues found in ${env.JOB_NAME} #${env.BUILD_NUMBER}"
                    )
                }
            }
        }
    }
}
```

## IDE Integration

### VS Code Tasks
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Code Review - Current Changes",
            "type": "shell",
            "command": "qodo",
            "args": [
                "code_review",
                "--include_suggestions=true"
            ],
            "group": {
                "kind": "test",
                "isDefault": true
            },
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared",
                "showReuseMessage": true,
                "clear": false
            },
            "problemMatcher": []
        },
        {
            "label": "Code Review - Security Focus",
            "type": "shell",
            "command": "qodo",
            "args": [
                "code_review",
                "--focus_areas=security",
                "--severity_threshold=high",
                "--exclude_files=*.test.js,*.spec.ts"
            ],
            "group": "test",
            "presentation": {
                "echo": true,
                "reveal": "always",
                "focus": false,
                "panel": "shared"
            }
        },
        {
            "label": "Code Review - Comprehensive",
            "type": "shell",
            "command": "qodo",
            "args": [
                "code_review",
                "--target_branch=main",
                "--focus_areas=security,performance,maintainability",
                "--include_suggestions=true",
                "--severity_threshold=medium"
            ],
            "group": "test"
        }
    ]
}
```

### IntelliJ IDEA External Tool
```xml
<tool name="Code Review" description="Run code review on current changes" showInMainMenu="true" showInEditor="true" showInProject="true" showInSearchPopup="true" disabled="false" useConsole="true" showConsoleOnStdOut="false" showConsoleOnStdErr="false" synchronizeAfterRun="true">
  <exec>
    <option name="COMMAND" value="qodo" />
    <option name="PARAMETERS" value="code_review --focus_areas=security,performance --include_suggestions=true" />
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
      - id: code-review
        name: Code review for staged changes
        entry: qodo
        args: [code_review, --severity_threshold=high, --focus_areas=security]
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

### Git Hook Script
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running code review on staged changes..."

# Run the code review
qodo -q --ci code_review --severity_threshold=high --focus_areas=security > /tmp/review-results.json

# Check if successful
if [ $? -ne 0 ]; then
    echo "❌ Code review failed"
    cat /tmp/review-results.json
    exit 1
fi

# Parse results
critical_issues=$(jq -r '.summary.critical_issues' /tmp/review-results.json 2>/dev/null || echo "0")
high_issues=$(jq -r '.summary.high_issues' /tmp/review-results.json 2>/dev/null || echo "0")
overall_score=$(jq -r '.summary.overall_score' /tmp/review-results.json 2>/dev/null || echo "0")

echo "Code Review Results:"
echo "  Critical Issues: $critical_issues"
echo "  High Issues: $high_issues"
echo "  Overall Score: $overall_score/10"

# Block commit if critical issues found
if [ "$critical_issues" -gt 0 ]; then
    echo "❌ Commit blocked: Critical security or quality issues found"
    echo "Please fix the following issues before committing:"
    jq -r '.issues[] | select(.severity == "critical") | "  - \(.file):\(.line) - \(.title)"' /tmp/review-results.json
    exit 1
fi

# Warn about high issues but allow commit
if [ "$high_issues" -gt 0 ]; then
    echo "⚠️  Warning: $high_issues high severity issues found"
    echo "Consider addressing these issues:"
    jq -r '.issues[] | select(.severity == "high") | "  - \(.file):\(.line) - \(.title)"' /tmp/review-results.json
fi

echo "✅ Code review passed"
exit 0
```

## Troubleshooting Examples

### Debug Mode
```bash
# Run with verbose output
qodo code_review --log=debug.log --severity_threshold=low

# Check the debug log
cat debug.log

# Save all output for analysis
qodo code_review > review-results.json 2> errors.log
```

### Common Issues and Solutions

#### No Changes Detected
```bash
# Check git status
git status

# Ensure you're in a git repository
git rev-parse --git-dir

# Check if target branch exists
git branch -a | grep main

# Force review of specific files
git add -A && qodo code_review
```

#### False Positives
```bash
# Adjust severity threshold
qodo code_review --severity_threshold=high

# Focus on specific areas only
qodo code_review --focus_areas=security

# Exclude problematic files
qodo code_review --exclude_files="legacy/*,vendor/*"
```

#### Performance Issues
```bash
# Exclude large files or directories
qodo code_review --exclude_files="dist/*,build/*,node_modules/*"

# Review smaller changesets
git add specific-file.js
qodo code_review

# Use specific focus areas
qodo code_review --focus_areas=security
```

## Output Examples

### Successful Review (No Issues)
```json
{
  "summary": {
    "total_issues": 0,
    "critical_issues": 0,
    "high_issues": 0,
    "medium_issues": 0,
    "low_issues": 0,
    "files_reviewed": 2,
    "overall_score": 10.0
  },
  "issues": [],
  "suggestions": [
    {
      "file": "src/utils.js",
      "type": "performance",
      "description": "Consider using Map instead of Object for frequent lookups",
      "implementation": "Replace object with new Map() for better performance"
    }
  ],
  "approved": true,
  "requires_changes": false
}
```

### Review with Critical Issues
```json
{
  "summary": {
    "total_issues": 3,
    "critical_issues": 1,
    "high_issues": 1,
    "medium_issues": 1,
    "low_issues": 0,
    "files_reviewed": 4,
    "overall_score": 6.5
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
    },
    {
      "file": "src/utils.js",
      "line": 15,
      "severity": "high",
      "category": "performance",
      "title": "Inefficient Loop",
      "description": "Nested loop with O(n²) complexity could be optimized",
      "suggestion": "Use Map or Set for faster lookups",
      "code_example": "const lookup = new Map(items.map(item => [item.id, item]));"
    },
    {
      "file": "src/config.js",
      "line": 8,
      "severity": "medium",
      "category": "maintainability",
      "title": "Hard-coded Configuration",
      "description": "Configuration values should be externalized",
      "suggestion": "Move to environment variables or config file"
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

### Review with Warnings Only
```json
{
  "summary": {
    "total_issues": 2,
    "critical_issues": 0,
    "high_issues": 0,
    "medium_issues": 1,
    "low_issues": 1,
    "files_reviewed": 3,
    "overall_score": 8.5
  },
  "issues": [
    {
      "file": "src/helpers.js",
      "line": 23,
      "severity": "medium",
      "category": "maintainability",
      "title": "Complex Function",
      "description": "Function has high cyclomatic complexity (12)",
      "suggestion": "Consider breaking into smaller functions"
    },
    {
      "file": "src/styles.css",
      "line": 45,
      "severity": "low",
      "category": "maintainability",
      "title": "Unused CSS Rule",
      "description": "CSS rule appears to be unused",
      "suggestion": "Remove unused styles to reduce bundle size"
    }
  ],
  "suggestions": [
    {
      "file": "src/helpers.js",
      "type": "refactoring",
      "description": "Extract validation logic into separate utility functions",
      "implementation": "Create validateInput(), sanitizeData(), and formatOutput() functions"
    }
  ],
  "approved": true,
  "requires_changes": false
}
```