# Usage Examples — Reliability Guardian Agent

This document provides usage instructions and integration examples for the **Reliability Guardian Agent** — a Qodo agent that evaluates project reliability, test robustness, and historical stability trends.

---

## Basic Usage

### Analyze Current Project
```bash
# Run a full reliability analysis on the current branch(main)
qodo reliability_guardian
```

### Compare Against a Specific Branch
```bash
qodo reliability_guardian --target_branch=develop
```

### Limit Historical Commits for Trend Tracking
```bash
qodo reliability_guardian --max_commits=3
```

### Disable Certain Tests
```bash
# Disable mutation testing
qodo reliability_guardian --mutation_testing=false

# Disable fuzz testing
qodo reliability_guardian --fuzz_testing=false
```

### Exclude Files or Directories
```bash
qodo reliability_guardian --exclude_files="tests/mocks/*,migrations/*"
```

## ⚙️ Advanced Examples

### Node.js / Express API
```bash
qodo reliability_guardian \
  --target_branch=main \
  --exclude_files="node_modules/*,dist/*" \
  --mutation_testing=true \
  --fuzz_testing=true
```

### Python (Django / FastAPI)
```bash
qodo reliability_guardian \
  --target_branch=develop \
  --max_commits=5 \
  --exclude_files="*.pyc,__pycache__/*,migrations/*"
```

### Java / Spring Boot 
```bash
qodo reliability_guardian \
  --target_branch=main \
  --exclude_files="target/*,*.class"
```

## 🧪 Output Schema

