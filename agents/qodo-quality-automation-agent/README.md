# Quality Automation Agent 

**Comprehensive code quality automation for the entire SDLC**

Orchestrates security scanning, code review, license compliance, dependency health checks, test coverage analysis, and code quality metrics in both local and CI/CD environments. Execute automated quality gates with intelligent reporting and actionable recommendations.

## Features

- **🔍 Multi-Stage Quality Pipeline**: Orchestrates 6+ quality checks automatically across your entire codebase
- **🛡️ Security First**: Vulnerability scanning, secret detection, and dependency security analysis
- **📜 License Compliance**: Automated license compatibility checks with configurable allow/block lists
- **📊 Dependency Health**: Real-time package health assessment using Snyk Advisor data
- **📈 Code Quality Metrics**: Maintainability index, technical debt, and code duplication analysis
- **🔄 CI/CD Ready**: Native GitHub Actions integration with PR comments and status checks
- **🎨 Flexible Reporting**: Generate comprehensive reports in Markdown, JSON, or HTML formats
- **⚙️ Smart Quality Gates**: Configurable thresholds for blocking vs warning based on severity levels
- **🚫 Zero Configuration**: Works out-of-the-box with sensible defaults for most projects

---

### ✅ Workflow Integration

**Seamless integration across the SDLC:**

- **Local Development**: Run checks before committing
- **Pre-commit Hooks**: Prevent bad code from being pushed
- **CI/CD Pipelines**: Automated quality gates on every PR
- **GitHub Integration**: PR comments, status checks, and artifacts
- **Cross-tool Orchestration**: Git, Qodo Merge, Shell, GitHub MCP

**Triggers where work happens:**

- Git hooks for local validation
- GitHub Actions on PR creation/update
- Manual CLI execution for deep analysis
- Scheduled runs for continuous monitoring

## 🚀 Quick Start

```bash
# Quick Start 
qodo quality_automation

# Analyze code quality in your project
qodo --agent-file=agent.toml quality_automation --set mode=local

# Run with custom coverage threshold
qodo --agent-file=agent.toml quality_automation --set min_coverage=90

# Security-focused scan with strict thresholds
qodo --agent-file=agent.toml quality_automation \
  --set severity_threshold=critical \
  --set allowed_licenses="MIT,Apache-2.0"

# CI mode with strict quality gates
qodo --agent-file=agent.toml quality_automation \
  --set mode=ci \
  --set min_coverage=90 \
  --set severity_threshold=critical \
  --set fail_on_warnings=true
```

## Configuration

### Arguments

| Argument                | Type    | Required | Default                                          | Description                                                      |
| ----------------------- | ------- | -------- | ------------------------------------------------ | ---------------------------------------------------------------- |
| `mode`                  | string  | ❌       | `"auto"`                                         | Execution mode: `local`, `ci`, or `auto` (auto-detect)           |
| `target_branch`         | string  | ❌       | `"main"`                                         | Target branch to compare against                                 |
| `min_coverage`          | number  | ❌       | `80`                                             | Minimum code coverage percentage (0-100)                         |
| `severity_threshold`    | string  | ❌       | `"high"`                                         | Minimum severity to fail CI: `low`, `medium`, `high`, `critical` |
| `allowed_licenses`      | string  | ❌       | `"MIT,BSD-2-Clause,BSD-3-Clause,Apache-2.0,ISC"` | Comma-separated allowed licenses                                 |
| `blocked_licenses`      | string  | ❌       | `"GPL-3.0,AGPL-3.0,SSPL-1.0"`                    | Comma-separated blocked licenses                                 |
| `skip_tests`            | boolean | ❌       | `false`                                          | Skip test execution and coverage analysis                        |
| `skip_dependencies`     | boolean | ❌       | `false`                                          | Skip dependency health checks                                    |
| `output_format`         | string  | ❌       | `"markdown"`                                     | Report format: `markdown`, `json`, `html`                        |
| `fail_on_warnings`      | boolean | ❌       | `false`                                          | Fail CI even on non-critical warnings                            |
| `create_github_comment` | boolean | ❌       | `true`                                           | Post results as GitHub PR comment (CI mode only)                 |
| `focus_files`           | string  | ❌       | `""`                                             | Comma-separated list of files to focus analysis on               |

## Prerequisites

### System Requirements

- Node.js 18+ (for Qodo CLI)
- Git repository
- Package manager

### Installation

```bash
# Install Qodo CLI globally
npm install -g @qodo/command

# Set up required environment variables
export QODO_API_KEY="your-qodo-api-key"  # Get from https://qodo.ai
export GITHUB_PERSONAL_ACCESS_TOKEN="your-github-token"  # For CI mode
```

## Quality Pipeline Overview

The Quality Automation Agent executes a comprehensive 8-stage pipeline:

### 🔍 Stage 1: Environment Detection

- Detects CI/CD environment vs local development
- Identifies changed files since target branch
- Sets quality thresholds based on environment

### 🛡️ Stage 2: Code Review & Static Analysis

- Uses Qodo Merge for intelligent code analysis
- Detects security vulnerabilities, code smells, performance issues
- Generates severity-categorized findings

