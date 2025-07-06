# Diff Test Suite Agent

An intelligent test generation agent that analyzes code diffs and automatically generates comprehensive test suites covering all changed behaviors.

## Overview

This agent analyzes code changes in your repository and generates targeted test cases that:
- **Cover all modified functions and methods**
- **Test edge cases and error conditions**
- **Validate positive, negative, and boundary scenarios**
- **Follow project-specific testing patterns and frameworks**
- **Ensure no regressions in existing functionality**

## Features

- 🔍 **Smart Diff Analysis**: Automatically detects changed files and functions
- 🧪 **Comprehensive Test Generation**: Creates tests for all modified behaviors
- 🎯 **Framework Detection**: Adapts to your project's testing framework (Jest, pytest, JUnit, etc.)
- ✅ **Test Validation**: Runs generated tests to ensure they pass
- 📊 **Coverage Reporting**: Provides detailed summary of test coverage
- 🔧 **Configurable**: Customizable test directory and execution options

## Quick Start

### Basic Usage

```bash
# Generate tests for current working changes
qodo diff_test_suite

# Generate tests comparing current branch to main
qodo diff_test_suite --ignore_working_changes=true

# Generate tests with custom base branch
qodo diff_test_suite --base_branch=develop
```

### Advanced Configuration

```bash
# Comprehensive test generation with custom settings
qodo diff_test_suite \
  --base_branch=main \
  --test_directory=tests/generated \
  --files_to_ignore="*.config.js,*.d.ts" \
  --run_tests=true
```

## Configuration

The agent accepts the following parameters:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `files_to_ignore` | string | No | "" | Comma-separated list of files to ignore |
| `ignore_working_changes` | boolean | No | false | If true, compares current branch vs main instead of working changes |
| `base_branch` | string | No | "main" | Branch to compare against |
| `test_directory` | string | No | "" | Directory for generated tests (auto-detected if empty) |
| `run_tests` | boolean | No | true | Whether to run tests after generation |

## How It Works

### 1. Preparation Phase
- Uses Git to identify all changed files
- Analyzes specific lines and functions that were modified
- Reads file contents to understand the changes

### 2. Analysis Phase
- Understands new or altered behaviors in the code
- Identifies edge cases and potential failure points
- Plans comprehensive test scenarios

### 3. Implementation Phase
- Detects project's testing framework and patterns
- Generates well-structured, readable test code
- Places tests in appropriate directories

### 4. Validation Phase
- Runs each generated test file individually
- Debugs and fixes any failing tests
- Ensures all tests pass before completion

### 5. Completion Phase
- Runs full test suite to check for regressions
- Provides comprehensive summary and coverage report

## Output Format

The agent returns structured JSON output:

```json
{
  "summary": "Generated 15 test cases covering 8 modified functions across 3 files. All tests pass successfully with 100% coverage of changed code.",
  "generated_tests": [
    "tests/auth/test_login_service.py",
    "tests/utils/test_validation_helpers.py",
    "tests/api/test_user_controller.py"
  ],
  "test_results": {
    "passed": 15,
    "failed": 0,
    "failures": []
  },
  "success": true
}
```

## Framework Support

The agent automatically detects and supports various testing frameworks:

### JavaScript/TypeScript
- **Jest** - React, Node.js projects
- **Mocha** - Node.js applications
- **Jasmine** - Angular projects
- **Vitest** - Vite-based projects

### Python
- **pytest** - Modern Python testing
- **unittest** - Standard library testing
- **nose2** - Extended unittest

### Java
- **JUnit 5** - Modern Java testing
- **JUnit 4** - Legacy Java projects
- **TestNG** - Enterprise Java testing

### Other Languages
- **Go** - `go test` with testify
- **Rust** - Built-in test framework
- **C#** - xUnit, NUnit, MSTest
- **Ruby** - RSpec, Minitest
- **PHP** - PHPUnit

## Usage

### GitHub Actions

The most common way to use this agent is through GitHub Actions to automatically generate tests for pull requests:

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

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Generating tests for staged changes..."
qodo -q --ci diff_test_suite --run_tests=true

if [ $? -ne 0 ]; then
    echo "Test generation failed. Please review the changes."
    exit 1
