# Basic Usage Examples

This document provides basic usage examples for the Code Review Agent.

## Simple Code Review

Review current changes against the main branch:

```bash
qodo code_review
```

## Review Against Specific Branch

Compare changes against a different target branch:

```bash
qodo code_review --target_branch=develop
```

## Focus on Security Issues

Review only security-related issues with high severity:

```bash
qodo code_review --focus_areas=security --severity_threshold=high
```

## Include Improvement Suggestions

Get detailed improvement suggestions along with issue detection:

```bash
qodo code_review --include_suggestions=true
```

## Exclude Specific Files

Skip test files and generated code from review:

```bash
qodo code_review --exclude_files="*.test.js,*.spec.ts,dist/*,build/*"
```

## Comprehensive Review

Run a comprehensive review with all options:

```bash
qodo code_review \
  --target_branch=main \
  --severity_threshold=medium \
  --focus_areas=security,performance,maintainability \
  --include_suggestions=true \
  --exclude_files="*.test.js,*.spec.ts"
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
  "suggestions": [],
  "approved": true,
  "requires_changes": false
}
```

### Review with Issues Found

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