```json
{
  "summary": {
    "files_analyzed": 4,
    "functions_checked": 8,
    "total_issues": 18,
    "critical_issues": 3,
    "reliability_score": {
      "overall": 3.5,
      "logic_consistency": 4.0,
      "validation_coverage": 3.0,
      "exception_safety": 4.0,
      "test_strength": 3.0
    },
    "trend": {
      "previous_scores": [2.2],
      "improvement": 1.3,
      "best_commit": "065f7c9",
      "worst_commit": "be1abae"
    }
  },
  "issues": [
    {
      "file": "src/payment.py",
      "line": 1,
      "severity": "critical",
      "category": "logic_conflict",
      "description": "Premium users get worse discount (15%) when amount > 100 compared to base premium discount (20%). This is a business logic contradiction.",
      "suggestion": "Invert the logic so higher amounts get better discounts (e.g., 25% for amount > 100, 20% otherwise)",
      "code_patch": "if user_type == 'premium':\n    discount = 0.25 if amount > 100 else 0.20"
    },
    {
      "file": "src/calculator.py",
      "line": 10,
      "severity": "critical",
      "category": "exception_risk",
      "description": "average() function will raise ZeroDivisionError when passed an empty list",
      "suggestion": "Add validation to check for empty input before division",
      "code_patch": "if values is None or len(values) == 0:\n    raise ValueError('values must be a non-empty sequence')"
    },
    {
      "file": "src/utils.py",
      "line": 1,
      "severity": "critical",
      "category": "exception_risk",
      "description": "safe_get() catches all exceptions with 'except Exception', masking programming errors and making debugging difficult",
      "suggestion": "Only catch specific exceptions (KeyError, TypeError) to avoid hiding unrelated bugs",
      "code_patch": "except (KeyError, TypeError):\n    return default"
    },
    {
      "file": "src/auth.py",
      "line": 5,
      "severity": "high",
      "category": "validation_gap",
      "description": "authenticate_user() accepts any types without validation; no None/empty checks",
      "suggestion": "Add type and empty string validation before authentication logic",
      "code_patch": "if not isinstance(username, str) or not isinstance(password, str):\n    return False\nif not username or not password:\n    return False"
    },
    {
      "file": "src/payment.py",
      "line": 1,
      "severity": "high",
      "category": "validation_gap",
      "description": "calculate_discount() lacks input validation for user_type domain and amount (negative values, type checking)",
      "suggestion": "Add validation for user_type and amount before processing",
      "code_patch": "if not isinstance(amount, (int, float)) or amount < 0:\n    raise ValueError('amount must be a non-negative number')\nif user_type not in ('premium', 'basic'):\n    raise ValueError(f'invalid user_type: {user_type}')"
    },
    {
      "file": "src/calculator.py",
      "line": 10,
      "severity": "high",
      "category": "validation_gap",
      "description": "average() lacks validation for non-numeric elements in the list",
      "suggestion": "Add type checking for all elements before processing",
      "code_patch": "if not all(isinstance(x, (int, float)) for x in values):\n    raise TypeError('all values must be numeric')"
    },
    {
      "file": "src/calculator.py",
      "line": 15,
      "severity": "medium",
      "category": "validation_gap",
      "description": "add_safe() has misleading name suggesting validation, but performs no type enforcement; will concatenate strings or raise TypeError with None",
      "suggestion": "Either add type validation or rename function to reflect actual behavior"
    },
    {
      "file": "tests/test_auth.py",
      "line": 6,
      "severity": "high",
      "category": "weak_test",
      "description": "test_auth_admin expects authenticate_user('admin','123') to return True, but actual implementation requires password 'secret'. Test is failing.",
      "suggestion": "Fix test to match actual implementation or fix implementation to match test contract",
      "code_patch": "def test_auth_success():\n    assert authenticate_user('admin', 'secret') is True"
    },
    {
      "file": "tests/test_auth.py",
      "line": 1,
      "severity": "high",
      "category": "weak_test",
      "description": "test_email_valid only tests happy path; missing tests for invalid emails, None, empty strings",
      "suggestion": "Add negative test cases for malformed emails",
      "code_patch": "def test_email_invalid_cases():\n    assert not validate_email('')\n    assert not validate_email('invalid')\n    assert not validate_email('a@b.')\n    assert not validate_email('@example.com')"
    }
  ],
  "suggestions": [
    {
      "area": "logic",
      "description": "Fix payment discount logic contradiction where premium users get worse discount for higher amounts. Invert the condition so amount > 100 gets 25% discount instead of 15%.",
      "example_patch": "if user_type == 'premium':\n    discount = 0.25 if amount > 100 else 0.20\nelse:\n    discount = 0.10"
    },
    {
      "area": "validation",
      "description": "Add comprehensive input validation across all functions: type checking, None checks, empty collection checks, domain validation for enums, and range validation for numeric inputs.",
      "example_patch": "if not isinstance(amount, (int, float)) or amount < 0:\n    raise ValueError('amount must be a non-negative number')\nif user_type not in ('premium', 'basic'):\n    raise ValueError(f'invalid user_type: {user_type}')"
    },
    {
      "area": "error_handling",
      "description": "Replace broad 'except Exception' clauses with specific exception types to avoid masking programming errors. Only catch expected exceptions like KeyError, TypeError, ValueError.",
      "example_patch": "try:\n    return d[key]\nexcept (KeyError, TypeError):\n    return default"
    },
    {
      "area": "validation",
      "description": "Strengthen email validation to reject malformed patterns like 'a@b.', '@example.com', 'a@@b.com'. Implement proper parsing with split and validation of local/domain parts.",
      "example_patch": "local, domain = email.split('@', 1)\nif not local or '.' not in domain:\n    return False\nlabel, tld = domain.rsplit('.', 1)\nreturn bool(label) and len(tld) >= 2"
    },
    {
      "area": "testing",
      "description": "Expand test coverage to include edge cases and negative tests: empty inputs, None values, type errors, boundary conditions, and invalid domain values. Fix failing test in test_auth_admin.",
      "example_patch": "def test_auth_failures():\n    assert authenticate_user('admin', 'wrong') is False\n    assert authenticate_user('', 'secret') is False\n    assert authenticate_user(None, 'secret') is False"
    },
    {
      "area": "testing",
      "description": "Implement mutation testing to measure test effectiveness. Current tests likely have weak mutation kill rate due to minimal assertions and lack of negative tests.",
      "example_patch": "# Run mutation testing with mutmut:\n# mutmut run --paths-to-mutate=src/\n# Expected improvement: mutation score from ~30% to >80% after adding edge case tests"
    }
  ],
  "approved": false,
  "requires_changes": true
}
```

## 🧰 CI/CD Integrations

### GitHub Actions

```yaml
name: Reliability Guardian Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  reliability-check:
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

      - name: Run Reliability Guardian
        uses: qodo-ai/command@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
        with:
          prompt: reliability_guardian
          agent-file: path/to/agent.toml
          key-value-pairs: |
            target_branch=${{ github.base_ref }}
            max_commits=5
            mutation_testing=true
            fuzz_testing=true
            exclude_files=node_modules/*,*.md
```

### 🚀 GitLab CI – Reliability Analysis + Quality Gate

```yaml
stages:
  - reliability-analysis
  - quality-gate

reliability-guardian:
  stage: reliability-analysis
  image: node:18
  before_script:
    - npm install -g @qodo/gen
  script:
    - |
      echo "🧠 Running Reliability Guardian Agent..."
      qodo -q --ci reliability_guardian \
        --target_branch=${CI_MERGE_REQUEST_TARGET_BRANCH_NAME:-main} \
        --max_commits=5 \
        --mutation_testing=true \
        --fuzz_testing=true \
        --exclude_files="node_modules/*,dist/*,migrations/*"
  only:
    - merge_requests

quality-gate:
  stage: quality-gate
  image: alpine:latest
  before_script:
    - apk add --no-cache jq
  script:
    - |
      echo "📊 Evaluating reliability quality gate..."
      # You can parse console output if redirected, or rely on reliability score
      overall_score=$(grep -Eo '"overall": [0-9]+\.[0-9]+' reliability.log | grep -Eo '[0-9]+\.[0-9]+')
      if [ -z "$overall_score" ]; then
        echo "⚠️ Could not determine reliability score. Skipping gate."
        exit 0
      fi
      echo "Detected Reliability Score: $overall_score"
      if (( $(echo "$overall_score < 7.0" | bc -l) )); then
        echo "❌ Quality gate failed: Reliability score below 7.0"
        exit 1
      fi
      echo "✅ Reliability check passed with score $overall_score"
  dependencies:
    - reliability-guardian
  only:
    - merge_requests

```