fi

echo "Tests generated and validated successfully!"
```

### VS Code Task

```json
{
  "tasks": [
    {
      "label": "Generate Tests for Changes",
      "type": "shell",
      "command": "qodo",
      "args": ["diff_test_suite", "--run_tests=true"],
      "group": "test",
      "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
      },
      "problemMatcher": []
    }
  ]
}
```

## Best Practices

### 1. Regular Test Generation
- Run after implementing new features
- Use in pull request workflows
- Integrate with continuous integration

### 2. Review Generated Tests
- Always review generated tests before committing
- Ensure tests match your quality standards
- Add additional edge cases if needed

### 3. Test Directory Organization
- Use consistent test directory structure
- Mirror source code organization in tests
- Follow project naming conventions

### 4. Framework Configuration
- Ensure your testing framework is properly configured
- Install necessary dependencies before running
- Configure test runners in package.json or similar

## Troubleshooting

### Common Issues

**No tests generated:**
- Ensure there are actual code changes to analyze
- Check that changed files aren't in the ignore list
- Verify the base branch exists and is accessible

**Tests fail to run:**
- Check that testing framework dependencies are installed
- Verify test directory permissions
- Ensure test runner is properly configured

**Generated tests are low quality:**
- Review the source code changes for clarity
- Ensure functions have clear interfaces and documentation
- Consider adding more context in commit messages

### Debug Mode

```bash
# Generate tests with detailed logging
qodo diff_test_suite --log=debug.log

# Save output for analysis
qodo -q diff_test_suite > test-generation-results.json 2> debug.log
```

### Manual Test Directory

If auto-detection fails, specify the test directory:

```bash
# For Python projects
qodo diff_test_suite --test_directory=tests

# For JavaScript projects
qodo diff_test_suite --test_directory=__tests__

# For Java projects
qodo diff_test_suite --test_directory=src/test/java
```

## Examples

### Python Example

**Source Change:**
```python
# src/calculator.py
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Generated Test:**
```python
# tests/test_calculator.py
import pytest
from src.calculator import divide

class TestDivide:
    def test_divide_positive_numbers(self):
        result = divide(10, 2)
        assert result == 5.0
    
    def test_divide_negative_numbers(self):
        result = divide(-10, 2)
        assert result == -5.0
    
    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            divide(10, 0)
    
    def test_divide_zero_by_number(self):
        result = divide(0, 5)
        assert result == 0.0
```

### JavaScript Example

**Source Change:**
```javascript
// src/auth.js
export function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
```

**Generated Test:**
```javascript
// tests/auth.test.js
import { validateEmail } from '../src/auth.js';

describe('validateEmail', () => {
    test('should return true for valid email', () => {
        expect(validateEmail('user@example.com')).toBe(true);
    });
    
    test('should return false for email without @', () => {
        expect(validateEmail('userexample.com')).toBe(false);
    });
    
    test('should return false for email without domain', () => {
        expect(validateEmail('user@')).toBe(false);
    });
    
    test('should return false for empty string', () => {
        expect(validateEmail('')).toBe(false);
    });
    
    test('should return false for email with spaces', () => {
        expect(validateEmail('user @example.com')).toBe(false);
    });
});
```

## Requirements

- GitHub repository with appropriate permissions
- `GITHUB_TOKEN` with write access to contents and pull requests
- `QODO_API_KEY` for the Qodo platform, get one at [Qodo](https://qodo.ai)
- Repository should have the agent configuration file accessible
- Testing framework dependencies installed in the project

## Examples

See the [examples](examples/) directory for:
- Different GitHub Actions configurations
- Language-specific examples
- Testing framework integrations
- Custom agent configurations

## Contributing

Found an issue or want to improve this agent? Please see our [Contributing Guide](../../CONTRIBUTING.md).

### Reporting Issues
- Include the programming language and testing framework
- Provide sample code changes that reproduce the issue
- Include the generated test output and any error messages

### Suggesting Improvements
- Describe the enhancement and its benefits
- Provide examples of desired test generation behavior
- Consider compatibility with different testing frameworks

## License

This agent is part of the Qodo Agent Reference Implementations and is licensed under the MIT License.