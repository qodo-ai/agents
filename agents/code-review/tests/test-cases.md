# Test Cases for Code Review Agent

This document outlines test scenarios for validating the Code Review Agent functionality.

## Test Categories

### 1. Security Vulnerability Detection

#### Test Case 1.1: SQL Injection
- **Input**: Code with direct string concatenation in SQL queries
- **Expected**: Critical severity issue detected
- **File**: `sample-input/sql-injection.diff`
- **Expected Output**: `expected-output/sql-injection.json`

#### Test Case 1.2: XSS Vulnerability
- **Input**: Code with unescaped user input in HTML output
- **Expected**: High severity security issue
- **File**: `sample-input/xss-vulnerability.diff`
- **Expected Output**: `expected-output/xss-vulnerability.json`

#### Test Case 1.3: Hardcoded Secrets
- **Input**: Code with API keys or passwords in source
- **Expected**: Critical security issue
- **File**: `sample-input/hardcoded-secrets.diff`
- **Expected Output**: `expected-output/hardcoded-secrets.json`

### 2. Performance Issues

#### Test Case 2.1: Inefficient Algorithm
- **Input**: Code with O(n²) complexity that could be O(n)
- **Expected**: Medium/High performance issue
- **File**: `sample-input/inefficient-algorithm.diff`
- **Expected Output**: `expected-output/inefficient-algorithm.json`

#### Test Case 2.2: Memory Leak
- **Input**: Code with potential memory leaks
- **Expected**: High severity performance issue
- **File**: `sample-input/memory-leak.diff`
- **Expected Output**: `expected-output/memory-leak.json`

### 3. Code Quality Issues

#### Test Case 3.1: Code Duplication
- **Input**: Duplicated code blocks
- **Expected**: Medium maintainability issue
- **File**: `sample-input/code-duplication.diff`
- **Expected Output**: `expected-output/code-duplication.json`

#### Test Case 3.2: Complex Function
- **Input**: Function with high cyclomatic complexity
- **Expected**: Medium maintainability issue
- **File**: `sample-input/complex-function.diff`
- **Expected Output**: `expected-output/complex-function.json`

### 4. Best Practices Violations

#### Test Case 4.1: Missing Error Handling
- **Input**: Code without proper error handling
- **Expected**: Medium severity issue
- **File**: `sample-input/missing-error-handling.diff`
- **Expected Output**: `expected-output/missing-error-handling.json`

#### Test Case 4.2: Inconsistent Naming
- **Input**: Code with inconsistent naming conventions
- **Expected**: Low severity style issue
- **File**: `sample-input/inconsistent-naming.diff`
- **Expected Output**: `expected-output/inconsistent-naming.json`

### 5. Configuration Tests

#### Test Case 5.1: Severity Threshold Filtering
- **Input**: Mixed severity issues
- **Command**: `--severity_threshold=high`
- **Expected**: Only high and critical issues reported

#### Test Case 5.2: Focus Area Filtering
- **Input**: Mixed category issues
- **Command**: `--focus_areas=security`
- **Expected**: Only security-related issues reported

#### Test Case 5.3: File Exclusion
- **Input**: Issues in test files
- **Command**: `--exclude_files="*.test.js"`
- **Expected**: Test file issues excluded

### 6. Integration Tests

#### Test Case 6.1: Large Diff Processing
- **Input**: Large diff with 100+ files
- **Expected**: Successful processing within reasonable time
- **Performance**: < 30 seconds for analysis

#### Test Case 6.2: Binary File Handling
- **Input**: Diff containing binary files
- **Expected**: Binary files skipped gracefully

#### Test Case 6.3: Empty Diff
- **Input**: Empty or no-change diff
- **Expected**: Clean output with no issues

### 7. Output Format Tests

#### Test Case 7.1: JSON Schema Validation
- **Input**: Any valid code review
- **Expected**: Output matches defined JSON schema
- **Validation**: All required fields present

#### Test Case 7.2: Suggestion Generation
- **Input**: Code with improvement opportunities
- **Command**: `--include_suggestions=true`
- **Expected**: Actionable suggestions provided

### 8. Error Handling Tests

#### Test Case 8.1: Invalid Git Repository
- **Input**: Run in non-git directory
- **Expected**: Graceful error message

#### Test Case 8.2: Invalid Target Branch
- **Input**: `--target_branch=nonexistent`
- **Expected**: Clear error about missing branch

#### Test Case 8.3: Network Connectivity Issues
- **Input**: Simulate network failure
- **Expected**: Appropriate error handling and retry logic

## Test Execution

### Manual Testing

```bash
# Run all test cases
./run-tests.sh

# Run specific category
./run-tests.sh security

# Run single test case
./run-tests.sh sql-injection
```

### Automated Testing

```bash
# CI/CD pipeline test
npm test

# Performance benchmarks
npm run benchmark

# Integration tests
npm run test:integration
```

## Test Data Management

### Sample Input Files
- Located in `sample-input/` directory
- Each test case has corresponding `.diff` file
- Files contain realistic code changes

### Expected Output Files
- Located in `expected-output/` directory
- JSON files with expected agent responses
- Include all required schema fields

### Test Validation

```javascript
// Example validation script
const validateOutput = (actual, expected) => {
  // Validate JSON schema
  assert(validateSchema(actual));
  
  // Check issue count
  assert.equal(actual.summary.total_issues, expected.summary.total_issues);
  
  // Validate severity distribution
  assert.equal(actual.summary.critical_issues, expected.summary.critical_issues);
  
  // Check specific issues
  expected.issues.forEach(expectedIssue => {
    const actualIssue = actual.issues.find(i => 
      i.file === expectedIssue.file && 
      i.line === expectedIssue.line
    );
    assert(actualIssue, `Missing expected issue: ${expectedIssue.title}`);
    assert.equal(actualIssue.severity, expectedIssue.severity);
  });
};
```

## Performance Benchmarks

### Response Time Targets
- Small diff (< 10 files): < 5 seconds
- Medium diff (10-50 files): < 15 seconds
- Large diff (50+ files): < 30 seconds

### Accuracy Metrics
- Security issue detection: > 95%
- Performance issue detection: > 85%
- False positive rate: < 10%

## Continuous Testing

### Regression Tests
- Run on every commit
- Validate against known good outputs
- Performance regression detection

### Quality Gates
- All tests must pass for release
- Performance benchmarks must be met
- Security test coverage > 90%