> 💡 This version reads the reliability score directly from console output instead of JSON. You can redirect output with > reliability.log if you’d like to parse it explicitly.

### 🧩 Jenkins Pipeline – Reliability Scoring & Gate

```bash
// Jenkins Pipeline for Reliability Guardian Agent with Quality Gate
pipeline {
    agent any

    environment {
        QODO_API_KEY = credentials('qodo-api-key')
        GITHUB_TOKEN = credentials('github-token')
    }

    stages {
        stage('Setup') {
            steps {
                sh 'npm install -g @qodo/gen || true'
            }
        }

        stage('Reliability Analysis') {
            steps {
                script {
                    def targetBranch = env.CHANGE_TARGET ?: 'main'
                    // Run agent and log output
                    sh """
                      echo "🔍 Running Reliability Guardian Agent..."
                      qodo -q --ci reliability_guardian \
                        --target_branch=${targetBranch} \
                        --max_commits=5 \
                        --mutation_testing=true \
                        --fuzz_testing=true \
                        --exclude_files="node_modules/*,dist/*,migrations/*" \
                        > reliability.log
                    """
                    sh 'cat reliability.log'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                script {
                    def logContent = readFile('reliability.log')
                    def matcher = (logContent =~ /"overall":\s*([0-9]+(\.[0-9]+)?)/)
                    def score = matcher ? matcher[0][1].toFloat() : 0.0
                    echo "Detected Reliability Score: ${score}"
                    if (score < 7.0) {
                        error("❌ Quality Gate Failed: Reliability score below threshold (${score})")
                    } else {
                        echo "✅ Reliability Passed: Score ${score}"
                    }
                }
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reliability.log', fingerprint: true
        }
    }
}
```

⚙️ **Thresholds:**

- Fail below 7.0 reliability

- You can raise it for stricter standards (>= 8.0 for production).

## IDE Integration

### 🧑‍💻 VS Code Integration

```json
{
  "version": "1.0.0",
  "tasks": [
    {
      "label": "Reliability Guardian - Full Analysis",
      "type": "shell",
      "command": "qodo",
      "args": [
        "reliability_guardian",
        "--target_branch=main",
        "--max_commits=5",
        "--mutation_testing=true",
        "--fuzz_testing=true"
      ],
      "group": "test",
      "presentation": {
        "reveal": "always"
      }
    },
    {
      "label": "Reliability Guardian - Quick Trend Check",
      "type": "shell",
      "command": "qodo",
      "args": [
        "reliability_guardian",
        "--max_commits=3"
      ],
      "group": "test"
    }
  ]
}
```

### IntelliJ IDEA External Tool
```xml
<tool name="Reliability Guardian" description="Analyze project reliability, logic consistency, and test robustness" showInMainMenu="true" showInEditor="true" showInProject="true" showInSearchPopup="true" disabled="false" useConsole="true" synchronizeAfterRun="true">
  <exec>
    <option name="COMMAND" value="qodo" />
    <option name="PARAMETERS" value="reliability_guardian --max_commits=5 --mutation_testing=true --fuzz_testing=true" />
    <option name="WORKING_DIRECTORY" value="$ProjectFileDir$" />
  </exec>
</tool>
```

## 🪝 Pre-commit Hook

### Using pre-commit Framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: reliability-guardian
        name: Run Reliability Guardian Analysis
        entry: qodo
        args: [reliability_guardian, --max_commits=3, --mutation_testing=true]
        language: system
        pass_filenames: false
        always_run: true
        stages: [commit]
```

### Git Hook Script

```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "🧩 Running Reliability Guardian Agent..."
qodo -q --ci reliability_guardian --max_commits=3 --mutation_testing=true --fuzz_testing=true > /tmp/reliability.log
if [ $? -ne 0 ]; then
    echo "❌ Reliability check failed"
    cat /tmp/reliability.log
    exit 1
fi

score=$(grep -Eo '"overall": [0-9]+\.[0-9]+' /tmp/reliability.log | grep -Eo '[0-9]+\.[0-9]+')
echo "Reliability Score: $score"

if (( $(echo "$score < 7.0" | bc -l) )); then
  echo "❌ Reliability gate failed — score below 7.0"
  exit 1
fi

echo "✅ Reliability check passed!"
exit 0
```

