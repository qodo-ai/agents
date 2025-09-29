# Code Quality Podman Pipeline Agent

## Overview

This agent automates comprehensive code quality checks using Podman containers, providing consistent, scalable quality assurance across different environments. It orchestrates multiple quality tools in containerized pipelines to ensure code meets security, maintainability, and performance standards.

## Features

- **Multi-Language Support**: Supports 12+ programming languages including Python, JavaScript, TypeScript, Java, Go, Rust, C++, C#, PHP, Ruby, Kotlin, and Scala
- **Containerized Execution**: Uses Podman containers for consistent, isolated quality checks across environments
- **Comprehensive Analysis**: Integrates static analysis, security scanning, complexity analysis, dependency checking, and performance profiling
- **Parallel Processing**: Executes quality checks in parallel for optimal performance
- **Quality Gates**: Configurable thresholds and blocking conditions for automated quality enforcement
- **Multiple Report Formats**: Generates reports in JSON, XML, HTML, SARIF, JUnit, and SonarQube formats
- **CI/CD Integration**: Ready-to-use templates for GitHub Actions, GitLab CI, Jenkins, Azure DevOps, and more
- **Security-First**: Built-in SAST/DAST scanning with industry-standard security tools
- **Monitoring & Alerting**: Continuous quality metrics tracking with dashboard integration

## Requirements

- **Podman** >= 4.0
- **Git** (for repository analysis)
- **Bash** (for pipeline execution)
- Container registry access (Docker Hub by default)

## Supported Quality Tools

### Static Analysis
- **SonarQube** - Comprehensive code quality analysis
- **CodeClimate** - Maintainability and complexity analysis
- **ESLint** - JavaScript/TypeScript linting
- **Pylint** - Python code analysis
- **RuboCop** - Ruby style guide enforcement
- **golangci-lint** - Go linting suite
- **Clippy** - Rust linting and suggestions

### Security Scanners
- **Bandit** - Python security vulnerability scanner
- **Semgrep** - Multi-language static analysis security tool
- **CodeQL** - GitHub's semantic code analysis
- **Trivy** - Container and dependency vulnerability scanner
- **Snyk** - Dependency vulnerability management
- **OWASP Dependency Check** - Known vulnerability identification

### Code Formatters
- **Prettier** - JavaScript/TypeScript/JSON/YAML/Markdown formatting
- **Black** - Python code formatter
- **gofmt** - Go code formatter
- **rustfmt** - Rust code formatter

### Complexity & Performance Analyzers
- **Radon** - Python complexity analysis
- **JSComplexity** - JavaScript complexity metrics
- **gocyclo** - Go cyclomatic complexity
- **py-spy** - Python performance profiling
- **clinic.js** - Node.js performance analysis

## Usage

### Basic Usage

```bash
# Auto-detect language and run all applicable quality checks
qodo code_quality_podman

# Specify language and tools
qodo code_quality_podman --language=python --quality_tools=pylint,bandit,black

# Security-focused scan
qodo code_quality_podman --quality_tools=semgrep,bandit,trivy --severity_threshold=high
```

### Advanced Configuration

```bash
# Comprehensive scan with custom settings
qodo code_quality_podman \
  --language=javascript \
  --quality_tools=eslint,semgrep,prettier \
  --severity_threshold=medium \
  --parallel_execution=true \
  --report_format=json,html \
  --exclude_paths=node_modules,dist \
  --cache_enabled=true
```

### CI/CD Integration

```bash
# Production pipeline with notifications
qodo code_quality_podman \
  --language=auto \
  --quality_tools=all \
  --severity_threshold=medium \
  --report_format=sarif \
  --notification_webhook=$WEBHOOK_URL
```

## Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `language` | string | No | "auto" | Programming language (auto, python, javascript, java, go, rust, etc.) |
| `quality_tools` | string | No | "all" | Comma-separated list of quality tools to include |
| `severity_threshold` | string | No | "medium" | Minimum severity level to fail pipeline (low, medium, high, critical) |
| `container_registry` | string | No | "docker.io" | Container registry for quality tool images |
| `parallel_execution` | boolean | No | true | Run quality checks in parallel for faster execution |
| `cache_enabled` | boolean | No | true | Enable caching for faster subsequent runs |
| `report_format` | string | No | "json" | Output format for quality reports (json, xml, html, sarif) |
| `exclude_paths` | string | No | - | Comma-separated list of paths to exclude from quality checks |
| `custom_rules` | string | No | - | Path to custom quality rules configuration file |
| `notification_webhook` | string | No | - | Webhook URL for quality check notifications |

## Pipeline Stages

The agent executes quality checks through the following stages:

1. **Setup** - Initialize environment and pull container images
2. **Lint** - Code style and syntax checking (parallel)
3. **Security** - Security vulnerability scanning (parallel)
4. **Complexity** - Code complexity analysis (parallel)
5. **Dependencies** - Dependency vulnerability scanning (parallel)
6. **Performance** - Performance analysis
7. **Report** - Generate consolidated reports

## Quality Gates

Default quality gates ensure code meets minimum standards:

| Gate | Threshold | Blocking | Description |
|------|-----------|----------|-------------|
| Critical Security Issues | 0 | ✅ | No critical security vulnerabilities allowed |
| High Security Issues | 2 | ✅ | Maximum 2 high severity security issues |
| Code Coverage | 80% | ❌ | Minimum 80% code coverage recommended |
| Complexity Score | 10 | ❌ | Maximum cyclomatic complexity of 10 |
| Maintainability Index | 70 | ❌ | Minimum maintainability index of 70 |
| Dependency Vulnerabilities | 5 | ✅ | Maximum 5 dependency vulnerabilities |

## Output Formats

The agent supports multiple output formats for integration with different tools:

- **JSON** - Machine-readable format for API integration
- **XML** - Compatible with legacy systems
- **HTML** - Human-readable reports with visualizations
- **SARIF** - Static Analysis Results Interchange Format
- **JUnit** - Test result format for CI/CD systems
- **SonarQube** - Direct integration with SonarQube platforms

## CI/CD Integration Examples

### GitHub Actions

```yaml
name: Code Quality Check
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Code Quality Pipeline
        run: |
          qodo code_quality_podman \
            --language=auto \
            --quality_tools=all \
            --severity_threshold=medium \
            --report_format=sarif \
            --parallel_execution=true
```

### GitLab CI

```yaml
code_quality:
  stage: test
  script:
    - qodo code_quality_podman --language=auto --report_format=json
  artifacts:
    reports:
      codequality: quality-report.json
```

### Jenkins Pipeline

```groovy
pipeline {
    agent any
    stages {
        stage('Code Quality') {
            steps {
                sh '''
                    qodo code_quality_podman \
                      --language=auto \
                      --quality_tools=all \
                      --report_format=junit
                '''
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'quality-results.xml'
                }
            }
        }
    }
}
```

## Monitoring & Dashboards

The agent provides comprehensive monitoring capabilities:

### Metrics Collected
- Pipeline execution time
- Quality score trends
- Security issues count
- Code coverage percentage
- Dependency vulnerabilities
- Complexity metrics

### Available Dashboards
- **Quality Trends Dashboard** - Historical quality metrics
- **Security Metrics Dashboard** - Security vulnerability tracking
- **Performance Metrics Dashboard** - Performance analysis results
- **Team Quality Scorecard** - Team-level quality comparisons

## Integration Platforms

### Quality Platforms
- SonarQube
- CodeClimate
- Codacy
- DeepSource

### Security Platforms
- Snyk
- WhiteSource
- Veracode
- Checkmarx

### Notification Channels
- Slack
- Microsoft Teams
- Email
- Webhook
- PagerDuty

## Language-Specific Configurations

### Python
```bash
qodo code_quality_podman \
  --language=python \
  --quality_tools=pylint,bandit,black,radon \
  --custom_rules=.pylintrc
```

### JavaScript/TypeScript
```bash
qodo code_quality_podman \
  --language=javascript \
  --quality_tools=eslint,prettier,semgrep \
  --custom_rules=.eslintrc.json
```

### Go
```bash
qodo code_quality_podman \
  --language=go \
  --quality_tools=golangci-lint,gofmt,gocyclo \
  --severity_threshold=high
```

### Java
```bash
qodo code_quality_podman \
  --language=java \
  --quality_tools=sonarqube,semgrep \
  --report_format=sonarqube
```

## Best Practices

### Performance Optimization
- Enable caching for faster subsequent runs
- Use parallel execution for independent checks
- Exclude unnecessary paths (node_modules, build directories)
- Use specific tool selection instead of "all" for faster execution

### Security Configuration
- Set appropriate severity thresholds for your project
- Configure blocking quality gates for critical issues
- Regularly update container images for latest security patches
- Use custom rules for organization-specific security requirements

### CI/CD Integration
- Cache container images between pipeline runs
- Use appropriate report formats for your CI/CD system
- Configure notifications for quality gate failures
- Set up quality trend monitoring

## Troubleshooting

### Common Issues

**Container Pull Failures**
```bash
# Check Podman connectivity
podman pull hello-world

# Use alternative registry
qodo code_quality_podman --container_registry=quay.io
```

**Permission Issues**
```bash
# Ensure Podman is properly configured
podman system info

# Check file permissions
ls -la /path/to/project
```

**Quality Tool Failures**
```bash
# Run with specific tools to isolate issues
qodo code_quality_podman --quality_tools=pylint

# Check tool-specific logs
podman logs <container_id>
```

**Memory/Resource Issues**
```bash
# Disable parallel execution
qodo code_quality_podman --parallel_execution=false

# Exclude large directories
qodo code_quality_podman --exclude_paths=node_modules,vendor
```

## Contributing

When contributing to this agent:

1. Follow containerization best practices
2. Ensure new tools are properly integrated with existing pipeline stages
3. Update quality gates and thresholds documentation
4. Test with multiple programming languages
5. Maintain backward compatibility with existing configurations

## Related Agents

- **[Code Review](../code-review/)** - Automated code review and feedback
- **[License Compliance](../license-compliance/)** - License compliance checking
- **[Package Health Reviewer](../package-health-reviewer/)** - Package dependency health analysis
- **[OpenSSF Scorecard Fixer](../openssf-scorecard-fixer/)** - Security scorecard improvements

---

**Built with ❤️ for consistent, automated code quality assurance**
