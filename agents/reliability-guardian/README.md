# 🛡️ Reliability Guardian Agent

A specialized Qodo AI Agent that evaluates and safeguards your project’s code reliability through deep analysis of logic consistency, validation coverage, test strength, and historical stability trends.

## 🧭 Overview

The **Reliability Guardian Agent** ensures your software remains robust and dependable by performing a multi-dimensional reliability analysis, including:

- ⚙️ **Logic Consistency**: Detects contradictions, redundant branches, and unsafe operations

- 🧩 **Validation Coverage**: Identifies missing or weak input validation

- 🧠 **Exception Safety**: Evaluates exception handling and fail-safes

- 🧪 **Test Effectiveness**: Simulates mutation or fuzz testing to assess test resilience

- 📈 **Historical Reliability Trend**: Tracks and compares reliability scores across commits

This agent is perfect for teams aiming to maintain high reliability standards and track software stability evolution over time.

## ✨ Features

- 🔍 **Automated Reliability Audit**: Scans code for logical flaws, validation gaps, and unsafe behavior

- 🧪 **Test Robustness Simulation**: Virtually “mutates” or “fuzzes” code paths to estimate test coverage quality

- 📊 **Comprehensive Reliability Scoring**: Calculates sub-scores for logic, validation, safety, and test effectiveness

- 🕒 **Historical Trend Tracking**: Analyzes recent commits to detect improvements or regressions

- 💡 **Actionable Fix Suggestions**: Generates targeted code patches and recommendations

- 🧰 **CI/CD Ready**: Works with GitHub Actions, GitLab CI, Jenkins, and Azure Pipelines


## 🚀 Quick Start

**Run reliability analysis locally**
```bash
qodo reliability_guardian
```

**Compare with another branch**
```bash
qodo reliability_guardian --target_branch=develop
```

**Analyze last 10 commits for reliability trend**
```bash
qodo reliability_guardian --max_commits=10
```

**Run without mutation or fuzz simulation**
```bash
qodo reliability_guardian --mutation_testing=false --fuzz_testing=false
```

## ⚙️ Configuration
The agent accepts the following parameters:

| Parameter          | Type    | Required | Default  | Description                                                           |
| ------------------ | ------- | -------- | -------- | --------------------------------------------------------------------- |
| `target_branch`    | string  | No       | `master` | Branch to compare for reliability diff and trend analysis             |
| `max_commits`      | number  | No       | `5`      | Number of recent commits to analyze for reliability trends            |
| `mutation_testing` | boolean | No       | `true`   | Enable simulated mutation testing                                     |
| `fuzz_testing`     | boolean | No       | `true`   | Enable simulated fuzz reliability probing                             |
| `exclude_files`    | string  | No       | -        | Comma-separated list of files to exclude (e.g. mocks, generated code) |


## Output Format

The agent returns structured JSON output:

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

## 🧰 Tools Used
This agent uses the following tools from the Qodo ecosystem:

- 🧠 **qodo_merge** – Merges and compares reliability context from diffs and commits

- 📂 **filesystem** – Reads source and test files for structure and coverage simulation

- 🐙 **git** – Extracts commit metadata and history for trend analysis

## 🧑‍💻 Usage Examples

### GitHub Actions (Pull Request Reviews)

The most common way to use this agent is through GitHub Actions to automatically review pull requests:

```yaml
name: Reliability Guardian Agent
on:
  pull_request:
    branches: [main, develop]

jobs:
  reliability-guardian:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      checks: write

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Run Reliability Guardian Agent
        uses: qodo-ai/command@v1
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          prompt: reliability_guardian
          agent-file: path/to/agent.toml
          key-value-pairs: |
            target_branch=${{ github.base_ref }}
            max_commits=5
            mutation_testing=true
            fuzz_testing=true

```
### Pre-commit Hook
```bash
#!/bin/bash
echo "Running Reliability Guardian Agent..."
qodo reliability_guardian

if [ $? -ne 0 ]; then
    echo "❌ Reliability check failed. Please fix the issues before committing."
    exit 1
fi

echo "✅ Code looks great!"
```

### VS Code Integration

```json
{
  "label": "Qodo Reliability Guardian Agent",
  "type": "shell",
  "command": "qodo",
  "args": ["reliability_guardian"],
  "group": "build",
  "presentation": {
    "echo": true,
    "reveal": "always",
    "panel": "shared"
  }
}
```

## 🔑 Requirements

- GitHub repository with appropriate permissions
- `GITHUB_TOKEN` with read access to contents and write access to pull requests and checks
- `QODO_API_KEY` get one at [Qodo](https://qodo.ai)
- Repository should have the agent configuration file accessible

## 🧱 Examples

You can find example setups in the `examples/` folder:

- CI/CD pipelines

- Pre-commit setup

- IDE task runners

- Custom configuration templates

## 📜 License
MIT License.