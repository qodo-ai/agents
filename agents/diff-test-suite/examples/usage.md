# Usage Examples

This document provides practical examples of using the Diff Test Suite Agent in various scenarios.

## Basic Usage

### Generate Tests for Current Changes
```bash
# Generate tests for all unstaged and staged changes
qodo diff_test_suite

# Generate tests but don't run them
qodo diff_test_suite --run_tests=false

# Generate tests with custom test directory
qodo diff_test_suite --test_directory=spec
```

### Compare Against Different Branches
```bash
# Compare current branch against develop
qodo diff_test_suite --base_branch=develop

# Always compare against main, ignoring working changes
qodo diff_test_suite --ignore_working_changes=true --base_branch=main

# Compare feature branch against main
git checkout feature/new-api
qodo diff_test_suite --base_branch=main
```

## Advanced Configuration

### Ignore Specific Files
```bash
# Ignore configuration and generated files
qodo diff_test_suite --files_to_ignore="*.config.js,dist/*,*.generated.ts"

# Ignore test files themselves
qodo diff_test_suite --files_to_ignore="*.test.js,*.spec.ts,__tests__/*"

# Ignore documentation and assets
qodo diff_test_suite --files_to_ignore="*.md,*.png,*.jpg,docs/*"
```

### Project-Specific Examples

#### Node.js/Express API
```bash
# Generate tests for API changes
qodo diff_test_suite \
  --test_directory=tests \
  --files_to_ignore="package-lock.json,node_modules/*" \
  --base_branch=main
```

#### Python Django Project
```bash
# Generate tests for Django app changes
qodo diff_test_suite \
  --test_directory=tests \
  --files_to_ignore="*.pyc,__pycache__/*,migrations/*" \
  --base_branch=develop
```

#### Java Spring Boot
```bash
# Generate tests for Spring Boot changes
qodo diff_test_suite \
  --test_directory=src/test/java \
  --files_to_ignore="target/*,*.class" \
  --base_branch=main
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
name: Diff Test Suite Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  generate-tests:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run diff test suite agent
        uses: qodo-ai/command@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          prompt: diff-test-suite
          agent-file: path/to/agent.toml
          key-value-pairs: |
            base_branch=${{ github.base_ref }}
            files_to_ignore=package-lock.json,*.md
            run_tests=true
```

### GitLab CI Pipeline
```yaml
stages:
  - test-generation
  - test-execution

generate-tests:
  stage: test-generation
  image: node:18
  before_script:
    - npm install -g @qodo/gen
  script:
    - |
      qodo -q --ci diff_test_suite \
        --base_branch=$CI_MERGE_REQUEST_TARGET_BRANCH_NAME \
        --files_to_ignore="node_modules/*,dist/*" \
        > test-results.json
    - cat test-results.json
    - |
      success=$(jq -r '.success' test-results.json)
      if [ "$success" != "true" ]; then
        echo "Test generation failed"
        exit 1
      fi
  artifacts:
    paths:
      - tests/
      - test-results.json
    expire_in: 1 hour
  only:
    - merge_requests

run-generated-tests:
  stage: test-execution
  image: node:18
  dependencies:
    - generate-tests
  script:
    - npm install
    - npm test
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
        
        stage('Generate Tests') {
            steps {
                script {
                    def baseBranch = env.CHANGE_TARGET ?: 'main'
                    sh """
                        qodo -q --ci diff_test_suite \
                          --base_branch=${baseBranch} \
                          --files_to_ignore="Jenkinsfile,*.md" \
                          > test-results.json
                    """
                    
                    def results = readJSON file: 'test-results.json'
                    if (!results.success) {
                        error("Test generation failed: ${results.summary}")
                    }
                    
                    echo "Generated ${results.generated_tests.size()} test files"
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                sh 'npm test'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'test-results.json', fingerprint: true
            publishTestResults testResultsPattern: 'test-results.xml'
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
            "label": "Generate Tests for Changes",
            "type": "shell",
            "command": "qodo",
            "args": [
                "diff_test_suite",
                "--run_tests=true"
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
            "label": "Generate Tests (No Run)",
            "type": "shell",
            "command": "qodo",
            "args": [
                "diff_test_suite",
                "--run_tests=false",
                "--test_directory=${workspaceFolder}/tests"
            ],
            "group": "test",
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

### IntelliJ IDEA External Tool
```xml
<tool name="Generate Tests" description="Generate tests for code changes" showInMainMenu="true" showInEditor="true" showInProject="true" showInSearchPopup="true" disabled="false" useConsole="true" showConsoleOnStdOut="false" showConsoleOnStdErr="false" synchronizeAfterRun="true">
  <exec>
    <option name="COMMAND" value="qodo" />
    <option name="PARAMETERS" value="diff_test_suite --test_directory=src/test/java" />
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
      - id: generate-tests
        name: Generate tests for changes
        entry: qodo
        args: [diff_test_suite, --run_tests=true]
        language: system
        pass_filenames: false
        always_run: true
