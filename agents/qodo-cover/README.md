# Test Generation Agent

Automated test coverage bot for GitHub PRs - analyzes changes, generates meaningful passing tests, and creates follow-up PRs.

## Overview

This agent automatically generates tests for uncovered code changes in pull requests. It:
- Analyzes PR diffs to identify untested changes
- Learns from existing test patterns in your codebase
- Generates meaningful, passing tests following your conventions
- Creates a follow-up PR with the new tests
- Verifies test effectiveness using chaos engineering

## Features

- **Smart Coverage**: Only tests lines actually changed in the PR
- **Pattern Learning**: Analyzes existing tests to match your style
- **Chaos Testing**: Verifies tests actually catch bugs
- **Table-Driven Tests**: Groups related test cases efficiently
- **Multi-Language Support**: Auto-detects language and test framework
- **Quality Focus**: Prioritizes meaningful tests over quantity

## Configuration

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `desired_coverage` | number | No | 80 | Target coverage % for modified lines |

## Usage

### GitHub Actions

Trigger on PRs with the `qodo-cover` label:

```yaml
name: Test Generative Bot

on:
  pull_request:
    branches:
      - main
    types:
      - labeled
      - synchronize
      - reopened

permissions:
  pull-requests: write
  contents: write

jobs:
  coverage:
    if: |
      (
        (github.event.action == 'labeled' && contains(github.event.label.name, 'qodo-cover')) ||
        (github.event.action == 'synchronize' && contains(github.event.pull_request.labels.*.name, 'qodo-cover')) ||
        (github.event.action == 'reopened' && contains(github.event.pull_request.labels.*.name, 'qodo-cover'))
      ) &&
      github.event.pull_request.state == 'open' &&
      github.event.pull_request.draft == false
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.pull_request.head.sha }}
          fetch-depth: 0
        
      - name: Run Qodo Coverage Bot
        uses: qodo-ai/command@v1
        with:
          prompt: "qodo-cover"
          agent-file: "${{ github.workspace }}/.qodo/agents/qodo-cover.toml"
          key-value-pairs: |
            desired_coverage=80
        env:
          QODO_API_KEY: ${{ secrets.QODO_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PR_NUMBER: ${{ github.event.pull_request.number }}
```

## How It Works

1. **Analyzes PR Changes**: Identifies which files and lines were modified
2. **Learns Patterns**: Studies existing tests to understand your testing style
3. **Generates Tests**: Creates tests only for uncovered changed lines
4. **Verifies Quality**: Uses chaos engineering to ensure tests catch real bugs
5. **Opens Follow-up PR**: Creates a PR targeting your feature branch with new tests

## Requirements

- `QODO_API_KEY` from [Qodo](https://qodo.ai)
- `GITHUB_TOKEN` with write permissions
- Label PRs with `qodo-cover` to trigger

## Examples

See [examples/ci](examples/ci/) for the complete GitHub Actions workflow.