### 🔒 Stage 3: Security Scanning

- Scans dependencies for known vulnerabilities
- Checks for hardcoded secrets and credentials
- Verifies secure coding practices with CVE references

### 📜 Stage 4: License Compliance

- Scans all dependencies (direct and transitive)
- Compares against allowed/blocked license lists
- Identifies copyleft risks and compatibility issues

### 📊 Stage 5: Dependency Health Assessment

- Analyzes package health using Snyk Advisor data
- Checks for deprecated packages and maintenance status
- Suggests alternatives for risky dependencies

### ✅ Stage 6: Test Coverage Analysis

- Runs existing test suites and calculates coverage metrics
- Identifies untested code paths
- Enforces minimum coverage requirements

### 📈 Stage 7: Code Quality Metrics

- Calculates maintainability index and technical debt
- Analyzes code duplication and documentation coverage
- Measures code churn and volatility

### 📋 Stage 8: Reporting & Integration

- Generates comprehensive reports in multiple formats
- Creates actionable fix recommendations
- Posts GitHub PR comments in CI mode

## Output Reports

The agent generates exactly 3 files in the `report/` directory:

### 📊 `report/quality-metrics.json`

Complete metrics and scores with structured data for automation:

```json
{
  "overall_quality_score": 85,
  "safe_to_merge": true,
  "execution_mode": "ci",
  "stages": {
    "security_scan": { "status": "passed", "vulnerabilities": [] },
    "license_compliance": { "status": "passed", "violations": [] },
    "test_coverage": { "status": "passed", "coverage_percent": 87 }
  },
  "merge_recommendation": "APPROVE"
}
```

### 📝 `report/key-findings.md`

Executive summary with critical issues and quality metrics:

```markdown
# Quality Automation - Key Findings

## 🔍 Executive Summary

- Overall Quality Score: 85/100
- Merge Status: ✅ SAFE

## � Critical Issues (Blockers)

No critical issues found.

## 📊 Quality Metrics

- Security: 0 vulnerabilities found
- License: 0 compliance issues
- Coverage: 87% (threshold: 80%)
```

### ✅ `report/actions-required.md`

Actionable recommendations and merge decision:

```markdown
# Actions Required for Quality Improvement

## 🚨 IMMEDIATE ACTIONS (Before Merge)

No critical actions required.

## 📈 RECOMMENDED IMPROVEMENTS

- [ ] Increase test coverage for UserService class (current: 72%)
- [ ] Consider updating lodash to latest version for security patches

## 📋 MERGE DECISION

**Status**: ✅ APPROVED
```

---

## Examples

### Test with a Sample Project

```bash
# Clone a test repository
git clone https://github.com/example/sample-js-project
cd sample-js-project

# Run basic quality check
qodo --agent-file=agent.toml quality_automation

# Run with focused analysis on specific files
qodo --agent-file=agent.toml quality_automation \
  --set focus_files="src/auth.js,src/api.js"

```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Quality Automation
on: [pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"

      - name: Install Qodo CLI
        run: npm install -g @qodo/command

      - name: Run Quality Automation
        run: |
          qodo --agent-file=agent.toml quality_automation \
            --set mode=ci \
            --set target_branch=${{ github.base_ref }} \
            --set create_github_comment=true
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Upload Reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: quality-reports
          path: report/
```

## Quality Scoring System

### 🟢 High Quality (Score: 80-100)

- **Security**: No critical/high vulnerabilities
- **Coverage**: Meets or exceeds threshold (default 80%)
- **License**: All dependencies use allowed licenses
- **Dependencies**: All packages healthy, no deprecated/risky ones
- **Code Quality**: Low technical debt, good maintainability

### 🟡 Moderate Quality (Score: 60-79)

- **Security**: Some medium vulnerabilities, no critical issues
- **Coverage**: Slightly below threshold but acceptable
- **License**: Minor compliance issues with non-critical dependencies
- **Dependencies**: Some packages need updates but not risky
- **Code Quality**: Moderate technical debt, room for improvement

### 🔴 Low Quality (Score: 0-59)

- **Security**: Critical/high vulnerabilities present
- **Coverage**: Significantly below minimum threshold
- **License**: Blocked licenses or major compliance issues
- **Dependencies**: Deprecated, unmaintained, or risky packages
- **Code Quality**: High technical debt, maintainability concerns

---

## Tools

This agent uses the following tools:

- **Qodo Merge**: Code review and improvement suggestions
- **Git**: Repository analysis and change detection
- **Filesystem**: Configuration and dependency scanning
- **Shell**: Test execution and coverage calculation
- **GitHub MCP**: PR comments and status updates (CI mode)

---

## License

See top-level [LICENSE](https://github.com/qodo-ai/agents/blob/main/LICENSE) file for details.

## Support

- 📚 [Qodo Documentation](https://docs.qodo.ai/qodo-documentation/qodo-command)
- 💬 [Discord Community](https://discord.gg/qodo)
- 🐛 [Report Issues](https://github.com/qodo-ai/agents/issues)

## Contributing
Follow [Contributing guidelines](https://github.com/qodo-ai/agents/blob/main/CONTRIBUTING.md).
