# The Undertaker - Dead Code Detection Agent

Find unused functions, classes, variables, imports, and unreachable code with confidence scoring across your repository.

## Overview

The Undertaker is a reliable dead code detection agent that identifies unused code elements using static analysis. It provides deterministic confidence-based scoring to help you safely remove dead code while minimizing false positives.

## Features

- **Comprehensive Detection**: Identifies unused functions, classes, methods, variables, imports, types, enums, and unreachable code
- **Multi-Language Support**: Analyzes multiple programming languages
- **Confidence Scoring**: Deterministic scoring (50-100%) based on reference counts and export status
- **Safe Analysis**: Read-only static analysis that never modifies your code
- **Unreachable Code Detection**: Finds code after return/throw/break statements
- **Export-Aware**: Distinguishes between private and exported/public code
- **Detailed Reporting**: JSON output with actionable findings and reasoning

## Quick Start

### Basic Usage

```bash
# Run default analysis with 70% confidence threshold
qodo undertaker

# Use custom confidence threshold
qodo undertaker --min_confidence=80

# Include test files in analysis
qodo undertaker --include_tests=true

# Use both options together
qodo undertaker --min_confidence=85 --include_tests=true
```

## Configuration

The agent accepts the following parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `min_confidence` | number | 70 | Minimum confidence threshold (50-100). Only results meeting or exceeding this threshold are included. |
| `include_tests` | boolean | false | Whether to include test files in the dead code analysis. |

## How It Works

### Analysis Process

1. **Project Discovery**: Scans source files while excluding generated and vendor directories
2. **Definition Detection**: Identifies function/class/variable/import definitions using language-specific patterns
3. **Reference Counting**: Counts actual usage of each identifier across the codebase (excluding its definition)
4. **Export Analysis**: Determines whether code is exported/public, which affects confidence scoring
5. **Unreachable Code Detection**: Finds code after terminating statements (return/throw/break)
6. **Confidence Scoring**: Applies deterministic rules to generate confidence scores

### Confidence Scoring

The agent uses the following rules to calculate confidence scores:

| Condition | Confidence | Tier |
|-----------|-----------|------|
| No references + not exported | 100% | Very High |
| No references + exported | 90% | Very High |
| 1 reference + not exported | 75% | High |
| 1 reference + exported | 70% | High |
| 2+ references | 60% or lower | Medium |
| Unreachable code | 100% | Very High |

## Output Format

The agent returns a JSON object with the following structure:

```json
{
  "summary": {
    "total_files_scanned": 42,
    "total_dead_code_items": 5,
    "confidence_counts": {
      "very_high": 3,
      "high": 1,
      "medium": 1
    },
    "estimated_lines_removable": 127
  },
  "dead_code_items": [
    {
      "identifier": "unusedFunction",
      "type": "function",
      "location": "src/utils.ts:42-55",
      "confidence_score": 100,
      "reference_count": 0,
      "is_exported": false,
      "reasoning": "Function is not referenced anywhere in the codebase and is not exported"
    }
  ],
  "warnings": [],
  "success": true
}
```

## Interpreting Results

- **Very High Confidence (90-100%)**: Safe to remove. These are unused code elements with no references and typically not exported.
- **High Confidence (70-89%)**: Likely safe to remove. Usually has minimal references or is exported but not used.
- **Medium Confidence (50-69%)**: Exercise caution. Has some references but may still be dead code. Review before removing.

## Use Cases

### Clean Up Your Codebase
Remove unused code that accumulates over time as features are refactored or deprecated.

### Pre-Refactoring Analysis
Identify what can be safely removed before major refactoring efforts.

### Code Review
Use in your CI/CD pipeline to flag potential dead code during code reviews.

### Dependency Reduction
Identify unused exports that can be kept private or removed entirely.

## Tools Used

- **Git**: Version control operations
- **Filesystem**: Directory and file traversal
- **Ripgrep**: Efficient pattern matching and searching

## Error Handling

The agent handles errors gracefully:
- If tools fail, analysis continues with warnings
- Falls back to filesystem reading if pattern matching fails
- Returns `success: true` with warnings rather than failing entirely
- Handles cross-platform compatibility issues automatically

## Technical Details

The agent uses ripgrep for efficient cross-repository searching with language-specific patterns. It filters out comments and strings to minimize false positives and deduplicates results for accuracy.

## Limitations

- Static analysis only - cannot detect runtime dead code
- May have false negatives if code is referenced dynamically
- External library references may be missed if not directly imported in source files
- Consider running multiple times with different `min_confidence` values for comprehensive analysis

## Examples

### Example 1: Basic Analysis

```bash
qodo undertaker
```

Scans the repository and returns all dead code with confidence >= 70%.

### Example 2: High Confidence Only

```bash
qodo undertaker --min_confidence=90
```

Returns only the most reliable dead code detections (90-100% confidence).

### Example 3: Including Tests

```bash
qodo undertaker --include_tests=true
```

Includes test files in the analysis, which is useful for identifying unused test helpers or fixtures.

## Integration

The JSON output can be easily integrated into:
- CI/CD pipelines for automated reporting
- Code review tools
- Custom analysis scripts

## Best Practices

1. Start with the default `min_confidence=70` threshold
2. Review "Very High" confidence items first as candidates for removal
3. Use version control to safely remove dead code in isolated commits
4. Run the agent periodically to maintain code quality

## Support

For issues or questions about the Undertaker agent, please refer to the project documentation or create an issue in the repository.