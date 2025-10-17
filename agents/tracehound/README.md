# TraceHound - Observability Enforcement Agent

Language-agnostic observability enforcement agent that verifies critical API paths have proper logging, tracing, error handling, and metrics collection.

## Overview

TraceHound is an observability guard agent that enforces observability contracts across backend API code. It verifies that critical API endpoints have proper observability signals at every step of a request's code flow, helping you identify missing instrumentation before it becomes a production problem.

## Features

- **Multi-Language Support**: Built-in patterns for TypeScript, JavaScript, Python, Java, Go, Rust, and C#
- **Contract-Based Verification**: Define observability contracts for your critical API endpoints
- **Code Flow Analysis**: Traces request paths through multiple layers (controllers, services, DAL, middleware)
- **Pattern Detection**: Automatically detects logging, tracing, error handling, and metrics instrumentation
- **Actionable Reports**: Generates detailed violation reports with specific recommendations
- **Configurable Severity**: Filter violations by severity level (CRITICAL, HIGH, MEDIUM, LOW)
- **Safe Analysis**: Read-only static analysis that never modifies your code
- **Auto-Configuration**: Creates template config file if none exists

## Quick Start

### First Run - Create Config

```bash
# Run the agent - it will create observe-config.json template
qodo tracehound
# Output: ✅ Created observe-config.json - Please edit it to define your API monitoring contracts and re-run the agent.
```

### Edit Config

Open `observe-config.json` and define your critical API endpoints:

```json
{
  "metadata": {
    "language": "typescript"
  },
  "contracts": [
    {
      "id": "create-order",
      "name": "POST /api/orders - Create Order",
      "enabled": true,
      "code_flow": [
        {
          "layer": "controller",
          "file_pattern": "src/api/orders.ts",
          "signals": ["logging", "error_handling"]
        },
        {
          "layer": "service",
          "file_pattern": "src/services/orderService.ts",
          "signals": ["logging", "error_handling", "metrics"]
        },
        {
          "layer": "dal",
          "file_pattern": "src/dal/orders.ts",
          "signals": ["logging", "error_handling"]
        }
      ]
    }
  ]
}
```

### Run Analysis

```bash
# Run with default settings (TypeScript, MEDIUM threshold, fail on violations)
qodo tracehound

# Analyze Python project
qodo tracehound --language=python

# Only show HIGH and CRITICAL violations
qodo tracehound --severity_threshold=HIGH

# Run without failing the build
qodo tracehound --fail_on_violations=false

# Combine options
qodo tracehound --language=java --severity_threshold=CRITICAL --fail_on_violations=true
```

## Configuration

### Agent Arguments

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `language` | string | typescript | Primary language to analyze (typescript, python, java, go, rust, csharp) |
| `severity_threshold` | string | MEDIUM | Minimum violation severity to report (CRITICAL, HIGH, MEDIUM, LOW) |
| `fail_on_violations` | boolean | true | Exit with code 1 if violations found |

### Config File Structure

The `observe-config.json` file defines your observability contracts:

```json
{
  "metadata": {
    "language": "typescript"
  },
  "contracts": [
    {
      "id": "unique-contract-id",
      "name": "Descriptive Name",
      "enabled": true,
      "code_flow": [
        {
          "layer": "controller|service|dal|middleware",
          "file_pattern": "path/to/file.ts",
          "signals": ["logging", "error_handling", "tracing", "metrics"]
        }
      ]
    }
  ]
}
```

## How It Works

### Execution Flow

**PHASE 1: CONFIG VALIDATION**
1. Checks if `observe-config.json` exists
2. If not found, creates template config from `observability-template.json`
3. Validates config structure and required fields
4. Validates language is supported
5. Parses and stores contracts

**PHASE 2: PATTERN INITIALIZATION**

Initializes language-specific observability patterns based on the configured language. The agent has built-in knowledge of logging, error handling, tracing, and metrics patterns for each supported language.

**PHASE 3: CONTRACT VERIFICATION**

For each enabled contract:
1. Verifies each code flow layer exists
2. Reads file content once per layer
3. Scans for all required observability signals
4. Flags missing signals as violations
5. Assigns severity based on layer criticality

**PHASE 4: REPORT GENERATION**
1. Aggregates all violations
2. Calculates compliance score
3. Generates prioritized recommendations
4. Outputs structured JSON report

## Use Cases

### Pre-Deployment Checks
Verify observability coverage before deploying to production. Catch missing instrumentation in CI/CD.

### API Monitoring Standards
Enforce organization-wide observability standards for critical API endpoints.

### Incident Prevention
Identify gaps in logging and error handling before they cause blind spots in production.

### Refactoring Validation
Ensure observability isn't lost during code refactoring or feature additions.

### Team Onboarding
Help new team members understand what observability signals are expected in the codebase.

## Tools Used

- **Filesystem**: Config loading and file content reading
- **Ripgrep**: Efficient pattern matching for signal detection
- **Git**: Repository context and file discovery

## Severity Levels

Violations are assigned severity based on the layer and missing signal type:

- **CRITICAL**: Missing error handling in any layer, missing logging in DAL
- **HIGH**: Missing logging in controller/service, missing metrics in service
- **MEDIUM**: Missing tracing in any layer, missing metrics in controller
- **LOW**: Optional signals or less critical combinations

## Output Format

The agent outputs a structured JSON report:

```json
{
  "report_metadata": {
    "generated_at": "2025-10-17T10:30:00Z",
    "project_root": "/path/to/project",
    "language": "typescript",
    "config_file": "observe-config.json",
    "execution_time_ms": 1234
  },
  "summary": {
    "total_contracts_analyzed": 3,
    "total_endpoints_verified": 3,
    "overall_compliance_score": 85.5,
    "violations_by_severity": {
      "CRITICAL": 0,
      "HIGH": 2,
      "MEDIUM": 4,
      "LOW": 1
    }
  },
  "violations": [
    {
      "contract_id": "create-order",
      "contract_name": "POST /api/orders",
      "severity": "HIGH",
      "layer": "service",
      "file_pattern": "src/services/orderService.ts",
      "signal_type": "logging",
      "file": "src/services/orderService.ts",
      "line": 45,
      "issue": "Missing logging in orderService.ts service layer",
      "recommendation": "Add logger.info() or logger.error() calls to track order processing"
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "type": "critical_gap",
      "target": "Error Handling",
      "recommendation": "Add try-catch blocks in all service layers",
      "impact": "Prevents silent failures and improves debugging"
    }
  ],
  "warnings": [],
  "success": true
}
```

## Error Handling

TraceHound handles errors gracefully:
- Continues analysis if config file has warnings
- Logs tool failures as warnings
- Proceeds with partial results if some contracts fail
- Returns success with warnings rather than failing entirely
- Creates helpful template if config is missing

## Integration

### GitHub Actions

```yaml
- name: Check Observability
  run: |
    npm install -g @qodo/command
    qodo tracehound --severity_threshold=HIGH
```

### GitLab CI

```yaml
observability-check:
  script:
    - npm install -g @qodo/command
    - qodo tracehound --language=typescript
```

### Jenkins

```groovy
stage('Observability') {
  steps {
    sh 'qodo tracehound --fail_on_violations=true'
  }
}
```

## Support

For issues or questions about the TraceHound agent, please refer to the project documentation or create an issue in the repository.