```

### Git Hook Script
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Generating tests for staged changes..."

# Run the agent
qodo -q --ci diff_test_suite --run_tests=true > /tmp/test-results.json

# Check if successful
if [ $? -ne 0 ]; then
    echo "❌ Test generation failed"
    cat /tmp/test-results.json
    exit 1
fi

# Parse results
success=$(jq -r '.success' /tmp/test-results.json 2>/dev/null || echo "false")
generated_count=$(jq -r '.generated_tests | length' /tmp/test-results.json 2>/dev/null || echo "0")

if [ "$success" = "true" ]; then
    echo "✅ Generated $generated_count test files successfully"
    
    # Stage any new test files
    git add tests/ 2>/dev/null || true
    
    exit 0
else
    echo "❌ Test generation or execution failed"
    jq -r '.summary' /tmp/test-results.json 2>/dev/null || echo "Unknown error"
    exit 1
fi
```

## Troubleshooting Examples

### Debug Mode
```bash
# Run with verbose output
qodo diff_test_suite --log=debug.log --run_tests=false

# Check the debug log
cat debug.log

# Save all output for analysis
qodo diff_test_suite > results.json 2> errors.log
```

### Common Issues and Solutions

#### No Changes Detected
```bash
# Check git status
git status

# Ensure you're in a git repository
git rev-parse --git-dir

# Check if base branch exists
git branch -a | grep main
```

#### Test Framework Not Detected
```bash
# Manually specify test directory
qodo diff_test_suite --test_directory=tests

# Check existing test files
find . -name "*.test.*" -o -name "*.spec.*"

# Verify package.json or requirements.txt
cat package.json | jq '.devDependencies'
cat requirements.txt | grep -i test
```

#### Generated Tests Fail
```bash
# Generate without running
qodo diff_test_suite --run_tests=false

# Check generated test syntax
npx eslint tests/
python -m py_compile tests/*.py

# Run tests manually
npm test
pytest tests/
```

## Output Examples

### Successful Generation
```json
{
  "summary": "Generated 12 test cases covering 5 modified functions across 3 files. All tests pass successfully with comprehensive coverage of edge cases and error conditions.",
  "generated_tests": [
    "tests/auth/login.test.js",
    "tests/api/users.test.js",
    "tests/utils/validation.test.js"
  ],
  "test_results": {
    "passed": 12,
    "failed": 0,
    "failures": []
  },
  "success": true
}
```

### Partial Failure
```json
{
  "summary": "Generated 8 test cases but 2 tests failed due to missing mock dependencies. Manual review required for complete test suite.",
  "generated_tests": [
    "tests/service/payment.test.js",
    "tests/model/user.test.js"
  ],
  "test_results": {
    "passed": 6,
    "failed": 2,
    "failures": [
      "tests/service/payment.test.js: ReferenceError: PaymentGateway is not defined",
      "tests/model/user.test.js: TypeError: Cannot read property 'findById' of undefined"
    ]
  },
  "success": false
}
```